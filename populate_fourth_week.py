#!/usr/bin/env python3
"""
Populate scripture_readings.json with Fourth Week of Pascha readings.
"""

import json

def main():
    readings = {
        'pascha': {
            '21': {
                'title': 'Fourth Sunday of Pascha: The Paralytic',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 9,
                        'verses': '32-42',
                        'text': '',
                        'context': 'Acts 9:32-42'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 5,
                        'verses': '1-15',
                        'text': '',
                        'context': 'John 5:1-15'
                    }
                ],
                'matins_gospel': {
                    'book': 'Luke',
                    'chapter': 24,
                    'verses': '1-12',
                    'text': """But on the first day of the week, at early dawn, they went to the tomb, taking the spices which they had prepared. And they found the stone rolled away from the tomb, but when they went in they did not find the body. While they were perplexed about this, behold, two men stood by them in dazzling apparel; and as they were frightened and bowed their faces to the ground, the men said to them, "Why do you seek the living among the dead? Remember how he told you, while he was still in Galilee, that the Son of man must be delivered into the hands of sinful men, and be crucified, and on the third day rise." And they remembered his words, and returning from the tomb they told all this to the eleven and to all the rest. Now it was Mary Magdalene and Jo-an'na and Mary the mother of James and the other women with them who told this to the apostles; but these words seemed to them an idle tale, and they did not believe them. But Peter rose and ran to the tomb; stooping and looking in, he saw the linen cloths by themselves; and he went home wondering at what had happened.""",
                    'context': 'Luke 24:1-12'
                }
            },
            '22': {
                'title': 'Monday of Fourth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 10,
                        'verses': '1-16',
                        'text': '',
                        'context': 'Acts 10:1-16'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 6,
                        'verses': '56-69',
                        'text': '',
                        'context': 'John 6:56-69'
                    }
                ]
            },
            '23': {
                'title': 'Tuesday of Fourth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 10,
                        'verses': '21-33',
                        'text': '',
                        'context': 'Acts 10:21-33'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 7,
                        'verses': '1-13',
                        'text': '',
                        'context': 'John 7:1-13'
                    }
                ]
            },
            '24': {
                'title': 'Wednesday of Fourth Week: Mid-Pentecost',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 14,
                        'verses': '6b-18',
                        'text': '',
                        'context': 'Acts 14:6b-18'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 7,
                        'verses': '14-30',
                        'text': '',
                        'context': 'John 7:14-30'
                    }
                ],
                'vespers_paramia': [
                    {
                        'book': 'Micah',
                        'chapter': 4,
                        'verses': '2-3, 5',
                        'text': '',
                        'context': 'Micah 4:2-3, 5'
                    },
                    {
                        'book': 'Isaiah',
                        'chapter': 55,
                        'verses': '1-3, 6-13',
                        'text': '',
                        'context': 'Isaiah 55:1-3, 6-13'
                    },
                    {
                        'book': 'Proverbs',
                        'chapter': 9,
                        'verses': '1-11',
                        'text': '',
                        'context': 'Proverbs 9:1-11'
                    }
                ]
            },
            '25': {
                'title': 'Thursday of Fourth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 10,
                        'verses': '34-43',
                        'text': '',
                        'context': 'Acts 10:34-43'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 8,
                        'verses': '12-20',
                        'text': '',
                        'context': 'John 8:12-20'
                    }
                ]
            },
            '26': {
                'title': 'Friday of Fourth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 10,
                        'verses': '44-11:10',
                        'text': '',
                        'context': 'Acts 10:44-11:10'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 8,
                        'verses': '21-30',
                        'text': '',
                        'context': 'John 8:21-30'
                    }
                ]
            },
            '27': {
                'title': 'Saturday of Fourth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 12,
                        'verses': '1-11',
                        'text': '',
                        'context': 'Acts 12:1-11'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 8,
                        'verses': '31-42a',
                        'text': '',
                        'context': 'John 8:31-42a'
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