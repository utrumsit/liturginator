# Tone Calculation Comparison

## Your Implementation (tone.py) vs Orthocal's Implementation

### Your Current Logic:

```python
def get_tone(date):
    # Before Pascha: Tone 8 (simplified)
    if date < pascha:
        return 8
    
    # Pascha: Tone 1
    if days_since_pascha == 0:
        return 1
    
    # Bright Week (days 1-6): Tones 2,3,4,5,6,8 (omitting 7)
    elif 1 <= days_since_pascha <= 6:
        bright_tones = [2, 3, 4, 5, 6, 8]
        return bright_tones[days_since_pascha - 1]
    
    # Thomas Sunday (day 7): Tone 1
    elif days_since_pascha == 7:
        return 1
    
    # After Pentecost: cycle calculation
    else:
        days_after_pentecost = (date - pentecost).days
        number = days_after_pentecost // 7
        if number <= 2:
            tone = 1
        else:
            tone = ((number - 2) % 8) + 1
        return tone
```

### Orthocal's Logic (from day.py):

```python
@cached_property
def tone(self):
    """The proper tone for this day."""
    
    # Holy Week (days -8 to -1): No tone (octoechos not employed)
    if -9 < self.pdist < 0:
        return 0
    
    # Bright Week (days 0-6): Cycle through tones, skipping tone 7
    # Tone 7 is too somber for bright week
    if 0 <= self.pdist < 7:
        bright_tones = 1, 2, 3, 4, 5, 6, 8  # Note: starts with 1 for Pascha!
        return bright_tones[self.pdist]
    
    # TODO: check for great feasts and set tone to 0
    
    # Regular cycle: Thomas Sunday (pdist=7) is 1st Sunday
    # Formula: ((nth_sunday - 1) % 8) + 1
    nth_sunday = self.preceding_pdist // 7
    return (nth_sunday - 1) % 8 + 1
```

## Key Differences:

### 1. **Bright Week Tones**
- **Your code**: Day 0 (Pascha) = Tone 1, Days 1-6 = [2,3,4,5,6,8]
- **Orthocal**: Days 0-6 = [1,2,3,4,5,6,8]
- **Issue**: Your bright_tones array is off by one!

### 2. **Holy Week Treatment**
- **Your code**: Returns Tone 8 for all pre-Pascha dates
- **Orthocal**: Returns 0 (no tone) for Holy Week (pdist -8 to -1)
- **Reality**: Holy Week DOES have tones, but they're special/unique per service
- **Issue**: Both implementations are incomplete! Holy Week has its own tone structure
  - Different tones for different services (Matins, Vespers, Hours)
  - Not part of the regular 8-tone octoechos cycle
  - Should return 0 to indicate "not in octoechos cycle" but actual tones still exist

### 3. **Cycle Calculation**
- **Your code**: Complex logic with Pentecost + special cases for first 2 weeks
- **Orthocal**: Simple pdist-based formula: `(nth_sunday - 1) % 8 + 1`
- **Better**: Orthocal's is cleaner and more correct

### 4. **Great Feasts**
- **Your code**: No special handling
- **Orthocal**: TODO comment to set tone to 0 for great feasts
- **Note**: Great feasts sometimes use tone 0 or special tones

## Recommended Fix:

Replace your `get_tone()` with orthocal's logic using pdist:

```python
def get_tone(date, pascha):
    """
    Calculate liturgical tone using pdist (days from Pascha).
    Based on orthocal-python implementation.
    """
    pdist = (date - pascha).days
    
    # Holy Week: octoechos not employed
    if -9 < pdist < 0:
        return 0
    
    # Bright Week: cycle through tones, skipping tone 7
    # Pascha = Tone 1, Mon = Tone 2, etc.
    if 0 <= pdist < 7:
        bright_tones = (1, 2, 3, 4, 5, 6, 8)
        return bright_tones[pdist]
    
    # TODO: Check for great feasts and return 0
    
    # Regular Sunday cycle starting with Thomas Sunday
    # Thomas Sunday (pdist 7) = 1st Sunday = Tone 1
    nth_sunday = pdist // 7
    return (nth_sunday - 1) % 8 + 1
```

## Testing:

Let's verify with some key dates for 2025 (Pascha = April 20):

| Date | Pdist | Your Code | Orthocal | Correct |
|------|-------|-----------|----------|---------|
| Apr 20 (Pascha) | 0 | 1 | 1 | ✓ |
| Apr 21 (Mon) | 1 | 2 | 2 | ✓ |
| Apr 27 (Thomas) | 7 | 1 | 1 | ✓ |
| May 4 (2nd Sun) | 14 | ? | 2 | ? |
| Nov 30 (25th Sun) | 224 | ? | ? | ? |

## Integration with Lectionary:

Since you already use pdist in `lectionary_pdist.py`, adding tone is trivial:

```python
def get_readings(self, date):
    # ... existing code ...
    
    # Add tone calculation
    tone = self._calculate_tone(pdist, date, key_dates)
    
    return {
        'title': title,
        'tone': tone,  # Add this
        'pdist': pdist,
        # ... rest of result ...
    }

def _calculate_tone(self, pdist, date, key_dates):
    """Calculate liturgical tone."""
    # Use orthocal's logic
    if -9 < pdist < 0:
        return 0
    
    if 0 <= pdist < 7:
        return (1, 2, 3, 4, 5, 6, 8)[pdist]
    
    # Check for great feasts (feast_level >= 7)
    # Return 0 if great feast
    
    nth_sunday = pdist // 7
    return (nth_sunday - 1) % 8 + 1
```

## Troparia Selection:

Once you have the tone, you can select the proper troparia:

```python
def get_troparia(date, tone, feast_level, feast_name):
    """Get troparia for matins."""
    troparia = []
    
    # Priority 1: Great feast (level >= 7)
    if feast_level >= 7:
        troparia.append(get_feast_troparion(feast_name))
        return troparia
    
    # Priority 2: Sunday resurrection troparion
    weekday = date.weekday()
    if weekday == 6:  # Sunday
        troparia.append(get_resurrection_troparion(tone))
    
    # Priority 3: Saint troparion (level 4-6)
    if 4 <= feast_level < 7:
        troparia.append(get_saint_troparion(feast_name))
    
    # Always add theotokion in same tone
    troparia.append(get_theotokion(tone))
    
    return troparia
```

## Sources:

- Your implementation: `tone.py`
- Orthocal implementation: `orthocal/calendarium/liturgics/day.py` lines 202-225
- Algorithm reference: https://mci.archpitt.org/liturgy/EightTones.html (cited in orthocal code)
