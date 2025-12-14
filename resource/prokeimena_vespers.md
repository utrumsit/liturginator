# Prokeimena at Vespers

## Sources

- **Časoslov (Book of Hours)**, Ruthenian recension, pages 259-261
- **MCI Daily Vespers** guidelines
- **orthocal.info** liturgics implementation (feast_levels.json)

## Usage Rules

1. **Ordinary Time** ("God is the Lord" period): Use the weekday prokeimenon below

2. **Great Lent** (Clean Monday through Lazarus Saturday): Use Alleluia verses
   - Exception: "On Sunday and Friday evenings, Alleluia is never sung" (Časoslov p.261)
   - Note: Saturday evening is liturgically Sunday, so it uses prokeimenon

3. **Minor Fasts** (Nativity Nov 15-Dec 24, Apostles, Dormition Aug 1-14):
   - If the day is marked as "Day of Alleluia" (feast_level = 0), use Alleluia
   - "On certain days in the minor fasts (which are indicated in the typikon), the alleluia is taken in place of the daily prokeimenon" (MCI Daily Vespers)
   - Sunday and Friday evenings still use prokeimenon

4. **Feast days** (feast_level >= 4): Always use prokeimenon

See `vespers_prokeimenon.py` for programmatic access to this logic.

---

## Ordinary Time (God the Lord period)

### Saturday Evening
*Tone 6, Psalm 92*

The Lord reigns, He is clothed in majesty!
*Verse:* Robed is the Lord and girt about with strength.
*Verse:* The world He made firm, not to be moved.
*Verse:* Holiness is fitting to Your house, O Lord, until the end of time.

### Sunday Evening
*Tone 8, Psalm 133*

Come, bless the Lord, all you who serve the Lord.
*Verse:* Who stand in the house of the Lord, in the courts of the house of our God.

### Monday Evening
*Tone 4, Psalm 4*

The Lord hears me whenever I call Him.
*Verse:* When I call, answer me, O God of Justice.

### Tuesday Evening
*Tone 1, Psalm 22*

My help shall come from the Lord, Who made heaven and earth.
*Verse:* I lift up my eyes to the mountains, from where shall come my help?

### Wednesday Evening
*Tone 5, Psalm 53*

O God, save me by Your Name, by Your power uphold my cause.
*Verse:* O God, hear my prayer; listen to the words of my mouth.

### Thursday Evening
*Tone 6, Psalm 120*

Your mercy, O Lord, shall follow me all the days of my life.
*Verse:* The Lord is my shepherd, there is nothing I shall want; fresh and green are the pastures where He gives me repose.

### Friday Evening
*Tone 7, Psalm 58*

You, O God, are my defender and Your mercy goes before me.
*Verse:* Rescue me, O God, from my foes; protect me from those who attack me.

---

## Great Lent (Alleluia period)

*Note: On Sunday and Friday evenings, Alleluia is never sung.*

### Monday Evening
*Tone 6, Psalm 6*

Alleluia, alleluia, alleluia.
*Verse:* O Lord, rebuke me not in Your anger, chastise me not in Your wrath. Alleluia!
*Verse:* Now and ever and forever. Alleluia!

### Tuesday Evening
*Psalm 98*

Alleluia, alleluia, alleluia.
*Verse:* Extol the Lord, our God, and worship at His footstool for He is holy. Alleluia!
*Verse:* Now and ever and forever. Alleluia!

### Wednesday Evening
*Psalm 18*

Alleluia, alleluia, alleluia.
*Verse:* Through all the earth their voice resounds; their message reaches to the ends of the world. Alleluia!
*Verse:* Now and ever and forever. Alleluia!

### Thursday Evening
*Psalm 98*

Alleluia, alleluia, alleluia.
*Verse:* Extol the Lord, our God, and worship at His footstool for He is holy. Alleluia!
*Verse:* Now and ever and forever. Alleluia!
