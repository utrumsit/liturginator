#!/usr/bin/env python3
"""
Vespers Prokeimenon Logic

Determines whether to use the weekday prokeimenon or Alleluia at vespers,
based on the liturgical calendar (Lent, minor fasts, feast levels).

SOURCES:
=========

1. Časoslov (Book of Hours), Ruthenian recension
   - Pages 259-261: "Order of Vespers"
   - Page 259: Weekday prokeimena for "God the Lord" periods
     "If it is [a period when] God the Lord [is sung] these prokeimena are sung..."
   - Page 260-261: Lenten Alleluia verses
     "It is necessary to be aware if it is the Fast and Alleluia [is sung],
      in place of the prokeimena we sing this..."
   - Page 261: "But on Sunday and Friday evenings, Alleluia is never sung."

2. MCI Daily Vespers PDF (referenced in work log)
   - "On certain days in the minor fasts (which are indicated in the typikon),
      the alleluia is taken in place of the daily prokeimenon."

3. orthocal.info liturgics implementation
   - FeastLevels enum in datetools.py
   - Feast level 0-3: "Day of Alleluia" (ordinary/minor saint)
   - Feast level 4+: "God is the Lord" (polyeleos/vigil/great feast)

4. feast_levels.json in this project
   - Level 0: "Ordinary day (Alleluia)"
   - Level 4+: "Polyeleos rank (God is the Lord)"

RULES (derived from above sources):
====================================

1. GREAT LENT (Clean Monday through Lazarus Saturday):
   - Mon-Thu evenings: Alleluia verses (per chasoslov p.260-261)
   - Fri evening: Prokeimenon (Alleluia never sung)
   - Sat evening: Prokeimenon (liturgically Sunday)
   - Sun evening: Prokeimenon (Alleluia never sung)

   The chasoslov (p.261) says: "On Sunday and Friday evenings, Alleluia is never sung"
   This refers to vespers on the civil Sunday evening and Friday evening.
   Saturday evening is also liturgically Sunday, so it follows the same rule.

2. MINOR FASTS (Nativity Nov 15-Dec 24, Dormition Aug 1-14, Apostles):
   - If feast_level == 0 ("Day of Alleluia" in typikon): Use Alleluia
   - If feast_level >= 1: Use prokeimenon
   - Exception: Sun & Fri evenings always use prokeimenon

3. ORDINARY TIME:
   - Always use the weekday prokeimenon

4. FEAST DAYS (feast_level >= 4):
   - Always use prokeimenon (major feasts use "God is the Lord")

Note: The "Day of Alleluia" marking in the typikon indicates days when there
is no special commemoration that would require "God is the Lord" at Matins.
The same logic applies to Vespers: if Alleluia is sung at Matins, Alleluia
verses replace the prokeimenon at Vespers on fasting days.
"""

from datetime import date, timedelta
from pascha import calculate_pascha
from lent import is_lent
import json
import os


# Weekday prokeimena (Ordinary Time)
# Key is day of week for the EVENING (i.e., Saturday evening = start of Sunday)
PROKEIMENA = {
    # Saturday evening (for Sunday)
    5: {
        "tone": 6,
        "psalm": 92,
        "prokeimenon": "The Lord reigns, He is clothed in majesty!",
        "verses": [
            "Robed is the Lord and girt about with strength.",
            "The world He made firm, not to be moved.",
            "Holiness is fitting to Your house, O Lord, until the end of time."
        ]
    },
    # Sunday evening (for Monday)
    6: {
        "tone": 8,
        "psalm": 133,
        "prokeimenon": "Come, bless the Lord, all you who serve the Lord.",
        "verses": [
            "Who stand in the house of the Lord, in the courts of the house of our God."
        ]
    },
    # Monday evening (for Tuesday)
    0: {
        "tone": 4,
        "psalm": 4,
        "prokeimenon": "The Lord hears me whenever I call Him.",
        "verses": [
            "When I call, answer me, O God of Justice."
        ]
    },
    # Tuesday evening (for Wednesday)
    1: {
        "tone": 1,
        "psalm": 22,
        "prokeimenon": "My help shall come from the Lord, Who made heaven and earth.",
        "verses": [
            "I lift up my eyes to the mountains, from where shall come my help?"
        ]
    },
    # Wednesday evening (for Thursday)
    2: {
        "tone": 5,
        "psalm": 53,
        "prokeimenon": "O God, save me by Your Name, by Your power uphold my cause.",
        "verses": [
            "O God, hear my prayer; listen to the words of my mouth."
        ]
    },
    # Thursday evening (for Friday)
    3: {
        "tone": 6,
        "psalm": 120,
        "prokeimenon": "Your mercy, O Lord, shall follow me all the days of my life.",
        "verses": [
            "The Lord is my shepherd, there is nothing I shall want; fresh and green are the pastures where He gives me repose."
        ]
    },
    # Friday evening (for Saturday)
    4: {
        "tone": 7,
        "psalm": 58,
        "prokeimenon": "You, O God, are my defender and Your mercy goes before me.",
        "verses": [
            "Rescue me, O God, from my foes; protect me from those who attack me."
        ]
    }
}

# Lenten Alleluia verses (by evening)
LENTEN_ALLELUIA = {
    # Monday evening
    0: {
        "tone": 6,
        "psalm": 6,
        "verses": [
            "O Lord, rebuke me not in Your anger, chastise me not in Your wrath.",
            "Now and ever and forever."
        ]
    },
    # Tuesday evening
    1: {
        "tone": None,
        "psalm": 98,
        "verses": [
            "Extol the Lord, our God, and worship at His footstool for He is holy.",
            "Now and ever and forever."
        ]
    },
    # Wednesday evening
    2: {
        "tone": None,
        "psalm": 18,
        "verses": [
            "Through all the earth their voice resounds; their message reaches to the ends of the world.",
            "Now and ever and forever."
        ]
    },
    # Thursday evening
    3: {
        "tone": None,
        "psalm": 98,
        "verses": [
            "Extol the Lord, our God, and worship at His footstool for He is holy.",
            "Now and ever and forever."
        ]
    },
    # Friday and Saturday evenings: never Alleluia in Lent, use prokeimenon
}


def get_feast_level(date_obj):
    """Look up feast level from menaion_complete.json or feast_levels.json."""
    # Try menaion_complete.json first
    try:
        menaion_path = os.path.join(os.path.dirname(__file__), 'menaion_complete.json')
        with open(menaion_path, 'r') as f:
            data = json.load(f)

        month_str = str(date_obj.month)
        day_str = str(date_obj.day)

        if month_str in data and day_str in data[month_str]:
            return data[month_str][day_str].get('feast_level', 0)
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        pass

    # Fall back to feast_levels.json
    try:
        feast_path = os.path.join(os.path.dirname(__file__), 'feast_levels.json')
        with open(feast_path, 'r') as f:
            data = json.load(f)

        month_str = str(date_obj.month)
        day_str = str(date_obj.day)

        if month_str in data and day_str in data[month_str]:
            return data[month_str][day_str]
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        pass

    return 0  # Default to ordinary day


def is_minor_fast(date_obj):
    """
    Check if date is in a minor fast (Nativity, Apostles, or Dormition fast).

    Minor fasts:
    - Apostles Fast: Monday after All Saints until June 28 (eve of Sts. Peter & Paul)
    - Dormition Fast: August 1-14
    - Nativity Fast: November 15 - December 24
    """
    month, day = date_obj.month, date_obj.day

    # Dormition Fast: August 1-14
    if month == 8 and 1 <= day <= 14:
        return True

    # Nativity Fast: November 15 - December 24
    if month == 11 and day >= 15:
        return True
    if month == 12 and day <= 24:
        return True

    # Apostles Fast: Monday after All Saints until June 28
    # All Saints = Sunday after Pentecost = pdist 56
    # Monday after = pdist 57
    # June 29 = Sts Peter & Paul, so fast ends June 28
    pascha = calculate_pascha(date_obj.year)
    pdist = (date_obj - pascha).days

    # Start: pdist 57 (Monday after All Saints)
    # End: June 28 (day before Sts. Peter & Paul)
    if pdist >= 57:
        peter_paul = date(date_obj.year, 6, 29)
        if date_obj < peter_paul:
            return True

    return False


def get_vespers_prokeimenon(date_obj, feast_level=None):
    """
    Get the prokeimenon or Alleluia for vespers on a given date.

    Parameters:
    -----------
    date_obj : date
        The date of the vespers service
    feast_level : int, optional
        Override feast level (auto-detected if not provided)

    Returns:
    --------
    dict with keys:
        - type: "prokeimenon" or "alleluia"
        - data: the prokeimenon/alleluia data dict
        - reason: explanation of why this was chosen
    """
    if feast_level is None:
        feast_level = get_feast_level(date_obj)

    weekday = date_obj.weekday()  # 0=Monday, 6=Sunday

    # Rule 1: Feast days (polyeleos or higher) always use prokeimenon
    if feast_level >= 4:
        return {
            "type": "prokeimenon",
            "data": PROKEIMENA[weekday],
            "reason": f"Feast level {feast_level} (polyeleos or higher)"
        }

    # Rule 2: Great Lent (but not Sunday or Friday evenings)
    # Per chasoslov p.261: "On Sunday and Friday evenings, Alleluia is never sung"
    # - Sunday evening = civil Sunday evening (Python weekday 6)
    # - Friday evening = civil Friday evening (Python weekday 4)
    # - Saturday evening = civil Saturday (Python weekday 5) = liturgically Sunday
    if is_lent(date_obj):
        # Sunday, Friday, and Saturday evenings: use prokeimenon
        # (Saturday evening is liturgically Sunday, so same rule applies)
        if weekday in (4, 5, 6):  # Friday, Saturday, Sunday
            return {
                "type": "prokeimenon",
                "data": PROKEIMENA[weekday],
                "reason": "Lent, but Sunday/Friday/Saturday evening uses prokeimenon"
            }
        # Mon-Thu evenings in Lent: use Alleluia
        if weekday in LENTEN_ALLELUIA:
            return {
                "type": "alleluia",
                "data": LENTEN_ALLELUIA[weekday],
                "reason": "Great Lent"
            }

    # Rule 3: Minor fasts with Day of Alleluia (feast_level 0)
    if is_minor_fast(date_obj) and feast_level == 0:
        # On minor fasts, ordinary days (level 0) may take Alleluia
        # But Sunday, Friday, Saturday evenings still use prokeimenon
        if weekday not in (4, 5, 6):  # Not Friday, Saturday, Sunday
            # Use the Lenten Alleluia verses if available for this day
            if weekday in LENTEN_ALLELUIA:
                return {
                    "type": "alleluia",
                    "data": LENTEN_ALLELUIA[weekday],
                    "reason": f"Minor fast, Day of Alleluia (feast level {feast_level})"
                }

    # Default: use the regular weekday prokeimenon
    return {
        "type": "prokeimenon",
        "data": PROKEIMENA[weekday],
        "reason": "Ordinary time"
    }


def format_prokeimenon(data, type_="prokeimenon"):
    """Format prokeimenon/alleluia for display."""
    lines = []

    if type_ == "prokeimenon":
        tone_str = f"Tone {data['tone']}, " if data.get('tone') else ""
        lines.append(f"*{tone_str}Psalm {data['psalm']}*")
        lines.append("")
        lines.append(data['prokeimenon'])
        for verse in data['verses']:
            lines.append(f"*Verse:* {verse}")
    else:
        # Alleluia
        tone_str = f"Tone {data['tone']}, " if data.get('tone') else ""
        psalm_str = f"Psalm {data['psalm']}" if data.get('psalm') else ""
        if tone_str or psalm_str:
            lines.append(f"*{tone_str}{psalm_str}*")
            lines.append("")
        lines.append("Alleluia, alleluia, alleluia.")
        for verse in data['verses']:
            lines.append(f"*Verse:* {verse} Alleluia!")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Get the vespers prokeimenon or alleluia for a given date."
    )
    parser.add_argument('date', nargs='?', default=None,
                        help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--feast-level', type=int, default=None,
                        help='Override feast level')
    args = parser.parse_args()

    if args.date:
        try:
            test_date = date.fromisoformat(args.date)
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        test_date = date.today()

    result = get_vespers_prokeimenon(test_date, args.feast_level)

    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    feast_level = args.feast_level if args.feast_level is not None else get_feast_level(test_date)

    print(f"Date: {test_date} ({weekday_names[test_date.weekday()]} evening)")
    print(f"Feast level: {feast_level}")
    print(f"Is Lent: {is_lent(test_date)}")
    print(f"Is minor fast: {is_minor_fast(test_date)}")
    print(f"Reason: {result['reason']}")
    print()
    print(f"=== {result['type'].upper()} ===")
    print()
    print(format_prokeimenon(result['data'], result['type']))
