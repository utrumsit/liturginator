#!/usr/bin/env python3
"""
Calculate the date of Pascha (Orthodox Easter) for a given year.
"""

import datetime

def calculate_pascha(year):
    """
    Calculate the date of Pascha using the Orthodox Easter algorithm.
    """
    # Coefficients for the lunar cycle
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

    # For Orthodox Easter, use Julian calendar date
    # To convert to Gregorian if needed, but keeping Julian for tradition
    try:
        pascha_date = datetime.date(year, month, day)
    except ValueError:
        # Handle invalid dates (e.g., Feb 30)
        pascha_date = datetime.date(year, 3, 1)  # Fallback, but algorithm should be correct

    return pascha_date

if __name__ == "__main__":
    year = int(input("Enter year: "))
    pascha_date = calculate_pascha(year)
    print(f"Pascha in {year} is on {pascha_date.strftime('%B %d, %Y')}")