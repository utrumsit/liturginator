#!/usr/bin/env python3
import json
import re

def populate_missing_texts():
    bible = load_rsv_bible()  # Use existing function
    
    with open('scripture_readings.json', 'r') as f:
        data = json.load(f)
    
    def update_reading(reading):
        if 'text' in reading and reading['text'] and 'No texts found' not in reading['text']:
            return
        
        book = reading['book']
        chapter = reading.get('chapter', '')
        verses = reading['verses']
        
        # Extract chapter from verses if missing: "9:37-43a" -> chapter=9
        if not chapter and ':' in verses:
            match = re.match(r'^(\d+):(.+)$', verses)
            if match:
                chapter = match.group(1)
                verses = match.group(2)
        
        # Clean verse suffixes: "43a" -> "43"
        verses_clean = re.sub(r'(\d+)[a-zA-Z]', r'\1', verses)
        
        text = get_rsv_text(bible, book, chapter, verses_clean)
        reading['text'] = text
        
        if text.startswith('No texts found'):
            print(f"Failed: {book} {chapter}:{verses}")
    
    def recurse(obj):
        if isinstance(obj, dict):
            if 'book' in obj and 'chapter' in obj and 'verses' in obj:
                update_reading(obj)
            for v in obj.values():
                recurse(v)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)
    
    recurse(data)
    
    with open('scripture_readings.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("Population complete.")

if __name__ == '__main__':
    populate_missing_texts()
