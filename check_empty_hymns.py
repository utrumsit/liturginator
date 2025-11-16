import json

# Load menaion_data.json
with open('menaion_data.json', 'r') as f:
    data = json.load(f)

print("Dates with empty troparia or kontakia:")
for month in data:
    for date in data[month]:
        feast = data[month][date]
        troparia = feast.get('troparia', {})
        kontakia = feast.get('kontakia', {})
        if not troparia and not kontakia:
            print(f"{month} {date}: No hymns at all")
        elif not troparia:
            print(f"{month} {date}: Empty troparia")
        elif not kontakia:
            print(f"{month} {date}: Empty kontakia")

print("Check these against chasoslov.md to see if hymns are missing.")