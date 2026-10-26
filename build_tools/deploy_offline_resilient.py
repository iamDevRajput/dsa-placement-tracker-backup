import os, shutil, zipfile

source_path = "/Users/devrajput/.gemini/antigravity-ide/scratch/integrated_master.html"
with open(source_path, "r", encoding="utf-8") as f:
    content = f.read()

targets = [
    "/Users/devrajput/@Resources/Tracker/integrated_master.html",
    "/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html",
    "/Users/devrajput/@Resources/Tracker/index.html",
    "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"
]

for t in targets:
    os.makedirs(os.path.dirname(t), exist_ok=True)
    with open(t, "w", encoding="utf-8") as out:
        out.write(content)
    print(f"Deployed: {t} ({len(content)} bytes)")

# Update README with complete offline and backup/restore documentation
readme_text = """# 🚀 Placement Preparation Dashboard & Dual DSA Tracker

A self-contained personal Placement Preparation Dashboard featuring dual independent trackers: **184 DSA Patterns** and **455 Striver A2Z DSA Sheet**.

Engineered for **100% offline functionality**, **zero data loss**, **multi-tier storage safety (LocalStorage + IndexedDB + Rolling Snapshots)**, and seamless version updates.

---

## 🔒 Offline & Data Safety Guarantees

1. **100% Offline Independence**:
   - Zero external CDNs, scripts, or server runtimes required.
   - Built with local CSS, system-native font stacks, and embedded SVG icons.
   - All 184 DSA questions, 455 Striver questions, and 65 motivational lessons are bundled directly inside the file.
   - Launches instantly via double-click (`file://`) even when your computer has no internet access.

2. **StorageGuard Persistence Architecture**:
   - **Primary LocalStorage**: `dsa_placement_prep_v3` and `striver_a2z_tracker_v3`.
   - **IndexedDB Replicas**: Continuously mirrors all progress to `PlacementTrackerDB` for browser cache wipe protection.
   - **Automatic Rolling Snapshots**: Keeps the last 5 state snapshots with timestamps (`prep_dashboard_snapshot_history`).
   - **Overwrite Guard**: Prevents empty memory states from overwriting non-empty browser storage.
   - **Startup Version Archiving**: Creates an emergency pre-upgrade snapshot whenever code is updated.
   - **Visible Storage Error Banner**: Alerts you immediately if browser storage quota is ever exceeded.

3. **Dual Independent Trackers**:
   - **DSA Patterns**: 184 questions organized into 19 proven patterns.
   - **Striver Sheet**: 455 problems organized into 18 systematic steps with YouTube video and documentation badges.
   - Modifying one tracker NEVER affects the progress of the other.

---

## 🚀 How to Run Completely Offline

### Method 1: Double-Click Launch (Recommended - Zero Installation)
Double-click `integrated_master.html`, `index.html`, or `dsa_patterns_trackerfinal copy.html` in Chrome, Safari, Edge, Brave, or Firefox.
- Works offline out of the box.
- Bookmark the file in your browser (`Cmd + D` on Mac, `Ctrl + D` on Windows) for instant daily access.

### Method 2: Localhost Server / PWA Mode
To run with Service Worker caching and install as a standalone desktop app:
```bash
# Navigate to the project folder and launch:
cd /Users/devrajput/@Resources/Tracker/dsa-placement-dashboard
bash start-server.sh

# Or using Python directly:
python3 -m http.server 8000
```
Then navigate to `http://localhost:8000` and click the **Install App** button in your browser address bar.

---

## 💾 How to Backup, Restore & Sync Across Files

### 1. Manual JSON Export
1. Go to **Settings & Backup** in the sidebar.
2. Click **📥 Export All Data (JSON)**.
3. Save the timestamped `.json` file to your computer or cloud drive.

### 2. Manual JSON Import / Restore
1. In **Settings & Backup**, click **📤 Import Backup (JSON)**.
2. Select your `.json` file.
3. The dashboard will preview your solved problem counts and diary entries before you confirm the restore.

### 3. 1-Click Clipboard Sync (Quick Transfer Between Files/Browsers)
If you download a new version of the HTML file, move to another laptop, or switch browsers:
1. In your existing dashboard, go to **Settings & Backup** and click **📋 Copy All Data Code**.
2. Open the new HTML file.
3. Paste the code into the text box and click **📥 Paste & Restore Data Code**.
All your progress, revision timelines, diary entries, and settings will appear instantly!

### 4. Rollback to an Automatic Snapshot
If you ever make an accidental change or want to revert:
1. Go to **Settings & Backup** -> **Automatic Snapshots & Rollback**.
2. Inspect the timestamps in the snapshot history list.
3. Click **🔄 Rollback to Latest Snapshot**.

---

## 📁 Package Contents
```
dsa-placement-dashboard/
├── index.html                   # Complete standalone application
├── manifest.json                # PWA manifest
├── service-worker.js            # PWA offline cache service worker
├── start-server.sh              # 1-click local server launcher
└── README.md                    # Documentation & user manual
```
"""

readme_targets = [
    "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/README.md",
    "/Users/devrajput/@Resources/Tracker/README.md"
]
for rt in readme_targets:
    with open(rt, "w", encoding="utf-8") as out:
        out.write(readme_text)
    print(f"Updated: {rt}")

# Rebuild ZIP (Safe whitelist, never include private assets)
proj_dir = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard"
zip_path = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard.zip"
allowed_files = ["index.html", "start-server.sh", "README.md", "manifest.json", "service-worker.js"]
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for fname in allowed_files:
        fpath = os.path.join(proj_dir, fname)
        if os.path.exists(fpath):
            zipf.write(fpath, fname)

print(f"Rebuilt ZIP Archive: {zip_path} ({os.path.getsize(zip_path)} bytes)")
