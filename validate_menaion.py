import json
import re

# Load the actual menaion_data.json
with open('menaion_data.json', 'r') as f:
    actual = json.load(f)

# Load chasoslov.md
with open('resource/chasoslov.md', 'r') as f:
    content = f.read()

# Find the Menologion section
start_pattern = r'Menologion\s*-\s*September'
start_match = re.search(start_pattern, content)
if not start_match:
    print("Menologion start not found")
    exit(1)

start_pos = start_match.start()

# End at "We Praise You, O God"
end_pattern = r'We Praise You, O God'
end_match = re.search(end_pattern, content[start_pos:])
if end_match:
    end_pos = start_pos + end_match.start()
else:
    end_pos = len(content)

section = content[start_pos:end_pos]

# Parse expected data
expected = {}
current_month = None
current_date = None
current_feast = {}

lines = section.split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    # Month header
    if re.match(r'Menologion\s*-\s*\w+', line):
        month_match = re.search(r'Menologion\s*-\s*(\w+)', line)
        if month_match:
            current_month = month_match.group(1)
            expected[current_month] = {}
    # Date
    elif re.match(r'^\d+$', line) and current_month:
        current_date = line
        current_feast = {'saints': [], 'troparia': {}, 'kontakia': {}}
        expected[current_month][current_date] = current_feast
    # Saints (until Troparion or Kontakion)
    elif line and current_date and not line.startswith('Troparion') and not line.startswith('Kontakion') and not re.match(r'^\d+$', line):
        if 'saints' not in current_feast:
            current_feast['saints'] = []
        current_feast['saints'].append(line)
    # Hymns
    elif (line.startswith('Troparion') or line.startswith('Kontakion')) and current_date:
        hymn_type = 'troparia' if line.startswith('Troparion') else 'kontakia'
        key = line
        text = ''
        i += 1
        while i < len(lines) and not re.match(r'^\d+$', lines[i].strip()) and not lines[i].strip().startswith('Menologion'):
            line_text = lines[i].strip()
            if line_text and not line_text.startswith('And'):
                text += line_text + '\n'
            i += 1
        text = text.strip()
        if text:
            current_feast[hymn_type][key] = text
        i -= 1  # Adjust
    i += 1

# Clean expected (replace page refs with full texts)
def clean_text(text):
    replacements = {
        r'Your martyrs, O Lord our God: see page 551\.?': 'Your martyrs, O Lord our God, in their struggles received incorruptible crowns from You. With Your strength, they brought down the tyrants and broke the cowardly valor of demons. Through their prayers, O Christ our God, save our souls.',
        r'Your martyrs, O Lord our God: See page 551\.?': 'Your martyrs, O Lord our God, in their struggles received incorruptible crowns from You. With Your strength, they brought down the tyrants and broke the cowardly valor of demons. Through their prayers, O Christ our God, save our souls.',
        r'Your martyr.*?: see page 550\.?': 'Your martyr (Name), O Lord our God, in his struggle received an incorruptible crown from You. With Your strength, he brought down the tyrants and broke the cowardly valor of demons. Through his prayers, O Christ our God, save our souls.',
        # Add more as needed
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r'see page \d+', '', text)
    text = re.sub(r'See page \d+', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

for month in expected:
    for date in expected[month]:
        feast = expected[month][date]
        for hymns in [feast['troparia'], feast['kontakia']]:
            for k in list(hymns.keys()):
                hymns[k] = clean_text(hymns[k])

# Compare
errors = []
for month in expected:
    if month not in actual:
        errors.append(f"Missing month: {month}")
        continue
    for date in expected[month]:
        if date not in actual[month]:
            errors.append(f"Missing date: {month} {date}")
            continue
        exp_feast = expected[month][date]
        act_feast = actual[month][date]
        
        # Compare saints
        exp_saints = set(exp_feast['saints'])
        act_saints = set(act_feast['saints'])
        if exp_saints != act_saints:
            errors.append(f"Saints mismatch for {month} {date}: Expected {exp_saints}, Got {act_saints}")
        
        # Compare hymns
        for typ in ['troparia', 'kontakia']:
            exp_hymns = exp_feast[typ]
            act_hymns = act_feast[typ]
            for key, exp_text in exp_hymns.items():
                if key not in act_hymns:
                    errors.append(f"Missing hymn {typ} for {month} {date}: {key}")
                elif exp_text not in act_hymns[key]:
                    errors.append(f"Hymn text mismatch for {month} {date} {typ}: Expected contains '{exp_text[:50]}...', Got '{act_hymns[key][:50]}...'")

# Report
if errors:
    print("Errors found:")
    for err in errors:
        print(f"- {err}")
else:
    print("No errors found!")

# Save expected for reference
with open('expected_menaion.json', 'w') as f:
    json.dump(expected, f, indent=2)