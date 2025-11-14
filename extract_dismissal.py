import re

with open('resource/chasoslov.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find start: [The Doxology]
start = content.find('[The Doxology]', content.find('Weekday and Lenten Matins'))

# Find end: before SUNDAY AND FESTAL MATINS
end = content.find('SUNDAY AND FESTAL MATINS', start)

dismissal = content[start:end].strip()

# Clean
dismissal = re.sub(r'The Book of Hours:.*?\n', '', dismissal)
dismissal = re.sub(r'\n\d+\n', '\n', dismissal)
dismissal = re.sub(r'\n\s*\n\s*\n', '\n\n', dismissal)

with open('resource/dismissal_matins.md', 'w', encoding='utf-8') as f:
    f.write(dismissal)