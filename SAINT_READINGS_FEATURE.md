# Saint Readings Feature

## Overview

The lectionary system now provides BOTH daily cycle readings AND saint feast readings when appropriate, matching the behavior of orthocal.info.

## How It Works

### Feast Level Precedence

The system uses feast levels (0-8) to determine which readings to display:

| Feast Level | Type | Behavior | Examples |
|------------|------|----------|----------|
| 0-1 | Minor commemoration | Daily cycle only | Most commemorations |
| 2-3 | Lesser saint feast | Both daily + saint | Various saints |
| 4-5 | Major saint feast | Both daily + saint | St. Andrew, Prophet Elijah |
| 6-7 | Great feast | Feast readings only | Exaltation of the Cross |
| 8 | Highest feast | Feast readings only | Nativity, Theophany, Pascha |

### Output Format

#### Regular Day (No Feast)
```
======================================================================
Saturday of the 25th week after Pentecost
======================================================================

EPISTLE
Reference: Galatians 1.3-10
[RSV text...]

GOSPEL
Reference: Luke 10.19-21
[RSV text...]
```

#### Saint Feast Day (Level 2-5)
```
======================================================================
Sunday of the 25th week after Pentecost
Feast: Holy Apostle Andrew the First Called (Level 4)
======================================================================

DAILY CYCLE READINGS
======================================================================

EPISTLE
Reference: Ephesians 4.1-6
[RSV text for Sunday...]

GOSPEL
Reference: Luke 13.10-17
[RSV text for Sunday...]

=
SAINT READINGS: Holy Apostle Andrew the First Called
======================================================================

EPISTLE
Reference: 1 Corinthians 4.9-16
[RSV text for Apostle...]

GOSPEL
Reference: John 1.35-51
[RSV text for Apostle...]
```

#### Major Feast (Level 6-8)
```
======================================================================
Thursday of the 29th week after Pentecost
Feast: Nativity of Christ (Level 8)
======================================================================

EPISTLE
Reference: Galatians 4.4-7
[RSV text for Nativity...]

GOSPEL
Reference: Matthew 2.1-12
[RSV text for Nativity...]
```

## API Response Structure

### With Saint Readings (Level 2-5)
```python
{
    'title': 'Sunday of the 25th week after Pentecost',
    'feast_name': 'Holy Apostle Andrew the First Called',
    'feast_level': 4,
    'pdist': 224,
    
    # Primary readings (for backward compatibility - points to daily cycle)
    'epistle': {...},
    'gospel': {...},
    
    # Daily cycle readings
    'daily_epistle': {
        'display': 'Ephesians 4.1-6',
        'rsv_text': '...'
    },
    'daily_gospel': {
        'display': 'Luke 13.10-17',
        'rsv_text': '...'
    },
    
    # Saint readings
    'saint_epistle': {
        'display': '1 Corinthians 4.9-16',
        'rsv_text': '...'
    },
    'saint_gospel': {
        'display': 'John 1.35-51',
        'rsv_text': '...'
    }
}
```

### Major Feast (Level 6-8)
```python
{
    'title': 'Thursday of the 29th week after Pentecost',
    'feast_name': 'Nativity of Christ',
    'feast_level': 8,
    'pdist': 249,
    
    # Only feast readings
    'epistle': {
        'display': 'Galatians 4.4-7',
        'rsv_text': '...'
    },
    'gospel': {
        'display': 'Matthew 2.1-12',
        'rsv_text': '...'
    }
    # No daily_epistle/gospel or saint_epistle/gospel fields
}
```

## Testing Examples

```bash
# Saint feast with both readings (Level 4)
python get_readings.py 2025-11-30  # St. Andrew

# Saint feast with both readings (Level 5)
python get_readings.py 2025-07-20  # Prophet Elijah

# Major feast with only feast readings (Level 8)
python get_readings.py 2025-12-25  # Nativity

# Regular day with only daily cycle
python get_readings.py 2025-11-29  # Regular Saturday
```

## Implementation Details

### In `lectionary_pdist.py`

1. **Always fetch daily cycle readings** from paschal cycle
2. **Check for fixed feast** by date (MM-DD)
3. **Fetch saint readings** if feast exists
4. **Apply feast level logic**:
   - Level ≥ 6: Return only feast readings
   - Level 2-5: Return both daily + saint
   - Level < 2: Return only daily
5. **Add RSV text** to all reading sets

### In `get_readings.py`

1. **Detect if both sets exist** (`saint_epistle` or `saint_gospel` present)
2. **Format accordingly**:
   - If both: Show "DAILY CYCLE READINGS" section, then "SAINT READINGS" section
   - If only one set: Show single readings section
3. **Include feast information** in header when present

## Liturgical Usage

This matches Orthodox liturgical practice:

- **On major feasts**: Only the feast readings are proclaimed
- **On saint feast days**: Often both the daily cycle AND the saint's readings are available:
  - Parish may use saint readings at Divine Liturgy
  - Daily cycle readings may be used at other services (Matins, Vespers)
  - Or both may be proclaimed at Liturgy
- **On regular days**: Only the daily cycle

## Data Source

All feast levels and saint readings come from orthocal-python:
- Repository: https://github.com/brianglass/orthocal-python
- License: MIT License, Copyright 2022 Brian Glass
- File: `orthocal_complete_lectionary.json`

RSV text extracted from `rsv.xml` (RSV 1952).
