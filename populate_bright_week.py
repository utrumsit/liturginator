#!/usr/bin/env python3
"""
Populate scripture_readings.json with Bright Week readings.
"""

import json

def main():
    readings = {
        'pascha': {
            '0': {
                'title': 'Pascha',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 1,
                        'verses': '1-8',
                        'text': '',
                        'context': 'Acts 1:1-8'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 1,
                        'verses': '1-17',
                        'text': '',
                        'context': 'John 1:1-17'
                    }
                ]
            },
            '1': {
                'title': 'Monday of Bright Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 1,
                        'verses': '12-17, 21-26',
                        'text': '',
                        'context': 'Acts 1:12-17, 21-26'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 1,
                        'verses': '18-28',
                        'text': '',
                        'context': 'John 1:18-28'
                    }
                ]
            },
            '2': {
                'title': 'Tuesday of Bright Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 2,
                        'verses': '14-21',
                        'text': '',
                        'context': 'Acts 2:14-21'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Luke',
                        'chapter': 24,
                        'verses': '12-35',
                        'text': '',
                        'context': 'Luke 24:12-35'
                    }
                ]
            },
            '3': {
                'title': 'Wednesday of Bright Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 2,
                        'verses': '22-36',
                        'text': '',
                        'context': 'Acts 2:22-36'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 1,
                        'verses': '35-51',
                        'text': '',
                        'context': 'John 1:35-51'
                    }
                ]
            },
            '4': {
                'title': 'Thursday of Bright Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 2,
                        'verses': '38-43',
                        'text': '',
                        'context': 'Acts 2:38-43'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 3,
                        'verses': '1-15',
                        'text': '',
                        'context': 'John 3:1-15'
                    }
                ]
            },
            '5': {
                'title': 'Friday of Bright Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 3,
                        'verses': '1-8',
                        'text': '',
                        'context': 'Acts 3:1-8'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 2,
                        'verses': '12-22',
                        'text': '',
                        'context': 'John 2:12-22'
                    }
                ]
            },
            '6': {
                'title': 'Saturday of Bright Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 3,
                        'verses': '11-16',
                        'text': '',
                        'context': 'Acts 3:11-16'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 3,
                        'verses': '22-33',
                        'text': '',
                        'context': 'John 3:22-33'
                    }
                ]
            }
        }
    }
    with open('scripture_readings.json', 'w') as f:
        json.dump(readings, f, indent=2)

if __name__ == '__main__':
    main()