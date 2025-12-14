#!/usr/bin/env python3
"""
Generate Byzantine Catholic filtered readings JSON
Removes problematic saints like Alexis Toth
"""
from datetime import date, timedelta
import json
from lectionary_pdist import LectionaryPdist

# Byzantine Catholic SAFE saints/feasts only
BYZANTINE_SAFE = [
    'Theotokos', 'Basil the Great', 'John Chrysostom', 'Gregory the Theologian',
    'Nicholas', 'Stephen', 'Lawrence', 'Andrew', 'Philip', 'James', 'Thomas',
    'Matthias', 'Bartholomew', 'Seraphim of Sarov', 'Anthony the Great',
    'Mary of Egypt', 'Great Martyr', 'Hieromartyr', 'Theophany', 'Nativity',
    'Transfiguration', 'Annunciation', 'Dormition', 'Nativity of John Baptist'
]

PROBLEMATIC_Saints = [
    'Alexis Toth', 'Toth', 'OCA', 'Orthodoxy in America'
]

lect = LectionaryPdist(rsv_xml_path='rsv.xml')
start = date(2025, 12, 14)
end = date(2035, 12, 13)
days = (end - start).days + 1

print('Generating Byzantine Catholic filtered readings...')

readings = {}
problematic_count = 0
for i in range(days):
    d = start + timedelta(i)
    result = lect.get_readings(d)
    
    # Filter saint readings
    if result.get('feast_name'):
        feast_name = result['feast_name'].lower()
        is_problematic = any(p.lower() in feast_name for p in PROBLEMATIC_Saints)
        if is_problematic:
            print(f'SKIPPING problematic saint: {result['feast_name']} on {d}')
            problematic_count += 1
            # Keep daily readings, remove saint readings
            result['saint_epistle'] = None
            result['saint_gospel'] = None
            result['feast_level'] = 1  # Downgrade to minor
        else:
            # Safe saint - keep as-is
            pass
    
    readings[str(d)] = result
    
    if i % 500 == 0:
        print(f'Progress: {i}/{days}')

print(f'✅ FILTERED: {problematic_count} problematic saints removed')
print(f'✅ SAFE: {len(readings)} days Byzantine Catholic approved')

with open('docs/readings_2025-2035-bc.json', 'w') as f:
    json.dump(readings, f, default=str, indent=1)

print('✅ BYZANTINE CATHOLIC JSON ready: docs/readings_2025-2035-bc.json')
