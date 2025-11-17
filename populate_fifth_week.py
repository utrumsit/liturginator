#!/usr/bin/env python3
"""
Populate scripture_readings.json with Fifth Week of Pascha readings.
"""

import json

def main():
    readings = {
        'pascha': {
            '28': {
                'title': 'Fifth Sunday of Pascha: The Samaritan Woman',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 11,
                        'verses': '19-26, 29-30',
                        'text': '',
                        'context': 'Acts 11:19-26, 29-30'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 4,
                        'verses': '5-42',
                        'text': '',
                        'context': 'John 4:5-42'
                    }
                ],
                'matins_gospel': {
                    'book': 'John',
                    'chapter': 20,
                    'verses': '1-10',
                    'text': """Now on the first day of the week Mary Mag'dalene came to the tomb early, while it was still dark, and saw that the stone had been taken away from the tomb. So she ran, and went to Simon Peter and the other disciple, the one whom Jesus loved, and said to them, "They have taken the Lord out of the tomb, and we do not know where they have laid him." Peter then came out with the other disciple, and they went toward the tomb. They both ran, but the other disciple outran Peter and reached the tomb first; and stooping to look in, he saw the linen cloths lying there, but he did not go in. Then Simon Peter came, following him, and went into the tomb; he saw the linen cloths lying, and the napkin, which had been on his head, not lying with the linen cloths but rolled up in a place by itself. Then the other disciple, who reached the tomb first, also went in, and he saw and believed; for as yet they did not know the scripture, that he must rise from the dead. Then the disciples went back to their homes.""",
                    'context': 'John 20:1-10'
                }
            },
            '29': {
                'title': 'Monday of Fifth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 12,
                        'verses': '12-17',
                        'text': '',
                        'context': 'Acts 12:12-17'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 8,
                        'verses': '42-51',
                        'text': '',
                        'context': 'John 8:42-51'
                    }
                ]
            },
            '30': {
                'title': 'Tuesday of Fifth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 12,
                        'verses': '25-13:12',
                        'text': '',
                        'context': 'Acts 12:25-13:12'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 8,
                        'verses': '51-59',
                        'text': '',
                        'context': 'John 8:51-59'
                    }
                ]
            },
            '31': {
                'title': 'Wednesday of Fifth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 13,
                        'verses': '13-24',
                        'text': '',
                        'context': 'Acts 13:13-24'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 6,
                        'verses': '5-14',
                        'text': '',
                        'context': 'John 6:5-14'
                    }
                ]
            },
            '32': {
                'title': 'Thursday of Fifth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 14,
                        'verses': '20b-27',
                        'text': '',
                        'context': 'Acts 14:20b-27'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 9,
                        'verses': '39-10:9',
                        'text': '',
                        'context': 'John 9:39-10:9'
                    }
                ]
            },
            '33': {
                'title': 'Friday of Fifth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 15,
                        'verses': '5-34',
                        'text': '',
                        'context': 'Acts 15:5-34'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 10,
                        'verses': '17-28',
                        'text': '',
                        'context': 'John 10:17-28'
                    }
                ]
            },
            '34': {
                'title': 'Saturday of Fifth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 15,
                        'verses': '35-41',
                        'text': '',
                        'context': 'Acts 15:35-41'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 10,
                        'verses': '27-38',
                        'text': '',
                        'context': 'John 10:27-38'
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