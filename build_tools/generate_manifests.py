import json, re, os, glob
from collections import defaultdict

CATALOG_PATH = "data/mik_catalog.json"
SCRATCH_DIR = "/Users/devrajput/.gemini/antigravity-ide/brain/5211636e-5599-42fd-8999-866a63b2edb4/scratch"
REPO_DIR = f"{SCRATCH_DIR}/Interview_DS_Algo"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Lookup maps
cat_by_id = {p["id"]: p for p in catalog}
cat_by_yt = {}
cat_by_lc = {}
cat_by_title_clean = {}

def clean_title(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

for p in catalog:
    if p.get("youtube_url"):
        m = re.search(r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_\-]{11})', p["youtube_url"])
        if m:
            cat_by_yt[m.group(1)] = p
    if p.get("leetcode_url"):
        slug_m = re.search(r'leetcode\.com/problems/([^/]+)', p["leetcode_url"])
        if slug_m:
            cat_by_lc[slug_m.group(1).lower()] = p
    cat_by_title_clean[clean_title(p["title"])] = p

print(f"Loaded {len(catalog)} problems. Indexed {len(cat_by_yt)} YT links, {len(cat_by_lc)} LC links.")
