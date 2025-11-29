#!/usr/bin/env python3
import json
import re
import xml.etree.ElementTree as ET

def load_rsv_bible():
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
    tree = ET.parse('rsv.xml')
    root = tree.getroot()
    bible = {}
    for book in root.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}div'):
        if book.get('type') == 'book':
            book_id = book.get('osisID')
            if book_id:
                book_name = book_id  # Use OSIS ID directly
                bible[book_name] = {}
                for chapter in book.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}chapter'):
                    chapter_id = chapter.get('osisID')
                    if chapter_id:
                        chapter_num = chapter_id.split('.')[1]
                        bible[book_name][chapter_num] = {}
                        for verse in chapter.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}verse'):
                            verse_id = verse.get('osisID')
                            if verse_id:
                                verse_num = verse_id.split('.')[2]
                                text = verse.text or ''
                                bible[book_name][chapter_num][verse_num] = text
    print("Bible loaded with", len(bible), "books")
    return bible

def parse_verses(verses_str):
    verses_str = re.sub(r'(\d+)[a-zA-Z]', r'\1', verses_str)  # 43a -> 43
    if ':' in verses_str:
        verses_str = verses_str.split(':', 1)[1]
    parts = re.split(r'[,\s]+', verses_str)
    verse_nums = []
    for part in parts:
        part = part.strip()
        if not part: continue
        if '-' in part:
            start_str, end_str = part.split('-', 1)
            try:
                verse_nums.extend(range(int(start_str), int(end_str) + 1))
            except: pass
        else:
            try:
                verse_nums.append(int(part))
            except: pass
    return verse_nums

def get_rsv_text(bible, book, chapter, verses):
    if book not in bible:
        return f"Book {book} not found"
    
    chapter = str(chapter) if chapter else '1'
    if chapter not in bible[book]:
        return f"Chapter {chapter} not found for {book}"
    
    chap = bible[book][chapter]
    verse_nums = parse_verses(verses)
    texts = []
    for v in verse_nums:
        v_str = str(v)
        texts.append(chap.get(v_str, f"[Verse {v} missing]"))
    return ' '.join(texts).strip()

def populate_all():
    bible = load_rsv_bible()
    with open('scripture_readings.json', 'r') as f:
        data = json.load(f)
    
    def update(obj):
        if isinstance(obj, dict) and all(k in obj for k in ['book', 'chapter', 'verses', 'text']):
            if not obj['text'] or 'No texts found' in obj['text']:
                # Fix chapter from verses if empty
                if not obj['chapter'] and ':' in obj['verses']:
                    m = re.match(r'^(\d+):(.+)$', obj['verses'])
                    if m:
                        obj['chapter'] = m.group(1)
                        obj['verses'] = m.group(2)
                
                text = get_rsv_text(bible, obj['book'], obj['chapter'], obj['verses'])
                obj['text'] = text
        
        for v in obj.values():
            update(v) if isinstance(v, (dict, list)) else None
    
    update(data)
    with open('scripture_readings.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("✅ All RSV texts populated!")

if __name__ == '__main__':
    populate_all()
