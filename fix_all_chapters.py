#!/usr/bin/env python3
import json
import re

def fix_all_chapterless():
    """Fix ALL readings with empty chapter by extracting from verses"""
    with open('scripture_readings.json', 'r') as f:
        data = json.load(f)
    
    fixed_count = 0
    def fix_recursive(obj):
        nonlocal fixed_count
        if isinstance(obj, dict):
            if 'book' in obj and 'chapter' in obj and not obj['chapter'] and 'verses' in obj:
                # Extract chapter from verses "9:37-43a" -> chapter=9
                match = re.match(r'^(\d+):(.+)$', obj['verses'])
                if match:
                    obj['chapter'] = match.group(1)
                    fixed_count += 1
                    print(f"Fixed {obj['book']} {obj['chapter']}:{obj['verses']}")
            
            for key, value in obj.items():
                fix_recursive(value)
        elif isinstance(obj, list):
            for item in obj:
                fix_recursive(item)
    
    fix_recursive(data)
    print(f"Fixed {fixed_count} readings total.")
    
    with open('scripture_readings.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved updated JSON.")

if __name__ == '__main__':
    fix_all_chapterless()
