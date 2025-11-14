import re

with open('resource/chasoslov.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find start of Hexapsalm: Psalm 3
start = content.find('Psalm 3', content.find('WEEKDAY AND LENTEN MATINS'))

# Find end: before Hymn of Light
end = content.find('Hymn of Light', start)

hexapsalm = content[start:end].strip()

# Clean: remove "The Book of Hours..." and page numbers
hexapsalm = re.sub(r'The Book of Hours:.*?\n', '', hexapsalm)
hexapsalm = re.sub(r'\n\d+\n', '\n', hexapsalm)
hexapsalm = re.sub(r'\n\s*\n\s*\n', '\n\n', hexapsalm)  # reduce multiple newlines

with open('resource/hexapsalm_matins.md', 'w', encoding='utf-8') as f:
    f.write(hexapsalm)