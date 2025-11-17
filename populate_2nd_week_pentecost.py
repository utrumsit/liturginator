#!/usr/bin/env python3
"""
Populate scripture_readings.json with 2nd Week after Pentecost.
"""

import json

def main():
    readings = {
        'pentecostarion': {
            '2': {  # 2nd week after Pentecost
                '0': {  # Monday
                    'title': 'Monday of 2nd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 2,
                            'verses': '28-3:18',
                            'text': '',
                            'context': 'Romans 2:28-3:18'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 6,
                            'verses': '31-34; 7:9-11',
                            'text': '',
                            'context': 'Matthew 6:31-34; 7:9-11'
                        }
                    ]
                },
                '1': {  # Tuesday
                    'title': 'Tuesday of 2nd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 4,
                            'verses': '4-12',
                            'text': '',
                            'context': 'Romans 4:4-12'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 7,
                            'verses': '15-21',
                            'text': '',
                            'context': 'Matthew 7:15-21'
                        }
                    ]
                },
                '2': {  # Wednesday
                    'title': 'Wednesday of 2nd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 4,
                            'verses': '13-25',
                            'text': '',
                            'context': 'Romans 4:13-25'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 7,
                            'verses': '21-23',
                            'text': '',
                            'context': 'Matthew 7:21-23'
                        }
                    ]
                },
                '3': {  # Thursday
                    'title': 'Thursday of 2nd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 5,
                            'verses': '10-16',
                            'text': '',
                            'context': 'Romans 5:10-16'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 8,
                            'verses': '23-27',
                            'text': '',
                            'context': 'Matthew 8:23-27'
                        }
                    ]
                },
                '4': {  # Friday
                    'title': 'Friday of 2nd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 5,
                            'verses': '17-6:2',
                            'text': '',
                            'context': 'Romans 5:17-6:2'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 9,
                            'verses': '14-17',
                            'text': '',
                            'context': 'Matthew 9:14-17'
                        }
                    ]
                },
                '5': {  # Saturday
                    'title': 'Saturday of 2nd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 3,
                            'verses': '19-26',
                            'text': '',
                            'context': 'Romans 3:19-26'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 7,
                            'verses': '1-8',
                            'text': '',
                            'context': 'Matthew 7:1-8'
                        }
                    ]
                },
                '6': {  # Sunday
                    'title': '2nd Sunday after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 2,
                            'verses': '10-16',
                            'text': '',
                            'context': 'Romans 2:10-16'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 4,
                            'verses': '18-23',
                            'text': '',
                            'context': 'Matthew 4:18-23'
                        }
                    ],
                    'matins_gospel': {
                        'book': 'Mark',
                        'chapter': 16,
                        'verses': '1-8',
                        'text': '',
                        'context': 'Mark 16:1-8'
                    }
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