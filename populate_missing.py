#!/usr/bin/env python3
import json

def main():
    missing = {
        'pentecostarion': {
            '30': {'0': {'title': 'Monday 30th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 8, 'verses': '7-13', 'text': '', 'context': 'Hebrews 8:7-13'}, {'type': 'gospel', 'book': 'Mark', 'chapter': 8, 'verses': '11-21', 'text': '', 'context': 'Mark 8:11-21'}]}, '1': {'title': 'Tuesday 30th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 9, 'verses': '8-10, 15-23', 'text': '', 'context': 'Hebrews 9:8-10, 15-23'}, {'type': 'gospel', 'book': 'Mark', 'chapter': 8, 'verses': '22-26', 'text': '', 'context': 'Mark 8:22-26'}]}, # Full 30-36...
        },
        'triodion': {
            'publican_pharisee': {'title': 'Publican Pharisee Sunday', 'readings': [{'type': 'epistle', 'book': '2 Timothy', 'chapter': 3, 'verses': '10-15', 'text': '', 'context': '2 Timothy 3:10-15'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 18, 'verses': '10-14', 'text': '', 'context': 'Luke 18:10-14'}]},
            # Full pre-lenten...
        },
        'lent': {
            '1': {'0': {'title': '1st Sunday Lent Orthodoxy', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 11, 'verses': '24-26, 32-12:2a', 'text': '', 'context': 'Hebrews 11:24-26, 32-12:2a'}, {'type': 'gospel', 'book': 'John', 'chapter': 1, 'verses': '43-51', 'text': '', 'context': 'John 1:43-51'}]}, # Full Lent...
        },
        'fixed': {
            'transfiguration': {'title': 'Transfiguration Aug 6', 'readings': [{'type': 'epistle', 'book': '2 Peter', 'chapter': 1, 'verses': '16-19', 'text': '', 'context': '2 Peter 1:16-19'}, {'type': 'gospel', 'book': 'Matthew', 'chapter': 17, 'verses': '1-9', 'text': '', 'context': 'Matthew 17:1-9'}]},
            # Full fixed...
        }
    }
    with open('scripture_readings.json', 'r') as f:
        existing = json.load(f)
    for sec, items in missing.items():
        if sec not in existing:
            existing[sec] = {}
        for k, v in items.items():
            existing[sec][k] = v
    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)
    print('Missing populated.')

if __name__ == '__main__':
    main()
