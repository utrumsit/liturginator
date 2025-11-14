import re

# Read the chasoslov.md file
with open('resource/chasoslov.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Midnight Service section by searching for the heading
midnight_start = content.find('THE ORDER OF THE MIDNIGHT')
if midnight_start != -1:
    # For demo, take to the next major section
    saturday_start = content.find('SATURDAY MIDNIGHT SERVICE', midnight_start)
    if saturday_start != -1:
        midnight_end = saturday_start
    else:
        midnight_end = len(content)
    midnight_section = content[midnight_start:midnight_end]
    print(f"Section length: {len(midnight_section)}")
else:
    midnight_section = None

if midnight_section:
    # Write to a file for full output
    with open('chunk_example_output.txt', 'w', encoding='utf-8') as out:
        out.write("Found Midnight Service section:\n")
        out.write("=" * 50 + "\n")
        out.write(midnight_section + "\n")

        out.write("\nExample Markers in the text:\n")
        out.write("- 'Glory: now and ever:' separates troparia blocks.\n")
        out.write("- 'Lord, have mercy.' indicates responses.\n")
        out.write("- 'Tone 8:' indicates variable troparia.\n")

        # Extract fixed prayers, e.g., Lord's Prayer
        lords_prayer_pattern = r'Our Father, Who art in heaven.*?\.'
        lords_match = re.search(lords_prayer_pattern, midnight_section, re.DOTALL)
        if lords_match:
            out.write("\nExtracted Lord's Prayer (constant chunk):\n")
            out.write(lords_match.group(0) + "\n")

        # Show a variable part: the troparia at the end
        troparia_start = midnight_section.find('Behold, the Bridegroom comes')
        if troparia_start != -1:
            troparia_end = midnight_section.find('Then Lord, have mercy. 40.', troparia_start)
            if troparia_end == -1:
                troparia_end = len(midnight_section)
            troparia_block = midnight_section[troparia_start:troparia_end]
            out.write("\nExtracted Troparia Block (variable chunk, changes by day/tone):\n")
            out.write(troparia_block + "\n")

    print("Output written to chunk_example_output.txt")
else:
    print("Midnight Service section not found.")