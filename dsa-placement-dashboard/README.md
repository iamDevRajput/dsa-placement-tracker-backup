# 🚀 Placement Preparation Dashboard & Triple DSA Tracker

A self-contained, offline-first personal Placement Preparation Dashboard featuring three independent, fully isolated trackers:
1. **184 DSA Patterns**: 19 curated algorithmic patterns with spaced repetition.
2. **455 Striver A2Z Sheet**: 18 comprehensive steps from basics to advanced graphs & dynamic programming.
3. **385 RisingBrain Pattern Wise Sheet**: 17 topics, 68 patterns with problem strategy explanations, recognition clues, and 6-state progress tracking.

Engineered for **100% offline functionality**, **zero data loss**, **multi-tier storage safety (LocalStorage + IndexedDB + Rolling Snapshots)**, and seamless version updates.

---

## 🔒 Offline & Data Safety Guarantees

1. **100% Offline Independence**:
   - Zero external CDNs, scripts, or server runtimes required.
   - Built with local CSS, system-native font stacks, and embedded SVG icons.
   - All 184 DSA questions, 455 Striver questions, 385 RisingBrain questions with strategy & recognition clues, and 65 motivational lessons are bundled directly inside the file.
   - Launches instantly via double-click (`file://`) even when your computer has no internet access.

2. **StorageGuard Persistence Architecture**:
   - **DSA Patterns**: `dsa_placement_prep_v3`
   - **Striver Sheet**: `striver_a2z_tracker_v3`
   - **RisingBrain Sheet**: `risingbrain_tracker_v1`
   - **IndexedDB Replicas**: Continuously mirrors all progress to `PlacementTrackerDB` (`snapshots` store).
   - **Automatic Rolling Snapshots**: Keeps the last 5 state snapshots with timestamps (`prep_dashboard_snapshot_history`).
   - **Overwrite Guard**: Prevents empty memory states from overwriting non-empty browser storage.
   - **Startup Version Archiving**: Creates an emergency pre-upgrade snapshot whenever code is updated.

3. **Triple Independent Trackers**:
   - Modifying one tracker NEVER affects the progress of another.
   - Separate completion statistics, separate filters, and separate checkboxes.
   - Cross-reference badges link identical problems across sheets without merging records.

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
3. The dashboard will preview your solved problem counts for DSA Patterns, Striver Sheet, and RisingBrain before you confirm the restore.

### 3. 1-Click Clipboard Sync (Quick Transfer Between Files/Browsers)
1. In your existing dashboard, go to **Settings & Backup** and click **📋 Copy All Data Code**.
2. Open the new HTML file.
3. Paste the code into the text box and click **📥 Paste & Restore Data Code**.

---

## 📁 Package Contents
```
dsa-placement-dashboard/
├── index.html                   # Complete standalone application (Triple Tracker)
├── manifest.json                # PWA manifest
├── service-worker.js            # PWA offline cache service worker
├── start-server.sh              # 1-click local server launcher
└── README.md                    # Documentation & user manual
```
