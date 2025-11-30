# Quick Start: Byzantine Lectionary with RSV Text

## Get Today's Readings

```bash
python get_readings.py
```

Output:
```
======================================================================
Saturday of the 25th week after Pentecost
======================================================================

EPISTLE
----------------------------------------------------------------------
Reference: Galatians 1.3-10

Grace to you and peace from God the Father and our Lord Jesus Christ,
who gave himself for our sins to deliver us from the present evil age,
according to the will of our God and Father; to whom be the glory for
ever and ever. Amen. I am astonished that you are so quickly deserting
him who called you in the grace of Christ and turning to a different
gospel...

GOSPEL
----------------------------------------------------------------------
Reference: Luke 10.19-21

Behold, I have given you authority to tread upon serpents and
scorpions, and over all the power of the enemy; and nothing shall hurt
you...

======================================================================
```

## Get Readings for Any Date

```bash
python get_readings.py 2025-12-25  # Nativity
python get_readings.py 2026-01-06  # Theophany
```

## Get JSON Output

```bash
python get_readings.py 2025-11-29 --json
```

## Python API

```python
from lectionary_pdist import LectionaryPdist
import datetime

# Initialize
lect = LectionaryPdist(rsv_xml_path='rsv.xml')

# Get readings
result = lect.get_readings(datetime.date(2025, 11, 29))

# Access data
print(result['title'])                   # "Saturday of the 25th week..."
print(result['epistle']['display'])      # "Galatians 1.3-10"
print(result['epistle']['rsv_text'])     # Full RSV text
print(result['gospel']['display'])       # "Luke 10.19-21"
print(result['gospel']['rsv_text'])      # Full RSV text
```

## What's Included

✅ Correct Lukan Jump implementation (from orthocal-python)  
✅ Fixed feast precedence (Nativity, Theophany, etc.)  
✅ Saint feast readings with daily cycle (St. Andrew, Prophet Elijah, etc.)  
✅ RSV Bible text extraction from rsv.xml  
✅ Complete lectionary schedule (412 paschal + 366 fixed feasts)  
✅ Human-readable and JSON output formats  

## How It Works

1. **Pascha Distance (pdist)**: Every day identified by days from Pascha
2. **Lukan Jump**: Gospel readings shift forward after Sept 14
3. **Feast Precedence**: 
   - Major feasts (Level 6-8): Only feast readings shown
   - Saint feasts (Level 2-5): Both daily AND saint readings shown
   - Minor commemorations: Only daily readings shown
4. **RSV Integration**: Extracts actual verse text from rsv.xml

## Credits

- Lectionary algorithm: orthocal-python by Brian Glass (MIT License)
- RSV text: Division of Christian Education, NCCC USA
- Integration: liturginator project

## More Info

- Full documentation: `RSV_INTEGRATION.md`
- Algorithm details: `ORTHOCAL_ALGORITHM.md`
- Attribution: `ORTHOCAL_ATTRIBUTION.md`
