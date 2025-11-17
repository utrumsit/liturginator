#!/usr/bin/env python3
"""
Populate scripture_readings.json with Sixth Week of Pascha readings.
"""

import json

def main():
    readings = {
        'pascha': {
            '35': {
                'title': 'Sixth Sunday of Pascha: The Blind Man',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 16,
                        'verses': '16-34',
                        'text': '',
                        'context': 'Acts 16:16-34'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 9,
                        'verses': '1-38',
                        'text': '',
                        'context': 'John 9:1-38'
                    }
                ],
                'matins_gospel': {
                    'book': 'John',
                    'chapter': 20,
                    'verses': '19-23',
                    'text': 'Unique test text for Pentecost matins gospel',
                    'context': 'John 20:19-23'
                }
            },
            '36': {
                'title': 'Monday of Sixth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 17,
                        'verses': '1-15',
                        'text': '',
                        'context': 'Acts 17:1-15'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 11,
                        'verses': '47-56',
                        'text': '',
                        'context': 'John 11:47-56'
                    }
                ]
            },
            '37': {
                'title': 'Tuesday of Sixth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 17,
                        'verses': '19-28a',
                        'text': '',
                        'context': 'Acts 17:19-28a'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 12,
                        'verses': '19-36a',
                        'text': '',
                        'context': 'John 12:19-36a'
                    }
                ]
            },
            '38': {
                'title': 'Wednesday of Sixth Week: Leavetaking of Pascha',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 18,
                        'verses': '22-28',
                        'text': '',
                        'context': 'Acts 18:22-28'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 12,
                        'verses': '36-47',
                        'text': '',
                        'context': 'John 12:36-47'
                    }
                ]
            },
            '39': {
                'title': 'Ascension of the Lord',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 1,
                        'verses': '1-12',
                        'text': '',
                        'context': 'Acts 1:1-12'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Luke',
                        'chapter': 24,
                        'verses': '36-53',
                        'text': '',
                        'context': 'Luke 24:36-53'
                    }
                ],
                'matins_gospel': {
                    'book': 'Mark',
                    'chapter': 16,
                    'verses': '9-20',
                    'text': """Now when he rose early on the first day of the week, he appeared first to Mary Magdalene, from whom he had cast out seven demons. She went and told those who had been with him, as they mourned and wept. But when they heard that he was alive and had been seen by her, they would not believe it. After this he appeared in another form to two of them, as they were walking into the country. And they went back and told the rest, but they did not believe them. Afterward he appeared to the eleven themselves as they sat at table; and he upbraided them for their unbelief and hardness of heart, because they had not believed those who saw him after he had risen. And he said to them, "Go into all the world and preach the gospel to the whole creation. He who believes and is baptized will be saved; but he who does not believe will be condemned. And these signs will accompany those who believe: in my name they will cast out demons; they will speak in new tongues; they will pick up serpents, and if they drink any deadly thing, it will not hurt them; they will lay their hands on the sick, and they will recover." So then the Lord Jesus, after he had spoken to them, was taken up into heaven, and sat down at the right hand of God. And they went forth and preached everywhere, while the Lord worked with them and confirmed the message by the accompanying signs.""",
                    'context': 'Mark 16:9-20'
                },
                'vespers_paramia': [
                    {
                        'book': 'Isaiah',
                        'chapter': 2,
                        'verses': '2-3, 5',
                        'text': '',
                        'context': 'Isaiah 2:2-3, 5'
                    },
                    {
                        'book': 'Isaiah',
                        'chapter': 62,
                        'verses': '10-63:3, 7-9',
                        'text': '',
                        'context': 'Isaiah 62:10-63:3, 7-9'
                    },
                    {
                        'book': 'Zechariah',
                        'chapter': 14,
                        'verses': '1, 4, 8-11',
                        'text': '',
                        'context': 'Zechariah 14:1, 4, 8-11'
                    }
                ]
            },
            '40': {
                'title': 'Friday of Sixth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 19,
                        'verses': '1-8',
                        'text': '',
                        'context': 'Acts 19:1-8'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 14,
                        'verses': '1-11a',
                        'text': '',
                        'context': 'John 14:1-11a'
                    }
                ]
            },
            '41': {
                'title': 'Saturday of Sixth Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 20,
                        'verses': '7-12',
                        'text': '',
                        'context': 'Acts 20:7-12'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 14,
                        'verses': '10b-21',
                        'text': '',
                        'context': 'John 14:10b-21'
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