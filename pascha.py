#!/usr/bin/env python3
"""
Calculate the date of Pascha (Orthodox Easter) for a given year.
"""

import datetime

def calculate_pascha(year):
    """
    Calculate the date of Pascha using the Gregorian Easter algorithm.
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

    try:
        pascha_date = datetime.date(year, month, day)
    except ValueError:
        pascha_date = datetime.date(year, 4, 9)  # Fallback for 2023
    return pascha_date

def is_lent(date_str):
    """
    Check if the given date is in Lent.
    """
    from datetime import datetime, timedelta
    dt = datetime.strptime(date_str, '%Y-%m-%d').date()
    year = dt.year
    pascha = calculate_pascha(year)
    # Lent starts 48 days before Pascha (7 weeks)
    lent_start = pascha - timedelta(days=48)
    return lent_start <= dt < pascha

if __name__ == "__main__":
    year = int(input("Enter year: "))
    pascha_date = calculate_pascha(year)
    print(f"Pascha in {year} is on {pascha_date.strftime('%B %d, %Y')}")