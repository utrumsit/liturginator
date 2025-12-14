#!/usr/bin/env python3
from datetime import date, timedelta
import json
from lectionary_pdist import LectionaryPdist

lect = LectionaryPdist()
extractor = lect.rsv_extractor  # Get extractor directly

start = date(2025, 12, 14)
end = date(2035, 12, 13)
days = (end - start).days + 1

print(f'Regenerating {days} days WITH CORRECT RSV TEXT...')

readings = {}
for i in range(days):
    d = start + timedelta(i)
    result = lect.get_readings(d)
    
    # FORCE RSV extraction for ALL readings
    for key in ['epistle', 'gospel', 'saint_epistle', 'saint_gospel']:
        if key in result and result[key] and 'display' in result[key]:
            rsv_text = extractor.extract_text(result[key]['display']) if extractor else None
            result[key]['rsv_text'] = rsv_text or ''
    
    readings[str(d)] = result
    
    if i % 500 == 0:
        print(f'Progress: {i}/{days} ({i/days*100:.1f}%)')

with open('docs/readings_2025-2035-full.json', 'w') as f:
    json.dump(readings, f, default=str, indent=1)

print(f'✅ REGENERATED: docs/readings_2025-2035-full.json with FULL RSV text!')
