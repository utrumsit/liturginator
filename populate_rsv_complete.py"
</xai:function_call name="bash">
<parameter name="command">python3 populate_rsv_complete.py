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
                book_name = book_id  # Use OSIS ID directly (Gen, Matt, Luke, etc.)
                bible[book_name] = {}
                for chapter_elem in book_elem.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}chapter'):
                    chapter_id = chapter_elem.get('osisID')
                    if chapter_id:
                        chapter_num = chapter_id.split('.')[1]
                        bible[book_name][chapter_num] = {}
                        for verse_elem in chapter_elem.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}verse'):
                            verse_id = verse_elem.get('osisID')
                            if verse_id:
                                verse_num = verse_id.split('.')[2]
                                text = verse_elem.text or ''
                                bible[book_name][chapter_num][verse_num] = text.strip()
    print(f"Bible loaded: {len(bible)} books")
    return bible

def parse_verses(verses_str):
    # Remove letter suffixes: 43a -> 43
    verses_str = re.sub(r'(\d+)[a-zA-Z]', r'\1', verses_str)
    if ':' in verses_str:
        verses_str = verses_str.split(':', 1)[1]
    parts = re.split(r'[,\s]+', verses_str)
    verse_nums = []
    for part in parts:
        part = part.strip()
        if not part: continue
        if '-' in part:
            try:
                start, end = part.split('-', 1)
                verse_nums.extend(range(int(start), int(end) + 1))
            except: pass
        else:
            try:
                verse_nums.append(int(part))
            except: pass
    return verse_nums

def get_rsv_text(bible, book, chapter, verses):
    # Map common names to OSIS IDs
    book_map = {
        'Matthew': 'Matt', 'Mt': 'Matt',
        'Mark': 'Mark', 'Mk': 'Mark',
        'Luke': 'Luke', 'Lk': 'Luke',
        'John': 'John', 'Jn': 'John',
        'Acts': 'Acts',
        'Romans': 'Rom', 'Rom.': 'Rom',
        '1 Corinthians': '1Cor', '1 Cor': '1Cor',
        '2 Corinthians': '2Cor', '2 Cor': '2Cor',
        'Galatians': 'Gal',
        'Ephesians': 'Eph',
        'Philippians': 'Phil',
        'Colossians': 'Col',
        '1 Thessalonians': '1Thess', '1 Thess': '1Thess',
        '2 Thessalonians': '2Thess', '2 Thess': '2Thess',
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
    
    book_osid = book_map.get(book.strip(), book.strip())
    
    if book_osid not in bible:
        return f"Book '{book_osid}' not found (tried {book})"
    
    chapter = str(chapter) if chapter else '1'
    if chapter not in bible[book_osid]:
        return f"Chapter {chapter} not found in {book}"
    
    chap = bible[book_osid][chapter]
    verse_nums = parse_verses(verses)
    texts = []
    for v in verse_nums:
        v_str = str(v)
        texts.append(chap.get(v_str, f"[v{v_str} missing]"))
    return ' '.join(texts)

def populate():
    bible = load_rsv_bible()
    with open('scripture_readings.json', 'r') as f:
        data = json.load(f)
    
    def update(obj):
        if isinstance(obj, dict) and all(k in obj for k in ['book', 'chapter', 'verses', 'text']):
            if not obj['text'] or 'No texts found' in obj['text'] or 'not found' in obj['text']:
                text = get_rsv_text(bible, obj['book'], obj['chapter'], obj['verses'])
                obj['text'] = text
        
        if isinstance(obj, (dict, list)):
            for v in obj.values() if isinstance(obj, dict) else obj:
                update(v)
    
    update(data)
    with open('scripture_readings.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("✅ All RSV texts populated!")

if __name__ == '__main__':
    populate()
