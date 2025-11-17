#!/usr/bin/env python3
"""
Parse mci-lectionary.md and populate scripture_readings.json with all readings.
"""

import json
import re

def parse_markdown_table():
    """
    Parse the markdown table from mci-lectionary.md.
    """
    with open('mci-lectionary.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    readings = {
        'fixed': {},
        'lent': {},
        'pascha': {},
        'pentecostarion': {},
        'triodion': {}
    }

    current_section = None
    day_map = {'Sunday': '0', 'Monday': '1', 'Tuesday': '2', 'Wednesday': '3', 'Thursday': '4', 'Friday': '5', 'Saturday': '6'}

    previous_day = None
    epistle_matches = []
    gospel_matches = []

    def process_day_matches(day, epistle_matches, gospel_matches):
        if epistle_matches and gospel_matches:
            # Take the first epistle and first gospel
            ep_match = epistle_matches[0]
            gos_match = gospel_matches[0]
            book_e, verses_e = ep_match
            book_g, verses_g = gos_match
            # Process epistle
            if ':' in verses_e:
                chapter_num, verse_part = verses_e.split(':', 1)
                chapter_e = int(chapter_num)
                verses_e = verse_part
            else:
                return
            # Process gospel
            if ':' in verses_g:
                chapter_num, verse_part = verses_g.split(':', 1)
                chapter_g = int(chapter_num)
                verses_g = verse_part
            else:
                return
            if day not in readings[current_section]:
                readings[current_section][day] = []
            readings[current_section][day].extend([
                {
                    'type': 'epistle',
                    'book': book_e,
                    'chapter': chapter_e,
                    'verses': verses_e,
                    'text': '',
                    'context': f"{book_e} {chapter_e}:{verses_e}"
                },
                {
                    'type': 'gospel',
                    'book': book_g,
                    'chapter': chapter_g,
                    'verses': verses_g,
                    'text': '',
                    'context': f"{book_g} {chapter_g}:{verses_g}"
                }
            ])

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if '**BRIGHT WEEK**' in line:
            current_section = 'pascha'
        elif '**PENTECOST' in line:
            current_section = 'pentecostarion'
        elif '**TRIodion' in line.upper():
            current_section = 'triodion'
        elif '**LENT' in line.upper():
            current_section = 'lent'

        if current_section and '|' in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 2:
                first_part = parts[0]
                day = None
                for day_name, day_num in day_map.items():
                    if day_name in first_part:
                        day = day_num
                        break
                if day:
                    # Process previous day's matches
                    if previous_day is not None:
                        process_day_matches(previous_day, epistle_matches, gospel_matches)
                    # Reset for new day
                    previous_day = day
                    epistle_matches = []
                    gospel_matches = []
                # Extract readings from the line
                text = ' '.join(parts[1:])
                matches = re.findall(r'([A-Za-z0-9\s]+) §\d+ \((\d+:\d+(?:-\d+)?(?:, \d+:\d+(?:-\d+)?)*)\)', text)
                for match in matches:
                    book, verses = match
                    book = book.strip()
                    if book in ['Matthew', 'Mark', 'Luke', 'John']:
                        gospel_matches.append((book, verses))
                    else:
                        epistle_matches.append((book, verses))
        i += 1

    # Process last day's matches
    if previous_day is not None:
        process_day_matches(previous_day, epistle_matches, gospel_matches)

    return readings

def main():
    readings = parse_markdown_table()
    # Merge with existing
    try:
        with open('scripture_readings.json', 'r', encoding='utf-8') as f:
            existing = json.load(f)
    except:
        existing = readings

    # Update existing with new
    for section, data in readings.items():
        if section not in existing:
            existing[section] = {}
        for key, value in data.items():
            existing[section][key] = value

    with open('scripture_readings.json', 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()