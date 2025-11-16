import json
import re

# Read the chasoslov.md file
with open('resource/chasoslov.md', 'r') as f:
    content = f.read()

# Find the Theotokia section
start_pattern = r'Theotokia and Stavrotheotokia of the Eight Tones'
start_match = re.search(start_pattern, content)
if not start_match:
    raise ValueError("Theotokia section not found")

start_pos = start_match.start()

# Find the end of the section (next major section)
end_pattern = r'Troparia and Kontakia of the\s+Classes of Saints'
end_match = re.search(end_pattern, content[start_pos:])
if not end_match:
    raise ValueError("End of Theotokia section not found")

end_pos = start_pos + end_match.start()

section = content[start_pos:end_pos]

# Parse the tones
tones = {}
current_tone = None
current_type = None  # 'standard' or 'stavro'
current_text = ''

lines = section.split('\n')
i = 0
while i < len(lines):
    line = lines[i].strip()
    if 'Theotokion, Tone' in line and ':' in line:
        # Save previous
        if current_tone and current_type and current_text:
            if current_type not in tones[current_tone]:
                tones[current_tone][current_type] = []
            tones[current_tone][current_type].append(current_text.strip())
        match = re.search(r'Tone (\d+)', line)
        if match:
            tone_num = int(match.group(1))
            current_tone = tone_num
            current_type = 'standard'
            if current_tone not in tones:
                tones[current_tone] = {'standard': [], 'stavro': []}
            current_text = ''
    elif 'Stavrotheotokion, Tone' in line and ':' in line:
        # Save previous
        if current_tone and current_type and current_text:
            if current_type not in tones[current_tone]:
                tones[current_tone][current_type] = []
            tones[current_tone][current_type].append(current_text.strip())
        match = re.search(r'Tone (\d+)', line)
        if match:
            tone_num = int(match.group(1))
            current_tone = tone_num
            current_type = 'stavro'
            if current_tone not in tones:
                tones[current_tone] = {'standard': [], 'stavro': []}
            current_text = ''
    elif current_type and line and not re.match(r'^\d+$', line) and not line.startswith('Troparia'):
        current_text += line + '\n'
    i += 1

# Save last one
if current_tone and current_type and current_text:
    if current_type not in tones[current_tone]:
        tones[current_tone][current_type] = []
    tones[current_tone][current_type].append(current_text.strip())

# Clean up
for tone in tones:
    for typ in tones[tone]:
        tones[tone][typ] = [text.strip() for text in tones[tone][typ]]

# Write to JSON
with open('theotokia.json', 'w') as f:
    json.dump(tones, f, indent=2)

print("Extracted Theotokia to theotokia.json")