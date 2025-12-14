#!/usr/bin/env python3
"""
Byzantine Catholic Saints Filter
Keep: Pre-1600 saints + verified BC saints (Romzha)
Remove: Post-1600 Orthodox-only saints (Toth, etc.)
"""
from datetime import date, timedelta
import json
from lectionary_pdist import LectionaryPdist

# Byzantine Catholic SAFE saints (pre-1600 + verified post-1600)
BC_SAFE_Saints = [
    # Pre-1600 universal saints
    'Theotokos', 'Basil the Great', 'John Chrysostom', 'Gregory the Theologian',
    'Nicholas', 'Stephen', 'Demetrius', 'George', 'Michael', 'Gabriel',
    'Anthony the Great', 'Mary of Egypt', 'Seraphim of Sarov', 'Sergius of Radonezh',
    
    # Verified Byzantine Catholic saints/martyrs
    'Theodore Romzha', 'Teodor Romzha', 'Romzha', 'Rohmza',
    
    # Major feasts (always safe)
    'Nativity', 'Theophany', 'Transfiguration', 'Annunciation', 'Dormition',
    'Exaltation of the Cross', 'Nativity of John Baptist'
]

PROBLEMATIC = [
    'Alexis Toth', 'Toth', 'OCA', 'Orthodoxy in America', 'Confessor and Defender'
]

lect = LectionaryPdist(rsv_xml_path='rsv.xml')
start = date(2025, 12, 14)
end = date(2035, 12, 13)

print('Creating Byzantine Catholic calendar (Pre-1600 + Romzha)...')

readings = {}
skipped = 0
for i in range((end - start).days + 1):
    d = start + timedelta(i)
    result = lect.get_readings(d)
    
    # Filter saint readings
    if result.get('feast_name'):
        feast_lower = result['feast_name'].lower()
        
        # Skip problematic saints
        if any(p.lower() in feast_lower for p in PROBLEMATIC):
            print(f'SKIPPED: {result["feast_name"]} ({d})')
            skipped += 1
            result['saint_epistle'] = None
            result['saint_gospel'] = None
            result['feast_level'] = 1  # Downgrade
        else:
            # Keep if pre-1600 or verified BC saint
            is_safe = any(s.lower() in feast_lower for s in BC_SAFE_Saints)
            if not is_safe and 'st ' in feast_lower and not any(f.lower() in feast_lower for f in ['theotokos', 'nativity', 'theophany']):
                print(f'FILTERED: {result["feast_name"]} ({d})')
                result['saint_epistle'] = None
                result['saint_gospel'] = None
                result['feast_level'] = 1
    
    readings[str(d)] = result
    
    if i % 500 == 0:
        print(f'Progress: {i}/{(end - start).days + 1}')

print(f'✅ Byzantine Catholic calendar ready!')
print(f'✅ Skipped {skipped} problematic saints')
print(f'✅ {len(readings)} safe days')

with open('docs/readings_2025-2035-bc-safe.json', 'w') as f:
    json.dump(readings, f, default=str, indent=1)

print('✅ SAVED: docs/readings_2025-2035-bc-safe.json')
