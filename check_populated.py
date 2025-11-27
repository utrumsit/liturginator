#!/usr/bin/env python3
import json

def check_populated():
    with open('scripture_readings.json', 'r') as f:
        data = json.load(f)

    missing = []

    # Pentecostarion: weeks 1-36, days 0-6
    if 'pentecostarion' in data:
        for week in range(1, 37):
            week_str = str(week)
            if week_str not in data['pentecostarion']:
                missing.append(f'pentecostarion {week_str}')
            else:
                for day in range(7):
                    day_str = str(day)
                    if day_str not in data['pentecostarion'][week_str]:
                        missing.append(f'pentecostarion {week_str} day {day_str}')

    # Triodion: check specific keys
    triodion_keys = ['publican_pharisee', 'prodigal_son', 'meatfare', 'cheesefare'] + [str(w) for w in range(34, 37)] + [f'lent_{w}' for w in range(1, 7)]
    if 'triodion' in data:
        for key in triodion_keys:
            if key not in data['triodion']:
                missing.append(f'triodion {key}')
            elif key.isdigit() or key.startswith('lent_'):
                for day in range(7):
                    day_str = str(day)
                    if day_str not in data['triodion'][key]:
                        missing.append(f'triodion {key} day {day_str}')

    # Lent: weeks 1-6, days 0-6
    if 'lent' in data:
        for week in range(1, 7):
            week_str = str(week)
            if week_str not in data['lent']:
                missing.append(f'lent {week_str}')
            else:
                for day in range(7):
                    day_str = str(day)
                    if day_str not in data['lent'][week_str]:
                        missing.append(f'lent {week_str} day {day_str}')

    # Holy Week: specific days
    holy_days = ['lazarus', 'palm']
    if 'holy_week' in data:
        for day in holy_days:
            if day not in data['holy_week']:
                missing.append(f'holy_week {day}')

    # Fixed: check some major ones
    fixed_keys = ['nativity_theotokos', 'exaltation_cross', 'protection_theotokos', 'entry_theotokos', 'st_nicholas', 'nativity_christ', 'circumcision', 'theophany', 'meeting_lord', 'annunciation', 'nativity_john', 'peter_paul', 'transfiguration', 'dormition', 'beheading_john']
    if 'fixed' in data:
        for key in fixed_keys:
            if key not in data['fixed']:
                missing.append(f'fixed {key}')

    if missing:
        print('Missing entries:')
        for m in missing:
            print(m)
    else:
        print('All expected entries are populated.')

if __name__ == '__main__':
    check_populated()
