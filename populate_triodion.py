#!/usr/bin/env python3
\"\"\"Populate triodion pre-lenten + Lent weeks.\"\"\"
import json

def main():
    readings = {
        'triodion': {
            'publican_pharisee': {'title': 'Sunday of the Publican and Pharisee', 'readings': [{'type': 'epistle', 'book': '2 Timothy', 'chapter': 3, 'verses': '10-15', 'text': '', 'context': '2 Timothy 3:10-15'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 18, 'verses': '10-14', 'text': '', 'context': 'Luke 18:10-14'}]},
            '34': {  # Pre-lenten week 34
                '0': {'title': 'Monday of 34th Week (Publican/Pharisee)', 'readings': [{'type': 'epistle', 'book': '2 Peter', 'chapter': 1, 'verses': '20-2:9', 'text': '', 'context': '2 Peter 1:20-2:9'}, {'type': 'gospel', 'book': 'Mark', 'chapter': 13, 'verses': '9-13', 'text': '', 'context': 'Mark 13:9-13'}]},
                # Add other days...
            },
            # Add Meatfare, Cheesefare Sundays, Lent weeks 1-6 similarly from mci
        }
    }
    # Merge logic same as populate_pentecost_30to36.py
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}
    if 'triodion' not in existing:
        existing['triodion'] = {}
    existing['triodion'].update(readings['triodion'])
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)
    print('Populated Triodion.')

if __name__ == '__main__':
    main()
