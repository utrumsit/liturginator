# Liturginator

A Python CLI app for Byzantine Catholic Church prayer texts.

## Installation

1. Clone or download the repository.
2. Set up the virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install click python-dateutil`

## Usage

- `python liturginator.py recite <prayer>`: Recite a prayer (trisagion, lords_prayer, credo, jesus_prayer)
- `python liturginator.py list-prayers`: List available prayers
- `python liturginator.py daily-liturgy [--date YYYY-MM-DD]`: Show daily liturgy
- `python liturginator.py vespers`: Show Vespers prayers
- `python liturginator.py favorite <prayer>`: Mark a prayer as favorite
- `python liturginator.py show-favorites`: Show favorite prayers
- `python liturginator.py search <query>`: Search prayers by text

## Features

- Recite common prayers
- Daily liturgy readings
- Vespers prayers
- Favorite prayers (persistent)
- Search functionality

## File Catalog

### Core Application Files
- `liturginator.py`: Main CLI application for generating liturgical services (Matins, Vespers, Hours) and reciting prayers.
- `menaion.py`: Class for querying menaion data (saints, hymns) by date.
- `pascha.py`: Calculates Orthodox Easter (Pascha) and checks Lent periods.
- `tone.py`: Determines liturgical tone based on date.
- `matins_logic.py`: Assembles full Matins service text from components.
- `vespers_logic.py`: Assembles Vespers service text.
- `hours_logic.py`: Assembles Hours service text.

### Data Files
- `menaion_data.json`: JSON database of ~351 menaion feasts with saints, troparia, kontakia, and notes.
- `resurrection_troparia.json`: Resurrection troparia and hymns by tone.
- `theotokia.json`: Theotokia hymns by tone.
- `favorites.json`: User-favorited prayers (persistent).

### Resource Files
- `resource/chasoslov.md`: Original source text for Byzantine liturgical prayers.
- `resource/matins/`: Directory with Matins components:
  - `introductory_prayers_matins.md`: Introductory prayers and psalms for Matins.
  - `hexapsalm_matins.md`: Six psalms for Matins.
  - `theLordisGod.md`: "The Lord is God" hymn.
  - `praises_matins.md`: Praises section.
  - `dismissal_matins.md`: Dismissal prayers.
  - `royal_service.md`: Royal service prayers.
  - `priest_morningprayers.md`: Priest morning prayers.
- Other resource .md files: `chasoslovintro.md`, `kathisma.md`, `kathismata.md`, `GrailKathismata.md`, `introductory_prayers.md`.

### Scripts and Utilities
- Extraction scripts: `extract_menaion.py`, `extract_resurrection.py`, `extract_theotokia.py`, `extract_hexapsalm.py`, `extract_dismissal.py`.
- Cleaning/formatting: `clean_psalms.py`, `clean_spaces.py`, `tighten_formatting.py`, `add_spaces.py`.
- Testing/validation: `test_menaion.py`, `validate_menaion.py`, `check_empty_hymns.py`.
- Other: `merge_menaion.py`, `chunk_example.py`, `lent.py`, `kathismata.py`.

### Documentation
- `README.md`: This file – project overview, installation, usage.
- `architecture.md`: High-level project architecture and design.
- `men-check.md`: Checklist for menaion data validation.
- `format-guide.md`: Guide for text chunking, formatting, and maintenance.

### Temporary/Intermediate Files
- Raw data: `menaion_raw.md`, `menaion_raw_clean.md`, `menaion_raw_new.txt`, `classes_raw.md`, `classes_raw-1.md`.
- Examples/outputs: `chunk_example_output.txt`, `chunk_example.py`.
- Expected data: `expected_menaion.json`.
- Cache: `__pycache__/` (Python bytecode).
- Config: `.gitignore`, `.grok/settings.json`.

### Dependencies
- `requirements.txt`: Python packages (click, python-dateutil, rich, prompt_toolkit).

## Development

### Chunking and Formatting Text
Liturgical text is chunked from `resource/chasoslov.md` into modular `.md` files for easy assembly. See `format-guide.md` for the cleaning process, scripts, and tips to maintain consistency when adding new chunks.
