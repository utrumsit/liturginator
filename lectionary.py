#!/usr/bin/env python3
"""
Lectionary query by date: calculates pascha, determines season/week/day, checks fixed feasts, returns readings.
"""
import json
import datetime
from pascha import calculate_pascha as pascha_date

def get_readings(date):
    """
    date: datetime.date
    Returns: dict with 'title', 'readings' (list of dicts), 'vespers_paramia' (list), 'matins_gospel' (dict), etc.
    """
    year = date.year
    pascha = pascha_date(year)
    days_since_pascha = (date - pascha).days

    with open('scripture_readings.json', 'r') as f:
        data = json.load(f)

    # Check fixed feasts first (priority)
    fixed_dates = {
        datetime.date(year, 9, 8): 'nativity_theotokos',
        datetime.date(year, 9, 14): 'exaltation_cross',
        datetime.date(year, 10, 1): 'protection_theotokos',
        datetime.date(year, 11, 21): 'entry_theotokos',
        datetime.date(year, 12, 6): 'st_nicholas',
        datetime.date(year, 12, 25): 'nativity_christ',
        datetime.date(year, 1, 1): 'circumcision',
        datetime.date(year, 1, 6): 'theophany',
        datetime.date(year, 2, 2): 'meeting_lord',
        datetime.date(year, 3, 25): 'annunciation',
        datetime.date(year, 6, 24): 'nativity_john',
        datetime.date(year, 6, 29): 'peter_paul',
        datetime.date(year, 8, 6): 'transfiguration',
        datetime.date(year, 8, 15): 'dormition',
        datetime.date(year, 8, 29): 'beheading_john',
        datetime.date(year, 1, 5): 'sunday_before_theophany',
        datetime.date(year, 1, 12): 'sunday_after_theophany',
        datetime.date(year, 1, 19): '35th_after_pentecost',
        datetime.date(year, 1, 26): '36th_after_pentecost',
        datetime.date(year, 2, 2): '37th_after_pentecost'
    }
    if date in fixed_dates:
        return data['fixed'][fixed_dates[date]]

    # Variable feasts (e.g., Sunday after Exaltation: Sep 15-21)
    if date.month == 9 and 15 <= date.day <= 21 and date.weekday() == 6:  # Sunday
        return {'title': 'Sunday after the Exaltation of the Cross', 'readings': [{'type': 'epistle', 'book': 'Galatians', 'chapter': 2, 'verses': '16-20', 'text': '', 'context': 'Galatians 2:16-20'}, {'type': 'gospel', 'book': 'Mark', 'chapter': 8, 'verses': '34-9:1', 'text': '', 'context': 'Mark 8:34-9:1'}]}  # Placeholder

    # Determine season
    if days_since_pascha < 0:  # Before Pascha: Triodion
        triodion_week = abs(days_since_pascha) // 7 + 1
        day = abs(days_since_pascha) % 7
        if f'lent_{triodion_week}' in data['triodion']:
            return data['triodion'][f'lent_{triodion_week}'][str(day)]
        elif str(triodion_week) in data['triodion']:
            return data['triodion'][str(triodion_week)][str(day)]
    elif 0 <= days_since_pascha < 50:  # Pascha
        return data['pascha'][str(days_since_pascha)]
    elif 50 <= days_since_pascha < 320:  # Pentecostarion
        pentecost_week = (days_since_pascha - 49) // 7 + 1
        day = (days_since_pascha - 49) % 7
        if str(pentecost_week) in data['pentecostarion'] and str(day) in data['pentecostarion'][str(pentecost_week)]:
            return data['pentecostarion'][str(pentecost_week)][str(day)]
        else:
            return {'title': f'Pentecostarion Week {pentecost_week} Day {day} not populated', 'readings': []}
    else:  # After Pentecost: Triodion again
        post_pentecost_week = (days_since_pascha - 319) // 7 + 1
        day = (days_since_pascha - 319) % 7
        if str(post_pentecost_week) in data['triodion']:
            return data['triodion'][str(post_pentecost_week)][str(day)]

    return {'title': 'No readings found', 'readings': []}

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        date_str = sys.argv[1]  # YYYY-MM-DD
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
        readings = get_readings(date)
        print(json.dumps(readings, indent=2))
    else:
        print('Usage: python3 lectionary.py YYYY-MM-DD')
