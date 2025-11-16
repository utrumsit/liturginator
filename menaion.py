import json
import sys
from datetime import datetime

class Menaion:
    def __init__(self, data_file='menaion_data.json'):
        with open(data_file, 'r') as f:
            self.data = json.load(f)
    
    def get_feast(self, month, day):
        month_str = month.capitalize()
        day_str = str(day)
        if month_str in self.data and day_str in self.data[month_str]:
            return self.data[month_str][day_str]
        return None

def bold(text):
    return f"\033[1m{text}\033[0m"

def print_feast(date_str, feast):
    print(f"{bold('Date:')} {date_str}")
    if feast:
        print(f"{bold('Saints:')}")
        for saint in feast.get('saints', []):
            print(f"  • {saint}")
        print(f"{bold('Troparia:')}")
        for key, text in feast.get('troparia', {}).items():
            print(f"  {bold(key)}")
            for line in text.split('\n'):
                print(f"    {line}")
        print(f"{bold('Kontakia:')}")
        for key, text in feast.get('kontakia', {}).items():
            print(f"  {bold(key)}")
            for line in text.split('\n'):
                print(f"    {line}")
        notes = feast.get('notes', [])
        if notes:
            print(f"{bold('Liturgical Notes:')}")
            for note in notes:
                print(f"  • {note}")
    else:
        print("No feast data available.")

if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Default to today
        today = datetime.now()
        month = today.strftime('%B')
        day = today.day
        date_str = today.strftime('%Y-%m-%d')
    elif len(sys.argv) == 2:
        # YYYY-MM-DD
        try:
            dt = datetime.strptime(sys.argv[1], '%Y-%m-%d')
            month = dt.strftime('%B')
            day = dt.day
            date_str = sys.argv[1]
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD or provide month and day.")
            sys.exit(1)
    elif len(sys.argv) == 3:
        # Month Day
        month = sys.argv[1]
        try:
            day = int(sys.argv[2])
            dt = datetime(2000, datetime.strptime(month, '%B').month, day)  # Dummy year
            date_str = dt.strftime('%Y-%m-%d')
        except (ValueError, KeyError):
            print("Invalid month or day.")
            sys.exit(1)
    else:
        print("Usage: python menaion.py [YYYY-MM-DD] or python menaion.py <month> <day>")
        sys.exit(1)
    
    menaion = Menaion()
    feast = menaion.get_feast(month, day)
    print_feast(date_str, feast)