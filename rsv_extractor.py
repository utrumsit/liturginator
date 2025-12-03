#!/usr/bin/env python3
"""
RSV Text Extractor
Parses pericope references (e.g., "Luke 10.19-21") and extracts actual verse text from rsv.xml
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional

class RSVExtractor:
    """Extract RSV verse text from rsv.xml based on pericope references"""
    
    # Book name mapping (various formats -> OSIS book IDs)
    BOOK_MAP = {
        # Old Testament
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
                                    # Get complete verse text including nested elements
                                    full_text = ''.join(verse_elem.itertext()).strip()
                                    bible[book_id][chapter_num][verse_num] = full_text
        
        return bible
    
    def _parse_pericope(self, pericope_ref: str) -> Optional[Dict]:
        """
        Parse pericope reference into components
        Examples:
            "Luke 10.19-21" -> {book: 'Luke', chapter: 10, verses: [19,20,21]}
            "Galatians 1.3-10" -> {book: 'Gal', chapter: 1, verses: [3,4,5,6,7,8,9,10]}
            "Matthew 2.1-12" -> {book: 'Matt', chapter: 2, verses: [1..12]}
            "John 1.1" -> {book: 'John', chapter: 1, verses: [1]}
        """
        # Pattern: "BookName Chapter.Verses"
        # Verses can be: "1", "1-5", "1,3,5", "1-5,7-9", etc.
        match = re.match(r'^([A-Za-z0-9 ]+)\s+(\d+)\.(.+)$', pericope_ref.strip())
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
        """
        Parse verse range string into list of verse numbers
        Examples:
            "1" -> [1]
            "1-5" -> [1,2,3,4,5]
            "1,3,5" -> [1,3,5]
            "1-5,7-9" -> [1,2,3,4,5,7,8,9]
            "19-21" -> [19,20,21]
        """
        # Remove letters (e.g., "43a" -> "43")
        verses_clean = re.sub(r'[a-zA-Z]', '', verses_str)
        
        # Split by comma or semicolon
        parts = re.split(r'[,;]', verses_clean)
        all_verses = []
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            if '-' in part:
                # Range: "1-5"
                try:
                    start_str, end_str = part.split('-', 1)
                    start = int(start_str.strip())
                    end = int(end_str.strip())
                    all_verses.extend(range(start, end + 1))
                except (ValueError, AttributeError):
                    continue
            else:
                # Single verse: "1"
                try:
                    all_verses.append(int(part))
                except ValueError:
                    continue
        
        return all_verses
    
    def extract_text(self, pericope_ref: str) -> Optional[str]:
        """
        Extract RSV text for a given pericope reference.
        Supports multi-passage references separated by commas.
        
        Examples:
            "Luke 10.19-21" -> single passage
            "1 Timothy 1.18-20, 2.8-15" -> two passages from same book
        
        Returns: full text of verses joined together, or None if not found
        """
        # Check if this is a multi-passage reference (contains comma between chapter.verse patterns)
        # Pattern matches: "1.18-20, 2.8" or "1.18, 2.8-15" etc.
        if ', ' in pericope_ref and re.search(r'\d+\.[\d-]+,\s*\d+\.', pericope_ref):
            # Multi-passage reference like "1 Timothy 1.18-20, 2.8-15"
            # Extract book name from first part
            first_part = pericope_ref.split(',')[0].strip()
            match = re.match(r'^([A-Za-z0-9 ]+)\s+\d+\.', first_part)
            if match:
                book_name = match.group(1).strip()
                # Split into individual passages
                parts = pericope_ref.split(',')
                all_texts = []
                
                for i, part in enumerate(parts):
                    part = part.strip()
                    # First part has full book name, subsequent parts just have chapter.verses
                    if i == 0:
                        full_ref = part
                    else:
                        # Prepend book name to subsequent passages
                        full_ref = f"{book_name} {part}"
                    
                    # Extract this passage
                    passage_text = self._extract_single_passage(full_ref)
                    if passage_text:
                        all_texts.append(passage_text)
                
                return '\n\n'.join(all_texts) if all_texts else None
        
        # Single passage
        return self._extract_single_passage(pericope_ref)
    
    def _extract_single_passage(self, pericope_ref: str) -> Optional[str]:
        """
        Extract RSV text for a single passage reference.
        Helper method for extract_text().
        """
        parsed = self._parse_pericope(pericope_ref)
        if not parsed:
            return None
        
        book_id = parsed['book_id']
        chapter = parsed['chapter']
        verses = parsed['verses']
        
        # Special case: "Apostol" without specific book
        if book_id == 'Apostol':
            return f"[Epistle reading - specific book needed: {pericope_ref}]"
        
        # Look up in bible
        if book_id not in self.bible:
            return None
        
        if chapter not in self.bible[book_id]:
            return None
        
        chapter_data = self.bible[book_id][chapter]
        
        # Collect verse texts
        texts = []
        for verse_num in verses:
            verse_str = str(verse_num)
            if verse_str in chapter_data:
                texts.append(chapter_data[verse_str])
            else:
                texts.append(f'[Verse {verse_str} not found]')
        
        return ' '.join(texts)
    
    def extract_with_metadata(self, pericope_ref: str) -> Dict:
        """
        Extract text with metadata
        Returns: {
            'reference': 'Luke 10.19-21',
            'text': '...',
            'book': 'Luke',
            'chapter': 10,
            'verses': [19, 20, 21]
        }
        """
        parsed = self._parse_pericope(pericope_ref)
        if not parsed:
            return {
                'reference': pericope_ref,
                'text': None,
                'error': 'Could not parse pericope reference'
            }
        
        text = self.extract_text(pericope_ref)
        
        return {
            'reference': pericope_ref,
            'text': text,
            'book': parsed['book_id'],
            'chapter': int(parsed['chapter']),
            'verses': parsed['verses']
        }


def main():
    """Test the extractor"""
    import sys
    
    extractor = RSVExtractor()
    
    # Test cases
    test_refs = [
        "Luke 10.19-21",
        "Galatians 1.3-10",
        "Matthew 2.1-12",
        "John 1.1",
        "Romans 1.1-7"
    ]
    
    if len(sys.argv) > 1:
        # Extract specific reference from command line
        ref = ' '.join(sys.argv[1:])
        result = extractor.extract_with_metadata(ref)
        print(f"\nReference: {result['reference']}")
        if result.get('text'):
            print(f"Text: {result['text'][:200]}..." if len(result['text']) > 200 else f"Text: {result['text']}")
        else:
            print(f"Error: {result.get('error', 'Text not found')}")
    else:
        # Run test cases
        print("Testing RSV Extractor\n" + "="*60)
        for ref in test_refs:
            result = extractor.extract_with_metadata(ref)
            print(f"\n{ref}")
            print("-" * 60)
            if result.get('text'):
                text_preview = result['text'][:150] + "..." if len(result['text']) > 150 else result['text']
                print(f"{text_preview}")
            else:
                print(f"ERROR: {result.get('error', 'Not found')}")


if __name__ == '__main__':
    main()
