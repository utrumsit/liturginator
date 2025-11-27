#!/usr/bin/env python3
"""
Populate scripture_readings.json with RSV texts from rsv.xml.
"""

import json
import xml.etree.ElementTree as ET
import re

RSV_XML = 'rsv.xml'

def load_rsv_bible():
    """
    Load RSV Bible from XML into dict: book_abbr -> chapter -> verse -> text
    """
    ns = {'osis': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
    book_map = {
        'Gen': 'Genesis',
        'Exod': 'Exodus',
        'Lev': 'Leviticus',
        'Num': 'Numbers',
        'Deut': 'Deuteronomy',
        'Josh': 'Joshua',
        'Judg': 'Judges',
        'Ruth': 'Ruth',
        '1Sam': '1 Samuel',
        '2Sam': '2 Samuel',
        '1Kgs': '1 Kings',
        '2Kgs': '2 Kings',
        '1Chr': '1 Chronicles',
        '2Chr': '2 Chronicles',
        'Ezra': 'Ezra',
        'Neh': 'Nehemiah',
        'Esth': 'Esther',
        'Job': 'Job',
        'Ps': 'Psalm',
        'Prov': 'Proverbs',
        'Eccl': 'Ecclesiastes',
        'Song': 'Song of Solomon',
        'Isa': 'Isaiah',
        'Jer': 'Jeremiah',
        'Lam': 'Lamentations',
        'Ezek': 'Ezekiel',
        'Dan': 'Daniel',
        'Hos': 'Hosea',
        'Joel': 'Joel',
        'Amos': 'Amos',
        'Obad': 'Obadiah',
        'Jonah': 'Jonah',
        'Mic': 'Micah',
        'Nah': 'Nahum',
        'Hab': 'Habakkuk',
        'Zeph': 'Zephaniah',
        'Hag': 'Haggai',
        'Zech': 'Zechariah',
        'Mal': 'Malachi',
        'Matt': 'Matthew',
        'Mark': 'Mark',
        'Luke': 'Luke',
        'John': 'John',
        'Acts': 'Acts',
        'Rom': 'Romans',
        '1Cor': '1 Corinthians',
        '2Cor': '2 Corinthians',
        'Gal': 'Galatians',
        'Eph': 'Ephesians',
        'Phil': 'Philippians',
        'Col': 'Colossians',
        '1Thess': '1 Thessalonians',
        '2Thess': '2 Thessalonians',
        '1Tim': '1 Timothy',
        '2Tim': '2 Timothy',
        'Titus': 'Titus',
        'Phlm': 'Philemon',
        'Heb': 'Hebrews',
        'Jas': 'James',
        '1Pet': '1 Peter',
        '2Pet': '2 Peter',
        '1John': '1 John',
        '2John': '2 John',
        '3John': '3 John',
        'Jude': 'Jude',
        'Rev': 'Revelation'
    }
    tree = ET.parse('rsv.xml')
    root = tree.getroot()
    bible = {}
    for book in root.iter('{http://www.bibletechnologies.net/2003/OSIS/namespace}div'):
        if book.get('type') == 'book':
            book_id = book.get('osisID')
            if book_id:
                book_name = book_map.get(book_id, book_id)
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
    """
    Parse verses string like "1-17" or "1:1-8" or "39-49, 56" into list of verse numbers.
    """
    # If verses_str contains ':', split and take the verse part
    if ':' in verses_str:
        verses_str = verses_str.split(':', 1)[1]
    parts = re.split(r'[,\s]+', verses_str)
    verse_nums = []
    for part in parts:
        if '-' in part:
            split_part = part.split('-')
            if len(split_part) == 2:
                start_str, end_str = split_part
                try:
                    start, end = int(start_str), int(end_str)
                    verse_nums.extend(range(start, end + 1))
                except:
                    continue
            else:
                # Invalid
                continue
        else:
            try:
                verse_nums.append(int(part))
            except:
                continue
    return verse_nums

def get_rsv_text(bible, book, chapter, verses):
    """
    Extract text for a pericope, handling cross-chapter and non-consecutive verses.
    """
    book_abbr = book
    if book_abbr not in bible:
        return f"Book {book} not found"

    if ':' in verses:
        # Cross-chapter or complex
        parts = verses.split(',')
        all_texts = []
        current_chapter = chapter
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-', 1)
                start = start.strip()
                end = end.strip()
                try:
                    if ':' in start:
                        start_ch, start_v_str = start.split(':', 1)
                        start_ch = int(start_ch)
                        start_v = int(start_v_str) if start_v_str.isdigit() else 0
                    else:
                        start_ch = current_chapter
                        start_v = int(start) if start.isdigit() else 0
                    if ':' in end:
                        end_ch, end_v_str = end.split(':', 1)
                        end_ch = int(end_ch)
                        end_v = int(end_v_str) if end_v_str.isdigit() else 0
                    else:
                        end_ch = current_chapter
                        end_v = int(end) if end.isdigit() else 0
                    # Collect texts
                    if start_ch == end_ch:
                        if str(start_ch) in bible[book_abbr]:
                            chap = bible[book_abbr][str(start_ch)]
                            for v in range(start_v, end_v + 1):
                                if str(v) in chap:
                                    all_texts.append(chap[str(v)])
                    else:
                        # From start_ch:start_v to end of start_ch
                        if str(start_ch) in bible[book_abbr]:
                            chap = bible[book_abbr][str(start_ch)]
                            max_v = max((int(v) for v in chap.keys() if v.isdigit()), default=0)
                            for v in range(start_v, max_v + 1):
                                if str(v) in chap:
                                    all_texts.append(chap[str(v)])
                        # From end_ch:1 to end_v
                        if str(end_ch) in bible[book_abbr]:
                            chap = bible[book_abbr][str(end_ch)]
                            for v in range(1, end_v + 1):
                                if str(v) in chap:
                                    all_texts.append(chap[str(v)])
                    current_chapter = end_ch
                except ValueError:
                    # Skip invalid verse ranges
                    continue
            else:
                # Single verse
                try:
                    v = int(part)
                    if str(current_chapter) in bible[book_abbr] and str(v) in bible[book_abbr][str(current_chapter)]:
                        all_texts.append(bible[book_abbr][str(current_chapter)][str(v)])
                except ValueError:
                    continue
        result = ' '.join(all_texts).strip()
        return result if result else f"No texts found for {book} {chapter}:{verses}"
    else:
        # Normal single chapter
        if str(chapter) not in bible[book_abbr]:
            return f"Chapter {chapter} not found"
        chap = bible[book_abbr][str(chapter)]
        verse_nums = parse_verses(verses)
        texts = []
        for v in verse_nums:
            if str(v) in chap:
                texts.append(chap[str(v)])
            else:
                texts.append(f"[Verse {v} not found]")
        result = ' '.join(texts).strip()
        return result if result else f"No texts found for {book} {chapter}:{verses}"

def populate_json():
    """
    Populate scripture_readings.json with texts.
    """
    bible = load_rsv_bible()
    with open('scripture_readings.json', 'r', encoding='utf-8') as f:
        readings = json.load(f)

    def update_texts(data):
        if isinstance(data, dict):
            if 'book' in data and 'chapter' in data and 'verses' in data and 'text' in data and data['text'] == "":
                text = get_rsv_text(bible, data['book'], data['chapter'], data['verses'])
                data['text'] = text
            else:
                for key, value in data.items():
                    update_texts(value)
        elif isinstance(data, list):
            for item in data:
                update_texts(item)

    for section, data in readings.items():
        update_texts(data)

    with open('scripture_readings.json', 'w', encoding='utf-8') as f:
        json.dump(readings, f, indent=2, ensure_ascii=True)

if __name__ == '__main__':
    populate_json()