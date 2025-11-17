#!/usr/bin/env python3
"""
Automate extraction of all Pentecostarion weeks from mci-lectionary.md and populate scripture_readings.json.
"""

import json
import re

def parse_reading(text):
    # Parse "Romans §83 (2:28-3:18)" to book, chapter, verses
    match = re.search(r'(\w+(?:\s+\w+)*) §\d+ \((\d+):([^)]+)\)', text)
    if match:
        book = match.group(1)
        chapter = int(match.group(2))
        verses = match.group(3)
        return book, chapter, verses
    return None, None, None

def main():
    with open('mci-lectionary.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    pentecostarion = {}
    current_week = None
    current_day = None
    readings = {}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if '**' in line and 'WEEK after PENTECOST' in line:
            # New week
            match = re.search(r'(\d+)(?:ST|ND|RD|TH)', line)
            if match:
                week_num = int(match.group(1))
                if week_num > 29:
                    break  # Stop at 29
                current_week = week_num
                pentecostarion[current_week] = {}
        elif current_week and '|' in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 1 and '*' in parts[0]:
                day_name = parts[0].replace('*', '').strip()
                day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
                if day_name in day_map:
                    current_day = day_map[day_name]
                    # For the day line
                    epistle_text = parts[1] if len(parts) > 1 else ''
                    gospel_text = parts[2] if len(parts) > 2 else ''
                    # Next line for continuation
                    i += 1
                    if i < len(lines):
                        line2 = lines[i].strip()
                        if '|' in line2:
                            parts2 = [p.strip() for p in line2.split('|') if p.strip()]
                            if len(parts2) > 2 and parts2[2]:
                                gospel_text += ' ' + parts2[2]
                    gospel_text = gospel_text.strip()
                    # Parse
                    book_e, ch_e, vs_e = parse_reading(epistle_text)
                    book_g, ch_g, vs_g = parse_reading(gospel_text)
                    if book_e and book_g:
                        pentecostarion[current_week][current_day] = {
                            'title': f'{day_name} of {current_week}{"st" if current_week==1 else "nd" if current_week==2 else "rd" if current_week==3 else "th"} Week after Pentecost',
                            'readings': [
                                {'type': 'epistle', 'book': book_e, 'chapter': ch_e, 'verses': vs_e, 'text': '', 'context': f'{book_e} {ch_e}:{vs_e}'},
                                {'type': 'gospel', 'book': book_g, 'chapter': ch_g, 'verses': vs_g, 'text': '', 'context': f'{book_g} {ch_g}:{vs_g}'}
                            ]
                        }
                        if day_name == 'Sunday':
                            # Check for matins
                            # For now, skip
                            pass
        i += 1

    # Now, merge into JSON
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}
    if 'pentecostarion' not in existing:
        existing['pentecostarion'] = {}
    existing['pentecostarion'].update(pentecostarion)
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)

if __name__ == '__main__':
    main()