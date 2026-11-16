/**
 * DATA & STORAGE CENTER ENGINE — PREPARATION DASHBOARD
 * Zero-dependency, offline storage auditor, backup builder, and safe restore engine.
 */

// Dedicated key for verified successful backup timestamp
const BACKUP_LAST_SUCCESS_KEY = 'prep_dashboard_last_successful_backup_timestamp';
const BACKUP_REMINDER_INTERVAL_MS = 7 * 24 * 60 * 60 * 1000; // 7 full days

// Comprehensive dictionary of dashboard-owned LocalStorage keys
const DASHBOARD_STORAGE_KEY_MAP = {
  'dsa_placement_prep_v3': { name: 'DSA Patterns Tracker (v3)', cat: 'DSA Tracker', desc: '184 problems, completion status, revisions & permanent notes' },
  'dsa_patterns_progress_v2': { name: 'DSA Patterns (v2 Legacy)', cat: 'DSA Tracker (Legacy)', desc: 'Legacy v2 snapshot for rollback safety' },
  'dsa_patterns_progress_v1': { name: 'DSA Patterns (v1 Legacy)', cat: 'DSA Tracker (Legacy)', desc: 'Legacy v1 snapshot for rollback safety' },
  'striver_a2z_tracker_v3': { name: 'Striver A2Z Sheet (v3)', cat: 'Striver A2Z', desc: '455 problems, sub-steps, notes, streak & starred questions' },
  'a2z_v2': { name: 'Striver A2Z (v2 Mirror)', cat: 'Striver (Legacy)', desc: 'Legacy done problems mirror' },
  'a2z_starred': { name: 'Striver Starred Mirror', cat: 'Striver (Legacy)', desc: 'Legacy starred problems mirror' },
  'a2z_notes': { name: 'Striver Notes Mirror', cat: 'Striver (Legacy)', desc: 'Legacy problem notes mirror' },
  'a2z_dates': { name: 'Striver Dates Mirror', cat: 'Striver (Legacy)', desc: 'Legacy completion dates mirror' },
  'a2z_maxstreak': { name: 'Striver Max Streak', cat: 'Striver (Legacy)', desc: 'Legacy max streak record' },
  'risingbrain_tracker_v1': { name: 'RisingBrain Pattern Wise', cat: 'RisingBrain', desc: '385 problems across 17 pattern topics' },
  'mik_interview_dsa_tracker_v1': { name: 'MIK Interview DSA', cat: 'MIK DSA', desc: '1526 curated interview problems across 23 topics' },
  'core_subjects_hub_v1_state': { name: 'Core Subjects Progress', cat: 'Core Subjects', desc: 'CS subjects topic checkboxes and completion status' },
  'core_subjects_hub_v1_notes': { name: 'Core Subjects Notes', cat: 'Core Subjects', desc: 'Markdown study notes and cards for CS subjects' },
  'skills_learning_hub_v1': { name: 'Skills Learning Hub', cat: 'Skills Hub', desc: 'Learning tracks, completed lessons and lesson notes' },
  'study_clock_sessions_v1': { name: 'Study Clock History', cat: 'Study Clock', desc: 'Logged pomodoro and focused study sessions' },
  'study_clock_active_session_v1': { name: 'Study Clock Active Session', cat: 'Study Clock', desc: 'Active timer state and elapsed time timestamps' },
  'daily_task_planner_v1': { name: 'Daily Task Planner', cat: 'Workspace', desc: 'Daily tasks, time blocks, and priorities' },
  'daily_coding_log_v1': { name: 'Daily Coding Log', cat: 'Workspace', desc: 'Daily solved problem log and submissions' },
  'daily_potd_v1': { name: 'Daily Problem of the Day', cat: 'Workspace', desc: 'POTD history, links and personal solutions' },
  'daily_routines_v1': { name: 'Daily Routines Checklist', cat: 'Workspace', desc: 'Morning/evening placement preparation routines' },
  'dsa_diary_entries_v1': { name: 'Private Placement Journal', cat: 'Journal & Diary', desc: 'Daily reflection entries and placement mindset logs' },
  'dsa_planner_tasks_v1': { name: 'Legacy Planner Tasks', cat: 'Workspace (Legacy)', desc: 'Legacy task planner storage' },
  'dsa_study_logs_v1': { name: 'Study Logs Tracker', cat: 'Study Clock (Legacy)', desc: 'Day-by-day study minutes tracking' },
  'dsa_app_settings_v1': { name: 'App Settings & Intervals', cat: 'Settings', desc: 'Spaced repetition revision intervals & preferences' },
  'prep_dashboard_snapshot_latest': { name: 'Rolling Snapshot (Latest)', cat: 'System Snapshot', desc: 'Automatic rolling recovery bundle' },
  'prep_dashboard_snapshot_history': { name: 'Rolling Snapshot History', cat: 'System Snapshot', desc: 'Audit log of last 5 snapshots' },
  'prep_dashboard_snapshot_startup': { name: 'Startup Archive Snapshot', cat: 'System Snapshot', desc: 'Safety archive generated on build version updates' },
  'motivation_library_v1': { name: 'Motivation Library', cat: 'Motivation', desc: 'Custom placement resources, quotes and favorites' },
  'my_daily_quotes_v1': { name: 'Daily Quotes & Reflections', cat: 'Motivation', desc: 'Personal reflections and featured quotes' },
  'mummy_papa_notes_v1': { name: 'Mummy-Papa Private Notes', cat: 'Personal', desc: 'Private dedication notes and family blessings' },
  'mummy_papa_photo_v1': { name: 'Mummy-Papa Photo Fallback', cat: 'Personal', desc: 'Local photo fallback (if IndexedDB unavailable)' },
  'prep_app_build_version': { name: 'App Build Version', cat: 'System', desc: 'Current offline application build signature' },
  'prep_dashboard_last_successful_backup_timestamp': { name: 'Last Successful Backup Timestamp', cat: 'System', desc: 'Timestamp of last verified external backup file save' },
  'prep_dashboard_last_backup_meta': { name: 'Last Backup Metadata', cat: 'System', desc: 'Timestamp, size and record count of last JSON backup' },
  'prep_dashboard_last_restore_meta': { name: 'Last Restore Metadata', cat: 'System', desc: 'Timestamp and source of last restoration' },
  'prep_dashboard_emergency_before_restore': { name: 'Emergency Pre-Restore Safety', cat: 'System Snapshot', desc: 'Safety checkpoint created immediately prior to import' }
};

let currentPendingRestoreData = null;
let currentPendingEmergencyBackup = null;
let cachedLsInventory = [];
let pendingManualBackupMeta = null;

/* --- UTILITY HELPERS --- */
function formatStorageBytes(bytes) {
  if (bytes === undefined || bytes === null || isNaN(bytes)) return '--';
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KiB';
  if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MiB';
  return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GiB';
}

function getKolkataFormattedTime(dateInput) {
  if (!dateInput) return 'No record';
  try {
    const d = new Date(dateInput);
    if (isNaN(d.getTime())) return String(dateInput);
    return d.toLocaleString('en-IN', {
      timeZone: 'Asia/Kolkata',
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }) + ' IST';
  } catch (e) {
    return String(dateInput);
  }
}

function getRelativeTimeString(timestamp) {
  if (!timestamp) return 'Never';
  const now = Date.now();
  const diffSec = Math.floor((now - timestamp) / 1000);
  if (diffSec < 60) return 'Just now';
  const diffMin = Math.floor(diffSec / 60);
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHour = Math.floor(diffMin / 60);
  if (diffHour < 24) return `${diffHour}h ago`;
  const diffDay = Math.floor(diffHour / 24);
  return `${diffDay}d ago`;
}

function getBackupReminderState() {
  const rawTimestamp = localStorage.getItem(BACKUP_LAST_SUCCESS_KEY);
  if (!rawTimestamp) {
    return {
      hasBackup: false,
      lastBackupTime: null,
      nextDueTime: null,
      isDue: false,
      daysRemaining: null,
      daysElapsed: null,
      statusText: 'No backup recorded yet'
    };
  }

  const lastBackupTime = Number(rawTimestamp);
  if (isNaN(lastBackupTime) || lastBackupTime <= 0) {
    return {
      hasBackup: false,
      lastBackupTime: null,
      nextDueTime: null,
      isDue: false,
      daysRemaining: null,
      daysElapsed: null,
      statusText: 'No backup recorded yet'
    };
  }

  const now = Date.now();
  const elapsedMs = now - lastBackupTime;
  const nextDueTime = lastBackupTime + BACKUP_REMINDER_INTERVAL_MS;
  const isDue = elapsedMs >= BACKUP_REMINDER_INTERVAL_MS;
  const daysElapsed = Math.floor(elapsedMs / (24 * 60 * 60 * 1000));
  const daysRemaining = Math.max(0, Math.ceil((nextDueTime - now) / (24 * 60 * 60 * 1000)));

  return {
    hasBackup: true,
    lastBackupTime: lastBackupTime,
    nextDueTime: nextDueTime,
    isDue: isDue,
    daysRemaining: daysRemaining,
    daysElapsed: daysElapsed,
    statusText: isDue ? `Backup Due (${daysElapsed}d ago)` : `Up to Date (Due in ${daysRemaining}d)`
  };
}

/* --- STORAGE AUDIT & SCANNING --- */
async function auditBrowserStorageQuota() {
  const result = {
    supported: false,
    measured: false,
    usageBytes: 0,
    quotaBytes: 0,
    percent: 0,
    origin: window.location.origin || (window.location.protocol === 'file:' ? 'file://local' : 'local')
  };

  if (navigator.storage && navigator.storage.estimate) {
    try {
      const estimate = await navigator.storage.estimate();
      if (estimate && typeof estimate.usage === 'number' && typeof estimate.quota === 'number') {
        result.supported = true;
        result.measured = true;
        result.usageBytes = estimate.usage;
        result.quotaBytes = estimate.quota;
        result.percent = estimate.quota > 0 ? (estimate.usage / estimate.quota) * 100 : 0;
      }
    } catch (e) {
      console.warn('Storage quota estimation error:', e);
    }
  }
  return result;
}

async function auditBrowserStoragePersistence() {
  const result = {
    supported: false,
    persisted: false
  };

  if (navigator.storage && navigator.storage.persisted) {
    try {
      result.supported = true;
      result.persisted = await navigator.storage.persisted();
    } catch (e) {
      console.warn('Storage persistence query error:', e);
    }
  }
  return result;
}

async function requestBrowserStoragePersistence() {
  if (!navigator.storage || !navigator.storage.persist) {
    alert('Persistent Storage API is not supported in this browser environment.');
    return;
  }
  try {
    const granted = await navigator.storage.persist();
    if (granted) {
      showToast('🛡️ Persistent browser storage granted! Eviction protection is active.');
    } else {
      showToast('Browser retained standard eviction policy (default for local files/browsers).');
    }
    await refreshStorageCenterUI(false);
  } catch (e) {
    alert('Error requesting persistence: ' + e.message);
  }
}

function scanLocalStorageInventory() {
  const inventory = [];
  let totalAppBytes = 0;
  let totalAllBytes = 0;
  let largeKeysCount = 0;

  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    const rawVal = localStorage.getItem(key) || '';
    // Standard UTF-16 character calculation (2 bytes per character)
    const keyBytes = key.length * 2;
    const valBytes = rawVal.length * 2;
    const totalKeyBytes = keyBytes + valBytes;

    totalAllBytes += totalKeyBytes;

    const meta = DASHBOARD_STORAGE_KEY_MAP[key] || {
      name: key,
      cat: 'Other / Browser',
      desc: 'Non-cataloged or external key'
    };

    if (DASHBOARD_STORAGE_KEY_MAP[key]) {
      totalAppBytes += totalKeyBytes;
    }

    const isLarge = totalKeyBytes > 500 * 1024; // > 500 KiB
    if (isLarge) largeKeysCount++;

    // Calculate approximate items count
    let recordCountDesc = '1 entry';
    try {
      if (rawVal.startsWith('{') || rawVal.startsWith('[')) {
        const parsed = JSON.parse(rawVal);
        if (Array.isArray(parsed)) {
          recordCountDesc = `${parsed.length} items`;
        } else if (parsed && typeof parsed === 'object') {
          if (parsed.problems) {
            recordCountDesc = `${Object.keys(parsed.problems).length} problems`;
          } else if (parsed.entries) {
            recordCountDesc = `${Object.keys(parsed.entries).length} entries`;
          } else if (parsed.tasks) {
            recordCountDesc = `${Object.keys(parsed.tasks).length} schedules`;
          } else if (parsed.days) {
            recordCountDesc = `${Object.keys(parsed.days).length} logged days`;
          } else {
            recordCountDesc = `${Object.keys(parsed).length} keys`;
          }
        }
      } else {
        recordCountDesc = `${rawVal.length} chars`;
      }
    } catch (e) {
      recordCountDesc = `${rawVal.length} chars`;
    }

    inventory.push({
      key: key,
      name: meta.name,
      category: meta.cat,
      description: meta.desc,
      sizeBytes: totalKeyBytes,
      isAppKey: !!DASHBOARD_STORAGE_KEY_MAP[key],
      isLarge: isLarge,
      recordCountDesc: recordCountDesc
    });
  }

  // Sort descending by size
  inventory.sort((a, b) => b.sizeBytes - a.sizeBytes);
  cachedLsInventory = inventory;

  const typicalLimitBytes = 5 * 1024 * 1024; // 5.0 MiB
  const percentOfLimit = (totalAllBytes / typicalLimitBytes) * 100;

  return {
    inventory: inventory,
    totalAppBytes: totalAppBytes,
    totalAllBytes: totalAllBytes,
    typicalLimitBytes: typicalLimitBytes,
    percentOfLimit: percentOfLimit,
    largeKeysCount: largeKeysCount,
    keyCount: inventory.length
  };
}

async function scanIndexedDBInventory() {
  const dbs = [
    { name: 'PlacementTrackerDB', version: 1, storeName: 'snapshots', purpose: 'Rolling Snapshots & High-Quota Data Mirror' },
    { name: 'FamilyPhotosDB', version: 1, storeName: 'photos', purpose: 'Private Family Photo & Dedication Storage' }
  ];

  const results = [];

  for (const dbDef of dbs) {
    const item = {
      name: dbDef.name,
      version: dbDef.version,
      storeName: dbDef.storeName,
      purpose: dbDef.purpose,
      count: 0,
      approxSize: 0,
      status: 'Available',
      error: null
    };

    if (!window.indexedDB) {
      item.status = 'Not Supported';
      results.push(item);
      continue;
    }

    try {
      await new Promise((resolve) => {
        const req = indexedDB.open(dbDef.name, dbDef.version);
        req.onerror = (e) => {
          item.status = 'Inaccessible';
          item.error = e.target.error?.message || 'Permission denied';
          resolve();
        };
        req.onsuccess = (e) => {
          const db = e.target.result;
          if (!db.objectStoreNames.contains(dbDef.storeName)) {
            item.status = 'Store Not Created Yet';
            db.close();
            resolve();
            return;
          }
          try {
            const tx = db.transaction([dbDef.storeName], 'readonly');
            const store = tx.objectStore(dbDef.storeName);
            const countReq = store.count();
            countReq.onsuccess = () => {
              item.count = countReq.result || 0;
            };

            // Estimate size if feasible
            const getAllReq = store.getAll();
            getAllReq.onsuccess = () => {
              try {
                const str = JSON.stringify(getAllReq.result || []);
                item.approxSize = str.length * 2;
                item.status = item.count > 0 ? 'Active & Synced' : 'Ready (Empty)';
              } catch (err) {
                item.status = 'Active';
              }
              db.close();
              resolve();
            };
            getAllReq.onerror = () => {
              db.close();
              resolve();
            };
          } catch (txErr) {
            item.status = 'Error';
            item.error = txErr.message;
            db.close();
            resolve();
          }
        };
      });
    } catch (err) {
      item.status = 'Error';
      item.error = err.message;
    }

    results.push(item);
  }

  return results;
}

async function scanCacheStorageInventory() {
  const result = {
    supported: false,
    caches: []
  };

  if (window.caches && caches.keys) {
    result.supported = true;
    try {
      const keys = await caches.keys();
      for (const key of keys) {
        try {
          const cache = await caches.open(key);
          const reqs = await cache.keys();
          result.caches.push({
            name: key,
            entryCount: reqs.length
          });
        } catch (e) {
          result.caches.push({ name: key, entryCount: 0 });
        }
      }
    } catch (err) {
      console.warn('Cache keys error:', err);
    }
  }
  return result;
}

/* --- REFRESH STORAGE CENTER UI --- */
async function refreshStorageCenterUI(showUserToast = false) {
  // 1. LocalStorage (Synchronous DOM update)
  const lsData = scanLocalStorageInventory();
  const elLsVal = document.getElementById('scLsUsageValue');
  const elLsFill = document.getElementById('scLsMeterFill');
  const elLsSub = document.getElementById('scLsSubtext');
  const elLsPill = document.getElementById('scLsHealthPill');
  const elTabLsCount = document.getElementById('scTabLsCount');

  if (elLsVal) elLsVal.textContent = `${formatStorageBytes(lsData.totalAllBytes)} / 5.0 MiB`;
  if (elLsFill) {
    const cappedPercent = Math.min(100, Math.max(2, lsData.percentOfLimit));
    elLsFill.style.width = cappedPercent + '%';
    elLsFill.className = 'sc-meter-fill ' + (lsData.percentOfLimit >= 85 ? 'sc-meter-fill-red' : (lsData.percentOfLimit >= 70 ? 'sc-meter-fill-amber' : 'sc-meter-fill-blue'));
  }
  if (elLsSub) {
    elLsSub.textContent = `${lsData.keyCount} keys (${formatStorageBytes(lsData.totalAppBytes)} app data · ${lsData.largeKeysCount} large)`;
  }
  if (elLsPill) {
    if (lsData.percentOfLimit >= 85) {
      elLsPill.className = 'sc-metric-pill sc-pill-critical';
      elLsPill.textContent = 'Critical (>85%)';
    } else if (lsData.percentOfLimit >= 70) {
      elLsPill.className = 'sc-metric-pill sc-pill-warning';
      elLsPill.textContent = 'Warning (>70%)';
    } else {
      elLsPill.className = 'sc-metric-pill sc-pill-healthy';
      elLsPill.textContent = 'Optimal (<70%)';
    }
  }
  if (elTabLsCount) elTabLsCount.textContent = lsData.keyCount;
  renderLocalStorageTable(lsData.inventory);

  // 2. Backup Status & Reminder State (Synchronous DOM update)
  const reminderState = getBackupReminderState();
  let lastBackupMeta = null;
  try {
    const raw = localStorage.getItem('prep_dashboard_last_backup_meta');
    if (raw) lastBackupMeta = JSON.parse(raw);
  } catch (e) {}

  const elBackupTime = document.getElementById('scBackupTimeValue');
  const elBackupNextDue = document.getElementById('scBackupNextDue');
  const elBackupSub = document.getElementById('scBackupSubtext');
  const elBackupPill = document.getElementById('scBackupStatusPill');

  if (reminderState.hasBackup && reminderState.lastBackupTime) {
    if (elBackupTime) elBackupTime.textContent = getKolkataFormattedTime(reminderState.lastBackupTime);
    if (elBackupNextDue) {
      if (reminderState.isDue) {
        elBackupNextDue.innerHTML = `<span style="color:#fbbf24; font-weight:600;">⚠️ Due now</span> (was due ${getKolkataFormattedTime(reminderState.nextDueTime)})`;
      } else {
        elBackupNextDue.innerHTML = `<span style="color:#34d399;">✓ Next due:</span> ${getKolkataFormattedTime(reminderState.nextDueTime)} <span style="color:var(--text-muted); font-size:11px;">(${reminderState.daysRemaining}d remaining)</span>`;
      }
    }
    if (elBackupSub) {
      const sizeStr = lastBackupMeta?.sizeBytes ? formatStorageBytes(lastBackupMeta.sizeBytes) : '--';
      elBackupSub.textContent = `Size: ${sizeStr} · Saved ${getRelativeTimeString(reminderState.lastBackupTime)} · Verified save`;
    }
    if (elBackupPill) {
      if (reminderState.isDue) {
        elBackupPill.className = 'sc-metric-pill sc-pill-warning';
        elBackupPill.textContent = 'Backup Due (>7d)';
      } else {
        elBackupPill.className = 'sc-metric-pill sc-pill-healthy';
        elBackupPill.textContent = 'Up to Date';
      }
    }
  } else {
    if (elBackupTime) elBackupTime.textContent = 'Never Exported';
    if (elBackupNextDue) {
      elBackupNextDue.textContent = 'Next Due: Pending initial manual backup';
    }
    if (elBackupSub) {
      elBackupSub.textContent = 'Manual backup required to start 7-day schedule';
    }
    if (elBackupPill) {
      elBackupPill.className = 'sc-metric-pill sc-pill-neutral';
      elBackupPill.textContent = 'First Backup Pending';
    }
  }

  // 3. Render Smart Alerts synchronously
  renderSmartStorageAlerts({
    lsPercent: lsData.percentOfLimit,
    lsTotalBytes: lsData.totalAllBytes,
    largeKeysCount: lsData.largeKeysCount,
    quotaPercent: 0,
    quotaSupported: false,
    reminderState: reminderState
  });

  // 4. Async operations: Browser Quota, Persistence, IndexedDB, Cache
  const quota = await auditBrowserStorageQuota();
  const elQuotaVal = document.getElementById('scOriginUsageValue');
  const elQuotaFill = document.getElementById('scOriginMeterFill');
  const elQuotaSub = document.getElementById('scOriginSubtext');
  const elQuotaPill = document.getElementById('scOriginHealthPill');

  if (quota.supported && quota.measured) {
    if (elQuotaVal) elQuotaVal.textContent = `${formatStorageBytes(quota.usageBytes)} / ${formatStorageBytes(quota.quotaBytes)}`;
    if (elQuotaFill) {
      const qPercent = Math.min(100, Math.max(1, quota.percent));
      elQuotaFill.style.width = qPercent.toFixed(1) + '%';
      elQuotaFill.className = 'sc-meter-fill ' + (quota.percent >= 85 ? 'sc-meter-fill-red' : (quota.percent >= 70 ? 'sc-meter-fill-amber' : 'sc-meter-fill-blue'));
    }
    if (elQuotaSub) elQuotaSub.textContent = `Actual origin usage: ${quota.percent.toFixed(2)}% of browser quota`;
    if (elQuotaPill) {
      if (quota.percent >= 85) {
        elQuotaPill.className = 'sc-metric-pill sc-pill-critical';
        elQuotaPill.textContent = 'Critical (≥85%)';
      } else if (quota.percent >= 70) {
        elQuotaPill.className = 'sc-metric-pill sc-pill-warning';
        elQuotaPill.textContent = 'Warning (≥70%)';
      } else {
        elQuotaPill.className = 'sc-metric-pill sc-pill-healthy';
        elQuotaPill.textContent = 'Healthy (<70%)';
      }
    }
  } else {
    if (elQuotaVal) elQuotaVal.textContent = 'Unavailable (Sandbox)';
    if (elQuotaFill) elQuotaFill.style.width = '0%';
    if (elQuotaSub) elQuotaSub.textContent = 'Browser Storage API restricted (common on direct file:// URLs)';
    if (elQuotaPill) {
      elQuotaPill.className = 'sc-metric-pill sc-pill-neutral';
      elQuotaPill.textContent = 'Restricted';
    }
  }

  // Persistence
  const persist = await auditBrowserStoragePersistence();
  const elPersistVal = document.getElementById('scPersistValue');
  const elPersistPill = document.getElementById('scPersistPill');
  const elBtnPersist = document.getElementById('scBtnRequestPersist');

  if (persist.supported) {
    if (persist.persisted) {
      if (elPersistVal) elPersistVal.textContent = 'Granted (Protected)';
      if (elPersistPill) {
        elPersistPill.className = 'sc-metric-pill sc-pill-healthy';
        elPersistPill.textContent = 'Protected';
      }
      if (elBtnPersist) elBtnPersist.style.display = 'none';
    } else {
      if (elPersistVal) elPersistVal.textContent = 'Best-Effort (Standard)';
      if (elPersistPill) {
        elPersistPill.className = 'sc-metric-pill sc-pill-neutral';
        elPersistPill.textContent = 'Default Policy';
      }
      if (elBtnPersist) elBtnPersist.style.display = 'inline-flex';
    }
  } else {
    if (elPersistVal) elPersistVal.textContent = 'Not Supported';
    if (elPersistPill) {
      elPersistPill.className = 'sc-metric-pill sc-pill-neutral';
      elPersistPill.textContent = 'N/A';
    }
    if (elBtnPersist) elBtnPersist.style.display = 'none';
  }

  // Update alerts if quota is high
  if (quota.supported && quota.percent >= 85) {
    renderSmartStorageAlerts({
      lsPercent: lsData.percentOfLimit,
      lsTotalBytes: lsData.totalAllBytes,
      largeKeysCount: lsData.largeKeysCount,
      quotaPercent: quota.percent,
      quotaSupported: quota.supported,
      reminderState: reminderState
    });
  }

  // IndexedDB & Cache Breakdown
  await renderIndexedDBBreakdown();
  await renderCacheBreakdown();

  if (showUserToast) {
    showToast('✓ Storage scan refreshed with live measurements!');
  }
}

function renderSmartStorageAlerts(metrics) {
  const container = document.getElementById('scStorageAlertsContainer');
  if (!container) return;

  const alerts = [];
  const reminder = metrics.reminderState;

  // 7-Day Backup Reminder (ONLY show if a backup was previously taken AND 7+ full days have elapsed)
  if (reminder && reminder.hasBackup && reminder.isDue) {
    alerts.push(`
      <div class="sc-alert sc-alert-warning">
        <span class="sc-alert-icon">⚠️</span>
        <div class="sc-alert-content">
          <div><b>Backup Due:</b> It has been ${reminder.daysElapsed} days since your last verified backup (${getKolkataFormattedTime(reminder.lastBackupTime)}). Your next backup was due on ${getKolkataFormattedTime(reminder.nextDueTime)}. Export a fresh complete backup now to keep your recent notes and progress safe.</div>
          <button class="sc-alert-btn" onclick="exportCompleteBackup()">📥 Export Complete Backup Now</button>
        </div>
      </div>
    `);
  }

  // LocalStorage Alert (>70% or >85%)
  if (metrics.lsPercent >= 85) {
    alerts.push(`
      <div class="sc-alert sc-alert-critical">
        <span class="sc-alert-icon">🚨</span>
        <div class="sc-alert-content">
          <div><b>Critical LocalStorage Usage (${metrics.lsPercent.toFixed(1)}%):</b> Application LocalStorage is approaching the standard 5 MiB browser ceiling (${formatStorageBytes(metrics.lsTotalBytes)} used). Further writes may trigger <code>QuotaExceededError</code>. Export an external backup now.</div>
          <button class="sc-alert-btn" onclick="exportCompleteBackup()">📥 Export Backup Immediately</button>
        </div>
      </div>
    `);
  } else if (metrics.lsPercent >= 70) {
    alerts.push(`
      <div class="sc-alert sc-alert-warning">
        <span class="sc-alert-icon">⚠️</span>
        <div class="sc-alert-content">
          <div><b>LocalStorage Warning (${metrics.lsPercent.toFixed(1)}%):</b> LocalStorage has crossed 70% of standard capacity. Check the key breakdown below to identify unusually large data keys.</div>
        </div>
      </div>
    `);
  }

  // Origin Quota Alert
  if (metrics.quotaSupported && metrics.quotaPercent >= 85) {
    alerts.push(`
      <div class="sc-alert sc-alert-critical">
        <span class="sc-alert-icon">🚨</span>
        <div class="sc-alert-content">
          <div><b>Critical Origin Storage Pressure (${metrics.quotaPercent.toFixed(1)}%):</b> Your browser origin storage is under extreme space pressure. Free up device disk space or back up your data.</div>
        </div>
      </div>
    `);
  }

  container.innerHTML = alerts.join('');
}

function renderLocalStorageTable(inventory) {
  const tbody = document.getElementById('scLsTableBody');
  if (!tbody) return;

  if (!inventory || inventory.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:1.5rem; color:var(--text-muted);">No LocalStorage keys found.</td></tr>';
    return;
  }

  let html = '';
  inventory.forEach(item => {
    html += `
      <tr>
        <td>
          <div class="sc-key-name" title="${escapeHtmlPnote(item.key)}">
            <span>🔑</span>
            <span>${escapeHtmlPnote(item.name)}</span>
          </div>
          <div style="font-family:var(--font-mono); font-size:10.5px; color:var(--text-muted); margin-top:2px;">
            ${escapeHtmlPnote(item.key)}
          </div>
        </td>
        <td>
          <span class="sc-key-cat">${escapeHtmlPnote(item.category)}</span>
        </td>
        <td>
          <span class="sc-key-size">${formatStorageBytes(item.sizeBytes)}</span>
        </td>
        <td style="color:var(--text-muted); font-size:11.5px;">
          ${escapeHtmlPnote(item.recordCountDesc)}
        </td>
        <td>
          ${item.isLarge ? '<span class="sc-badge-large">⚠️ Large Key</span>' : '<span style="color:#34d399; font-size:11px;">✓ OK</span>'}
        </td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

function filterStorageKeysTable() {
  const input = document.getElementById('scLsSearchInput');
  const filter = (input ? input.value : '').toLowerCase().trim();
  const filtered = cachedLsInventory.filter(item => {
    return item.key.toLowerCase().includes(filter) ||
           item.name.toLowerCase().includes(filter) ||
           item.category.toLowerCase().includes(filter);
  });
  renderLocalStorageTable(filtered);
}

async function renderIndexedDBBreakdown() {
  const grid = document.getElementById('scIdbGrid');
  const tabCount = document.getElementById('scTabIdbCount');
  if (!grid) return;

  const idbItems = await scanIndexedDBInventory();
  if (tabCount) tabCount.textContent = idbItems.length;

  let html = '';
  idbItems.forEach(item => {
    html += `
      <div class="sc-store-card">
        <div class="sc-store-header">
          <span class="sc-store-title">💾 ${escapeHtmlPnote(item.name)}</span>
          <span class="sc-metric-pill ${item.count > 0 ? 'sc-pill-healthy' : 'sc-pill-neutral'}">${escapeHtmlPnote(item.status)}</span>
        </div>
        <div style="font-size:12px; color:var(--text-muted); margin-bottom:0.75rem;">
          ${escapeHtmlPnote(item.purpose)}
        </div>
        <div style="display:flex; justify-content:space-between; font-size:12px; border-top:1px solid rgba(255,255,255,0.06); padding-top:0.6rem;">
          <span style="color:var(--text-muted);">Object Store: <code>${escapeHtmlPnote(item.storeName)}</code></span>
          <span style="color:#e2e8f0; font-weight:600;">${item.count} records</span>
        </div>
        ${item.approxSize > 0 ? `
          <div style="display:flex; justify-content:space-between; font-size:11.5px; color:var(--text-muted); margin-top:0.3rem;">
            <span>Approximate Payload:</span>
            <span style="font-family:var(--font-mono); color:#38bdf8;">${formatStorageBytes(item.approxSize)}</span>
          </div>
        ` : ''}
      </div>
    `;
  });

  grid.innerHTML = html;
}

async function renderCacheBreakdown() {
  const container = document.getElementById('scCacheContainer');
  const tabCount = document.getElementById('scTabCacheCount');
  if (!container) return;

  const cacheInfo = await scanCacheStorageInventory();
  if (tabCount) tabCount.textContent = cacheInfo.caches.length;

  if (!cacheInfo.supported || cacheInfo.caches.length === 0) {
    container.innerHTML = `
      <div style="padding:1.5rem; text-align:center; color:var(--text-muted); background:rgba(11,15,25,0.5); border-radius:8px;">
        No active Service Worker caches detected for this origin.
      </div>
    `;
    return;
  }

  let html = '<div class="sc-store-grid">';
  cacheInfo.caches.forEach(c => {
    html += `
      <div class="sc-store-card">
        <div class="sc-store-header">
          <span class="sc-store-title">🌐 ${escapeHtmlPnote(c.name)}</span>
          <span class="sc-metric-pill sc-pill-healthy">Active Cache</span>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:12px; border-top:1px solid rgba(255,255,255,0.06); padding-top:0.6rem;">
          <span style="color:var(--text-muted);">Cached Responses:</span>
          <span style="color:#e2e8f0; font-weight:600;">${c.entryCount} items</span>
        </div>
      </div>
    `;
  });
  html += '</div>';

  container.innerHTML = html;
}

function switchStorageCenterTab(tabId, btn) {
  document.querySelectorAll('.sc-breakdown-nav .sc-tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.sc-tab-pane').forEach(p => p.classList.remove('active'));

  if (btn) btn.classList.add('active');

  const paneMap = {
    'localstorage': 'scPaneLocalstorage',
    'indexeddb': 'scPaneIndexeddb',
    'cache': 'scPaneCache',
    'protection': 'scPaneProtection'
  };

  const targetId = paneMap[tabId];
  if (targetId) {
    const pane = document.getElementById(targetId);
    if (pane) pane.classList.add('active');
  }
}

/* --- COMPREHENSIVE BACKUP BUILDER --- */
function buildComprehensiveBackupBundle() {
  const dsaDone = (typeof state !== 'undefined' && state.problems) ? Object.values(state.problems).filter(p => p.done).length : 0;
  const striverDone = (typeof striverState !== 'undefined' && striverState.problems) ? Object.values(striverState.problems).filter(p => p.done).length : 0;
  const rbDone = (typeof risingBrainState !== 'undefined' && risingBrainState.problems) ? Object.values(risingBrainState.problems).filter(p => p.done).length : 0;
  const mikDone = (typeof mikState !== 'undefined' && mikState.problems) ? Object.values(mikState.problems).filter(p => p.done).length : 0;
  const csTopicsDone = (typeof coreSubjectsState !== 'undefined' && coreSubjectsState.completedTopics) ? Object.keys(coreSubjectsState.completedTopics).length : 0;
  const diaryEntriesCount = (typeof diaryState !== 'undefined' && diaryState.entries) ? Object.keys(diaryState.entries).length : 0;
  const studySessionsCount = (typeof studyClockHistory !== 'undefined' && Array.isArray(studyClockHistory)) ? studyClockHistory.length : 0;

  const now = new Date();
  const kolkataTimeStr = getKolkataFormattedTime(now);

  const bundle = {
    schemaVersion: 6,
    version: 6,
    appBuildVersion: typeof APP_BUILD_VERSION !== 'undefined' ? APP_BUILD_VERSION : '2026.10.26-offline-v5',
    exportedAt: now.toISOString(),
    backupDateKolkata: kolkataTimeStr,
    manifest: {
      generator: 'Preparation Dashboard Data & Storage Center',
      categories: [
        'dsaPatterns', 'striverA2Z', 'risingBrain', 'mikInterview',
        'coreSubjects', 'skillsHub', 'studyClock', 'dailyWorkspace',
        'diary', 'planner', 'studyLogs', 'settings', 'motivation', 'personalNotes'
      ],
      metrics: {
        dsaSolved: dsaDone,
        striverSolved: striverDone,
        risingBrainSolved: rbDone,
        mikSolved: mikDone,
        coreSubjectsCompleted: csTopicsDone,
        diaryEntries: diaryEntriesCount,
        studyClockSessions: studySessionsCount
      }
    },
    // Category Groupings
    categories: {
      dsaPatterns: typeof state !== 'undefined' ? state : null,
      striverA2Z: typeof striverState !== 'undefined' ? striverState : null,
      risingBrain: typeof risingBrainState !== 'undefined' ? risingBrainState : null,
      mikInterview: typeof mikState !== 'undefined' ? mikState : null,
      coreSubjects: {
        state: typeof coreSubjectsState !== 'undefined' ? coreSubjectsState : null,
        notes: typeof coreSubjectsNotes !== 'undefined' ? coreSubjectsNotes : null
      },
      skillsHub: typeof skillsHubData !== 'undefined' ? skillsHubData : null,
      studyClock: {
        history: typeof studyClockHistory !== 'undefined' ? studyClockHistory : null,
        activeSession: typeof studyClockActiveSession !== 'undefined' ? studyClockActiveSession : null
      },
      dailyWorkspace: {
        tasks: typeof plannerTasks !== 'undefined' ? plannerTasks : null,
        codingLog: typeof codingLog !== 'undefined' ? codingLog : null,
        potd: typeof potdRecords !== 'undefined' ? potdRecords : null,
        routines: typeof routineTemplates !== 'undefined' ? routineTemplates : null,
        diary: typeof diaryState !== 'undefined' ? diaryState : null,
        legacyTasks: typeof plannerState !== 'undefined' ? plannerState : null
      },
      studyLogs: typeof studyState !== 'undefined' ? studyState : null,
      settings: typeof settingsState !== 'undefined' ? settingsState : null,
      motivation: {
        library: typeof motivationLibraryData !== 'undefined' ? motivationLibraryData : null,
        dailyQuotes: typeof myDailyQuotesData !== 'undefined' ? myDailyQuotesData : null
      },
      personalNotes: localStorage.getItem(MP_STORAGE_KEY_NOTE) || ''
    },
    // Backwards-Compatible Top-Level Keys
    dsaState: typeof state !== 'undefined' ? state : null,
    striverState: typeof striverState !== 'undefined' ? striverState : null,
    risingBrainState: typeof risingBrainState !== 'undefined' ? risingBrainState : null,
    mikState: typeof mikState !== 'undefined' ? mikState : null,
    diaryState: typeof diaryState !== 'undefined' ? diaryState : null,
    plannerState: typeof plannerState !== 'undefined' ? plannerState : null,
    studyState: typeof studyState !== 'undefined' ? studyState : null,
    settingsState: typeof settingsState !== 'undefined' ? settingsState : null,
    coreSubjectsState: typeof coreSubjectsState !== 'undefined' ? coreSubjectsState : null,
    coreSubjectsNotes: typeof coreSubjectsNotes !== 'undefined' ? coreSubjectsNotes : null,
    skillsHubData: typeof skillsHubData !== 'undefined' ? skillsHubData : null,
    studyClockHistory: typeof studyClockHistory !== 'undefined' ? studyClockHistory : null,
    studyClockActiveSession: typeof studyClockActiveSession !== 'undefined' ? studyClockActiveSession : null,
    plannerTasks: typeof plannerTasks !== 'undefined' ? plannerTasks : null,
    codingLog: typeof codingLog !== 'undefined' ? codingLog : null,
    potdRecords: typeof potdRecords !== 'undefined' ? potdRecords : null,
    routineTemplates: typeof routineTemplates !== 'undefined' ? routineTemplates : null
  };

  return bundle;
}

/* --- EXPORT COMPLETE BACKUP WITH SAVE VERIFICATION --- */
async function exportCompleteBackup() {
  try {
    const bundle = buildComprehensiveBackupBundle();
    const jsonStr = JSON.stringify(bundle, null, 2);

    // Unique timestamp-based filename down to seconds to guarantee zero collisions
    const now = new Date();
    const y = now.getFullYear();
    const m = String(now.getMonth() + 1).padStart(2, '0');
    const d = String(now.getDate()).padStart(2, '0');
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');
    const fileName = `prep_dashboard_complete_backup_${y}-${m}-${d}_${hh}${mm}${ss}.json`;

    // 1. Where supported: Use browser File System Access API (showSaveFilePicker)
    // Success is recorded ONLY after creating writable, writing, and closing file stream
    if (typeof window.showSaveFilePicker === 'function') {
      try {
        const opts = {
          suggestedName: fileName,
          types: [{
            description: 'JSON Backup File',
            accept: { 'application/json': ['.json'] }
          }]
        };
        const fileHandle = await window.showSaveFilePicker(opts);
        const writable = await fileHandle.createWritable();
        await writable.write(jsonStr);
        await writable.close();

        // Actual disk write verified!
        recordSuccessfulBackup(now.getTime(), jsonStr.length, fileHandle.name || fileName, 'file_system_api');
        showToast('✓ Backup file written directly to disk! Next reminder in 7 days.');
        return true;
      } catch (pickerErr) {
        if (pickerErr.name === 'AbortError') {
          console.log('User cancelled save file dialog');
          showToast('Backup save was cancelled. Timestamp not updated.');
          return false;
        }
        console.warn('showSaveFilePicker threw error, falling back to download workflow:', pickerErr);
      }
    }

    // 2. Where unsupported or fallen back:
    // Generate and initiate download
    downloadFile(jsonStr, fileName, 'application/json');

    // Store pending metadata in memory (DO NOT update timestamp until user confirms!)
    pendingManualBackupMeta = {
      timestamp: now.getTime(),
      sizeBytes: jsonStr.length,
      fileName: fileName,
      method: 'confirmed_download'
    };

    // Prompt user with explicit "I have saved the backup" confirmation action
    const modalEl = document.getElementById('modalBackupDownloadConfirmation');
    const nameEl = document.getElementById('scPendingBackupFileName');
    const sizeEl = document.getElementById('scPendingBackupFileSize');
    if (nameEl) nameEl.textContent = fileName;
    if (sizeEl) sizeEl.textContent = formatStorageBytes(jsonStr.length);

    if (modalEl) {
      openModal('modalBackupDownloadConfirmation');
    } else {
      const confirmed = window.confirm(
        `Backup file download initiated: ${fileName}\n\nDid you successfully save the backup file? Click OK if "I have saved the backup".`
      );
      if (confirmed) {
        confirmBackupSaveManually();
      } else {
        cancelBackupSaveConfirmation();
      }
    }

  } catch (err) {
    console.error('Backup generation error:', err);
    alert('Failed to generate backup: ' + err.message);
  }
}

function confirmBackupSaveManually() {
  if (!pendingManualBackupMeta) return;
  const { timestamp, sizeBytes, fileName, method } = pendingManualBackupMeta;
  recordSuccessfulBackup(timestamp, sizeBytes, fileName, method);
  pendingManualBackupMeta = null;
  closeModal('modalBackupDownloadConfirmation');
  showToast('✓ Backup verified and recorded! Next reminder in 7 days.');
}

function cancelBackupSaveConfirmation() {
  pendingManualBackupMeta = null;
  closeModal('modalBackupDownloadConfirmation');
  showToast('Backup unconfirmed. Timestamp was not updated.');
}

function recordSuccessfulBackup(timestamp, sizeBytes, fileName, method) {
  const now = new Date(timestamp);
  const nextDue = new Date(timestamp + BACKUP_REMINDER_INTERVAL_MS);

  // Store in dedicated storage key
  try {
    localStorage.setItem(BACKUP_LAST_SUCCESS_KEY, String(timestamp));
  } catch (e) {
    console.warn('Could not store backup timestamp in dedicated key:', e);
  }

  // Store rich metadata
  const meta = {
    timestamp: timestamp,
    iso: now.toISOString(),
    kolkataTime: getKolkataFormattedTime(now),
    nextDueTimestamp: nextDue.getTime(),
    nextDueKolkata: getKolkataFormattedTime(nextDue),
    sizeBytes: sizeBytes,
    fileName: fileName,
    schemaVersion: 6,
    method: method
  };

  try {
    localStorage.setItem('prep_dashboard_last_backup_meta', JSON.stringify(meta));
  } catch (e) {
    console.warn('Could not store backup meta:', e);
  }

  // Immediately refresh storage center UI & reminders
  refreshStorageCenterUI(false);
}

/* --- SAFE RESTORE & IMPORT WORKFLOW --- */
function handleStorageCenterImportFile(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const rawText = e.target.result;
      const parsed = JSON.parse(rawText);

      if (!parsed || typeof parsed !== 'object') {
        throw new Error('File does not contain valid JSON data structure.');
      }

      // Check if it's a dashboard backup
      const hasDsa = !!(parsed.dsaState || parsed.problems || (parsed.categories && parsed.categories.dsaPatterns));
      const hasStriver = !!(parsed.striverState || (parsed.categories && parsed.categories.striverA2Z));
      const hasCoreSubjects = !!(parsed.coreSubjectsState || (parsed.categories && parsed.categories.coreSubjects));
      const hasStudyClock = !!(parsed.studyClockHistory || (parsed.categories && parsed.categories.studyClock));
      const hasWorkspace = !!(parsed.plannerTasks || parsed.dailyWorkspace || (parsed.categories && parsed.categories.dailyWorkspace));

      if (!hasDsa && !hasStriver && !hasCoreSubjects && !hasStudyClock && !hasWorkspace) {
        throw new Error('Unrecognized backup schema. This file does not contain recognized Preparation Dashboard data.');
      }

      currentPendingRestoreData = parsed;

      // 1. Automatically create an emergency pre-restore snapshot of current live state
      try {
        currentPendingEmergencyBackup = buildComprehensiveBackupBundle();
        localStorage.setItem('prep_dashboard_emergency_before_restore', JSON.stringify(currentPendingEmergencyBackup));
        sessionStorage.setItem('prep_emergency_backup', JSON.stringify(currentPendingEmergencyBackup));
      } catch (err) {
        console.warn('Could not save local emergency snapshot:', err);
      }

      // 2. Populate inspection preview in modal
      const elDate = document.getElementById('scRestoreDateText');
      const elVersion = document.getElementById('scRestoreVersionText');
      const elSize = document.getElementById('scRestoreSizeText');

      if (elDate) {
        elDate.textContent = parsed.backupDateKolkata || (parsed.exportedAt ? getKolkataFormattedTime(parsed.exportedAt) : 'Unknown Date');
      }
      if (elVersion) {
        elVersion.textContent = `Schema v${parsed.schemaVersion || parsed.version || 'Legacy'} · ${parsed.appBuildVersion || 'Standard'}`;
      }
      if (elSize) {
        elSize.textContent = formatStorageBytes(rawText.length);
      }

      // 3. Populate Category Checklist
      renderRestoreCategoryChecklist(parsed);

      openModal('modalDataCenterRestore');

    } catch (err) {
      alert('Could not parse backup file:\n\n' + err.message);
    } finally {
      event.target.value = '';
    }
  };
  reader.readAsText(file);
}

function renderRestoreCategoryChecklist(parsed) {
  const container = document.getElementById('scRestoreChecklist');
  if (!container) return;

  const dsaStateData = parsed.categories?.dsaPatterns || parsed.dsaState || (parsed.problems ? parsed : null);
  const striverData = parsed.categories?.striverA2Z || parsed.striverState;
  const rbData = parsed.categories?.risingBrain || parsed.risingBrainState;
  const mikData = parsed.categories?.mikInterview || parsed.mikState;
  const csStateData = parsed.categories?.coreSubjects?.state || parsed.coreSubjectsState;
  const csNotesData = parsed.categories?.coreSubjects?.notes || parsed.coreSubjectsNotes;
  const skillsData = parsed.categories?.skillsHub || parsed.skillsHubData;
  const studyClockData = parsed.categories?.studyClock?.history || parsed.studyClockHistory;
  const workspaceData = parsed.categories?.dailyWorkspace || {
    tasks: parsed.plannerTasks,
    codingLog: parsed.codingLog,
    potd: parsed.potdRecords,
    routines: parsed.routineTemplates
  };
  const diaryData = parsed.categories?.dailyWorkspace?.diary || parsed.diaryState;
  const settingsData = parsed.categories?.settings || parsed.settingsState;
  const motivationData = parsed.categories?.motivation || {
    library: parsed.motivationLibraryData,
    dailyQuotes: parsed.myDailyQuotesData
  };

  const dsaDone = dsaStateData?.problems ? Object.values(dsaStateData.problems).filter(p => p.done).length : 0;
  const dsaNotes = dsaStateData?.problems ? Object.values(dsaStateData.problems).filter(p => p.notes && (typeof p.notes === 'string' ? p.notes.trim() : (p.notes.content || p.notes.approach))).length : 0;
  const striverDone = striverData?.problems ? Object.values(striverData.problems).filter(p => p.done).length : 0;
  const rbDone = rbData?.problems ? Object.values(rbData.problems).filter(p => p.done).length : 0;
  const mikDone = mikData?.problems ? Object.values(mikData.problems).filter(p => p.done).length : 0;
  const csTopics = csStateData?.completedTopics ? Object.keys(csStateData.completedTopics).length : 0;
  const csNotes = csNotesData ? Object.keys(csNotesData).length : 0;
  const clockSessions = Array.isArray(studyClockData) ? studyClockData.length : 0;
  const diaryEntries = diaryData?.entries ? Object.keys(diaryData.entries).length : 0;

  const categories = [
    { id: 'cat_dsa', label: 'DSA Patterns Tracker', desc: `${dsaDone} solved · ${dsaNotes} permanent notes`, present: !!dsaStateData },
    { id: 'cat_striver', label: 'Striver A2Z Sheet', desc: `${striverDone} solved problems`, present: !!striverData },
    { id: 'cat_rb', label: 'RisingBrain Pattern Wise', desc: `${rbDone} solved problems`, present: !!rbData },
    { id: 'cat_mik', label: 'MIK Interview DSA', desc: `${mikDone} solved problems`, present: !!mikData },
    { id: 'cat_cs', label: 'Core Subjects & Notes', desc: `${csTopics} completed · ${csNotes} study notes`, present: !!(csStateData || csNotesData) },
    { id: 'cat_skills', label: 'Skills Learning Hub', desc: 'Tracks, lessons & progress', present: !!skillsData },
    { id: 'cat_clock', label: 'Study Clock & Pomodoro', desc: `${clockSessions} logged study sessions`, present: !!studyClockData },
    { id: 'cat_workspace', label: 'Daily Planner & POTD', desc: 'Task schedules, coding log & routines', present: !!workspaceData },
    { id: 'cat_diary', label: 'Private Journal & Diary', desc: `${diaryEntries} reflection entries`, present: !!diaryData },
    { id: 'cat_settings', label: 'App Settings & Intervals', desc: 'Spaced repetition revision intervals', present: !!settingsData },
    { id: 'cat_motivation', label: 'Motivation Library', desc: 'Custom quotes & resources', present: !!motivationData }
  ];

  let html = '';
  categories.forEach(cat => {
    html += `
      <label class="sc-check-item">
        <input type="checkbox" id="scRestore_${cat.id}" ${cat.present ? 'checked' : 'disabled'}>
        <div>
          <span class="sc-check-label">${escapeHtmlPnote(cat.label)}</span>
          <span class="sc-check-desc">${cat.present ? escapeHtmlPnote(cat.desc) : 'Not found in this backup'}</span>
        </div>
      </label>
    `;
  });

  container.innerHTML = html;
}

function toggleAllRestoreCategories(selectAll) {
  const checkboxes = document.querySelectorAll('#scRestoreChecklist input[type="checkbox"]:not(:disabled)');
  checkboxes.forEach(cb => { cb.checked = selectAll; });
}

function downloadPreRestoreEmergencyBackup() {
  if (!currentPendingEmergencyBackup) {
    currentPendingEmergencyBackup = buildComprehensiveBackupBundle();
  }
  const jsonStr = JSON.stringify(currentPendingEmergencyBackup, null, 2);
  const fileName = `emergency_backup_before_restore_${Date.now()}.json`;
  downloadFile(jsonStr, fileName, 'application/json');
  showToast('✓ Emergency pre-restore backup saved to your downloads!');
}

function executeDataCenterRestoreConfirmed() {
  if (!currentPendingRestoreData) return;

  const parsed = currentPendingRestoreData;
  let restoredCount = 0;

  try {
    // 1. DSA Patterns Tracker
    const cbDsa = document.getElementById('scRestore_cat_dsa');
    if (cbDsa && cbDsa.checked) {
      const dsaStateData = parsed.categories?.dsaPatterns || parsed.dsaState || (parsed.problems ? parsed : null);
      if (dsaStateData) {
        if (dsaStateData.problems) {
          state = {
            version: 3,
            problems: dsaStateData.problems,
            maxStreak: dsaStateData.maxStreak || 0,
            collapsedSteps: dsaStateData.collapsedSteps || state.collapsedSteps || {}
          };
        } else {
          state = dsaStateData;
        }
        saveState();
        restoredCount++;
      }
    }

    // 2. Striver A2Z
    const cbStriver = document.getElementById('scRestore_cat_striver');
    if (cbStriver && cbStriver.checked) {
      const striverData = parsed.categories?.striverA2Z || parsed.striverState;
      if (striverData) {
        striverState = striverData;
        saveStriverState();
        restoredCount++;
      }
    }

    // 3. RisingBrain
    const cbRb = document.getElementById('scRestore_cat_rb');
    if (cbRb && cbRb.checked) {
      const rbData = parsed.categories?.risingBrain || parsed.risingBrainState;
      if (rbData) {
        risingBrainState = rbData;
        saveRisingBrainState();
        restoredCount++;
      }
    }

    // 4. MIK DSA
    const cbMik = document.getElementById('scRestore_cat_mik');
    if (cbMik && cbMik.checked) {
      const mikData = parsed.categories?.mikInterview || parsed.mikState;
      if (mikData) {
        mikState = mikData;
        saveMikState();
        restoredCount++;
      }
    }

    // 5. Core Subjects & Notes
    const cbCs = document.getElementById('scRestore_cat_cs');
    if (cbCs && cbCs.checked) {
      const csStateData = parsed.categories?.coreSubjects?.state || parsed.coreSubjectsState;
      const csNotesData = parsed.categories?.coreSubjects?.notes || parsed.coreSubjectsNotes;
      if (csStateData) {
        coreSubjectsState = csStateData;
        saveCoreSubjectsState();
        restoredCount++;
      }
      if (csNotesData) {
        coreSubjectsNotes = csNotesData;
        saveCoreSubjectsNotes();
      }
    }

    // 6. Skills Hub
    const cbSkills = document.getElementById('scRestore_cat_skills');
    if (cbSkills && cbSkills.checked) {
      const skillsData = parsed.categories?.skillsHub || parsed.skillsHubData;
      if (skillsData) {
        skillsHubData = skillsData;
        saveSkillsHubData();
        restoredCount++;
      }
    }

    // 7. Study Clock
    const cbClock = document.getElementById('scRestore_cat_clock');
    if (cbClock && cbClock.checked) {
      const studyClockData = parsed.categories?.studyClock?.history || parsed.studyClockHistory;
      if (studyClockData && Array.isArray(studyClockData)) {
        studyClockHistory = studyClockData;
        saveStudyClockHistory();
        restoredCount++;
      }
    }

    // 8. Daily Workspace (Tasks, Coding Log, POTD, Routines)
    const cbWorkspace = document.getElementById('scRestore_cat_workspace');
    if (cbWorkspace && cbWorkspace.checked) {
      const ws = parsed.categories?.dailyWorkspace;
      if (ws) {
        if (ws.tasks) { plannerTasks = ws.tasks; saveTasks(); }
        if (ws.codingLog) { codingLog = ws.codingLog; saveCodingLog(); }
        if (ws.potd) { potdRecords = ws.potd; savePotdRecords(); }
        if (ws.routines) { routineTemplates = ws.routines; saveRoutines(); }
      } else {
        if (parsed.plannerTasks) { plannerTasks = parsed.plannerTasks; saveTasks(); }
        if (parsed.codingLog) { codingLog = parsed.codingLog; saveCodingLog(); }
        if (parsed.potdRecords) { potdRecords = parsed.potdRecords; savePotdRecords(); }
        if (parsed.routineTemplates) { routineTemplates = parsed.routineTemplates; saveRoutines(); }
      }
      restoredCount++;
    }

    // 9. Diary
    const cbDiary = document.getElementById('scRestore_cat_diary');
    if (cbDiary && cbDiary.checked) {
      const diaryData = parsed.categories?.dailyWorkspace?.diary || parsed.diaryState;
      if (diaryData) {
        diaryState = diaryData;
        saveDiaryState();
        restoredCount++;
      }
    }

    // 10. Settings & Intervals
    const cbSettings = document.getElementById('scRestore_cat_settings');
    if (cbSettings && cbSettings.checked) {
      const settingsData = parsed.categories?.settings || parsed.settingsState;
      if (settingsData) {
        settingsState = settingsData;
        saveSettingsState();
        restoredCount++;
      }
    }

    // 11. Motivation
    const cbMotivation = document.getElementById('scRestore_cat_motivation');
    if (cbMotivation && cbMotivation.checked) {
      const motLib = parsed.categories?.motivation?.library || parsed.motivationLibraryData;
      const motQuotes = parsed.categories?.motivation?.dailyQuotes || parsed.myDailyQuotesData;
      if (motLib) { motivationLibraryData = motLib; saveMotivationLibraryData(); }
      if (motQuotes) { myDailyQuotesData = motQuotes; saveMyDailyQuotesData(); }
      restoredCount++;
    }

    // 12. Personal Notes
    if (parsed.personalNotes || parsed.categories?.personalNotes) {
      const pNotes = parsed.personalNotes || parsed.categories?.personalNotes;
      if (typeof pNotes === 'string' && pNotes.trim()) {
        try { localStorage.setItem(MP_STORAGE_KEY_NOTE, pNotes); } catch (e) {}
      }
    }

    // Record last restore metadata
    const restoreMeta = {
      timestamp: Date.now(),
      kolkataTime: getKolkataFormattedTime(new Date()),
      categoriesRestored: restoredCount,
      source: parsed.backupDateKolkata || parsed.exportedAt || 'Custom file'
    };
    try {
      localStorage.setItem('prep_dashboard_last_restore_meta', JSON.stringify(restoreMeta));
    } catch (e) {}

    closeModal('modalDataCenterRestore');

    // Smooth UI re-render across all modules
    if (typeof refreshAllUI === 'function') refreshAllUI();
    if (typeof updateHeaderStats === 'function') updateHeaderStats();
    if (typeof renderSnapshotHistoryUI === 'function') renderSnapshotHistoryUI();
    if (typeof renderCoreSubjectsView === 'function') renderCoreSubjectsView();
    if (typeof updateCoreSubjectsStats === 'function') updateCoreSubjectsStats();
    if (typeof renderSkillsHubView === 'function') renderSkillsHubView();
    if (typeof updateSkillsHubStats === 'function') updateSkillsHubStats();
    if (typeof renderCodingLog === 'function') renderCodingLog();
    if (typeof updatePotdUi === 'function') updatePotdUi();
    if (typeof renderRoutineTemplates === 'function') renderRoutineTemplates();
    if (typeof enhancedRenderMotivationView === 'function') enhancedRenderMotivationView();
    if (typeof initStudyClockEngine === 'function') initStudyClockEngine();

    refreshStorageCenterUI(false);

    showToast(`✓ Backup restored successfully (${restoredCount} categories updated)!`);

  } catch (err) {
    console.error('Restore error:', err);
    alert('Restoration error: ' + err.message);
  }
}

function handleImportFile(event) {
  handleStorageCenterImportFile(event);
}
