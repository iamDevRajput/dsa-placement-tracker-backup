import json
import re
import os
import glob
from collections import defaultdict

CATALOG_PATH = "data/mik_catalog.json"
SCRATCH_DIR = "/Users/devrajput/.gemini/antigravity-ide/brain/5211636e-5599-42fd-8999-866a63b2edb4/scratch"

with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    catalog = json.load(f)

cat_by_id = {p["id"]: p for p in catalog}
cat_by_yt = {}
cat_by_lc = {}
def clean_title(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

cat_by_clean_title = {}
for p in catalog:
    cat_by_clean_title[clean_title(p["title"])] = p
    if p.get("youtube_url"):
        m = re.search(r'(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_\-]{11})', p["youtube_url"])
        if m: cat_by_yt[m.group(1)] = p
    if p.get("leetcode_url"):
        sm = re.search(r'leetcode\.com/problems/([^/]+)', p["leetcode_url"])
        if sm: cat_by_lc[sm.group(1).lower()] = p

# ==============================================================================
# 1. BUILD PLAYLISTS MANIFEST (data/mik_playlists.json & js)
# ==============================================================================
playlist_configs = [
    {
        "file": "bs_playlist.json",
        "id": "PLpIkg8OmuX-LkgtrEF7eyyYWJM3m5tVQY",
        "title": "Binary Search : Popular Interview Problems",
        "topic": "Arrays",
        "subtopic": "Binary Search",
        "description": "50 curated Binary Search problems asked at Google, Amazon, Microsoft, Meta."
    },
    {
        "file": "sliding_window_playlist.json",
        "id": "PLpIkg8OmuX-J2Ivo9YdY7bRDstPPTVGvN",
        "title": "Sliding Window : Popular Interview Problems",
        "topic": "Sliding Window",
        "subtopic": "General",
        "description": "Complete Sliding Window series covering fixed window, variable window, and frequency maps."
    },
    {
        "file": "backtracking_playlist.json",
        "id": "PLpIkg8OmuX-KJPC18SGiRUzJQAYo839ox",
        "title": "BACKTRACKING : Popular Interview Problems",
        "topic": "Backtracking",
        "subtopic": "General",
        "description": "25 comprehensive Backtracking problems covering subsets, permutations, and grid exploration."
    },
    {
        "file": "dp_playlist.json",
        "id": "PLpIkg8OmuX-JhFpkhgrAwZRtukO0SkwAt",
        "title": "DP Concepts & Qns : Convert Story To Code",
        "topic": "DP",
        "subtopic": "General",
        "description": "Dynamic Programming master series with intuition building and story-to-code conversions."
    },
    {
        "file": "graph_playlist.json",
        "id": "PLpIkg8OmuX-LZB9jYzbbZchk277H5CbdY",
        "title": "Graph Concepts & Qns : Convert Story To Code",
        "topic": "Graph",
        "subtopic": "General",
        "description": "Graph algorithms from BFS/DFS and Topological Sort to Dijkstra and Disjoint Set Union."
    },
    {
        "file": "hashmap_set_playlist.json",
        "id": "PLpIkg8OmuX-JVSpdssgeSsB5srSoNn55o",
        "title": "Hash Map/Set : Popular Interview Problems",
        "topic": "HashMap",
        "subtopic": "General",
        "description": "Hash Map and Hash Set interview problems and frequency map techniques."
    },
    {
        "file": "bit_manipulation_playlist.json",
        "id": "PLpIkg8OmuX-I-t2eiSxfO0UjiLhmNGfon",
        "title": "Bit-Manipulation (Popular Interview Problems)",
        "topic": "Bit_Magic",
        "subtopic": "General",
        "description": "Bit manipulation tricks, bitmasking, and bitwise operations."
    },
    {
        "file": "recursion_playlist.json",
        "id": "PLpIkg8OmuX-IXOgDP_YYiJFqfCFKFBDkO",
        "title": "RECURSION : Popular Interview Problems",
        "topic": "Recursion",
        "subtopic": "General",
        "description": "Foundational recursion and intuition building for interview problem solving."
    },
    {
        "file": "segment_tree_playlist.json",
        "id": "PLpIkg8OmuX-K1qUIQToCllUO0UIKXt8dB",
        "title": "Segment Tree Concepts and Questions",
        "topic": "Segment Tree",
        "subtopic": "General",
        "description": "Range queries, point updates, lazy propagation and segment tree templates."
    },
    {
        "file": "diff_array_playlist.json",
        "id": "PLpIkg8OmuX-Kqkb8DqDe_4-Tiav6ilS_L",
        "title": "Difference Array Technique: Concepts & Questions",
        "topic": "Arrays",
        "subtopic": "Difference Array Technique",
        "description": "O(1) range update techniques using difference arrays."
    },
    {
        "file": "line_sweep_playlist.json",
        "id": "PLpIkg8OmuX-IOG_-Bv92l-EhuBQX28LOm",
        "title": "Line Sweep Technique: Concepts & Questions",
        "topic": "Line Sweep Technique",
        "subtopic": "General",
        "description": "Interval overlapping and coordinate compression using line sweep."
    },
    {
        "file": "bst_playlist.json",
        "id": "PLpIkg8OmuX-JpV83mP-tNpMz3xsDiE-u1",
        "title": "Binary Search Tree (BST) (Popular Interview Problems)",
        "topic": "Tree",
        "subtopic": "BST",
        "description": "BST properties, validations, and search algorithms."
    },
    {
        "file": "design_playlist.json",
        "id": "PLpIkg8OmuX-JW5294URE-iwVhl_tdWEP5",
        "title": "Design Data Structure : Popular Interview Problems",
        "topic": "Design",
        "subtopic": "General",
        "description": "LRU, LFU, MinStack, and custom data structure designs."
    }
]

playlists_manifest = []

for cfg in playlist_configs:
    filepath = os.path.join(SCRATCH_DIR, cfg["file"])
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r", encoding="utf-8") as f:
        d = json.load(f)

    items = []
    def search_lockups(o):
        if isinstance(o, dict):
            if 'lockupViewModel' in o:
                items.append(o['lockupViewModel'])
            for v in o.values():
                search_lockups(v)
        elif isinstance(o, list):
            for x in o:
                search_lockups(x)
    search_lockups(d)

    videos = []
    unmatched = []

    for i, it in enumerate(items):
        cid = it.get('contentId')
        vtitle = it.get('metadata', {}).get('lockupMetadataViewModel', {}).get('title', {}).get('content', '')

        # 1. Match by exact YouTube ID
        matched_prob = cat_by_yt.get(cid)
        match_confidence = "exact_youtube_id" if matched_prob else None

        # 2. Secondary match by title / LC slug if not matched
        if not matched_prob:
            # clean title
            cleaned = clean_title(vtitle.split('|')[0].split('-')[0].strip())
            if cleaned in cat_by_clean_title:
                matched_prob = cat_by_clean_title[cleaned]
                match_confidence = "verified_title"

        # 3. Secondary match by LC number
        if not matched_prob:
            m_lc = re.search(r'Leetcode[- ]*(\d+)', vtitle, re.IGNORECASE)
            if m_lc:
                num = m_lc.group(1)
                for p in catalog:
                    if f'/{num}/' in p.get('leetcode_url', '') or p.get('leetcode_url', '').rstrip('/').endswith(f'-{num}'):
                        matched_prob = p
                        match_confidence = "verified_lc_number"
                        break

        v_obj = {
            "seq": i + 1,
            "video_id": cid,
            "video_title": vtitle,
            "video_url": f"https://www.youtube.com/watch?v={cid}",
            "problem_id": matched_prob["id"] if matched_prob else None,
            "problem_title": matched_prob["title"] if matched_prob else None,
            "practice_url": matched_prob["leetcode_url"] if matched_prob else "",
            "github_url": matched_prob["github_url"] if matched_prob else "",
            "match_confidence": match_confidence
        }

        videos.append(v_obj)
        if not matched_prob:
            unmatched.append({
                "seq": i + 1,
                "video_id": cid,
                "video_title": vtitle,
                "video_url": f"https://www.youtube.com/watch?v={cid}",
                "reason": "Video from playlist not mapped to existing catalog problem ID"
            })

    matched_count = len(videos) - len(unmatched)
    playlists_manifest.append({
        "id": cfg["id"],
        "title": cfg["title"],
        "topic": cfg["topic"],
        "subtopic": cfg["subtopic"],
        "description": cfg["description"],
        "total_videos": len(videos),
        "matched_count": matched_count,
        "unmatched_count": len(unmatched),
        "videos": videos,
        "unmatched_videos": unmatched
    })

print(f"Generated {len(playlists_manifest)} playlists.")
for pl in playlists_manifest:
    print(f"  {pl['title']}: {pl['matched_count']}/{pl['total_videos']} matched")

# Write mik_playlists.json & mik_playlists.js
with open("data/mik_playlists.json", "w", encoding="utf-8") as f:
    json.dump(playlists_manifest, f, indent=2)

with open("data/mik_playlists.js", "w", encoding="utf-8") as f:
    f.write("window.MIK_PLAYLISTS = " + json.dumps(playlists_manifest) + ";\n")

print("Saved data/mik_playlists.json and data/mik_playlists.js")
