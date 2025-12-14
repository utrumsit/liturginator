#!/usr/bin/env python3
"""
RSV Text Extractor - Complete cross-chapter support
Handles Galatians 5.22-6.2 → Gal 5:22-end + 6:1-2
"""
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

class RSVExtractor:
    BOOK_MAP = {
        'Genesis': 'Gen', 'Exodus': 'Exod', 'Leviticus': 'Lev', 'Numbers': 'Num', 
        'Deuteronomy': 'Deut', 'Joshua': 'Josh', 'Judges': 'Judg', 'Ruth': 'Ruth',
        '1 Samuel': '1Sam', '2 Samuel': '2Sam', '1 Kings': '1Kgs', '2 Kings': '2Kgs',
        '1 Chronicles': '1Chr', '2 Chronicles': '2Chr', 'Ezra': 'Ezra', 'Nehemiah': 'Neh',
        'Esther': 'Esth', 'Job': 'Job', 'Psalms': 'Ps', 'Proverbs': 'Prov',
        'Ecclesiastes': 'Eccl', 'Song of Solomon': 'Song', 'Isaiah': 'Isa',
        'Jeremiah': 'Jer', 'Lamentations': 'Lam', 'Ezekiel': 'Ezek', 'Daniel': 'Dan',
        'Matthew': 'Matt', 'Mark': 'Mark', 'Luke': 'Luke', 'John': 'John',
        'Acts': 'Acts', 'Romans': 'Rom', '1 Corinthians': '1Cor', '2 Corinthians': '2Cor',
        'Galatians': 'Gal', 'Ephesians': 'Eph', 'Philippians': 'Phil', 'Colossians': 'Col',
        '1 Thessalonians': '1Thess', '2 Thessalonians': '2Thess', '1 Timothy': '1Tim',
        '2 Timothy': '2Tim', 'Titus': 'Titus', 'Philemon': 'Phlm', 'Hebrews': 'Heb',
        'James': 'Jas', '1 Peter': '1Pet', '2 Peter': '2Pet', '1 John': '1John',
        '2 John': '2John', '3 John': '3John', 'Jude': 'Jude', 'Revelation': 'Rev',
        'Apostol': 'Apostol'
    }
    
    def __init__(self, xml_path: str = 'rsv.xml'):
        self.xml_path = xml_path
        self.bible = self._load_bible()
    
    def _load_bible(self) -> Dict:
        bible = {}
        tree = ET.parse(self.xml_path)
        root = tree.getroot()
        ns = '{http://www.bibletechnologies.net/2003/OSIS/namespace}'
        
        for book_elem in root.iter(f'{ns}div'):
            if book_elem.get('type') == 'book':
                book_id = book_elem.get('osisID')
                if book_id:
                    bible[book_id] = {}
                    for chapter_elem in book_elem.iter(f'{ns}chapter'):
                        chapter_id = chapter_elem.get('osisID')
                        if chapter_id:
                            chapter_num = chapter_id.split('.')[1]
                            bible[book_id][chapter_num] = {}
                            for verse_elem in chapter_elem.iter(f'{ns}verse'):
                                verse_id = verse_elem.get('osisID')
                                if verse_id:
                                    verse_num = verse_id.split('.')[2]
                                    full_text = ''.join(verse_elem.itertext()).strip()
                                    bible[book_id][chapter_num][verse_num] = full_text
        return bible
    
    def extract_text(self, pericope_ref: str) -> Optional[str]:
        pericope_ref = pericope_ref.replace('.', ':')
        match = re.match(r'^([A-Za-z0-9 ]+)\s+(\d+):(.+)$', pericope_ref.strip())
        if not match:
            return None
        
        book_name = match.group(1).strip()
        chapter = match.group(2)
        verses_str = match.group(3).strip()
        
        book_id = self.BOOK_MAP.get(book_name)
        if not book_id or book_id not in self.bible:
            return None
        
        texts = []
        
        # Handle cross-chapter: "5:22-6:2"
        if '-' in verses_str and ':' in verses_str:
            parts = verses_str.split('-')
            if len(parts) == 2:
                # First part: current chapter from start verse to end
                start_v_str = parts[0].strip()
                try:
                    start_v = int(start_v_str)
                    if chapter in self.bible[book_id]:
                        ch_data = self.bible[book_id][chapter]
                        max_v = max(map(int, ch_data.keys())) if ch_data else 30
                        for v in range(start_v, max_v + 1):
                            v_str = str(v)
                            if v_str in ch_data:
                                texts.append(ch_data[v_str])
                except ValueError:
                    pass
                
                # Second part: next chapter verses 1-end_v
                end_part = parts[1].strip()
                if ':' in end_part:
                    end_ch_str, end_v_str = end_part.split(':', 1)
                    next_ch = str(int(chapter) + 1)
                    try:
                        end_v = int(end_v_str)
                        if next_ch in self.bible[book_id]:
                            ch_data = self.bible[book_id][next_ch]
                            for v in range(1, end_v + 1):
                                v_str = str(v)
                                if v_str in ch_data:
                                    texts.append(ch_data[v_str])
                    except ValueError:
                        pass
                    return ' '.join(texts)
        
        # Single chapter fallback
        verse_nums = self._simple_parse_verses(verses_str)
        if chapter in self.bible[book_id]:
            ch_data = self.bible[book_id][chapter]
            for v_num in verse_nums:
                v_str = str(v_num)
                if v_str in ch_data:
                    texts.append(ch_data[v_str])
        
        return ' '.join(texts)
    
    def _simple_parse_verses(self, verses_str: str) -> List[int]:
        verses_clean = re.sub(r'[a-zA-Z:]', '', verses_str)
        parts = re.split(r'[,;]', verses_clean)
        all_verses = []
        for part in parts:
            part = part.strip()
            if not part or '-' not in part:
                try:
                    all_verses.append(int(part))
                except ValueError:
                    continue
            else:
                try:
                    start_str, end_str = part.split('-', 1)
                    start = int(start_str.strip())
                    end = min(int(end_str.strip()), 30)
                    all_verses.extend(range(start, end + 1))
                except ValueError:
                    continue
        return all_verses

if __name__ == '__main__':
    extractor = RSVExtractor()
    print(extractor.extract_text("Galatians 5.22-6.2"))
