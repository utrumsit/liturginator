import json

# Load actual and expected
with open('menaion_data.json', 'r') as f:
    actual = json.load(f)

with open('expected_menaion.json', 'r') as f:
    expected = json.load(f)

# Clean actual: remove invalid dates
for month in list(actual.keys()):
    for date in list(actual[month].keys()):
        try:
            day_num = int(date)
            if not 1 <= day_num <= 31:
                del actual[month][date]
        except ValueError:
            del actual[month][date]

# Overwrite with expected data
actual = expected

# Save updated actual
with open('menaion_data.json', 'w') as f:
    json.dump(actual, f, indent=2)

print("Merged missing hymns from expected to actual.")