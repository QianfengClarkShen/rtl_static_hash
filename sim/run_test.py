import glob
import os
import argparse
from pathlib import Path
from typing import List
import random
import itertools

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.regression import TestFactory
from cocotb.runner import get_runner
from cocotb.queue import Queue
from cocotb.utils import get_sim_time
from cocotbext.axi import AxiStreamFrame, AxiStreamBus, AxiStreamSource, AxiStreamMonitor, AxiStreamSink, AxiLiteBus, AxiLiteMaster

from static_hash import StaticHasher

#module name
TOP_MODULE = "tb"

mem_initialized = False

class AXISMonitor:
    def __init__(self, axis_mon: AxiStreamMonitor):
        self.values = Queue[List[int]]()
        self._coro = None
        self.axis_mon = axis_mon
        self._pkt_cnt = 0

    def start(self) -> None:
        """Start monitor"""
        if self._coro is not None:
            raise RuntimeError("Monitor already started")
        self._coro = cocotb.start_soon(self._run())

    def stop(self) -> None:
        """Stop monitor"""
        if self._coro is None:
            raise RuntimeError("Monitor never started")
        self._coro.kill()
        self._coro = None

    def get_pkt_cnt(self) -> int:
        """Get the number of samples"""
        return self._pkt_cnt

    async def _run(self) -> None:
        while True:
            frame = await self.axis_mon.recv()
            #cocotb.log.info(f"Received AXIS frame: tdata={tdata}")
            self.values.put_nowait(frame.tdata)
            self._pkt_cnt += 1

class AXISChecker:
    def __init__(self, dut, source_name, sink_name, clk, rst, check_func):
        self.dut = dut
        self.source_mon = AXISMonitor(AxiStreamMonitor(AxiStreamBus.from_prefix(dut, source_name), clk, rst))
        self.sink_mon = AXISMonitor(AxiStreamSink(AxiStreamBus.from_prefix(dut, sink_name), clk, rst))
        self.check_func = check_func
        self._checker = None

    def start(self) -> None:
        """Starts monitors, model, and checker coroutine"""
        if self._checker is not None:
            raise RuntimeError("Monitor already started")
        self.source_mon.start()
        self.sink_mon.start()
        self._checker = cocotb.start_soon(self._check())

    def stop(self) -> None:
        """Stops everything"""
        if self._checker is None:
            raise RuntimeError("Monitor never started")
        self.source_mon.stop()
        self.sink_mon.stop()
        self._checker.kill()
        self._checker = None

    def is_busy(self) -> bool:
        return self.source_mon.get_pkt_cnt() != self.sink_mon.get_pkt_cnt()

    async def _check(self) -> None:
        while True:
            actual_output = await self.sink_mon.values.get()
            actual_input = await self.source_mon.values.get()
            self.check_func(actual_input, actual_output)

async def unit_test(dut, traffic_rate, backpressure_rate):
    CRC_WIDTH = dut.CRC_WIDTH.value
    input_file = dut.IN_FILE.value.decode('utf-8')
    max_ids = 2**CRC_WIDTH
    static_hash = StaticHasher(max_ids)
    static_hash.process_file(input_file)
    mem = static_hash.hash_table_bin
    hash_table = static_hash.hash_table

    def make_check_func(hash_table):
        table = hash_table
        def check_func(actual_input, actual_output):
            string = actual_input.decode('ascii').rstrip('\x00')
            id = table[string]
            assert int.from_bytes(actual_output, 'little') == id
        return check_func

    check_func = make_check_func(hash_table)

    cocotb.start_soon(Clock(dut.clk, 2, units="ns").start())
    axis_checker = AXISChecker(dut, "sparse_axis", "uuid_axis", dut.clk, dut.rst, check_func)
    axis_checker.start()

    axis_source = AxiStreamSource(AxiStreamBus.from_prefix(dut, "sparse_axis"), dut.clk, dut.rst)
    axis_sink = AxiStreamSink(AxiStreamBus.from_prefix(dut, "uuid_axis"), dut.clk, dut.rst)
    axil_source = AxiLiteMaster(AxiLiteBus.from_prefix(dut, "cfg_axil"), dut.clk, dut.rst)

    axis_source.set_pause_generator(itertools.cycle([random.random() >= traffic_rate for _ in range(10000000)]))
    axis_sink.set_pause_generator(itertools.cycle([random.random() < backpressure_rate for _ in range(10000000)]))

    dut._log.info("Initialize and reset model")

    dut.rst.value = 0
    await ClockCycles(dut.clk, 20)
    dut.rst.value = 1
    await ClockCycles(dut.clk, 20)
    dut.rst.value = 0
    await RisingEdge(dut.clk)
    #out of reset
    dut._log.info("Test Started")

    dut._log.info("Write static hash tables in to internal memories")
    global mem_initialized
    if not mem_initialized:
        mem_initialized = True
        for i in range(8*max_ids):
            content_to_write = mem[i*4:(i+1)*4]
            await axil_source.write(i*4, content_to_write)
    dut._log.info("Start symbol->uuid mapping test")
    lines = []
    with open(input_file, 'r', encoding='ascii') as f:
        lines = f.readlines()
    for line in lines:
        text_bytes = line.strip().encode('ascii')
        await axis_source.send(AxiStreamFrame(text_bytes))
    #now = get_sim_time(units="us")
    while True:
        await RisingEdge(dut.clk)
        if not axis_checker.is_busy() and axis_source.idle():
            break
    await ClockCycles(dut.clk, 20)
    dut._log.info("Test Finished")

def test_runner():
    global input_file
    sim = os.getenv("SIM", "verilator")

    sim_path = Path(__file__).resolve().parent
    proj_path = Path(__file__).resolve().parent.parent / "rtl"
    module_name = Path(__file__).stem

    verilog_sources = list(proj_path.rglob("*.sv")) + list(proj_path.rglob("*.v")) + [sim_path / "tb.sv"]

    if not input_file or not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    lines = []
    with open(input_file, 'r', encoding='ascii') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    CRC_WIDTH = (len(lines)-1).bit_length()
    DATA_WIDTH = max(map(len, lines), default=0)*8
    IN_FILE = f'"{input_file}"'

    parameters = {
        "DATA_WIDTH": DATA_WIDTH,
        "CRC_WIDTH": CRC_WIDTH,
        "IN_FILE": IN_FILE
    }

    runner = get_runner(sim)

    runner.build(
        hdl_toplevel=TOP_MODULE,
        verilog_sources=verilog_sources,
        includes=[proj_path],
        parameters=parameters,
        waves=True,
        build_args=["-Wno-WIDTHEXPAND","-Wno-UNOPTFLAT","+1800-2012ext+sv"]
    )

    runner.test(
        hdl_toplevel=TOP_MODULE,
        hdl_toplevel_lang="verilog",
        waves=True,
        test_module=module_name
    )


if cocotb.SIM_NAME:
    factory = TestFactory(unit_test)
    factory.add_option("traffic_rate", [0.1, 0.5, 0.9, 1])
    factory.add_option("backpressure_rate", [0, 0.1, 0.5,0.9])
    factory.generate_tests()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Static Hash Cocotb simulation")
    parser.add_argument("--input_file", type=Path, help="Path to the input file")
    args = parser.parse_args()

    input_file = args.input_file
    test_runner()