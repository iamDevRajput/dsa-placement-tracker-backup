import json, os, re

base_path = "/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html"
with open(base_path, "r", encoding="utf-8") as f:
    html = f.read()

with open("/Users/devrajput/.gemini/antigravity-ide/scratch/risingbrain_data.js", "r", encoding="utf-8") as f:
    rb_data_js = f.read()

# 1. Update APP_BUILD_VERSION
html = html.replace("const APP_BUILD_VERSION = '2026.10.25-offline-v4';", "const APP_BUILD_VERSION = '2026.10.26-offline-v5';")

# 2. Inject RISINGBRAIN_DATA right before STRIVER_DATA
idx_striver = html.find("/* ==========================================================================\n   STRIVER A2Z 455 QUESTIONS DATASET")
if idx_striver != -1:
    rb_block = "\n/* ==========================================================================\n   RISINGBRAIN PATTERN WISE 385 QUESTIONS DATASET\n   ========================================================================== */\n" + rb_data_js + "\n\n"
    html = html[:idx_striver] + rb_block + html[idx_striver:]
else:
    print("Warning: STRIVER_DATA header not found")

# 3. Add CSS styles for RisingBrain section
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
.rb-status-select.status-not_started { color: var(--text-dim); }
.rb-status-select.status-attempted { color: #f59e0b; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.08); }
.rb-status-select.status-solved_independent { color: #10b981; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.1); }
.rb-status-select.status-solved_hint { color: #f97316; border-color: rgba(249, 115, 22, 0.4); background: rgba(249, 115, 22, 0.1); }
.rb-status-select.status-needs_revision { color: #a855f7; border-color: rgba(168, 85, 247, 0.4); background: rgba(168, 85, 247, 0.1); }
.rb-status-select.status-mastered { color: #eab308; border-color: rgba(234, 179, 8, 0.5); background: rgba(234, 179, 8, 0.12); }

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
"""

idx_style_end = html.find("</style>")
if idx_style_end != -1:
    html = html[:idx_style_end] + rb_css + "\n" + html[idx_style_end:]
else:
    print("Warning: </style> not found")

# 4. Add Sidebar Navigation item for RisingBrain
nav_striver_btn = """    <button class="nav-item" onclick="switchView('striver', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
      <span>Striver Sheet</span>
      <span class="nav-badge accent" id="nav-striver-badge">0/455</span>
    </button>"""

nav_rb_btn = """    <button class="nav-item" onclick="switchView('striver', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
      <span>Striver Sheet</span>
      <span class="nav-badge accent" id="nav-striver-badge">0/455</span>
    </button>
    <button class="nav-item" onclick="switchView('risingbrain', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 18V5"/><path d="M15 13a4.17 4.17 0 0 1-3-4 4.17 4.17 0 0 1-3 4"/><path d="M17.598 6.5A3 3 0 1 0 12 5a3 3 0 1 0-5.598 1.5"/><path d="M17.997 5.125a4 4 0 0 1 2.526 5.77"/><path d="M18 18a4 4 0 0 0 2-7.464"/><path d="M19.967 17.483A4 4 0 1 1 12 18a4 4 0 1 1-7.967-.517"/><path d="M6 18a4 4 0 0 1-2-7.464"/><path d="M6.003 5.125a4 4 0 0 0-2.526 5.77"/></svg>
      <span>RisingBrain Sheet</span>
      <span class="nav-badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3);" id="nav-risingbrain-badge">0/385</span>
    </button>"""

if nav_striver_btn in html:
    html = html.replace(nav_striver_btn, nav_rb_btn)
else:
    print("Warning: nav_striver_btn exact text not found")

# 5. Add Dashboard overview card for RisingBrain
dashboard_cards_anchor = """      <div class="stat-card">
        <div class="stat-card-header">
          <span class="stat-label">Striver Sheet</span>
          <span class="stat-badge accent">455 Problems</span>
        </div>
        <div class="stat-val" id="db-striver-solved-num">0 <span style="font-size:14px; font-weight:500; color:var(--text-muted);">/ 455</span></div>
        <div class="progress-bar-wrap" style="margin-top:0.5rem;">
          <div class="progress-bar-fill accent" id="db-striver-progress" style="width:0%;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.6rem;">
          <span style="font-size:11.5px; color:var(--text-dim);" id="db-striver-pct">0% Complete · 18 Steps</span>
          <button class="btn btn-sm btn-ghost" onclick="switchView('striver')" style="color:var(--accent); padding:2px 8px; font-size:11.5px;">Open →</button>
        </div>
      </div>"""

rb_dashboard_card = """      <div class="stat-card" style="border-top:3px solid #10b981;">
        <div class="stat-card-header">
          <span class="stat-label">RisingBrain Sheet</span>
          <span class="stat-badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3);">385 Problems</span>
        </div>
        <div class="stat-val" id="db-rb-solved-num">0 <span style="font-size:14px; font-weight:500; color:var(--text-muted);">/ 385</span></div>
        <div class="progress-bar-wrap" style="margin-top:0.5rem;">
          <div class="progress-bar-fill" id="db-rb-progress" style="width:0%; background:#10b981;"></div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.6rem;">
          <span style="font-size:11.5px; color:var(--text-dim);" id="db-rb-pct">0% Complete · 17 Topics</span>
          <button class="btn btn-sm btn-ghost" onclick="switchView('risingbrain')" style="color:#10b981; padding:2px 8px; font-size:11.5px;">Open →</button>
        </div>
      </div>"""

if dashboard_cards_anchor in html:
    html = html.replace(dashboard_cards_anchor, dashboard_cards_anchor + "\n" + rb_dashboard_card)
else:
    print("Warning: dashboard_cards_anchor not found")

# 6. Add view-risingbrain section after view-striver
view_striver_end = "</section>\n\n    <!-- VIEW: SPACED REVISION CENTER -->"
if view_striver_end in html:
    rb_section_html = """</section>

    <!-- VIEW: RISINGBRAIN PATTERN-WISE SHEET -->
    <section class="view-section" id="view-risingbrain">
      <div class="striver-header-banner" style="border-left: 4px solid #10b981;">
        <div style="flex:1;">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
            <span class="badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3);">🧠 RisingBrain Sheet</span>
            <span style="font-size:12px; color:var(--text-dim);">385 Problems · 17 Topics · 68 Patterns</span>
          </div>
          <h2 style="font-size:1.5rem; font-weight:800; margin:0 0 4px 0;">RisingBrain Pattern Wise Sheet</h2>
          <p style="font-size:13px; color:var(--text-muted); margin:0;">Master data structures and algorithms topic by topic, grouped by pattern with recognition clues and verified problem links.</p>
        </div>
        <div style="display:flex; gap:1.5rem; align-items:center; margin-top:0.75rem;">
          <div style="text-align:right;">
            <div style="font-size:1.25rem; font-weight:800; font-family:var(--font-mono); color:#10b981;" id="rb-solved-total-display">0 / 385</div>
            <div style="font-size:11.5px; color:var(--text-muted);" id="rb-pct-total-display">0% Completed</div>
          </div>
          <div style="width:140px;">
            <div class="progress-bar-wrap">
              <div class="progress-bar-fill" id="rb-main-progress-bar" style="width:0%; background:#10b981;"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Search, Difficulty, Status & Topic Filter Bar -->
      <div class="filter-bar" style="margin-top:1rem; flex-wrap:wrap; gap:0.5rem; background:var(--surface2); padding:0.75rem 1rem; border-radius:var(--radius-md); border:1px solid var(--border-subtle);">
        <div class="search-input-wrap" style="flex:1; min-width:240px;">
          <input type="text" id="rbSearchInput" class="search-input" placeholder="🔍 Search problem, reference (e.g. LC 167), pattern, company..." oninput="renderRisingBrainContent()">
        </div>

        <select id="rbTopicFilter" class="filter-select" onchange="filterRisingBrainTopic(this.value)" style="border-radius:6px; padding:6px 10px; background:var(--surface3); color:var(--text-main); border:1px solid var(--border-subtle);">
          <option value="all">📚 All 17 Topics (385)</option>
        </select>

        <div class="filter-btn-group" id="rbDiffFilterGroup">
          <button class="filter-btn active" data-diff="all" onclick="filterRisingBrainDiff('all')">All (385)</button>
          <button class="filter-btn" data-diff="e" onclick="filterRisingBrainDiff('e')">Easy (81)</button>
          <button class="filter-btn" data-diff="m" onclick="filterRisingBrainDiff('m')">Medium (251)</button>
          <button class="filter-btn" data-diff="h" onclick="filterRisingBrainDiff('h')">Hard (53)</button>
        </div>

        <select id="rbStatusFilter" class="filter-select" onchange="filterRisingBrainStatus(this.value)" style="border-radius:6px; padding:6px 10px; background:var(--surface3); color:var(--text-main); border:1px solid var(--border-subtle);">
          <option value="all">⚡ All Statuses</option>
          <option value="not_started">⚪ Not Started</option>
          <option value="attempted">🟡 Attempted</option>
          <option value="solved">🟢 Solved (All)</option>
          <option value="solved_independent">🟢 Solved Solo</option>
          <option value="solved_hint">🟠 Solved Hint</option>
          <option value="needs_revision">🟣 Needs Revision</option>
          <option value="mastered">🏆 Mastered</option>
          <option value="starred">⭐ Starred Only</option>
        </select>

        <select id="rbCompanyFilter" class="filter-select" onchange="filterRisingBrainCompany(this.value)" style="border-radius:6px; padding:6px 10px; background:var(--surface3); color:var(--text-main); border:1px solid var(--border-subtle);">
          <option value="all">🏢 All Companies</option>
        </select>

        <div style="display:flex; gap:4px; margin-left:auto;">
          <button class="btn btn-sm btn-ghost" onclick="toggleAllRbPatterns(true)" title="Expand All Patterns">▼ Expand All</button>
          <button class="btn btn-sm btn-ghost" onclick="toggleAllRbPatterns(false)" title="Collapse All Patterns">▲ Collapse All</button>
        </div>
      </div>

      <!-- Content Container -->
      <div id="risingBrainContent" style="margin-top:1.25rem;"></div>
    </section>

    <!-- VIEW: SPACED REVISION CENTER -->"""
    html = html.replace(view_striver_end, rb_section_html)
else:
    print("Warning: view_striver_end exact anchor not found")

with open("/Users/devrajput/.gemini/antigravity-ide/scratch/integrated_step1.html", "w", encoding="utf-8") as out:
    out.write(html)

print("Step 1 completed: injected CSS, navigation, dashboard card, and view section.")
