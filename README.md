# Static Hash System

A complete hardware-software system for static hashing of ASCII strings to unique IDs using multiple CRC functions. The system includes a Python-based hash table generator (software) and a SystemVerilog-based hash lookup engine (hardware RTL).

## Overview

This project implements a static hash system that maps ASCII strings to unique numerical IDs with zero collisions. The software component generates optimized hash tables using multiple CRC polynomials, while the hardware component provides high-speed lookup functionality for real-time applications.

### Key Features

- **Zero-collision guarantee**: Multi-layer CRC approach eliminates hash conflicts
- **Configurable ID ranges**: Support from 8-bit to 30-bit CRCs (256 to 1+ billion IDs)
- **Research-backed polynomials**: Uses Philip Koopman's optimal CRC polynomials
- **Hardware acceleration**: SystemVerilog RTL for high-speed lookups
- **AXI interfaces**: Industry-standard AXI-Stream and AXI-Lite connectivity
- **Complete simulation environment**: Cocotb-based verification framework

## System Architecture

```
Input Strings → Python Generator → Binary Hash Table → Hardware RTL → Unique IDs
              (Software Phase)    (Interface)         (Hardware Phase)
```

The system operates in two phases:
1. **Offline Generation**: Python scripts process string lists and generate binary hash tables
2. **Runtime Lookup**: Hardware RTL performs real-time string-to-ID mapping

## Project Structure

```
├── py/                          # Software Components
│   ├── static_hash.py           # Main hash table generator
│   └── crc_polynomials.py       # CRC polynomial database (Koopman's)
├── rtl/                         # Hardware Components
│   ├── static_hash.sv           # Top-level hash lookup engine
│   ├── static_hash_axil.sv      # AXI-Lite configuration interface
│   ├── simple_crc.sv           # Parallel CRC calculation units
│   ├── simple_dp_ram.sv        # Dual-port memory for hash tables
│   ├── crc_polynomials.svh     # SystemVerilog CRC definitions
│   └── crc.svh                 # CRC calculation functions
├── sim/                         # Simulation Environment
│   ├── run_test.py             # Cocotb test framework
│   ├── tb.sv                   # SystemVerilog testbench
│   ├── CMakeLists.txt          # Build system configuration
│   ├── static_hash.py          # Simulation model
│   └── crc_polynomials.py      # Simulation CRC database
├── test/                        # Test Data
│   ├── generate_*.py           # Test data generators
│   └── test_symbols*.txt       # Sample string datasets
└── README.md                    # This file
```

## Software Component (Python)

### Usage

```bash
# Basic usage (default: 32K IDs, auto CRC width selection)
python py/static_hash.py input.txt

# Specify maximum IDs (automatically selects optimal CRC width)
python py/static_hash.py input.txt --max-ids 65536    # Uses CRC-16
python py/static_hash.py input.txt --max-ids 1000000  # Uses CRC-20

# Hexadecimal input format
python py/static_hash.py hex_input.txt --format hex

# Custom output file
python py/static_hash.py input.txt -o custom_table.bin
```

### Algorithm

The software uses a sophisticated multi-layer approach:

1. **CRC Width Selection**: Automatically selects optimal CRC width based on required ID range
2. **Layer Assignment**: Assigns strings to CRC functions layer by layer to eliminate conflicts
3. **Binary Generation**: Creates memory-mapped binary hash table for hardware

### Output Format

The generator produces:
- **Binary hash table**: Memory-mapped format for direct hardware loading
- **Text report**: Human-readable mapping statistics
- **Verification data**: Hash table contents for simulation validation

## Hardware Component (SystemVerilog)

### Architecture

The hardware consists of several key modules:

- **static_hash.sv**: Top-level module with AXI interfaces
- **static_hash_axil.sv**: AXI-Lite slave for hash table configuration
- **simple_crc.sv**: CRC calculation engines
- **simple_dp_ram.sv**: Simple dual-port memory blocks for hash table storage

### Interfaces

#### AXI-Lite Configuration Interface
- **Purpose**: Load hash tables from software-generated binary files
- **Width**: Configurable based on CRC width
- **Access**: Write-only for table initialization

#### AXI-Stream Input Interface
- **Purpose**: Receive ASCII strings for lookup
- **Data Width**: Configurable
- **Flow Control**: Ready/valid handshaking

#### AXI-Stream Output Interface
- **Purpose**: Output unique IDs for input strings
- **Data Width**: Matches CRC width configuration
- **Latency**: 3 clock cycles (pipeline: input → CRC calc → memory read → output)

### Performance

- **Throughput**: One lookup per clock cycle
- **Latency**: 3 clock cycles per lookup
- **Fmax**: Limited by memory access and CRC calculation, easy to reach 500 MHz on an modern FPGA
- **Parallelism**: Up to 8 parallel CRC engines for conflict resolution

## Simulation and Verification

### Framework

Uses Cocotb (Python-based testbench) with:
- **Verilator**: Fast SystemVerilog simulation
- **CMake**: Build system with dependency checking
- **AXI verification**: Industry-standard AXI VIP components

### Test Environment

```bash
# Build and run simulation
cd sim
mkdir build && cd build
cmake ..
make

# Run specific test
make sim_4k
```

### Dependencies

The simulation environment requires:
- **g++** (≥11.0.0): C++ compiler for Verilator
- **Verilator** (≥5.022): SystemVerilog simulator
- **Python** (≥3.8): Cocotb framework
- **cocotb** (≥1.9.2): Python testbench framework
- **cocotbext-axi**: AXI verification components
- **pycrc**: CRC calculation library

Install Python dependencies:
```bash
pip install cocotb cocotbext-axi pycrc
```

## CRC Polynomial Database

The system uses Philip Koopman's research-backed CRC polynomials, providing optimal error detection properties:

### Supported CRC Widths
- **8-bit**: Up to 256 unique IDs
- **10-bit**: Up to 1,024 unique IDs
- **12-bit**: Up to 4,096 unique IDs
- **14-bit**: Up to 16,384 unique IDs
- **16-bit**: Up to 65,536 unique IDs
- **18-bit**: Up to 262,144 unique IDs
- **20-bit**: Up to 1,048,576 unique IDs
- **22-30-bit**: Up to billions of unique IDs

Each width provides 8 different polynomial options for conflict resolution.

## Example Workflow

1. **Prepare Input**: Create text file with ASCII strings (one per line, max 32 bytes)
   ```
   AAPL
   GOOGL
   MSFT
   TSLA
   ```

2. **Generate Hash Table**: Run Python generator
   ```bash
   python py/static_hash.py stocks.txt --max-ids 1000
   ```

3. **Load Hardware**: Use generated binary in simulation or FPGA
   ```bash
   cd sim/build
   python ../run_test.py --input_file ../../stocks.txt
   ```

4. **Runtime Lookup**: Send strings via AXI-Stream, receive unique IDs

## Applications

- **Financial Trading**: Stock symbol to ID mapping for high-frequency trading
- **Network Processing**: Protocol field hashing for packet classification
- **Database Indexing**: Fast string key to row ID translation
- **Embedded Systems**: Resource-constrained string lookup tables

## Requirements

### Software
- Python 3.9+
- pycrc library

### Hardware Simulation
- Verilator 5.022+
- g++ 11.0+
- CMake 3.16+
- cocotb 1.9.2+
- cocotbext-axi

### Hardware Synthesis
- Any SystemVerilog-compatible synthesis tool
- Configurable memory blocks (simple dual-port RAM)
- AXI interface support
