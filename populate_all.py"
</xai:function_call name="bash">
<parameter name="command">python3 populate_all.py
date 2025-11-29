#!/usr/bin/env python3
import json
import re
from populate_scripture_local import load_rsv_bible, get_rsv_text, parse_verses

def populate_all_missing():
    bible = load_rsv_bible()
    
    with open('scripture_readings.json', 'r') as f:
        data = json.load(f)
    
    fixed = 0
    def update(obj):
        nonlocal fixed
        if isinstance(obj, dict):
            if 'book' in obj and 'chapter' in obj and 'verses' in obj and 'text' in obj:
                if obj['text'] == '' or 'No texts found' in obj['text'] or 'not found' in obj['text']:
                    # Fix chapter from verses if needed
                    if not obj['chapter'] and ':' in obj['verses']:
                        match = re.match(r'^(\d+):(.+)$', obj['verses'])
                        if match:
                            obj['chapter'] = match.group(1)
                            obj['verses'] = match.group(2)
                    
                    # Clean verse suffixes
                    verses_clean = re.sub(r'(\d+)[a-zA-Z]', r'\1', obj['verses'])
                    
                    text = get_rsv_text(bible, obj['book'], obj['chapter'], verses_clean)
                    obj['text'] = text
                    fixed += 1
                    if fixed % 50 == 0:
                        print(f"Fixed {fixed} readings...")
            
            for v in obj.values():
                update(v)
        elif isinstance(obj, list):
            for item in obj:
                update(item)
    
    update(data)
    
    with open('scripture_readings.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ COMPLETE: Fixed {fixed} readings. Run 'grep -c \"No texts found\" scripture_readings.json' to verify.")

if __name__ == '__main__':
    populate_all_missing()
