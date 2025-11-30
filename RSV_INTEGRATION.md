# RSV Text Integration with Byzantine Lectionary

## Overview

This system combines the liturgical calendar schedule from orthocal-python (MIT license, by Brian Glass) with RSV Bible text extraction to provide complete daily scripture readings for the Byzantine Catholic lectionary.

## Components

### 1. RSV Extractor (`rsv_extractor.py`)
- Parses `rsv.xml` (OSIS format) into memory
- Extracts verse text based on pericope references
- Handles various book name formats and verse ranges
- Examples:
  - `"Luke 10.19-21"` → extracts Luke chapter 10, verses 19-21
  - `"Galatians 1.3-10"` → extracts Galatians chapter 1, verses 3-10
  - Supports single verses, ranges, and comma-separated lists

### 2. Lectionary with Pdist (`lectionary_pdist.py`)
- Uses orthocal's pascha-distance (pdist) algorithm
- Correctly implements the Lukan Jump for Gospel readings
- Handles feast day precedence (major feasts override daily cycle)
- Optionally integrates RSV text extraction

### 3. User Interface (`get_readings.py`)
- Simple command-line interface
- Formats readings in human-readable format
- Usage:
  ```bash
  python get_readings.py              # Today's readings
  python get_readings.py 2025-12-25   # Specific date
  python get_readings.py --json       # JSON output
  ```

## How It Works

### The Pdist System
1. **Pascha Distance**: Every day is identified by its distance from Pascha (Easter)
   - Example: Pentecost is pdist 49 (49 days after Pascha)
   - November 29, 2025 is pdist 223 (223 days after Pascha 2025)

2. **Lukan Jump**: After the Exaltation of the Cross (Sept 14):
   - Gospel readings "jump" forward in the cycle
   - This allows the cycle to synchronize properly by Theophany (Jan 6)
   - Formula: `gospel_pdist = actual_pdist + lukan_jump`
   - For 2025: jump is 14 days

3. **Fixed Feasts and Saints**: The system handles feast precedence by level:
   - **Level 6-8**: Major feasts (Nativity, Theophany, etc.) - Only feast readings shown
   - **Level 2-5**: Saint feasts - BOTH daily cycle AND saint readings shown
   - **Level 0-1**: Minor commemorations - Only daily cycle shown
   - Examples: 
     - Nativity (Level 8): Only Nativity readings
     - St. Andrew (Level 4): Both Sunday readings AND Apostle readings
     - Prophet Elijah (Level 5): Both daily cycle AND Prophet readings

### Example: November 29, 2025
```
Actual pdist: 223
Gospel pdist: 223 + 14 = 237 (applies Lukan Jump)
Epistle pdist: 223 (no jump)

Readings:
- Epistle: Galatians 1.3-10 (pdist 223)
- Gospel: Luke 10.19-21 (pdist 237)
```

### Example: Nativity (December 25, 2025)
```
Fixed feast with feast_level = 8
Uses fixed readings only (overrides paschal cycle):
- Epistle: Galatians 4.4-7 (Nativity reading)
- Gospel: Matthew 2.1-12 (Nativity reading)
```

### Example: St. Andrew (November 30, 2025)
```
Saint feast with feast_level = 4
Shows BOTH daily cycle and saint readings:

Daily Cycle:
- Epistle: Ephesians 4.1-6 (Sunday cycle)
- Gospel: Luke 13.10-17 (Sunday cycle)

Saint Readings:
- Epistle: 1 Corinthians 4.9-16 (Apostle reading)
- Gospel: John 1.35-51 (Apostle reading)
```

## Data Sources

### Lectionary Schedule
**Source**: orthocal-python by Brian Glass
- Repository: https://github.com/brianglass/orthocal-python
- License: MIT License, Copyright 2022 Brian Glass
- File: `orthocal_complete_lectionary.json` (extracted from orthocal)
- Contains: 412 paschal cycle readings + 366 fixed feast readings

### Bible Text
**Source**: RSV (Revised Standard Version)
- File: `rsv.xml` (OSIS format)
- Copyright: Division of Christian Education of the National Council of Churches of Christ in the USA, 1946, 1952, 1973
- Format: OSIS XML with standard book IDs (e.g., `Matt.1.1`, `Luke.10.19`)

## Files Created

1. **rsv_extractor.py** - RSV text extraction module
2. **lectionary_pdist.py** (updated) - Now supports RSV integration
3. **get_readings.py** - User-friendly CLI interface
4. **orthocal_complete_lectionary.json** - Complete reading schedule from orthocal
5. **ORTHOCAL_ALGORITHM.md** - Documentation of the pdist algorithm
6. **ORTHOCAL_ATTRIBUTION.md** - Attribution and licensing

## Usage Examples

### Command Line

Get today's readings:
```bash
python get_readings.py
```

Get readings for a specific date:
```bash
python get_readings.py 2025-12-25
```

Get JSON output:
```bash
python get_readings.py 2025-11-29 --json
```

### Python API

```python
from lectionary_pdist import LectionaryPdist
import datetime

# Initialize with RSV text extraction
lect = LectionaryPdist(rsv_xml_path='rsv.xml')

# Get readings for a date
date = datetime.date(2025, 11, 29)
result = lect.get_readings(date)

# Access the data
print(result['title'])
print(result['epistle']['display'])      # Reference: "Galatians 1.3-10"
print(result['epistle']['rsv_text'])     # Full RSV text
print(result['gospel']['display'])       # Reference: "Luke 10.19-21"
print(result['gospel']['rsv_text'])      # Full RSV text
```

## Testing

Verify the system works correctly:

```bash
# Test Lukan Jump (should return Luke 10.19-21)
python get_readings.py 2025-11-29

# Test saint feast with both readings (St. Andrew)
python get_readings.py 2025-11-30

# Test major feast (should return Nativity readings only)
python get_readings.py 2025-12-25

# Test regular day
python get_readings.py 2025-06-15

# Test another saint feast (Prophet Elijah)
python get_readings.py 2025-07-20
```

## Next Steps

Potential enhancements:
1. Add Old Testament readings (prophets, wisdom literature)
2. Integrate with matins/vespers service generation
3. Add prokeimenon, alleluia verses, and communion verses
4. Support for multiple reading sets (vigils, liturgy, etc.)
5. Add saints' feast day hymns (troparia, kontakia)
6. Generate complete daily office (Hours, Vespers, Matins)

## Credits

- **Lectionary Schedule**: Brian Glass (orthocal-python, MIT License)
- **RSV Bible Text**: Division of Christian Education, NCCC USA
- **Integration**: Karl Schudt, liturginator project
- **Algorithm Documentation**: Based on analysis of orthocal-python source code
