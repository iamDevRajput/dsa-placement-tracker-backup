#!/usr/bin/env python3
import os
import re
import shutil

TARGET_FILE = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"
BACKUP_FILE = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html.pre_notes_vault_bak"

print("Step 1: Creating safety backup...")
shutil.copyfile(TARGET_FILE, BACKUP_FILE)
print(f"Safety backup saved to {BACKUP_FILE}")

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# ----------------------------------------------------------------------
# 1. ADD NOTES RECOVERY VAULT AND SMART MERGE LOGIC
# ----------------------------------------------------------------------
vault_and_merge_logic = '''
/* ==========================================================================
   NOTES RECOVERY VAULT & SMART MULTI-WINDOW MERGE ENGINE
   ========================================================================== */
const STORAGE_NOTES_VAULT_KEY = 'prep_notes_recovery_vault_v1';

function saveNoteToVault(tracker, probId, text, extraMeta = {}) {
  if (!text || typeof text !== 'string' || !text.trim()) return;
  try {
    let vault = {};
    const raw = localStorage.getItem(STORAGE_NOTES_VAULT_KEY);
    if (raw) {
      try { vault = JSON.parse(raw) || {}; } catch(e) {}
    }
    const key = `${tracker}_${probId}`;
    const now = new Date();
    vault[key] = {
      key: key,
      tracker: tracker,
      id: probId,
      text: text,
      charCount: text.length,
      lineCount: text.split('\\n').length,
      updatedAt: now.toISOString(),
      updatedDisplay: now.toLocaleString(),
      title: extraMeta.title || `Item #${probId}`,
      diff: extraMeta.diff || ''
    };
    localStorage.setItem(STORAGE_NOTES_VAULT_KEY, JSON.stringify(vault));
    updateStorageCenterVaultCount();
  } catch(e) {
    console.warn('Error saving to notes recovery vault:', e);
  }
}

function getNoteFromVault(tracker, probId) {
  try {
    const raw = localStorage.getItem(STORAGE_NOTES_VAULT_KEY);
    if (!raw) return null;
    const vault = JSON.parse(raw) || {};
    return vault[`${tracker}_${probId}`] || null;
  } catch(e) {
    return null;
  }
}

function getAllNotesFromVault() {
  try {
    const raw = localStorage.getItem(STORAGE_NOTES_VAULT_KEY);
    if (!raw) return {};
    return JSON.parse(raw) || {};
  } catch(e) {
    return {};
  }
}

function updateStorageCenterVaultCount() {
  const el = document.getElementById('scVaultNoteCount');
  if (el) {
    const vault = getAllNotesFromVault();
    el.textContent = Object.keys(vault).length;
  }
}

function safeMergeProblemCollection(existingProbs, incomingProbs, activelyEditedId = null) {
  if (!existingProbs || typeof existingProbs !== 'object') return incomingProbs || {};
  if (!incomingProbs || typeof incomingProbs !== 'object') return existingProbs || {};

  const merged = Object.assign({}, incomingProbs);

  for (const probId of Object.keys(existingProbs)) {
    const existing = existingProbs[probId];
    const incoming = merged[probId];

    if (!incoming) {
      merged[probId] = existing;
      continue;
    }

    // 1. NOTES MERGE GUARD:
    // If this problem was NOT actively edited in this current session:
    if (String(probId) !== String(activelyEditedId)) {
      const existingNotes = (typeof existing.notes === 'string') ? existing.notes : (existing.notes?.content || existing.notes?.approach || '');
      const incomingNotes = (typeof incoming.notes === 'string') ? incoming.notes : (incoming.notes?.content || incoming.notes?.approach || '');

      if (existingNotes && existingNotes.trim().length > 0) {
        if (!incomingNotes || incomingNotes.trim().length === 0 || existingNotes.length > incomingNotes.length) {
          if (typeof incoming.notes === 'object' && incoming.notes !== null) {
            incoming.notes.content = existingNotes;
            incoming.notes.approach = existingNotes;
          } else {
            incoming.notes = existing.notes;
          }
        }
      }
    }

    // 2. PROGRESS MERGE GUARD:
    // Preserve completed status if another tab solved it
    if (existing.done && !incoming.done && String(probId) !== String(activelyEditedId)) {
      incoming.done = true;
      if (!incoming.completedOn && existing.completedOn) incoming.completedOn = existing.completedOn;
      if (!incoming.firstSolvedDate && existing.firstSolvedDate) incoming.firstSolvedDate = existing.firstSolvedDate;
      if (existing.status && existing.status !== 'NOT_STARTED') incoming.status = existing.status;
    }

    // 3. REVISIONS MERGE GUARD:
    if (Array.isArray(existing.revisions) && existing.revisions.length > 0) {
      if (!Array.isArray(incoming.revisions) || incoming.revisions.length < existing.revisions.length) {
        incoming.revisions = existing.revisions;
        incoming.revisionCount = existing.revisions.length;
      }
    }
  }

  return merged;
}

function safeMergeMikProblems(existingProbs, incomingProbs, activelyEditedId = null) {
  if (!existingProbs || typeof existingProbs !== 'object') return incomingProbs || {};
  if (!incomingProbs || typeof incomingProbs !== 'object') return existingProbs || {};

  const merged = Object.assign({}, incomingProbs);

  for (const probId of Object.keys(existingProbs)) {
    const existing = existingProbs[probId];
    const incoming = merged[probId];

    if (!incoming) {
      merged[probId] = existing;
      continue;
    }

    if (String(probId) !== String(activelyEditedId)) {
      const exNotes = existing.notes || '';
      const inNotes = incoming.notes || '';
      if (exNotes && exNotes.trim().length > 0) {
        if (!inNotes || inNotes.trim().length === 0 || exNotes.length > inNotes.length) {
          incoming.notes = exNotes;
        }
      }
    }

    if (existing.done && !incoming.done && String(probId) !== String(activelyEditedId)) {
      incoming.done = true;
      incoming.status = existing.status || 'COMPLETED';
    }
  }

  return merged;
}

function healAndRecoverNotesOnStartup() {
  try {
    let recoveredCount = 0;

    // Scan snapshots for any notes that might have been lost in state
    const snapshotKeys = [SNAPSHOT_LATEST_KEY, SNAPSHOT_STARTUP_KEY];
    snapshotKeys.forEach(sKey => {
      try {
        const raw = localStorage.getItem(sKey);
        if (!raw) return;
        const snap = JSON.parse(raw);
        if (!snap) return;

        // Check DSA
        if (snap.dsaState && snap.dsaState.problems) {
          Object.keys(snap.dsaState.problems).forEach(pId => {
            const snNotes = getCombinedProblemNotes(snap.dsaState.problems[pId]);
            const curPs = getProblemState(pId);
            const curNotes = getCombinedProblemNotes(curPs);
            if (snNotes && snNotes.trim().length > 0) {
              saveNoteToVault('dsa', pId, snNotes, { title: `Problem #${pId}`, tracker: 'dsa' });
              if (!curNotes || curNotes.trim().length === 0) {
                if (!curPs.notes || typeof curPs.notes !== 'object') curPs.notes = {};
                curPs.notes.content = snNotes;
                curPs.notes.approach = snNotes;
                state.problems[pId] = curPs;
                recoveredCount++;
              }
            }
          });
        }

        // Check Striver
        if (snap.striverState && snap.striverState.problems) {
          Object.keys(snap.striverState.problems).forEach(pId => {
            const snNotes = getCombinedProblemNotes(snap.striverState.problems[pId]);
            const curPs = getStriverProblemState(pId);
            const curNotes = getCombinedProblemNotes(curPs);
            if (snNotes && snNotes.trim().length > 0) {
              saveNoteToVault('striver', pId, snNotes, { title: `Striver #${pId}`, tracker: 'striver' });
              if (!curNotes || curNotes.trim().length === 0) {
                if (!curPs.notes || typeof curPs.notes !== 'object') curPs.notes = {};
                curPs.notes.content = snNotes;
                curPs.notes.approach = snNotes;
                striverState.problems[pId] = curPs;
                recoveredCount++;
              }
            }
          });
        }

        // Check RisingBrain
        if (snap.risingBrainState && snap.risingBrainState.problems) {
          Object.keys(snap.risingBrainState.problems).forEach(pId => {
            const snNotes = getCombinedProblemNotes(snap.risingBrainState.problems[pId]);
            const curPs = getRisingBrainProblemState(pId);
            const curNotes = getCombinedProblemNotes(curPs);
            if (snNotes && snNotes.trim().length > 0) {
              saveNoteToVault('risingbrain', pId, snNotes, { title: `RisingBrain #${pId}`, tracker: 'risingbrain' });
              if (!curNotes || curNotes.trim().length === 0) {
                if (!curPs.notes || typeof curPs.notes !== 'object') curPs.notes = {};
                curPs.notes.content = snNotes;
                curPs.notes.approach = snNotes;
                risingBrainState.problems[pId] = curPs;
                recoveredCount++;
              }
            }
          });
        }

        // Check MIK
        if (snap.mikState && snap.mikState.problems) {
          Object.keys(snap.mikState.problems).forEach(pId => {
            const snNotes = snap.mikState.problems[pId]?.notes || '';
            const curPs = getMikProblemState(pId);
            if (snNotes && snNotes.trim().length > 0) {
              saveNoteToVault('mik', pId, snNotes, { title: `MIK #${pId}`, tracker: 'mik' });
              if (!curPs.notes || curPs.notes.trim().length === 0) {
                curPs.notes = snNotes;
                mikState.problems[pId] = curPs;
                recoveredCount++;
              }
            }
          });
        }
      } catch(err) {}
    });

    // Index all current non-empty notes into vault
    if (state && state.problems) {
      Object.keys(state.problems).forEach(pId => {
        const text = getCombinedProblemNotes(state.problems[pId]);
        if (text && text.trim().length > 0) {
          saveNoteToVault('dsa', pId, text, { title: `DSA #${pId}`, tracker: 'dsa' });
        }
      });
    }
    if (striverState && striverState.problems) {
      Object.keys(striverState.problems).forEach(pId => {
        const text = getCombinedProblemNotes(striverState.problems[pId]);
        if (text && text.trim().length > 0) {
          saveNoteToVault('striver', pId, text, { title: `Striver #${pId}`, tracker: 'striver' });
        }
      });
    }
    if (typeof risingBrainState !== 'undefined' && risingBrainState.problems) {
      Object.keys(risingBrainState.problems).forEach(pId => {
        const text = getCombinedProblemNotes(risingBrainState.problems[pId]);
        if (text && text.trim().length > 0) {
          saveNoteToVault('risingbrain', pId, text, { title: `RisingBrain #${pId}`, tracker: 'risingbrain' });
        }
      });
    }
    if (typeof mikState !== 'undefined' && mikState.problems) {
      Object.keys(mikState.problems).forEach(pId => {
        const text = mikState.problems[pId]?.notes || '';
        if (text && text.trim().length > 0) {
          saveNoteToVault('mik', pId, text, { title: `MIK #${pId}`, tracker: 'mik' });
        }
      });
    }
    if (typeof coreSubjectsNotes === 'object' && coreSubjectsNotes !== null) {
      Object.keys(coreSubjectsNotes).forEach(sId => {
        const text = coreSubjectsNotes[sId] || '';
        if (text && text.trim().length > 0) {
          saveNoteToVault('core_subject', sId, text, { title: `Core Subject: ${sId.toUpperCase()}`, tracker: 'core_subject' });
        }
      });
    }
    if (typeof skillsHubData === 'object' && skillsHubData !== null && skillsHubData.skills) {
      Object.keys(skillsHubData.skills).forEach(sId => {
        const lessons = skillsHubData.skills[sId]?.lessons || {};
        Object.keys(lessons).forEach(lId => {
          const text = lessons[lId]?.notes || '';
          if (text && text.trim().length > 0) {
            saveNoteToVault('skill', lId, text, { title: `Skill Lesson #${lessons[lId].num || lId}`, tracker: 'skill' });
          }
        });
      });
    }

    if (recoveredCount > 0) {
      console.log(`[NOTES RECOVERY] Healed & restored ${recoveredCount} notes from backup history!`);
      saveState();
      saveStriverState();
      saveRisingBrainState();
      if (typeof saveMikState === 'function') saveMikState();
      setTimeout(() => {
        if (typeof showToast === 'function') {
          showToast(`🛡️ Notes Vault: Auto-recovered ${recoveredCount} note(s) from safety backup!`, 'success');
        }
      }, 1000);
    }
    updateStorageCenterVaultCount();
  } catch(e) {
    console.warn('Heal and recover notes error:', e);
  }
}

function openNotesRecoveryVaultModal() {
  renderNotesRecoveryVaultList();
  openModal('modalNotesRecoveryVault');
}

function renderNotesRecoveryVaultList(filterTracker = 'all', searchQuery = '') {
  const container = document.getElementById('vaultNotesListContainer');
  const countEl = document.getElementById('vaultModalTotalCount');
  if (!container) return;

  const vault = getAllNotesFromVault();
  let items = Object.values(vault);

  if (filterTracker !== 'all') {
    items = items.filter(it => it.tracker === filterTracker);
  }
  if (searchQuery && searchQuery.trim()) {
    const q = searchQuery.toLowerCase().trim();
    items = items.filter(it => (it.title && it.title.toLowerCase().includes(q)) || (it.text && it.text.toLowerCase().includes(q)));
  }

  items.sort((a, b) => new Date(b.updatedAt || 0) - new Date(a.updatedAt || 0));

  if (countEl) countEl.textContent = `${items.length} saved note${items.length === 1 ? '' : 's'}`;

  if (items.length === 0) {
    container.innerHTML = `<div style="text-align:center; padding:2.5rem 1rem; color:var(--text-dim);">No saved notes found in recovery vault.</div>`;
    return;
  }

  let html = '';
  items.forEach(it => {
    const badgeColor = {
      'dsa': '#38bdf8',
      'striver': '#10b981',
      'risingbrain': '#a855f7',
      'mik': '#f59e0b',
      'core_subject': '#ec4899',
      'skill': '#6366f1',
      'diary': '#f43f5e'
    }[it.tracker] || '#94a3b8';

    const safeTitle = escapeHtml(it.title || `Item #${it.id}`);
    const timeStr = it.updatedDisplay || formatDateDisplay(it.updatedAt);
    const chars = (it.charCount || it.text.length).toLocaleString();
    const preview = escapeHtml(it.text.substring(0, 220) + (it.text.length > 220 ? '...' : ''));

    html += `
      <div style="padding:0.9rem; margin-bottom:0.65rem; background:var(--surface); border:1px solid var(--border-subtle); border-radius:10px;">
        <div style="display:flex; justify-content:space-between; align-items:center; width:100%; margin-bottom:0.4rem;">
          <div style="display:flex; align-items:center; gap:0.5rem;">
            <span style="font-size:10px; font-weight:700; text-transform:uppercase; padding:2px 8px; border-radius:4px; background:${badgeColor}22; color:${badgeColor}; border:1px solid ${badgeColor}44;">${it.tracker.toUpperCase()}</span>
            <span style="font-weight:700; font-size:13.5px; color:#f1f5f9;">${safeTitle}</span>
          </div>
          <span style="font-size:11px; font-family:var(--font-mono); color:var(--text-dim);">${timeStr} · ${chars} chars</span>
        </div>
        <div style="font-size:12px; color:var(--text-dim); line-height:1.45; font-family:var(--font-mono); white-space:pre-wrap; background:rgba(0,0,0,0.25); padding:0.5rem 0.65rem; border-radius:6px; width:100%; max-height:85px; overflow:hidden; text-overflow:ellipsis;">${preview}</div>
        <div style="display:flex; gap:0.5rem; margin-top:0.6rem; justify-content:flex-end;">
          <button type="button" class="btn btn-secondary btn-sm" onclick="copyVaultNote('${it.key}')" style="font-size:11px; padding:0.25rem 0.6rem;">📋 Copy Markdown</button>
          <button type="button" class="btn btn-primary btn-sm" onclick="restoreNoteFromVault('${it.key}')" style="font-size:11px; padding:0.25rem 0.6rem;">🔄 Restore to Tracker</button>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function copyVaultNote(key) {
  const vault = getAllNotesFromVault();
  const it = vault[key];
  if (!it || !it.text) return;
  navigator.clipboard.writeText(it.text).then(() => {
    if (typeof showToast === 'function') showToast('✓ Note markdown copied to clipboard!', 'success');
  });
}

function restoreNoteFromVault(key) {
  const vault = getAllNotesFromVault();
  const it = vault[key];
  if (!it || !it.text) return;

  if (it.tracker === 'dsa') {
    const ps = getProblemState(it.id);
    if (!ps.notes || typeof ps.notes !== 'object') ps.notes = {};
    ps.notes.content = it.text;
    ps.notes.approach = it.text;
    state.problems[it.id] = ps;
    saveState();
  } else if (it.tracker === 'striver') {
    const ps = getStriverProblemState(it.id);
    if (!ps.notes || typeof ps.notes !== 'object') ps.notes = {};
    ps.notes.content = it.text;
    ps.notes.approach = it.text;
    striverState.problems[it.id] = ps;
    saveStriverState();
  } else if (it.tracker === 'risingbrain') {
    const ps = getRisingBrainProblemState(it.id);
    if (!ps.notes || typeof ps.notes !== 'object') ps.notes = {};
    ps.notes.content = it.text;
    ps.notes.approach = it.text;
    risingBrainState.problems[it.id] = ps;
    saveRisingBrainState();
  } else if (it.tracker === 'mik') {
    const ps = getMikProblemState(it.id);
    ps.notes = it.text;
    mikState.problems[it.id] = ps;
    saveMikState();
  } else if (it.tracker === 'core_subject') {
    coreSubjectsNotes[it.id] = it.text;
    saveCoreSubjectsNotes();
  } else if (it.tracker === 'skill') {
    const skill = getActiveSkill();
    if (skill.lessons && skill.lessons[it.id]) {
      skill.lessons[it.id].notes = it.text;
      saveSkillsHubData();
    }
  }

  if (typeof showToast === 'function') showToast(`✓ Successfully restored note for ${it.title}!`, 'success');
  renderNotesRecoveryVaultList();
}

function downloadAllVaultNotes() {
  const vault = getAllNotesFromVault();
  const str = JSON.stringify(vault, null, 2);
  const blob = new Blob([str], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `notes_recovery_vault_backup_${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
'''

# Place vault_and_merge_logic before `function saveState()`
idx_savestate = content.find('function saveState() {')
if idx_savestate != -1:
    content = content[:idx_savestate] + vault_and_merge_logic + '\n\n' + content[idx_savestate:]
    print("✓ Added Notes Recovery Vault and Smart Merge Engine before saveState()")
else:
    raise ValueError("Could not find saveState in index.html")

# ----------------------------------------------------------------------
# 2. UPGRADE saveState WITH SMART MERGE
# ----------------------------------------------------------------------
old_savestate = '''function saveState() {
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

    localStorage.setItem(STORAGE_KEY_V3, JSON.stringify(state));'''

new_savestate = '''function saveState() {
  try {
    const existingRaw = localStorage.getItem(STORAGE_KEY_V3);
    if (existingRaw) {
      try {
        const parsed = JSON.parse(existingRaw);
        if (parsed && parsed.problems) {
          state.problems = safeMergeProblemCollection(parsed.problems, state.problems, activeModalProbNum);
          if (parsed.maxStreak && parsed.maxStreak > (state.maxStreak || 0)) {
            state.maxStreak = parsed.maxStreak;
          }
        }
      } catch(err) {
        console.warn('Merge check note in saveState:', err);
      }
    }

    // Overwrite guard: Do not overwrite non-empty storage with empty memory state
    const currentDone = Object.values(state.problems).filter(p => p.done).length;
    if (currentDone === 0 && existingRaw) {
      try {
        const parsed = JSON.parse(existingRaw);
        const existingDone = Object.values(parsed.problems || {}).filter(p => p.done).length;
        if (existingDone > 0) {
          console.warn('Safety guard blocked empty overwrite of DSA state. Existing done:', existingDone);
          return;
        }
      } catch(err) {}
    }

    localStorage.setItem(STORAGE_KEY_V3, JSON.stringify(state));'''

if old_savestate in content:
    content = content.replace(old_savestate, new_savestate, 1)
    print("✓ Upgraded saveState() with safe merge guard")
else:
    raise ValueError("Could not find old saveState snippet")

# ----------------------------------------------------------------------
# 3. UPGRADE saveStriverState WITH SMART MERGE
# ----------------------------------------------------------------------
old_striver_save = '''function saveStriverState() {
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

    localStorage.setItem(STORAGE_STRIVER_KEY, JSON.stringify(striverState));'''

new_striver_save = '''function saveStriverState() {
  try {
    const existingRaw = localStorage.getItem(STORAGE_STRIVER_KEY);
    if (existingRaw) {
      try {
        const parsed = JSON.parse(existingRaw);
        if (parsed && parsed.problems) {
          striverState.problems = safeMergeProblemCollection(parsed.problems, striverState.problems, activeModalProbNum);
          if (parsed.maxStreak && parsed.maxStreak > (striverState.maxStreak || 0)) {
            striverState.maxStreak = parsed.maxStreak;
          }
        }
      } catch(err) {
        console.warn('Merge check note in saveStriverState:', err);
      }
    }

    // Overwrite guard: Do not overwrite non-empty storage with empty memory state
    const currentDone = Object.values(striverState.problems).filter(p => p.done).length;
    if (currentDone === 0 && existingRaw) {
      try {
        const parsed = JSON.parse(existingRaw);
        const existingDone = Object.values(parsed.problems || {}).filter(p => p.done).length;
        if (existingDone > 0) {
          console.warn('Safety guard blocked empty overwrite of Striver state. Existing done:', existingDone);
          return;
        }
      } catch(err) {}
    }

    localStorage.setItem(STORAGE_STRIVER_KEY, JSON.stringify(striverState));'''

if old_striver_save in content:
    content = content.replace(old_striver_save, new_striver_save, 1)
    print("✓ Upgraded saveStriverState() with safe merge guard")
else:
    raise ValueError("Could not find old saveStriverState snippet")

# ----------------------------------------------------------------------
# 4. UPGRADE saveRisingBrainState WITH SMART MERGE
# ----------------------------------------------------------------------
old_rb_save = '''function saveRisingBrainState() {
  try {
    // Overwrite guard: Do not overwrite non-empty storage with empty memory state
    const currentDone = Object.values(risingBrainState.problems).filter(p => p.done).length;
    if (currentDone === 0) {
      const existingRaw = localStorage.getItem(STORAGE_RISINGBRAIN_KEY);
      if (existingRaw) {
        try {
          const parsed = JSON.parse(existingRaw);
          const existingDone = Object.values(parsed.problems || {}).filter(p => p.done).length;
          if (existingDone > 0) {
            console.warn('[STORAGEGUARD] Overwrite prevented: Non-empty RisingBrain storage preserved against empty in-memory state.');
            return;
          }
        } catch(err) {}
      }
    }

    localStorage.setItem(STORAGE_RISINGBRAIN_KEY, JSON.stringify(risingBrainState));'''

new_rb_save = '''function saveRisingBrainState() {
  try {
    const existingRaw = localStorage.getItem(STORAGE_RISINGBRAIN_KEY);
    if (existingRaw) {
      try {
        const parsed = JSON.parse(existingRaw);
        if (parsed && parsed.problems) {
          risingBrainState.problems = safeMergeProblemCollection(parsed.problems, risingBrainState.problems, activeModalProbNum);
          if (parsed.maxStreak && parsed.maxStreak > (risingBrainState.maxStreak || 0)) {
            risingBrainState.maxStreak = parsed.maxStreak;
          }
        }
      } catch(err) {
        console.warn('Merge check note in saveRisingBrainState:', err);
      }
    }

    // Overwrite guard: Do not overwrite non-empty storage with empty memory state
    const currentDone = Object.values(risingBrainState.problems).filter(p => p.done).length;
    if (currentDone === 0 && existingRaw) {
      try {
        const parsed = JSON.parse(existingRaw);
        const existingDone = Object.values(parsed.problems || {}).filter(p => p.done).length;
        if (existingDone > 0) {
          console.warn('[STORAGEGUARD] Overwrite prevented: Non-empty RisingBrain storage preserved against empty in-memory state.');
          return;
        }
      } catch(err) {}
    }

    localStorage.setItem(STORAGE_RISINGBRAIN_KEY, JSON.stringify(risingBrainState));'''

if old_rb_save in content:
    content = content.replace(old_rb_save, new_rb_save, 1)
    print("✓ Upgraded saveRisingBrainState() with safe merge guard")
else:
    raise ValueError("Could not find old saveRisingBrainState snippet")

# ----------------------------------------------------------------------
# 5. UPGRADE saveMikState WITH SMART MERGE
# ----------------------------------------------------------------------
old_mik_save = '''function saveMikState() {
  try {
    localStorage.setItem(STORAGE_MIK_KEY, JSON.stringify(mikState));
    if (typeof mirrorToIndexedDB === 'function') mirrorToIndexedDB();
    if (typeof recordSnapshot === 'function') recordSnapshot('auto-mik-state-save');
  } catch (e) {
    console.error('Error saving MIK state:', e);
  }
}'''

new_mik_save = '''function saveMikState() {
  try {
    const existingRaw = localStorage.getItem(STORAGE_MIK_KEY);
    if (existingRaw) {
      try {
        const parsed = JSON.parse(existingRaw);
        if (parsed && parsed.problems) {
          mikState.problems = safeMergeMikProblems(parsed.problems, mikState.problems, typeof activeMikModalProbId !== 'undefined' ? activeMikModalProbId : null);
        }
      } catch (err) {
        console.warn('Merge check note in saveMikState:', err);
      }
    }
    localStorage.setItem(STORAGE_MIK_KEY, JSON.stringify(mikState));
    if (typeof mirrorToIndexedDB === 'function') mirrorToIndexedDB();
    if (typeof recordSnapshot === 'function') recordSnapshot('auto-mik-state-save');
  } catch (e) {
    console.error('Error saving MIK state:', e);
  }
}'''

if old_mik_save in content:
    content = content.replace(old_mik_save, new_mik_save, 1)
    print("✓ Upgraded saveMikState() with safe merge guard")
else:
    raise ValueError("Could not find old saveMikState snippet")

# ----------------------------------------------------------------------
# 6. UPGRADE saveCoreSubjectsNotes WITH SMART MERGE
# ----------------------------------------------------------------------
old_cs_save = '''function saveCoreSubjectsNotes() {
  try {
    localStorage.setItem(CS_STORAGE_KEY_NOTES, JSON.stringify(coreSubjectsNotes));
  } catch (e) {
    console.error('Error saving core subjects notes:', e);
  }
}'''

new_cs_save = '''function saveCoreSubjectsNotes() {
  try {
    const raw = localStorage.getItem(CS_STORAGE_KEY_NOTES);
    if (raw) {
      try {
        const existing = JSON.parse(raw);
        if (existing && typeof existing === 'object') {
          for (const sId of Object.keys(existing)) {
            if (existing[sId] && (!coreSubjectsNotes[sId] || coreSubjectsNotes[sId].trim().length === 0)) {
              coreSubjectsNotes[sId] = existing[sId];
            }
          }
        }
      } catch(err) {}
    }
    localStorage.setItem(CS_STORAGE_KEY_NOTES, JSON.stringify(coreSubjectsNotes));
  } catch (e) {
    console.error('Error saving core subjects notes:', e);
  }
}'''

if old_cs_save in content:
    content = content.replace(old_cs_save, new_cs_save, 1)
    print("✓ Upgraded saveCoreSubjectsNotes() with safe merge guard")
else:
    raise ValueError("Could not find old saveCoreSubjectsNotes snippet")

# ----------------------------------------------------------------------
# 7. UPGRADE saveSkillsHubData WITH SMART MERGE
# ----------------------------------------------------------------------
old_sk_save = '''function saveSkillsHubData() {
  try {
    localStorage.setItem(SKILLS_HUB_STORAGE_KEY, JSON.stringify(skillsHubData));
  } catch (e) {
    console.error('Error saving skills hub data:', e);
  }
  updateSkillsHubStats();
  if (typeof updateHeaderStats === 'function') updateHeaderStats();
}'''

new_sk_save = '''function saveSkillsHubData() {
  try {
    const raw = localStorage.getItem(SKILLS_HUB_STORAGE_KEY);
    if (raw) {
      try {
        const existing = JSON.parse(raw);
        if (existing && existing.skills && skillsHubData && skillsHubData.skills) {
          for (const sId of Object.keys(existing.skills)) {
            if (skillsHubData.skills[sId]) {
              const exLessons = existing.skills[sId].lessons || {};
              const memLessons = skillsHubData.skills[sId].lessons || {};
              for (const lId of Object.keys(exLessons)) {
                if (exLessons[lId]?.notes && (!memLessons[lId]?.notes || memLessons[lId].notes.trim().length === 0)) {
                  if (memLessons[lId]) memLessons[lId].notes = exLessons[lId].notes;
                }
                if (exLessons[lId]?.status === 'completed' && memLessons[lId]?.status !== 'completed') {
                  if (memLessons[lId]) memLessons[lId].status = 'completed';
                }
              }
            }
          }
        }
      } catch(err) {}
    }
    localStorage.setItem(SKILLS_HUB_STORAGE_KEY, JSON.stringify(skillsHubData));
  } catch (e) {
    console.error('Error saving skills hub data:', e);
  }
  updateSkillsHubStats();
  if (typeof updateHeaderStats === 'function') updateHeaderStats();
}'''

if old_sk_save in content:
    content = content.replace(old_sk_save, new_sk_save, 1)
    print("✓ Upgraded saveSkillsHubData() with safe merge guard")
else:
    raise ValueError("Could not find old saveSkillsHubData snippet")

# ----------------------------------------------------------------------
# 8. UPGRADE saveDiaryState WITH SMART MERGE
# ----------------------------------------------------------------------
old_diary_save = '''function saveDiaryState() {
  try {
    localStorage.setItem(STORAGE_DIARY_KEY, JSON.stringify(diaryState));
  } catch(e) {}
}'''

new_diary_save = '''function saveDiaryState() {
  try {
    const raw = localStorage.getItem(STORAGE_DIARY_KEY);
    if (raw) {
      try {
        const existing = JSON.parse(raw);
        if (existing && existing.entries) {
          if (!diaryState.entries) diaryState.entries = {};
          for (const dateKey of Object.keys(existing.entries)) {
            if (!diaryState.entries[dateKey]) {
              diaryState.entries[dateKey] = existing.entries[dateKey];
            } else if (dateKey !== currentDiaryDate) {
              diaryState.entries[dateKey] = existing.entries[dateKey];
            }
          }
        }
      } catch(err) {}
    }
    localStorage.setItem(STORAGE_DIARY_KEY, JSON.stringify(diaryState));
  } catch(e) {}
}'''

if old_diary_save in content:
    content = content.replace(old_diary_save, new_diary_save, 1)
    print("✓ Upgraded saveDiaryState() with safe merge guard")
else:
    raise ValueError("Could not find old saveDiaryState snippet")

# ----------------------------------------------------------------------
# 9. UPGRADE saveProblemNotesExplicitly TO SUPPORT SILENT AND VAULT WRITE
# ----------------------------------------------------------------------
old_pnotes_exp = '''function saveProblemNotesExplicitly() {
  if (!activeModalProbNum) return;
  const isRisingBrain = activeModalTracker === 'risingbrain';
  const isStriver = activeModalTracker === 'striver';
  const ps = isRisingBrain ? getRisingBrainProblemState(activeModalProbNum) : isStriver ? getStriverProblemState(activeModalProbNum) : getProblemState(activeModalProbNum);

  const contentEl = document.getElementById('probNoteContent');
  const text = contentEl ? contentEl.value : '';

  if (!ps.notes || typeof ps.notes !== 'object') {
    ps.notes = { content: '', approach: '', mistakes: '', complexity: '' };
  }
  ps.notes.content = text;
  ps.notes.approach = text; // preserved for legacy compatibility

  if (isRisingBrain) {
    risingBrainState.problems[activeModalProbNum] = ps;
    saveRisingBrainState();
  } else if (isStriver) {
    striverState.problems[activeModalProbNum] = ps;
    saveStriverState();
  } else {
    state.problems[activeModalProbNum] = ps;
    saveState();
  }

  const badge = document.getElementById('probNotesSavedIndicator');
  if (badge) {
    badge.style.display = 'inline-flex';
    setTimeout(() => { if (badge) badge.style.display = 'none'; }, 2000);
  }
  if (typeof showToast === 'function') {
    showToast('Problem notes saved ✓');
  }
  updateProbNotesCharCount(text);
}'''

new_pnotes_exp = '''function saveProblemNotesExplicitly(opts = {}) {
  const silent = opts && opts.silent === true;
  if (!activeModalProbNum) return;
  const isRisingBrain = activeModalTracker === 'risingbrain';
  const isStriver = activeModalTracker === 'striver';
  const ps = isRisingBrain ? getRisingBrainProblemState(activeModalProbNum) : isStriver ? getStriverProblemState(activeModalProbNum) : getProblemState(activeModalProbNum);

  const contentEl = document.getElementById('probNoteContent');
  const text = contentEl ? contentEl.value : '';

  if (!ps.notes || typeof ps.notes !== 'object') {
    ps.notes = { content: '', approach: '', mistakes: '', complexity: '' };
  }
  ps.notes.content = text;
  ps.notes.approach = text;

  if (isRisingBrain) {
    risingBrainState.problems[activeModalProbNum] = ps;
    saveRisingBrainState();
  } else if (isStriver) {
    striverState.problems[activeModalProbNum] = ps;
    saveStriverState();
  } else {
    state.problems[activeModalProbNum] = ps;
    saveState();
  }

  // Record to Notes Recovery Vault
  const titleEl = document.getElementById('revModalProbTitle')?.textContent || `Problem #${activeModalProbNum}`;
  saveNoteToVault(activeModalTracker || 'dsa', activeModalProbNum, text, { title: titleEl, tracker: activeModalTracker || 'dsa' });

  const badge = document.getElementById('probNotesSavedIndicator');
  if (badge) {
    badge.style.display = 'inline-flex';
    setTimeout(() => { if (badge) badge.style.display = 'none'; }, 2000);
  }
  if (!silent && typeof showToast === 'function') {
    showToast('Problem notes saved ✓');
  }
  updateProbNotesCharCount(text);
}'''

if old_pnotes_exp in content:
    content = content.replace(old_pnotes_exp, new_pnotes_exp, 1)
    print("✓ Upgraded saveProblemNotesExplicitly() with options and vault saving")
else:
    raise ValueError("Could not find old saveProblemNotesExplicitly snippet")

# ----------------------------------------------------------------------
# 10. REAL-TIME DEBOUNCED AUTO-SAVE FOR pnoteEditTextarea
# ----------------------------------------------------------------------
old_pnote_input = '''function handlePnoteEditorInput(val) {
  isPnoteDirty = (val !== pnoteOriginalText);
  updatePnoteDirtyState(isPnoteDirty);
  updatePnoteStats(val);

  clearTimeout(pnoteLivePreviewDebounce);
  pnoteLivePreviewDebounce = setTimeout(() => {
    updatePnoteLivePreview();
  }, 120);
}'''

new_pnote_input = '''let pnoteAutoSaveDebounce = null;

function autoSavePnoteSilently() {
  const ta = document.getElementById('pnoteEditTextarea');
  if (!ta) return;
  const text = ta.value;

  // Sync to probNoteContent textarea in modalRevision
  const contentEl = document.getElementById('probNoteContent');
  if (contentEl) {
    contentEl.value = text;
    updateProbNotesCharCount(text);
  }

  saveProblemNotesExplicitly({ silent: true });
  pnoteOriginalText = text;
  isPnoteDirty = false;
  updatePnoteDirtyState(false);

  // Subtle auto-saved badge
  const autoBadge = document.getElementById('pnoteSavedIndicator');
  if (autoBadge) {
    autoBadge.textContent = 'Auto-saved locally ✓';
    autoBadge.style.display = 'inline-flex';
    setTimeout(() => { if (autoBadge) autoBadge.style.display = 'none'; }, 2000);
  }
}

function handlePnoteEditorInput(val) {
  isPnoteDirty = (val !== pnoteOriginalText);
  updatePnoteDirtyState(isPnoteDirty);
  updatePnoteStats(val);

  clearTimeout(pnoteLivePreviewDebounce);
  pnoteLivePreviewDebounce = setTimeout(() => {
    updatePnoteLivePreview();
  }, 120);

  // Continuous auto-save after 400ms typing pause
  clearTimeout(pnoteAutoSaveDebounce);
  pnoteAutoSaveDebounce = setTimeout(() => {
    autoSavePnoteSilently();
  }, 400);
}'''

if old_pnote_input in content:
    content = content.replace(old_pnote_input, new_pnote_input, 1)
    print("✓ Added autoSavePnoteSilently() and debounced auto-save to handlePnoteEditorInput")
else:
    raise ValueError("Could not find old handlePnoteEditorInput snippet")

# ----------------------------------------------------------------------
# 11. AUTO-SAVE ON MODE SWITCH (READ <-> EDIT)
# ----------------------------------------------------------------------
old_pnote_mode = '''function setPnoteMode(mode) {
  pnoteCurrentMode = mode;'''

new_pnote_mode = '''function setPnoteMode(mode) {
  if (pnoteCurrentMode === 'edit' && typeof isPnoteDirty !== 'undefined' && isPnoteDirty) {
    if (typeof autoSavePnoteSilently === 'function') autoSavePnoteSilently();
  }
  pnoteCurrentMode = mode;'''

if old_pnote_mode in content:
    content = content.replace(old_pnote_mode, new_pnote_mode, 1)
    print("✓ Added auto-save on setPnoteMode switch")
else:
    raise ValueError("Could not find old setPnoteMode snippet")

# ----------------------------------------------------------------------
# 12. AUTO-SAVE ON MODAL CLOSE (requestClosePnoteModal)
# ----------------------------------------------------------------------
old_close_pnote = '''function requestClosePnoteModal() {
  if (isPnoteDirty) {
    const shouldSave = confirm('You have unsaved changes in your problem notes.\\n\\nClick OK to SAVE before closing, or CANCEL to discard changes.');
    if (shouldSave) {
      savePnoteExplicitlyFromModal();
      closeModal('modalViewProblemNotes');
      return;
    }
  }
  closeModal('modalViewProblemNotes');
}'''

new_close_pnote = '''function requestClosePnoteModal() {
  if (isPnoteDirty) {
    if (typeof autoSavePnoteSilently === 'function') autoSavePnoteSilently();
  }
  closeModal('modalViewProblemNotes');
}'''

if old_close_pnote in content:
    content = content.replace(old_close_pnote, new_close_pnote, 1)
    print("✓ Upgraded requestClosePnoteModal() to automatically save before closing")
else:
    raise ValueError("Could not find old requestClosePnoteModal snippet")

# ----------------------------------------------------------------------
# 13. UPGRADE closeModal(id) AND ESCAPE & OUTSIDE CLICK HANDLERS
# ----------------------------------------------------------------------
old_close_modal = '''function closeModal(id) {
  const el = document.getElementById(id);
  if(el) el.classList.remove('active');
}

function showToast(message) {
  const container = document.getElementById('toastContainer');
  if(!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>✓</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 250);
  }, 3000);
}

/* Keyboard shortcuts */
document.addEventListener('keydown', (e) => {
  if(e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
  }
});

/* Close modals when clicking outside */
document.querySelectorAll('.modal-overlay').forEach(modal => {
  modal.addEventListener('click', (e) => {
    if(e.target === modal) modal.classList.remove('active');
  });
});'''

new_close_modal = '''function flushAllActiveNotesDrafts() {
  try {
    if (typeof isPnoteDirty !== 'undefined' && isPnoteDirty) {
      if (typeof autoSavePnoteSilently === 'function') autoSavePnoteSilently();
    }
    const probContentEl = document.getElementById('probNoteContent');
    if (probContentEl && activeModalProbNum) {
      if (typeof saveProblemNotesExplicitly === 'function') saveProblemNotesExplicitly({ silent: true });
    }
    const mikNotesEl = document.getElementById('mikModalNotesTextarea');
    if (mikNotesEl && typeof activeMikModalProbId !== 'undefined' && activeMikModalProbId) {
      if (typeof saveMikModalNotesExplicitly === 'function') saveMikModalNotesExplicitly({ silent: true });
    }
    if (typeof currentViewingSubjectId !== 'undefined' && currentViewingSubjectId) {
      if (typeof saveCoreSubjectNotesExplicitly === 'function') saveCoreSubjectNotesExplicitly(currentViewingSubjectId);
    }
    if (typeof currentViewingLessonId !== 'undefined' && currentViewingLessonId) {
      if (typeof saveSkillLessonNotesExplicitly === 'function') saveSkillLessonNotesExplicitly(currentViewingLessonId);
    }
    if (typeof saveDiaryFromInputs === 'function' && typeof isViewActive === 'function' && isViewActive('diary')) {
      saveDiaryFromInputs();
    }
  } catch(e) {
    console.warn('Flush notes note:', e);
  }
}

function closeModal(id) {
  if (id === 'modalViewProblemNotes') {
    if (typeof isPnoteDirty !== 'undefined' && isPnoteDirty) {
      if (typeof autoSavePnoteSilently === 'function') autoSavePnoteSilently();
    }
  } else if (id === 'modalRevision') {
    if (typeof saveProblemNotesExplicitly === 'function' && activeModalProbNum) {
      saveProblemNotesExplicitly({ silent: true });
    }
  } else if (id === 'modalMikProblemDetail') {
    if (typeof saveMikModalNotesExplicitly === 'function' && typeof activeMikModalProbId !== 'undefined' && activeMikModalProbId) {
      saveMikModalNotesExplicitly({ silent: true });
    }
  } else if (id === 'modalViewCoreSubjectNotes') {
    if (typeof currentViewingSubjectId !== 'undefined' && currentViewingSubjectId) {
      if (typeof saveCoreSubjectNotesExplicitly === 'function') saveCoreSubjectNotesExplicitly(currentViewingSubjectId);
    }
  }
  const el = document.getElementById(id);
  if(el) el.classList.remove('active');
}

function showToast(message) {
  const container = document.getElementById('toastContainer');
  if(!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>✓</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    setTimeout(() => toast.remove(), 250);
  }, 3000);
}

/* Keyboard shortcuts */
document.addEventListener('keydown', (e) => {
  if(e.key === 'Escape') {
    flushAllActiveNotesDrafts();
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
  }
});

/* Close modals when clicking outside */
document.querySelectorAll('.modal-overlay').forEach(modal => {
  modal.addEventListener('click', (e) => {
    if(e.target === modal) {
      closeModal(modal.id);
    }
  });
});

window.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') flushAllActiveNotesDrafts();
});
window.addEventListener('beforeunload', () => {
  flushAllActiveNotesDrafts();
});
window.addEventListener('blur', () => {
  flushAllActiveNotesDrafts();
});'''

if old_close_modal in content:
    content = content.replace(old_close_modal, new_close_modal, 1)
    print("✓ Upgraded closeModal(), Escape key, and outside click with auto-save guards")
else:
    raise ValueError("Could not find old closeModal snippet")

# ----------------------------------------------------------------------
# 14. EXPAND MULTI-WINDOW STORAGE LISTENER FOR ALL SECTIONS
# ----------------------------------------------------------------------
old_storage_listener = '''// Cross-Tab LocalStorage Listener for DSA <-> RisingBrain
window.addEventListener('storage', function(e) {
  if (e.key === STORAGE_KEY_V3) {
    loadState();
    if (isViewActive('dsa')) renderDsaContent();
    updateDsaStats();
    updateHeaderStats();
  } else if (e.key === STORAGE_RISINGBRAIN_KEY) {
    loadRisingBrainState();
    if (isViewActive('risingbrain')) renderRisingBrainContent();
    updateRisingBrainStats();
    updateHeaderStats();
  } else if (e.key === STORAGE_MIK_KEY) {
    if (typeof loadMikState === 'function') loadMikState();
    if (isViewActive('mik')) renderMikContent();
    if (typeof updateMikStats === 'function') updateMikStats();
    updateHeaderStats();
  }
});'''

new_storage_listener = '''// Comprehensive Cross-Window / Multi-Tab Synchronization Listener
window.addEventListener('storage', function(e) {
  if (!e.key) return;

  if (e.key === STORAGE_KEY_V3) {
    loadState();
    if (typeof isViewActive === 'function' && isViewActive('dsa')) renderDsaContent();
    updateDsaStats();
    updateHeaderStats();
    if (activeModalProbNum && activeModalTracker === 'dsa') {
      const ps = getProblemState(activeModalProbNum);
      const newText = getCombinedProblemNotes(ps);
      const noteTa = document.getElementById('probNoteContent');
      if (noteTa && document.activeElement !== noteTa) {
        noteTa.value = newText;
        updateProbNotesCharCount(newText);
      }
      const pnoteTa = document.getElementById('pnoteEditTextarea');
      if (pnoteTa && document.activeElement !== pnoteTa && (!isPnoteDirty || isPnoteDirty === false)) {
        pnoteTa.value = newText;
        renderPnoteReadingView(newText);
      }
    }
  } else if (e.key === STORAGE_STRIVER_KEY) {
    loadStriverState();
    if (typeof isViewActive === 'function' && isViewActive('striver')) renderStriverContent();
    if (typeof updateStriverStepDropdown === 'function') updateStriverStepDropdown();
    updateHeaderStats();
    if (activeModalProbNum && activeModalTracker === 'striver') {
      const ps = getStriverProblemState(activeModalProbNum);
      const newText = getCombinedProblemNotes(ps);
      const noteTa = document.getElementById('probNoteContent');
      if (noteTa && document.activeElement !== noteTa) {
        noteTa.value = newText;
        updateProbNotesCharCount(newText);
      }
      const pnoteTa = document.getElementById('pnoteEditTextarea');
      if (pnoteTa && document.activeElement !== pnoteTa && (!isPnoteDirty || isPnoteDirty === false)) {
        pnoteTa.value = newText;
        renderPnoteReadingView(newText);
      }
    }
  } else if (e.key === STORAGE_RISINGBRAIN_KEY) {
    loadRisingBrainState();
    if (typeof isViewActive === 'function' && isViewActive('risingbrain')) renderRisingBrainContent();
    updateRisingBrainStats();
    updateHeaderStats();
    if (activeModalProbNum && activeModalTracker === 'risingbrain') {
      const ps = getRisingBrainProblemState(activeModalProbNum);
      const newText = getCombinedProblemNotes(ps);
      const noteTa = document.getElementById('probNoteContent');
      if (noteTa && document.activeElement !== noteTa) {
        noteTa.value = newText;
        updateProbNotesCharCount(newText);
      }
      const pnoteTa = document.getElementById('pnoteEditTextarea');
      if (pnoteTa && document.activeElement !== pnoteTa && (!isPnoteDirty || isPnoteDirty === false)) {
        pnoteTa.value = newText;
        renderPnoteReadingView(newText);
      }
    }
  } else if (e.key === STORAGE_MIK_KEY) {
    if (typeof loadMikState === 'function') loadMikState();
    if (typeof isViewActive === 'function' && isViewActive('mik')) renderMikContent();
    if (typeof updateMikStats === 'function') updateMikStats();
    updateHeaderStats();
    if (typeof activeMikModalProbId !== 'undefined' && activeMikModalProbId) {
      const ps = getMikProblemState(activeMikModalProbId);
      const mikTa = document.getElementById('mikModalNotesTextarea');
      if (mikTa && document.activeElement !== mikTa) {
        mikTa.value = ps.notes || '';
      }
    }
  } else if (e.key === CS_STORAGE_KEY_NOTES) {
    try {
      const rawNotes = localStorage.getItem(CS_STORAGE_KEY_NOTES);
      coreSubjectsNotes = rawNotes ? JSON.parse(rawNotes) : {};
      if (typeof isViewActive === 'function' && isViewActive('coresubjects')) renderCoreSubjectsView();
      if (typeof currentViewingSubjectId !== 'undefined' && currentViewingSubjectId) {
        const display = document.getElementById('csViewNotesContentDisplay');
        const text = coreSubjectsNotes[currentViewingSubjectId] || '';
        if (display) display.innerHTML = renderMarkdownToHtml(text);
      }
    } catch(err) {}
  } else if (e.key === CS_STORAGE_KEY_STATE) {
    try {
      const rawState = localStorage.getItem(CS_STORAGE_KEY_STATE);
      coreSubjectsState = rawState ? JSON.parse(rawState) : {};
      if (typeof isViewActive === 'function' && isViewActive('coresubjects')) renderCoreSubjectsView();
      updateCoreSubjectsStats();
    } catch(err) {}
  } else if (e.key === SKILLS_HUB_STORAGE_KEY) {
    if (typeof loadSkillsHubData === 'function') loadSkillsHubData();
    if (typeof isViewActive === 'function' && isViewActive('skills')) renderSkillsHubView();
    updateSkillsHubStats();
  } else if (e.key === STORAGE_DIARY_KEY) {
    try {
      const rawDiary = localStorage.getItem(STORAGE_DIARY_KEY);
      if (rawDiary) diaryState = JSON.parse(rawDiary);
      if (typeof isViewActive === 'function' && isViewActive('diary')) renderDiaryView();
    } catch(err) {}
  } else if (e.key === STORAGE_PLANNER_KEY || e.key === 'planner_tasks') {
    try {
      const rawPlanner = localStorage.getItem(STORAGE_PLANNER_KEY);
      if (rawPlanner) plannerState = JSON.parse(rawPlanner);
      if (typeof isViewActive === 'function' && isViewActive('planner')) renderPlannerView();
    } catch(err) {}
  } else if (e.key === STORAGE_STUDY_KEY) {
    try {
      const rawStudy = localStorage.getItem(STORAGE_STUDY_KEY);
      if (rawStudy) studyState = JSON.parse(rawStudy);
      if (typeof isViewActive === 'function' && isViewActive('clock')) renderStudyClockView();
    } catch(err) {}
  } else if (e.key === STORAGE_NOTES_VAULT_KEY) {
    updateStorageCenterVaultCount();
  }
});'''

if old_storage_listener in content:
    content = content.replace(old_storage_listener, new_storage_listener, 1)
    print("✓ Replaced storage listener with comprehensive multi-window synchronizer")
else:
    raise ValueError("Could not find old storage listener snippet")

# ----------------------------------------------------------------------
# 15. CALL healAndRecoverNotesOnStartup IN init()
# ----------------------------------------------------------------------
old_init_head = '''function init() {
  handleVersionUpgradeArchiving();
  initIndexedDB();
  loadState();
  loadStriverState();
  loadRisingBrainState();
  if (typeof loadMikState === 'function') loadMikState();
  loadOtherStates();
  reconcileDsaRbOnStartup();'''

new_init_head = '''function init() {
  handleVersionUpgradeArchiving();
  initIndexedDB();
  loadState();
  loadStriverState();
  loadRisingBrainState();
  if (typeof loadMikState === 'function') loadMikState();
  loadOtherStates();
  reconcileDsaRbOnStartup();
  healAndRecoverNotesOnStartup();'''

if old_init_head in content:
    content = content.replace(old_init_head, new_init_head, 1)
    print("✓ Added healAndRecoverNotesOnStartup() call to init()")
else:
    raise ValueError("Could not find old init snippet")

# ----------------------------------------------------------------------
# 16. ADD NOTES RECOVERY VAULT CARD TO STORAGE CENTER UI
# ----------------------------------------------------------------------
sc_card_insertion_target = '<div class="sc-metric-card" id="scCardOriginQuota">'
sc_vault_card_html = '''<!-- Card 0: Notes Recovery Vault -->
    <div class="sc-metric-card" id="scCardNotesVault" style="border-color: rgba(56, 189, 248, 0.4); background: linear-gradient(135deg, rgba(56, 189, 248, 0.08) 0%, rgba(15, 23, 42, 0.6) 100%);">
      <div class="sc-metric-top">
        <span class="sc-metric-label">Notes Recovery Vault</span>
        <span class="sc-metric-pill sc-pill-good" id="scVaultHealthPill">Active 🛡️</span>
      </div>
      <div class="sc-metric-value" style="font-size: 22px; color: #38bdf8;">
        <span id="scVaultNoteCount">0</span> <span style="font-size:14px; font-weight:400; color:var(--text-dim);">Notes Secured</span>
      </div>
      <div class="sc-metric-sub" style="margin-top:0.35rem; font-size:11.5px; color:var(--text-dim);">
        Cross-window real-time backup across DSA, Striver, MIK & Core Subjects.
      </div>
      <button type="button" class="btn btn-secondary btn-sm" onclick="openNotesRecoveryVaultModal()" style="margin-top: 0.65rem; width:100%; font-size:11.5px; border-color: rgba(56, 189, 248, 0.4);">
        🔍 Inspect & Restore Notes Vault
      </button>
    </div>

    '''

if sc_card_insertion_target in content:
    content = content.replace(sc_card_insertion_target, sc_vault_card_html + sc_card_insertion_target, 1)
    print("✓ Added Notes Recovery Vault card into Data & Storage Center metrics grid")
else:
    raise ValueError("Could not find scCardOriginQuota target in Storage Center")

# ----------------------------------------------------------------------
# 17. ADD NOTES RECOVERY VAULT MODAL HTML
# ----------------------------------------------------------------------
vault_modal_html = '''
<!-- MODAL: NOTES RECOVERY VAULT INSPECTOR & RESTORER -->
<div class="modal-overlay" id="modalNotesRecoveryVault" style="z-index: 1250;">
  <div class="modal-card" style="max-width: 900px; width: 95%; max-height: 90vh; display: flex; flex-direction: column; padding: 1.5rem; background: var(--surface); border: 1px solid rgba(56, 189, 248, 0.4); border-radius: var(--radius-xl); box-shadow: 0 25px 60px rgba(0,0,0,0.7);">
    <!-- Modal Header -->
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.85rem;">
      <div style="display:flex; align-items:center; gap:0.75rem;">
        <div style="font-size: 26px;">🛡️</div>
        <div>
          <h2 style="font-family: var(--font-heading); font-size: 18px; font-weight: 700; color: #f8fafc; margin: 0;">Notes Recovery Vault</h2>
          <p style="font-size: 12.5px; color: var(--text-dim); margin: 0.2rem 0 0;">Inspect, copy, or restore all notes automatically preserved across multi-tab edits and sessions.</p>
        </div>
      </div>
      <div style="display:flex; align-items:center; gap:0.5rem;">
        <button type="button" class="btn btn-secondary btn-sm" onclick="downloadAllVaultNotes()" title="Download entire notes vault as JSON" style="font-size:11.5px;">
          📥 Download JSON
        </button>
        <button type="button" class="modal-close" onclick="closeModal('modalNotesRecoveryVault')" style="font-size: 18px; background:transparent; border:none; color:var(--text-dim); cursor:pointer;">✕</button>
      </div>
    </div>

    <!-- Filter and Search Toolbar -->
    <div style="display: flex; flex-wrap: wrap; gap: 0.6rem; align-items: center; justify-content: space-between; margin-bottom: 1rem; background: rgba(0,0,0,0.25); padding: 0.65rem 0.85rem; border-radius: 8px;">
      <div style="display: flex; gap: 0.4rem; overflow-x: auto; max-width: 100%;">
        <button type="button" class="fpill active" onclick="document.querySelectorAll('#vaultFilterGroup .fpill').forEach(b=>b.classList.remove('active')); this.classList.add('active'); renderNotesRecoveryVaultList('all', document.getElementById('vaultSearchInput')?.value)" id="vaultF_all" style="font-size:11px; padding:3px 10px;">All Notes</button>
        <button type="button" class="fpill" onclick="document.querySelectorAll('#vaultFilterGroup .fpill').forEach(b=>b.classList.remove('active')); this.classList.add('active'); renderNotesRecoveryVaultList('dsa', document.getElementById('vaultSearchInput')?.value)" id="vaultF_dsa" style="font-size:11px; padding:3px 10px;">DSA Patterns</button>
        <button type="button" class="fpill" onclick="document.querySelectorAll('#vaultFilterGroup .fpill').forEach(b=>b.classList.remove('active')); this.classList.add('active'); renderNotesRecoveryVaultList('striver', document.getElementById('vaultSearchInput')?.value)" id="vaultF_striver" style="font-size:11px; padding:3px 10px;">Striver A2Z</button>
        <button type="button" class="fpill" onclick="document.querySelectorAll('#vaultFilterGroup .fpill').forEach(b=>b.classList.remove('active')); this.classList.add('active'); renderNotesRecoveryVaultList('risingbrain', document.getElementById('vaultSearchInput')?.value)" id="vaultF_rb" style="font-size:11px; padding:3px 10px;">RisingBrain</button>
        <button type="button" class="fpill" onclick="document.querySelectorAll('#vaultFilterGroup .fpill').forEach(b=>b.classList.remove('active')); this.classList.add('active'); renderNotesRecoveryVaultList('mik', document.getElementById('vaultSearchInput')?.value)" id="vaultF_mik" style="font-size:11px; padding:3px 10px;">MIK DSA</button>
        <button type="button" class="fpill" onclick="document.querySelectorAll('#vaultFilterGroup .fpill').forEach(b=>b.classList.remove('active')); this.classList.add('active'); renderNotesRecoveryVaultList('core_subject', document.getElementById('vaultSearchInput')?.value)" id="vaultF_core" style="font-size:11px; padding:3px 10px;">Core Subjects</button>
        <button type="button" class="fpill" onclick="document.querySelectorAll('#vaultFilterGroup .fpill').forEach(b=>b.classList.remove('active')); this.classList.add('active'); renderNotesRecoveryVaultList('skill', document.getElementById('vaultSearchInput')?.value)" id="vaultF_skill" style="font-size:11px; padding:3px 10px;">Skills Hub</button>
      </div>
      <div style="display:flex; align-items:center; gap:0.5rem; flex: 1; max-width: 260px; min-width: 180px;">
        <input type="text" id="vaultSearchInput" placeholder="Search notes..." class="form-input" style="padding: 0.35rem 0.65rem; font-size: 12px; width: 100%; border-radius: 6px;" oninput="renderNotesRecoveryVaultList(document.querySelector('#vaultFilterGroup .fpill.active')?.id?.replace('vaultF_','') || 'all', this.value)">
      </div>
    </div>

    <!-- Notes List Container -->
    <div id="vaultNotesListContainer" style="flex: 1; overflow-y: auto; padding-right: 0.25rem; max-height: calc(85vh - 200px);"></div>

    <!-- Modal Footer -->
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid var(--border-subtle); font-size: 12px; color: var(--text-dim);">
      <span id="vaultModalTotalCount">0 saved notes</span>
      <button type="button" class="btn btn-secondary btn-sm" onclick="closeModal('modalNotesRecoveryVault')">Close</button>
    </div>
  </div>
</div>
'''

# Place modal before closing </body>
idx_body = content.rfind('</body>')
if idx_body != -1:
    content = content[:idx_body] + vault_modal_html + '\n' + content[idx_body:]
    print("✓ Added Notes Recovery Vault modal HTML before </body>")
else:
    raise ValueError("Could not find closing </body> tag in index.html")

# Write updated content
with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nSuccessfully wrote updated {TARGET_FILE} ({len(content)} chars)")
