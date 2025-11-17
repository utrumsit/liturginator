#!/usr/bin/env python3
"""
Populate scripture_readings.json with Second Week of Pascha readings.
"""

import json

def main():
    readings = {
        'pascha': {
            '7': {
                'title': 'Second Sunday of Pascha: Thomas Sunday',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 5,
                        'verses': '12-20',
                        'text': '',
                        'context': 'Acts 5:12-20'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 20,
                        'verses': '19-31',
                        'text': '',
                        'context': 'John 20:19-31'
                    }
                ],
                'matins_gospel': {
                    'book': 'Matthew',
                    'chapter': 28,
                    'verses': '16-20',
                    'text': 'Now the eleven disciples went to Galilee, to the mountain to which Jesus had directed them. And when they saw him they worshiped him; but some doubted. And Jesus came and said to them, \"All authority in heaven and on earth has been given to me. Go therefore and make disciples of all nations, baptizing them in the name of the Father and of the Son and of the Holy Spirit, teaching them to observe all that I have commanded you; and lo, I am with you always, to the close of the age.\"',
                    'context': 'Matthew 28:16-20'
                }
            },
            '8': {
                'title': 'Monday of Second Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 3,
                        'verses': '19-26',
                        'text': '',
                        'context': 'Acts 3:19-26'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 2,
                        'verses': '1-11',
                        'text': '',
                        'context': 'John 2:1-11'
                    }
                ]
            },
            '9': {
                'title': 'Tuesday of Second Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 4,
                        'verses': '1-10',
                        'text': '',
                        'context': 'Acts 4:1-10'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 3,
                        'verses': '16-21',
                        'text': '',
                        'context': 'John 3:16-21'
                    }
                ]
            },
            '10': {
                'title': 'Wednesday of Second Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 4,
                        'verses': '13-22',
                        'text': '',
                        'context': 'Acts 4:13-22'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 5,
                        'verses': '17b-24',
                        'text': '',
                        'context': 'John 5:17b-24'
                    }
                ]
            },
            '11': {
                'title': 'Thursday of Second Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 4,
                        'verses': '23-31',
                        'text': '',
                        'context': 'Acts 4:23-31'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 5,
                        'verses': '24-30',
                        'text': '',
                        'context': 'John 5:24-30'
                    }
                ]
            },
            '12': {
                'title': 'Friday of Second Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 5,
                        'verses': '1-11',
                        'text': '',
                        'context': 'Acts 5:1-11'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 5,
                        'verses': '30b-6:2',
                        'text': '',
                        'context': 'John 5:30b-6:2'
                    }
                ]
            },
            '13': {
                'title': 'Saturday of Second Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 5,
                        'verses': '21-33',
                        'text': '',
                        'context': 'Acts 5:21-33'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 6,
                        'verses': '14-27',
                        'text': '',
                        'context': 'John 6:14-27'
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