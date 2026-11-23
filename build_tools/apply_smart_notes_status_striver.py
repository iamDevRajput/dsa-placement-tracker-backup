#!/usr/bin/env python3
import os
import shutil

TARGET_FILE = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"
BACKUP_FILE = "/Users/devrajput/@Resources/Tracker/build_tools/index.html.pre_striver_smart_notes_bak"

print("Step 1: Creating safety backup before Striver Smart Notes enhancement...")
shutil.copyfile(TARGET_FILE, BACKUP_FILE)
print(f"Safety backup saved to {BACKUP_FILE}")

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# ----------------------------------------------------------------------
# 1. ADD CSS STYLING FOR SMART NOTES BUTTONS
# ----------------------------------------------------------------------
css_notes_rules = '''
/* SMART NOTES STATUS INDICATOR STYLING */
.rb-notes-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 3px !important;
  padding: 4px 8px !important;
  border-radius: 6px !important;
  cursor: pointer !important;
  transition: all 0.18s ease !important;
  user-select: none !important;
  line-height: 1 !important;
}

.rb-notes-btn.no-notes {
  background: rgba(255, 255, 255, 0.03) !important;
  color: var(--text-dim, #94a3b8) !important;
  border: 1px solid rgba(255, 255, 255, 0.09) !important;
}

.rb-notes-btn.no-notes:hover {
  background: rgba(255, 255, 255, 0.09) !important;
  color: #f1f5f9 !important;
  border-color: rgba(255, 255, 255, 0.22) !important;
  transform: translateY(-1px);
}

.rb-notes-btn.has-notes {
  background: rgba(16, 185, 129, 0.14) !important;
  color: #10b981 !important;
  border: 1px solid rgba(16, 185, 129, 0.45) !important;
  box-shadow: 0 0 8px rgba(16, 185, 129, 0.18);
}

.rb-notes-btn.has-notes:hover {
  background: rgba(16, 185, 129, 0.22) !important;
  border-color: rgba(16, 185, 129, 0.75) !important;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.35);
  transform: translateY(-1px);
}

.rb-notes-indicator-icon {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  line-height: 1;
}

.rb-notes-badge-check {
  font-size: 11px;
  font-weight: 800;
  color: #10b981;
  line-height: 1;
}
'''

# Place CSS right before closing </style>
idx_style = content.find('</style>')
if idx_style != -1:
    content = content[:idx_style] + css_notes_rules + '\n' + content[idx_style:]
    print("✓ Added smart notes CSS styling into <style>")
else:
    raise ValueError("Could not find closing </style> tag in index.html")

# ----------------------------------------------------------------------
# 2. ADD NOTE HELPERS & clearNoteFromVault
# ----------------------------------------------------------------------
js_helpers = '''
function hasProblemNotes(ps) {
  if (!ps || !ps.notes) return false;
  if (typeof ps.notes === 'string') return ps.notes.trim().length > 0;
  if (typeof ps.notes === 'object') {
    if (typeof ps.notes.content === 'string' && ps.notes.content.trim().length > 0) return true;
    if (typeof ps.notes.approach === 'string' && ps.notes.approach.trim().length > 0) return true;
    if (typeof ps.notes.mistakes === 'string' && ps.notes.mistakes.trim().length > 0) return true;
  }
  return false;
}

function striverProblemHasNotes(n) {
  const ps = getStriverProblemState(n);
  if (hasProblemNotes(ps)) return true;
  if (typeof getNoteFromVault === 'function') {
    const v = getNoteFromVault('striver', n);
    if (v && typeof v.text === 'string' && v.text.trim().length > 0) return true;
  }
  return false;
}

function clearNoteFromVault(tracker, probId) {
  try {
    const raw = localStorage.getItem(STORAGE_NOTES_VAULT_KEY);
    if (!raw) return;
    const vault = JSON.parse(raw) || {};
    const key = `${tracker}_${probId}`;
    if (vault[key]) {
      delete vault[key];
      localStorage.setItem(STORAGE_NOTES_VAULT_KEY, JSON.stringify(vault));
      if (typeof updateStorageCenterVaultCount === 'function') updateStorageCenterVaultCount();
    }
  } catch(e) {}
}

function updateStriverProblemNotesButton(probNum) {
  const btn = document.getElementById(`striver-notes-btn-${probNum}`);
  const hasNotes = striverProblemHasNotes(probNum);
  if (btn) {
    btn.className = `rb-action-btn rb-notes-btn ${hasNotes ? 'has-notes' : 'no-notes'}`;
    btn.title = hasNotes ? 'Notes Saved – Click to View/Edit' : 'No Notes – Click to Add';
    btn.innerHTML = hasNotes ? `
      <span class="rb-notes-indicator-icon">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        <span class="rb-notes-badge-check">✓</span>
      </span>
    ` : `
      <span class="rb-notes-indicator-icon">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      </span>
    `;
  }
}
'''

# Place JS helpers before `function renderStriverContent()`
idx_render_striver = content.find('function renderStriverContent() {')
if idx_render_striver != -1:
    content = content[:idx_render_striver] + js_helpers + '\n\n' + content[idx_render_striver:]
    print("✓ Added hasProblemNotes, striverProblemHasNotes, clearNoteFromVault, and updateStriverProblemNotesButton")
else:
    raise ValueError("Could not find function renderStriverContent in index.html")

# ----------------------------------------------------------------------
# 3. ADD NOTES FILTER PILLS IN STRIVER HTML
# ----------------------------------------------------------------------
striver_filter_target = '''            <button class="rb-pill" id="f-striver-never" onclick="setStriverFilter('never', this)">Never Revised</button>
            <button class="rb-pill" id="f-striver-mastered" onclick="setStriverFilter('mastered', this)">👑 Mastered</button>
          </div>'''

striver_filter_replacement = '''            <button class="rb-pill" id="f-striver-never" onclick="setStriverFilter('never', this)">Never Revised</button>
            <button class="rb-pill" id="f-striver-mastered" onclick="setStriverFilter('mastered', this)">👑 Mastered</button>
          </div>

          <div class="rb-pill-divider"></div>

          <div class="rb-pill-group">
            <button class="rb-pill" id="f-striver-notes-has" onclick="setStriverFilter('has_notes', this)" title="Show questions with saved notes">
              <span style="color:#10b981; font-weight:800;">✓</span> With Notes <span class="rb-pill-count" id="striver-stat-chip-hasnotes">0</span>
            </button>
            <button class="rb-pill" id="f-striver-notes-no" onclick="setStriverFilter('no_notes', this)" title="Show questions without notes">
              Without Notes <span class="rb-pill-count" id="striver-stat-chip-nonotes">455</span>
            </button>
          </div>'''

if striver_filter_target in content:
    content = content.replace(striver_filter_target, striver_filter_replacement, 1)
    print("✓ Added With Notes and Without Notes filter pills to Striver controls row")
else:
    raise ValueError("Could not find striver_filter_target in index.html")

# ----------------------------------------------------------------------
# 4. UPDATE renderStriverContent TO SUPPORT NOTES FILTER & SMART ICON
# ----------------------------------------------------------------------
old_filter_checks = '''      else if (currentStriverFilter === 'never') matchesFilter = ps.done && (ps.revisionCount || 0) === 0;
      else if (currentStriverFilter === 'mastered') matchesFilter = (ps.revisionCount || 0) >= 3 || ps.status === 'MASTERED';'''

new_filter_checks = '''      else if (currentStriverFilter === 'never') matchesFilter = ps.done && (ps.revisionCount || 0) === 0;
      else if (currentStriverFilter === 'mastered') matchesFilter = (ps.revisionCount || 0) >= 3 || ps.status === 'MASTERED';
      else if (currentStriverFilter === 'has_notes') matchesFilter = striverProblemHasNotes(p.n);
      else if (currentStriverFilter === 'no_notes') matchesFilter = !striverProblemHasNotes(p.n);'''

if old_filter_checks in content:
    content = content.replace(old_filter_checks, new_filter_checks, 1)
    print("✓ Added has_notes and no_notes filter logic to renderStriverContent()")
else:
    raise ValueError("Could not find old_filter_checks in renderStriverContent")

# Update row rendering in renderStriverContent
old_striver_row_head = '''              ${visibleProblems.map(p => {
                const ps = getStriverProblemState(p.n);
                const isDone = !!ps.done;
                const isStarred = !!ps.starred;'''

new_striver_row_head = '''              ${visibleProblems.map(p => {
                const ps = getStriverProblemState(p.n);
                const isDone = !!ps.done;
                const isStarred = !!ps.starred;
                const hasNotes = striverProblemHasNotes(p.n);'''

if old_striver_row_head in content:
    content = content.replace(old_striver_row_head, new_striver_row_head, 1)
    print("✓ Added hasNotes resolution to problem mapping in renderStriverContent")
else:
    raise ValueError("Could not find old_striver_row_head in renderStriverContent")

# Update the notes button in the row
old_notes_btn_snippet = '''<button class="rb-action-btn" onclick="openRevisionModal(${p.n}, 'striver')" title="Notes & History" style="padding:4px 8px; font-size:12px;">📝</button>'''

new_notes_btn_snippet = '''<button class="rb-action-btn rb-notes-btn ${hasNotes ? 'has-notes' : 'no-notes'}" id="striver-notes-btn-${p.n}" onclick="openRevisionModal(${p.n}, 'striver')" title="${hasNotes ? 'Notes Saved – Click to View/Edit' : 'No Notes – Click to Add'}" style="padding:4px 8px; font-size:12px;">
                        ${hasNotes ? `
                          <span class="rb-notes-indicator-icon">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                            <span class="rb-notes-badge-check">✓</span>
                          </span>
                        ` : `
                          <span class="rb-notes-indicator-icon">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                          </span>
                        `}
                      </button>'''

if old_notes_btn_snippet in content:
    content = content.replace(old_notes_btn_snippet, new_notes_btn_snippet, 1)
    print("✓ Replaced neutral notes button with dynamic Smart Notes Status Indicator")
else:
    raise ValueError("Could not find old_notes_btn_snippet in index.html")

# ----------------------------------------------------------------------
# 5. UPDATE updateStriverStats TO CALCULATE With Notes & Without Notes COUNTS
# ----------------------------------------------------------------------
old_update_stats_tail = '''  const chipRev = document.getElementById('striver-stat-chip-needsrev');
  if (chipRev) chipRev.textContent = `🟣 ${needsRevCount}`;'''

new_update_stats_tail = '''  const chipRev = document.getElementById('striver-stat-chip-needsrev');
  if (chipRev) chipRev.textContent = `🟣 ${needsRevCount}`;

  let withNotesCount = 0;
  let withoutNotesCount = 0;
  STRIVER_DATA.forEach(s => {
    s.problems.forEach(p => {
      if (striverProblemHasNotes(p.n)) withNotesCount++;
      else withoutNotesCount++;
    });
  });

  const chipWithNotes = document.getElementById('striver-stat-chip-hasnotes');
  if (chipWithNotes) chipWithNotes.textContent = String(withNotesCount);

  const chipWithoutNotes = document.getElementById('striver-stat-chip-nonotes');
  if (chipWithoutNotes) chipWithoutNotes.textContent = String(withoutNotesCount);'''

if old_update_stats_tail in content:
    content = content.replace(old_update_stats_tail, new_update_stats_tail, 1)
    print("✓ Added withNotesCount and withoutNotesCount calculations in updateStriverStats()")
else:
    raise ValueError("Could not find old_update_stats_tail in updateStriverStats")

# ----------------------------------------------------------------------
# 6. TRIGGER REAL-TIME ICON UPDATE ON SAVE & CLEAR IN saveProblemNotesExplicitly
# ----------------------------------------------------------------------
old_pnotes_save_end = '''  // Record to Notes Recovery Vault
  const titleEl = document.getElementById('revModalProbTitle')?.textContent || `Problem #${activeModalProbNum}`;
  saveNoteToVault(activeModalTracker || 'dsa', activeModalProbNum, text, { title: titleEl, tracker: activeModalTracker || 'dsa' });'''

new_pnotes_save_end = '''  // Record to Notes Recovery Vault or clear if emptied
  const titleEl = document.getElementById('revModalProbTitle')?.textContent || `Problem #${activeModalProbNum}`;
  if (!text || !text.trim()) {
    if (typeof clearNoteFromVault === 'function') {
      clearNoteFromVault(activeModalTracker || 'dsa', activeModalProbNum);
    }
  } else {
    saveNoteToVault(activeModalTracker || 'dsa', activeModalProbNum, text, { title: titleEl, tracker: activeModalTracker || 'dsa' });
  }

  // Real-time update of Striver Notes Status Indicator
  if (activeModalTracker === 'striver' && activeModalProbNum) {
    if (typeof updateStriverProblemNotesButton === 'function') {
      updateStriverProblemNotesButton(activeModalProbNum);
    }
    if (typeof updateStriverStats === 'function') {
      updateStriverStats();
    }
    if (typeof currentStriverFilter !== 'undefined' && (currentStriverFilter === 'has_notes' || currentStriverFilter === 'no_notes')) {
      if (typeof renderStriverContent === 'function') renderStriverContent();
    }
  }'''

if old_pnotes_save_end in content:
    content = content.replace(old_pnotes_save_end, new_pnotes_save_end, 1)
    print("✓ Connected saveProblemNotesExplicitly() to real-time Striver Notes indicator update")
else:
    raise ValueError("Could not find old_pnotes_save_end in saveProblemNotesExplicitly")

# Write updated content
with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nSuccessfully updated {TARGET_FILE} ({len(content)} chars)")
