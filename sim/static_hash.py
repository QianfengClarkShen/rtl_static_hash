#!/usr/bin/env python3
"""
Static Hash Script for ASCII Strings using Multiple CRC Functions

This script maps ASCII strings to unique IDs using multiple CRC hash functions
to minimize conflicts through a layered approach. Supports configurable ID ranges
with automatic CRC polynomial selection using high-quality polynomials from
Philip Koopman's CRC polynomial database.

Key Features:
- Configurable ID ranges (8-bit to 32-bit CRCs)
- High-quality CRC polynomials from Koopman's database
- Automatic CRC width selection (even-bit widths only)
- Multi-layer conflict resolution strategy
- Support for ASCII text and hexadecimal input formats
- Efficient table-driven CRC calculation using pycrc library

CRC Polynomials Used:
- 8-bit CRCs for up to 256 IDs
- 10-bit CRCs for up to 1,024 IDs
- 12-bit CRCs for up to 4,096 IDs
- 14-bit CRCs for up to 16,384 IDs
- 16-bit CRCs for up to 65,536 IDs
- 18-bit CRCs for up to 262,144 IDs
- 20-bit CRCs for up to 1,048,576 IDs
- And larger widths as needed...

All polynomials are based on Philip Koopman's extensive research into
optimal CRC polynomials for error detection.
"""

import pycrc.algorithms as crc_algorithms
import sys
import argparse
import math
from collections import defaultdict
from typing import Dict, List, Tuple

# Import CRC polynomials from separate module
from crc_polynomials import KOOPMAN_POLYNOMIALS, get_poly_index

class StaticHasher:
    def __init__(self, max_ids: int = 32768):
        """
        Initialize StaticHasher with configurable ID range.

        Args:
            max_ids: Maximum number of IDs to support (default: 32768 for 15-bit)
        """
        # Round up to power of two
        self.max_ids = 2**((max_ids -1).bit_length())

        # Calculate required CRC width (even numbers only)
        required_bits = int(math.log2(max_ids))
        self.crc_width = required_bits if required_bits % 2 == 0 else required_bits + 1

        if self.crc_width > 30:
            raise ValueError("Maximum supported number of IDs is is 2**30")

        # Use minimum available CRC width if required width is too small
        min_available_width = min(KOOPMAN_POLYNOMIALS.keys())
        if self.crc_width < min_available_width:
            self.crc_width = min_available_width

        self.id_mask = (1 << required_bits) - 1
        self.polynomials = KOOPMAN_POLYNOMIALS[self.crc_width]

        # Initialize CRC calculators
        self.crc_calculators = {}
        for name, (poly, _, reflect_in, xor_in, reflect_out, xor_out) in self.polynomials.items():
            # Create CRC calculator using correct pycrc API
            crc_calc = crc_algorithms.Crc(
                width=self.crc_width,
                poly=poly,
                reflect_in=reflect_in,
                xor_in=xor_in,
                reflect_out=reflect_out,
                xor_out=xor_out
            )
            self.crc_calculators[name] = crc_calc

        if not self.crc_calculators:
            raise ValueError(f"No CRC-{self.crc_width} calculators could be created")
        #hash table in binary format
        self.id_bytes = 4 #4 bytes per entry
        self.hash_table_bin = bytearray(self.id_bytes*8*self.max_ids)
        #human readable hash table
        self.hash_table = {}

    def calculate_crc(self, text: bytes, crc_name: str) -> int:
        """Calculate CRC for given text using specified CRC function"""
        crc_calc = self.crc_calculators[crc_name]
        # Use table_driven method for better performance
        crc_value = crc_calc.table_driven(text)
        # Mask to the configured ID range
        return crc_value & self.id_mask

    def find_conflicts(self, strings: List[bytes], crc_name: str) -> Dict[int, List[bytes]]:
        """Find conflicts for a given CRC function"""
        hash_to_strings = defaultdict(list)

        for string in strings:
            hash_value = self.calculate_crc(string, crc_name)
            hash_to_strings[hash_value].append(string)

        # Return only conflicting entries (hash values with multiple strings)
        conflicts = {k: v for k, v in hash_to_strings.items() if len(v) > 1}
        return conflicts

    def assign_hash_functions(self, strings: List[bytes]) -> Dict[bytes, Tuple[str, int]]:
        """
        Assign CRC functions to strings to minimize conflicts.
        Returns dict mapping string -> (crc_function_name, unique_id)
        """
        result = {}
        remaining_strings = strings.copy()
        next_unique_id = 0  # Counter for unique IDs starting from 0
        for crc_name in self.crc_calculators:
            # Get conflicts for the selected CRC function
            conflicts = self.find_conflicts(remaining_strings, crc_name)

            # Assign only non-conflicting strings to this CRC function
            newly_assigned = set()
            conflicted_strings = set()
            # Collect all strings that have conflicts
            for _, conflicting_strings in conflicts.items():
                for string in conflicting_strings:
                    conflicted_strings.add(string)

            # Assign only strings that don't have any conflicts
            for string in remaining_strings:
                if string not in conflicted_strings:
                    result[string] = (crc_name, next_unique_id)
                    next_unique_id += 1
                    newly_assigned.add(string)

            # Remove assigned strings from remaining list
            remaining_strings = [s for s in remaining_strings if s not in newly_assigned]
            if not remaining_strings:
                break
        if len(remaining_strings) != 0:
            raise ValueError(f"Could not resolve all conflicts, {len(remaining_strings)} strings remain unassigned")
        return result

    def process_file(self, input_file: str, format: str = 'ascii'):
        """Process input file and generate results"""
        try:
            # Read input file
            lines = None
            with open(input_file, 'r', encoding='ascii') as f:
                lines = f.readlines()

            # Clean and validate strings
            strings = []
            for i, line in enumerate(lines):
                line = line.strip()
                if format == 'ascii':
                    if len(line) > 32:
                        raise ValueError(f"Line {i+1} exceeds 32 bytes: {line}")
                    if line:  # Skip empty lines
                        strings.append(line)
                elif format == 'hex':
                    if line:  # Skip empty lines
                        # Convert hex string to bytes
                        hex_bytes = bytes.fromhex(line)
                        if len(hex_bytes) > 32:
                            raise ValueError(f"Line {i+1} exceeds 32 bytes: {line}")
                        strings.append(hex_bytes)

            if len(strings) > self.max_ids:
                raise ValueError(f"Input file '{input_file}' contains too many strings (>{self.max_ids})")
            hex_strings = strings
            line_size = max(map(len, strings), default=0)
            if format == 'ascii':
                hex_strings = [int.from_bytes(s.encode("ascii"), 'little').to_bytes(line_size,'little') for s in strings]
            # Assign hash functions
            assignments = self.assign_hash_functions(hex_strings)

            # Write results
            # Set each ID entry to 4 bytes (max 30-bit ID + 1 bit validity < 32-bit)
            id_bytes = 4

            for string, (crc_func, unique_id) in assignments.items():
                poly_idx = get_poly_index(crc_func)
                hash_val = self.calculate_crc(string, crc_func)
                addr = (poly_idx << self.crc_width) | hash_val
                content = unique_id | (1 << self.crc_width)
                self.hash_table_bin[addr*id_bytes:(addr+1)*id_bytes] = content.to_bytes(id_bytes, 'little')
            for string in strings:
                unique_id = assignments[int.from_bytes(string.encode("ascii"), 'little').to_bytes(line_size,'little') if format == 'ascii' else string][1]
                self.hash_table[string] = unique_id

        except FileNotFoundError:
            print(f"Error: Input file '{input_file}' not found")
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Error: Input file '{input_file}' contains non-ASCII characters")
            sys.exit(1)
        except Exception as e:
            print(f"Error processing file: {e}")
            sys.exit(1)
    def dump_binary_table(self, output_file: str = "result.bin"):
        with open(output_file, 'wb') as f:
            f.write(self.hash_table_bin)
    def dump_readable_table(self, output_file: str = "result.txt"):
        with open(output_file, 'w', encoding='ascii') as f:
            for string, unique_id in self.hash_table.items():
                f.write(f"{string} -> {unique_id}\n")

def main():
    parser = argparse.ArgumentParser(
        description='Static Hash Script for ASCII Strings using Multiple CRC Functions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script maps ASCII strings to unique IDs using multiple CRC hash functions
to eliminate conflicts through a layered approach. Supports configurable ID ranges
with automatic CRC polynomial selection.

Input file format:
  - One ASCII string per line
  - Maximum 32 bytes per string
  - Up to specified maximum total strings

The script will:
  1. Use a multi-layer approach to resolve conflicts
  2. Generate unique IDs for all input strings
  3. Output results to 'result.bin' and 'result.txt' (or specified output file)

Example:
  python static_hash.py input.txt
  python static_hash.py input.txt --max-ids 65536
  python static_hash.py input.txt --max-ids 65536 --output_bin custom.bin --output_txt custom.txt
        """
    )

    parser.add_argument(
        'input_file',
        help='Input file containing ASCII strings (one per line, max 32 bytes each)'
    )

    parser.add_argument(
        '--max-ids',
        type=int,
        default=32768,
        help='Maximum number of IDs to support (default: 32768). Script will automatically select appropriate CRC width.'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['ascii', 'hex'],
        default='ascii',
        help='Input format: ascii for text strings, hex for hexadecimal strings (default: ascii)'
    )

    parser.add_argument(
        '--output_bin',
        default=None,
        help='Output file for binary results (default: result.bin)'
    )

    parser.add_argument(
        '--output_txt',
        default=None,
        help='Output file for readable results (default: result.txt)'
    )

    args = parser.parse_args()

    hasher = StaticHasher(max_ids=args.max_ids)
    hasher.process_file(args.input_file, args.format)

    if args.output_bin:
        hasher.dump_binary_table(args.output_bin)
    if args.output_txt:
        hasher.dump_readable_table(args.output_txt)

if __name__ == "__main__":
    main()