#!/usr/bin/env python3
import json
from datetime import date, timedelta
from lectionary_pdist import LectionaryPdist

lect = LectionaryPdist()
start = date(2025, 12, 14)
end = date(2035, 12, 13)
days = (end - start).days + 1

print(f'Generating {days} days WITH FULL RSV TEXT...')

readings = {}
for i in range(days):
    d = start + timedelta(i)
    result = lect.get_readings(d)
    
    # Add FULL RSV text to each reading (safe access)
    for key in ['daily_epistle', 'epistle', 'saint_epistle']:
        if key in result and result[key] and 'display' in result[key]:
            result[key]['rsv_text'] = lect.rsv_extractor.extract_text(result[key]['display']) if lect.rsv_extractor else None
    
    for key in ['daily_gospel', 'gospel', 'saint_gospel']:
        if key in result and result[key] and 'display' in result[key]:
            result[key]['rsv_text'] = lect.rsv_extractor.extract_text(result[key]['display']) if lect.rsv_extractor else None
    
    readings[str(d)] = result
    
    if i % 500 == 0:
        print(f'Progress: {i}/{days} ({i/days*100:.1f}%)')

with open('docs/readings_2025-2035-full.json', 'w') as f:
    json.dump(readings, f, default=str, indent=1)

print(f'✅ COMPLETE: docs/readings_2025-2035-full.json ({len(readings)} days with FULL RSV text!)')
