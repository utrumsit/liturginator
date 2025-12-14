import json
import sys
from datetime import datetime

class Menaion:
    def __init__(self, data_file='menaion_complete.json'):
        with open(data_file, 'r') as f:
            self.data = json.load(f)

    def get_feast(self, month, day):
        """Get feast data for a given month and day.

        Args:
            month: Can be month number (int or str) or month name (str)
            day: Day of month (int or str)
        """
        # Convert month name to number if needed
        if isinstance(month, str) and not month.isdigit():
            try:
                month_num = str(datetime.strptime(month, '%B').month)
            except ValueError:
                return None
        else:
            month_num = str(int(month))

        day_str = str(day)
        if month_num in self.data and day_str in self.data[month_num]:
            return self.data[month_num][day_str]
        return None

    def get_stichera(self, month, day):
        """Get stichera for Lord I Have Cried at Vespers."""
        feast = self.get_feast(month, day)
        if feast and 'vespers' in feast:
            return feast['vespers'].get('stichera_lord_i_cried', [])
        return []

def bold(text):
    return f"\033[1m{text}\033[0m"

def print_feast(date_str, feast):
    print(f"{bold('Date:')} {date_str}")
    if feast:
        # Saint name
        saint = feast.get('saint', '')
        if saint:
            print(f"{bold('Saint:')} {saint}")

        # Feast level
        level = feast.get('feast_level', '')
        if level:
            print(f"{bold('Feast Level:')} {level}")

        # Troparia
        troparia = feast.get('troparia', {})
        if troparia:
            print(f"{bold('Troparia:')}")
            # Main troparion
            main = troparia.get('main', {})
            if main:
                tone = main.get('tone', '')
                text = main.get('text', '')
                print(f"  {bold(f'Tone {tone}:')}")
                for line in text.split('\n'):
                    print(f"    {line}")
            # Additional troparia
            for t in troparia.get('additional', []):
                tone = t.get('tone', '')
                text = t.get('text', '')
                print(f"  {bold(f'Tone {tone}:')}")
                for line in text.split('\n'):
                    print(f"    {line}")

        # Kontakia
        kontakia = feast.get('kontakia', {})
        if kontakia:
            print(f"{bold('Kontakia:')}")
            # Main kontakion
            main = kontakia.get('main', {})
            if main:
                tone = main.get('tone', '')
                text = main.get('text', '')
                print(f"  {bold(f'Tone {tone}:')}")
                for line in text.split('\n'):
                    print(f"    {line}")
            # Additional kontakia
            for k in kontakia.get('additional', []):
                tone = k.get('tone', '')
                text = k.get('text', '')
                print(f"  {bold(f'Tone {tone}:')}")
                for line in text.split('\n'):
                    print(f"    {line}")

        # Stichera
        vespers = feast.get('vespers', {})
        stichera = vespers.get('stichera_lord_i_cried', [])
        if stichera:
            print(f"{bold('Stichera at Lord I Have Cried:')} ({len(stichera)} stichera)")
            for i, s in enumerate(stichera, 1):
                tone = s.get('tone', '')
                melody = s.get('melody', '')
                text = s.get('text', '')
                header = f"  {bold(f'{i}. Tone {tone}')}"
                if melody:
                    header += f" (Melody: {melody})"
                print(header)
                for line in text.split('\n'):
                    print(f"    {line}")
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