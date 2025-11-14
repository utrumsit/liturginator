import os
import re

# Directory with the files
directory = 'resource/'

# Process all .md files
for filename in os.listdir(directory):
    if filename.endswith('.md'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace multiple spaces with single space
        cleaned = re.sub(r' {2,}', ' ', content)

        # Optionally, fix any leading/trailing spaces on lines, but keep structure
        cleaned = '\n'.join(line.rstrip() for line in cleaned.split('\n'))

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)

        print(f"Cleaned {filename}")