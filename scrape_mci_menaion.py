#!/usr/bin/env python3
"""
MCI Menaion Scraper

Scrapes hymn texts, service structure, and feast data from Metropolitan Cantor Institute
menaion pages (https://metropolitancantorinstitute.org/menaion/).

Extracts:
- Saint names and feast information
- Troparia and kontakia with tones
- Stichera (ordered arrays) for vespers/matins
- Prokeimena, Alleluia verses, communion hymns for liturgy
- Feast levels (inferred from rubrics)

Output: menaion_complete.json
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import date

BASE_URL = "https://metropolitancantorinstitute.org/menaion"

# Month name mapping for URL construction
MONTHS = {
    1: ("01", 31), 2: ("02", 29), 3: ("03", 31), 4: ("04", 30),
    5: ("05", 31), 6: ("06", 30), 7: ("07", 31), 8: ("08", 31),
    9: ("09", 30), 10: ("10", 31), 11: ("11", 30), 12: ("12", 31)
}


def infer_feast_level(soup, day_data):
    """
    Infer feast level from page content.
    
    Returns:
        int: Feast level 0-8
    """
    # Check for explicit "Day of Alleluia"
    text_content = soup.get_text()
    if "Day of Alleluia" in text_content:
        return 0
    
    # Check for feast image indicators
    imgs = soup.find_all('img')
    for img in imgs:
        alt = img.get('alt', '').lower()
        if 'great feast' in alt:
            return 6  # Great Feast minimum
        if 'vigil' in alt:
            return 5
        if 'polyeleos' in alt:
            return 4
    
    # Check for rubrics indicating feast rank
    if "eight stichera" in text_content.lower():
        # 8 stichera = polyeleos or vigil
        if day_data.get('vespers', {}).get('stichera_litija'):
            return 5  # Has litija = vigil rank
        return 4  # No litija = polyeleos
    
    if "six stichera" in text_content.lower():
        return 3  # Doxology rank
    
    # Default to ordinary
    return 0


def extract_tone_and_text(element):
    """
    Extract tone number and text from a hymn element.
    
    Returns:
        dict: {"tone": int, "melody": str or None, "text": str}
    """
    result = {"tone": None, "melody": None, "text": ""}
    
    # Find tone in strong tags
    strong_tags = element.find_all('strong')
    for strong in strong_tags:
        text = strong.get_text()
        tone_match = re.search(r'Tone (\d+)', text)
        if tone_match:
            result['tone'] = int(tone_match.group(1))
        
        # Check for special melody
        if 'melody' in text.lower():
            # Extract melody name from emphasis tag following
            next_elem = strong.find_next('emphasis')
            if next_elem:
                melody_text = next_elem.get_text().strip(' .')
                if melody_text:
                    result['melody'] = melody_text
    
    # Extract text content (everything after strong tags)
    text_parts = []
    for content in element.contents:
        if content.name != 'strong':
            if hasattr(content, 'get_text'):
                text_parts.append(content.get_text())
            elif isinstance(content, str):
                text_parts.append(content)
    
    result['text'] = ' '.join(text_parts).strip()
    return result


def scrape_day(month, day):
    """
    Scrape a single day's menaion page.
    
    Returns:
        dict: Day's complete data or None if page doesn't exist
    """
    url = f"{BASE_URL}/{month:02d}-{day:02d}.html"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 404:
            return None
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    day_data = {
        "saint": None,
        "feast_level": 0,
        "troparia": {},
        "kontakia": {},
        "vespers": {},
        "liturgy": {}
    }
    
    # Extract saint name from first blockquote
    blockquote = soup.find('blockquote')
    if blockquote:
        strong = blockquote.find('strong')
        if strong:
            saint_text = strong.get_text()
            # Remove feast indicators from saint name
            saint_text = re.sub(r'\s*\(.*?\)\s*$', '', saint_text)
            day_data['saint'] = saint_text.strip()
    
    # Extract troparia
    troparia = []
    for p in soup.find_all('p'):
        if 'Troparion' in p.get_text():
            trop_data = extract_tone_and_text(p)
            if trop_data['text']:
                troparia.append(trop_data)
    
    if troparia:
        day_data['troparia']['main'] = troparia[0]
        if len(troparia) > 1:
            day_data['troparia']['additional'] = troparia[1:]
    
    # Extract kontakia
    kontakia = []
    for p in soup.find_all('p'):
        text = p.get_text()
        if 'Kontakion' in text and 'Glory' in text:
            kont_data = extract_tone_and_text(p)
            if kont_data['text']:
                kontakia.append(kont_data)
    
    if kontakia:
        day_data['kontakia']['main'] = kontakia[0]
    
    # Extract stichera (need ordered arrays)
    stichera_lord_i_cried = []
    stichera_litija = []
    stichera_aposticha = []
    
    # Find vespers section
    vespers_heading = soup.find('h2', string=re.compile(r'At Vespers', re.I))
    if vespers_heading:
        # Get all paragraphs until next h2
        current = vespers_heading.find_next_sibling()
        while current and current.name != 'h2':
            if current.name == 'p':
                text = current.get_text()
                
                # Check for stichera sections
                if 'litija' in text.lower():
                    # Start collecting litija stichera
                    next_p = current.find_next_sibling('p')
                    while next_p and next_p.name == 'p' and 'Glory' not in next_p.get_text()[:20]:
                        stic = extract_tone_and_text(next_p)
                        if stic['text'] and len(stic['text']) > 50:
                            stichera_litija.append(stic)
                        next_p = next_p.find_next_sibling('p')
                
                elif 'aposticha' in text.lower():
                    # Start collecting aposticha stichera
                    next_p = current.find_next_sibling('p')
                    while next_p and next_p.name == 'p' and not re.match(r'^Troparion', next_p.get_text()):
                        # Check for verse marker
                        blockquote = next_p.find_previous_sibling('blockquote')
                        verse = blockquote.get_text().strip() if blockquote else None
                        
                        stic = extract_tone_and_text(next_p)
                        if stic['text'] and len(stic['text']) > 50:
                            if verse:
                                stic['verse'] = verse
                            stichera_aposticha.append(stic)
                        next_p = next_p.find_next_sibling('p')
                
                # Collect main stichera at "O Lord I have cried"
                elif current.find('strong') and 'Tone' in current.get_text():
                    stic = extract_tone_and_text(current)
                    if stic['text'] and len(stic['text']) > 50:
                        # Check if this is before litija section (i.e., main stichera)
                        if not stichera_litija and not stichera_aposticha:
                            stichera_lord_i_cried.append(stic)
            
            current = current.find_next_sibling()
    
    if stichera_lord_i_cried:
        day_data['vespers']['stichera_lord_i_cried'] = stichera_lord_i_cried
    if stichera_litija:
        day_data['vespers']['stichera_litija'] = stichera_litija
    if stichera_aposticha:
        day_data['vespers']['stichera_aposticha'] = stichera_aposticha
    
    # Extract liturgy elements
    liturgy_heading = soup.find('h2', string=re.compile(r'At the Divine Liturgy', re.I))
    if liturgy_heading:
        current = liturgy_heading.find_next_sibling()
        while current and current.name != 'h2':
            if current.name == 'p':
                text = current.get_text()
                
                # Prokeimenon
                if 'Prokeimenon' in text:
                    prok_match = re.search(r'Prokeimenon, Tone (\d+)', text)
                    if prok_match:
                        tone = int(prok_match.group(1))
                        # Extract text and verse
                        full_text = current.get_text()
                        parts = full_text.split('V.')
                        main_text = parts[0].split(').', 1)[-1].strip() if ').' in parts[0] else parts[0].split(':', 1)[-1].strip()
                        verse = parts[1].strip() if len(parts) > 1 else None
                        
                        day_data['liturgy']['prokeimenon'] = {
                            'tone': tone,
                            'text': main_text,
                            'verse': verse
                        }
                
                # Alleluia
                elif 'Alleluia' in text and 'Tone' in text:
                    all_match = re.search(r'Alleluia.*?Tone (\d+)', text)
                    if all_match:
                        tone = int(all_match.group(1))
                        verses = []
                        # Find V. markers for verses
                        verse_parts = text.split('V.')
                        for part in verse_parts[1:]:  # Skip first part before any V.
                            verse_text = part.strip()
                            if verse_text and not verse_text.startswith('Alleluia'):
                                verses.append(verse_text)
                        
                        day_data['liturgy']['alleluia'] = {
                            'tone': tone,
                            'verses': verses
                        }
                
                # Communion Hymn
                elif 'Communion Hymn' in text:
                    comm_text = text.split('Communion Hymn', 1)[-1]
                    # Extract psalm reference
                    ref_match = re.search(r'\(([^)]+)\)', comm_text)
                    reference = ref_match.group(1) if ref_match else None
                    
                    # Get main text (strip psalm ref and alleluias)
                    main_text = re.sub(r'\([^)]+\)', '', comm_text)
                    main_text = re.sub(r'Alleuia.*$', '', main_text, flags=re.IGNORECASE).strip()
                    
                    day_data['liturgy']['communion_hymn'] = {
                        'text': main_text,
                        'reference': reference
                    }
            
            current = current.find_next_sibling()
    
    # Infer feast level
    day_data['feast_level'] = infer_feast_level(soup, day_data)
    
    return day_data


def scrape_all_months():
    """
    Scrape all 12 months of the menaion.
    
    Returns:
        dict: Complete menaion organized by month/day
    """
    menaion = {}
    
    for month, (month_str, days) in MONTHS.items():
        print(f"\nScraping month {month}...")
        menaion[str(month)] = {}
        
        for day in range(1, days + 1):
            print(f"  Day {month}/{day}...", end=" ")
            
            day_data = scrape_day(month, day)
            
            if day_data:
                menaion[str(month)][str(day)] = day_data
                print(f"✓ {day_data.get('saint', 'Unknown')}")
            else:
                print("(no page)")
            
            # Be nice to the server
            time.sleep(0.5)
    
    return menaion


def main():
    """Main entry point."""
    print("MCI Menaion Scraper")
    print("=" * 50)
    print(f"Target: {BASE_URL}")
    print()
    
    # Scrape all data
    menaion = scrape_all_months()
    
    # Save to JSON
    output_file = "menaion_complete.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(menaion, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 50)
    print(f"Scraping complete! Saved to {output_file}")
    
    # Print summary statistics
    total_days = sum(len(days) for days in menaion.values())
    total_with_stichera = sum(
        1 for month_data in menaion.values()
        for day_data in month_data.values()
        if day_data.get('vespers', {}).get('stichera_lord_i_cried')
    )
    
    print(f"Total days scraped: {total_days}")
    print(f"Days with stichera: {total_with_stichera}")


if __name__ == "__main__":
    main()
