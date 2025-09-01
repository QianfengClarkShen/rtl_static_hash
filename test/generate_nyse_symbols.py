#!/usr/bin/env python3
"""
Generate NYSE-style stock symbol names for testing static_hash.py

This script generates realistic NYSE-style stock symbols following common patterns:
- 1-5 character symbols (most common: 1-4 characters)
- Uses only uppercase letters A-Z
- Follows real NYSE symbol patterns and conventions
- Includes common patterns like tech companies, banks, utilities, etc.
"""

import random
import string
import sys
import argparse
from pathlib import Path

def generate_symbols(count=65536, seed=42):
    """
    Generate count unique NYSE-style stock symbols

    Args:
        count: Number of symbols to generate
        seed: Random seed for reproducible results
    """
    random.seed(seed)
    symbols = set()

    # Common NYSE symbol patterns and prefixes
    tech_prefixes = ['AAPL', 'GOOGL', 'MSFT', 'META', 'NFLX', 'NVDA', 'TSLA', 'AMD', 'INTC', 'ORCL']
    bank_prefixes = ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'USB', 'PNC', 'TFC', 'COF']
    utility_prefixes = ['NEE', 'DUK', 'SO', 'AEP', 'EXC', 'XEL', 'PEG', 'ED', 'ETR', 'ES']

    # Common suffixes for different share classes or variants
    suffixes = ['', 'A', 'B', 'C', 'D', 'PR', 'RT', 'WS', 'WT']

    # Industry-specific letter combinations
    industry_patterns = [
        # Technology
        ['TECH', 'SOFT', 'DATA', 'CYBER', 'CLOUD', 'AI', 'ROBO'],
        # Finance
        ['FIN', 'BANK', 'CRED', 'CAP', 'FUND', 'INVT', 'LOAN'],
        # Healthcare
        ['BIO', 'PHARM', 'MED', 'HLTH', 'CARE', 'DRUG', 'THER'],
        # Energy
        ['OIL', 'GAS', 'ENR', 'PWR', 'FUEL', 'COAL', 'WIND'],
        # Manufacturing
        ['MFG', 'IND', 'MACH', 'AUTO', 'STEEL', 'CHEM', 'MAT'],
        # Retail/Consumer
        ['RTL', 'SHOP', 'FOOD', 'CONS', 'HOME', 'FASH', 'LUXE']
    ]

    print(f"Generating {count} NYSE-style stock symbols...")

    # Method 1: Add some real-looking symbols based on patterns
    real_patterns = tech_prefixes + bank_prefixes + utility_prefixes
    for pattern in real_patterns:
        if len(symbols) >= count:
            break
        for suffix in suffixes:
            symbol = pattern + suffix
            if len(symbol) <= 5 and symbol:  # NYSE symbols are max 5 characters
                symbols.add(symbol)
                if len(symbols) >= count:
                    break

    # Method 2: Generate industry-based symbols
    attempts = 0
    max_attempts = count * 20

    while len(symbols) < count and attempts < max_attempts:
        attempts += 1

        # Choose symbol length (weighted towards shorter symbols like real NYSE)
        length_weights = [5, 25, 35, 25, 10]  # 1-char: 5%, 2-char: 25%, 3-char: 35%, 4-char: 25%, 5-char: 10%
        symbol_length = random.choices(range(1, 6), weights=length_weights)[0]

        # Generate symbol based on different strategies
        strategy = random.choice(['industry', 'random', 'company_style', 'abbreviation'])

        if strategy == 'industry':
            # Use industry patterns
            industry = random.choice(industry_patterns)
            base = random.choice(industry)
            if len(base) > symbol_length:
                symbol = base[:symbol_length]
            elif len(base) == symbol_length:
                symbol = base
            else:
                # Add random letters to reach desired length
                remaining = symbol_length - len(base)
                symbol = base + ''.join(random.choices(string.ascii_uppercase, k=remaining))

        elif strategy == 'company_style':
            # Generate company-style abbreviations
            if symbol_length <= 2:
                # Use initials style
                symbol = ''.join(random.choices(string.ascii_uppercase, k=symbol_length))
            else:
                # Use consonant-heavy patterns (more realistic)
                consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
                vowels = 'AEIOU'

                symbol = ''
                for i in range(symbol_length):
                    if i == 0 or (i > 0 and symbol[-1] in vowels):
                        # Start with consonant or follow vowel with consonant
                        symbol += random.choice(consonants)
                    else:
                        # Mix consonants and vowels
                        symbol += random.choice(string.ascii_uppercase)

        elif strategy == 'abbreviation':
            # Create abbreviation-style symbols
            if symbol_length >= 3:
                # Common abbreviation patterns
                patterns = ['ABC', 'XYZ', 'INC', 'CRP', 'GRP', 'SYS', 'TEC', 'DEV']
                base = random.choice(patterns)[:symbol_length-1]
                symbol = base + random.choice(string.ascii_uppercase)
            else:
                symbol = ''.join(random.choices(string.ascii_uppercase, k=symbol_length))

        else:  # random
            symbol = ''.join(random.choices(string.ascii_uppercase, k=symbol_length))

        # Add to set (automatically handles uniqueness)
        if symbol and len(symbol) <= 5:
            symbols.add(symbol)

        # Progress indicator
        if attempts % 50000 == 0:
            print(f"Generated {len(symbols)} unique symbols (attempt {attempts})...")

    if len(symbols) < count:
        print(f"WARNING: Could only generate {len(symbols)} unique symbols after {max_attempts} attempts")

    # Convert to sorted list for consistent output
    symbol_list = sorted(list(symbols))
    return symbol_list[:count]

def analyze_symbols(symbols):
    """Analyze the generated symbols"""
    print(f"\n=== SYMBOL ANALYSIS ===")
    print(f"Total symbols: {len(symbols)}")
    print(f"Unique symbols: {len(set(symbols))}")

    # Length distribution
    lengths = [len(s) for s in symbols]
    length_counts = {}
    for length in lengths:
        length_counts[length] = length_counts.get(length, 0) + 1

    print(f"Length distribution:")
    for length in sorted(length_counts.keys()):
        count = length_counts[length]
        percentage = (count / len(symbols)) * 100
        print(f"  {length} chars: {count:5d} symbols ({percentage:5.1f}%)")

    # Character frequency
    all_chars = ''.join(symbols)
    char_freq = {}
    for char in all_chars:
        char_freq[char] = char_freq.get(char, 0) + 1

    print(f"\nMost common starting letters:")
    first_chars = [s[0] for s in symbols]
    first_char_freq = {}
    for char in first_chars:
        first_char_freq[char] = first_char_freq.get(char, 0) + 1

    sorted_first = sorted(first_char_freq.items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_first[:10]:
        percentage = (count / len(symbols)) * 100
        print(f"  {char}: {count:4d} ({percentage:4.1f}%)")

    # Sample symbols by length
    print(f"\nSample symbols by length:")
    by_length = {}
    for s in symbols:
        length = len(s)
        if length not in by_length:
            by_length[length] = []
        by_length[length].append(s)

    for length in sorted(by_length.keys()):
        samples = by_length[length][:10]  # Show 10 samples per length
        print(f"  Length {length}: {samples}")

def main():
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description='Generate NYSE-style stock symbols for testing')
    parser.add_argument('-c', '--count', type=int, default=65536,
                       help='Number of symbols to generate (default: 65536)')
    parser.add_argument('-s', '--seed', type=int, default=42,
                       help='Random seed for reproducible results (default: 42)')
    parser.add_argument('-o', '--output', type=Path, default=script_dir / 'test_symbols.txt',
                       help='Output file (default: test_symbols.txt)')
    parser.add_argument('--analyze', action='store_true',
                       help='Show detailed analysis of generated symbols')
    parser.add_argument('--sort', action='store_true',
                       help='Sort symbols alphabetically (default: True)')

    args = parser.parse_args()

    # Generate symbols
    symbols = generate_symbols(count=args.count, seed=args.seed)

    if not args.sort:
        # Shuffle if not sorting
        random.shuffle(symbols)

    if args.analyze:
        analyze_symbols(symbols)

    # Write to file
    try:
        with open(args.output, 'w', encoding='ascii') as f:
            for symbol in symbols:
                f.write(symbol + '\n')

        print(f"\n{len(symbols)} symbols written to {args.output}")

    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
