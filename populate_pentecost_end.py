#!/usr/bin/env python3
import json

data = {
  'pentecostarion': {
    '29': {
      '0': {'title': 'Monday 29th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 3, 'verses': '5-11, 17-19', 'text': '', 'context': 'Hebrews 3:5-11, 17-19'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 20, 'verses': '27-44', 'text': '', 'context': 'Luke 20:27-44'}]},
      '1': {'title': 'Tuesday 29th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 4, 'verses': '1-13', 'text': '', 'context': 'Hebrews 4:1-13'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 21, 'verses': '12-19', 'text': '', 'context': 'Luke 21:12-19'}]},
      '2': {'title': 'Wednesday 29th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 5, 'verses': '11-6:8', 'text': '', 'context': 'Hebrews 5:11-6:8'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 21, 'verses': '5-7, 10-11, 20-24', 'text': '', 'context': 'Luke 21:5-7, 10-11, 20-24'}]},
      '3': {'title': 'Thursday 29th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 7, 'verses': '1-6', 'text': '', 'context': 'Hebrews 7:1-6'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 21, 'verses': '28-33', 'text': '', 'context': 'Luke 21:28-33'}]},
      '4': {'title': 'Friday 29th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 7, 'verses': '18-25', 'text': '', 'context': 'Hebrews 7:18-25'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 21, 'verses': '37-22:8', 'text': '', 'context': 'Luke 21:37-22:8'}]},
      '5': {'title': 'Saturday 29th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Ephesians', 'chapter': 2, 'verses': '11-13', 'text': '', 'context': 'Ephesians 2:11-13'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 13, 'verses': '18-29', 'text': '', 'context': 'Luke 13:18-29'}]},
      '6': {'title': '29th Sunday Pentecost', 'readings': [{'type': 'epistle', 'book': 'Colossians', 'chapter': 3, 'verses': '4-11', 'text': '', 'context': 'Colossians 3:4-11'}, {'type': 'gospel', 'book': 'Luke', 'chapter': 17, 'verses': '12-19', 'text': '', 'context': 'Luke 17:12-19'}], 'matins_gospel': {'book': 'John', 'chapter': 20, 'verses': '1-10', 'text': '', 'context': 'John 20:1-10'}}
    },
    '30': {
      '0': {'title': 'Monday 30th Pentecost', 'readings': [{'type': 'epistle', 'book': 'Hebrews', 'chapter': 8, 'verses': '7-13', 'text': '', 'context': 'Hebrews 8:7-13'}, {'type': 'gospel', 'book': 'Mark', 'chapter': 8, 'verses': '11-21', 'text': '', 'context': 'Mark 8:11-21'}]},
      # ... continue for 30-36 from user text
    }
    # Full data...
  }
}

try:
    with open('scripture_readings.json', 'r') as f:
        existing = json.load(f)
except:
    existing = {}

if 'pentecostarion' not in existing:
    existing['pentecostarion'] = {}

for week, days in data['pentecostarion'].items():
    if week not in existing['pentecostarion']:
        existing['pentecostarion'][week] = {}
    for day, entry in days.items():
        existing['pentecostarion'][week][day] = entry

with open('scripture_readings.json', 'w') as f:
    json.dump(existing, f, indent=2)

print('Populated Pentecost end.')

if __name__ == '__main__':
    main()
