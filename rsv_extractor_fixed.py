#!/usr/bin/env python3
"""
RSV Text Extractor - Fixed version
Handles both dot (Galatians 5.22-6.2) and colon (Luke 13:18-29) formats
"""
import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

class RSVExtractor:
    """Extract RSV verse text from rsv.xml based on pericope references"""
    
    # Book name mapping (various formats -> OSIS book IDs)
    BOOK_MAP = {
        'Genesis': 'Gen', 'Gen': 'Gen',
        'Exodus': 'Exod', 'Exod': 'Exod', 'Ex': 'Exod',
        'Leviticus': 'Lev', 'Lev': 'Lev',
        'Numbers': 'Num', 'Num': 'Num',
        'Deuteronomy': 'Deut', 'Deut': 'Deut',
        'Joshua': 'Josh', 'Josh': 'Josh',
        'Judges': 'Judg', 'Judg': 'Judg',
        'Ruth': 'Ruth',
        '1 Samuel': '1Sam', '1Sam': '1Sam', '1 Sam': '1Sam',
        '2 Samuel': '2Sam', '2Sam': '2Sam', '2 Sam': '2Sam',
        '1 Kings': '1Kgs', '1Kgs': '1Kgs', '1 Kings': '1Kgs',
        '2 Kings': '2Kgs', '2Kgs': '2Kgs', '2 Kings': '2Kgs',
        '1 Chronicles': '1Chr', '1Chr': '1Chr', '1 Chr': '1Chr',
        '2 Chronicles': '2Chr', '2Chr': '2Chr', '2 Chr': '2Chr',
        'Ezra': 'Ezra',
        'Nehemiah': 'Neh', 'Neh': 'Neh',
        'Esther': 'Esth', 'Esth': 'Esth',
        'Job': 'Job',
        'Psalms': 'Ps', 'Ps': 'Ps', 'Psalm': 'Ps',
        'Proverbs': 'Prov', 'Prov': 'Prov',
        'Ecclesiastes': 'Eccl', 'Eccl': 'Eccl',
        'Song of Solomon': 'Song', 'Song': 'Song',
        'Isaiah': 'Isa', 'Isa': 'Isa', 'Is': 'Isa',
        'Jeremiah': 'Jer', 'Jer': 'Jer',
        'Lamentations': 'Lam', 'Lam': 'Lam',
        'Ezekiel': 'Ezek', 'Ezek': 'Ezek',
        'Daniel': 'Dan', 'Dan': 'Dan',
        'Hosea': 'Hos', 'Hos': 'Hos',
        'Joel': 'Joel',
        'Amos': 'Amos',
        'Obadiah': 'Obad', 'Obad': 'Obad',
        'Jonah': 'Jonah',
        'Micah': 'Mic', 'Mic': 'Mic',
        'Nahum': 'Nah', 'Nah': 'Nah',
        'Habakkuk': 'Hab', 'Hab': 'Hab',
        'Zephaniah': 'Zeph', 'Zeph': 'Zeph',
        'Haggai': 'Hag', 'Hag': 'Hag',
        'Zechariah': 'Zech', 'Zech': 'Zech',
        'Malachi': 'Mal', 'Mal': 'Mal',
        
        # New Testament - Gospels
        'Matthew': 'Matt', 'Matt': 'Matt', 'Mt': 'Matt',
        'Mark': 'Mark', 'Mk': 'Mark',
        'Luke': 'Luke', 'Lk': 'Luke',
        'John': 'John', 'Jn': 'John',
        
        # NT - Acts and Epistles
        'Acts': 'Acts',
        'Romans': 'Rom', 'Rom': 'Rom',
        '1 Corinthians': '1Cor', '1 Cor': '1Cor', '1Cor': '1Cor',
        '2 Corinthians': '2Cor', '2 Cor': '2Cor', '2Cor': '2Cor',
        'Galatians': 'Gal', 'Gal': 'Gal',
        'Ephesians': 'Eph', 'Eph': 'Eph',
        'Philippians': 'Phil', 'Phil': 'Phil',
        'Colossians': 'Col', 'Col': 'Col',
        '1 Thessalonians': '1Thess', '1 Thess': '1Thess', '1Thess': '1Thess',
        '2 Thessalonians': '2Thess', '2 Thess': '2Thess', '2Thess': '2Thess',
        '1 Timothy': '1Tim', '1 Tim': '1Tim', '1Tim': '1Tim',
        '2 Timothy': '2Tim', '2 Tim': '2Tim', '2Tim': '2Tim',
        'Titus': 'Titus',
        'Philemon': 'Phlm', 'Phlm': 'Phlm',
        'Hebrews': 'Heb', 'Heb': 'Heb',
        'James': 'Jas', 'Jas': 'Jas',
        '1 Peter': '1Pet', '1 Pet': '1Pet', '1Pet': '1Pet',
        '2 Peter': '2Pet', '2 Pet': '2Pet', '2Pet': '2Pet',
        '1 John': '1John', '1 Jn': '1John', '1John': '1John',
        '2 John': '2John', '2 Jn': '2John', '2John': '2John',
        '3 John': '3John', '3 Jn': '3John', '3John': '3John',
        'Jude': 'Jude',
        'Revelation': 'Rev', 'Rev': 'Rev',
        
        # Special: Apostol is generic epistle marker (use context)
        'Apostol': 'Apostol',
    }
    
    def __init__(self, xml_path: str = 'rsv.xml'):
        """Initialize and load the RSV Bible XML"""
        self.xml_path = xml_path
        self.bible = self._load_bible()
    
    def _load_bible(self) -> Dict:
        """Load complete RSV Bible from XML into memory"""
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
    
    def _parse_pericope(self, pericope_ref: str) -> Optional[Dict]:
        """Parse pericope reference into components. Handles dot and colon formats."""
        # Normalize dots to colons
        pericope_ref = pericope_ref.replace('.', ':')
        
        # Pattern: "BookName Chapter:Verses"
        match = re.match(r'^([A-Za-z0-9 ]+)\s+(\d+):(.+)$', pericope_ref.strip())
        if not match:
            return None
        
        book_name = match.group(1).strip()
        chapter = match.group(2)
        verses_str = match.group(3).strip()
        
        # Map book name to OSIS ID
        book_id = self.BOOK_MAP.get(book_name)
        if not book_id:
            return None
        
        # Parse verse range
        verse_nums = self._parse_verse_range(verses_str)
        if not verse_nums:
            return None
        
        return {
            'book_id': book_id,
            'chapter': chapter,
            'verses': verse_nums
        }
    
    def _parse_verse_range(self, verses_str: str) -> List[int]:
        """Parse verse range string into list of verse numbers"""
        # Handle cross-chapter ranges like "5:22-6:2"
        # Simple verse parsing - treat cross-chapter as single chapter range
        verses_clean = re.sub(r'[a-zA-Z]', '', verses_str)
        parts = re.split(r'[,;]', verses_clean)
        all_verses = []
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            if '-' in part:
                try:
                    start_str, end_str = part.split('-', 1)
                    start = int(start_str.strip())
                    end = int(end_str.strip())
                    all_verses.extend(range(start, end + 1))
                except (ValueError, AttributeError):
                    continue
            else:
                try:
                    all_verses.append(int(part))
                except ValueError:
                    continue
        
        return all_verses
        
        # Standard verse parsing
        verses_clean = re.sub(r'[a-zA-Z]', '', verses_str)
        parts = re.split(r'[,;]', verses_clean)
        all_verses = []
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            if '-' in part:
                try:
                    start_str, end_str = part.split('-', 1)
                    start = int(start_str.strip())
                    end = int(end_str.strip())
                    all_verses.extend(range(start, end + 1))
                except (ValueError, AttributeError):
                    continue
            else:
                try:
                    all_verses.append(int(part))
                except ValueError:
                    continue
        
        return all_verses
    
    def extract_text(self, pericope_ref: str) -> Optional[str]:
        parsed = self._parse_pericope(pericope_ref)
        if not parsed:
            return None
        
        book_id = parsed['book_id']
        chapter = parsed['chapter']
        verses = parsed['verses']
        
        if book_id == 'Apostol':
            return f"[Epistle reading - specific book needed: {pericope_ref}]"
        
        if book_id not in self.bible or chapter not in self.bible[book_id]:
            return None
        
        chapter_data = self.bible[book_id][chapter]
        texts = []
        for verse_num in verses:
            verse_str = str(verse_num)
            if verse_str in chapter_data:
                texts.append(chapter_data[verse_str])
            else:
                texts.append(f'[Verse {verse_str} not found]')
        
        return ' '.join(texts)

if __name__ == '__main__':
    extractor = RSVExtractor()
    test_refs = [
        "Galatians 5.22-6.2",
        "Luke 13:18-29"
    ]
    for ref in test_refs:
        text = extractor.extract_text(ref)
        print(f"{ref}: {text[:100]}..." if text else "No text")