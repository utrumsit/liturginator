#!/usr/bin/env python3
"""
calendar_lookup.py — small standalone wrapper for the Facebook skill.

Reads the already-populated data files (no CLI dependency):
  - docs/readings_2025-2035-final.json (10-year daily readings w/ RSV text)
  - menaion_complete.json                (saints + troparia/kontakia by date)

For a given date, returns a markdown digest with:
  - Liturgical week / season
  - Saint(s) of the day
  - Daily epistle + gospel (with RSV text)
  - Tone of the week (if computable)

Usage:
    python3 calendar_lookup.py                    # today
    python3 calendar_lookup.py 2026-07-21         # specific date
    python3 calendar_lookup.py --week             # next 7 days digest
    python3 calendar_lookup.py --week 2026-07-21  # week starting from date
"""

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).parent
READINGS_FILE = HERE / "docs" / "readings_2025-2035-final.json"
MENAION_FILE = HERE / "menaion_complete.json"

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def load_readings():
    with open(READINGS_FILE) as f:
        return json.load(f)


def load_menaion():
    with open(MENAION_FILE) as f:
        return json.load(f)


def get_saint(menaion, dt):
    """Return saint info for a date, or None."""
    month_str = str(dt.month)
    day_str = str(dt.day)
    month_data = menaion.get(month_str, {})
    return month_data.get(day_str)


def fmt_saint(saint):
    """Render saint(s) as a one-line summary."""
    if not saint:
        return "*No fixed commemorations in the Menaion.*"
    parts = []
    name = saint.get("saint")
    if name:
        parts.append(name)
    extra = saint.get("additional_saints", [])
    if extra:
        parts.append("; " + "; ".join(extra))
    return "\n".join(parts) if parts else "(Menaion entry present but no saint name)"


def fmt_reading(reading):
    """Render one reading (epistle or gospel) compactly."""
    if not reading:
        return "*None.*"
    out = []
    display = reading.get("display", "?")
    # Some entries already include the book in display; some don't.
    # Prefer 'display' alone; fall back to book + display.
    book = reading.get("book", "")
    if book and not display.lower().startswith(book.lower()):
        out.append(f"**{book} {display}**")
    else:
        out.append(f"**{display}**")
    if reading.get("pericope"):
        out.append(f"*Pericope {reading['pericope']}*")
    text = reading.get("rsv_text")
    if text:
        out.append("")
        out.append(f"> {text}")
    return "\n".join(out)


def digest_one(readings, menaion, dt):
    """Build the markdown digest for a single date."""
    iso = dt.isoformat()
    out = []
    out.append(f"# {dt.strftime('%A, %B %-d, %Y')} ({iso})")
    out.append("")

    # Liturgical position (from live 10-year JSON)
    entry = readings.get(iso, {})
    title = entry.get("title", "")
    if title:
        out.append(f"**Liturgical day:** {title}")
    if entry.get("feast_name"):
        out.append(f"**Feast:** {entry['feast_name']} (level {entry.get('feast_level', '?')})")
    out.append("")

    # Saint(s) (from menaion)
    saint = get_saint(menaion, dt)
    out.append("**Saints commemorated:**")
    out.append(fmt_saint(saint))
    out.append("")

    # Daily epistle + gospel
    if entry.get("epistle"):
        out.append("## Epistle")
        out.append(fmt_reading(entry["epistle"]))
        out.append("")
    if entry.get("gospel"):
        out.append("## Gospel")
        out.append(fmt_reading(entry["gospel"]))
        out.append("")

    # Saint readings (if feast has them)
    if entry.get("saint_epistle") or entry.get("saint_gospel"):
        out.append("## Saint's own readings")
        if entry.get("saint_epistle"):
            out.append(fmt_reading(entry["saint_epistle"]))
            out.append("")
        if entry.get("saint_gospel"):
            out.append(fmt_reading(entry["saint_gospel"]))
            out.append("")

    # Source citation
    out.append("---")
    out.append("*Source: liturginator data (10-year readings JSON + menaion).*")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("date", nargs="?", help="ISO date (YYYY-MM-DD); default = today")
    p.add_argument("--week", action="store_true", help="Show next 7 days from given date")
    args = p.parse_args()

    readings = load_readings()
    menaion = load_menaion()

    if args.date:
        try:
            start = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            sys.exit(f"Bad date: {args.date}")
    else:
        start = date.today()

    if args.week:
        for offset in range(7):
            dt = start + timedelta(days=offset)
            print(digest_one(readings, menaion, dt))
            print()
            print("=" * 72)
            print()
    else:
        print(digest_one(readings, menaion, start))


if __name__ == "__main__":
    main()
