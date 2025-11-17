#!/usr/bin/env python3
"""
Populate scripture_readings.json with Seventh Week of Pascha readings.
"""

import json

def main():
    readings = {
        'pascha': {
            '42': {
                'title': 'Seventh Sunday of Pascha: Fathers of the 1st Council',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 20,
                        'verses': '16-18a, 28-36',
                        'text': '',
                        'context': 'Acts 20:16-18a, 28-36'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 17,
                        'verses': '1-13',
                        'text': '',
                        'context': 'John 17:1-13'
                    }
                ],
                'matins_gospel': {
                    'book': 'John',
                    'chapter': 21,
                    'verses': '1-14',
                    'text': """After this Jesus revealed himself again to the disciples by the Sea of Tibe'ri-as; and he revealed himself in this way. Simon Peter, Thomas called the Twin, Nathan'a-el of Cana in Galilee, the sons of Zeb'edee, and two others of his disciples were together. Simon Peter said to them, "I am going fishing." They said to him, "We will go with you." They went out and got into the boat; but that night they caught nothing. Just as day was breaking, Jesus stood on the beach; yet the disciples did not know that it was Jesus. Jesus said to them, "Children, have you any fish?" They answered him, "No." He said to them, "Cast the net on the right side of the boat, and you will find some." So they cast it, and now they were not able to haul it in, for the quantity of fish. That disciple whom Jesus loved said to Peter, "It is the Lord!" When Simon Peter heard that it was the Lord, he put on his clothes, for he was stripped for work, and sprang into the sea. But the other disciples came in the boat, dragging the net full of fish, for they were not far from the land, but about a hundred yards off. When they got out on land, they saw a charcoal fire there, with fish lying on it, and bread. Jesus said to them, "Bring some of the fish that you have just caught." So Simon Peter went aboard and hauled the net ashore, full of large fish, a hundred and fifty-three of them; and although there were so many, the net was not torn. Jesus said to them, "Come and have breakfast." Now none of the disciples dared ask him, "Who are you?" They knew it was the Lord. Jesus came and took the bread and gave it to them, and so with the fish. This was now the third time that Jesus was revealed to the disciples after he was raised from the dead.""",
                    'context': 'John 21:1-14'
                },
                'vespers_paramia': [
                    {
                        'book': 'Genesis',
                        'chapter': 14,
                        'verses': '14-20',
                        'text': '',
                        'context': 'Genesis 14:14-20'
                    },
                    {
                        'book': 'Deuteronomy',
                        'chapter': 1,
                        'verses': '8-11, 15-17',
                        'text': '',
                        'context': 'Deuteronomy 1:8-11, 15-17'
                    },
                    {
                        'book': 'Deuteronomy',
                        'chapter': 10,
                        'verses': '14-21',
                        'text': '',
                        'context': 'Deuteronomy 10:14-21'
                    }
                ]
            },
            '43': {
                'title': 'Monday of Seventh Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 21,
                        'verses': '8-14',
                        'text': '',
                        'context': 'Acts 21:8-14'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 14,
                        'verses': '27b-15:7',
                        'text': '',
                        'context': 'John 14:27b-15:7'
                    }
                ]
            },
            '44': {
                'title': 'Tuesday of Seventh Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 21,
                        'verses': '26-32',
                        'text': '',
                        'context': 'Acts 21:26-32'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 16,
                        'verses': '2b-13a',
                        'text': '',
                        'context': 'John 16:2b-13a'
                    }
                ]
            },
            '45': {
                'title': 'Wednesday of Seventh Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 23,
                        'verses': '1-11',
                        'text': '',
                        'context': 'Acts 23:1-11'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 16,
                        'verses': '15-23',
                        'text': '',
                        'context': 'John 16:15-23'
                    }
                ]
            },
            '46': {
                'title': 'Thursday of Seventh Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 25,
                        'verses': '13-19',
                        'text': '',
                        'context': 'Acts 25:13-19'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 16,
                        'verses': '23b-33a',
                        'text': '',
                        'context': 'John 16:23b-33a'
                    }
                ]
            },
            '47': {
                'title': 'Friday of Seventh Week',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 27,
                        'verses': '1-44',
                        'text': '',
                        'context': 'Acts 27:1-44'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 17,
                        'verses': '18-26',
                        'text': '',
                        'context': 'John 17:18-26'
                    }
                ]
            },
            '48': {
                'title': 'Saturday of Seventh Week: Trinity Saturday',
                'readings': [
                    {
                        'type': 'epistle',
                        'book': 'Acts',
                        'chapter': 28,
                        'verses': '1-31',
                        'text': '',
                        'context': 'Acts 28:1-31'
                    },
                    {
                        'type': 'gospel',
                        'book': 'John',
                        'chapter': 21,
                        'verses': '15-25',
                        'text': '',
                        'context': 'John 21:15-25'
                    },
                    {
                        'type': 'epistle',
                        'book': '1 Thessalonians',
                        'chapter': 4,
                        'verses': '13-17',
                        'text': '',
                        'context': '1 Thessalonians 4:13-17'
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