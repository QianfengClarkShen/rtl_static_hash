#!/usr/bin/env python3
"""
CRC Polynomial Database

High-quality CRC polynomials from Philip Koopman's CRC polynomial database.
These polynomials have been extensively tested for optimal error detection
capabilities across different data lengths.

References:
- https://users.ece.cmu.edu/~koopman/crc/
- Philip Koopman's "Cyclic Redundancy Code (CRC) Polynomial Selection For Embedded Systems"

Polynomial Format:
Each entry is a tuple: (poly_hex, name, reflect_in, xor_in, reflect_out, xor_out)

- poly_hex: Polynomial value in hexadecimal
- name: Descriptive name of the polynomial
- reflect_in: Whether to reflect input data bits
- xor_in: Initial XOR value (usually 0)
- reflect_out: Whether to reflect output CRC bits
- xor_out: Final XOR value (usually 0)
"""

from typing import Dict, List, Tuple

# High-quality CRC polynomials from Philip Koopman's database
# Format: width -> {name -> (poly_hex, name, reflect_in, xor_in, reflect_out, xor_out), ...}
KOOPMAN_POLYNOMIALS: Dict[int, Dict[str, Tuple[int, str, bool, int, bool, int]]] = {
    8: {
        "CRC-8F-3": (0x1cf, "CRC-8F-3", False, 0, False, 0),
        "CRC-8K-3": (0x14d, "CRC-8K-3", False, 0, False, 0),
        "SAE-J1850": (0x11d, "SAE-J1850", False, 0, False, 0),
        "CCITT-8": (0x163, "CCITT-8", False, 0, False, 0),
        "CRC-8F-8": (0x17f, "CRC-8F-8", False, 0, False, 0),
        "CRC-8-AUTOSAR": (0x12f, "CRC-8-AUTOSAR", False, 0, False, 0),
        "CRC-8-Bluetooth": (0x1a7, "CRC-8-Bluetooth", False, 0, False, 0),
        "WCDMA-8": (0x19b, "WCDMA-8", False, 0, False, 0),
    },
    10: {
        "CRC-10F-3": (0x64f, "CRC-10F-3", False, 0, False, 0),
        "CRC-10F-8.1": (0x5fb, "CRC-10F-8.1", False, 0, False, 0),
        "CRC-10F-6.1": (0x58f, "CRC-10F-6.1", False, 0, False, 0),
        "FP-10": (0x409, "FP-10", False, 0, False, 0),
        "CRC-10F-4.2": (0x48f, "CRC-10F-4.2", False, 0, False, 0),
        "CRC-10F-8.2": (0x5bd, "CRC-10F-8.2", False, 0, False, 0),
        "CRC-10-CDMA2000": (0x7d9, "CRC-10-CDMA2000", False, 0, False, 0),
        "FOP-11": (0x40d, "FOP-11", False, 0, False, 0),
    },
    12: {
        "CRC-12F-3": (0x130f, "CRC-12F-3", False, 0, False, 0),
        "CRC-12K-7": (0x1467, "CRC-12K-7", False, 0, False, 0),
        "FP-12": (0x1053, "FP-12", False, 0, False, 0),
        "CRC-12F-9": (0x1bbf, "CRC-12F-9", False, 0, False, 0),
        "CRC-12K-5.2": (0x17bf, "CRC-12K-5.2", False, 0, False, 0),
        "CRC-12F-6.1": (0x107d, "CRC-12F-6.1", False, 0, False, 0),
        "CRC-12F-4.2": (0x11e7, "CRC-12F-4.2", False, 0, False, 0),
        "CRC-12-CDMA2000": (0x1f13, "CRC-12-CDMA2000", False, 0, False, 0),
    },
    14: {
        "CRC-14F-3": (0x4f9f, "CRC-14F-3", False, 0, False, 0),
        "CRC-14F-7": (0x5153, "CRC-14F-7", False, 0, False, 0),
        "CRC-14F-11": (0x6fdf, "CRC-14F-11", False, 0, False, 0),
        "FP-14": (0x402b, "FP-14", False, 0, False, 0),
        "CRC-14F-10.1": (0x7577, "CRC-14F-10.1", False, 0, False, 0),
        "CRC-14F-9": (0x692f, "CRC-14F-9", False, 0, False, 0),
        "CRC-14K-3": (0x4ed3, "CRC-14K-3", False, 0, False, 0),
        "CRC-14K-8": (0x549f, "CRC-14K-8", False, 0, False, 0),
    },
    16: {
        "CRC-16F-3": (0x11b2b, "CRC-16F-3", False, 0, False, 0),
        "CRC-16F-11": (0x1fb7f, "CRC-16F-11", False, 0, False, 0),
        "FP-16": (0x1002d, "FP-16", False, 0, False, 0),
        "CRC-16K-3": (0x18f57, "CRC-16K-3", False, 0, False, 0),
        "CRC-16F-10.1": (0x12f3d, "CRC-16F-10.1", False, 0, False, 0),
        "CRC-16K-5": (0x12c4f, "CRC-16K-5", False, 0, False, 0),
        "CRC-16-CDMA2000": (0x1c867, "CRC-16-CDMA2000", False, 0, False, 0),
        "CRC-16-T10-DIF": (0x18bb7, "CRC-16-T10-DIF", False, 0, False, 0),
    },
    18: {
        "CRC-18K-3.1": (0x472f3, "CRC-18K-3.1", False, 0, False, 0),
        "FP-18": (0x40027, "FP-18", False, 0, False, 0),
        "CRC-18K-3.5": (0x4717d, "CRC-18K-3.5", False, 0, False, 0),
        "CRC-18K-3.6": (0x5a13f, "CRC-18K-3.6", False, 0, False, 0),
        "CRC-18K-3.4": (0x43757, "CRC-18K-3.4", False, 0, False, 0),
        "CRC-18K-3.2": (0x57dad, "CRC-18K-3.2", False, 0, False, 0),
        "CRC-18K-3.3": (0x5dc93, "CRC-18K-3.3", False, 0, False, 0),
        "CRC-18K-11": (0x4d47b, "CRC-18K-11", False, 0, False, 0),
    },
    20: {
        "CRC-20K-3.1": (0x16b04f, "CRC-20K-3.1", False, 0, False, 0),
        "CRC-20K-3.5": (0x168d6f, "CRC-20K-3.5", False, 0, False, 0),
        "CRC-20K-3.7": (0x189b0f, "CRC-20K-3.7", False, 0, False, 0),
        "CRC-20K-3.2": (0x15eadf, "CRC-20K-3.2", False, 0, False, 0),
        "CRC-20K-3.3": (0x19bdf3, "CRC-20K-3.3", False, 0, False, 0),
        "CRC-20K-3.6": (0x174497, "CRC-20K-3.6", False, 0, False, 0),
        "CRC-20K-3.8": (0x15f9b7, "CRC-20K-3.8", False, 0, False, 0),
        "CRC-20K-3.4": (0x151193, "CRC-20K-3.4", False, 0, False, 0),
    },
    22: {
        "CRC-22K-3.1": (0x611fa7, "CRC-22K-3.1", False, 0, False, 0),
        "CRC-22K-3.5": (0x6dc801, "CRC-22K-3.5", False, 0, False, 0),
        "CRC-22K-3.7": (0x529aa9, "CRC-22K-3.7", False, 0, False, 0),
        "CRC-22K-3.10": (0x722bd3, "CRC-22K-3.10", False, 0, False, 0),
        "CRC-22K-3.9": (0x4e536b, "CRC-22K-3.9", False, 0, False, 0),
        "CRC-22K-3.2": (0x77862d, "CRC-22K-3.2", False, 0, False, 0),
        "CRC-22K-3.4": (0x7df163, "CRC-22K-3.4", False, 0, False, 0),
        "CRC-22K-3.3": (0x4bdefb, "CRC-22K-3.3", False, 0, False, 0),
    },
    24: {
        "CRC-24K-3.1": (0x100001b, "CRC-24K-3.1", False, 0, False, 0),
        "CRC-24K-3.2": (0x11f21c7, "CRC-24K-3.2", False, 0, False, 0),
        "CRC-24K-3.8": (0x17b49ab, "CRC-24K-3.8", False, 0, False, 0),
        "CRC-24K-3.3": (0x127969f, "CRC-24K-3.3", False, 0, False, 0),
        "CRC-24K-3.7": (0x16ebd57, "CRC-24K-3.7", False, 0, False, 0),
        "CRC-24K-3.6": (0x12826ad, "CRC-24K-3.6", False, 0, False, 0),
        "CRC-24K-3.9": (0x14e6b4f, "CRC-24K-3.9", False, 0, False, 0),
        "CRC-24K-3.10": (0x170ea2b, "CRC-24K-3.10", False, 0, False, 0),
    },
    26: {
        "CRC-26K-3.1": (0x67833df, "CRC-26K-3.1", False, 0, False, 0),
        "CRC-26K-3.6": (0x74cdc9f, "CRC-26K-3.6", False, 0, False, 0),
        "CRC-26K-3.11": (0x4fd6f67, "CRC-26K-3.11", False, 0, False, 0),
        "CRC-26K-3.7": (0x52145f5, "CRC-26K-3.7", False, 0, False, 0),
        "CRC-26K-3.2": (0x6c95597, "CRC-26K-3.2", False, 0, False, 0),
        "CRC-26K-3.5": (0x76c28cf, "CRC-26K-3.5", False, 0, False, 0),
        "CRC-26K-3.12": (0x7d32257, "CRC-26K-3.12", False, 0, False, 0),
        "CRC-26K-3.4": (0x529ef3d, "CRC-26K-3.4", False, 0, False, 0),
    },
    28: {
        "CRC-28K-3.1": (0x123b83c7, "CRC-28K-3.1", False, 0, False, 0),
        "CRC-28K-3.5": (0x102c41cb, "CRC-28K-3.5", False, 0, False, 0),
        "CRC-28K-3.4": (0x17a0e8a7, "CRC-28K-3.4", False, 0, False, 0),
        "CRC-28K-3.9": (0x19ed232f, "CRC-28K-3.9", False, 0, False, 0),
        "CRC-28K-3.2": (0x11747ad7, "CRC-28K-3.2", False, 0, False, 0),
        "CRC-28K-3.8": (0x112a0cbd, "CRC-28K-3.8", False, 0, False, 0),
        "CRC-28K-3.11": (0x10d6cab9, "CRC-28K-3.11", False, 0, False, 0),
        "CRC-28K-3.10": (0x169d901f, "CRC-28K-3.10", False, 0, False, 0),
    },
    30: {
        "CRC-30K-3.1": (0x6268545f, "CRC-30K-3.1", False, 0, False, 0),
        "CRC-30K-3.3": (0x54b7233b, "CRC-30K-3.3", False, 0, False, 0),
        "CRC-30K-3.11": (0x68a55347, "CRC-30K-3.11", False, 0, False, 0),
        "CRC-30K-3.8": (0x41667891, "CRC-30K-3.8", False, 0, False, 0),
        "CRC-30K-3.9": (0x4922d0ab, "CRC-30K-3.9", False, 0, False, 0),
        "CRC-30K-3.2": (0x6220e663, "CRC-30K-3.2", False, 0, False, 0),
        "CRC-30K-3.13": (0x512ff0cb, "CRC-30K-3.13", False, 0, False, 0),
        "CRC-30K-3.12": (0x46d305c7, "CRC-30K-3.12", False, 0, False, 0),
    }
}
def get_polynomials() -> List[Tuple[int, str, bool, int, bool, int]]:
    polynomials = []
    for entry in KOOPMAN_POLYNOMIALS.values():
        polynomials += list(entry.values())
    return polynomials

def get_poly_index(poly: str) -> int:
    for grp in KOOPMAN_POLYNOMIALS.values():
        if poly in grp.keys():
            return list(grp.keys()).index(poly)