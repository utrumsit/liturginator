#!/usr/bin/env python3
"""
Robust MCI lectionary parser - handles all weeks 1-36, Triodion/Lent/fixed, paramia/matins, merge lists/dicts.
"""
import json
import re
from collections import defaultdict

def slugify(text):
    text = re.sub(r'[^a-z0-9 ]', '', text.lower())
    return re.sub(r'\s+', '_', text.strip())

def parse_ref(ref):
    m = re.search(r'([A-Za-z\s]+?)\s*§?\d*\s*\((\d+):(.+)\)', ref)
    if m:
        return m.group(1).strip(), int(m.group(2)), m.group(3)
    return None, None, None

def main():
    with open('mci-lectionary.md', 'r') as f:
        lines = f.readlines()

    data = defaultdict(lambda: defaultdict(dict))
    current_section = None
    current_week = None
    current_day = None
    current_title = ''
    readings = []
    vespers_paramia = []
    matins_gospel = None
    feast_slug = ''
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        i += 1

        # Section
        m = re.search(r'\*\*(.+?)\*\*', line)
        if m:
            sec = m.group(1).strip().lower()
            if 'bright week' in sec:
                current_section = 'pascha'
            elif 'pentecostarion' in sec:
                current_section = 'pentecostarion'
            elif 'triodion' in sec:
                current_section = 'triodion'
            elif 'lent' in sec:
                current_section = 'lent'
            continue

        # Week
        m = re.search(r'\*\*(\d+)(?:ST|ND|RD|TH)\s+WEEK\s+(?:after\s+)?PENTECOST\*\*', line)
        if m and current_section == 'pentecostarion':
            current_week = m.group(1)
            continue

        # Fixed feast
        if 'feast' in line.lower() and re.search(r'\*\*(.+?)\*\*', line):
            feast_slug = slugify(m.group(1))
            current_section = 'fixed'
            current_title = m.group(1)
            continue

        # Day in table row
        day_m = re.search(r'\|.*?(\*?\s*(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\s*\*?)', line)
        if day_m:
            day_name = day_m.group(2)
            current_day = {'Sunday': '0', 'Monday': '1', 'Tuesday': '2', 'Wednesday': '3', 'Thursday': '4', 'Friday': '5', 'Saturday': '6'}[day_name]
            current_title = f"{day_name} of {current_week}th Week after Pentecost" if current_week else line
            continue

        # Readings table row
        if current_section and current_day and '|' in line:
            parts = [p.strip() for p in line.split('|') if p.strip()]
            for p in parts:
                book_e, ch_e, vs_e = parse_ref(p)
                if book_e:
                    readings.append({'type': 'epistle', 'book': book_e, 'chapter': ch_e, 'verses': vs_e, 'text': '', 'context': f'{book_e} {ch_e}:{vs_e}'})
                book_g, ch_g, vs_g = parse_ref(p)
                if book_g:
                    readings.append({'type': 'gospel', 'book': book_g, 'chapter': ch_g, 'verses': vs_g, 'text': '', 'context': f'{book_g} {ch_g}:{vs_g}'})

        # Paramia
        if '*Vespers Paramia:' in line:
            vespers_paramia = []
            while i < len(lines) and '*Matins' not in lines[i] and '*Vespers' not in lines[i]:
                m = re.search(r'\( \d+ \)\s*([A-Za-z\s]+?)\s*(\d+):(.+)', lines[i])
                if m:
                    book, ch, vs = m.group(1).strip(), int(m.group(2)), m.group(3)
                    vespers_paramia.append({'book': book, 'chapter': ch, 'verses': vs, 'text': '', 'context': f'{book} {ch}:{vs}'})
                i += 1
            i -= 1
            continue

        # Matins Gospel
        if '*Matins Gospel:' in line:
            m = re.search(r'([A-Za-z\s]+?)\s*§?\d*\s*\((\d+):(.+)\)', line)
            if m:
                book, ch, vs = m.group(1).strip(), int(m.group(2)), m.group(3)
                matins_gospel = {'book': book, 'chapter': ch, 'verses': vs, 'text': '', 'context': f'{book} {ch}:{vs}'}

        # Save
        if readings:
            entry = {'title': current_title, 'readings': readings}
            if vespers_paramia:
                entry['vespers_paramia'] = vespers_paramia
            if matins_gospel:
                entry['matins_gospel'] = matins_gospel

            if current_section == 'pascha':
                data['pascha'][current_day] = entry
            elif current_section == 'pentecostarion' and current_week:
                if current_week not in data['pentecostarion']:
                    data['pentecostarion'][current_week] = {}
                data['pentecostarion'][current_week][current_day] = entry
            elif current_section == 'fixed':
                data['fixed'][feast_slug] = entry
            # reset
            readings = []
            current_day = None

    # Merge with existing
    try:
        with open('scripture_readings.json', 'r') as f:
            existing = json.load(f)
    except:
        existing = {}

    for sec, weeks in data.items():
        if sec not in existing:
            existing[sec] = {}
        for w, days in weeks.items():
            if isinstance(days, dict):
                for d, entry in days.items():
                    if d in existing[sec]:
                        e = existing[sec][d]
                        if isinstance(e, list):
                            e = {'readings': e}
                        e['readings'] = entry.get('readings', e.get('readings', []))
                        e['vespers_paramia'] = entry.get('vespers_paramia', e.get('vespers_paramia', []))
                        e['matins_gospel'] = entry.get('matins_gospel', e.get('matins_gospel', {}))
                        e['title'] = entry.get('title', e.get('title', ''))
                    else:
                        existing[sec][d] = entry
                if w in existing[sec] and isinstance(existing[sec][w], dict):
                    for d in days:
                        existing[sec][w][d] = days[d]

    with open('scripture_readings.json', 'w') as f:
        json.dump(existing, f, indent=2)

if __name__ == '__main__':
    main()
