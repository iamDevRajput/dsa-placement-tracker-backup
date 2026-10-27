# Mirror sync and safe zip packaging
import os
import shutil
import zipfile
import hashlib

SOURCE_HTML = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"

TARGET_HTMLS = [
    "/Users/devrajput/@Resources/Tracker/index.html",
    "/Users/devrajput/@Resources/Tracker/integrated_master.html",
    "/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html",
    "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"
]

with open(SOURCE_HTML, "r", encoding="utf-8") as f:
    content = f.read()

source_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
print(f"Source HTML: {len(content)} bytes, SHA256: {source_hash[:16]}...")

for target in TARGET_HTMLS:
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Synced mirror: {target} ({len(content)} bytes)")

# Ensure data catalog files exist in both locations
CATALOG_SOURCES = [
    ("data/mik_catalog.json", "/Users/devrajput/@Resources/Tracker/data/mik_catalog.json", "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/data/mik_catalog.json"),
    ("data/mik_catalog.js", "/Users/devrajput/@Resources/Tracker/data/mik_catalog.js", "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/data/mik_catalog.js")
]

for rel, root_dest, dash_dest in CATALOG_SOURCES:
    if os.path.exists(dash_dest):
        shutil.copyfile(dash_dest, root_dest)
        print(f"Synced catalog: {root_dest} ({os.path.getsize(root_dest)} bytes)")

# Rebuild safe ZIP
DASHBOARD_DIR = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard"
ZIP_PATH = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard.zip"

ALLOWED_ZIP_FILES = [
    "index.html",
    "start-server.sh",
    "README.md",
    "manifest.json",
    "service-worker.js",
    "data/mik_catalog.js",
    "data/mik_catalog.json"
]

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for rel_path in ALLOWED_ZIP_FILES:
        full_p = os.path.join(DASHBOARD_DIR, rel_path)
        if os.path.exists(full_p):
            zipf.write(full_p, rel_path)
            print(f"Packaged into ZIP: {rel_path} ({os.path.getsize(full_p)} bytes)")
        else:
            print(f"Warning: {full_p} does not exist!")

print(f"\nFinal Offline ZIP built: {ZIP_PATH} ({os.path.getsize(ZIP_PATH)} bytes)")

# Verify ZIP integrity
with zipfile.ZipFile(ZIP_PATH, 'r') as zipf:
    namelist = zipf.namelist()
    print("ZIP contents verified:", namelist)
