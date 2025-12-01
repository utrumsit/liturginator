"""
Alleluia Period Determination for Byzantine Liturgy

In the Byzantine tradition, "Alleluia" is sung at the beginning of Matins
(after the Six Psalms) instead of "God is the Lord" on certain days.

This module determines when those days occur.

Based on:
- Časoslov (Book of Hours), Ruthenian recension
- orthocal liturgics implementation
- MCI (Metropolitan Cantor Institute) guidelines
"""

from datetime import date
import json
import os
from pascha import calculate_pascha


def get_feast_level(date_obj):
    """
    Look up the feast level for a given date from feast_levels.json.
    
    Parameters:
    -----------
    date_obj : date
        The date to look up
        
    Returns:
    --------
    int
        Feast level (0-8), or 0 if not found
    """
    try:
        feast_levels_path = os.path.join(os.path.dirname(__file__), 'feast_levels.json')
        with open(feast_levels_path, 'r') as f:
            feast_data = json.load(f)
        
        month_str = str(date_obj.month)
        day_str = str(date_obj.day)
        
        if month_str in feast_data and day_str in feast_data[month_str]:
            return feast_data[month_str][day_str]
        
        return 0  # Ordinary day
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return 0  # Default to ordinary day if file not found


def is_alleluia_day(date_obj=None, pdist=None, weekday=None, feast_level=None):
    """
    Determine if "Alleluia" is sung instead of "God is the Lord" at Matins.
    
    Parameters:
    -----------
    date_obj : date, optional
        The date to check. If provided, pdist and weekday will be calculated.
    pdist : int, optional
        Pascha distance (days from Pascha). Required if date_obj not provided.
    weekday : int, optional
        Day of week (0=Sunday, 6=Saturday). Required if date_obj not provided.
    feast_level : int, default=0
        Feast ranking (0=ordinary, 2-3=minor, 4+=polyeleos or higher)
        
    Returns:
    --------
    bool
        True if Alleluia should be sung, False otherwise
        
    Examples:
    ---------
    >>> # Monday after Pentecost (pdist 50, Monday)
    >>> is_alleluia_day(pdist=50, weekday=1, feast_level=0)
    True
    
    >>> # Sunday (any pdist > 49)
    >>> is_alleluia_day(pdist=100, weekday=0, feast_level=0)
    False
    
    >>> # Lent weekday
    >>> is_alleluia_day(pdist=-20, weekday=2, feast_level=0)
    False
    
    >>> # Polyeleos feast on a weekday
    >>> is_alleluia_day(pdist=100, weekday=3, feast_level=4)
    False
    """
    
    # Calculate pdist and weekday if date_obj provided
    if date_obj is not None:
        if not isinstance(date_obj, date):
            raise TypeError("date_obj must be a datetime.date object")
        
        pascha = calculate_pascha(date_obj.year)
        # Adjust for liturgical year (before Pascha = use this year's Pascha)
        if date_obj < pascha:
            pascha_ref = pascha
        else:
            pascha_ref = pascha
            
        pdist = (date_obj - pascha_ref).days
        weekday = date_obj.weekday()
        # Convert Python weekday (0=Monday) to Byzantine weekday (0=Sunday)
        weekday = (weekday + 1) % 7
        
        # Auto-detect feast level if not provided
        if feast_level is None:
            feast_level = get_feast_level(date_obj)
    
    # Validate required parameters
    if pdist is None or weekday is None:
        raise ValueError("Must provide either date_obj OR (pdist and weekday)")
    
    # Default feast_level if still None
    if feast_level is None:
        feast_level = 0
    
    # Rule 1: Must be a weekday (not Sunday)
    if weekday == 0:
        return False
    
    # Rule 2: Must NOT be in Lent or Holy Week (Meatfare Monday through Holy Saturday)
    # Meatfare Monday is approximately pdist -49
    # Holy Saturday is pdist -1
    if -49 <= pdist < 0:
        return False
    
    # Rule 3: Must NOT be in Bright Week through Pentecost (Pascha through Pentecost)
    # These days use "Christ is risen" or "God is the Lord" with Paschal troparia
    if 0 <= pdist <= 49:
        return False
    
    # Rule 4: Must NOT be a major feast (polyeleos rank or higher)
    # Feast levels: 0-1=ordinary, 2-3=minor, 4+=polyeleos/vigil/great feast
    if feast_level >= 4:
        return False
    
    # If all rules pass, this is an Alleluia day
    return True


def get_alleluia_verses(tone):
    """
    Return the psalm verses used with Alleluia for the given tone.
    
    Parameters:
    -----------
    tone : int
        The tone (1-8) for the current week
        
    Returns:
    --------
    list of str
        Three psalm verses used with Alleluia (sung 3x total)
        
    Note:
    -----
    The actual verses vary by tone and are found in the Octoechos.
    This is a placeholder - actual verses should be loaded from data files.
    """
    
    # TODO: Load actual Alleluia verses from octoechos data
    # For now, return common verses as placeholders
    
    common_verses = {
        1: [
            "From the rising of the sun to its setting, the name of the Lord is to be praised.",
            "Blessed is the Lord from Zion, Who dwells in Jerusalem.",
            "O give thanks to the Lord, for He is good; for His mercy endures forever."
        ],
        # Add verses for tones 2-8 as data becomes available
    }
    
    return common_verses.get(tone, common_verses[1])


def get_matins_opening(date_obj=None, pdist=None, weekday=None, feast_level=None):
    """
    Determine what should be sung at the beginning of Matins after the Six Psalms.
    
    Returns:
    --------
    str
        One of: "alleluia", "god_is_lord", "christ_is_risen", "lenten_alleluia"
    """
    
    # Calculate pdist if needed
    if date_obj is not None:
        pascha = calculate_pascha(date_obj.year)
        if date_obj < pascha:
            pascha_ref = pascha
        else:
            pascha_ref = pascha
        pdist = (date_obj - pascha_ref).days
        weekday = (date_obj.weekday() + 1) % 7
        
        # Auto-detect feast level if not provided
        if feast_level is None:
            feast_level = get_feast_level(date_obj)
    
    if pdist is None or weekday is None:
        raise ValueError("Must provide either date_obj OR (pdist and weekday)")
    
    # Bright Week (Pascha through Bright Saturday)
    if 0 <= pdist <= 6:
        return "christ_is_risen"
    
    # Lent and Holy Week (different Alleluia, somber tone)
    if -49 <= pdist < 0:
        return "lenten_alleluia"
    
    # Check if regular Alleluia day
    if is_alleluia_day(pdist=pdist, weekday=weekday, feast_level=feast_level):
        return "alleluia"
    
    # Default: "God is the Lord" (Sundays, major feasts, Paschal season)
    return "god_is_lord"


if __name__ == "__main__":
    import sys
    import argparse
    parser = argparse.ArgumentParser(
        description="Determine if Alleluia is sung at Matins for a given date.",
        epilog="Returns the Matins opening type: alleluia, god_is_lord, christ_is_risen, or lenten_alleluia"
    )
    parser.add_argument('date', nargs='?', default=None, help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--feast-level', type=int, default=None, help='Feast level (0-8, default: auto-detect from feast_levels.json)')
    args = parser.parse_args()
    
    if args.date:
        try:
            test_date = date.fromisoformat(args.date)
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        test_date = date.today()
    
    # Calculate values
    pascha = calculate_pascha(test_date.year)
    if test_date < pascha:
        pascha_ref = pascha
    else:
        pascha_ref = pascha
    
    pdist = (test_date - pascha_ref).days
    weekday = (test_date.weekday() + 1) % 7  # Convert to Byzantine (0=Sunday)
    weekday_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    
    # Auto-detect feast level if not provided via command line
    if args.feast_level is None:
        detected_level = get_feast_level(test_date)
    else:
        detected_level = args.feast_level
    
    # Get results
    is_alleluia = is_alleluia_day(date_obj=test_date, feast_level=detected_level)
    opening = get_matins_opening(date_obj=test_date, feast_level=detected_level)
    
    # Output
    print(f"Date: {test_date} ({weekday_names[weekday]})")
    print(f"Pascha: {pascha_ref}, pdist: {pdist}")
    if args.feast_level is None:
        print(f"Feast level: {detected_level} (auto-detected)")
    else:
        print(f"Feast level: {detected_level} (manual override)")
    print(f"")
    print(f"Is Alleluia day? {is_alleluia}")
    print(f"Matins opening: {opening}")
