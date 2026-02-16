import json
from pathlib import Path

p = Path(__file__).resolve().parent / "sample-data.json"

with open(p, "r", encoding="utf-8") as f:
    data = json.load(f)

print(data)
