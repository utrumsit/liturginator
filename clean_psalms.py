#!/usr/bin/env python3
"""
Script to clean up psalm headers in kathisma.md:
- Replace Hebrew numbering with Greek numbering from parentheses.
- Remove Latin titles on the same line.
"""

import re

def clean_psalms():
    input_file = 'resource/kathisma-source.md'
    output_file = 'resource/kathisma.md'

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith('## Psalm'):
            # Match: ## Psalm X(Y) Latin Title
            match = re.match(r'^## Psalm ([0-9.]+)\(([^)]+)\) (.+)$', line.strip())
            if match:
                greek_num = match.group(2)
                new_line = f'## Psalm {greek_num}\n'
                new_lines.append(new_line)
            else:
                # If no match, keep as is
                new_lines.append(line)
        else:
            new_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

    print(f"Cleaned psalms written to {output_file}")

if __name__ == "__main__":
    clean_psalms()