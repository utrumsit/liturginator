# Liturginator Architecture Plan

## Overview
Liturginator is a Python program that generates the full liturgical texts for Matins, Vespers, and the Hours for a given date in the Byzantine Rite. It defaults to the current date but accepts user-specified dates. The program integrates solar (fixed feasts like Christmas) and lunar (Easter/Pascha-related) calendars to determine seasonal context, feast status, and appropriate prayers/hymns, assembling complete service texts from the Horologion (Časoslov).

## Core Functionality
- **Input**: Date (defaults to today; accepts YYYY-MM-DD format).
- **Processing**: Analyze solar/lunar calendar interactions to select hymns, prayers, and service structures.
- **Output**: Full texts for Matins, Vespers, and the Hours, formatted for recitation.

## Day Characteristics Analysis
The program integrates solar and lunar calendars to determine service content:

1. **Solar Calendar (Fixed Dates)**
   - Extract date components (year, month, day).
   - Check for fixed feasts (e.g., Christmas on Dec 25, Transfiguration on Aug 6).
   - Determine fasting/seasonal periods (e.g., Nativity Fast).
   - Output: Date info, fixed feast (if any), solar season.

2. **Lunar Calendar (Easter/Pascha-Related)**
   - Calculate Easter date for the year (via `pascha.py`).
   - Determine movable feasts, Lent, Pentecostarion, etc., relative to Pascha.
   - Output: Lunar season (e.g., "Great Lent", "Pentecost"), tone of the week.

3. **Combined Feast and Hymn Selection**
   - Query `menaion.py` for solar feasts; override with lunar if applicable (e.g., Pascha takes precedence).
   - If feast: Retrieve troparia, kontakia, theotokia from Menaion or Triodion/Pentecostarion.
   - If ordinary: Use Resurrection Troparia/Theotokia by tone; adjust for weekday (e.g., Monday angelic).
   - Output: Feast status, hymns, tone.

## Module Structure
- **`liturginator.py`**: Main script. Handles input, orchestrates calendar checks, assembles and outputs full service texts.
- **`menaion.py`**: Manages Menaion data. Loads solar feast hymns by date; returns feast details or "no feast".
- **`tone.py`**: Calculates octoechos tone for a given date.
- **`pascha.py`**: Handles Paschalion (Easter date) and lunar seasonal logic (e.g., Lent, Pentecost).
- **`matins_logic.py`**: Generates Matins text structure, incorporating hymns and prayers.
- **`vespers_logic.py`**: Generates Vespers text structure.
- **`hours_logic.py`**: Generates Hours text structure.
- **`gospel.py`**: Determines Gospel reading for the day, accounting for lunar calendar, fixed feasts, and Lucan Jump rules.
- **`epistle.py`**: Determines Epistle reading for the day, following similar rules as Gospel.
- **`lent.py`**: Handles Lenten-specific logic and texts.
- **Data Files**: Extracted from `chasoslov.md` and other sources:
  - `resurrection_troparia.json`: Dict of troparia/theotokia by tone.
  - `theotokia.json`: Dict of theotokia by tone (standard, stavro variants).
  - `menaion_data.json`: Nested dict of solar feasts by month/date.
  - `triodion_data.json`: Lenten/Paschalion hymns.
  - `horologion_texts.json`: Base prayers/psalms for Hours, Vespers, Matins.
  - `gospel_readings.json`: Database of Gospel pericopes by date/season.
  - `epistle_readings.json`: Database of Epistle pericopes by date/season.

## Data Extraction and Preparation
- Source: `resource/chasoslov.md`.
- Extraction Scripts: Separate Python scripts to parse and export JSON (e.g., `extract_resurrection.py`).
- Key Extractions:
  - Resurrection Troparia: 8 tones, each with troparion, theotokion, hypakoe.
  - Theotokia: 8 tones, with variants for days/seasons.
  - Menaion: Feast troparia by date, including levels (e.g., major feasts override Resurrection).
- Validation: Cross-check extracted data against source for completeness.

## Service Generation
- **Matins**: Assemble from `matins_logic.py`, including hexapsalm, praises, Gospel, and appointed hymns.
- **Vespers**: Include psalms, prokeimena, appointed hymns, and litia if applicable.
- **Hours**: Base on Horologion, with troparia/theotokia inserted per rules.
- **Hymn Integration**:
  - Priority: Feast hymns > Resurrection by tone.
  - Recitation: Single troparion twice + theotokion; two troparia: first twice + second + theotokion.
- **Full Text Assembly**: Combine static prayers from `chasoslov.md` with dynamic hymns.

## User Interface
- Command-line: `python liturginator.py [YYYY-MM-DD] [service]`, where service is matins/vespers/hours/all.
- Output: Full plain text for selected service(s), with sections (e.g., "Hexapsalm", "Troparia").
- Error Handling: Invalid dates, missing data, calendar conflicts.

## Future Extensions
- **Scripture Readings**: Implement `gospel.py` and `epistle.py` to generate daily Epistle and Gospel readings, handling lunar calendar cycles, fixed feast overrides, and the Lucan Jump (Matthew/Mark/Luke/John rotation with special rules for Lent and Pascha).
- Web interface or GUI.
- Additional services (e.g., Liturgy, Compline).
- Localization (Slavonic vs. English variants).
- Calendar generation for multiple days or weeks.

## Dependencies
- Python 3.x
- Standard libraries: `datetime`, `json`, `os`.
- Optional: `dateutil` for date parsing.

## Testing
- Unit tests for each module (e.g., tone calculation, feast lookup).
- Integration tests with known dates (e.g., Christmas, Pascha).
- Edge cases: Leap years, tone transitions, feast overrides.</content>
<parameter name="filePath">architecture.md