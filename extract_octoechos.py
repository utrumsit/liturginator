#!/usr/bin/env python3
"""
Octoechos Extractor

Extracts Vespers stichera and theotokia from Octoechos PDF.

Output: octoechos_stichera.json, octoechos_theotokia.json
"""

import pdfplumber
import json
import re

def extract_text_from_pdf(pdf_path):
    """Extract all text from PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def parse_stichera(text):
    """Parse stichera from text."""
    # Split by TONE sections
    tone_pattern = re.compile(r'TONE (\d+)', re.IGNORECASE)
    tone_sections = tone_pattern.split(text)[1:]  # Skip first empty

    octoechos = {}
    days = ["SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY"]

    for i in range(0, len(tone_sections), 2):
        tone_num = int(tone_sections[i])
        section = tone_sections[i+1]

        octoechos[tone_num] = {}

        for day in days:
            day_pattern = re.compile(rf'{day} VESPERS', re.IGNORECASE)
            day_match = day_pattern.search(section)
            if not day_match:
                continue

            # Find start of stichera
            start = day_match.end()
            # Find next day or end
            next_day = None
            for next_d in days[days.index(day.upper()) + 1:]:
                next_match = re.search(rf'{next_d} VESPERS', section[start:], re.IGNORECASE)
                if next_match:
                    next_day = next_match.start() + start
                    break
            if not next_day:
                next_day = len(section)

            day_text = section[start:next_day]

            # Extract stichera after "LORD I CALL..."
            lord_call = re.search(r'LORD I CALL', day_text, re.IGNORECASE)
            if not lord_call:
                continue

            stichera_text = day_text[lord_call.end():]

            # Split into stichera (assuming they are separated by blank lines or specific markers)
            # This is rough; may need refinement
            stichera = []
            parts = re.split(r'\n\s*\n', stichera_text.strip())
            for part in parts:
                part = part.strip()
                if len(part) > 50:  # Filter short parts
                    stichera.append(part)

            if stichera:
                octoechos[tone_num][day.lower()] = stichera[:3]  # Take first 3 as per plan

    return octoechos

def parse_theotokia(text):
    """Parse theotokia from text."""
    # Assume theotokia are at the end, after "THEOTOKIA" or similar
    theotokia_pattern = re.compile(r'THEOTOKIA', re.IGNORECASE)
    match = theotokia_pattern.search(text)
    if not match:
        return {}

    theotokia_text = text[match.end():]

    # Split by tone
    theotokia = {}
    tone_pattern = re.compile(r'Tone (\d+)', re.IGNORECASE)
    parts = tone_pattern.split(theotokia_text)[1:]

    for i in range(0, len(parts), 2):
        tone_num = int(parts[i])
        content = parts[i+1].strip()
        # Split into variants if any
        variants = re.split(r'\n\s*\n', content)
        theotokia[tone_num] = [v.strip() for v in variants if v.strip()]

    return theotokia

def main():
    pdf_path = "octoechos.pdf"
    text = extract_text_from_pdf(pdf_path)

    stichera = parse_stichera(text)
    theotokia = parse_theotokia(text)

    with open("octoechos_stichera.json", "w") as f:
        json.dump(stichera, f, indent=2)

    with open("octoechos_theotokia.json", "w") as f:
        json.dump(theotokia, f, indent=2)

    print("Extraction complete!")

if __name__ == "__main__":
    main()