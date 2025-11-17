#!/usr/bin/env python3
"""
Populate scripture_readings.json with readings from MCI Lectionary and RSV texts from Bible Gateway.
"""

import json
import re

# MCI HTML content (paste the fetched HTML here)
mci_html = """
[Insert the full MCI HTML here]
"""

def extract_readings_from_mci(html):
    """
    Extract reading references from MCI HTML.
    Returns a dict of sections with readings.
    """
    readings = {
        'fixed': {},
        'lent': {},
        'pascha': {},
        'pentecostarion': {},
        'triodion': {}
    }
    # Use regex to find patterns like "Acts §1 (1:1-8)"
    pattern = r'(\w+) §(\d+) \((\d+:\d+(?:-\d+)?(?:, \d+:\d+(?:-\d+)?)*)\)'
    matches = re.findall(pattern, html)
    # Map to sections (simplified; need better mapping)
    # For now, add to pascha as example
    readings['pascha']['0'] = []
    for match in matches[:10]:  # Limit for testing
        book, section_num, verses = match
        readings['pascha']['0'].append({
            'type': 'epistle' if 'Acts' in book else 'gospel',
            'book': book,
            'chapter': int(section_num),
            'verses': verses,
            'text': '',
            'context': 'Pascha'
        })
    return readings

def fetch_rsv_text(book, chapter, verses):
    """
    Fetch RSV text from Bible Gateway using webfetch.
    """
    search = f"{book} {chapter}:{verses}"
    url = f"https://www.biblegateway.com/passage/?search={search}&version=RSV"
    # Use webfetch (but since it's a tool, simulate)
    # For now, return placeholder
    return f"Fetched RSV text for {book} {chapter}:{verses}"

def populate_json():
    """
    Populate scripture_readings.json.
    """
    readings = extract_readings_from_mci(mci_html)
    # For each reading, fetch text
    for section, data in readings.items():
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    for reading in value:
                        if 'book' in reading and 'chapter' in reading and 'verses' in reading:
                            text = fetch_rsv_text(reading['book'], reading['chapter'], reading['verses'])
                            reading['text'] = text

    with open('scripture_readings.json', 'w') as f:
        json.dump(readings, f, indent=2)

if __name__ == '__main__':
    populate_json()