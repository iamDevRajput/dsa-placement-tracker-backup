import json

with open("data/mik_catalog.json") as f:
    cat = json.load(f)
with open("data/mik_playlists.json") as f:
    pls = json.load(f)
with open("data/mik_learning_order.json") as f:
    lo = json.load(f)
with open("data/mik_patterns.json") as f:
    pat = json.load(f)

print(f"Catalog: {len(cat)} problems")
print(f"Playlists: {len(pls)} verified playlists")
print(f"Learning Roadmap: {len(lo)} stages")
print(f"Patterns: {len(pat)} patterns")
