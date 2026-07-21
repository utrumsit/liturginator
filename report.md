# Liturginator - Current State Report
*Generated: 2026-05-02*

## Project Purpose
Automate generation of liturgical texts for Byzantine Catholic Church services (Matins, Vespers, Hours, Divine Liturgy). Uses date logic borrowed from orthocal.info library.

---

## Two Codebase Branches

The project has TWO different implementations:

### 1. Django App (older, seems abandoned?)
- **Location**: Root level Python files
- **Key files**: `day.py`, `year.py`, `datetools.py`
- **Imports**: `asgiref.sync`, `django.db.models`, `django.utils.functional`
- **Status**: Seems outdated/inactive

### 2. Standalone CLI (current focus)
- **Location**: `liturginator.py`, `vespers_logic.py`, etc.
- **Key files**: `liturginator.py` (Click CLI), `vespers_logic.py` (VespersAssembler class)
- **Dependencies**: Click, python-dateutil, rich
- **Status**: Active development

---

## What's Been Done

### Date Logic ✅
- `datetools.py`: Computes Pascha (Easter), pdist (paschal distance), feast levels
- `pascha.py`: Orthodox Easter calculation, Lent detection
- `tone.py`: Determines liturgical tone based on week after Pentecost

### Service Logic (Standalone) ✅
- `vespers_logic.py`: `VespersAssembler` class - assembles full Vespers text
  - Blessing, Come Let Us Worship, Introductory Prayers
  - Psalm 103, Great Litany, Kathisma
  - Lamplighting Psalms with Stichera insertion
  - O Joyful Light, Prokeimenon, Readings, Troparion/Theotokion, Dismissal
- `matins_logic.py`: Matins assembly logic
- `hours_logic.py`: Hours assembly logic

### Data Files ✅
| File | Contents | Size |
|------|----------|------|
| `menaion_complete.json` | Saints, troparia, kontakia, stichera | 1.7MB |
| `octoechos_stichera.json` | Octoechos stichera by tone/day | 250KB |
| `orthocal_complete_lectionary.json` | Scripture readings (RSV) | 245KB |
| `rsv.xml` | Full RSV Bible | 5MB |
| `scripture_readings.json` | Formatted scripture texts | 134KB |

### Resource Files ✅
Located in `resource/`:
- `psalm103.md`, `great_litany.md`, `lamplighting_psalms.md`
- `o_joyful_light.md`, `introductory_prayers.md`
- `prokeimena_vespers.md`, `kathismata.md`

### Specialized Modules ✅
- `vespers_prokeimenon.py`: Prokeimenon logic (weekday vs Lenten Alleluia)
- `vespers_paramia.py`: Old Testament readings for Vespers
- `kathismata.py`: Kathisma (psalm section) scheduling logic

---

## Last Work: Vespers Assembly

### Git History (recent commits)
```
2749555 Update readings_2025-2035-final.json (RSV text, reserves logic)
5a7b80b Refactor: Port Reserves and Lukan jump logic to lectionary_pdist
676b498 Feat: Implement Kathisma logic in VespersAssembler  ← LAST VESPERS WORK
6c9604a Add Vespers assembler with Octoechos data extraction
```

### What VespersAssembler Does (`vespers_logic.py`)
1. Blessing: "Blessed is our God..."
2. Come, let us worship (3x)
3. Introductory prayers
4. Psalm 103
5. Great Litany
6. Kathisma (based on season: summer/winter/lent schedule)
7. Lamplighting Psalms with Stichera (Octoechos + Menaion)
8. O Joyful Light
9. Prokeimenon (weekday or Alleluia in Lent)
10. Readings (paramia for feast eves)
11. Troparion/Theotokion
12. Dismissal

### What's Implemented vs What's Stubs
| Component | Status | Source |
|-----------|--------|--------|
| Blessing | ✅ Hardcoded text | `vespers_logic.py` |
| Come Let Us Worship | ✅ Hardcoded text | `vespers_logic.py` |
| Introductory Prayers | ✅ File | `resource/introductory_prayers.md` |
| Psalm 103 | ✅ File | `resource/psalm103.md` |
| Great Litany | ✅ File | `resource/great_litany.md` |
| Kathisma | ✅ Logic implemented | `kathismata.py`, `vespers_logic.py:93-108` |
| Lamplighting Psalms | ✅ File with markers | `resource/lamplighting_psalms.md` |
| Stichera Insertion | ✅ Partial | `vespers_logic.py:110-159` |
| O Joyful Light | ✅ File | `resource/o_joyful_light.md` |
| Prokeimenon | ✅ Full logic | `vespers_prokeimenon.py` |
| Readings (Paramia) | ✅ Full logic | `vespers_paramia.py` |
| Troparion/Theotokion | ✅ Partial | Uses menaion data |
| Dismissal | ⚠️ Stub | "Dismissal for Vespers" |

---

## Stichera Logic

From `work-2024-12-07.md`:
- **6 stichera total** (typical feast day):
  - 3 from Octoechos (based on day of week + tone of week)
  - 3 from Menaion (for the saint)
- Insertion: Start at **On X:** marker matching count, work down
- **Glory** = Doxasticon from Menaion
- **Now and ever** = Theotokion from Octoechos (tone follows doxasticon, NOT weekly tone)

---

## Data Gaps (from assessment.md)

### Populate Scripts (20+ duplicate files)
Many one-off scripts like `populate_1st_week_pentecost.py` through `populate_pentecost_end.py`. Should consolidate into a single generator.

### Missing Data
- Lenten paramia not fully populated (only some days)
- Holy Week logic incomplete
- Hours (1st, 3rd, 6th, 9th) not implemented

### Dead Ends / Clean Up Needed
- `menaion_raw*.md/txt` files (raw data)
- `chunk_example*` files (test data)
- `.sync-conflict-*.DS_Store` files
- Old plan files (`PLAN-2025-11-27.md`, `work-*.md`)

---

## Next Steps (Recommendations)

### High Priority
1. **Integrate VespersAssembler** into the main CLI (`liturginator.py`)
   - Currently `vespers_logic.py` is standalone, not wired up
   - Add `liturginator.py vespers [--date YYYY-MM-DD]` command

2. **Test the Vespers output**
   - Run `VespersAssembler(date).assemble()` for various dates
   - Check stichera insertion, prokeimenon selection, readings

3. **Fix dismissal** - Needs real dismissal text (feast-specific)

### Medium Priority
4. **Consolidate populate scripts** → single `populate.py --cycle triodion|pentecostarion|menaion`

5. **Complete Matins and Hours** - Currently only Vespers has full assembler

6. **Data validation** - Run `./liturginator.py daily 2025-04-20` full year and verify

### Low Priority
7. **GUI or PDF output** - Current output is terminal-only
8. **GUI export** - Print styles, Joplin export

---

## File Inventory Summary

### Core (Working)
- `liturginator.py` - Main CLI (needs Vespers integration)
- `vespers_logic.py` - VespersAssembler (complete logic)
- `day.py`, `year.py`, `datetools.py` - Django-based (may be obsolete?)

### Service Assemblers
- `vespers_logic.py` ✅
- `matins_logic.py` ⚠️ (needs review)
- `hours_logic.py` ⚠️ (needs review)

### Specialized Logic
- `vespers_prokeimenon.py` ✅
- `vespers_paramia.py` ✅
- `kathismata.py` ✅
- `alleluia_period.py` ⚠️ (partial)

### Data Processing
- `lectionary.py` ✅
- `lectionary_pdist.py` ✅ (latest version)
- `get_readings.py` ✅
- `menaion.py` ✅

### Populate Scripts (need consolidation)
- `populate_fixed.py` - Fixed feasts
- `populate_triodion.py` - Triodion period
- `populate_full_pentecostarion.py` - Pentecostarion
- `populate_lent_holy.py` - Lent and Holy Week
- Plus 20+ `populate_*week*.py` files (duplicates)

### Scripts (Cleanup Candidates)
- `extract_*.py` - 5 files (consolidate?)
- `check_*.py`, `clean_*.py`, `add_*.py` - One-offs

---

## To Resume Work

1. **Quick test**:
   ```bash
   source venv/bin/activate
   python -c "
   from vespers_logic import VespersAssembler
   v = VespersAssembler('2026-05-02')
   print(v.assemble())
   "
   ```

2. **Wire up to CLI**:
   - Edit `liturginator.py` to call `VespersAssembler`
   - Add `--service vespers` option

3. **Check data coverage**:
   - Run for several dates (feast days, Lent, ordinary days)
   - See what's missing in output

---

*This report compiled from git history, file inspection, and existing documentation.*