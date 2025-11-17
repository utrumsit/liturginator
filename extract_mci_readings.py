#!/usr/bin/env python3
"""
Extract readings from MCI HTML and populate scripture_readings.json.
"""

import json
import re
from bs4 import BeautifulSoup

# MCI HTML file
MCI_HTML_FILE = 'mci-lectionary.html'

def parse_mci_html():
    """
    Parse MCI HTML to extract readings by section.
    """
    with open(MCI_HTML_FILE, 'r', encoding='utf-8') as f:
        html = f.read()
    print("HTML length:", len(html))
    print("HTML start:", html[:100])
    soup = BeautifulSoup(html, 'html.parser')
    readings = {
        'fixed': {},
        'lent': {},
        'pascha': {},
        'pentecostarion': {},
        'triodion': {}
    }
    # Find the main table (the one with BRIGHT WEEK)
    table = None
    for t in soup.find_all('table', {'width': '513'}):
        if 'BRIGHT WEEK' in t.get_text():
            table = t
            break
    print("Table found:", table is not None)
    if not table:
        return readings
    current_section = 'pascha'  # Start with Pascha
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
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if not cells:
            continue
        first_cell = cells[0].get_text().strip()
        if 'BRIGHT WEEK' in first_cell.upper():
            current_section = 'pascha'
        elif 'SECOND WEEK' in first_cell.upper():
            current_section = 'pascha'
        # Add more for other weeks
        elif 'PENTECOST' in first_cell.upper():
            current_section = 'pentecostarion'
        # Check for day
        day = None
        for d in day_map:
            if d in first_cell:
                day = day_map[d]
                break
        if day:
            # Process previous day's matches
            if previous_day is not None:
                process_day_matches(previous_day, epistle_matches, gospel_matches)
            # Reset for new day
            previous_day = day
            epistle_matches = []
            gospel_matches = []
        # Extract readings from cells
        for cell in cells[1:]:
            text = cell.get_text()
            matches = re.findall(r'([A-Za-z0-9\s]+) §\d+ \((\d+:\d+(?:-\d+)?(?:, \d+:\d+(?:-\d+)?)*)\)', text)
            for match in matches:
                book, verses = match
                book = book.strip()
                if book in ['Matthew', 'Mark', 'Luke', 'John']:
                    gospel_matches.append((book, verses))
                else:
                    epistle_matches.append((book, verses))
    # Process last day's matches
    if previous_day is not None:
        process_day_matches(previous_day, epistle_matches, gospel_matches)
    return readings

def main():
    readings = parse_mci_html()
    print("Readings:", readings)
    with open('scripture_readings.json', 'w') as f:
        json.dump(readings, f, indent=2)

if __name__ == '__main__':
    main()