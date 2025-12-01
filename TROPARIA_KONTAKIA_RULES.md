# Troparia and Kontakia Rules for Matins
## Byzantine Catholic / Orthodox Usage

## Summary from Chasoslov.md

### 1. After "The Lord is God" (or Alleluia during Lent)

**Pattern:**
- First troparion: said **TWICE**
- Second troparion (if any): said **ONCE**
- Theotokion: said **ONCE** (in same tone as troparia)

**Source:** Chasoslov p. 107 (lines 3741-3744)
> "Then we say the appointed troparion twice and the theotokion in the same tone. 
> If two troparia are appointed, the first is always said twice, then the second 
> and the theotokion are said."

**During Lent/Alleluia Period:**
- Instead of "The Lord is God", sing Alleluia 3x in tone of octoechos
- Then Trinitarian Hymns of the tone (each once)
- Different endings for different days of week

### 2. During the Hours (Third Hour, Sixth Hour, Ninth Hour)

**At Glory:**
- Troparion of the day, OR
- Troparion of the feast, OR  
- Troparion of the saint

**After "For Thine is the kingdom":**
- Kontakion of the day, OR
- Kontakion of the saint, OR
- Kontakion of the feast

**Source:** Chasoslov p. 199 (lines 7361, 7429)

**During Fast:**
- If no kontakion, use specified troparia (Tone 8)

### 3. After the Great Doxology (end of Matins)

**Priority:**
1. **If Feast of Master or Theotokos:** troparion of the feast
2. **If Sunday:** resurrection troparion (variant depends on tone)
   - Tones 1, 3, 5, 7: "Today salvation has come to the world..."
   - Tones 2, 4, 6, 8: "Rising from the tomb and breaking the bonds..."

**Source:** Chasoslov p. 162 (lines 6049-6074)

## Questions Needing Research

### 1. Precedence Rules
- **When do you use BOTH saint troparion AND daily troparion?**
- How do feast levels affect which troparia are used?
- What about multiple saints on same day?

### 2. Polyeleos / Gospel Sequence
- Troparia/kontakia after Gospel reading?
- After Polyeleos (festive Matins)?
- Sessional hymns vs troparia?

### 3. Tone Determination
- How is the tone determined for troparia?
- Does it follow octoechos cycle?
- How do feast troparia interact with weekly tone?

### 4. Combining Multiple Commemorations
- Saint feast + Sunday: which comes first?
- Saint feast + fixed feast: precedence?
- Multiple saints: order and repetition?

### 5. Kathismata and Sessional Hymns
- Relationship to troparia?
- When are they used?

## Data Needed for Coding

To implement this systematically, we need:

1. **Troparion database** with:
   - Text
   - Tone
   - Type (resurrection, feast, saint, daily)
   - Feast level / priority

2. **Kontakion database** with similar structure

3. **Precedence rules matrix:**
   ```
   Priority | Type              | When Used
   ---------|-------------------|------------------
   1        | Great Feast       | Level 8 feasts
   2        | Theotokos Feast   | Level 6-7
   3        | Resurrection      | Sundays (if no feast)
   4        | Saint (major)     | Level 4-5
   5        | Daily/Weekday     | Default
   ```

4. **Combination rules:**
   - Which get said twice
   - Order of multiple troparia
   - When theotokion is added

## Sources to Research

### Primary Sources Needed:
1. **Typikon** - The liturgical rule book
2. **Horologion** - Book of Hours (fuller version)
3. **Oktoechos** - Eight-tone cycle book
4. **Menaion** - Monthly saint commemorations

### Online Resources to Check:
1. Orthodox Church in America (OCA) liturgical guides
2. Antiochian Archdiocese liturgical resources
3. Byzantine Catholic resources
4. Monastic typikon explanations

### Specific Questions for Sources:
- What determines "appointed" troparion of the day?
- Rules for commemorating multiple saints
- Interaction between movable (Pascha cycle) and fixed (Menologion) cycles
- Weekday vs Sunday vs Feast day variations

## Implementation Plan

Once rules are clarified:

1. Create troparion/kontakion database (JSON)
2. Build precedence logic function
3. Integrate with existing lectionary system
4. Add tone determination logic
5. Output formatter for Matins structure

## Notes

- Your existing `menaion_data.json` has troparia and kontakia for ~351 feasts
- Need to extract/organize resurrection troparia by tone
- Need daily (weekday) troparia for each day of the week
- Theotokia organized by tone (you have `theotokia.json`)
