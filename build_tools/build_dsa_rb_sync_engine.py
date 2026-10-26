import json, sys

print("Loading sync map...")
with open("dsa_rb_sync_map.json") as f:
    sync_map = json.load(f)

print(f"Loaded {sync_map['total_pairs']} bidirectional pairs.")

with open("/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html") as f:
    html = f.read()

# 1. Add CSS for .rb-sync-indicator
sync_css = """
/* DSA <-> RisingBrain Synchronization Indicator */
.rb-sync-indicator {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-size: 10px;
  font-weight: 600;
  color: var(--accent, #10b981);
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.22);
  padding: 1px 7px;
  border-radius: 9999px;
  margin-left: 6px;
  vertical-align: middle;
  line-height: 1.4;
  cursor: help;
  transition: all 0.2s ease;
  letter-spacing: 0.01em;
}
.rb-sync-indicator:hover {
  background: rgba(16, 185, 129, 0.16);
  border-color: rgba(16, 185, 129, 0.45);
  transform: translateY(-0.5px);
}
"""

style_tag = "</style>"
if style_tag not in html:
    print("ERROR: </style> not found")
    sys.exit(1)
html = html.replace(style_tag, sync_css + "\n" + style_tag, 1)
print("1. Added sync CSS.")

# 2. Add DSA_RB_SYNC_MAP and Sync Manager functions
sync_js_template = """
/* ==========================================================================
   DSA PATTERNS <-> RISINGBRAIN BIDIRECTIONAL SYNC ENGINE (OFFLINE)
   Total Verified Identical Pairs: __TOTAL_PAIRS__
   Striver A2Z: Completely Independent & Untouched
   ========================================================================== */
const DSA_RB_SYNC_MAP = __SYNC_MAP_JSON__;

let isDsaRbSyncing = false;

function isViewActive(viewName) {
  const el = document.getElementById('view-' + viewName);
  return el ? el.classList.contains('active') : false;
}

function syncDsaToRisingBrain(dsaNum, checked) {
  if (isDsaRbSyncing) return;
  const match = DSA_RB_SYNC_MAP.dsa_to_rb[dsaNum];
  if (!match) return; // Independent question

  const rbNum = match.rb_num;
  const rbPs = getRisingBrainProblemState(rbNum);
  if (rbPs.done === checked) return; // Already in sync

  isDsaRbSyncing = true;
  try {
    const today = getTodayKey();
    rbPs.done = checked;
    if (checked) {
      if (!rbPs.firstSolvedDate) rbPs.firstSolvedDate = today;
      rbPs.completedOn = today;
      if (!rbPs.status || rbPs.status === 'NOT_STARTED') {
        rbPs.status = 'SOLVED_INDEPENDENT';
      }
    } else {
      rbPs.status = 'NOT_STARTED';
    }

    saveRisingBrainState();
    updateRisingBrainStats();

    // Immediate DOM update if present
    const rbRow = document.getElementById('rb-prob-' + rbNum);
    if (rbRow) {
      rbRow.classList.toggle('is-done', checked);
      const chk = rbRow.querySelector('input[type="checkbox"]');
      if (chk) chk.checked = checked;
    }

    if (isViewActive('risingbrain')) {
      renderRisingBrainContent();
    }
    updateHeaderStats();
    console.log('[DSA-RB SYNC] DSA #' + dsaNum + ' (' + (checked ? 'SOLVED' : 'UNSOLVED') + ') -> RisingBrain #' + rbNum);
  } catch (err) {
    console.error('[DSA-RB SYNC] Error syncing DSA to RisingBrain:', err);
  } finally {
    isDsaRbSyncing = false;
  }
}

function syncRisingBrainToDsa(rbNum, checked) {
  if (isDsaRbSyncing) return;
  const match = DSA_RB_SYNC_MAP.rb_to_dsa[rbNum];
  if (!match) return; // Independent question

  const dsaNum = match.dsa_num;
  const dsaPs = getProblemState(dsaNum);
  if (dsaPs.done === checked) return; // Already in sync

  isDsaRbSyncing = true;
  try {
    const today = getTodayKey();
    dsaPs.done = checked;
    if (checked) {
      if (!dsaPs.firstSolvedDate) dsaPs.firstSolvedDate = today;
      dsaPs.completedOn = today;
    }

    saveState();
    updateDsaStats();

    // Immediate DOM update if present
    const dsaRow = document.getElementById('prob-' + dsaNum);
    if (dsaRow) {
      dsaRow.classList.toggle('is-done', checked);
      const chk = dsaRow.querySelector('input[type="checkbox"]');
      if (chk) chk.checked = checked;
    }

    if (isViewActive('dsa')) {
      renderDsaContent();
    }
    updateHeaderStats();
    console.log('[DSA-RB SYNC] RisingBrain #' + rbNum + ' (' + (checked ? 'SOLVED' : 'UNSOLVED') + ') -> DSA #' + dsaNum);
  } catch (err) {
    console.error('[DSA-RB SYNC] Error syncing RisingBrain to DSA:', err);
  } finally {
    isDsaRbSyncing = false;
  }
}

function reconcileDsaRbOnStartup() {
  let reconciledCount = 0;
  let dsaUpdated = false;
  let rbUpdated = false;
  const today = getTodayKey();

  for (const [dsaNumStr, match] of Object.entries(DSA_RB_SYNC_MAP.dsa_to_rb)) {
    const dsaNum = Number(dsaNumStr);
    const rbNum = match.rb_num;
    const dsaPs = getProblemState(dsaNum);
    const rbPs = getRisingBrainProblemState(rbNum);

    if (dsaPs.done && !rbPs.done) {
      rbPs.done = true;
      if (!rbPs.firstSolvedDate) rbPs.firstSolvedDate = dsaPs.firstSolvedDate || today;
      if (!rbPs.completedOn) rbPs.completedOn = dsaPs.completedOn || today;
      if (!rbPs.status || rbPs.status === 'NOT_STARTED') {
        rbPs.status = 'SOLVED_INDEPENDENT';
      }
      rbUpdated = true;
      reconciledCount++;
    } else if (rbPs.done && !dsaPs.done) {
      dsaPs.done = true;
      if (!dsaPs.firstSolvedDate) dsaPs.firstSolvedDate = rbPs.firstSolvedDate || today;
      if (!dsaPs.completedOn) dsaPs.completedOn = rbPs.completedOn || today;
      dsaUpdated = true;
      reconciledCount++;
    }
  }

  if (dsaUpdated) {
    saveState();
    updateDsaStats();
  }
  if (rbUpdated) {
    saveRisingBrainState();
    updateRisingBrainStats();
  }
  if (reconciledCount > 0) {
    console.log('[DSA-RB SYNC] Reconciled ' + reconciledCount + ' questions between DSA Patterns and RisingBrain on startup.');
  }
}

// Cross-Tab LocalStorage Listener for DSA <-> RisingBrain
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
  }
});
"""

sync_js = sync_js_template.replace("__TOTAL_PAIRS__", str(sync_map["total_pairs"])).replace("__SYNC_MAP_JSON__", json.dumps(sync_map))

rb_anchor = "/* ==========================================================================\n   RISINGBRAIN PATTERN-WISE STATE & NAMESPACED PERSISTENCE"
if rb_anchor not in html:
    print("ERROR: rb_anchor not found")
    sys.exit(1)
html = html.replace(rb_anchor, sync_js + "\n\n" + rb_anchor, 1)
print("2. Added sync engine JavaScript.")

# 3. Modify toggleProblemDone
old_toggle_dsa = """function toggleProblemDone(n, checked) {
  const ps = getProblemState(n);
  ps.done = checked;
  const today = getTodayKey();
  if (checked) {
    if (!ps.firstSolvedDate) ps.firstSolvedDate = today;
    ps.completedOn = today;
  }
  saveState();
  updateDsaStats();
  renderDsaContent();
  updateHeaderStats();
}"""

new_toggle_dsa = """function toggleProblemDone(n, checked) {
  const ps = getProblemState(n);
  ps.done = checked;
  const today = getTodayKey();
  if (checked) {
    if (!ps.firstSolvedDate) ps.firstSolvedDate = today;
    ps.completedOn = today;
  }
  saveState();
  updateDsaStats();
  renderDsaContent();
  updateHeaderStats();

  // Synchronize with RisingBrain if mapped
  syncDsaToRisingBrain(n, checked);
}"""

if old_toggle_dsa not in html:
    print("ERROR: old_toggle_dsa not found")
    sys.exit(1)
html = html.replace(old_toggle_dsa, new_toggle_dsa, 1)
print("3. Modified toggleProblemDone.")

# 4. Modify setRisingBrainStatus
old_set_rb = """function setRisingBrainStatus(n, newStatus) {
  const ps = getRisingBrainProblemState(n);
  ps.status = newStatus;
  const isDone = (newStatus === 'SOLVED_INDEPENDENT' || newStatus === 'SOLVED_HINT' || newStatus === 'MASTERED');
  ps.done = isDone;
  const today = getTodayKey();
  if (isDone) {
    if (!ps.firstSolvedDate) ps.firstSolvedDate = today;
    ps.completedOn = today;
  }
  saveRisingBrainState();
  updateRisingBrainStats();
  renderRisingBrainContent();
  updateHeaderStats();
}"""

new_set_rb = """function setRisingBrainStatus(n, newStatus) {
  const ps = getRisingBrainProblemState(n);
  ps.status = newStatus;
  const isDone = (newStatus === 'SOLVED_INDEPENDENT' || newStatus === 'SOLVED_HINT' || newStatus === 'MASTERED');
  ps.done = isDone;
  const today = getTodayKey();
  if (isDone) {
    if (!ps.firstSolvedDate) ps.firstSolvedDate = today;
    ps.completedOn = today;
  }
  saveRisingBrainState();
  updateRisingBrainStats();
  renderRisingBrainContent();
  updateHeaderStats();

  // Synchronize with DSA Patterns if mapped
  syncRisingBrainToDsa(n, isDone);
}"""

if old_set_rb not in html:
    print("ERROR: old_set_rb not found")
    sys.exit(1)
html = html.replace(old_set_rb, new_set_rb, 1)
print("4. Modified setRisingBrainStatus.")

# 5. Modify revision completion hook
old_rev_block = """  if (trackerType === 'risingbrain') {
    risingBrainState.problems[probNum] = ps;
    saveRisingBrainState();
    renderRisingBrainContent();
    updateRisingBrainStats();
  } else if (isStriver) {
    striverState.problems[probNum] = ps;
    saveStriverState();
    renderStriverContent();
  } else {
    state.problems[probNum] = ps;
    saveState();
    refreshAllUI();
  }"""

new_rev_block = """  if (trackerType === 'risingbrain') {
    risingBrainState.problems[probNum] = ps;
    saveRisingBrainState();
    renderRisingBrainContent();
    updateRisingBrainStats();
    if (ps.done) syncRisingBrainToDsa(probNum, true);
  } else if (isStriver) {
    striverState.problems[probNum] = ps;
    saveStriverState();
    renderStriverContent();
  } else {
    state.problems[probNum] = ps;
    saveState();
    refreshAllUI();
    if (ps.done) syncDsaToRisingBrain(probNum, true);
  }"""

if old_rev_block not in html:
    print("ERROR: old_rev_block not found")
    sys.exit(1)
html = html.replace(old_rev_block, new_rev_block, 1)
print("5. Modified revision completion hook.")

# 6. Add UI sync indicator in renderDsaContent
old_dsa_title_line = """<span class="rb-ref-pill">P${step.id}</span>
                        <span class="rb-prob-name" title="${p.t}">${p.t}</span>
                        <span class="rb-diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>"""

new_dsa_title_line = """<span class="rb-ref-pill">P${step.id}</span>
                        <span class="rb-prob-name" title="${p.t}">${p.t}</span>
                        ${(typeof DSA_RB_SYNC_MAP !== 'undefined' && DSA_RB_SYNC_MAP.dsa_to_rb[p.n]) ? `<span class="rb-sync-indicator" title="Auto-synced with RisingBrain #${DSA_RB_SYNC_MAP.dsa_to_rb[p.n].rb_num}: ${DSA_RB_SYNC_MAP.dsa_to_rb[p.n].rb_title.replace(/"/g, '&quot;')}">🔄 Synced</span>` : ''}
                        <span class="rb-diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>"""

if old_dsa_title_line not in html:
    print("ERROR: old_dsa_title_line not found")
    sys.exit(1)
html = html.replace(old_dsa_title_line, new_dsa_title_line, 1)
print("6. Added sync indicator in renderDsaContent.")

# 7. Add UI sync indicator in renderRisingBrainContent
old_rb_title_line = """<span class="rb-prob-name" title="${p.t}">${p.t}</span>
                          <span class="rb-diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>"""

new_rb_title_line = """<span class="rb-prob-name" title="${p.t}">${p.t}</span>
                          ${(typeof DSA_RB_SYNC_MAP !== 'undefined' && DSA_RB_SYNC_MAP.rb_to_dsa[p.n]) ? `<span class="rb-sync-indicator" title="Auto-synced with DSA Patterns #${DSA_RB_SYNC_MAP.rb_to_dsa[p.n].dsa_num}: ${DSA_RB_SYNC_MAP.rb_to_dsa[p.n].dsa_title.replace(/"/g, '&quot;')}">🔄 Synced</span>` : ''}
                          <span class="rb-diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>"""

if old_rb_title_line not in html:
    print("ERROR: old_rb_title_line not found")
    sys.exit(1)
html = html.replace(old_rb_title_line, new_rb_title_line, 1)
print("7. Added sync indicator in renderRisingBrainContent.")

# 8. Add reconcileDsaRbOnStartup() to init()
old_init_block = """  loadState();
  loadStriverState();
  loadRisingBrainState();
  loadOtherStates();"""

new_init_block = """  loadState();
  loadStriverState();
  loadRisingBrainState();
  loadOtherStates();
  reconcileDsaRbOnStartup();"""

if old_init_block not in html:
    print("ERROR: old_init_block not found")
    sys.exit(1)
html = html.replace(old_init_block, new_init_block, 1)
print("8. Added startup reconciliation to init().")

# Save to test_sync_assembled.html
with open("test_sync_assembled.html", "w") as f:
    f.write(html)

print("SUCCESS: Assembled test_sync_assembled.html cleanly!")
