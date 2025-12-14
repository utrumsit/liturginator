#!/usr/bin/env python3
"""
Kathismanator: Determine the kathismata for Matins and Vespers based on date and liturgical season,
and display the psalm texts with navigation.
"""

import argparse
import re
import sys
from datetime import date, timedelta
from rich.console import Console
from rich.markdown import Markdown
console = Console()

def calculate_catholic_easter(year):
    """
    Calculate the date of Catholic Easter for the given year
    using the Gregorian calendar (Meeus algorithm).
    """
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
    return date(year, month, day)

def is_lent(today):
    """
    Check if the given date is within Lent.
    """
    year = today.year
    easter = calculate_catholic_easter(year)
    clean_monday = easter - timedelta(days=55)
    lazarus_saturday = easter - timedelta(days=8)
    return clean_monday <= today <= lazarus_saturday

def get_season(today, pascha):
    """
    Determine the liturgical season for the given date.
    Returns: 'lent', 'bright_week', 'summer', 'winter', or None if no kathismata.
    """
    if is_lent(today):
        return 'lent'
    
    # Bright Week: Pascha to Pascha + 6 days
    if pascha <= today < pascha + timedelta(days=7):
        return 'bright_week'
    
    # Christmas season: Dec 20 to Jan 14
    christmas_start = date(today.year, 12, 20)
    christmas_end = date(today.year + 1, 1, 14) if today.month == 12 else date(today.year, 1, 14)
    if christmas_start <= today <= christmas_end:
        return 'summer'
    
    # Cheesefare Sunday: Pascha - 56 days
    cheesefare_sunday = pascha - timedelta(days=56)
    clean_monday = pascha - timedelta(days=55)
    # Meatfare Week: week before Cheesefare
    meatfare_sunday = cheesefare_sunday - timedelta(days=7)
    if meatfare_sunday <= today < clean_monday:
        return 'summer'
    
    # Summer: Thomas Sunday (Pascha +7) to Sept 21
    thomas_sunday = pascha + timedelta(days=7)
    summer_end = date(today.year, 9, 21)
    if thomas_sunday <= today <= summer_end:
        return 'summer'
    
    # Prodigal Son Sunday: Pascha - 70 days
    prodigal_sunday = pascha - timedelta(days=70)
    winter_start = date(today.year, 9, 22)
    if winter_start <= today <= prodigal_sunday:
        return 'winter'
    
    # Default to winter if not covered
    return 'winter'

# Define schedules
SUMMER_MATINS = {
    6: [2, 3],  # Sun
    0: [4, 5],  # Mon
    1: [7, 8],  # Tue
    2: [10, 11],  # Wed
    3: [13, 14],  # Thu
    4: [19, 20],  # Fri
    5: [16, 17],  # Sat
}

SUMMER_VESPERS = {
    0: [6],
    1: [9],
    2: [12],
    3: [15],
    4: [18],
    5: [1],
    6: None,
}

WINTER_MATINS = {
    0: [4, 5, 6],
    1: [7, 8, 9],
    2: [10, 11, 12],
    3: [13, 14, 15],
    4: [19, 20],
    5: [16, 17],
    6: [2, 3, 17],
}

WINTER_VESPERS = {
    0: [18],
    1: [18],
    2: [18],
    3: [18],
    4: [18],
    5: [1],
    6: None,
}

LENT_MATINS = {
    0: [4, 5, 6],
    1: [10, 11, 12],
    2: [19, 20, 1],
    3: [6, 7, 8],
    4: [13, 14, 15],
    5: [16, 17],
    6: [2, 3, 17],
}

LENT_VESPERS = WINTER_VESPERS  # Same as winter

# Prayers after each stasis (not the Little Ektenia)
STASIS_ENDING_BASE = """
Glory to the Father and to the Son and to the Holy Spirit; Now and ever and unto ages of ages. Amen.

Alleluia, alleluia, alleluia. Glory to You, O God. *Three times.*

Lord, have mercy. *Three times.*

Glory to the Father and to the Son and to the Holy Spirit; Now and ever and unto ages of ages. Amen.

"""

STASIS_EXCLAMATION_1 = """*The priest exclaims:* For Yours is the might, and Yours are the kingdom and the power and the glory, Father, Son, and Holy Spirit, now and ever and forever.

*Choir:* Amen."""

STASIS_EXCLAMATION_2 = """*The priest exclaims:* For You are a good and loving God, and we give glory to You, Father, Son, and Holy Spirit, now and ever and forever.

*Choir:* Amen."""

STASIS_EXCLAMATION_3 = """*The priest exclaims:* For You are our God, and we give glory to You, Father, Son, and Holy Spirit, now and ever and forever.

*Choir:* Amen."""

def get_stasis_ending(stasis_num):
    """
    Get the stasis ending prayers with the appropriate exclamation for the given stasis number.
    """
    if stasis_num == 1:
        exclamation = STASIS_EXCLAMATION_1
    elif stasis_num == 2:
        exclamation = STASIS_EXCLAMATION_2
    else:
        exclamation = STASIS_EXCLAMATION_3
    return STASIS_ENDING_BASE + exclamation

# The Little Ektenia - said only once after the entire kathisma
LITTLE_EKTENIA = """
### Little Ektenia

*Deacon:* Again and again, in peace, let us pray to the Lord.

*Choir:* Lord, have mercy.

*Deacon:* Protect us, save us, have mercy on us and preserve us, O God, by Your grace.

*Choir:* Lord, have mercy.

*Deacon:* Commemorating our most holy, most pure, most blessed and glorious Lady, the Theotokos and Ever-Virgin Mary, with all the saints, let us commit ourselves and one another and our whole life to Christ our God.

*Choir:* To You, O Lord.

*The priest exclaims:* For Yours is the might, and Yours are the kingdom and the power and the glory, Father, Son, and Holy Spirit, now and ever and forever.

*Choir:* Amen."""

def extract_kathisma_text(kathisma_num):
    """
    Extract the text for a given kathisma number from kathisma.md,
    adding the stasis ending prayers after each stasis, and the Little Ektenia
    at the very end of the kathisma.
    """
    try:
        with open('resource/kathisma.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return ""

    # Find the Kathisma section
    pattern = rf'#\s*Kathisma\s+{kathisma_num}\n(.*?)(?=#\s*Kathisma\s+\d+|$)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        extracted_text = match.group(1).strip()

        # Insert stasis ending prayers after each stasis
        stasis_pattern = r'(###\s*Stasis\s+\d+)'
        parts = re.split(stasis_pattern, extracted_text)

        # parts will be: [before_first_stasis, 'Stasis 1', content1, 'Stasis 2', content2, 'Stasis 3', content3]
        result_parts = []
        stasis_count = 0

        for i, part in enumerate(parts):
            if re.match(stasis_pattern, part):
                stasis_count += 1
                # Before stasis 2 and 3, add ending prayers from previous stasis
                if stasis_count > 1:
                    result_parts.append("\n" + get_stasis_ending(stasis_count - 1) + "\n\n")
                result_parts.append(part)
            else:
                result_parts.append(part)

        # Add ending prayers after stasis 3, then the Little Ektenia
        if stasis_count > 0:
            result_parts.append("\n" + get_stasis_ending(stasis_count) + "\n")
            result_parts.append(LITTLE_EKTENIA + "\n")

        return ''.join(result_parts).strip()
    else:
        return ""

def display_interactive(matins_kaths, vespers_kaths):
    """
    Display kathismata with Rich for pretty formatting and paging.
    """
    import os
    import sys
    import termios
    import tty
    console = Console()
    
    if not matins_kaths and not vespers_kaths:
        console.print("## Matins: None\n## Vespers: None")
        return
    
    # Get console dimensions
    try:
        rows, cols = os.popen('stty size', 'r').read().split()
        max_rows = int(rows) - 5
        max_cols = int(cols)
    except:
        max_rows = 20
        max_cols = 80
    
    def clear_and_print_header(service, k):
        console.clear()
        console.print(f"[bold magenta on black]SERVICE: {service} | KATHISMA {k}[/bold magenta on black]")
        console.print()
        return 2  # Header takes 2 lines
    
    def get_single_key(prompt):
        """Get single keypress without requiring Enter"""
        console.print(prompt, end="")
        sys.stdout.flush()
        
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            tty.setcbreak(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch.lower() == 'q':
                console.clear()
                return True  # Quit
            else:
                return False  # Continue
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            console.print()  # Newline after input
    
    def print_with_paging(lines, service, kathisma, max_rows, max_cols):
        """Print lines with proper screen paging"""
        current_line = 2  # Start after header
        
        for i, line in enumerate(lines):
            # Check if we need to page BEFORE printing the line
            if current_line >= max_rows:
                if get_single_key("\n[bold cyan]--- Press Enter for more (q to quit) ---[/bold cyan]"):
                    return True  # User quit
                clear_and_print_header(service, kathisma)
                current_line = 2  # Reset after header
            
            # Truncate long lines
            display_line = line[:max_cols] if len(line) > max_cols else line
            
            # Simple markdown detection for formatting
            if line.strip().startswith(('#', '>', '-', '*', '1.', '•')) or '|' in line:
                try:
                    # For simple markdown, just use basic formatting
                    if line.strip().startswith('#'):
                        display_line = f"[bold]{display_line}[/bold]"
                    console.print(display_line)
                except:
                    console.print(display_line)
            else:
                console.print(display_line)
                
            current_line += 1
        
        return False  # Continue flag
    
    # Show schedule first - keep it short and visible
    console.clear()
    console.print("[bold yellow on black]=== TODAY'S KATHISMATA ===[/bold yellow on black]\n")
    
    schedule_lines = []
    for service, kaths in [("Matins", matins_kaths), ("Vespers", vespers_kaths)]:
        if kaths:
            schedule_lines.append(f"[bold cyan]{service}:[/bold cyan] [bold green]{', '.join(map(str, kaths))}[/bold green]")
    
    # Print schedule - it's short, so no paging needed
    for line in schedule_lines:
        console.print(line)
    
    if get_single_key("\n[bold cyan]--- Press Enter for psalm texts (q to quit) ---[/bold cyan]"):
        return
    
    # Now show psalm texts
    for service, kaths in [("Matins", matins_kaths), ("Vespers", vespers_kaths)]:
        if kaths:
            for k in kaths:
                text = extract_kathisma_text(k)
                
                if text:
                    lines = text.split('\n')
                    
                    # Start with header
                    clear_and_print_header(service, k)
                    
                    # Page through content
                    if print_with_paging(lines, service, k, max_rows, max_cols):
                        return  # User exited
                        
                    # Pause between kathismata
                    if not (service == "Vespers" and k == kaths[-1]):
                        if get_single_key(f"\n[bold cyan]--- Press Enter for next kathisma (q to quit) ---[/bold cyan]"):
                            return
    
    console.clear()
    console.print("[bold green on black]End of kathismata. Glory to Jesus Christ![/bold green on black]")

def get_kathismata(season, weekday):
    if season == 'lent':
        matins = LENT_MATINS.get(weekday, [])
        vespers = LENT_VESPERS.get(weekday, None)
    elif season == 'summer':
        matins = SUMMER_MATINS.get(weekday, [])
        vespers = SUMMER_VESPERS.get(weekday, None)
    elif season == 'winter':
        matins = WINTER_MATINS.get(weekday, [])
        vespers = WINTER_VESPERS.get(weekday, None)
    else:
        matins = []
        vespers = None
    
    return matins, vespers

def format_kathismata(kaths):
    if not kaths:
        return "None"
    return ", ".join(f"Kathisma {k}" for k in kaths)

def main():
    parser = argparse.ArgumentParser(description="Determine kathismata for Matins and Vespers.")
    parser.add_argument(
        '-d', '--date',
        type=str,
        help='Date in YYYY-MM-DD format. If not provided, uses today.'
    )
    args = parser.parse_args()

    if args.date:
        try:
            today = date.fromisoformat(args.date)
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return
    else:
        today = date.today()

    year = today.year
    pascha = calculate_catholic_easter(year)
    season = get_season(today, pascha)
    
    if season == 'bright_week':
        print("#Matins: None")
        print("#Vespers: None")
        return
    
    weekday = today.weekday()  # 0=Mon, 6=Sun
    matins, vespers = get_kathismata(season, weekday)
    
    if sys.stdout.isatty():
        # Interactive mode: Use Rich for formatted, paginated display
        display_interactive(matins, vespers or [])
    else:
        # Non-interactive: Output plain markdown
        print(f"#Matins: {format_kathismata(matins)}")
        print(f"#Vespers: {format_kathismata(vespers)}")
        for service, kaths in [("Matins", matins), ("Vespers", vespers or [])]:
            if kaths:
                print(f"\n#{service}")
                for k in kaths:
                    text = extract_kathisma_text(k)
                    if text:
                        print(f"## Kathisma {k}")
                        print(text)
                        print()  # Blank line between kathismata

if __name__ == "__main__":
    main()