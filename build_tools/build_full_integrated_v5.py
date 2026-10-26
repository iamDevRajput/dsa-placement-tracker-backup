import os, sys, re, json

source_file = "/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html"
with open(source_file, "r", encoding="utf-8") as f:
    html = f.read()

with open("/Users/devrajput/.gemini/antigravity-ide/scratch/risingbrain_data.js", "r", encoding="utf-8") as f:
    rb_data_js = f.read()

# 1. Update APP_BUILD_VERSION
html = html.replace("const APP_BUILD_VERSION = '2026.10.25-offline-v4';", "const APP_BUILD_VERSION = '2026.10.26-offline-v5';")

# 2. Inject RISINGBRAIN_DATA
striver_header = "/* ==========================================================================\n   STRIVER A2Z 455 QUESTIONS DATASET"
if striver_header in html:
    rb_block = "\n/* ==========================================================================\n   RISINGBRAIN PATTERN WISE 385 QUESTIONS DATASET\n   ========================================================================== */\n" + rb_data_js + "\n\n"
    html = html.replace(striver_header, rb_block + striver_header)
    print("Injected RISINGBRAIN_DATA")
else:
    print("Error: Striver header not found")
    sys.exit(1)

# 3. Add CSS styles
rb_css = """
/* ==========================================================================
   RISINGBRAIN PATTERN-WISE STYLES & CLUES
   ========================================================================== */
.rb-topic-section {
  background: var(--surface2);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  margin-bottom: 1.5rem;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: all var(--transition-fast);
}
.rb-topic-section:hover {
  border-color: rgba(16, 185, 129, 0.3);
}
.rb-topic-header {
  padding: 1rem 1.25rem;
  background: var(--surface3);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.rb-topic-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.rb-topic-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 13px;
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.rb-topic-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-main);
}
.rb-topic-desc {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}
.rb-pattern-card {
  margin: 0.85rem 1rem;
  background: var(--surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: border-color var(--transition-fast);
}
.rb-pattern-card:hover {
  border-color: rgba(16, 185, 129, 0.35);
}
.rb-pattern-header {
  padding: 0.85rem 1.1rem;
  background: rgba(255, 255, 255, 0.02);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
  transition: background var(--transition-fast);
}
.rb-pattern-header:hover {
  background: rgba(16, 185, 129, 0.05);
}
.rb-pattern-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.rb-pattern-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text-main);
}
.rb-pattern-info-box {
  padding: 0.85rem 1.1rem;
  background: rgba(0, 0, 0, 0.12);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.rb-strategy-box {
  font-size: 12.5px;
  line-height: 1.45;
  color: var(--text-muted);
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}
.rb-strategy-badge {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 2px 6px;
  border-radius: 4px;
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.3);
  white-space: nowrap;
}
.rb-clues-box {
  font-size: 12.5px;
  line-height: 1.45;
  color: var(--text-muted);
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}
.rb-clues-badge {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  padding: 2px 6px;
  border-radius: 4px;
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
  white-space: nowrap;
}
.rb-status-select {
  font-size: 11.5px;
  font-weight: 600;
  padding: 3px 6px;
  border-radius: 6px;
  background: var(--surface3);
  color: var(--text-main);
  border: 1px solid var(--border-subtle);
  outline: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.rb-status-select:focus {
  border-color: #10b981;
}
.rb-status-select.status-NOT_STARTED { color: var(--text-dim); }
.rb-status-select.status-ATTEMPTED { color: #f59e0b; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.08); }
.rb-status-select.status-SOLVED_INDEPENDENT { color: #10b981; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.1); }
.rb-status-select.status-SOLVED_HINT { color: #f97316; border-color: rgba(249, 115, 22, 0.4); background: rgba(249, 115, 22, 0.1); }
.rb-status-select.status-NEEDS_REVISION { color: #a855f7; border-color: rgba(168, 85, 247, 0.4); background: rgba(168, 85, 247, 0.1); }
.rb-status-select.status-MASTERED { color: #eab308; border-color: rgba(234, 179, 8, 0.5); background: rgba(234, 179, 8, 0.12); }

.cross-ref-badge {
  font-size: 10px;
  font-family: var(--font-mono);
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 4px;
  background: rgba(99, 102, 241, 0.12);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.3);
  display: inline-flex;
  align-items: center;
  gap: 3px;
  cursor: pointer;
  text-decoration: none;
  transition: all var(--transition-fast);
}
.cross-ref-badge:hover {
  background: rgba(99, 102, 241, 0.25);
  border-color: #818cf8;
  transform: translateY(-1px);
}
.cross-ref-badge.dsa-ref {
  background: rgba(168, 85, 247, 0.12);
  color: #c084fc;
  border-color: rgba(168, 85, 247, 0.3);
}
.cross-ref-badge.dsa-ref:hover {
  background: rgba(168, 85, 247, 0.25);
  border-color: #c084fc;
}
.rb-ref-badge {
  font-size: 10px;
  font-family: var(--font-mono);
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
  display: inline-block;
}
"""

idx_style_end = html.find("</style>")
if idx_style_end != -1:
    html = html[:idx_style_end] + rb_css + "\n" + html[idx_style_end:]
    print("Injected CSS")

# 4. Add Sidebar Navigation item for RisingBrain
nav_striver = """    <button class="nav-item" onclick="switchView('striver', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
      <span>Striver Sheet</span>
      <span class="nav-badge accent" id="nav-striver-badge">0/455</span>
    </button>"""

nav_rb = """    <button class="nav-item" onclick="switchView('striver', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
      <span>Striver Sheet</span>
      <span class="nav-badge accent" id="nav-striver-badge">0/455</span>
    </button>
    <button class="nav-item" onclick="switchView('risingbrain', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 18V5"/><path d="M15 13a4.17 4.17 0 0 1-3-4 4.17 4.17 0 0 1-3 4"/><path d="M17.598 6.5A3 3 0 1 0 12 5a3 3 0 1 0-5.598 1.5"/><path d="M17.997 5.125a4 4 0 0 1 2.526 5.77"/><path d="M18 18a4 4 0 0 0 2-7.464"/><path d="M19.967 17.483A4 4 0 1 1 12 18a4 4 0 1 1-7.967-.517"/><path d="M6 18a4 4 0 0 1-2-7.464"/><path d="M6.003 5.125a4 4 0 0 0-2.526 5.77"/></svg>
      <span>RisingBrain Sheet</span>
      <span class="nav-badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3);" id="nav-risingbrain-badge">0/385</span>
    </button>"""

if nav_striver in html:
    html = html.replace(nav_striver, nav_rb)
    print("Injected Sidebar Nav Item")

# 5. Add Dashboard overview 3-tracker overview row
dash_metric_end = """      <div class="grid-4" style="margin-bottom: 1.5rem;">
        <div class="metric-card">
          <div class="metric-label"><span>Unique Solved</span><span>✓</span></div>
          <div class="metric-val" id="m-solved">0</div>
          <div class="metric-sub" id="m-solved-pct">0% of 184 completed</div>
        </div>
        <div class="metric-card">
          <div class="metric-label"><span>Total Revisions</span><span>🔁</span></div>
          <div class="metric-val" id="m-revs">0</div>
          <div class="metric-sub" id="m-revs-avg">0.0 revs / solved question</div>
        </div>
        <div class="metric-card">
          <div class="metric-label"><span>Due for Revision</span><span>⏰</span></div>
          <div class="metric-val" id="m-due" style="color:var(--accent4);">0</div>
          <div class="metric-sub" id="m-overdue-sub">0 overdue</div>
        </div>
        <div class="metric-card">
          <div class="metric-label"><span>Day Streak</span><span>🔥</span></div>
          <div class="metric-val" id="m-streak" style="color:var(--streak);">0</div>
          <div class="metric-sub" id="m-maxstreak">Best streak: 0 days</div>
        </div>
      </div>"""

dash_3trackers_row = """      <!-- TRIPLE INDEPENDENT TRACKERS OVERVIEW -->
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
        <div class="card" style="padding:1.1rem; border-top:3px solid var(--accent3);">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:var(--accent3); letter-spacing:0.05em;">Curated Patterns</div>
              <div style="font-size:1.1rem; font-weight:700; color:var(--text-main); margin-top:2px;">184 DSA Patterns</div>
            </div>
            <span class="badge" style="background:var(--accent3-bg); color:var(--accent3);">19 Patterns</span>
          </div>
          <div style="font-size:1.5rem; font-weight:800; font-family:var(--font-mono); margin:0.75rem 0 0.25rem 0;" id="db-dsa-count-large">0 <span style="font-size:13px; color:var(--text-muted); font-weight:500;">/ 184</span></div>
          <div class="step-mini-bar" style="height:6px; margin-bottom:0.6rem;"><div class="step-mini-fill" id="db-dsa-bar-large" style="width:0%; background:var(--accent3);"></div></div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:11.5px; color:var(--text-dim);" id="db-dsa-pct-large">0% Solved</span>
            <button class="btn btn-sm btn-ghost" onclick="switchView('dsa')" style="color:var(--accent3); padding:2px 8px; font-size:11.5px;">Open DSA Patterns →</button>
          </div>
        </div>

        <div class="card" style="padding:1.1rem; border-top:3px solid var(--accent4);">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:var(--accent4); letter-spacing:0.05em;">Comprehensive Sheet</div>
              <div style="font-size:1.1rem; font-weight:700; color:var(--text-main); margin-top:2px;">Striver A2Z Sheet</div>
            </div>
            <span class="badge" style="background:var(--accent4-bg); color:var(--accent4);">18 Steps</span>
          </div>
          <div style="font-size:1.5rem; font-weight:800; font-family:var(--font-mono); margin:0.75rem 0 0.25rem 0;" id="db-striver-count-large">0 <span style="font-size:13px; color:var(--text-muted); font-weight:500;">/ 455</span></div>
          <div class="step-mini-bar" style="height:6px; margin-bottom:0.6rem;"><div class="step-mini-fill" id="db-striver-bar-large" style="width:0%; background:var(--accent4);"></div></div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:11.5px; color:var(--text-dim);" id="db-striver-pct-large">0% Solved</span>
            <button class="btn btn-sm btn-ghost" onclick="switchView('striver')" style="color:var(--accent4); padding:2px 8px; font-size:11.5px;">Open Striver Sheet →</button>
          </div>
        </div>

        <div class="card" style="padding:1.1rem; border-top:3px solid #10b981;">
          <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
              <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:#10b981; letter-spacing:0.05em;">Topic & Clues Sheet</div>
              <div style="font-size:1.1rem; font-weight:700; color:var(--text-main); margin-top:2px;">RisingBrain Pattern Wise</div>
            </div>
            <span class="badge" style="background:rgba(16,185,129,0.15); color:#10b981;">17 Topics</span>
          </div>
          <div style="font-size:1.5rem; font-weight:800; font-family:var(--font-mono); margin:0.75rem 0 0.25rem 0;" id="db-rb-count-large">0 <span style="font-size:13px; color:var(--text-muted); font-weight:500;">/ 385</span></div>
          <div class="step-mini-bar" style="height:6px; margin-bottom:0.6rem;"><div class="step-mini-fill" id="db-rb-bar-large" style="width:0%; background:#10b981;"></div></div>
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:11.5px; color:var(--text-dim);" id="db-rb-pct-large">0% Solved</span>
            <button class="btn btn-sm btn-ghost" onclick="switchView('risingbrain')" style="color:#10b981; padding:2px 8px; font-size:11.5px;">Open RisingBrain →</button>
          </div>
        </div>
      </div>"""

if dash_metric_end in html:
    html = html.replace(dash_metric_end, dash_metric_end + "\n" + dash_3trackers_row)
    print("Injected Dashboard 3-Tracker Row")

# 6. Add view-risingbrain section after view-striver
view_striver_anchor = """    <!-- VIEW 3: REVISION CENTER -->"""
view_risingbrain_markup = """    <!-- VIEW 2.7: RISINGBRAIN PATTERN-WISE SHEET -->
    <section class="view-section" id="view-risingbrain">
      <div class="dsa-controls">
        <div class="search-and-actions">
          <div class="search-box">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="text" id="rbSearch" placeholder="Search 385 RisingBrain problems by title, reference (e.g. LC 167), pattern, company..." oninput="renderRisingBrainContent()">
          </div>
          <select class="form-select pattern-dropdown-select" id="rbTopicSelectDropdown" onchange="jumpToRbTopic(this.value)">
            <!-- Populated dynamically with all 17 topics -->
          </select>
          <select class="form-select" id="rbCompanyFilter" onchange="setRbCompany(this.value)" style="min-width:160px; font-weight:600;">
            <option value="all">🏢 All Companies</option>
            <option value="Amazon">🛒 Amazon</option>
            <option value="Google">🔍 Google</option>
            <option value="Microsoft">🪟 Microsoft</option>
            <option value="Meta">👤 Meta</option>
            <option value="Apple">🍎 Apple</option>
            <option value="Bloomberg">📈 Bloomberg</option>
            <option value="Uber">🚗 Uber</option>
            <option value="Goldman Sachs">🏦 Goldman Sachs</option>
            <option value="Adobe">🎨 Adobe</option>
            <option value="Salesforce">☁️ Salesforce</option>
            <option value="Flipkart">🛍️ Flipkart</option>
          </select>
          <button class="btn btn-secondary" onclick="expandAllRbPatterns(true)">Expand All</button>
          <button class="btn btn-secondary" onclick="expandAllRbPatterns(false)">Collapse All</button>
        </div>

        <div class="filter-pills">
          <button class="fpill active" id="f-rb-all" onclick="setRbFilter('all', this)">All (385)</button>
          <button class="fpill" id="f-rb-easy" onclick="setRbFilter('e', this)">Easy (81)</button>
          <button class="fpill" id="f-rb-medium" onclick="setRbFilter('m', this)">Medium (251)</button>
          <button class="fpill" id="f-rb-hard" onclick="setRbFilter('h', this)">Hard (53)</button>
          <span style="border-left:1px solid var(--border-subtle); margin:0 4px; height:18px;"></span>
          <button class="fpill" id="f-rb-pending" onclick="setRbStatusFilter('pending', this)">Pending</button>
          <button class="fpill" id="f-rb-done" onclick="setRbStatusFilter('done', this)">Done</button>
          <button class="fpill" id="f-rb-attempted" onclick="setRbStatusFilter('attempted', this)">🟡 Attempted</button>
          <button class="fpill" id="f-rb-needsrev" onclick="setRbStatusFilter('needsrev', this)">🟣 Needs Rev</button>
          <button class="fpill" id="f-rb-mastered" onclick="setRbStatusFilter('mastered', this)">👑 Mastered</button>
          <button class="fpill" id="f-rb-starred" onclick="setRbStatusFilter('starred', this)">⭐ Starred</button>
        </div>
      </div>

      <div class="dsa-layout">
        <!-- Sidebar Jump To Topic -->
        <aside class="pattern-nav-sidebar" id="rbTopicNavSidebar">
          <!-- Populated dynamically: 17 Topics -->
        </aside>

        <!-- Main Topic Sections & Pattern Cards -->
        <div class="pattern-content-area" id="risingBrainContent">
          <!-- 17 Topics, 68 Patterns & 385 Problems -->
        </div>
      </div>
    </section>

"""

if view_striver_anchor in html:
    html = html.replace(view_striver_anchor, view_risingbrain_markup + view_striver_anchor)
    print("Injected view-risingbrain Section")

# 7. Add RisingBrain Storage Key, Global State, and Logic
rb_js_logic = """
/* ==========================================================================
   RISINGBRAIN PATTERN-WISE STATE & NAMESPACED PERSISTENCE
   ========================================================================== */
const STORAGE_RISINGBRAIN_KEY = 'risingbrain_tracker_v1';

let risingBrainState = {
  version: 1,
  problems: {},
  maxStreak: 0,
  collapsedPatterns: {},
  collapsedTopics: {}
};

let currentRbFilter = 'all';        // 'all' | 'e' | 'm' | 'h'
let currentRbStatusFilter = 'all';  // 'all' | 'pending' | 'done' | 'attempted' | 'needsrev' | 'mastered' | 'starred'
let currentActiveRbTopic = 'all';
let currentRbCompany = 'all';

function emptyRisingBrainProblemState() {
  return {
    status: 'NOT_STARTED',
    done: false,
    starred: false,
    firstSolvedDate: null,
    completedOn: null,
    revisions: [],
    revisionCount: 0,
    lastRevisedDate: null,
    nextDueDate: null,
    spacedIntervalLevel: 0,
    notes: { approach: '', mistakes: '', complexity: '' }
  };
}

function getRisingBrainProblemState(n) {
  if (!risingBrainState.problems[n]) {
    risingBrainState.problems[n] = emptyRisingBrainProblemState();
  }
  return risingBrainState.problems[n];
}

function totalRisingBrainProbs() {
  let cnt = 0;
  RISINGBRAIN_DATA.forEach(t => {
    t.patterns.forEach(p => {
      cnt += p.problems.length;
    });
  });
  return cnt;
}

function doneRisingBrainProbsForTopic(topic) {
  let doneCnt = 0;
  topic.patterns.forEach(pat => {
    pat.problems.forEach(p => {
      if (getRisingBrainProblemState(p.n).done) doneCnt++;
    });
  });
  return doneCnt;
}

function doneRisingBrainProbsForPattern(pattern) {
  return pattern.problems.filter(p => getRisingBrainProblemState(p.n).done).length;
}

function saveRisingBrainState() {
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

    localStorage.setItem(STORAGE_RISINGBRAIN_KEY, JSON.stringify(risingBrainState));
    mirrorToIndexedDB();
    recordSnapshot('saveRisingBrainState');
  } catch(e) {
    console.error('Storage error in saveRisingBrainState:', e);
    showStorageAlert('Could not save RisingBrain state. Check local storage quota.');
  }
}

function loadRisingBrainState() {
  try {
    const raw = localStorage.getItem(STORAGE_RISINGBRAIN_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && parsed.problems) {
        risingBrainState = {
          version: 1,
          problems: parsed.problems || {},
          maxStreak: parsed.maxStreak || 0,
          collapsedPatterns: parsed.collapsedPatterns || {},
          collapsedTopics: parsed.collapsedTopics || {}
        };
        RISINGBRAIN_DATA.forEach(topic => {
          topic.patterns.forEach(pat => {
            pat.problems.forEach(p => {
              if (!risingBrainState.problems[p.n]) {
                risingBrainState.problems[p.n] = emptyRisingBrainProblemState();
              } else {
                const ps = risingBrainState.problems[p.n];
                if (!Array.isArray(ps.revisions)) ps.revisions = [];
                ps.revisionCount = ps.revisions.length;
                if (!ps.notes) ps.notes = { approach: '', mistakes: '', complexity: '' };
                if (!ps.status) ps.status = ps.done ? 'SOLVED_INDEPENDENT' : 'NOT_STARTED';
              }
            });
          });
        });
        return;
      }
    }

    // Default clean initialization
    risingBrainState = { version: 1, problems: {}, maxStreak: 0, collapsedPatterns: {}, collapsedTopics: {} };
    RISINGBRAIN_DATA.forEach(topic => {
      topic.patterns.forEach(pat => {
        pat.problems.forEach(p => {
          risingBrainState.problems[p.n] = emptyRisingBrainProblemState();
        });
      });
    });
  } catch (e) {
    console.error('Error in loadRisingBrainState:', e);
  }
}

function setRisingBrainStatus(n, newStatus) {
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
}

function toggleRisingBrainDone(n, checked) {
  const newStatus = checked ? 'SOLVED_INDEPENDENT' : 'NOT_STARTED';
  setRisingBrainStatus(n, newStatus);
}

function toggleRisingBrainStar(n) {
  const ps = getRisingBrainProblemState(n);
  ps.starred = !ps.starred;
  saveRisingBrainState();
  renderRisingBrainContent();
}

function toggleRbTopicCollapse(topicId) {
  risingBrainState.collapsedTopics[topicId] = !risingBrainState.collapsedTopics[topicId];
  saveRisingBrainState();
  renderRisingBrainContent();
}

function toggleRbPatternCollapse(patId) {
  risingBrainState.collapsedPatterns[patId] = !risingBrainState.collapsedPatterns[patId];
  saveRisingBrainState();
  renderRisingBrainContent();
}

function expandAllRbPatterns(expand) {
  RISINGBRAIN_DATA.forEach(t => {
    risingBrainState.collapsedTopics[t.id] = !expand;
    t.patterns.forEach(p => {
      risingBrainState.collapsedPatterns[p.id] = !expand;
    });
  });
  saveRisingBrainState();
  renderRisingBrainContent();
}

function jumpToRbTopic(topicId) {
  currentActiveRbTopic = topicId;
  const dd = document.getElementById('rbTopicSelectDropdown');
  if (dd) dd.value = topicId;
  renderRisingBrainContent();
  if (topicId !== 'all') {
    const el = document.getElementById('rb-topic-' + topicId);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function setRbFilter(diff, btn) {
  currentRbFilter = diff;
  document.querySelectorAll('#view-risingbrain .filter-pills .fpill').forEach(b => {
    if (['f-rb-all', 'f-rb-easy', 'f-rb-medium', 'f-rb-hard'].includes(b.id)) b.classList.remove('active');
  });
  if (btn) btn.classList.add('active');
  renderRisingBrainContent();
}

function setRbStatusFilter(st, btn) {
  currentRbStatusFilter = st;
  document.querySelectorAll('#view-risingbrain .filter-pills .fpill').forEach(b => {
    if (['f-rb-pending', 'f-rb-done', 'f-rb-attempted', 'f-rb-needsrev', 'f-rb-mastered', 'f-rb-starred'].includes(b.id)) b.classList.remove('active');
  });
  if (btn) btn.classList.add('active');
  renderRisingBrainContent();
}

function setRbCompany(co) {
  currentRbCompany = co;
  renderRisingBrainContent();
}

function jumpToCrossSheet(sheet, pNum) {
  if (sheet === 'striver') {
    switchView('striver');
    setTimeout(() => {
      const el = document.getElementById('striver-prob-' + pNum);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.outline = '2px solid var(--accent)';
        setTimeout(() => el.style.outline = '', 2000);
      }
    }, 200);
  } else if (sheet === 'dsa') {
    switchView('dsa');
    setTimeout(() => {
      const el = document.getElementById('prob-' + pNum);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.outline = '2px solid var(--accent3)';
        setTimeout(() => el.style.outline = '', 2000);
      }
    }, 200);
  }
}

function renderRisingBrainContent() {
  const q = (document.getElementById('rbSearch')?.value || '').toLowerCase().trim();
  const content = document.getElementById('risingBrainContent');
  if (!content) return;

  let html = '';
  let totalVisible = 0;

  RISINGBRAIN_DATA.forEach(topic => {
    if (currentActiveRbTopic !== 'all' && currentActiveRbTopic !== topic.id) return;

    let topicHasVisible = false;
    let topicPatternsHtml = '';

    const doneTopicCount = doneRisingBrainProbsForTopic(topic);
    const totalTopicCount = topic.patterns.reduce((acc, p) => acc + p.problems.length, 0);
    const topicPct = totalTopicCount > 0 ? Math.round((doneTopicCount / totalTopicCount) * 100) : 0;
    const isTopicCollapsed = !!risingBrainState.collapsedTopics[topic.id];

    topic.patterns.forEach((pat, patIdx) => {
      const visibleProblems = pat.problems.filter(p => {
        const ps = getRisingBrainProblemState(p.n);

        // Search matching
        let matchesSearch = true;
        if (q) {
          const tMatch = p.t.toLowerCase().includes(q);
          const refMatch = (p.ref || '').toLowerCase().includes(q);
          const numMatch = ('#' + p.n).includes(q) || String(p.n) === q;
          const patMatch = pat.name.toLowerCase().includes(q);
          const topMatch = topic.name.toLowerCase().includes(q);
          const coMatch = Array.isArray(p.c) && p.c.some(c => c.toLowerCase().includes(q));
          matchesSearch = (tMatch || refMatch || numMatch || patMatch || topMatch || coMatch);
        }

        // Difficulty matching
        let matchesDiff = true;
        if (currentRbFilter !== 'all') {
          matchesDiff = (p.diff === currentRbFilter);
        }

        // Status matching
        let matchesStatus = true;
        if (currentRbStatusFilter === 'pending') matchesStatus = !ps.done;
        else if (currentRbStatusFilter === 'done') matchesStatus = !!ps.done;
        else if (currentRbStatusFilter === 'attempted') matchesStatus = (ps.status === 'ATTEMPTED');
        else if (currentRbStatusFilter === 'needsrev') matchesStatus = (ps.status === 'NEEDS_REVISION');
        else if (currentRbStatusFilter === 'mastered') matchesStatus = (ps.status === 'MASTERED');
        else if (currentRbStatusFilter === 'starred') matchesStatus = !!ps.starred;

        // Company matching
        let matchesCo = true;
        if (currentRbCompany !== 'all') {
          matchesCo = Array.isArray(p.c) && p.c.some(c => c.toLowerCase().includes(currentRbCompany.toLowerCase()));
        }

        return matchesSearch && matchesDiff && matchesStatus && matchesCo;
      });

      if (visibleProblems.length === 0) return;
      topicHasVisible = true;
      totalVisible += visibleProblems.length;

      const donePatCount = doneRisingBrainProbsForPattern(pat);
      const patPct = Math.round((donePatCount / pat.problems.length) * 100);
      const isPatCollapsed = !!risingBrainState.collapsedPatterns[pat.id];

      topicPatternsHtml += `
        <div class="rb-pattern-card" id="rb-pat-${pat.id}">
          <div class="rb-pattern-header" onclick="toggleRbPatternCollapse('${pat.id}')">
            <div class="rb-pattern-title-wrap">
              <span class="badge" style="background:rgba(16,185,129,0.15); color:#10b981; font-weight:800; font-size:11px;">P${patIdx + 1}</span>
              <span class="rb-pattern-title">${pat.name}</span>
            </div>
            <div style="display:flex; align-items:center; gap:0.75rem;">
              <span style="font-size:12px; font-family:var(--font-mono); color:var(--text-muted);">${donePatCount}/${pat.problems.length} (${patPct}%)</span>
              <div class="step-mini-bar" style="width:70px;"><div class="step-mini-fill" style="width:${patPct}%; background:#10b981;"></div></div>
              <svg style="transform:${isPatCollapsed ? 'rotate(-90deg)' : 'rotate(0deg)'}; transition:transform 0.2s;" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
            </div>
          </div>

          ${!isPatCollapsed ? `
            <div class="rb-pattern-info-box">
              ${pat.strategy ? `
                <div class="rb-strategy-box">
                  <span class="rb-strategy-badge">💡 Strategy</span>
                  <span>${pat.strategy}</span>
                </div>
              ` : ''}
              ${pat.identification ? `
                <div class="rb-clues-box">
                  <span class="rb-clues-badge">🔍 Recognition Clues</span>
                  <span>${pat.identification}</span>
                </div>
              ` : ''}
            </div>

            <div class="problems-list">
              ${visibleProblems.map(p => {
                const ps = getRisingBrainProblemState(p.n);
                const isDone = !!ps.done;
                const isStarred = !!ps.starred;
                const diffClass = p.diff === 'e' ? 'e' : p.diff === 'm' ? 'm' : 'h';
                const diffLabel = p.diff === 'e' ? 'Easy' : p.diff === 'm' ? 'Med' : 'Hard';

                let linksHtml = '';
                if (p.l) {
                  linksHtml += `
                    <a class="platform-badge lc-badge" href="${p.l}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Open problem on LeetCode: ${p.l}">
                      <span class="platform-brand">LC</span>
                      <span>LeetCode</span>
                      <svg class="ext-icon" viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
                }
                if (p.g) {
                  linksHtml += `
                    <a class="platform-badge gfg-badge" href="${p.g}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Open problem on GeeksforGeeks: ${p.g}">
                      <span class="platform-brand">GFG</span>
                      <span>GeeksforGeeks</span>
                      <svg class="ext-icon" viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
                }
                if (p.v) {
                  linksHtml += `
                    <a class="platform-badge yt-badge" href="${p.v}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Watch video solution: ${p.v}">
                      <span class="platform-brand">▶</span>
                      <span>YT Video</span>
                      <svg class="ext-icon" viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
                }

                let coTagsHtml = '';
                if (Array.isArray(p.c) && p.c.length > 0) {
                  const topCos = p.c.slice(0, 3);
                  const moreCount = p.c.length > 3 ? ` +${p.c.length - 3}` : '';
                  coTagsHtml = `<span class="company-tag" title="Companies: ${p.c.join(', ')}">🏢 ${topCos.join(', ')}${moreCount}</span>`;
                }

                let crossRefHtml = '';
                if (p.cross) {
                  if (p.cross.striver) {
                    crossRefHtml += `<a class="cross-ref-badge" href="javascript:void(0)" onclick="jumpToCrossSheet('striver', ${p.cross.striver.num})" title="Also in Striver Sheet: #${p.cross.striver.num} (${p.cross.striver.title}) in ${p.cross.striver.step}">🔗 Striver #${p.cross.striver.num}</a>`;
                  }
                  if (p.cross.dsa) {
                    crossRefHtml += `<a class="cross-ref-badge dsa-ref" href="javascript:void(0)" onclick="jumpToCrossSheet('dsa', ${p.cross.dsa.num})" title="Also in DSA Patterns: #${p.cross.dsa.num} (${p.cross.dsa.title}) in ${p.cross.dsa.pattern}">🔗 DSA #${p.cross.dsa.num}</a>`;
                  }
                }

                let dueTag = '';
                if (isProblemOverdue(ps)) {
                  dueTag = `<span class="due-badge overdue">⚠️ Overdue</span>`;
                } else if (isProblemDue(ps)) {
                  dueTag = `<span class="due-badge today">⏰ Due Today</span>`;
                } else if (ps.nextDueDate) {
                  dueTag = `<span class="due-badge future">Due: ${formatDateDisplay(ps.nextDueDate)}</span>`;
                }

                return `
                  <div class="prob-item${isDone ? ' done' : ''}" id="rb-prob-${p.n}">
                    <div class="prob-left-col">
                      <input type="checkbox" class="prob-cb" ${isDone ? 'checked' : ''} onchange="toggleRisingBrainDone(${p.n}, this.checked)" title="Toggle Solved Status">
                      <button type="button" class="star-btn${isStarred ? ' starred' : ''}" onclick="toggleRisingBrainStar(${p.n})" title="${isStarred ? 'Unstar' : 'Star problem'}">${isStarred ? '★' : '☆'}</button>
                      <span class="prob-num">#${p.n}</span>
                    </div>

                    <div class="prob-info">
                      <div class="prob-title-row">
                        <span class="prob-pattern-tag" style="color:#10b981; background:rgba(16,185,129,0.12);" title="${topic.name} · ${pat.name}">${topic.name}: ${pat.name}</span>
                        ${p.ref ? `<span class="rb-ref-badge">${p.ref}</span>` : ''}
                        <span class="prob-title">${p.t}</span>
                        <span class="diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>
                        ${dueTag}
                      </div>

                      <div class="prob-meta-row" style="margin-top:4px;">
                        <div class="platform-badges-container">
                          ${linksHtml}
                        </div>
                        ${coTagsHtml ? `<div class="company-tags-container">${coTagsHtml}</div>` : ''}
                        ${crossRefHtml ? `<div style="display:inline-flex; gap:4px; align-items:center;">${crossRefHtml}</div>` : ''}
                      </div>
                    </div>

                    <div class="prob-actions">
                      <select class="rb-status-select status-${ps.status || 'NOT_STARTED'}" onchange="setRisingBrainStatus(${p.n}, this.value)" title="Change Practice Status">
                        <option value="NOT_STARTED" ${ps.status === 'NOT_STARTED' ? 'selected' : ''}>⚪ Not Started</option>
                        <option value="ATTEMPTED" ${ps.status === 'ATTEMPTED' ? 'selected' : ''}>🟡 Attempted</option>
                        <option value="SOLVED_INDEPENDENT" ${ps.status === 'SOLVED_INDEPENDENT' ? 'selected' : ''}>🟢 Solved Solo</option>
                        <option value="SOLVED_HINT" ${ps.status === 'SOLVED_HINT' ? 'selected' : ''}>🟠 Solved Hint</option>
                        <option value="NEEDS_REVISION" ${ps.status === 'NEEDS_REVISION' ? 'selected' : ''}>🟣 Needs Revision</option>
                        <option value="MASTERED" ${ps.status === 'MASTERED' ? 'selected' : ''}>👑 Mastered</option>
                      </select>

                      <button class="btn btn-sm btn-ghost rev-counter-btn" onclick="openRevisionModal(${p.n}, 'risingbrain')" title="Log revision or inspect notes">
                        +1 Rev${ps.revisionCount > 0 ? ` <span class="badge" style="background:#10b981; color:#000; font-weight:800; margin-left:3px;">${ps.revisionCount}</span>` : ''}
                      </button>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          ` : ''}
        </div>
      `;
    });

    if (topicHasVisible) {
      html += `
        <div class="rb-topic-section" id="rb-topic-${topic.id}">
          <div class="rb-topic-header">
            <div class="rb-topic-title-wrap">
              <span class="rb-topic-icon">${topic.name.substring(0, 2).toUpperCase()}</span>
              <div>
                <div class="rb-topic-name">${topic.name}</div>
                <div class="rb-topic-desc">${topic.desc}</div>
              </div>
            </div>
            <div style="display:flex; align-items:center; gap:1rem;">
              <span style="font-size:12.5px; font-family:var(--font-mono); color:var(--text-muted);">${doneTopicCount} / ${totalTopicCount} solved</span>
              <div class="step-mini-bar" style="width:100px;"><div class="step-mini-fill" style="width:${topicPct}%; background:#10b981;"></div></div>
              <button class="btn btn-sm btn-ghost" onclick="toggleRbTopicCollapse('${topic.id}')" style="padding:2px 8px; font-size:12px;">
                ${isTopicCollapsed ? 'Expand Topic ▼' : 'Collapse Topic ▲'}
              </button>
            </div>
          </div>
          ${!isTopicCollapsed ? topicPatternsHtml : ''}
        </div>
      `;
    }
  });

  if (totalVisible === 0) {
    html = `
      <div class="card" style="text-align:center; padding:3rem 1.5rem; color:var(--text-muted);">
        <div style="font-size:2rem; margin-bottom:0.5rem;">🔍</div>
        <div style="font-size:1.1rem; font-weight:700; color:var(--text-main);">No matching RisingBrain problems found</div>
        <div style="font-size:13px; margin-top:4px;">Try adjusting your search query, difficulty filters, or company filters.</div>
      </div>
    `;
  }

  content.innerHTML = html;
}

function updateRisingBrainStats() {
  const total = totalRisingBrainProbs();
  const done = Object.values(risingBrainState.problems).filter(p => p.done).length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  const badge = document.getElementById('nav-risingbrain-badge');
  if (badge) badge.textContent = `${done}/${total}`;

  const disp = document.getElementById('rb-solved-total-display');
  if (disp) disp.textContent = `${done} / ${total}`;

  const pctDisp = document.getElementById('rb-pct-total-display');
  if (pctDisp) pctDisp.textContent = `${pct}% Completed`;

  const bar = document.getElementById('rb-main-progress-bar');
  if (bar) bar.style.width = `${pct}%`;

  // Update dashboard cards
  const dbCount = document.getElementById('db-rb-count-large');
  if (dbCount) dbCount.innerHTML = `${done} <span style="font-size:13px; color:var(--text-muted); font-weight:500;">/ ${total}</span>`;

  const dbBar = document.getElementById('db-rb-bar-large');
  if (dbBar) dbBar.style.width = `${pct}%`;

  const dbPct = document.getElementById('db-rb-pct-large');
  if (dbPct) dbPct.textContent = `${pct}% Solved · 17 Topics`;
}

function populateRisingBrainNav() {
  const sb = document.getElementById('rbTopicNavSidebar');
  const dd = document.getElementById('rbTopicSelectDropdown');
  if (!sb || !dd) return;

  let sbHtml = '<div class="sidebar-header" style="padding:0.5rem 0.75rem; font-size:11px; font-weight:800; text-transform:uppercase; color:var(--text-dim);">Topics (17)</div>';
  let ddHtml = '<option value="all">📚 All 17 Topics (385)</option>';

  sbHtml += `
    <div class="pattern-nav-item active" onclick="jumpToRbTopic('all')" style="border-left:2px solid transparent;">
      <span class="pnav-title">All Topics</span>
      <span class="pnav-count" id="rb-nav-all-count">385</span>
    </div>
  `;

  RISINGBRAIN_DATA.forEach(t => {
    const doneC = doneRisingBrainProbsForTopic(t);
    const totalC = t.patterns.reduce((acc, p) => acc + p.problems.length, 0);

    sbHtml += `
      <div class="pattern-nav-item" id="rb-pnav-${t.id}" onclick="jumpToRbTopic('${t.id}')">
        <span class="pnav-title">${t.name}</span>
        <span class="pnav-count">${doneC}/${totalC}</span>
      </div>
    `;
    ddHtml += `<option value="${t.id}">${t.name} (${doneC}/${totalC})</option>`;
  });

  sb.innerHTML = sbHtml;
  dd.innerHTML = ddHtml;
}
"""

# Inject before Initialization
init_anchor = "/* ==========================================================================\n   INITIALIZATION"
if init_anchor in html:
    html = html.replace(init_anchor, rb_js_logic + "\n" + init_anchor)
    print("Injected RisingBrain JS Logic")

# 8. Update switchView
switch_striver = "else if(viewName === 'striver') renderStriverContent();"
switch_rb = "else if(viewName === 'striver') renderStriverContent();\n  else if(viewName === 'risingbrain') { renderRisingBrainContent(); updateRisingBrainStats(); }"
html = html.replace(switch_striver, switch_rb)

title_striver = "striver: 'Striver A2Z DSA Sheet (455 Problems)',"
title_rb = "striver: 'Striver A2Z DSA Sheet (455 Problems)',\n    risingbrain: 'RisingBrain Pattern Wise (385 Problems · 17 Topics)',"
html = html.replace(title_striver, title_rb)

# 9. Update openRevisionModal and addRevisionEvent to support 'risingbrain'
tracker_tag_old = "const trackerTag = trackerType === 'striver' ? '[Striver A2Z]' : '[DSA Patterns]';"
tracker_tag_new = "const trackerTag = trackerType === 'risingbrain' ? '[RisingBrain]' : trackerType === 'striver' ? '[Striver A2Z]' : '[DSA Patterns]';"
html = html.replace(tracker_tag_old, tracker_tag_new)

pobj_lookup_old = "const pObj = isStriver ? getStriverProblemObj(probNum) : getProblemObj(probNum);"
pobj_lookup_new = """const pObj = trackerType === 'risingbrain' ? getRisingBrainProblemObj(probNum) : isStriver ? getStriverProblemObj(probNum) : getProblemObj(probNum);"""
html = html.replace(pobj_lookup_old, pobj_lookup_new)

stepname_old = "const stepName = isStriver ? (pObj?.stepName || 'Striver Step') : (stepObj?.name || 'DSA Pattern');"
stepname_new = "const stepName = trackerType === 'risingbrain' ? (pObj?.topicName + ' · ' + pObj?.patternName) : isStriver ? (pObj?.stepName || 'Striver Step') : (stepObj?.name || 'DSA Pattern');"
html = html.replace(stepname_old, stepname_new)

ps_lookup_old = "const ps = isStriver ? getStriverProblemState(probNum) : getProblemState(probNum);"
ps_lookup_new = "const ps = trackerType === 'risingbrain' ? getRisingBrainProblemState(probNum) : isStriver ? getStriverProblemState(probNum) : getProblemState(probNum);"
html = html.replace(ps_lookup_old, ps_lookup_new)

# In addRevisionEvent
rev_save_old = """  if (isStriver) {
    striverState.problems[probNum] = ps;
    saveStriverState();
    renderStriverContent();
  } else {
    state.problems[probNum] = ps;
    saveState();
    refreshAllUI();
  }"""

rev_save_new = """  if (trackerType === 'risingbrain') {
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
html = html.replace(rev_save_old, rev_save_new)

# Add getRisingBrainProblemObj helper
obj_helper = """
function getRisingBrainProblemObj(n) {
  for (const t of RISINGBRAIN_DATA) {
    for (const pat of t.patterns) {
      for (const p of pat.problems) {
        if (p.n === n) return { ...p, topicName: t.name, patternName: pat.name };
      }
    }
  }
  return null;
}
"""
html = html.replace("function getStriverProblemObj(n) {", obj_helper + "\nfunction getStriverProblemObj(n) {")

# 10. Update buildCompleteExportObject & backups
build_export_old = """function buildCompleteExportObject() {
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
}"""

build_export_new = """function buildCompleteExportObject() {
  return {
    version: 5,
    appBuildVersion: APP_BUILD_VERSION,
    exportedAt: new Date().toISOString(),
    dsaState: state,
    striverState: striverState,
    risingBrainState: risingBrainState,
    diaryState: diaryState,
    plannerState: plannerState,
    studyState: studyState,
    settingsState: settingsState
  };
}"""
html = html.replace(build_export_old, build_export_new)

# In handleVersionUpgradeArchiving:
raw_v3_arch = "const rawStriver = localStorage.getItem(STORAGE_STRIVER_KEY);"
raw_rb_arch = "const rawStriver = localStorage.getItem(STORAGE_STRIVER_KEY);\n      const rawRb = localStorage.getItem(STORAGE_RISINGBRAIN_KEY);"
html = html.replace(raw_v3_arch, raw_rb_arch)

raw_check = "if (rawV3 || rawStriver) {"
raw_check_new = "if (rawV3 || rawStriver || rawRb) {"
html = html.replace(raw_check, raw_check_new)

raw_store = "striverRaw: rawStriver\n        }));"
raw_store_new = "striverRaw: rawStriver,\n          risingBrainRaw: rawRb\n        }));"
html = html.replace(raw_store, raw_store_new)

# In handleImportFile:
import_stats_old = "const diaryCount = parsed.diaryState ? Object.keys(parsed.diaryState.entries || {}).length : 0;"
import_stats_new = """let rbCount = 0;
      if (parsed.risingBrainState && parsed.risingBrainState.problems) {
        Object.values(parsed.risingBrainState.problems).forEach(p => { if (p.done) rbCount++; });
      }
      const diaryCount = parsed.diaryState ? Object.keys(parsed.diaryState.entries || {}).length : 0;"""
html = html.replace(import_stats_old, import_stats_new)

preview_old = "<div>• Questions Solved: <b>${dsaCount}</b></div>"
preview_new = "<div>• DSA Questions Solved: <b>${dsaCount}</b></div>\n        <div>• Striver Solved: <b>${striverCount}</b></div>\n        <div>• RisingBrain Solved: <b>${rbCount}</b></div>"
html = html.replace(preview_old, preview_new)

# In executeImportConfirmed:
import_exec_old = "if(pendingImportData.striverState) { striverState = pendingImportData.striverState; saveStriverState(); }"
import_exec_new = "if(pendingImportData.striverState) { striverState = pendingImportData.striverState; saveStriverState(); }\n    if(pendingImportData.risingBrainState) { risingBrainState = pendingImportData.risingBrainState; saveRisingBrainState(); }"
html = html.replace(import_exec_old, import_exec_new)

# In triggerResetEverything:
reset_old = "const keysToRemove = [STORAGE_KEY_V3, STORAGE_KEY_V2, STORAGE_KEY_V1, STORAGE_STRIVER_KEY, 'a2z_v2', 'a2z_starred', 'a2z_notes', 'a2z_dates', 'a2z_maxstreak', STORAGE_DIARY_KEY, STORAGE_PLANNER_KEY, STORAGE_STUDY_KEY, STORAGE_SETTINGS_KEY];"
reset_new = "const keysToRemove = [STORAGE_KEY_V3, STORAGE_KEY_V2, STORAGE_KEY_V1, STORAGE_STRIVER_KEY, STORAGE_RISINGBRAIN_KEY, 'a2z_v2', 'a2z_starred', 'a2z_notes', 'a2z_dates', 'a2z_maxstreak', STORAGE_DIARY_KEY, STORAGE_PLANNER_KEY, STORAGE_STUDY_KEY, STORAGE_SETTINGS_KEY];"
html = html.replace(reset_old, reset_new)

# 11. Update updateHeaderStats
hdr_stats_old = "function updateHeaderStats() {"
hdr_stats_new = """function updateHeaderStats() {
  const dsaDone = Object.values(state.problems).filter(p => p.done).length;
  const striverDone = Object.values(striverState.problems).filter(p => p.done).length;
  const rbDone = Object.values(risingBrainState.problems).filter(p => p.done).length;

  const dsaTotal = 184;
  const striverTotal = 455;
  const rbTotal = totalRisingBrainProbs();

  const dsaBadge = document.getElementById('nav-dsa-badge');
  if (dsaBadge) dsaBadge.textContent = `${dsaDone}/${dsaTotal}`;

  const striverBadge = document.getElementById('nav-striver-badge');
  if (striverBadge) striverBadge.textContent = `${striverDone}/${striverTotal}`;

  const rbBadge = document.getElementById('nav-risingbrain-badge');
  if (rbBadge) rbBadge.textContent = `${rbDone}/${rbTotal}`;

  const activeView = document.querySelector('.view-section.active')?.id || 'view-dashboard';
  let curDone = dsaDone;
  let curTotal = dsaTotal;

  if (activeView === 'view-striver') {
    curDone = striverDone;
    curTotal = striverTotal;
  } else if (activeView === 'view-risingbrain') {
    curDone = rbDone;
    curTotal = rbTotal;
  }

  const hdrDone = document.getElementById('hdr-done');
  if (hdrDone) hdrDone.textContent = curDone;

  const hdrTotal = document.getElementById('hdr-total');
  if (hdrTotal) hdrTotal.textContent = curTotal;

  const hdrPct = document.getElementById('hdr-pct');
  if (hdrPct) hdrPct.textContent = `${curTotal > 0 ? Math.round((curDone / curTotal) * 100) : 0}%`;

  // Update large 3-tracker overview cards
  const dbDsaCount = document.getElementById('db-dsa-count-large');
  if (dbDsaCount) dbDsaCount.innerHTML = `${dsaDone} <span style="font-size:13px; color:var(--text-muted); font-weight:500;">/ ${dsaTotal}</span>`;
  const dbDsaBar = document.getElementById('db-dsa-bar-large');
  if (dbDsaBar) dbDsaBar.style.width = `${Math.round((dsaDone / dsaTotal) * 100)}%`;
  const dbDsaPct = document.getElementById('db-dsa-pct-large');
  if (dbDsaPct) dbDsaPct.textContent = `${Math.round((dsaDone / dsaTotal) * 100)}% Solved · 19 Patterns`;

  const dbStriverCount = document.getElementById('db-striver-count-large');
  if (dbStriverCount) dbStriverCount.innerHTML = `${striverDone} <span style="font-size:13px; color:var(--text-muted); font-weight:500;">/ ${striverTotal}</span>`;
  const dbStriverBar = document.getElementById('db-striver-bar-large');
  if (dbStriverBar) dbStriverBar.style.width = `${Math.round((striverDone / striverTotal) * 100)}%`;
  const dbStriverPct = document.getElementById('db-striver-pct-large');
  if (dbStriverPct) dbStriverPct.textContent = `${Math.round((striverDone / striverTotal) * 100)}% Solved · 18 Steps`;

  const dbRbCount = document.getElementById('db-rb-count-large');
  if (dbRbCount) dbRbCount.innerHTML = `${rbDone} <span style="font-size:13px; color:var(--text-muted); font-weight:500;">/ ${rbTotal}</span>`;
  const dbRbBar = document.getElementById('db-rb-bar-large');
  if (dbRbBar) dbRbBar.style.width = `${Math.round((rbDone / rbTotal) * 100)}%`;
  const dbRbPct = document.getElementById('db-rb-pct-large');
  if (dbRbPct) dbRbPct.textContent = `${Math.round((rbDone / rbTotal) * 100)}% Solved · 17 Topics`;
"""
html = html.replace(hdr_stats_old, hdr_stats_new)

# 12. Update init()
init_calls_old = "  loadState();\n  loadStriverState();\n  loadOtherStates();"
init_calls_new = "  loadState();\n  loadStriverState();\n  loadRisingBrainState();\n  loadOtherStates();"
html = html.replace(init_calls_old, init_calls_new)

init_render_old = "  renderDsaContent();\n  renderStriverContent();"
init_render_new = "  populateRisingBrainNav();\n  renderDsaContent();\n  renderStriverContent();\n  renderRisingBrainContent();\n  updateRisingBrainStats();"
html = html.replace(init_render_old, init_render_new)

# Save test output
out_file = "/Users/devrajput/.gemini/antigravity-ide/scratch/integrated_v5_test.html"
with open(out_file, "w", encoding="utf-8") as out:
    out.write(html)

print(f"Successfully generated {out_file}: {len(html)} bytes")
