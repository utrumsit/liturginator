#!/usr/bin/env python3
import json
import re
import xml.etree.ElementTree as ET

def load_rsv_bible():
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
    tree = ET.parse('rsv.xml')
    root = tree.getroot()
    bible = {}
    for book_elem in root.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}div'):
        if book_elem.get('type') == 'book':
            book_id = book_elem.get('osisID')
            if book_id:
                bible[book_id] = {}
                for chapter_elem in book_elem.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}chapter'):
                    chapter_id = chapter_elem.get('osisID')
                    if chapter_id:
                        chapter_num = chapter_id.split('.')[1]
                        bible[book_id][chapter_num] = {}
                        for verse_elem in chapter_elem.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}verse'):
                            verse_id = verse_elem.get('osisID')
                            if verse_id:
                                verse_num = verse_id.split('.')[2]
                                text = verse_elem.text or ''
                                bible[book_id][chapter_num][verse_num] = text.strip()
    print(f"Bible loaded: {len(bible)} books")
    return bible

def populate_all():
    bible = load_rsv_bible()
    with open('scripture_readings.json', 'r') as f:
        data = json.load(f)
    
    def update(obj):
        if isinstance(obj, dict) and all(k in obj for k in ['book', 'chapter', 'verses', 'text']):
            if not obj['text'] or 'No texts found' in obj['text']:
                # Map book names to OSIS IDs
                book_map = {
                    'Matthew': 'Matt', 'Mt': 'Matt',
                    'Mark': 'Mark', 'Mk': 'Mark',
                    'Luke': 'Luke', 'Lk': 'Luke',
                    'John': 'John', 'Jn': 'John',
                    'Acts': 'Acts',
                    'Romans': 'Rom',
                    '1 Corinthians': '1Cor', '1 Cor': '1Cor',
                    '2 Corinthians': '2Cor', '2 Cor': '2Cor',
                    'Galatians': 'Gal',
                    'Ephesians': 'Eph',
                    'Philippians': 'Phil',
                    'Colossians': 'Col',
                    '1 Thessalonians': '1Thess',
                    '2 Thessalonians': '2Thess',
                    '1 Timothy': '1Tim',
                    '2 Timothy': '2Tim',
                    'Hebrews': 'Heb',
                    'James': 'Jas',
                    '1 Peter': '1Pet',
                    '2 Peter': '2Pet',
                    '1 John': '1John',
                    '2 John': '2John',
                    '3 John': '3John',
                    'Jude': 'Jude',
                    'Revelation': 'Rev'
                }
                book_osid = book_map.get(obj['book'].strip(), obj['book'].strip())
                
                # Fix chapter from verses if empty
                if not obj['chapter'] and ':' in obj['verses']:
                    m = re.match(r'^(\d+):(.+)$', obj['verses'])
                    if m:
                        obj['chapter'] = m.group(1)
                        obj['verses'] = m.group(2)
                
                # Clean verse suffixes: 43a -> 43
                verses_clean = re.sub(r'(\d+)[a-zA-Z]', r'\1', obj['verses'])
                
                if book_osid in bible and obj['chapter'] in bible[book_osid]:
                    chap = bible[book_osid][obj['chapter']]
                    verse_nums = re.sub(r'(\d+)[a-zA-Z]', r'\1', obj['verses'])
                    verse_nums = re.split(r'[,\s-]+', verse_nums)
                    texts = []
                    for v_range in verse_nums:
                        v_range = v_range.strip()
                        if '-' in v_range:
                            start, end = v_range.split('-')
                            for v in range(int(start), int(end) + 1):
                                texts.append(chap.get(str(v), f"[v{v} missing]"))
                        else:
                            texts.append(chap.get(v_range, f"[v{v_range} missing]"))
                    obj['text'] = ' '.join(texts)
                else:
                    obj['text'] = f"Book/Chapter not found: {book_osid} {obj['chapter']}"
        
        if isinstance(obj, (dict, list)):
            items = obj.values() if isinstance(obj, dict) else obj
            for v in items:
                update(v)
    
    update(data)
    with open('scripture_readings.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("✅ COMPLETE: All RSV texts populated!")

if __name__ == '__main__':
    populate_all()
