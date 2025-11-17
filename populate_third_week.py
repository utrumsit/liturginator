#!/usr/bin/env python3
"""
Populate scripture_readings.json with Third Week of Pascha readings.
"""

import json

def main():
    readings = {
        'pascha': {
            '14': {
                'title': 'Third Sunday of Pascha: Myrrh-bearing Women',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 6,
                        'verses': '1-7',
                        'text': '',
                        'context': 'Acts 6:1-7'
                    },
                    {
                        'type': 'gospel',
                        'book': 'Mark',
                        'chapter': 15,
                        'verses': '43-16:8',
                        'text': '',
                        'context': 'Mark 15:43-16:8'
                    }
                ],
                'matins_gospel': {
                    'book': 'Mark',
                    'chapter': 16,
                    'verses': '9-20',
                    'text': 'Now when he rose early on the first day of the week, he appeared first to Mary Magdalene, from whom he had cast out seven demons. She went and told those who had been with him, as they mourned and wept. But when they heard that he was alive and had been seen by her, they would not believe it. After this he appeared in another form to two of them, as they were walking into the country. And they went back and told the rest, but they did not believe them. Afterward he appeared to the eleven themselves as they sat at table; and he upbraided them for their unbelief and hardness of heart, because they had not believed those who saw him after he had risen. And he said to them, \"Go into all the world and preach the gospel to the whole creation. He who believes and is baptized will be saved; but he who does not believe will be condemned. And these signs will accompany those who believe: in my name they will cast out demons; they will speak in new tongues; they will pick up serpents, and if they drink any deadly thing, it will not hurt them; they will lay their hands on the sick, and they will recover.\" So then the Lord Jesus, after he had spoken to them, was taken up into heaven, and sat down at the right hand of God. And they went forth and preached everywhere, while the Lord worked with them and confirmed the message by the accompanying signs.',
                    'context': 'Mark 16:9-20'
                }
            },
            '15': {
                'title': 'Monday of Third Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 6,
                        'verses': '8-7:5a, 47-60',
                        'text': '',
                        'context': 'Acts 6:8-7:5a, 47-60'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 4,
                        'verses': '46b-54',
                        'text': '',
                        'context': 'John 4:46b-54'
                    }
                ]
            },
            '16': {
                'title': 'Tuesday of Third Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 8,
                        'verses': '5-17',
                        'text': '',
                        'context': 'Acts 8:5-17'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 6,
                        'verses': '27-33',
                        'text': '',
                        'context': 'John 6:27-33'
                    }
                ]
            },
            '17': {
                'title': 'Wednesday of Third Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 8,
                        'verses': '18-25',
                        'text': '',
                        'context': 'Acts 8:18-25'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 6,
                        'verses': '35-39',
                        'text': '',
                        'context': 'John 6:35-39'
                    }
                ]
            },
            '18': {
                'title': 'Thursday of Third Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 8,
                        'verses': '26-39',
                        'text': '',
                        'context': 'Acts 8:26-39'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 6,
                        'verses': '40-44',
                        'text': '',
                        'context': 'John 6:40-44'
                    }
                ]
            },
            '19': {
                'title': 'Friday of Third Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 8,
                        'verses': '40-9:19a',
                        'text': '',
                        'context': 'Acts 8:40-9:19a'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 6,
                        'verses': '48-54',
                        'text': '',
                        'context': 'John 6:48-54'
                    }
                ]
            },
            '20': {
                'title': 'Saturday of Third Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 9,
                        'verses': '19-31',
                        'text': '',
                        'context': 'Acts 9:19-31'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 15,
                        'verses': '17-16:2',
                        'text': '',
                        'context': 'John 15:17-16:2'
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