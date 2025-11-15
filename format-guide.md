# Formatting Steps for Chunks

This document outlines the steps and scripts used to clean and format the liturgical text chunks extracted from `chasoslov.md`. These steps ensure consistent, readable Markdown files for reuse in the liturginator.

## Overview
- **Source**: Text extracted from PDF-derived Markdown (`chasoslov.md`).
- **Issues**: Duplicate spaces, page numbers, unwanted headers, long lines, inconsistent formatting.
- **Goal**: Clean, linted Markdown with preserved liturgical content.

## Steps

### 1. Manual Extraction and Initial Cleaning
- Extract sections from `chasoslov.md` using line ranges or patterns.
- Remove:
  - Page numbers (e.g., "12", "13").
  - "The Book of Hours: Časoslov" lines.
  - Unwanted headers (e.g., "Weekday and Lenten Matins").
- Save to `resource/*.md` files.

### 2. Remove Unwanted Lines
- Use `sed` to remove specific lines:
  ```
  sed -i '' '/^Weekday and Lenten Matins$/d' resource/*matins.md
  ```
- Or edit files manually for precision.

### 3. Markdown Linting
- Install `markdownlint-cli` via Homebrew: `brew install markdownlint-cli`.
- Run auto-fix: `markdownlint --fix resource/*.md`.
- Fixes: Trailing spaces, minor formatting. Note: Long lines (common in liturgical text) are flagged but not auto-fixed to preserve content.

### 4. Clean Duplicate Spaces
- Run the Python script `clean_spaces.py`:
  ```python
  import os
  import re

  directory = 'resource/'

  for filename in os.listdir(directory):
      if filename.endswith('.md'):
          filepath = os.path.join(directory, filename)
          with open(filepath, 'r', encoding='utf-8') as f:
              content = f.read()

          # Replace multiple spaces with single space
          cleaned = re.sub(r' {2,}', ' ', content)

          # Trim trailing spaces
          cleaned = '\n'.join(line.rstrip() for line in cleaned.split('\n'))

          with open(filepath, 'w', encoding='utf-8') as f:
              f.write(cleaned)

          print(f"Cleaned {filename}")
  ```
- This removes extra spaces from OCR/PDF artifacts while keeping structure.

## Scripts
- `clean_spaces.py`: Cleans spaces in all `.md` files.
- Future scripts: Add here as needed.

## Rubrics Guide
Rubrics are liturgical instructions (e.g., who says what, repetitions). Mark them in *italics* for clarity. Apply to all files eventually.

### Identifying Rubrics
- Speaker indicators: "If there is a priest, he says:", "If there is no priest, say:", "We:", "The priest:".
- Repetitions: "Three times", "12" (meaning "12 times").
- Structural cues: "Glory:", "now and ever:" (consider expanding to full text if short).
- Other: Any non-prayer text directing the liturgy.

### Formatting
- Wrap in `*italics*`: `*If there is a priest, he says:*`
- For numbers like "12", change to `*Twelve times*` or keep as `*12*` if space-constrained.
- Expand abbreviations: "Glory:" to `*Glory to the Father, and to the Son, and to the Holy Spirit:*` if it fits the flow.
- **Poetic Formatting**: For verse-like or poetic lines (e.g., "Come let us worship...", psalm verses), add two spaces after periods to preserve line breaks in rendering. Example: "Come let us worship our King and God.  " (note the two spaces).
- **Expand Abbreviations**: Replace abbreviated prayers (e.g., "Come let us worship:", "Trisagion.") with full text from other chunks (e.g., from introductory_prayers.md) to provide complete prayers. Generally prefer full prayers over abbreviations for clarity and completeness.

## Specific Formatting Rules
- **Introductory Prayers**: Certain prayers should be on single lines for better flow:
  - Trisagion: "Holy God, Holy and Mighty, Holy and Immortal, have mercy on us." (no line break before "mercy on us").
  - Doxology: "For Thine is the kingdom, and the power, and the glory, Father, Son, and Holy Spirit, now and ever and forever." (single line).
  - Final Invocation: "Come, let us worship and bow before the only Lord Jesus Christ, the King and our God." (single line).

### Application
- Manually edit files or use a script to wrap patterns (e.g., regex for ":\s*$" but carefully).
- Example: Change "Glory:" to `*Glory:*` or expand.
- Test rendering to ensure readability.

## Files Affected
- `resource/introductory_prayers.md`
- `resource/*_matins.md`
- And any new chunks.