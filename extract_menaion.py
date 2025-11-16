import json
import re

def lookup_hymn(phrase):
    """Lookup full hymn text in classes_raw.md based on first phrase."""
    try:
        with open('classes_raw.md', 'r') as f:
            content = f.read()
        # Find the phrase and extract the following text until next hymn or marker
        start = content.find(phrase)
        if start == -1:
            return phrase  # Fallback
        # Find end: next "Troparion" or "Kontakion" or "page:" or end of paragraph
        end = content.find('\n\n', start)
        if end == -1:
            end = len(content)
        full_text = content[start:end].strip()
        return full_text
    except FileNotFoundError:
        return phrase

def replace_page_refs(text):
    # First, handle known abbreviations
    if 'see page' in text.lower():
        # Extract phrase before "see page"
        phrase = re.split(r':?\s*see page', text, flags=re.IGNORECASE)[0].strip()
        if phrase:
            full_text = lookup_hymn(phrase)
            if full_text != phrase:  # Found better
                return full_text
    # Fallback to manual replacements
    replacements = {
        # Add any manual ones if needed
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r'see page \d+', '', text)
    text = re.sub(r'See page \d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Read the chasoslov.md file
with open('menaion_raw.md', 'r') as f:
    content = f.read()

# Start from the beginning
start_pos = 0

# Find the end of Menologion (before The Monastic Rule)
end_pattern = r'The Monastic Rule'
end_match = re.search(end_pattern, content[start_pos:])
if end_match:
    end_pos = start_pos + end_match.start()
else:
    end_pos = len(content)

# For now, to include all, set to end
end_pos = len(content)

section = content[start_pos:end_pos]
print(f"Section length: {len(section)}")

# Parse the Menologion
menaion = {}
current_month = None
current_date = None
current_feast = {}

lines = section.split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    # Month header
    if line.startswith('month:'):
        month_match = re.search(r'month:\s*(\w+)', line)
        if month_match:
            current_month = month_match.group(1)
            print(f"Found month: {current_month}")
            if current_month not in menaion:
                menaion[current_month] = {}
    # Date number
    elif line.startswith('day:'):
        date_match = re.search(r'day:\s*(\d+)', line)
        if date_match:
            current_date = date_match.group(1)
            current_feast = {'saints': [], 'troparia': {}, 'kontakia': {}, 'notes': []}
            menaion[current_month][current_date] = current_feast
    # Saints and notes
    elif line and not line.startswith('Troparion') and not line.startswith('Kontakion') and not line.startswith('month:') and not line.startswith('day:') and not line.startswith('page:') and not line.startswith('header:') and current_date:
        if 'Leave-taking' in line or 'Pre-festive' in line or 'Fore-feast' in line or 'beginning of the' in line.lower():
            current_feast['notes'].append(line)
        else:
            current_feast['saints'].append(line)
    # Hymns
    elif ('Troparion' in line or 'Kontakion' in line) and current_date:
        hymn_type = 'troparia' if 'Troparion' in line else 'kontakia'
        key = line
        text = ''
        i += 1
        while i < len(lines) and not (lines[i].strip().startswith('day:') or lines[i].strip().startswith('Troparion') or lines[i].strip().startswith('Kontakion') or lines[i].strip().startswith('month:')):
            line_text = lines[i].strip()
            if line_text and not line_text.startswith('And') and not line_text.startswith('page:') and not line_text.startswith('header:'):
                text += line_text + '\n'
            i += 1
        text = replace_page_refs(text.strip())
        if text:
            current_feast[hymn_type][key] = text
        i -= 1  # Adjust for loop
    i += 1

# Clean up
for month in list(menaion.keys()):
    for date in list(menaion[month].keys()):
        # Remove invalid dates
        try:
            day_num = int(date)
            if day_num < 1 or day_num > 31:
                del menaion[month][date]
                continue
        except ValueError:
            del menaion[month][date]
            continue
        # Clean saints
        saints = [s for s in menaion[month][date]['saints'] if s and not re.match(r'^\d+$', s)]
        menaion[month][date]['saints'] = saints

# Debug
print(f"Extracted data: {len(menaion)} months")

# Write to JSON
with open('menaion_data.json', 'w') as f:
    json.dump(menaion, f, indent=2)

print("Extracted full Menaion data to menaion_data.json")