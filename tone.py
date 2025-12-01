#!/usr/bin/env python3
"""
Tone Calculator for Byzantine Rite Liturgy

Determines the liturgical tone for a given date based on the 8-tone (octoechos) cycle.
Based on algorithm from orthocal-python by Brian Glass (MIT License).
Reference: https://mci.archpitt.org/liturgy/EightTones.html
"""

import datetime
from pascha import calculate_pascha

def get_tone(date=None, pascha=None):
    """
    Get the liturgical tone for the given date.
    
    Args:
        date: datetime.date object (default: today)
        pascha: datetime.date of Pascha for this year (optional, will calculate if not provided)
    
    Returns:
        int: 0 (not in octoechos cycle, e.g. Holy Week) or 1-8 (tone number)
    
    Notes:
        - Holy Week (8 days before Pascha): returns 0 (octoechos not employed)
        - Bright Week (Pascha + 6 days): special sequence 1,2,3,4,5,6,8 (tone 7 too somber)
        - Regular cycle: starts with Thomas Sunday (8th day after Pascha) = Tone 1
        - Great feasts may also use tone 0 (handled elsewhere)
    """
    if date is None:
        date = datetime.date.today()
    
    # Calculate Pascha if not provided
    if pascha is None:
        year = date.year
        pascha_this_year = calculate_pascha(year)
        pascha_next_year = calculate_pascha(year + 1)
        
        # Determine which Pascha this date is closest to
        # If we're before this year's Pascha, use this year's Pascha
        # This handles Holy Week and pre-Pascha dates correctly
        if date < pascha_this_year:
            pascha = pascha_this_year
        # If we're after this year's Pascha but before next year's, use this year's
        elif date < pascha_next_year:
            pascha = pascha_this_year
        else:
            pascha = pascha_next_year
    
    # Calculate pascha distance (pdist)
    pdist = (date - pascha).days
    
    # Holy Week: octoechos not employed (has its own special tones per service)
    # Lazarus Saturday through Holy Saturday (pdist -8 to -1)
    if -9 < pdist < 0:
        return 0
    
    # Bright Week: cycle through tones 1,2,3,4,5,6,8 (skip tone 7 - too somber)
    # Pascha = Tone 1, Monday = Tone 2, ..., Saturday = Tone 8
    if 0 <= pdist < 7:
        bright_tones = (1, 2, 3, 4, 5, 6, 8)
        return bright_tones[pdist]
    
    # TODO: Check for great feasts (feast_level >= 7) and return 0
    # This should be handled by the caller based on feast_level
    
    # Regular Sunday cycle: Thomas Sunday (pdist 7) is 1st Sunday after Pascha
    # Formula: ((nth_sunday - 1) % 8) + 1
    # This creates the repeating cycle: 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, ...
    nth_sunday = pdist // 7
    tone = (nth_sunday - 1) % 8 + 1
    
    return tone

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate the liturgical tone for a given date.",
        epilog="Returns 0 for Holy Week (not in octoechos cycle) or 1-8 for regular tones."
    )
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
    
    # Calculate pdist for display
    year = date.year
    pascha = calculate_pascha(year)
    if date < pascha:
        pascha = calculate_pascha(year - 1)
    pdist = (date - pascha).days
    
    if tone == 0:
        print(f"Tone for {date}: 0 (Holy Week - not in octoechos cycle)")
    else:
        print(f"Tone for {date}: {tone}")
    print(f"  Pascha: {pascha}, pdist: {pdist}")
