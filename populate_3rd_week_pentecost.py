#!/usr/bin/env python3
"""
Populate scripture_readings.json with 3rd Week after Pentecost.
"""

import json

def main():
    readings = {
        'pentecostarion': {
            '3': {  # 3rd week after Pentecost
                '0': {  # Monday
                    'title': 'Monday of 3rd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 7,
                            'verses': '1-13',
                            'text': '',
                            'context': 'Romans 7:1-13'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 9,
                            'verses': '36-10:8',
                            'text': '',
                            'context': 'Matthew 9:36-10:8'
                        }
                    ]
                },
                '1': {  # Tuesday
                    'title': 'Tuesday of 3rd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 7,
                            'verses': '14-8:2',
                            'text': '',
                            'context': 'Romans 7:14-8:2'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 10,
                            'verses': '9-15',
                            'text': '',
                            'context': 'Matthew 10:9-15'
                        }
                    ]
                },
                '2': {  # Wednesday
                    'title': 'Wednesday of 3rd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 8,
                            'verses': '2-13',
                            'text': '',
                            'context': 'Romans 8:2-13'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 10,
                            'verses': '16-22',
                            'text': '',
                            'context': 'Matthew 10:16-22'
                        }
                    ]
                },
                '3': {  # Thursday
                    'title': 'Thursday of 3rd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 8,
                            'verses': '22-27',
                            'text': '',
                            'context': 'Romans 8:22-27'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 10,
                            'verses': '23-31',
                            'text': '',
                            'context': 'Matthew 10:23-31'
                        }
                    ]
                },
                '4': {  # Friday
                    'title': 'Friday of 3rd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 9,
                            'verses': '6-19',
                            'text': '',
                            'context': 'Romans 9:6-19'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 10,
                            'verses': '32-36; 11:1',
                            'text': '',
                            'context': 'Matthew 10:32-36; 11:1'
                        }
                    ]
                },
                '5': {  # Saturday
                    'title': 'Saturday of 3rd Week after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 3,
                            'verses': '28-4:3',
                            'text': '',
                            'context': 'Romans 3:28-4:3'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 7,
                            'verses': '24-8:4',
                            'text': '',
                            'context': 'Matthew 7:24-8:4'
                        }
                    ]
                },
                '6': {  # Sunday
                    'title': '3rd Sunday after Pentecost',
                    'readings': [
                        {
                            'type': 'epistle',
                            'book': 'Romans',
                            'chapter': 5,
                            'verses': '1-10',
                            'text': '',
                            'context': 'Romans 5:1-10'
                        },
                        {
                            'type': 'gospel',
                            'book': 'Matthew',
                            'chapter': 6,
                            'verses': '22-34',
                            'text': '',
                            'context': 'Matthew 6:22-34'
                        }
                    ],
                    'matins_gospel': {
                        'book': 'Mark',
                        'chapter': 16,
                        'verses': '9-20',
                        'text': '',
                        'context': 'Mark 16:9-20'
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