#!/usr/bin/env python3
"""
Script to tighten formatting in kathisma.md:
1. Strip leading verse numbers (e.g., "1 " -> "").
2. Add two spaces at the end of each psalm verse line for poetic formatting.
"""

import re

def tighten_formatting():
    input_file = 'resource/kathisma.md'
    output_file = 'resource/kathisma_clean.md'  # Temporary output

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()
        if re.match(r'^\d+ ', stripped):
            # Remove leading number and space, add two spaces at end
            new_line = re.sub(r'^\d+ (.*)$', r'\1  ', stripped) + '\n'
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Tightened formatting written to {output_file}")

if __name__ == "__main__":
    tighten_formatting()