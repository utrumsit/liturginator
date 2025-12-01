# Alleluia Period Rules - Byzantine Liturgy

## Summary

In the Byzantine tradition, the phrase "period of Alleluia" (or "days when Alleluia is said") refers to a specific liturgical state where **Alleluia** is sung at the beginning of Matins instead of **"God is the Lord"** (Бог Господь).

## When Alleluia is Sung

Alleluia is sung at Matins on **ordinary weekdays** during the following period:

**From:** Monday after Pentecost  
**Until:** Saturday before Meatfare Sunday (start of Triodion)

### Specific Conditions (ALL must be true):

1. **Weekday only** - Not Sunday
2. **Outside Lent** - Not during Great Lent or Holy Week (pdist -49 to -1)
3. **Outside Paschal season** - Not during Bright Week through Pentecost (pdist 0 to 49)
4. **No major feast** - Not a polyeleos-rank feast or higher (feast_level < 4)

## When "God is the Lord" is Sung Instead

- **All Sundays** (always use "God is the Lord")
- **Polyeleos feasts and higher** (feast_level ≥ 4)
- **During Paschal season** (Bright Week through Pentecost)
- **Major fixed feasts** (Twelve Great Feasts, etc.)

## Special Cases

### Bright Week (Pascha through Bright Saturday)
- Sing **"Christ is risen from the dead"** instead of either Alleluia or "God is the Lord"
- This is the Paschal troparion itself

### Great Lent and Holy Week
- Sing **Alleluia** but in a **somber, Lenten tone** (different from the joyful post-Pentecost Alleluia)
- This is technically "Alleluia" but liturgically distinct from "period of Alleluia"
- Often called "Trinitarian Hymns" on weekdays

## Implementation

The `alleluia_period.py` module provides:

### `is_alleluia_day(date_obj=None, pdist=None, weekday=None, feast_level=0)`
Returns `True` if Alleluia should be sung (joyful ordinary-time Alleluia)

### `get_matins_opening(date_obj=None, pdist=None, weekday=None, feast_level=0)`
Returns one of:
- `"alleluia"` - Ordinary-time Alleluia with verses
- `"god_is_lord"` - "God is the Lord" with troparion
- `"christ_is_risen"` - Bright Week Paschal troparion
- `"lenten_alleluia"` - Somber Lenten Alleluia

## Liturgical Structure During Alleluia Period

On days when Alleluia is sung:

1. **After Six Psalms**: Sing Alleluia (3×) with psalm verses in the tone of the week
2. **Troparia at the Praises**: 
   - Troparion of the day's commemoration (saint/daily theme)
   - Theotokion of the current tone (or Stavrotheotokion on Wed/Fri)
3. **Great Doxology**: Use shorter "Small Doxology" on ordinary weekdays

## Feast Level Reference (from orthocal)

| Level | Description | "God is the Lord"? |
|-------|-------------|-------------------|
| -1 | No Liturgy | N/A |
| 0 | Ordinary weekday | Alleluia |
| 1 | Presanctified | Alleluia |
| 2 | 6-stich (minor) | Alleluia |
| 3 | Doxology rank | Alleluia |
| 4 | Polyeleos rank | **God is the Lord** |
| 5 | Vigil rank | **God is the Lord** |
| 6 | Great Feast | **God is the Lord** |
| 7 | Major Theotokos Feast | **God is the Lord** |
| 8 | Major Lord's Feast | **God is the Lord** |

## Sources

- **Časoslov (Book of Hours)**, Ruthenian recension, 1950 Rome edition
- **orthocal** liturgics implementation (feast/fast levels, pdist calculations)
- **MCI (Metropolitan Cantor Institute)** - mci.archpitt.org
- **Grok's summary** of Byzantine liturgical tradition

## Related Files

- `alleluia_period.py` - Implementation
- `tone.py` - Tone calculation for Alleluia verses
- `menaion_data.json` - Feast levels for daily commemorations
- `chasoslov.md` - Full Book of Hours with rubrics
