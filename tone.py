#!/usr/bin/env python3
"""
Tone Calculator for Byzantine Rite Liturgy

Determines the liturgical tone for a given date based on the 8-tone cycle starting from Pascha.
"""

import datetime
from dateutil.easter import easter  # For Western Easter, but we'll adjust for Orthodox

def calculate_orthodox_easter(year):
    """
    Calculate the date of Orthodox Easter (Pascha) for the given year.
    Orthodox Easter is the first Sunday after the first full moon after March 21,
    but calculated differently from Western Easter.
    For simplicity, using an approximation; in production, use a proper library.
    """
    # Placeholder: Orthodox Easter is usually 13 days after Western Easter, but not always.
    # For 2023: April 16, 2023
    # For 2024: May 5, 2024
    # For 2025: April 20, 2025
    # Implement proper calculation here.
    # For now, hardcode or use a formula.

    # Simple approximation: Orthodox Easter = Western Easter + 13 days, adjusted.
    western = easter(year)
    # Orthodox is the Sunday after the full moon following March 21 in Julian calendar.
    # This is complex; for demo, use a dict or formula.

    orthodox_dates = {
        2023: datetime.date(2023, 4, 16),
        2024: datetime.date(2024, 5, 5),
        2025: datetime.date(2025, 4, 20),
        # Add more years as needed
    }
    return orthodox_dates.get(year, datetime.date(year, 4, 16))  # Default to April 16

def get_tone(date=None):
    """
    Get the liturgical tone for the given date.
    Returns an integer 1-8.
    """
    if date is None:
        date = datetime.date.today()

    year = date.year
    pascha = calculate_orthodox_easter(year)

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
        # After Thomas Sunday
        # Calculate weeks after Pentecost
        # Pentecost is 50 days after Pascha
        pentecost = pascha + datetime.timedelta(days=49)  # 50th day is Pentecost
        if date <= pentecost:
            # Paschal season: special tones
            # For simplicity, use the regular cycle
            pass

        # Sundays after Pentecost: Tone = ((sunday_number - 1) % 8) + 1
        # But need to find the sunday number.

        # First, find the number of Sundays after Pentecost
        days_after_pentecost = (date - pentecost).days
        if days_after_pentecost < 0:
            # During Paschal season, perhaps Tone 1 or special
            return 1

        # Find the Sunday number
        # The second Sunday after Pentecost is Tone 1, etc.
        # So, for date, find how many Sundays have passed since Pentecost.

        # Calculate the date of the first Sunday after Pentecost
        first_sunday_after_pentecost = pentecost + datetime.timedelta(days=(7 - pentecost.weekday()))

        if date < first_sunday_after_pentecost:
            return 1  # Pentecost week or something

        weeks_after = ((date - first_sunday_after_pentecost).days // 7) + 1  # +1 for the first week
        tone = ((weeks_after - 1) % 8) + 1
        return tone

if __name__ == "__main__":
    import sys
    date_str = sys.argv[1] if len(sys.argv) > 1 else None
    if date_str:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = None
    tone = get_tone(date)
    print(f"Tone for {date or datetime.date.today()}: {tone}")