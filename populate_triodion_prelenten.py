#!/usr/bin/env python3
import json

def main():
    readings = {
        'triodion': {
            'publican_pharisee': {'title': 'Sunday of the Publican and Pharisee', 'readings': [{'type': 'epistle', 'book': '2 Timothy', 'chapter': 3, 'verses': '10-15', 'text': '', 'context': '2 Timothy 3:10-15'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 18, 'verses': '10-14', 'text': '', 'context': 'Luke 18:10-14'}]},
            'prodigal_son': {'title': 'Sunday of the Prodigal Son', 'readings': [{'type': 'epistle', 'book': '1 Corinthians', 'chapter': 6, 'verses': '12-20', 'text': '', 'context': '1 Corinthians 6:12-20'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 15, 'verses': '11-32', 'text': '', 'context': 'Luke 15:11-32'}]},
            'meatfare': {'title': 'Meatfare Sunday: Last Judgment', 'readings': [{'type': 'epistle', 'book': '1 Corinthians', 'chapter': 8, 'verses': '8-9:2', 'text': '', 'context': '1 Corinthians 8:8-9:2'}, {'type': 'gospel', 'book': 'Matthew', 'chapter': 25, 'verses': '31-46', 'text': '', 'context': 'Matthew 25:31-46'}]},
            'cheesefare': {'title': 'Cheesefare Sunday: Forgiveness', 'readings': [{'type': 'epistle', 'book': 'Romans', 'chapter': 13, 'verses': '11b-14:4', 'text': '', 'context': 'Romans 13:11b-14:4'}, {'type': 'gospel', 'book': 'Matthew', 'chapter': 6, 'verses': '14-21', 'text': '', 'context': 'Matthew 6:14-21'}]},
            'lent1': {
                '0': {'title': '1st Sunday Lent: Orthodoxy', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 11, 'verses': '24-26, 32-12:2a', 'text': '', 'context': 'Hebrews 11:24-26, 32-12:2a'}, {'type': 'gospel', 'book': 'John', 'chapter': 1, 'verses': '43-51', 'text': '', 'context': 'John 1:43-51'}]},
                # Add days 1-6 Mon-Sat from mci
            },
            # Continue for Lent weeks 2-6...
        }
    }
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}
    if 'triodion' not in existing:
        existing['triodion'] = {}
    existing['triodion'].update({k: v for weeks in readings['triodion'].values() for k, v in weeks.items() if isinstance(weeks, dict)})
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)
    print('Populated Triodion.')

if __name__ == '__main__':
    main()
