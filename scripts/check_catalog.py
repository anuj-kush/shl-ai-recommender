import json

with open("data/clean_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total Assessments: {len(data)}")

print("\nFirst 5 Assessments:\n")

for item in data[:5]:
    print("=" * 80)
    for key, value in item.items():
        print(f"{key}: {value}")