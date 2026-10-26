import json, re

with open("/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html") as f:
    lines = f.readlines()

line = lines[4353]
prefix = "const RISINGBRAIN_DATA = "
raw = line[len(prefix):].rstrip(";\n")
rb_data = json.loads(raw)

with open("extracted_dsa_data.json") as f:
    dsa_patterns = json.load(f)

dsa_problems = {}
for p in dsa_patterns:
    for prob in p.get("problems", []):
        dsa_problems[prob["n"]] = {
            "n": prob["n"],
            "t": prob["t"],
            "diff": prob["diff"],
            "l": prob.get("l", ""),
            "g": prob.get("g", ""),
            "pattern": p.get("name", "")
        }

rb_problems = {}
for topic in rb_data:
    for pat in topic.get("patterns", []):
        for prob in pat.get("problems", []):
            rb_problems[prob["n"]] = {
                "n": prob["n"],
                "t": prob["t"],
                "diff": prob["diff"],
                "l": prob.get("l", ""),
                "g": prob.get("g", ""),
                "ref": prob.get("ref", ""),
                "cross": prob.get("cross", {}),
                "pattern": pat.get("name", ""),
                "topic": topic.get("name", "")
            }

def get_lc_slug(url):
    if not url: return None
    m = re.search(r"leetcode\.com/problems/([^/?#]+)", url)
    return m.group(1).lower().strip() if m else None

def get_gfg_slug(url):
    if not url: return None
    m = re.search(r"geeksforgeeks\.org/problems/([^/?#]+)", url)
    return m.group(1).lower().strip() if m else None

def norm_title(t):
    t = re.sub(r"^\d+\.\s*", "", t)
    t = re.sub(r"^(problem challenge \d+:|challenge \d+:)", "", t, flags=re.IGNORECASE)
    t = re.sub(r"[^a-zA-Z0-9\s]", "", t).lower().strip()
    return re.sub(r"\s+", " ", t)

rb_by_lc = {}
rb_by_gfg = {}
rb_by_norm = {}

for n, p in rb_problems.items():
    lc = get_lc_slug(p["l"])
    if lc:
        rb_by_lc.setdefault(lc, []).append(p)
    gfg = get_gfg_slug(p["g"])
    if gfg:
        rb_by_gfg.setdefault(gfg, []).append(p)
    nt = norm_title(p["t"])
    if nt:
        rb_by_norm.setdefault(nt, []).append(p)

confirmed_matches = []
uncertain_matches = []
unmatched_dsa = []

for dn, dp in dsa_problems.items():
    dsa_lc = get_lc_slug(dp["l"])
    dsa_gfg = get_gfg_slug(dp["g"])
    dsa_nt = norm_title(dp["t"])
    
    # Priority 1: Match by LeetCode slug
    if dsa_lc and dsa_lc in rb_by_lc:
        matched_rb = rb_by_lc[dsa_lc]
        confirmed_matches.append({
            "dsa_num": dn,
            "dsa_title": dp["t"],
            "rb_num": matched_rb[0]["n"],
            "rb_title": matched_rb[0]["t"],
            "method": "leetcode_slug",
            "identifier": dsa_lc
        })
        continue

    # Priority 2: Match by GFG slug
    if dsa_gfg and dsa_gfg in rb_by_gfg:
        matched_rb = rb_by_gfg[dsa_gfg]
        confirmed_matches.append({
            "dsa_num": dn,
            "dsa_title": dp["t"],
            "rb_num": matched_rb[0]["n"],
            "rb_title": matched_rb[0]["t"],
            "method": "gfg_slug",
            "identifier": dsa_gfg
        })
        continue

    # Priority 3: Match by embedded cross reference if both have it
    embedded_match = None
    for rn, rp in rb_problems.items():
        cross_dsa = rp.get("cross", {}).get("dsa", {})
        if cross_dsa and cross_dsa.get("num") == dn:
            embedded_match = rp
            break
            
    if embedded_match:
        rb_n = embedded_match["n"]
        confirmed_matches.append({
            "dsa_num": dn,
            "dsa_title": dp["t"],
            "rb_num": rb_n,
            "rb_title": embedded_match["t"],
            "method": "embedded_cross_verified",
            "identifier": f"DSA #{dn} -> RB #{rb_n}"
        })
        continue

    # Priority 4: Match by exact normalized title (only if slug doesn't conflict)
    if dsa_nt in rb_by_norm:
        candidates = rb_by_norm[dsa_nt]
        if len(candidates) == 1:
            cand = candidates[0]
            cand_lc = get_lc_slug(cand["l"])
            if not dsa_lc or not cand_lc or dsa_lc == cand_lc:
                confirmed_matches.append({
                    "dsa_num": dn,
                    "dsa_title": dp["t"],
                    "rb_num": cand["n"],
                    "rb_title": cand["t"],
                    "method": "normalized_title",
                    "identifier": dsa_nt
                })
                continue
            else:
                uncertain_matches.append({
                    "dsa_num": dn,
                    "dsa_title": dp["t"],
                    "rb_num": cand["n"],
                    "rb_title": cand["t"],
                    "reason": f"Title matched ({dsa_nt}), but LC slugs differ ({dsa_lc} vs {cand_lc})"
                })
                continue

    # Priority 5: Collect uncertain fuzzy matches for manual review report
    fuzzy = []
    for nt, cands in rb_by_norm.items():
        if len(dsa_nt) > 5 and (dsa_nt in nt or nt in dsa_nt):
            for c in cands:
                fuzzy.append(c)
    if fuzzy:
        uncertain_matches.append({
            "dsa_num": dn,
            "dsa_title": dp["t"],
            "candidates": [{"rb_num": c["n"], "rb_title": c["t"]} for c in fuzzy],
            "reason": "Partial title similarity without canonical URL match"
        })
    else:
        unmatched_dsa.append({"dsa_num": dn, "dsa_title": dp["t"]})

print(f"Confirmed matches count: {len(confirmed_matches)}")
print(f"Uncertain matches count: {len(uncertain_matches)}")
print(f"Unmatched DSA count: {len(unmatched_dsa)}")

with open("dsa_rb_matches.json", "w") as f:
    json.dump({
        "confirmed": confirmed_matches,
        "uncertain": uncertain_matches,
        "unmatched": unmatched_dsa
    }, f, indent=2)
