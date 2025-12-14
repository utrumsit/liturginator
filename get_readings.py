#!/usr/bin/env python3
"""
Get Daily Byzantine Lectionary Readings
Simple interface to get today's or any date's readings with RSV text

Usage:
    python get_readings.py               # Get today's readings
    python get_readings.py 2025-12-25    # Get readings for specific date
    python get_readings.py --today       # Explicitly get today's readings
"""

import sys
import datetime
import json
from lectionary_pdist import LectionaryPdist

def format_reading_output(result, compact=False):
    """Format the reading result for display in markdown"""
    if compact:
        # Compact JSON output
        return json.dumps(result, indent=2, default=str)
    
    # Markdown format
    lines = []
    lines.append(f"# {result['title']}")
    lines.append("")
    
    # Add feast name if present
    if result.get('feast_name'):
        lines.append(f"**{result['feast_name']}** (Feast Level {result.get('feast_level', '?')})")
        lines.append("")
    
    # Check if we have both daily and saint readings
    has_both = result.get('saint_epistle') or result.get('saint_gospel')
    
    if has_both:
        # Show daily readings first
        lines.append("## Daily Cycle Readings")
        lines.append("")
        
        if result.get('daily_epistle'):
            epistle = result['daily_epistle']
            lines.append(f"### Epistle: {epistle.get('display', 'N/A')}")
            lines.append("")
            if epistle.get('rsv_text'):
                lines.append(epistle['rsv_text'])
                lines.append("")
        
        if result.get('daily_gospel'):
            gospel = result['daily_gospel']
            lines.append(f"### Gospel: {gospel.get('display', 'N/A')}")
            lines.append("")
            if gospel.get('rsv_text'):
                lines.append(gospel['rsv_text'])
                lines.append("")
        
        # Show saint readings
        lines.append(f"## Saint Readings: {result.get('feast_name', 'Unknown')}")
        lines.append("")
        
        if result.get('saint_epistle'):
            epistle = result['saint_epistle']
            lines.append(f"### Epistle: {epistle.get('display', 'N/A')}")
            lines.append("")
            if epistle.get('rsv_text'):
                lines.append(epistle['rsv_text'])
                lines.append("")
        
        if result.get('saint_gospel'):
            gospel = result['saint_gospel']
            lines.append(f"### Gospel: {gospel.get('display', 'N/A')}")
            lines.append("")
            if gospel.get('rsv_text'):
                lines.append(gospel['rsv_text'])
                lines.append("")
    else:
        # Single set of readings
        if result.get('epistle'):
            epistle = result['epistle']
            lines.append(f"## Epistle: {epistle.get('display', 'N/A')}")
            lines.append("")
            if epistle.get('rsv_text'):
                lines.append(epistle['rsv_text'])
                lines.append("")
        
        if result.get('gospel'):
            gospel = result['gospel']
            lines.append(f"## Gospel: {gospel.get('display', 'N/A')}")
            lines.append("")
            if gospel.get('rsv_text'):
                lines.append(gospel['rsv_text'])
                lines.append("")
    
    return "\n".join(lines)


def main():
    """Main entry point"""
    # Parse arguments
    date = None
    compact = False
    
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == '--today'):
        # Use today's date
        date = datetime.date.today()
    elif '--json' in sys.argv:
        compact = True
        # Find the date argument
        for arg in sys.argv[1:]:
            if arg != '--json':
                try:
                    date = datetime.datetime.strptime(arg, '%Y-%m-%d').date()
                except ValueError:
                    pass
        if not date:
            date = datetime.date.today()
    else:
        # Parse date from first argument
        try:
            date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d').date()
        except (ValueError, IndexError):
            print(__doc__)
            sys.exit(1)
    
    # Initialize lectionary with RSV
    lect = LectionaryPdist(rsv_xml_path='rsv.xml')
    
    # Get readings
    result = lect.get_readings(date)
    
    # Output
    if compact:
        print(format_reading_output(result, compact=True))
    else:
        print(format_reading_output(result, compact=False))


if __name__ == '__main__':
    main()
