# Liturginator

A Python CLI app for Byzantine Catholic Church prayer texts.

## Installation

1. Clone or download the repository.
2. Set up the virtual environment: `python3 -m venv venv`
3. Activate: `source venv/bin/activate`
4. Install dependencies: `pip install click`

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

## Development

### Chunking and Formatting Text
Liturgical text is chunked from `resource/chasoslov.md` into modular `.md` files for easy assembly. See `format-guide.md` for the cleaning process, scripts, and tips to maintain consistency when adding new chunks.
