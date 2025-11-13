#!/usr/bin/env python3
"""
Lentinator: A script to determine if the current date falls within Lent
for Byzantine Catholic tradition, using the Catholic date of Easter.

Lent is from Clean Monday to Lazarus Saturday.
"""

import argparse
from datetime import date, timedelta

def calculate_catholic_easter(year):
    """
    Calculate the date of Catholic Easter for the given year
    using the Gregorian calendar (Meeus algorithm).
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)

def is_lent(today=None):
    """
    Check if the given date (or today) is within Lent.
    Lent starts on Clean Monday and ends on Lazarus Saturday.
    """
    if today is None:
        today = date.today()
    year = today.year
    easter = calculate_catholic_easter(year)
    # If today is after Easter, check next year's Lent (but Lent is before Easter, so use current year)
    # Actually, since Lent is before Easter, if today > easter, Lent is over for this year.
    # But to handle edge cases, if today is before Clean Monday, it's not Lent.
    clean_monday = easter - timedelta(days=55)
    lazarus_saturday = easter - timedelta(days=8)
    return clean_monday <= today <= lazarus_saturday

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if a date is within Lent for Byzantine Catholic tradition. "
                    "Lent is from Clean Monday to Lazarus Saturday."
    )
    parser.add_argument(
        '-d', '--date',
        type=str,
        help='Date in YYYY-MM-DD format (e.g., 2025-03-17). If not provided, uses today.'
    )
    args = parser.parse_args()

    if args.date:
        try:
            today = date.fromisoformat(args.date)
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            exit(1)
    else:
        today = date.today()

    result = "true" if is_lent(today) else "false"
    print(result)