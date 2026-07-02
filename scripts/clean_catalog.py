import json
from pathlib import Path

INPUT_FILE = Path("data/shl_catalog.json")
OUTPUT_FILE = Path("data/clean_catalog.json")

# Words that indicate NON-assessment pages
EXCLUDED_KEYWORDS = [
    "report",
    "guide",
    "ebook",
    "whitepaper",
    "article",
    "brochure",
    "overview",
    "solution",
    "services"
]

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

print(f"Loaded {len(catalog)} records")

cleaned = []

for item in catalog:

    name = item.get("name", "").strip()

    # Skip invalid names
    if not name:
        continue

    # Remove reports/articles/etc.
    if any(word in name.lower() for word in EXCLUDED_KEYWORDS):
        continue

    description = item.get("description", "").strip()

    duration = item.get("duration", "").strip()

    languages = item.get("languages") or []

    job_levels = item.get("job_levels") or []

    keys = item.get("keys") or []

    remote = item.get("remote", "no")

    adaptive = item.get("adaptive", "no")

    url = item.get("link", "").strip()

    # Create semantic search text
    search_text = " ".join([
        name,
        description,
        " ".join(keys),
        " ".join(job_levels),
        " ".join(languages),
    ]).lower()

    cleaned.append({
        "id": item.get("entity_id"),
        "name": name,
        "description": description,
        "duration": duration,
        "languages": languages,
        "job_levels": job_levels,
        "keys": keys,
        "remote": remote,
        "adaptive": adaptive,
        "url": url,
        "search_text": search_text
    })

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned, f, indent=4, ensure_ascii=False)

print(f"Cleaned catalog contains {len(cleaned)} assessments")
print(f"Saved to {OUTPUT_FILE}")