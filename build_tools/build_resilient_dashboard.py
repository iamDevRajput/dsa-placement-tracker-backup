import json, os, subprocess

# 1. Read base files
with open("/Users/devrajput/.gemini/antigravity-ide/scratch/integrated_master.html", "r", encoding="utf-8") as f:
    html = f.read()

# 2. Make Google Fonts non-blocking and add robust system font stack
# Replace Google Fonts link with media="print" onload="this.media='all'" plus fallback
old_fonts_link = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@500;600;700;800&display=swap" rel="stylesheet">'
new_fonts_link = '<!-- Fonts: Non-blocking with system font fallbacks for 100% offline startup -->\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@500;600;700;800&display=swap" media="print" onload="this.media=\'all\'">\n<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Syne:wght@500;600;700;800&display=swap"></noscript>'

if old_fonts_link in html:
    html = html.replace(old_fonts_link, new_fonts_link, 1)

# Ensure font variables have optimal fallback stacks
old_font_heading = "--font-heading: 'Syne', -apple-system, BlinkMacSystemFont, sans-serif;"
new_font_heading = "--font-heading: 'Syne', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;"
html = html.replace(old_font_heading, new_font_heading, 1)

old_font_mono = "--font-mono: 'Space Mono', monospace;"
new_font_mono = "--font-mono: 'Space Mono', SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;"
html = html.replace(old_font_mono, new_font_mono, 1)

old_font_body = "--font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;"
new_font_body = "--font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;"
html = html.replace(old_font_body, new_font_body, 1)

# 3. Add Top Storage Alert Banner markup (hidden by default) right inside <body>
banner_html = """
<!-- STORAGE INTEGRITY & OFFLINE SAFETY BANNER -->
<div id="storageAlertBanner" style="display:none; position:fixed; top:0; left:0; right:0; z-index:999999; background:linear-gradient(90deg, #dc2626, #b91c1c); color:#ffffff; padding:0.6rem 1rem; font-family:var(--font-body); font-size:13px; font-weight:600; text-align:center; box-shadow:0 4px 15px rgba(0,0,0,0.5); align-items:center; justify-content:center; gap:0.75rem;">
  <span id="storageAlertMessage">⚠️ Storage Alert: Your browser storage write failed. Your progress could not be saved to localStorage.</span>
  <button class="btn btn-secondary" onclick="exportCompleteBackup()" style="padding:0.25rem 0.6rem; font-size:11px; background:#fff; color:#b91c1c; border:none; font-weight:700;">📥 Emergency Download Backup</button>
  <button onclick="document.getElementById('storageAlertBanner').style.display='none'" style="background:transparent; border:none; color:#fff; font-size:16px; cursor:pointer; margin-left:0.5rem;">✕</button>
</div>
"""
if "id=\"storageAlertBanner\"" not in html:
    html = html.replace("<body>", "<body>\n" + banner_html, 1)

# 4. Add "Snapshots & Rollback" and "Clipboard Quick Sync" in Settings view
settings_enhancement = """      <div class="settings-group">
        <h3 style="font-family:var(--font-heading); font-size:18px; margin-bottom:1rem;">🛡️ Automatic Snapshots & Rollback</h3>
        <div class="settings-card">
          <div style="font-weight:600; font-size:14px; margin-bottom:0.25rem;">Multi-Tier Recovery System</div>
          <p style="font-size:12.5px; color:var(--text-muted); margin-bottom:1rem;">The dashboard continuously saves rolling snapshots in both <b>LocalStorage</b> and <b>IndexedDB</b>. If you ever update the code, switch browsers, or make an accidental change, you can instantly rollback or inspect your previous snapshots.</p>
          <div style="display:flex; gap:0.75rem; flex-wrap:wrap; margin-bottom:1rem;">
            <button class="btn btn-secondary" onclick="restoreLatestSnapshotUI()">🔄 Rollback to Latest Snapshot</button>
            <button class="btn btn-secondary" onclick="exportCompleteBackup()">📥 Download JSON Backup</button>
          </div>
          <div id="snapshotHistoryList" style="font-family:var(--font-mono); font-size:11.5px; color:var(--text-dim); background:var(--surface2); padding:0.75rem; border-radius:6px; border:1px solid var(--border-subtle); max-height:120px; overflow-y:auto;">
            <!-- Rendered dynamically -->
          </div>
        </div>
      </div>

      <div class="settings-group">
        <h3 style="font-family:var(--font-heading); font-size:18px; margin-bottom:1rem;">📋 1-Click Clipboard Sync (Cross-Browser / File Transfer)</h3>
        <div class="settings-card">
          <div style="font-weight:600; font-size:14px; margin-bottom:0.25rem;">Move Progress Between Files or Browsers</div>
          <p style="font-size:12.5px; color:var(--text-muted); margin-bottom:0.75rem;">If you downloaded a new HTML file or opened the app in a different browser, transfer your entire progress in 1 second without needing a file upload:</p>
          <div style="display:flex; gap:0.5rem; flex-wrap:wrap; margin-bottom:0.75rem;">
            <button class="btn btn-secondary" onclick="copyStateToClipboard()">📋 Copy All Data Code</button>
            <button class="btn btn-primary" onclick="pasteStateFromInput()">📥 Paste & Restore Data Code</button>
          </div>
          <textarea id="syncDataTextarea" class="form-textarea" placeholder="Paste your exported JSON or data code here to instantly restore progress..." style="min-height:70px; font-family:var(--font-mono); font-size:11px;"></textarea>
        </div>
      </div>
"""

# Insert before Danger Zone in Settings
dz_pos = html.find('<div class="settings-group">\n        <h3 style="font-family:var(--font-heading); font-size:18px; margin-bottom:1rem; color:#ef4444;">⚠️ Danger Zone</h3>')
if dz_pos != -1 and "restoreLatestSnapshotUI()" not in html:
    html = html[:dz_pos] + settings_enhancement + "\n" + html[dz_pos:]

# 5. Inject StorageGuard & IndexedDB & Safe Persistence System into <script>
storage_guard_js = """
/* ==========================================================================
   STORAGEGUARD & OFFLINE RESILIENCE ARCHITECTURE
   ========================================================================== */
const APP_BUILD_VERSION = '2026.10.25-offline-v4';
const SNAPSHOT_LATEST_KEY = 'prep_dashboard_snapshot_latest';
const SNAPSHOT_HISTORY_KEY = 'prep_dashboard_snapshot_history';
const SNAPSHOT_STARTUP_KEY = 'prep_dashboard_snapshot_startup';
const IDB_NAME = 'PlacementTrackerDB';
const IDB_STORE = 'snapshots';

let idbDatabase = null;

// Initialize IndexedDB mirror for high-quota offline persistence
function initIndexedDB() {
  if (!window.indexedDB) return;
  try {
    const req = indexedDB.open(IDB_NAME, 1);
    req.onupgradeneeded = function(e) {
      const db = e.target.result;
      if (!db.objectStoreNames.contains(IDB_STORE)) {
        db.createObjectStore(IDB_STORE, { keyPath: 'key' });
      }
    };
    req.onsuccess = function(e) {
      idbDatabase = e.target.result;
      mirrorToIndexedDB();
    };
    req.onerror = function(e) {
      console.warn('IndexedDB unavailable, continuing with LocalStorage:', e);
    };
  } catch(err) {
    console.warn('IndexedDB init error:', err);
  }
}

function mirrorToIndexedDB() {
  if (!idbDatabase) return;
  try {
    const tx = idbDatabase.transaction([IDB_STORE], 'readwrite');
    const store = tx.objectStore(IDB_STORE);
    const bundle = buildCompleteExportObject();
    store.put({ key: 'current_state', data: bundle, updatedAt: Date.now() });
    store.put({ key: 'backup_' + getTodayKey(), data: bundle, updatedAt: Date.now() });
  } catch(e) {
    console.warn('IDB write note:', e);
  }
}

// Show visible error banner if storage ever fails
function showStorageAlert(msg) {
  const banner = document.getElementById('storageAlertBanner');
  const msgEl = document.getElementById('storageAlertMessage');
  if (banner && msgEl) {
    msgEl.textContent = '⚠️ ' + msg;
    banner.style.display = 'flex';
  } else {
    alert('Storage Alert: ' + msg);
  }
}

function hideStorageAlert() {
  const banner = document.getElementById('storageAlertBanner');
  if (banner) banner.style.display = 'none';
}

// Build complete bundled state object for backups, sync, and snapshots
function buildCompleteExportObject() {
  return {
    version: 4,
    appBuildVersion: APP_BUILD_VERSION,
    exportedAt: new Date().toISOString(),
    dsaState: state,
    striverState: striverState,
    diaryState: diaryState,
    plannerState: plannerState,
    studyState: studyState,
    settingsState: settingsState
  };
}

// Save rolling snapshots in LocalStorage with overwrite guard
function recordSnapshot(reason = 'auto') {
  try {
    const bundle = buildCompleteExportObject();
    const str = JSON.stringify(bundle);
    localStorage.setItem(SNAPSHOT_LATEST_KEY, str);

    // Maintain history of last 5 snapshots
    let hist = [];
    try {
      const rawHist = localStorage.getItem(SNAPSHOT_HISTORY_KEY);
      if (rawHist) hist = JSON.parse(rawHist) || [];
    } catch(e) {}

    const now = new Date();
    const timeStr = `${now.toLocaleDateString()} ${now.toLocaleTimeString()}`;
    const dsaDone = Object.values(state.problems).filter(p => p.done).length;
    const striverDone = Object.values(striverState.problems).filter(p => p.done).length;

    hist.unshift({
      timestamp: Date.now(),
      timeStr: timeStr,
      reason: reason,
      dsaSolved: dsaDone,
      striverSolved: striverDone
    });

    if (hist.length > 5) hist = hist.slice(0, 5);
    localStorage.setItem(SNAPSHOT_HISTORY_KEY, JSON.stringify(hist));

    renderSnapshotHistoryUI();
    mirrorToIndexedDB();
    hideStorageAlert();
  } catch(err) {
    console.error('Snapshot error:', err);
    showStorageAlert('Browser storage write failed. Click "Emergency Download Backup" to keep your data safe.');
  }
}

function renderSnapshotHistoryUI() {
  const container = document.getElementById('snapshotHistoryList');
  if (!container) return;
  try {
    const rawHist = localStorage.getItem(SNAPSHOT_HISTORY_KEY);
    const hist = rawHist ? JSON.parse(rawHist) : [];
    if (!hist || hist.length === 0) {
      container.innerHTML = '<div>No previous snapshots recorded yet.</div>';
      return;
    }
    let h = '';
    hist.forEach((s, idx) => {
      h += `<div style="padding:4px 0; border-bottom:1px solid rgba(255,255,255,0.06);">
        <b>#${idx + 1} [${s.timeStr}]</b> · ${s.reason} · DSA: <span style="color:var(--accent3);">${s.dsaSolved}</span> · Striver: <span style="color:var(--accent4);">${s.striverSolved}</span>
      </div>`;
    });
    container.innerHTML = h;
  } catch(e) {}
}

function restoreLatestSnapshotUI() {
  try {
    const raw = localStorage.getItem(SNAPSHOT_LATEST_KEY);
    if (!raw) {
      alert('No previous snapshot found in this browser storage.');
      return;
    }
    const parsed = JSON.parse(raw);
    if (confirm(`Restore previous snapshot from ${parsed.exportedAt || 'earlier'}?`)) {
      applyImportData(parsed);
      showToast('Successfully restored state from latest snapshot!');
    }
  } catch(e) {
    alert('Could not restore snapshot: ' + e.message);
  }
}

function copyStateToClipboard() {
  try {
    const bundle = buildCompleteExportObject();
    const str = JSON.stringify(bundle);
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(str).then(() => {
        showToast('All progress copied to clipboard! You can paste it into any other file or browser.');
      }).catch(() => fallbackCopy(str));
    } else {
      fallbackCopy(str);
    }
  } catch(e) {
    alert('Copy error: ' + e.message);
  }
}

function fallbackCopy(text) {
  const ta = document.getElementById('syncDataTextarea');
  if (ta) {
    ta.value = text;
    ta.select();
    document.execCommand('copy');
    showToast('All progress copied to textarea and clipboard!');
  }
}

function pasteStateFromInput() {
  const ta = document.getElementById('syncDataTextarea');
  const val = (ta ? ta.value : '').trim();
  if (!val) {
    alert('Please paste your JSON or data code into the box first.');
    return;
  }
  try {
    const parsed = JSON.parse(val);
    applyImportData(parsed);
    showToast('Successfully restored all progress from pasted code!');
    ta.value = '';
  } catch(e) {
    alert('Invalid data code: ' + e.message);
  }
}

// Unified state applier with validation
function applyImportData(parsed) {
  if (!parsed) throw new Error('Data is empty');

  if (parsed.dsaState) {
    state = parsed.dsaState;
  } else if (parsed.problems) {
    state = { version: 3, problems: parsed.problems, maxStreak: parsed.maxStreak || 0, collapsedSteps: {} };
  }

  if (parsed.striverState) {
    striverState = parsed.striverState;
  }

  if (parsed.diaryState) diaryState = parsed.diaryState;
  if (parsed.plannerState) plannerState = parsed.plannerState;
  if (parsed.studyState) studyState = parsed.studyState;
  if (parsed.settingsState) settingsState = parsed.settingsState;

  saveState();
  saveStriverState();
  saveDiaryState();
  savePlannerState();
  saveStudyState();
  saveSettingsState();
  recordSnapshot('Restored from backup/sync');
  refreshAllUI();
}

// Check startup version and archive pre-upgrade snapshot
function handleVersionUpgradeArchiving() {
  try {
    const storedVersion = localStorage.getItem('prep_app_build_version');
    if (storedVersion !== APP_BUILD_VERSION) {
      // Archive current state before upgrade
      const rawV3 = localStorage.getItem(STORAGE_KEY_V3);
      const rawStriver = localStorage.getItem(STORAGE_STRIVER_KEY);
      if (rawV3 || rawStriver) {
        localStorage.setItem(SNAPSHOT_STARTUP_KEY, JSON.stringify({
          archivedAt: new Date().toISOString(),
          priorVersion: storedVersion,
          dsaRaw: rawV3,
          striverRaw: rawStriver
        }));
      }
      localStorage.setItem('prep_app_build_version', APP_BUILD_VERSION);
    }
  } catch(e) {
    console.warn('Version check note:', e);
  }
}
"""

# Inject StorageGuard right before saveState()
ss_idx = html.find("function saveState()")
assert ss_idx != -1, "saveState anchor not found"
html = html[:ss_idx] + storage_guard_js + "\n\n" + html[ss_idx:]

# Update saveState and saveStriverState with overwrite guard & error handling
safe_save_state = """function saveState() {
  try {
    // Overwrite guard: Do not overwrite non-empty storage with empty memory state
    const currentDone = Object.values(state.problems).filter(p => p.done).length;
    if (currentDone === 0) {
      const existingRaw = localStorage.getItem(STORAGE_KEY_V3);
      if (existingRaw) {
        try {
          const parsed = JSON.parse(existingRaw);
          const existingDone = Object.values(parsed.problems || {}).filter(p => p.done).length;
          if (existingDone > 0) {
            console.warn('Safety guard blocked empty overwrite of DSA state. Existing done:', existingDone);
            return;
          }
        } catch(err) {}
      }
    }

    localStorage.setItem(STORAGE_KEY_V3, JSON.stringify(state));
    // Keep backward-compatible V2 in sync
    const v2Copy = {
      version: 2,
      problems: {},
      maxStreak: state.maxStreak || 0,
      collapsedSteps: state.collapsedSteps || {}
    };
    Object.keys(state.problems).forEach(k => {
      const p = state.problems[k];
      v2Copy.problems[k] = {
        done: p.done,
        firstSolvedDate: p.firstSolvedDate,
        completedOn: p.completedOn,
        starred: p.starred
      };
    });
    localStorage.setItem(STORAGE_KEY_V2, JSON.stringify(v2Copy));
    recordSnapshot('DSA progress updated');
  } catch(e) {
    console.error('Storage error in saveState:', e);
    showStorageAlert('Browser storage write failed for DSA progress: ' + e.message);
  }
}"""

old_save_state_end = html.find("function loadState()")
html = html[:html.find("function saveState()")] + safe_save_state + "\n\n" + html[old_save_state_end:]

safe_save_striver_state = """function saveStriverState() {
  try {
    // Overwrite guard: Do not overwrite non-empty storage with empty memory state
    const currentDone = Object.values(striverState.problems).filter(p => p.done).length;
    if (currentDone === 0) {
      const existingRaw = localStorage.getItem(STORAGE_STRIVER_KEY);
      if (existingRaw) {
        try {
          const parsed = JSON.parse(existingRaw);
          const existingDone = Object.values(parsed.problems || {}).filter(p => p.done).length;
          if (existingDone > 0) {
            console.warn('Safety guard blocked empty overwrite of Striver state. Existing done:', existingDone);
            return;
          }
        } catch(err) {}
      }
    }

    localStorage.setItem(STORAGE_STRIVER_KEY, JSON.stringify(striverState));
    const oldDone = {};
    const oldStarred = {};
    const oldNotes = {};
    const oldDates = {};
    Object.keys(striverState.problems).forEach(k => {
      const p = striverState.problems[k];
      if (p.done) oldDone[k] = true;
      if (p.starred) oldStarred[k] = true;
      if (p.notes && p.notes.approach) oldNotes[k] = p.notes.approach;
      if (p.firstSolvedDate || p.completedOn) {
        oldDates[k] = { firstSolvedDate: p.firstSolvedDate, completedOn: p.completedOn };
      }
    });
    localStorage.setItem('a2z_v2', JSON.stringify(oldDone));
    localStorage.setItem('a2z_starred', JSON.stringify(oldStarred));
    localStorage.setItem('a2z_notes', JSON.stringify(oldNotes));
    localStorage.setItem('a2z_dates', JSON.stringify(oldDates));
    localStorage.setItem('a2z_maxstreak', String(striverState.maxStreak || 0));
    recordSnapshot('Striver progress updated');
  } catch(e) {
    console.error('Storage error in saveStriverState:', e);
    showStorageAlert('Browser storage write failed for Striver progress: ' + e.message);
  }
}"""

old_save_striver_end = html.find("function loadStriverState()")
html = html[:html.find("function saveStriverState()")] + safe_save_striver_state + "\n\n" + html[old_save_striver_end:]

# Update triggerResetEverything to export emergency backup first and eliminate localStorage.clear()
old_reset_everything = """function triggerResetEverything() {
  const conf = prompt("WARNING: This will permanently delete all DSA progress, diary entries, planner goals, and study logs. Type 'RESET ALL' to confirm:");
  if(conf === 'RESET ALL') {
    localStorage.clear();
    state = { version: 3, problems: {}, maxStreak: 0, collapsedSteps: {} };
    diaryState = { version: 1, entries: {} };
    plannerState = { version: 1, tasks: {} };
    studyState = { version: 1, days: {} };
    showToast('All data has been reset.');
    location.reload();
  }
}"""

new_reset_everything = """function triggerResetEverything() {
  const conf = prompt("WARNING: This will reset progress. An emergency backup will be downloaded automatically first. Type 'RESET ALL' to confirm:");
  if(conf === 'RESET ALL') {
    exportCompleteBackup(); // Guarantee backup file is downloaded first!
    const keysToRemove = [STORAGE_KEY_V3, STORAGE_KEY_V2, STORAGE_KEY_V1, STORAGE_STRIVER_KEY, 'a2z_v2', 'a2z_starred', 'a2z_notes', 'a2z_dates', 'a2z_maxstreak', STORAGE_DIARY_KEY, STORAGE_PLANNER_KEY, STORAGE_STUDY_KEY, STORAGE_SETTINGS_KEY];
    keysToRemove.forEach(k => {
      try { localStorage.removeItem(k); } catch(e) {}
    });
    state = { version: 3, problems: {}, maxStreak: 0, collapsedSteps: {} };
    striverState = { version: 1, problems: {}, maxStreak: 0, collapsedSteps: {} };
    diaryState = { version: 1, entries: {} };
    plannerState = { version: 1, tasks: {} };
    studyState = { version: 1, days: {} };
    showToast('Data has been reset. Emergency backup was exported.');
    setTimeout(() => location.reload(), 1000);
  }
}"""
assert old_reset_everything in html, "triggerResetEverything anchor not found"
html = html.replace(old_reset_everything, new_reset_everything, 1)

# In init(), call handleVersionUpgradeArchiving(), initIndexedDB(), and renderSnapshotHistoryUI()
old_init_header = "function init() {\n  loadState();\n  loadStriverState();"
new_init_header = "function init() {\n  handleVersionUpgradeArchiving();\n  initIndexedDB();\n  loadState();\n  loadStriverState();"
assert old_init_header in html, "init header anchor not found"
html = html.replace(old_init_header, new_init_header, 1)

old_init_tail = "renderMotivationView();\n  updateTimerUI();"
new_init_tail = "renderMotivationView();\n  updateTimerUI();\n  renderSnapshotHistoryUI();"
assert old_init_tail in html, "init tail anchor not found"
html = html.replace(old_init_tail, new_init_tail, 1)

# Write to integrated_master.html
target_file = "/Users/devrajput/.gemini/antigravity-ide/scratch/integrated_master.html"
with open(target_file, "w", encoding="utf-8") as out:
    out.write(html)

print("Generated resilient integrated_master.html successfully! Size:", len(html))

# Validate syntax with node -c
script_start = html.find("<script>") + 8
script_end = html.rfind("</script>")
script_code = html[script_start:script_end]

with open("/Users/devrajput/.gemini/antigravity-ide/scratch/resilient_script_check.js", "w", encoding="utf-8") as out:
    out.write(script_code)

res = subprocess.run(["node", "-c", "/Users/devrajput/.gemini/antigravity-ide/scratch/resilient_script_check.js"], capture_output=True, text=True)
if res.returncode == 0:
    print("SUCCESS: node -c passed with 0 errors!")
else:
    print("Syntax error:")
    print(res.stderr)
