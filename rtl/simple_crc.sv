/**
Copyright (c) 2022, Qianfeng (Clark) Shen
All rights reserved.

This source code is licensed under the BSD-style license found in the
LICENSE file in the root directory of this source tree.
 * @author Qianfeng (Clark) Shen
 * @email qianfeng.shen@gmail.com
 * @create date 2022-03-18 13:57:54
 * @modify date 2022-03-18 13:57:54
 */

//this is a simplified version of https://github.com/QianfengClarkShen/Tbps_CRC/blob/main/rtl/tbps_crc.sv

`timescale 1ns / 1ps
module simple_crc # (
    parameter int DWIDTH = 512,
    parameter int CRC_WIDTH = 16,
    parameter CRC_POLY = 16'hda5f,
    parameter INIT = 16'b0,
    parameter XOR_OUT = 16'b0,
    parameter bit REFIN = 1'b0,
    parameter bit REFOUT = 1'b0
) (
    input logic clk,
    input logic rst,
    input logic [DWIDTH-1:0] s_axis_tdata,
    input logic s_axis_tvalid,
    output logic s_axis_tready,
    output logic [CRC_WIDTH-1:0] crc_tdata,
    output logic crc_tvalid,
    input logic crc_tready
);
    `include "crc.svh"
    localparam bit [CRC_WIDTH-1:0][CRC_WIDTH+DWIDTH-1:0] UNI_TABLE = gen_unified_table();
    localparam bit [CRC_WIDTH-1:0][CRC_WIDTH-1:0] CRC_TABLE = gen_crc_table(UNI_TABLE);
    localparam bit [CRC_WIDTH-1:0][DWIDTH-1:0] DATA_TABLE = gen_data_table(UNI_TABLE);

    //internal wire
    logic [CRC_WIDTH-1:0] crc_int;

    //refin-refout conversion
    logic [DWIDTH-1:0] din_refin;
    logic [CRC_WIDTH-1:0] crc_refout;

    always_comb begin
    //REFIN logic
        if (REFIN)
            din_refin = {<<{s_axis_tdata}};
        else
            din_refin = {<<8{s_axis_tdata}};
    end

    always_comb begin
    //calculate crc
        crc_int = '0;
        for (int i = 0; i < CRC_WIDTH; i++) begin
            for (int j = 0; j < CRC_WIDTH; j++)
                if (CRC_TABLE[i][j])
                    crc_int[i] = crc_int[i] ^ INIT[j];
            for (int j = 0; j < DWIDTH; j++)
                if (DATA_TABLE[i][j])
                    crc_int[i] = crc_int[i] ^ din_refin[j];
        end
    end

//refout logic
    always_comb begin
        if (REFOUT)
            crc_refout = {<<{crc_int}};
        else
            crc_refout = crc_int;
    end

//output the result
    always_ff @(posedge clk) begin
        if (rst) begin
            crc_tdata <= '0;
            crc_tvalid <= '0;
        end
        else if (crc_tready) begin
            if (s_axis_tvalid)
                crc_tdata <= crc_refout ^ XOR_OUT;
            crc_tvalid <= s_axis_tvalid;
        end
    end
    assign s_axis_tready = crc_tready;
endmodule