import re
import json

content = open('/Users/karlschudt/liturginator/mci-lectionary.md').read()
lines = content.split('\n')

days = {'Monday':0, 'Tuesday':1, 'Wednesday':2, 'Thursday':3, 'Friday':4, 'Saturday':5, 'Sunday':6}

def clean_ref(ref):
    ref = re.sub(r'§\d+', '', ref)
    ref = ref.replace('[', '(').replace(']', ')')
    ref = ' '.join(ref.split())
    return ref

pentecostarion = {}

week_starts = []
for i, line in enumerate(lines):
    if 'TH WEEK after PENTECOST' in line:
        match = re.search(r'(\d+)TH WEEK after PENTECOST', line)
        if match:
            num = int(match.group(1))
            if 1 <= num <= 36:
                week_starts.append((num, i))

week_starts.sort()

for idx, (week_num, start_idx) in enumerate(week_starts):
    end_idx = week_starts[idx+1][1] if idx+1 < len(week_starts) else len(lines)
    week_lines = lines[start_idx:end_idx]
    pentecostarion[str(week_num)] = {}
    for d in range(7):
        pentecostarion[str(week_num)][str(d)] = {'title': '', 'readings': [], 'matins_gospel': None}

    # parse table
    table_rows = []
    for line in week_lines:
        stripped = line.strip()
        if stripped.startswith('|'):
            table_rows.append(line)

    current_day = None
    for row in table_rows:
        parts = [p.strip() for p in row.split('|')[1:-1]]
        if not parts:
            continue
        day_str = parts[0]
        matins_set = False
        for p in parts:
            if p and 'Resurrectional Matins Gospel' in p:
                ref = p.split(':*')[1].strip()
                clean = clean_ref(ref)
                if current_day is not None:
                    pentecostarion[str(week_num)][str(current_day)]['matins_gospel'] = {'reference': clean}
                matins_set = True
                break
        if matins_set:
            continue
        if day_str.startswith('*') and day_str.endswith('*'):
            day_name = day_str[1:-1].strip()
            if day_name in days:
                current_day = days[day_name]
                if len(parts) > 1:
                    epistle = parts[1]
                    if epistle.startswith('**') and epistle.endswith('**'):
                        title = epistle[2:-2]
                        pentecostarion[str(week_num)][str(current_day)]['title'] = title
                        readings = []
                    else:
                        pentecostarion[str(week_num)][str(current_day)]['title'] = day_name
                        readings = []
                        if epistle:
                            readings.append({'epistle': clean_ref(epistle)})
                        if len(parts) > 2:
                            gospel = parts[2]
                            if gospel:
                                readings.append({'gospel': clean_ref(gospel)})
                    pentecostarion[str(week_num)][str(current_day)]['readings'] = readings
        elif current_day is not None and len(parts) >= 2:
            epistle = parts[0]
            gospel = parts[1] if len(parts) > 1 else ''
            if epistle:
                pentecostarion[str(week_num)][str(current_day)]['readings'].append({'epistle': clean_ref(epistle)})
            if gospel:
                pentecostarion[str(week_num)][str(current_day)]['readings'].append({'gospel': clean_ref(gospel)})

# set default titles
for week in pentecostarion:
    for day in pentecostarion[week]:
        if not pentecostarion[week][day]['title']:
            day_names = {v: k for k, v in days.items()}
            pentecostarion[week][day]['title'] = day_names[int(day)]

print(json.dumps({'pentecostarion': pentecostarion}, indent=2))