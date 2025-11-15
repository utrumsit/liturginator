#!/usr/bin/env python3
"""
Tone Calculator for Byzantine Rite Liturgy

Determines the liturgical tone for a given date based on the 8-tone cycle starting from Pascha.
"""

import datetime
from dateutil.easter import easter  # For Western Easter, but we'll adjust for Orthodox

def calculate_easter(year):
    """
    Calculate the date of Easter (Pascha) for the given year.
    Byzantine Catholic Church uses the Western (Gregorian) calculation.
    """
    return easter(year)

def get_tone(date=None):
    """
    Get the liturgical tone for the given date.
    Returns an integer 1-8.
    """
    if date is None:
        date = datetime.date.today()

    year = date.year
    pascha = calculate_easter(year)
    pentecost = pascha + datetime.timedelta(days=49)

    # If before Pascha, perhaps Tone 8 or special, but for simplicity, assume cycle starts at Pascha
    if date < pascha:
        # Pre-Pascha: during Lent, tones are mixed, but for now, return 8
        return 8

    days_since_pascha = (date - pascha).days

    if days_since_pascha == 0:
        # Pascha: Tone 1
        return 1
    elif 1 <= days_since_pascha <= 6:
        # Bright Week: Monday Tone 2, Tue 3, ..., Sat 8 (omitting 7)
        bright_tones = [2, 3, 4, 5, 6, 8]  # For days 1-6
        return bright_tones[days_since_pascha - 1]
    elif days_since_pascha == 7:
        # Thomas Sunday: Tone 1
        return 1
    else:
        days_after_pentecost = (date - pentecost).days
        number = days_after_pentecost // 7
        if number <= 2:
            tone = 1
        else:
            tone = ((number - 2) % 8) + 1
        return tone

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Calculate the liturgical tone for a given date.")
    parser.add_argument('date', nargs='?', default=None, help='Date in YYYY-MM-DD format (default: today)')
    args = parser.parse_args()

    if args.date:
        try:
            date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date()
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            exit(1)
    else:
        date = datetime.date.today()

    tone = get_tone(date)
    print(f"Tone for {date}: {tone}")