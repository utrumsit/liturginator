import json
import re

# Load the JSON
with open('menaion_data.json', 'r') as f:
    data = json.load(f)

# Function to clean text: replace page references with full text
def clean_text(text):
    # Replace specific page references with full hymns
    replacements = {
        r'Your martyrs, O Lord our God: see page 551\.?': 'Your martyrs, O Lord our God, in their struggles received incorruptible crowns from You. With Your strength, they brought down the tyrants and broke the cowardly valor of demons. Through their prayers, O Christ our God, save our souls.',
        r'Your martyrs, O Lord our God: See page 551\.?': 'Your martyrs, O Lord our God, in their struggles received incorruptible crowns from You. With Your strength, they brought down the tyrants and broke the cowardly valor of demons. Through their prayers, O Christ our God, save our souls.',
        # Add more as needed
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    # Remove any remaining "see page XXX"
    text = re.sub(r'see page \d+', '', text)
    text = re.sub(r'See page \d+', '', text)
    # Keep (Name) as placeholder
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to split hymns
def split_hymns(text):
    hymns = {}
    # Split on Troparion or Kontakion
    parts = re.split(r'((?:Troparion|Kontakion).*?:)', text)
    current_key = None
    for part in parts:
        part = part.strip()
        if re.match(r'(Troparion|Kontakion).*?:', part):
            current_key = part
            hymns[current_key] = ''
        elif current_key and part:
            hymns[current_key] += part + ' '
    # Clean
    for key in hymns:
        hymns[key] = clean_text(hymns[key])
    return hymns

# Function to get saint name
def get_saint_name(saints):
    for saint in saints:
        # Extract name after "The Holy" or similar
        match = re.search(r'The Holy.*?([A-Z][a-z]+)', saint)
        if match:
            return match.group(1)
    return "Saint"

# Refine the data
for month in data:
    for day in data[month]:
        feast = data[month][day]
        saint_name = get_saint_name(feast.get('saints', []))
        troparia = feast.get('troparia', {})
        kontakia = feast.get('kontakia', {})
        
        # Clean and replace page references
        for hymns_dict in [troparia, kontakia]:
            for key in hymns_dict:
                hymns_dict[key] = clean_text(hymns_dict[key])
        
        # Re-split only if embedded hymns
        all_hymns = {}
        for hymns_dict in [troparia, kontakia]:
            for key, text in hymns_dict.items():
                if 'Troparion' in text or 'Kontakion' in text:
                    # Has embedded hymns, split
                    all_hymns.update(split_hymns(text))
                else:
                    # No embedded, keep as is
                    all_hymns[key] = text
        
        # Separate into troparia and kontakia
        new_troparia = {}
        new_kontakia = {}
        for key, text in all_hymns.items():
            if 'Troparion' in key:
                new_troparia[key] = text
            elif 'Kontakion' in key:
                new_kontakia[key] = text
        
        feast['troparia'] = new_troparia
        feast['kontakia'] = new_kontakia
        
        # Clean all texts
        for key in troparia:
            troparia[key] = clean_text(troparia[key])
        for key in kontakia:
            kontakia[key] = clean_text(kontakia[key])

# Save the refined JSON
with open('menaion_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Refined menaion_data.json: split embedded kontakia and cleaned page references.")