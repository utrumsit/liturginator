#!/usr/bin/env python3
"""
Vespers Assembler

Assembles the full text of Vespers for a given date.
"""

from vespers_logic import VespersAssembler
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate Vespers liturgy for a given date.")
    parser.add_argument('date', help='Date in YYYY-MM-DD format')
    args = parser.parse_args()

    assembler = VespersAssembler(args.date)
    output = assembler.assemble()

    print(output)

if __name__ == "__main__":
    main()