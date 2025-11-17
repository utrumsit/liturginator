#!/usr/bin/env python3
"""
Populate scripture_readings.json with Pentecost readings.
"""

import json

def main():
    readings = {
        'pascha': {
            '49': {
                'title': 'Pentecost Sunday',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 2,
                        'verses': '1-11',
                        'text': '',
                        'context': 'Acts 2:1-11'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 7,
                        'verses': '37-52; 8:12',
                        'text': '',
                        'context': 'John 7:37-52; 8:12'
                    }
                ],
                'matins_gospel': {
                    'book': 'John',
                    'chapter': 20,
                    'verses': '19-23',
                    'text': '',
                    'context': 'John 20:19-23'
                },
                'vespers_paramia': [
                    {
                        'book': 'Numbers',
                        'chapter': 11,
                        'verses': '16-17, 24-29',
                        'text': '',
                        'context': 'Numbers 11:16-17, 24-29'
                    },
                    {
                        'book': 'Joel',
                        'chapter': 2,
                        'verses': '23-32',
                        'text': '',
                        'context': 'Joel 2:23-32'
                    },
                    {
                        'book': 'Ezekiel',
                        'chapter': 36,
                        'verses': '24-28',
                        'text': '',
                        'context': 'Ezekiel 36:24-28'
                    }
                ]
            }
        }
    }
    # Load existing and merge
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}
    if 'pascha' not in existing:
        existing['pascha'] = {}
    existing['pascha'].update(readings['pascha'])
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)

if __name__ == '__main__':
    main()