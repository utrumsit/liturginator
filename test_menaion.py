import json
import subprocess
import sys
from datetime import datetime

# Load menaion data
with open('menaion_data.json', 'r') as f:
    data = json.load(f)

def run_menaion(date_str):
    """Run menaion.py and return output."""
    result = subprocess.run([sys.executable, 'menaion.py', date_str], capture_output=True, text=True)
    return result.stdout

def test_date(month, day, feast):
    """Test a single date."""
    # Use a leap year to handle Feb 29
    month_num = datetime.strptime(month, '%B').month
    day_num = int(day)
    dt = datetime(2024, month_num, day_num)
    date_str = dt.strftime('%Y-%m-%d')
    
    output = run_menaion(date_str)
    
    # Check saints
    saints = feast.get('saints', [])
    for saint in saints:
        if saint not in output:
            return False, f"Missing saint: {saint}"
    
    # Check troparia
    troparia = feast.get('troparia', {})
    for key, text in troparia.items():
        if text not in output:
            return False, f"Missing troparion text: {text[:50]}..."
    
    # Check kontakia
    kontakia = feast.get('kontakia', {})
    for key, text in kontakia.items():
        if text not in output:
            return False, f"Missing kontakion text: {text[:50]}..."
    
    return True, "Pass"

# Test all dates with hymns
passes = 0
fails = 0
for month in data:
    for date in data[month]:
        try:
            day_num = int(date)
            if not 1 <= day_num <= 31:
                continue
        except ValueError:
            continue
        feast = data[month][date]
        if feast.get('troparia') or feast.get('kontakia'):
            success, msg = test_date(month, date, feast)
            if success:
                passes += 1
                print(f"✓ {month} {date}: {msg}")
            else:
                fails += 1
                print(f"✗ {month} {date}: {msg}")

print(f"\nTotal: {passes} passes, {fails} fails")