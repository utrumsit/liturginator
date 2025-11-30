# Orthocal Gospel Reading Algorithm

This document describes the complete algorithm used by orthocal.info for determining Gospel readings, including the Lukan Jump.

**Source**: https://github.com/brianglass/orthocal-python  
**Credit**: All logic below is from the orthocal-python project by Brian Glass

## Core Concept: Pascha Distance (pdist)

Everything is keyed by **pdist** - the number of days from Pascha:
- pdist = 0: Pascha Sunday
- pdist = 49: Pentecost Sunday  
- pdist = 50: Pentecost Monday (start of Post-Pentecost cycle)
- Negative pdist: days before Pascha (Triodion/Lent)

## Epistle vs Gospel Handling

**EPISTLES**: Always use actual pdist (with minor end-of-year wraparound)

**GOSPELS**: Complex adjustments for:
1. The Lukan Jump (after Exaltation of the Cross)
2. Christmas/Theophany season pause
3. Reserve Sundays after Theophany
4. End-of-year wraparound

## The gospel_pdist Algorithm

```python
def gospel_pdist(pdist, pyear):
    """
    Calculate the adjusted pdist for looking up Gospel readings.
    
    Args:
        pdist: Actual pascha distance for the date
        pyear: Year object with calculated values
    
    Returns:
        Adjusted pdist for Gospel lookup, or None if no daily reading
    """
    
    # Step 1: Check if daily readings are suppressed
    if not has_daily_readings(pdist, pyear):
        return None
    
    # Step 2: Special case - 11th Sunday of Luke = Forefathers Sunday
    # On this day, we read the Forefathers gospel (with lukan jump applied)
    if pdist == pyear.first_sun_luke + 10*7:
        return pyear.forefathers + pyear.lukan_jump
    
    # Step 3: Sundays after Theophany use "reserve" gospels
    # These are gospels that were skipped due to Nativity/Theophany feasts
    # or skipped over in the Lukan Jump
    if (weekday == Sunday and 
        pdist > pyear.sun_after_theophany and 
        pyear.extra_sundays > 1):
        i = (pdist - pyear.sun_after_theophany) // 7
        return pyear.reserves[i-1]
    
    # Step 4: After Saturday before Theophany - jump to next year's cycle
    # This is where the Luke cycle "ends" and we start from the beginning
    if pdist > pyear.sat_before_theophany:
        return jdn - pyear.next_pascha  # Negative pdist in next year
    
    # Step 5: After Sunday after Exaltation - apply the Lukan Jump
    # This synchronizes the Gospel cycle to the solar calendar
    if pdist > pyear.sun_after_elevation:
        return pdist + pyear.lukan_jump
    
    # Step 6: Default - no adjustment
    return pdist
```

## The Lukan Jump Calculation

```python
def calculate_lukan_jump(sun_after_elevation):
    """
    The Lukan Jump synchronizes the Gospel cycle to the solar calendar.
    
    Goal: The Gospel for the "18th Monday after Pentecost" (Luke 3:19-22)
          must be read on the Monday after the Sunday after Exaltation.
    
    The jump amount is how many days we need to skip forward.
    """
    # Target: Where the 18th Monday "should" be in the paschal cycle
    eighteenth_monday = 50 + 7*17  # Pentecost Monday + 17 weeks = pdist 169
    
    # Actual: Where we actually are in the solar calendar
    mon_after_elevation = sun_after_elevation + 1
    
    # Jump forward by this many days
    return eighteenth_monday - mon_after_elevation
```

**Key Insight**: The jump amount varies each year depending on when Pascha falls!
- Early Pascha → smaller jump (Exaltation is later in paschal cycle)
- Late Pascha → larger jump (Exaltation is earlier in paschal cycle)

## Key Dates Calculation

```python
def calculate_key_dates(year):
    """Calculate the key dates for a liturgical year."""
    
    pascha = calculate_pascha(year)
    
    # Exaltation of the Cross (September 14 - fixed solar date)
    exaltation = date(year, 9, 14)
    exaltation_pdist = (exaltation - pascha).days
    
    # Sunday after Exaltation
    weekday = exaltation_pdist % 7  # 0=Sunday in orthocal's system
    sun_after_elevation = exaltation_pdist + 7 - weekday
    
    # Saturday before Theophany (January 6)
    theophany = date(year + 1, 1, 6)
    theophany_pdist = (theophany - pascha).days
    weekday_theo = theophany_pdist % 7
    sat_before_theophany = theophany_pdist - (weekday_theo + 1) % 7 - 1
    sun_after_theophany = theophany_pdist + 7 - weekday_theo
    
    # Nativity (December 25)
    nativity = date(year, 12, 25)
    nativity_pdist = (nativity - pascha).days
    
    # Forefathers Sunday (2 weeks before Nativity, adjusted to Sunday)
    weekday_nat = nativity_pdist % 7
    forefathers = nativity_pdist - 14 + ((7 - weekday_nat) % 7)
    
    # First Sunday of Luke (Sunday after Exaltation + 1 week)
    first_sun_luke = sun_after_elevation + 7
    
    # Lukan Jump amount
    lukan_jump = (50 + 7*17) - (sun_after_elevation + 1)
    
    return {
        'sun_after_elevation': sun_after_elevation,
        'sat_before_theophany': sat_before_theophany,
        'sun_after_theophany': sun_after_theophany,
        'forefathers': forefathers,
        'first_sun_luke': first_sun_luke,
        'lukan_jump': lukan_jump,
        'nativity': nativity_pdist,
        'theophany': theophany_pdist,
    }
```

## Reserve Sundays

When Nativity/Theophany feasts occur, some Sunday gospels are skipped. These are saved as "reserves" and used on Sundays after Theophany (before the Triodion begins).

```python
def calculate_reserves(pyear):
    """
    Calculate which Sunday gospels were skipped and should be read after Theophany.
    """
    reserves = []
    
    first_luke = 49 + 7*18  # 18th Sunday after Pentecost
    thirteenth_luke = first_luke + 7*13
    
    # Calculate how many "extra" Sundays there are between 
    # Sunday after Theophany and the start of the Triodion
    next_pascha = calculate_pascha(pyear.year + 1)
    sun_before_zaccheus = (next_pascha - pyear.pascha) - 12*7
    extra_sundays = (sun_before_zaccheus - pyear.sun_after_theophany) // 7
    
    if extra_sundays:
        # These are Sundays skipped between Forefathers and Theophany
        # due to Nativity/Theophany feasts
        forefathers_adjusted = pyear.forefathers + pyear.lukan_jump + 7
        reserves.extend(range(forefathers_adjusted, thirteenth_luke + 1, 7))
        
        # If we still need more reserves, use Sundays that were 
        # jumped over in the Lukan Jump
        if remainder := extra_sundays - len(reserves):
            start = first_luke - remainder * 7
            end = first_luke - 6
            reserves.extend(range(start, end, 7))
    
    return reserves
```

## Example: November 29, 2025

```
Pascha 2025: April 20
Nov 29, 2025: pdist = 223 (Saturday)

Key dates:
- sun_after_elevation = 154
- lukan_jump = 14 days

Gospel lookup:
1. pdist (223) > sun_after_elevation (154)? YES
2. Apply lukan jump: 223 + 14 = 237
3. Look up Gospel for pdist 237 → Luke 10:19-21 ✓

Epistle lookup:
1. Use actual pdist = 223
2. Look up Epistle for pdist 223 → Galatians 1:3-10 ✓
```

## Daily Readings Suppression

Some days have their daily readings suppressed due to major feasts:

```python
no_daily = {
    sun_before_theophany, sun_after_theophany, 
    theophany - 5, theophany - 1, theophany,
    forefathers,
    sun_before_nativity, nativity - 1, nativity,
    nativity + 1, sun_after_nativity,
    # Plus conditional additions based on day of week
}
```

## Summary

The orthocal algorithm handles:

1. **Lukan Jump**: Synchronizes Gospel cycle to solar calendar after Exaltation
2. **Christmas/Theophany Pause**: Gospel cycle jumps to next year after sat_before_theophany
3. **Reserve Sundays**: Skipped gospels are recycled after Theophany
4. **Special Days**: Forefathers, floating feasts, etc. have custom handling
5. **End of Year Wraparound**: Both Epistles and Gospels wrap to next year's cycle

**Key Principle**: Epistles follow the lunar (paschal) calendar continuously, while Gospels are adjusted to synchronize key readings with the solar (fixed) calendar.
