import json
import re

# Read the chasoslov.md file
with open('resource/chasoslov.md', 'r') as f:
    content = f.read()

# Find the Resurrection Troparia section
start_pattern = r'Troparia and Kontakia of the Resurrection\s+of the Eight Tones'
start_match = re.search(start_pattern, content)
if not start_match:
    raise ValueError("Resurrection Troparia section not found")

start_pos = start_match.start()

# Find the end of the section (next major section)
end_pattern = r'Troparia and Kontakia of the\s+Days of the Week'
end_match = re.search(end_pattern, content[start_pos:])
if not end_match:
    raise ValueError("End of Resurrection Troparia section not found")

end_pos = start_pos + end_match.start()

section = content[start_pos:end_pos]

# Parse the tones
tones = {}
current_tone = None
current_part = None

lines = section.split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    if re.match(r'TONE \w+', line.upper()):
        # New tone
        tone_num = re.search(r'TONE (\w+)', line.upper()).group(1)
        if tone_num == 'ONE':
            current_tone = 1
        elif tone_num == 'TWO':
            current_tone = 2
        elif tone_num == 'THREE':
            current_tone = 3
        elif tone_num == 'FOUR':
            current_tone = 4
        elif tone_num == 'FIVE':
            current_tone = 5
        elif tone_num == 'SIX':
            current_tone = 6
        elif tone_num == 'SEVEN':
            current_tone = 7
        elif tone_num == 'EIGHT':
            current_tone = 8
        tones[current_tone] = {'troparion': '', 'theotokion': '', 'hypakoe': ''}
        current_part = None
    elif line.upper() == 'TROPARION':
        current_part = 'troparion'
    elif line.upper() == 'THEOTOKION':
        current_part = 'theotokion'
    elif line.upper() == 'HYPAKOJ' or line.upper() == 'HYPAKOE':
        current_part = 'hypakoe'
    elif current_part and line and not line.startswith('TONE') and not re.match(r'^\d+$', line):
        # Accumulate text
        if tones[current_tone][current_part]:
            tones[current_tone][current_part] += '\n'
        tones[current_tone][current_part] += line
    i += 1

# Clean up the texts (remove extra newlines, etc.)
for tone in tones:
    for part in tones[tone]:
        tones[tone][part] = tones[tone][part].strip()

# Write to JSON
with open('resurrection_troparia.json', 'w') as f:
    json.dump(tones, f, indent=2)

print("Extracted Resurrection Troparia to resurrection_troparia.json")