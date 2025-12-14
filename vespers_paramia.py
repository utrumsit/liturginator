#!/usr/bin/env python3
"""
Vespers Paremia (Readings) Module

Returns the Old Testament readings (paramia/paremias) for vespers on a given date.

SOURCES:
=========

1. Časoslov (Book of Hours), Ruthenian recension, page 262
   - Deacon: "Wisdom"
   - Lector: "A reading from [book name]"
   - Deacon: "Let us be attentive"
   - [Lector reads the passage]

2. scripture_readings.json in this project
   - Contains vespers_paramia for major feasts (fixed cycle)
   - Contains vespers_paramia for some paschal cycle days

3. orthocal liturgics
   - has_no_paremias / has_moved_paremias for edge cases

USAGE:
======

Paramia are read at vespers:
- On the eves of major feasts (typically 3 readings)
- On certain days in Lent (Great Lent has daily OT readings)
- When the typikon prescribes them

If no paramia are found for a date, a placeholder is returned indicating
that readings may be omitted or are not prescribed for that day.
"""

from datetime import date, timedelta
import json
import os
from pascha import calculate_pascha

# Cache for scripture readings
_SCRIPTURE_CACHE = None


def _load_scripture_readings():
    """Load scripture_readings.json and cache it."""
    global _SCRIPTURE_CACHE
    if _SCRIPTURE_CACHE is None:
        scripture_path = os.path.join(os.path.dirname(__file__), 'scripture_readings.json')
        with open(scripture_path, 'r') as f:
            _SCRIPTURE_CACHE = json.load(f)
    return _SCRIPTURE_CACHE


# Fixed feast date mappings
# Key = feast key in scripture_readings.json, value = (month, day)
FIXED_FEAST_DATES = {
    'circumcision': (1, 1),
    'meeting_lord': (2, 2),
    'annunciation': (3, 25),
    'nativity_john': (6, 24),
    'peter_paul': (6, 29),
    'transfiguration': (8, 6),
    'dormition': (8, 15),
    'beheading_john': (8, 29),
    'nativity_theotokos': (9, 8),
    'exaltation_cross': (9, 14),
    'protection_theotokos': (10, 1),
    'entry_theotokos': (11, 21),
    'st_nicholas': (12, 6),
    # Nativity and Theophany handled separately (movable eves)
}


def get_vespers_paramia(date_obj):
    """
    Get the vespers paramia (readings) for a given date.

    Parameters:
    -----------
    date_obj : date
        The date of the vespers service

    Returns:
    --------
    dict with keys:
        - has_readings: bool - True if paramia exist for this date
        - readings: list of dicts - Each with 'book', 'reference', 'text' (if available)
        - source: str - Where the readings come from ('fixed', 'paschal', etc.)
        - feast_name: str - Name of the feast (if applicable)
        - rubric: str - The standard rubric for announcing readings
    """
    data = _load_scripture_readings()

    # Calculate pascha distance
    year = date_obj.year
    pascha = calculate_pascha(year)
    if date_obj < pascha:
        pascha = calculate_pascha(year - 1)
    pdist = (date_obj - pascha).days

    # Check fixed feasts first (paramia are read on the EVE of feasts)
    # So check if TOMORROW is a major feast
    tomorrow = date_obj + timedelta(days=1)

    for feast_key, (month, day) in FIXED_FEAST_DATES.items():
        if tomorrow.month == month and tomorrow.day == day:
            if feast_key in data.get('fixed', {}):
                feast_data = data['fixed'][feast_key]
                if 'vespers_paramia' in feast_data:
                    readings = []
                    for r in feast_data['vespers_paramia']:
                        reading = {
                            'book': r.get('book', ''),
                            'reference': f"{r.get('book', '')} {r.get('chapter', '')}:{r.get('verses', '')}",
                            'text': r.get('text', ''),
                            'context': r.get('context', '')
                        }
                        readings.append(reading)

                    return {
                        'has_readings': True,
                        'readings': readings,
                        'source': 'fixed',
                        'feast_name': feast_data.get('title', feast_key),
                        'rubric': _generate_rubric(readings)
                    }

    # Check paschal cycle
    pdist_str = str(pdist)
    if pdist_str in data.get('pascha', {}):
        day_data = data['pascha'][pdist_str]
        if isinstance(day_data, dict) and 'vespers_paramia' in day_data:
            readings = []
            for r in day_data['vespers_paramia']:
                reading = {
                    'book': r.get('book', ''),
                    'reference': f"{r.get('book', '')} {r.get('chapter', '')}:{r.get('verses', '')}",
                    'text': r.get('text', ''),
                    'context': r.get('context', '')
                }
                readings.append(reading)

            return {
                'has_readings': True,
                'readings': readings,
                'source': 'paschal',
                'feast_name': day_data.get('title', ''),
                'rubric': _generate_rubric(readings)
            }

    # Check Lenten readings (if we have them)
    # Great Lent has OT readings at vespers daily
    if -48 <= pdist <= -8:  # Clean Monday through Friday before Lazarus Saturday
        if 'lent' in data:
            lent_day = str(pdist)
            if lent_day in data['lent']:
                day_data = data['lent'][lent_day]
                if isinstance(day_data, dict) and 'vespers_paramia' in day_data:
                    readings = []
                    for r in day_data['vespers_paramia']:
                        reading = {
                            'book': r.get('book', ''),
                            'reference': f"{r.get('book', '')} {r.get('chapter', '')}:{r.get('verses', '')}",
                            'text': r.get('text', ''),
                            'context': r.get('context', '')
                        }
                        readings.append(reading)

                    return {
                        'has_readings': True,
                        'readings': readings,
                        'source': 'lent',
                        'feast_name': day_data.get('title', 'Lenten Vespers'),
                        'rubric': _generate_rubric(readings)
                    }

    # No readings found
    return {
        'has_readings': False,
        'readings': [],
        'source': None,
        'feast_name': None,
        'rubric': None
    }


def _generate_rubric(readings):
    """Generate the liturgical rubric for announcing readings."""
    if not readings:
        return None

    lines = []
    for i, reading in enumerate(readings):
        book = reading.get('book', 'the Scripture')
        lines.append(f"*Deacon:* Wisdom!")
        lines.append(f"*Lector:* A reading from {book}.")
        lines.append(f"*Deacon:* Let us be attentive.")
        lines.append("")

    return "\n".join(lines)


def format_paramia_output(result):
    """Format paramia result for markdown output."""
    lines = []

    if not result['has_readings']:
        lines.append("## Readings")
        lines.append("")
        lines.append("*No paramia prescribed for this day.*")
        lines.append("*(Readings may be omitted.)*")
        return "\n".join(lines)

    if result.get('feast_name'):
        lines.append(f"## Readings for {result['feast_name']}")
    else:
        lines.append("## Readings")
    lines.append("")

    for i, reading in enumerate(result['readings'], 1):
        # Announce each reading
        book = reading.get('book', 'the Scripture')
        lines.append(f"*Deacon:* Wisdom!")
        lines.append(f"")
        lines.append(f"*Lector:* A reading from {book}.")
        lines.append(f"")
        lines.append(f"*Deacon:* Let us be attentive.")
        lines.append("")

        # Reading reference
        if reading.get('reference'):
            lines.append(f"**{reading['reference']}**")
            lines.append("")

        # Reading text (if available)
        if reading.get('text'):
            lines.append(reading['text'])
            lines.append("")
        else:
            lines.append(f"*[Text of {reading.get('context', reading.get('reference', 'reading'))}]*")
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Get vespers paramia (readings) for a given date."
    )
    parser.add_argument('date', nargs='?', default=None,
                        help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON instead of markdown')
    args = parser.parse_args()

    if args.date:
        try:
            test_date = date.fromisoformat(args.date)
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD.")
            sys.exit(1)
    else:
        test_date = date.today()

    result = get_vespers_paramia(test_date)

    if args.json:
        # JSON output (exclude text for brevity)
        output = {
            'date': str(test_date),
            'has_readings': result['has_readings'],
            'source': result['source'],
            'feast_name': result['feast_name'],
            'readings': [
                {'book': r['book'], 'reference': r['reference']}
                for r in result['readings']
            ] if result['readings'] else []
        }
        print(json.dumps(output, indent=2))
    else:
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        print(f"Date: {test_date} ({weekday_names[test_date.weekday()]} evening)")
        print(f"Source: {result['source'] or 'none'}")
        print()
        print(format_paramia_output(result))
