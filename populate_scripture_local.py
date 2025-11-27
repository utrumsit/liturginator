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
        'Mt': 'Matthew',
        'Mk': 'Mark',
        'Mrk': 'Mark',
        'Mark': 'Mark',
        'Luke': 'Luke',
        'Lk': 'Luke',
        'Luk': 'Luke',
        'John': 'John',
        'Jn': 'John',
        'Jhn': 'John',
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
        'Rev': 'Revelation',
        'Wisdom': 'Wisdom'
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
    # Add Wisdom (Apocrypha) manually
    bible['Wisdom'] = {
        '4': {
            '7': 'But the righteous man, though he die early, will find rest.',
            '8': 'For old age is not honored for length of days, nor measured by number of years;',
            '9': 'but understanding is gray hair for men, and a blameless life is ripe old age.',
            '10': 'There was one who pleased God and was loved by him, and while living among sinners he was taken up.',
            '11': 'He was caught up lest evil should change his understanding or guile deceive his soul.',
            '12': 'For the fascination of wickedness obscures what is good, and roving desire perverts the innocent mind.',
            '13': 'Being perfected in a short time, he fulfilled long years;',
            '14': 'for his soul was pleasing to the Lord, therefore he took him quickly from the midst of wickedness.',
            '15': 'Yet the peoples saw and did not understand, nor take such a thing to heart, that God\'s grace and mercy are with his saints, and he looks upon his chosen ones.',
            '16': 'But the righteous man who has died will condemn the ungodly who are living, and youth that was quickly perfected will condemn the prolonged old age of the unrighteous.',
            '17': 'For they will see the end of the wise man, and will not understand what the Lord purposed for him, and for what he kept him safe.',
            '19': 'For after death the righteous man will condemn the ungodly who are living, and youth that was quickly perfected will condemn the prolonged old age of the unrighteous.',
            '20': 'They will see and will have contempt for them, and the Lord will laugh them to scorn.',
        },
        '5': {
            '1': 'Then the righteous man will stand with great confidence in the presence of those who have afflicted him, and those who make light of his labors.',
            '2': 'When they see him, they will be shaken with dreadful fear, and they will be amazed at his unexpected salvation.',
            '3': 'They will speak to one another in repentance, and in anguish of spirit they will groan, and say,',
            '4': '"This is he whom we once held in derision and made a byword of reproach--',
            '5': 'we fools accounted his life madness and his end dishonorable.',
            '6': 'How is he numbered among the sons of God? And how is his lot among the saints?',
            '7': 'We have erred, therefore, and the way of righteousness we have not known; the light has not shone upon us, and the sun has not risen upon us.',
        }
    }
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
        print(f"Book {book} not found")
        return f"Book {book} not found"

    if ':' in verses or ';' in verses:
        # Cross-chapter or complex
        if ';' in verses:
            chapter_parts = verses.split(';')
        else:
            chapter_parts = [verses]
        all_texts = []
        for chap_part in chapter_parts:
            chap_part = chap_part.strip()
            if ':' in chap_part:
                ch_v = chap_part.split(':', 1)
                current_chapter = int(ch_v[0])
                verse_part = ch_v[1]
            else:
                current_chapter = chapter
                verse_part = chap_part
            parts = verse_part.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-', 1)
                    start = start.strip()
                    end = end.strip()
                    try:
                        start_v = int(start) if start.isdigit() else 0
                        end_v = int(end) if end.isdigit() else 0
                        # Collect texts
                        if str(current_chapter) in bible[book_abbr]:
                            chap = bible[book_abbr][str(current_chapter)]
                            for v in range(start_v, end_v + 1):
                                if str(v) in chap:
                                    all_texts.append(chap[str(v)])
                    except ValueError:
                        # Skip invalid
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
            print(f"Chapter {chapter} not found for {book}")
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
            if 'book' in data and 'chapter' in data and 'verses' in data and 'text' in data and (data['text'] == "" or "not found" in data['text']):
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