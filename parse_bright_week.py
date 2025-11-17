#!/usr/bin/env python3
"""
Parse bright_week.md and populate scripture_readings.json with Bright Week readings.
"""

import json
import re

def parse_bright_week():
    with open('bright_week.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    readings = {'pascha': {}}
    day_map = {'Sunday': '0', 'Monday': '1', 'Tuesday': '2', 'Wednesday': '3', 'Thursday': '4', 'Friday': '5', 'Saturday': '6'}

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if '|' in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if parts and '*' in parts[0]:
                day_name = parts[0].replace('*', '').strip()
                if day_name in day_map:
                    day = day_map[day_name]
                    readings['pascha'][day] = []
                    # Collect all matches for this day
                    epistle_matches = []
                    gospel_matches = []
                    i += 1
                    while i < len(lines) and not (lines[i].strip().startswith('| *') and any(d in lines[i] for d in day_map)):
                        line2 = lines[i].strip()
                        if '|' in line2:
                            parts2 = [p.strip() for p in line2.split('|') if p.strip()]
                            text = ' '.join(parts2[1:]) if len(parts2) > 1 else ''
                            matches = re.findall(r'([A-Za-z0-9\s]+) §\d+ \((\d+:\d+(?:-\d+)?(?:, \d+:\d+(?:-\d+)?)*)\)', text)
                            for match in matches:
                                book, verses = match
                                book = book.strip()
                                if book in ['Matthew', 'Mark', 'Luke', 'John']:
                                    gospel_matches.append((book, verses))
                                else:
                                    epistle_matches.append((book, verses))
                        i += 1
                    # Process
                    if epistle_matches and gospel_matches:
                        ep_match = epistle_matches[0]
                        gos_match = gospel_matches[0]
                        book_e, verses_e = ep_match
                        book_g, verses_g = gos_match
                        if ':' in verses_e:
                            chapter_num, verse_part = verses_e.split(':', 1)
                            chapter_e = int(chapter_num)
                            verses_e = verse_part
                        if ':' in verses_g:
                            chapter_num, verse_part = verses_g.split(':', 1)
                            chapter_g = int(chapter_num)
                            verses_g = verse_part
                        readings['pascha'][day] = [
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
                        ]
                    i -= 1  # Adjust for the while loop
        i += 1
    return readings

def main():
    readings = parse_bright_week()
    print("Parsed readings:", readings)
    with open('scripture_readings.json', 'w') as f:
        json.dump(readings, f, indent=2)

if __name__ == '__main__':
    main()