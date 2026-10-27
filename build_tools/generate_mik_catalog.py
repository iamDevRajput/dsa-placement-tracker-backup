# MIK Interview DSA Catalog Generator
import os
import json
import re
import urllib.parse
from collections import defaultdict, Counter

SOURCE_REPO = "/Users/devrajput/.gemini/antigravity-ide/brain/5211636e-5599-42fd-8999-866a63b2edb4/scratch/Interview_DS_Algo"
TARGET_JSON_DIR = "/Users/devrajput/@Resources/Tracker/data"
TARGET_DASHBOARD_JSON_DIR = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/data"

def clean_url(url):
    if not url:
        return ""
    strip_chars = ".) ,;>'\""
    return url.strip().rstrip(strip_chars)

COMPANY_NORM_MAP = {
    'amazon': 'Amazon',
    'google': 'Google',
    'microsoft': 'Microsoft',
    'meta': 'Meta',
    'facebook': 'Meta',
    'apple': 'Apple',
    'uber': 'Uber',
    'adobe': 'Adobe',
    'flipkart': 'Flipkart',
    'samsung': 'Samsung',
    'accolite': 'Accolite',
    'makemytrip': 'MakeMyTrip',
    'goldman sachs': 'Goldman Sachs',
    'morgan stanley': 'Morgan Stanley',
    'paytm': 'Paytm',
    'twitter': 'Twitter',
    'linkedin': 'LinkedIn',
    'oracle': 'Oracle',
    'zoho': 'Zoho',
    'snapdeal': 'Snapdeal',
    'bloomberg': 'Bloomberg',
    'salesforce': 'Salesforce',
    'walmart': 'Walmart',
    'cisco': 'Cisco',
    'atlassian': 'Atlassian',
    'qualcomm': 'Qualcomm',
    'paypal': 'PayPal',
    'intuit': 'Intuit',
    'd.e. shaw': 'D.E. Shaw',
    'de shaw': 'D.E. Shaw',
    'oyo': 'OYO Rooms',
    'oyo rooms': 'OYO Rooms',
    'directi': 'Directi',
    'swiggy': 'Swiggy',
    'zomato': 'Zomato',
    'ebay': 'eBay'
}

def normalize_company(c):
    c = c.strip().rstrip('.')
    cl = c.lower()
    return COMPANY_NORM_MAP.get(cl, c)

def build_catalog():
    if not os.path.isdir(SOURCE_REPO):
        raise FileNotFoundError(f"Source repository not found at {SOURCE_REPO}")

    all_problems = []
    company_set = Counter()
    missing_problem_links = []
    missing_yt_links = []
    pid = 1

    for root, dirs, files in os.walk(SOURCE_REPO):
        if ".git" in root or "iPad PDF Notes" in root:
            continue
        rel = os.path.relpath(root, SOURCE_REPO)
        parts = rel.split(os.sep)
        topic = parts[0] if parts and parts[0] != "." else "General"
        subtopic = "/".join(parts[1:]) if len(parts) > 1 else "General"

        for f in sorted(files):
            if not f.endswith(".cpp"):
                continue
            fpath = os.path.join(root, f)
            relp = os.path.relpath(fpath, SOURCE_REPO)
            fname = os.path.basename(fpath)
            title = re.sub(r"\.cpp$", "", fname).strip()

            with open(fpath, "r", errors="ignore") as fp:
                content = fp.read()

            yt_m = re.search(r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=[a-zA-Z0-9_-]+|youtu\.be/[a-zA-Z0-9_-]+)', content)
            yt_url = clean_url(yt_m.group(0)) if yt_m else ""
            if yt_url and not yt_url.startswith("http"):
                yt_url = "https://" + yt_url

            lc_m = re.search(r'https?://(?:www\.)?leetcode\.com/problems/[a-zA-Z0-9_/-]+', content)
            lc_url = clean_url(lc_m.group(0)) if lc_m else ""

            gfg_m = re.search(r'https?://(?:www\.)?(?:practice\.)?geeksforgeeks\.org/[a-zA-Z0-9_/-]+', content)
            gfg_url = clean_url(gfg_m.group(0)) if gfg_m else ""

            other_url = ""
            if not lc_url and not gfg_url:
                m = re.search(r'(?:Leetcode Link|Link|Problem Link|Question Link)\s*:\s*(https?://[^\s\*\)\"]+)', content, re.I)
                if m:
                    other_url = clean_url(m.group(1))

            companies = []
            comp_m = re.search(r'Company Tags\s*:\s*([^\r\n*]+)', content, re.I)
            if comp_m:
                raw = comp_m.group(1).strip()
                low = raw.lower()
                if not any(x in low for x in ["will update", "let me know", "none", "n/a", "soon", ":-)", "coming"]):
                    for t in re.split(r'[,|/]+', raw):
                        ct = t.strip()
                        if ct and len(ct) > 1 and not ct.startswith("http") and not ct.lower().startswith("leetcode"):
                            norm_c = normalize_company(ct)
                            if norm_c not in companies:
                                companies.append(norm_c)
                                company_set[norm_c] += 1

            freq_m = re.search(r'Frequency\s*:\s*([^\r\n*]+)', content, re.I)
            freq = freq_m.group(1).strip() if freq_m else ""

            tc_m = re.search(r'(?:T\.C|Time Complexity)\s*[:=]\s*([^\r\n*/]+)', content, re.I)
            tc = tc_m.group(1).strip() if tc_m else ""

            sc_m = re.search(r'(?:S\.C|Space Complexity)\s*[:=]\s*([^\\r\n*/]+)', content, re.I)
            sc = sc_m.group(1).strip() if sc_m else ""

            apps = []
            app_ms = re.findall(r'//\s*(Approach\s*[-0-9:]+[^\r\n]+|Using\s+[^\r\n]+)', content, re.I)
            for a in app_ms[:3]:
                ca = a.strip()
                if len(ca) < 120 and ca not in apps:
                    apps.append(ca)

            encoded_parts = [urllib.parse.quote(part) for part in relp.split("/")]
            github_url = "https://github.com/MAZHARMIK/Interview_DS_Algo/blob/master/" + "/".join(encoded_parts)

            if not (lc_url or gfg_url or other_url):
                missing_problem_links.append(relp)
            if not yt_url:
                missing_yt_links.append(relp)

            item = {
                "id": f"mik_{pid:04d}",
                "n": pid,
                "title": title,
                "topic": topic,
                "subtopic": subtopic,
                "youtube_url": yt_url,
                "leetcode_url": lc_url,
                "gfg_url": gfg_url,
                "other_url": other_url,
                "companies": companies,
                "frequency": freq,
                "tc": tc,
                "sc": sc,
                "approaches": apps,
                "github_url": github_url,
                "relpath": relp
            }
            all_problems.append(item)
            pid += 1

    os.makedirs(TARGET_JSON_DIR, exist_ok=True)
    os.makedirs(TARGET_DASHBOARD_JSON_DIR, exist_ok=True)

    json_payload = json.dumps(all_problems, indent=2, ensure_ascii=False)
    js_payload = "window.MIK_CATALOG_DATA = " + json.dumps(all_problems, ensure_ascii=False) + ";\n"

    for d in [TARGET_JSON_DIR, TARGET_DASHBOARD_JSON_DIR]:
        json_path = os.path.join(d, "mik_catalog.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(json_payload)
        print(f"Wrote {json_path} ({len(json_payload)} bytes)")

        js_path = os.path.join(d, "mik_catalog.js")
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(js_payload)
        print(f"Wrote {js_path} ({len(js_payload)} bytes)")

    print(f"\nCatalog built successfully! Total problems: {len(all_problems)}")
    return all_problems

if __name__ == "__main__":
    build_catalog()
