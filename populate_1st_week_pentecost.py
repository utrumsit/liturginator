#!/usr/bin/env python3
"""
Populate scripture_readings.json with 1st Week after Pentecost.
"""

import json

def main():
    readings = {
        'pentecostarion': {
            '1': {  # 1st week after Pentecost
            '0': {  # Monday
                'title': 'Monday of 1st Week after Pentecost',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Ephesians',
                        'chapter': 5,
                        'verses': '8b-19',
                        'text': '',
                        'context': 'Ephesians 5:8b-19'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Matthew',
                        'chapter': 18,
                        'verses': '10-20',
                        'text': '',
                        'context': 'Matthew 18:10-20'
                    }
                ]
            },
            '1': {  # Tuesday
                'title': 'Tuesday of 1st Week after Pentecost',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Romans',
                        'chapter': 1,
                        'verses': '1-7, 13-17',
                        'text': '',
                        'context': 'Romans 1:1-7, 13-17'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Matthew',
                        'chapter': 4,
                        'verses': '25-5:12a',
                        'text': '',
                        'context': 'Matthew 4:25-5:12a'
                    }
                ]
            },
            '2': {  # Wednesday
                'title': 'Wednesday of 1st Week after Pentecost',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Romans',
                        'chapter': 1,
                        'verses': '18-27',
                        'text': '',
                        'context': 'Romans 1:18-27'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Matthew',
                        'chapter': 5,
                        'verses': '20-26',
                        'text': '',
                        'context': 'Matthew 5:20-26'
                    }
                ]
            },
            '3': {  # Thursday
                'title': 'Thursday of 1st Week after Pentecost',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Romans',
                        'chapter': 1,
                        'verses': '28-2:9',
                        'text': '',
                        'context': 'Romans 1:28-2:9'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Matthew',
                        'chapter': 5,
                        'verses': '27-32',
                        'text': '',
                        'context': 'Matthew 5:27-32'
                    }
                ]
            },
            '4': {  # Friday
                'title': 'Friday of 1st Week after Pentecost',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Romans',
                        'chapter': 2,
                        'verses': '14-29',
                        'text': '',
                        'context': 'Romans 2:14-29'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Matthew',
                        'chapter': 5,
                        'verses': '33-41',
                        'text': '',
                        'context': 'Matthew 5:33-41'
                    }
                ]
            },
            '5': {  # Saturday
                'title': 'Saturday of 1st Week after Pentecost',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Romans',
                        'chapter': 1,
                        'verses': '7b-12',
                        'text': '',
                        'context': 'Romans 1:7b-12'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Matthew',
                        'chapter': 5,
                        'verses': '42-48',
                        'text': '',
                        'context': 'Matthew 5:42-48'
                    }
                ]
            },
            '6': {  # Sunday
                'title': '1st Sunday after Pentecost: Sunday of All Saints',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Hebrews',
                        'chapter': 11,
                        'verses': '33-12:2a',
                        'text': '',
                        'context': 'Hebrews 11:33-12:2a'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Matthew',
                        'chapter': 10,
                        'verses': '32-33, 37-38; 19:27-30',
                        'text': '',
                        'context': 'Matthew 10:32-33, 37-38; 19:27-30'
                    }
                ],
                'matins_gospel': {
                    'book': 'Matthew',
                    'chapter': 28,
                    'verses': '16-20',
                    'text': '',
                    'context': 'Matthew 28:16-20'
                },
                'vespers_paramia': [
                    {
                        'book': 'Isaiah',
                        'chapter': 43,
                        'verses': '9-14a',
                        'text': '',
                        'context': 'Isaiah 43:9-14a'
                    },
                    {
                        'book': 'Wisdom',
                        'chapter': 3,
                        'verses': '1-9',
                        'text': '',
                        'context': 'Wisdom 3:1-9'
                    },
                    {
                        'book': 'Wisdom',
                        'chapter': 5,
                        'verses': '15-6:3',
                        'text': '',
                        'context': 'Wisdom 5:15-6:3'
                    }
                ]
            }
            }
        }
    }
    # Load existing and merge
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}
    if 'pentecostarion' not in existing:
        existing['pentecostarion'] = {}
    existing['pentecostarion'].update(readings['pentecostarion'])
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)

if __name__ == '__main__':
    main()