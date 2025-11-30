# Orthocal Attribution and Integration

## What We're Using from Orthocal

This project uses the **lectionary algorithm and reading schedule** from [orthocal-python](https://github.com/brianglass/orthocal-python) by Brian Glass.

**HUGE thanks to Brian Glass** for creating orthocal.info and making the code open source! 🙏

### What We Borrowed:

1. **The Lukan Jump Algorithm** - Complete logic for how Gospel readings adjust after the Exaltation of the Cross
2. **Pascha Distance (pdist) System** - The elegant approach of keying everything to days from Pascha
3. **Reading Schedule** - Which pericopes (scripture references) to read on which days
4. **Fixed Feast Data** - Saints days, feast levels, and their readings
5. **Floating Feast Logic** - How Forefathers, Theophany weekends, etc. are calculated

### What We're NOT Using:

- **Scripture Text** - We use RSV instead of KJV
- **Prayer Texts** - We use Byzantine Catholic Book of Hours translations
- **Psalter** - We use Grail Psalter instead of their psalter
- **Saints Lives** - We may use our own commemorations

## Files Extracted from Orthocal

### `orthocal_complete_lectionary.json`
Complete reading schedule including:
- **paschal_cycle**: 380 pdist values with Epistle/Gospel assignments
- **fixed_feasts**: 178 fixed calendar dates with feast info and readings

Structure:
```json
{
  "paschal_cycle": {
    "223": {
      "epistle": {
        "display": "Galatians 1.3-10",
        "book": "Apostol",
        "pericope": "199"
      },
      "gospel": {
        "display": "Luke 9.37-43", 
        "book": "Luke",
        "pericope": "45"
      }
    }
  },
  "fixed_feasts": {
    "12-25": {
      "title": "Nativity of Christ",
      "feast_level": 8,
      "readings": [...]
    }
  }
}
```

### `ORTHOCAL_ALGORITHM.md`
Complete documentation of the pdist-based algorithm including:
- How pdist (Pascha distance) works
- Lukan Jump calculation and application
- Christmas/Theophany season handling
- Reserve Sundays logic
- End-of-year wraparound

### `lectionary_pdist.py`
Python implementation of the orthocal algorithm that:
- Calculates pdist for any date
- Applies Lukan Jump to Gospel readings
- Handles key liturgical dates
- Returns pericope references

## License Considerations

**Orthocal License**: Check https://github.com/brianglass/orthocal-python for their license

**Our Approach**:
- We use their **algorithm and schedule** (the "when" and "which")
- We provide our **own text sources** (the "what")
- This is a personal tool for Byzantine Catholic liturgy
- NOT intended for public distribution without:
  - Permission from orthocal project
  - Grail Psalter licensing
  - Byzantine Catholic Book of Hours permissions

## Integration Strategy

### Phase 1: Reading Schedule ✓
- Use orthocal's pdist algorithm
- Look up readings by pdist/date
- Map to our RSV text

### Phase 2: Complete Services
- Matins assembly using orthocal schedule + our texts
- Vespers assembly
- Hours assembly
- Kathismata from Grail Psalter

### Phase 3: Hymns and Feasts
- Saints troparia from our menaion data
- Resurrection troparia by tone
- Theotokia by tone
- Feast-specific hymns

## How to Give Back

If you use this project or orthocal's data:

1. **Star the orthocal repos**:
   - https://github.com/brianglass/orthocal-python
   - https://github.com/brianglass/orthocal

2. **Buy Brian a coffee/beer/pierogi** if you can!

3. **Contribute back**: If you find bugs in the algorithm or have improvements, submit PRs to orthocal

4. **Attribution**: Always credit orthocal.info when using their schedule/algorithm

## References

- **Orthocal.info**: https://orthocal.info
- **GitHub**: https://github.com/brianglass/orthocal-python
- **Lukan Jump Explanation**: https://www.orthodox.net/ustav/lukan-jump.html
- **Byzantine Lectionary**: Documentation of how the readings work

## Technical Notes

### Weekday Convention
Orthocal uses: `0=Sunday, 1=Monday, ..., 6=Saturday`  
Python uses: `0=Monday, ..., 6=Sunday`

We use orthocal's convention internally via `pdist % 7`.

### Fixed Feasts
Stored with `pdist=999` in orthocal's database.  
We extracted them to `fixed_feasts` keyed by "MM-DD".

### Precedence Rules
- Feast level ≥ 2: Include feast-specific readings
- Feast level ≥ 7: Major feasts that override daily cycle
- During Lent: Complex rules for when to use daily vs feast readings

### Key Dates Vary by Year
- Lukan Jump amount changes based on when Pascha falls
- All calculations use liturgical year (Pascha to Pascha)
- Dates before current year's Pascha use previous year's cycle
