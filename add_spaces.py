with open('resource/hexapsalm_matins.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

processed = []
for line in lines:
    stripped = line.rstrip()
    if stripped and not stripped.startswith('**') and not stripped.startswith('*') and stripped != '[The Royal Service]' and 'Logic Note' not in stripped:
        # Assume psalm lines, add two spaces
        processed.append(stripped + '  \n')
    else:
        processed.append(line)

with open('resource/hexapsalm_matins.md', 'w', encoding='utf-8') as f:
    f.writelines(processed)