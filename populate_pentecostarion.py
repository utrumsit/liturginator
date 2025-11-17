#!/usr/bin/env python3
"""
Populate scripture_readings.json with Pentecostarion Sundays 1-29.
"""

import json

def main():
    # Gospels
    matthew_gospels = [
        ("Matthew", 4, "18-23"),
        ("Matthew", 4, "25-5:12"),
        ("Matthew", 6, "22-33"),
        ("Matthew", 8, "5-13"),
        ("Matthew", 8, "28-9:1"),
        ("Matthew", 9, "9-13"),
        ("Matthew", 9, "27-35"),
        ("Matthew", 14, "14-22"),
        ("Matthew", 17, "14-23"),
        ("Matthew", 20, "1-16"),
        ("Matthew", 22, "2-14")
    ]
    mark_gospels = [
        ("Mark", 1, "23-28"),
        ("Mark", 2, "23-3:5"),
        ("Mark", 4, "24-34"),
        ("Mark", 6, "1-7"),
        ("Mark", 7, "14-24"),
        ("Mark", 8, "11-21"),
        ("Mark", 8, "34-9:1"),
        ("Mark", 10, "2-12"),
        ("Mark", 10, "24-32"),
        ("Mark", 12, "13-17"),
        ("Mark", 12, "28-37")
    ]
    luke_gospels = [
        ("Luke", 5, "1-11"),
        ("Luke", 6, "31-36"),
        ("Luke", 7, "11-16"),
        ("Luke", 8, "5-15"),
        ("Luke", 8, "26-39"),
        ("Luke", 16, "19-31"),
        ("Luke", 8, "41-56"),
        ("Luke", 10, "25-37"),
        ("Luke", 12, "16-21"),
        ("Luke", 13, "10-17"),
        ("Luke", 14, "1-11")
    ]

    # Epistles
    epistles_matt = [
        ("Romans", 12, "6-14"),
        ("Romans", 13, "1-10"),
        ("Romans", 14, "10-19"),
        ("Romans", 15, "1-7"),
        ("Romans", 15, "17-29"),
        ("Romans", 16, "1-16"),
        ("1 Corinthians", 1, "10-18"),
        ("1 Corinthians", 1, "26-29"),
        ("1 Corinthians", 2, "6-9"),
        ("1 Corinthians", 3, "18-23"),
        ("1 Corinthians", 4, "9-16")
    ]
    epistles_mark = [
        ("1 Corinthians", 9, "2-12"),
        ("1 Corinthians", 10, "12-22"),
        ("1 Corinthians", 11, "23-32"),
        ("1 Corinthians", 12, "7-11"),
        ("1 Corinthians", 13, "4-13"),
        ("1 Corinthians", 14, "20-25"),
        ("1 Corinthians", 15, "12-19"),
        ("1 Corinthians", 15, "39-45"),
        ("1 Corinthians", 16, "4-12"),
        ("2 Corinthians", 1, "21-24"),
        ("2 Corinthians", 2, "3-15")
    ]
    epistles_luke = [
        ("2 Corinthians", 4, "6-15"),
        ("2 Corinthians", 5, "1-10"),
        ("2 Corinthians", 5, "15-21"),
        ("2 Corinthians", 6, "1-10"),
        ("2 Corinthians", 6, "16-7:1"),
        ("2 Corinthians", 8, "1-5"),
        ("2 Corinthians", 9, "6-11"),
        ("2 Corinthians", 9, "12-10:7"),
        ("2 Corinthians", 10, "7-18"),
        ("2 Corinthians", 11, "5-21"),
        ("2 Corinthians", 11, "31-12:9")
    ]

    readings = {'pentecostarion': {}}

    # Matthew cycle (1-11)
    readings['pentecostarion']['1'] = {}
    for i in range(11):
        eb, ec, ev = epistles_matt[i]
        gb, gc, gv = matthew_gospels[i]
        readings['pentecostarion']['1'][str(i+1)] = [
            {
                'type': 'epistle',
                'book': eb,
                'chapter': ec,
                'verses': ev,
                'text': '',
                'context': f'{eb} {ec}:{ev}'
            },
            {
                'type': 'gospel',
                'book': gb,
                'chapter': gc,
                'verses': gv,
                'text': '',
                'context': f'{gb} {gc}:{gv}'
            }
        ]

    # Mark cycle (12-22)
    readings['pentecostarion']['2'] = {}
    for i in range(11):
        eb, ec, ev = epistles_mark[i]
        gb, gc, gv = mark_gospels[i]
        readings['pentecostarion']['2'][str(i+1)] = [
            {
                'type': 'epistle',
                'book': eb,
                'chapter': ec,
                'verses': ev,
                'text': '',
                'context': f'{eb} {ec}:{ev}'
            },
            {
                'type': 'gospel',
                'book': gb,
                'chapter': gc,
                'verses': gv,
                'text': '',
                'context': f'{gb} {gc}:{gv}'
            }
        ]

    # Luke cycle (23-33)
    readings['pentecostarion']['3'] = {}
    for i in range(11):
        eb, ec, ev = epistles_luke[i]
        gb, gc, gv = luke_gospels[i]
        readings['pentecostarion']['3'][str(i+1)] = [
            {
                'type': 'epistle',
                'book': eb,
                'chapter': ec,
                'verses': ev,
                'text': '',
                'context': f'{eb} {ec}:{ev}'
            },
            {
                'type': 'gospel',
                'book': gb,
                'chapter': gc,
                'verses': gv,
                'text': '',
                'context': f'{gb} {gc}:{gv}'
            }
        ]

    # Load existing and merge
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}
    if 'pentecostarion' not in existing:
        existing['pentecostarion'] = {}
    existing['pentecostarion'].update(readings['pentecostarion'])
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)

if __name__ == '__main__':
    main()