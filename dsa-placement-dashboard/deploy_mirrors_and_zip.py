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

# Ensure data catalog and manifest files exist in both locations
CATALOG_SOURCES = [
    "mik_catalog.json",
    "mik_catalog.js",
    "mik_playlists.json",
    "mik_playlists.js",
    "mik_learning_order.json",
    "mik_learning_order.js",
    "mik_patterns.json",
    "mik_patterns.js"
]

for filename in CATALOG_SOURCES:
    dash_dest = os.path.join("/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/data", filename)
    root_dest = os.path.join("/Users/devrajput/@Resources/Tracker/data", filename)
    if os.path.exists(dash_dest):
        shutil.copyfile(dash_dest, root_dest)
        print(f"Synced data asset: {root_dest} ({os.path.getsize(root_dest)} bytes)")

# Rebuild safe ZIP without personal assets or unrelated files
DASHBOARD_DIR = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard"
ZIP_PATH = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard.zip"

ALLOWED_ZIP_FILES = [
    "index.html",
    "start-server.sh",
    "README.md",
    "manifest.json",
    "service-worker.js",
    "data/mik_catalog.js",
    "data/mik_catalog.json",
    "data/mik_playlists.js",
    "data/mik_playlists.json",
    "data/mik_learning_order.js",
    "data/mik_learning_order.json",
    "data/mik_patterns.js",
    "data/mik_patterns.json"
]

with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for rel_path in ALLOWED_ZIP_FILES:
        full_p = os.path.join(DASHBOARD_DIR, rel_path)
        if os.path.exists(full_p):
            zipf.write(full_p, rel_path)
            print(f"Packaged into ZIP: {rel_path} ({os.path.getsize(full_p)} bytes)")
        else:
            print(f"Notice: optional file {rel_path} not found.")

print(f"\nFinal Offline ZIP built: {ZIP_PATH} ({os.path.getsize(ZIP_PATH)} bytes)")

# Verify ZIP integrity
with zipfile.ZipFile(ZIP_PATH, 'r') as zipf:
    namelist = zipf.namelist()
    print("ZIP contents verified:", namelist)
    # Ensure no photo or backup files exist in ZIP
    for item in namelist:
        assert 'mummy_papa' not in item.lower(), f"Forbidden asset found in zip: {item}"
        assert 'backup' not in item.lower(), f"Forbidden asset found in zip: {item}"
        assert '.git' not in item.lower(), f"Forbidden asset found in zip: {item}"
print("ZIP privacy & security audit: PASSED ✓")
