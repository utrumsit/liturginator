#!/usr/bin/env python3
"""
Add missing Sundays to Pentecostarion weeks.
"""

import json

# Sundays readings
sundays = {
    1: {'epistle': ('Hebrews', 11, '33-12:2a'), 'gospel': ('Matthew', 10, '32-33, 37-38; 19:27-30'), 'matins': ('Matthew', 28, '16-20'), 'vespers': [('Isaiah', 43, '9-14a'), ('Wisdom', 3, '1-9'), ('Wisdom', 5, '15-6:3')]},
    4: {'epistle': ('Romans', 2, '10-16'), 'gospel': ('Matthew', 4, '18-23'), 'matins': ('Luke', 24, '1-12')},
    5: {'epistle': ('Romans', 10, '1-10'), 'gospel': ('Matthew', 8, '28-9:1'), 'matins': ('Luke', 24, '12-35')},
    6: {'epistle': ('Romans', 12, '6-14'), 'gospel': ('Matthew', 9, '1-8'), 'matins': ('Luke', 24, '36-53')},
    7: {'epistle': ('Romans', 15, '1-7'), 'gospel': ('Matthew', 9, '27-35'), 'matins': ('John', 20, '1-10')},
    8: {'epistle': ('1 Corinthians', 1, '10-18'), 'gospel': ('Matthew', 14, '14-22'), 'matins': ('John', 20, '11-18')},
    9: {'epistle': ('1 Corinthians', 3, '9-17'), 'gospel': ('Matthew', 17, '14-23'), 'matins': ('John', 20, '19-31')},
    10: {'epistle': ('1 Corinthians', 4, '9-16'), 'gospel': ('Matthew', 20, '1-16'), 'matins': ('John', 21, '1-14')},
    11: {'epistle': ('1 Corinthians', 9, '2-12'), 'gospel': ('Matthew', 22, '15-22'), 'matins': ('Matthew', 28, '16-20')},
    12: {'epistle': ('2 Corinthians', 6, '16-7:1'), 'gospel': ('Mark', 1, '35-44'), 'matins': ('Mark', 16, '1-8')},
    13: {'epistle': ('2 Corinthians', '8', '7-15'), 'gospel': ('Mark', 6, '45-53'), 'matins': ('Mark', 16, '9-20')},
    14: {'epistle': ('2 Corinthians', 9, '12-10:7'), 'gospel': ('Mark', 8, '1-10'), 'matins': ('Luke', 24, '1-12')},
    15: {'epistle': ('2 Corinthians', 10, '7-18'), 'gospel': ('Mark', 8, '34-9:1'), 'matins': ('Luke', 24, '12-35')},
    16: {'epistle': ('2 Corinthians', 11, '21-30'), 'gospel': ('Mark', 10, '2-12'), 'matins': ('Luke', 24, '36-53')},
    17: {'epistle': ('2 Corinthians', 11, '31-12:9'), 'gospel': ('Mark', 10, '24-32'), 'matins': ('John', 20, '1-10')},
    18: {'epistle': ('Ephesians', 2, '4-10'), 'gospel': ('Mark', 10, '46-52'), 'matins': ('John', 20, '11-18')},
    19: {'epistle': ('Ephesians', 2, '14-22'), 'gospel': ('Mark', 12, '28-37'), 'matins': ('John', 20, '19-31')},
    20: {'epistle': ('Ephesians', 4, '17-25'), 'gospel': ('Luke', 4, '1-15'), 'matins': ('John', 21, '1-14')},
    21: {'epistle': ('Ephesians', 4, '25-32'), 'gospel': ('Luke', 5, '12-16'), 'matins': ('Matthew', 28, '16-20')},
    22: {'epistle': ('Ephesians', 5, '1-8'), 'gospel': ('Luke', 6, '17-23'), 'matins': ('Mark', 16, '1-8')},
    23: {'epistle': ('Ephesians', 5, '8-19'), 'gospel': ('Luke', 6, '24-30'), 'matins': ('Mark', 16, '9-20')},
    24: {'epistle': ('Ephesians', 5, '20-26'), 'gospel': ('Luke', 8, '1-3'), 'matins': ('Luke', 24, '1-12')},
    25: {'epistle': ('Ephesians', 5, '25-32'), 'gospel': ('Luke', 8, '16-21'), 'matins': ('Luke', 24, '12-35')},
    26: {'epistle': ('Ephesians', 6, '10-17'), 'gospel': ('Luke', 9, '18-22'), 'matins': ('Luke', 24, '36-53')},
    27: {'epistle': ('Ephesians', 6, '18-24'), 'gospel': ('Luke', 9, '44-50'), 'matins': ('John', 20, '1-10')},
    28: {'epistle': ('Colossians', 1, '12-18'), 'gospel': ('Luke', 12, '48-56'), 'matins': ('John', 20, '11-18')},
    29: {'epistle': ('2 Corinthians', 9, '6-11'), 'gospel': ('Luke', 8, '41-56'), 'matins': ('John', 20, '19-31')}
}

def main():
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}
    if 'pentecostarion' not in existing:
        existing['pentecostarion'] = {}
    for week, data in sundays.items():
        if str(week) not in existing['pentecostarion']:
            existing['pentecostarion'][str(week)] = {}
        eb, ec, ev = data['epistle']
        gb, gc, gv = data['gospel']
        mb, mc, mv = data['matins']
        sunday_data = {
            'title': f'{week}{"st" if week==1 else "nd" if week==2 else "rd" if week==3 else "th"} Sunday after Pentecost',
            'readings': [
                {'type': 'epistle', 'book': eb, 'chapter': ec, 'verses': ev, 'text': '', 'context': f'{eb} {ec}:{ev}'},
                {'type': 'gospel', 'book': gb, 'chapter': gc, 'verses': gv, 'text': '', 'context': f'{gb} {gc}:{gv}'}
            ],
            'matins_gospel': {'book': mb, 'chapter': mc, 'verses': mv, 'text': '', 'context': f'{mb} {mc}:{mv}'}
        }
        if 'vespers' in data:
            sunday_data['vespers_paramia'] = [
                {'book': b, 'chapter': c, 'verses': v, 'text': '', 'context': f'{b} {c}:{v}'} for b, c, v in data['vespers']
            ]
        existing['pentecostarion'][str(week)]['6'] = sunday_data
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)

if __name__ == '__main__':
    main()