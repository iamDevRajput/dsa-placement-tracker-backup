import os
import re

def generate_dsa_markup():
    return """<!-- VIEW 2: DSA PATTERNS (UPGRADED PREMIER DESIGN) -->
    <section class="view-section" id="view-dsa">
      <!-- 1. HERO BANNER & COMPACT PROGRESS DASHBOARD -->
      <div class="rb-hero-header">
        <div class="rb-hero-left">
          <div class="rb-hero-badge">
            <span class="rb-pulse-dot"></span>
            <span>Pattern-Wise Practice</span>
            <span class="rb-badge-tag">184 Problems · 19 Patterns · Placement Pro</span>
          </div>
          <h1 class="rb-hero-title">DSA Patterns Tracker</h1>
          <p class="rb-hero-subtitle">
            Master algorithmic problem-solving with 19 foundational coding interview patterns and spaced repetition review.
          </p>
          <div class="rb-hero-actions">
            <button class="rb-action-btn primary" onclick="jumpToNextUnsolvedDsaProblem()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <span>Resume Next Problem</span>
            </button>
            <button class="rb-action-btn" onclick="expandAllPatterns(true)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="7 13 12 18 17 13"/><polyline points="7 6 12 11 17 6"/></svg>
              <span>Expand All</span>
            </button>
            <button class="rb-action-btn" onclick="expandAllPatterns(false)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="17 11 12 6 7 11"/><polyline points="17 18 12 13 7 18"/></svg>
              <span>Collapse All</span>
            </button>
          </div>
        </div>

        <div class="rb-hero-dashboard">
          <div class="rb-metric-card">
            <div class="rb-radial-gauge-container">
              <svg class="rb-radial-gauge" viewBox="0 0 100 100">
                <circle class="rb-gauge-bg" cx="50" cy="50" r="42" />
                <circle class="rb-gauge-fill" id="dsa-gauge-circle" cx="50" cy="50" r="42" />
              </svg>
              <div class="rb-radial-content">
                <span class="rb-gauge-pct" id="dsa-radial-pct">0%</span>
                <span class="rb-gauge-label">Done</span>
              </div>
            </div>
            <div class="rb-metric-info">
              <div class="rb-metric-heading">Overall Completion</div>
              <div class="rb-metric-main-stat" id="dsa-header-solved-count">0 <span class="rb-metric-denom">/ 184</span></div>
              <div class="rb-quick-chips">
                <span class="rb-quick-chip starred" id="dsa-stat-chip-starred" title="Starred problems">★ 0</span>
                <span class="rb-quick-chip mastered" id="dsa-stat-chip-mastered" title="Mastered problems">👑 0</span>
                <span class="rb-quick-chip needsrev" id="dsa-stat-chip-needsrev" title="Needs revision">🟣 0</span>
              </div>
            </div>
          </div>

          <div class="rb-diff-bars-card">
            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-easy">Easy</span>
                <span class="rb-diff-bar-numbers" id="dsa-easy-ratio">0 / 56 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill easy" id="dsa-easy-fill" style="width:0%;"></div></div>
            </div>

            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-med">Medium</span>
                <span class="rb-diff-bar-numbers" id="dsa-med-ratio">0 / 93 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill med" id="dsa-med-fill" style="width:0%;"></div></div>
            </div>

            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-hard">Hard</span>
                <span class="rb-diff-bar-numbers" id="dsa-hard-ratio">0 / 35 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill hard" id="dsa-hard-fill" style="width:0%;"></div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. SEARCH & ADVANCED FILTER CONTROLS -->
      <div class="rb-controls-bar">
        <div class="rb-controls-top">
          <div class="rb-search-wrapper">
            <svg class="rb-search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="text" id="search" class="rb-search-input" placeholder="Search 184 problems by title, problem #, or pattern..." oninput="handleDsaSearchInput(this.value)">
            <button id="dsaSearchClearBtn" class="rb-search-clear" onclick="clearDsaSearch()" title="Clear search" style="display:none;">✕</button>
          </div>

          <div class="rb-filter-selects">
            <select class="form-select rb-select" id="patternSelectDropdown" onchange="jumpToPattern(this.value)">
              <!-- Populated dynamically with all 19 patterns -->
            </select>
          </div>
        </div>

        <div class="rb-filter-pills-row">
          <div class="rb-pill-group">
            <button class="rb-pill active" id="f-all" onclick="setDsaFilter('all', this)">All <span class="rb-pill-count">184</span></button>
            <button class="rb-pill diff-e" id="f-dsa-easy" onclick="setDsaFilter('easy', this)">Easy <span class="rb-pill-count">56</span></button>
            <button class="rb-pill diff-m" id="f-dsa-med" onclick="setDsaFilter('med', this)">Medium <span class="rb-pill-count">93</span></button>
            <button class="rb-pill diff-h" id="f-dsa-hard" onclick="setDsaFilter('hard', this)">Hard <span class="rb-pill-count">35</span></button>
          </div>

          <div class="rb-pill-divider"></div>

          <div class="rb-pill-group">
            <button class="rb-pill" id="f-pending" onclick="setDsaFilter('pending', this)">Pending</button>
            <button class="rb-pill" id="f-done" onclick="setDsaFilter('done', this)">Done</button>
            <button class="rb-pill" id="f-starred" onclick="setDsaFilter('starred', this)">⭐ Starred</button>
            <button class="rb-pill" id="f-due" onclick="setDsaFilter('due', this)">⏰ Due Today</button>
            <button class="rb-pill" id="f-overdue" onclick="setDsaFilter('overdue', this)">⚠️ Overdue</button>
            <button class="rb-pill" id="f-never" onclick="setDsaFilter('never', this)">Never Revised</button>
            <button class="rb-pill" id="f-mastered" onclick="setDsaFilter('mastered', this)">👑 Mastered</button>
          </div>
        </div>
      </div>

      <!-- 3. MAIN WORKSPACE: SIDEBAR & PATTERNS -->
      <div class="rb-main-workspace">
        <!-- Sidebar Jump To Pattern -->
        <aside class="rb-topic-sidebar" id="patternNavSidebar">
          <!-- Populated dynamically with 19 patterns -->
        </aside>

        <!-- Main Pattern Content -->
        <div class="rb-content-area" id="dsaContent">
          <!-- 19 Patterns & 184 problems -->
        </div>
      </div>
    </section>"""

def generate_striver_markup():
    return """<!-- VIEW 2.5: STRIVER SHEET (UPGRADED PREMIER DESIGN) -->
    <section class="view-section" id="view-striver">
      <!-- 1. HERO BANNER & COMPACT PROGRESS DASHBOARD -->
      <div class="rb-hero-header">
        <div class="rb-hero-left">
          <div class="rb-hero-badge">
            <span class="rb-pulse-dot"></span>
            <span>A2Z DSA Curriculum</span>
            <span class="rb-badge-tag">455 Problems · 18 Steps · SDE Roadmap</span>
          </div>
          <h1 class="rb-hero-title">Striver A2Z DSA Tracker</h1>
          <p class="rb-hero-subtitle">
            Comprehensive step-by-step roadmap from programming basics to advanced data structures, graphs, and dynamic programming.
          </p>
          <div class="rb-hero-actions">
            <button class="rb-action-btn primary" onclick="jumpToNextUnsolvedStriverProblem()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <span>Resume Next Problem</span>
            </button>
            <button class="rb-action-btn" onclick="expandAllStriverSteps(true)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="7 13 12 18 17 13"/><polyline points="7 6 12 11 17 6"/></svg>
              <span>Expand All</span>
            </button>
            <button class="rb-action-btn" onclick="expandAllStriverSteps(false)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="17 11 12 6 7 11"/><polyline points="17 18 12 13 7 18"/></svg>
              <span>Collapse All</span>
            </button>
          </div>
        </div>

        <div class="rb-hero-dashboard">
          <div class="rb-metric-card">
            <div class="rb-radial-gauge-container">
              <svg class="rb-radial-gauge" viewBox="0 0 100 100">
                <circle class="rb-gauge-bg" cx="50" cy="50" r="42" />
                <circle class="rb-gauge-fill" id="striver-gauge-circle" cx="50" cy="50" r="42" />
              </svg>
              <div class="rb-radial-content">
                <span class="rb-gauge-pct" id="striver-radial-pct">0%</span>
                <span class="rb-gauge-label">Done</span>
              </div>
            </div>
            <div class="rb-metric-info">
              <div class="rb-metric-heading">Overall Completion</div>
              <div class="rb-metric-main-stat" id="striver-header-solved-count">0 <span class="rb-metric-denom">/ 455</span></div>
              <div class="rb-quick-chips">
                <span class="rb-quick-chip starred" id="striver-stat-chip-starred" title="Starred problems">★ 0</span>
                <span class="rb-quick-chip mastered" id="striver-stat-chip-mastered" title="Mastered problems">👑 0</span>
                <span class="rb-quick-chip needsrev" id="striver-stat-chip-needsrev" title="Needs revision">🟣 0</span>
              </div>
            </div>
          </div>

          <div class="rb-diff-bars-card">
            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-easy">Easy</span>
                <span class="rb-diff-bar-numbers" id="striver-easy-ratio">0 / 125 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill easy" id="striver-easy-fill" style="width:0%;"></div></div>
            </div>

            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-med">Medium</span>
                <span class="rb-diff-bar-numbers" id="striver-med-ratio">0 / 255 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill med" id="striver-med-fill" style="width:0%;"></div></div>
            </div>

            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-hard">Hard</span>
                <span class="rb-diff-bar-numbers" id="striver-hard-ratio">0 / 75 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill hard" id="striver-hard-fill" style="width:0%;"></div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. SEARCH & ADVANCED FILTER CONTROLS -->
      <div class="rb-controls-bar">
        <div class="rb-controls-top">
          <div class="rb-search-wrapper">
            <svg class="rb-search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="text" id="striverSearch" class="rb-search-input" placeholder="Search 455 problems by title, problem #, or step..." oninput="handleStriverSearchInput(this.value)">
            <button id="striverSearchClearBtn" class="rb-search-clear" onclick="clearStriverSearch()" title="Clear search" style="display:none;">✕</button>
          </div>

          <div class="rb-filter-selects">
            <select class="form-select rb-select" id="striverStepSelectDropdown" onchange="jumpToStriverStep(this.value)">
              <!-- Populated dynamically with all 18 steps -->
            </select>

            <select class="form-select rb-select" id="striverCoFilter" onchange="setStriverCompany(this.value)">
              <option value="all">🏢 All Companies</option>
              <option value="amz">🛒 Amazon</option>
              <option value="ggl">🔍 Google</option>
              <option value="msft">🪟 Microsoft</option>
              <option value="meta">👤 Meta</option>
              <option value="fk">🛍️ Flipkart</option>
              <option value="adobe">🎨 Adobe</option>
              <option value="sam">📱 Samsung</option>
              <option disabled>── Mass Recruiters ──</option>
              <option value="tcs">🔵 TCS</option>
              <option value="wipro">🟣 Wipro</option>
              <option value="infy">🟡 Infosys</option>
              <option value="cog">🟠 Cognizant</option>
              <option value="cap">🔴 Capgemini</option>
              <option value="hcl">🟢 HCL</option>
              <option value="acc">⚫ Accenture</option>
              <option value="techm">🔷 Tech Mahindra</option>
            </select>
          </div>
        </div>

        <div class="rb-filter-pills-row">
          <div class="rb-pill-group">
            <button class="rb-pill active" id="f-striver-all" onclick="setStriverFilter('all', this)">All <span class="rb-pill-count">455</span></button>
            <button class="rb-pill diff-e" id="f-striver-easy" onclick="setStriverFilter('easy', this)">Easy <span class="rb-pill-count">125</span></button>
            <button class="rb-pill diff-m" id="f-striver-med" onclick="setStriverFilter('med', this)">Medium <span class="rb-pill-count">255</span></button>
            <button class="rb-pill diff-h" id="f-striver-hard" onclick="setStriverFilter('hard', this)">Hard <span class="rb-pill-count">75</span></button>
          </div>

          <div class="rb-pill-divider"></div>

          <div class="rb-pill-group">
            <button class="rb-pill" id="f-striver-pending" onclick="setStriverFilter('pending', this)">Pending</button>
            <button class="rb-pill" id="f-striver-done" onclick="setStriverFilter('done', this)">Done</button>
            <button class="rb-pill" id="f-striver-starred" onclick="setStriverFilter('starred', this)">⭐ Starred</button>
            <button class="rb-pill" id="f-striver-due" onclick="setStriverFilter('due', this)">⏰ Due Today</button>
            <button class="rb-pill" id="f-striver-overdue" onclick="setStriverFilter('overdue', this)">⚠️ Overdue</button>
            <button class="rb-pill" id="f-striver-never" onclick="setStriverFilter('never', this)">Never Revised</button>
            <button class="rb-pill" id="f-striver-mastered" onclick="setStriverFilter('mastered', this)">👑 Mastered</button>
          </div>
        </div>
      </div>

      <!-- 3. MAIN WORKSPACE: SIDEBAR & STEPS -->
      <div class="rb-main-workspace">
        <!-- Sidebar Jump To Step -->
        <aside class="rb-topic-sidebar" id="striverStepNavSidebar">
          <!-- Populated dynamically with 18 steps -->
        </aside>

        <!-- Main Step Content -->
        <div class="rb-content-area" id="striverContent">
          <!-- 18 Steps & 455 problems -->
        </div>
      </div>
    </section>"""

def generate_upgraded_dsa_js():
    return """
/* ==========================================================================
   DSA PATTERNS UPGRADED INTERACTIVE CONTROLLER (Emerald Theme)
   ========================================================================== */

function handleDsaSearchInput(val) {
  const clearBtn = document.getElementById('dsaSearchClearBtn');
  if (clearBtn) clearBtn.style.display = val && val.trim().length > 0 ? 'flex' : 'none';
  renderDsaContent();
}

function clearDsaSearch() {
  const input = document.getElementById('search');
  if (input) {
    input.value = '';
    input.focus();
  }
  const clearBtn = document.getElementById('dsaSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';
  renderDsaContent();
}

function resetAllDsaFilters() {
  const input = document.getElementById('search');
  if (input) input.value = '';
  const clearBtn = document.getElementById('dsaSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';

  currentDsaFilter = 'all';
  jumpToPattern('all');
  const allBtn = document.getElementById('f-all');
  if (allBtn) setDsaFilter('all', allBtn);
  renderDsaContent();
}

function jumpToNextUnsolvedDsaProblem() {
  let nextUnsolved = null;
  for (const step of DATA) {
    if (currentActiveStep !== 'all' && String(step.id) !== String(currentActiveStep)) continue;
    for (const p of step.problems) {
      const ps = getProblemState(p.n);
      if (!ps.done) {
        nextUnsolved = { step, prob: p };
        break;
      }
    }
    if (nextUnsolved) break;
  }

  if (!nextUnsolved && currentActiveStep !== 'all') {
    for (const step of DATA) {
      for (const p of step.problems) {
        const ps = getProblemState(p.n);
        if (!ps.done) {
          nextUnsolved = { step, prob: p };
          break;
        }
      }
      if (nextUnsolved) break;
    }
  }

  if (nextUnsolved) {
    delete state.collapsedSteps[nextUnsolved.step.id];
    saveState();
    renderDsaContent();

    setTimeout(() => {
      const el = document.getElementById('prob-' + nextUnsolved.prob.n);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.boxShadow = '0 0 0 3px #10b981, 0 0 20px rgba(16, 185, 129, 0.4)';
        setTimeout(() => el.style.boxShadow = '', 2500);
      }
    }, 150);
    showToast(`Jumped to Next Unsolved: #${nextUnsolved.prob.n} (${nextUnsolved.prob.t})`);
  } else {
    showToast('🎉 All 184 DSA Patterns problems are marked solved!');
  }
}

function updateDsaStats() {
  const total = totalProbs();
  const allStates = Object.values(state.problems);
  const done = allStates.filter(p => p.done).length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  let easyTotal = 0, easyDone = 0;
  let medTotal = 0, medDone = 0;
  let hardTotal = 0, hardDone = 0;
  let starredCount = 0, masteredCount = 0, needsRevCount = 0;

  DATA.forEach(s => {
    s.problems.forEach(p => {
      const ps = getProblemState(p.n);
      if (p.diff === 'e') {
        easyTotal++;
        if (ps.done) easyDone++;
      } else if (p.diff === 'm') {
        medTotal++;
        if (ps.done) medDone++;
      } else if (p.diff === 'h') {
        hardTotal++;
        if (ps.done) hardDone++;
      }
      if (ps.starred) starredCount++;
      if (ps.revisionCount >= 3) masteredCount++;
      if (isProblemDue(ps) || isProblemOverdue(ps)) needsRevCount++;
    });
  });

  const easyPct = easyTotal > 0 ? Math.round((easyDone / easyTotal) * 100) : 0;
  const medPct = medTotal > 0 ? Math.round((medDone / medTotal) * 100) : 0;
  const hardPct = hardTotal > 0 ? Math.round((hardDone / hardTotal) * 100) : 0;

  const badge = document.getElementById('nav-dsa-badge');
  if (badge) badge.textContent = `${done}/${total}`;

  const radialPct = document.getElementById('dsa-radial-pct');
  if (radialPct) radialPct.textContent = `${pct}%`;

  const gaugeCircle = document.getElementById('dsa-gauge-circle');
  if (gaugeCircle) {
    const circumference = 2 * Math.PI * 42;
    const offset = circumference - (pct / 100) * circumference;
    gaugeCircle.style.strokeDashoffset = offset;
  }

  const headerSolved = document.getElementById('dsa-header-solved-count');
  if (headerSolved) headerSolved.innerHTML = `${done} <span class="rb-metric-denom">/ ${total}</span>`;

  const chipStar = document.getElementById('dsa-stat-chip-starred');
  if (chipStar) chipStar.textContent = `★ ${starredCount}`;

  const chipMaster = document.getElementById('dsa-stat-chip-mastered');
  if (chipMaster) chipMaster.textContent = `👑 ${masteredCount}`;

  const chipRev = document.getElementById('dsa-stat-chip-needsrev');
  if (chipRev) chipRev.textContent = `🟣 ${needsRevCount}`;

  const eRatio = document.getElementById('dsa-easy-ratio');
  if (eRatio) eRatio.textContent = `${easyDone} / ${easyTotal} (${easyPct}%)`;
  const eFill = document.getElementById('dsa-easy-fill');
  if (eFill) eFill.style.width = `${easyPct}%`;

  const mRatio = document.getElementById('dsa-med-ratio');
  if (mRatio) mRatio.textContent = `${medDone} / ${medTotal} (${medPct}%)`;
  const mFill = document.getElementById('dsa-med-fill');
  if (mFill) mFill.style.width = `${medPct}%`;

  const hRatio = document.getElementById('dsa-hard-ratio');
  if (hRatio) hRatio.textContent = `${hardDone} / ${hardTotal} (${hardPct}%)`;
  const hFill = document.getElementById('dsa-hard-fill');
  if (hFill) hFill.style.width = `${hardPct}%`;
}

const DSA_PATTERN_ICONS = {
  1: 'TP', 2: 'SW', 3: 'FS', 4: 'MI', 5: 'CS',
  6: 'LL', 7: 'TB', 8: 'TD', 9: 'TH', 10: 'SS',
  11: 'BS', 12: 'BX', 13: 'TK', 14: 'KM', 15: 'KP',
  16: 'TS', 17: 'MT', 18: 'AP', 19: 'MS'
};

function buildPatternNavSidebar() {
  const sb = document.getElementById('patternNavSidebar');
  if (!sb) return;

  const total = totalProbs();
  const d = Object.values(state.problems).filter(p => p.done).length;
  const allPct = total > 0 ? Math.round((d / total) * 100) : 0;
  const isAllActive = currentActiveStep === 'all';

  let h = '<div class="rb-sidebar-heading">19 Patterns · 184 Problems</div>';
  h += `
    <div class="rb-topic-nav-item ${isAllActive ? 'active' : ''}" onclick="jumpToPattern('all')">
      <span class="rb-nav-icon-badge">ALL</span>
      <div class="rb-nav-info">
        <div class="rb-nav-title-row">
          <span class="rb-nav-topic-title">All Patterns</span>
          <span class="rb-nav-fraction">${d}/${total}</span>
        </div>
        <div class="rb-nav-track"><div class="rb-nav-fill" style="width:${allPct}%;"></div></div>
      </div>
    </div>
  `;

  DATA.forEach(s => {
    const doneC = doneProbsForStep(s);
    const pct = Math.round((doneC / s.problems.length) * 100);
    const shortName = s.name.replace(/^Pattern\s*\d*:?\s*/, '').replace(/^Pattern:\s*/, '');
    const isActive = String(currentActiveStep) === String(s.id);
    const iconCode = DSA_PATTERN_ICONS[s.id] || `P${s.id}`;

    h += `
      <div class="rb-topic-nav-item ${isActive ? 'active' : ''}" id="dsa-nav-${s.id}" onclick="jumpToPattern(${s.id})">
        <span class="rb-nav-icon-badge">${iconCode}</span>
        <div class="rb-nav-info">
          <div class="rb-nav-title-row">
            <span class="rb-nav-topic-title" title="${s.name}">${shortName}</span>
            <span class="rb-nav-fraction">${doneC}/${s.problems.length}</span>
          </div>
          <div class="rb-nav-track"><div class="rb-nav-fill" style="width:${pct}%;"></div></div>
        </div>
      </div>
    `;
  });

  sb.innerHTML = h;
}

function updatePatternDropdown() {
  const dropdown = document.getElementById('patternSelectDropdown');
  if (!dropdown) return;

  let h = `<option value="all"${currentActiveStep === 'all' ? ' selected' : ''}>All 19 Patterns (184 questions)</option>`;
  DATA.forEach(s => {
    const doneC = doneProbsForStep(s);
    const shortName = s.name.replace(/^Pattern\s*\d*:?\s*/, '').replace(/^Pattern:\s*/, '');
    const isSel = String(currentActiveStep) === String(s.id);
    h += `<option value="${s.id}"${isSel ? ' selected' : ''}>P${s.id}: ${shortName} (${doneC}/${s.problems.length})</option>`;
  });
  dropdown.innerHTML = h;
}

function jumpToPattern(id) {
  currentActiveStep = id;
  if (id !== 'all') {
    delete state.collapsedSteps[id];
    saveState();
  }
  const dd = document.getElementById('patternSelectDropdown');
  if (dd) dd.value = id;

  renderDsaContent();
  if (id !== 'all') {
    const el = document.getElementById('step-' + id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function setDsaFilter(f, btn) {
  currentDsaFilter = f;
  document.querySelectorAll('#view-dsa .filter-pills .fpill, #view-dsa .rb-pill').forEach(b => {
    b.classList.remove('active', 'active-done', 'active-overdue');
  });
  if (btn) btn.classList.add('active');
  renderDsaContent();
}

function toggleProblemDone(n, checked) {
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
}

function toggleProblemStar(n) {
  const ps = getProblemState(n);
  ps.starred = !ps.starred;
  saveState();
  updateDsaStats();
  renderDsaContent();
}

function togglePatternCollapse(id) {
  state.collapsedSteps[id] = !state.collapsedSteps[id];
  saveState();
  renderDsaContent();
}

function expandAllPatterns(expand) {
  DATA.forEach(s => {
    if (expand) delete state.collapsedSteps[s.id];
    else state.collapsedSteps[s.id] = true;
  });
  saveState();
  renderDsaContent();
}

function renderDsaContent() {
  const q = (document.getElementById('search')?.value || '').toLowerCase().trim();
  const content = document.getElementById('dsaContent');
  if (!content) return;

  let html = '';
  let totalVisible = 0;

  DATA.forEach(step => {
    if (currentActiveStep !== 'all' && String(step.id) !== String(currentActiveStep)) return;

    const visibleProblems = step.problems.filter(p => {
      const ps = getProblemState(p.n);
      const matchesSearch = !q || p.t.toLowerCase().includes(q) || ('#' + p.n).includes(q) || String(p.n) === q || step.name.toLowerCase().includes(q);

      let matchesFilter = true;
      if (currentDsaFilter === 'easy') matchesFilter = (p.diff === 'e');
      else if (currentDsaFilter === 'med') matchesFilter = (p.diff === 'm');
      else if (currentDsaFilter === 'hard') matchesFilter = (p.diff === 'h');
      else if (currentDsaFilter === 'pending') matchesFilter = !ps.done;
      else if (currentDsaFilter === 'done') matchesFilter = !!ps.done;
      else if (currentDsaFilter === 'starred') matchesFilter = !!ps.starred;
      else if (currentDsaFilter === 'due') matchesFilter = isProblemDue(ps);
      else if (currentDsaFilter === 'overdue') matchesFilter = isProblemOverdue(ps);
      else if (currentDsaFilter === 'never') matchesFilter = ps.done && (ps.revisionCount || 0) === 0;
      else if (currentDsaFilter === 'mastered') matchesFilter = (ps.revisionCount || 0) >= 3 || ps.status === 'MASTERED';

      return matchesSearch && matchesFilter;
    });

    if (visibleProblems.length === 0) return;
    totalVisible += visibleProblems.length;

    const doneC = doneProbsForStep(step);
    const pct = Math.round((doneC / step.problems.length) * 100);
    const isCollapsed = !!state.collapsedSteps[step.id];

    html += `
      <div class="rb-pattern-card" id="step-${step.id}">
        <div class="rb-pattern-header" onclick="togglePatternCollapse(${step.id})">
          <div class="rb-pattern-header-left">
            <span class="rb-pat-badge">P${step.id}</span>
            <h3 class="rb-pattern-title">${step.name}</h3>
          </div>
          <div class="rb-pattern-header-right">
            <span class="rb-pattern-ratio">${doneC}/${step.problems.length} solved</span>
            <div class="rb-pat-mini-track">
              <div class="rb-pat-mini-fill" style="width:${pct}%;"></div>
            </div>
            <span class="rb-pat-pct-badge">${pct}%</span>
            <svg class="rb-accordion-chevron ${isCollapsed ? 'collapsed' : ''}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
          </div>
        </div>

        ${!isCollapsed ? `
          <div class="rb-pattern-body">
            <div class="rb-problems-table">
              ${visibleProblems.map(p => {
                const ps = getProblemState(p.n);
                const isDone = !!ps.done;
                const isStarred = !!ps.starred;
                const diffClass = p.diff === 'e' ? 'diff-easy' : p.diff === 'm' ? 'diff-med' : 'diff-hard';
                const diffLabel = p.diff === 'e' ? 'Easy' : p.diff === 'm' ? 'Medium' : 'Hard';

                let linksHtml = '';
                if (p.l) {
                  linksHtml += `
                    <a class="rb-platform-link lc" href="${p.l}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Open on LeetCode: ${p.l}">
                      <span>LC</span>
                      <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
                }
                if (p.g) {
                  linksHtml += `
                    <a class="rb-platform-link gfg" href="${p.g}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Open on GeeksforGeeks: ${p.g}">
                      <span>GFG</span>
                      <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
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
                  <div class="rb-prob-row ${isDone ? 'is-done' : ''}" id="prob-${p.n}">
                    <div class="rb-col-check">
                      <label class="rb-custom-checkbox" title="Mark problem solved">
                        <input type="checkbox" ${isDone ? 'checked' : ''} onchange="toggleProblemDone(${p.n}, this.checked)">
                        <span class="rb-checkmark"></span>
                      </label>
                      <button type="button" class="rb-star-btn ${isStarred ? 'starred' : ''}" onclick="toggleProblemStar(${p.n})" title="${isStarred ? 'Unstar problem' : 'Star problem'}">${isStarred ? '★' : '☆'}</button>
                      <span class="rb-prob-index">#${p.n}</span>
                    </div>

                    <div class="rb-col-main">
                      <div class="rb-prob-title-line">
                        <span class="rb-ref-pill">P${step.id}</span>
                        <span class="rb-prob-name" title="${p.t}">${p.t}</span>
                        <span class="rb-diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>
                        ${dueTag}
                      </div>

                      <div class="rb-prob-sub-line">
                        <div class="rb-links-container">${linksHtml}</div>
                        <div class="rb-quick-chips">
                          <span class="rb-quick-chip" title="Revisions completed">🔁 ${ps.revisionCount || 0} revs</span>
                          ${isDone && ps.firstSolvedDate ? `<span class="rb-quick-chip mastered" title="First solved on ${formatDateDisplay(ps.firstSolvedDate)}">✓ ${formatDateDisplay(ps.firstSolvedDate)}</span>` : ''}
                          ${ps.lastRevisedDate ? `<span class="rb-quick-chip needsrev" title="Last revised on ${formatDateDisplay(ps.lastRevisedDate)}">Last: ${formatDateDisplay(ps.lastRevisedDate)}</span>` : ''}
                        </div>
                      </div>
                    </div>

                    <div class="rb-col-actions">
                      <button class="rb-rev-btn" onclick="openRevisionModal(${p.n})" title="Log revision or inspect notes">
                        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
                        <span>+1 Rev</span>
                        ${ps.revisionCount > 0 ? `<span class="rb-rev-badge">${ps.revisionCount}</span>` : ''}
                      </button>
                      <button class="rb-action-btn" onclick="openRevisionModal(${p.n})" title="Notes & History" style="padding:4px 8px; font-size:12px;">📝</button>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  });

  if (totalVisible === 0) {
    html = `
      <div class="rb-empty-state">
        <div class="rb-empty-icon">🔍</div>
        <div class="rb-empty-title">No Matching DSA Patterns Found</div>
        <div class="rb-empty-subtitle">We couldn't find any questions matching your current search query or filter combination.</div>
        <button class="rb-empty-reset-btn" onclick="resetAllDsaFilters()">Clear All Filters & Show 184 Problems</button>
      </div>
    `;
  }

  content.innerHTML = html;
  buildPatternNavSidebar();
  updatePatternDropdown();
}
"""

def generate_upgraded_striver_js():
    return """
/* ==========================================================================
   STRIVER A2Z UPGRADED INTERACTIVE CONTROLLER (Emerald Theme)
   ========================================================================== */

function handleStriverSearchInput(val) {
  const clearBtn = document.getElementById('striverSearchClearBtn');
  if (clearBtn) clearBtn.style.display = val && val.trim().length > 0 ? 'flex' : 'none';
  renderStriverContent();
}

function clearStriverSearch() {
  const input = document.getElementById('striverSearch');
  if (input) {
    input.value = '';
    input.focus();
  }
  const clearBtn = document.getElementById('striverSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';
  renderStriverContent();
}

function resetAllStriverFilters() {
  const input = document.getElementById('striverSearch');
  if (input) input.value = '';
  const clearBtn = document.getElementById('striverSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';

  const co = document.getElementById('striverCoFilter');
  if (co) co.value = 'all';
  currentStriverCompany = 'all';

  currentStriverFilter = 'all';
  jumpToStriverStep('all');
  const allBtn = document.getElementById('f-striver-all');
  if (allBtn) setStriverFilter('all', allBtn);
  renderStriverContent();
}

function jumpToNextUnsolvedStriverProblem() {
  let nextUnsolved = null;
  for (const step of STRIVER_DATA) {
    if (currentActiveStriverStep !== 'all' && String(step.id) !== String(currentActiveStriverStep)) continue;
    for (const p of step.problems) {
      const ps = getStriverProblemState(p.n);
      if (!ps.done) {
        nextUnsolved = { step, prob: p };
        break;
      }
    }
    if (nextUnsolved) break;
  }

  if (!nextUnsolved && currentActiveStriverStep !== 'all') {
    for (const step of STRIVER_DATA) {
      for (const p of step.problems) {
        const ps = getStriverProblemState(p.n);
        if (!ps.done) {
          nextUnsolved = { step, prob: p };
          break;
        }
      }
      if (nextUnsolved) break;
    }
  }

  if (nextUnsolved) {
    delete striverState.collapsedSteps[nextUnsolved.step.id];
    saveStriverState();
    renderStriverContent();

    setTimeout(() => {
      const el = document.getElementById('striver-prob-' + nextUnsolved.prob.n);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.boxShadow = '0 0 0 3px #10b981, 0 0 20px rgba(16, 185, 129, 0.4)';
        setTimeout(() => el.style.boxShadow = '', 2500);
      }
    }, 150);
    showToast(`Jumped to Next Unsolved: Striver #${nextUnsolved.prob.n} (${nextUnsolved.prob.t})`);
  } else {
    showToast('🎉 Incredible! All 455 Striver A2Z problems are marked solved!');
  }
}

function updateStriverStats() {
  const total = totalStriverProbs();
  const allStates = Object.values(striverState.problems);
  const done = allStates.filter(p => p.done).length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  let easyTotal = 0, easyDone = 0;
  let medTotal = 0, medDone = 0;
  let hardTotal = 0, hardDone = 0;
  let starredCount = 0, masteredCount = 0, needsRevCount = 0;

  STRIVER_DATA.forEach(s => {
    s.problems.forEach(p => {
      const ps = getStriverProblemState(p.n);
      if (p.diff === 'e') {
        easyTotal++;
        if (ps.done) easyDone++;
      } else if (p.diff === 'm') {
        medTotal++;
        if (ps.done) medDone++;
      } else if (p.diff === 'h') {
        hardTotal++;
        if (ps.done) hardDone++;
      }
      if (ps.starred) starredCount++;
      if (ps.revisionCount >= 3) masteredCount++;
      if (isProblemDue(ps) || isProblemOverdue(ps)) needsRevCount++;
    });
  });

  const easyPct = easyTotal > 0 ? Math.round((easyDone / easyTotal) * 100) : 0;
  const medPct = medTotal > 0 ? Math.round((medDone / medTotal) * 100) : 0;
  const hardPct = hardTotal > 0 ? Math.round((hardDone / hardTotal) * 100) : 0;

  const badge = document.getElementById('nav-striver-badge');
  if (badge) badge.textContent = `${done}/${total}`;

  const radialPct = document.getElementById('striver-radial-pct');
  if (radialPct) radialPct.textContent = `${pct}%`;

  const gaugeCircle = document.getElementById('striver-gauge-circle');
  if (gaugeCircle) {
    const circumference = 2 * Math.PI * 42;
    const offset = circumference - (pct / 100) * circumference;
    gaugeCircle.style.strokeDashoffset = offset;
  }

  const headerSolved = document.getElementById('striver-header-solved-count');
  if (headerSolved) headerSolved.innerHTML = `${done} <span class="rb-metric-denom">/ ${total}</span>`;

  const chipStar = document.getElementById('striver-stat-chip-starred');
  if (chipStar) chipStar.textContent = `★ ${starredCount}`;

  const chipMaster = document.getElementById('striver-stat-chip-mastered');
  if (chipMaster) chipMaster.textContent = `👑 ${masteredCount}`;

  const chipRev = document.getElementById('striver-stat-chip-needsrev');
  if (chipRev) chipRev.textContent = `🟣 ${needsRevCount}`;

  const eRatio = document.getElementById('striver-easy-ratio');
  if (eRatio) eRatio.textContent = `${easyDone} / ${easyTotal} (${easyPct}%)`;
  const eFill = document.getElementById('striver-easy-fill');
  if (eFill) eFill.style.width = `${easyPct}%`;

  const mRatio = document.getElementById('striver-med-ratio');
  if (mRatio) mRatio.textContent = `${medDone} / ${medTotal} (${medPct}%)`;
  const mFill = document.getElementById('striver-med-fill');
  if (mFill) mFill.style.width = `${medPct}%`;

  const hRatio = document.getElementById('striver-hard-ratio');
  if (hRatio) hRatio.textContent = `${hardDone} / ${hardTotal} (${hardPct}%)`;
  const hFill = document.getElementById('striver-hard-fill');
  if (hFill) hFill.style.width = `${hardPct}%`;
}

function buildStriverSidebar() {
  const sb = document.getElementById('striverStepNavSidebar');
  if (!sb) return;

  const total = totalStriverProbs();
  const d = Object.values(striverState.problems).filter(p => p.done).length;
  const allPct = total > 0 ? Math.round((d / total) * 100) : 0;
  const isAllActive = currentActiveStriverStep === 'all';

  let h = '<div class="rb-sidebar-heading">18 Steps · 455 Problems</div>';
  h += `
    <div class="rb-topic-nav-item ${isAllActive ? 'active' : ''}" onclick="jumpToStriverStep('all')">
      <span class="rb-nav-icon-badge">ALL</span>
      <div class="rb-nav-info">
        <div class="rb-nav-title-row">
          <span class="rb-nav-topic-title">All Steps</span>
          <span class="rb-nav-fraction">${d}/${total}</span>
        </div>
        <div class="rb-nav-track"><div class="rb-nav-fill" style="width:${allPct}%;"></div></div>
      </div>
    </div>
  `;

  STRIVER_DATA.forEach(s => {
    const doneC = doneStriverProbsForStep(s);
    const pct = Math.round((doneC / s.problems.length) * 100);
    const shortName = s.name.replace(/^Step\s*\d*:?\s*/, '');
    const isActive = String(currentActiveStriverStep) === String(s.id);
    const iconCode = `S${s.id}`;

    h += `
      <div class="rb-topic-nav-item ${isActive ? 'active' : ''}" id="striver-nav-${s.id}" onclick="jumpToStriverStep(${s.id})">
        <span class="rb-nav-icon-badge">${iconCode}</span>
        <div class="rb-nav-info">
          <div class="rb-nav-title-row">
            <span class="rb-nav-topic-title" title="${s.name}">${shortName}</span>
            <span class="rb-nav-fraction">${doneC}/${s.problems.length}</span>
          </div>
          <div class="rb-nav-track"><div class="rb-nav-fill" style="width:${pct}%;"></div></div>
        </div>
      </div>
    `;
  });

  sb.innerHTML = h;
}

function updateStriverStepDropdown() {
  const dropdown = document.getElementById('striverStepSelectDropdown');
  if (!dropdown) return;

  let h = `<option value="all"${currentActiveStriverStep === 'all' ? ' selected' : ''}>All 18 Striver Steps (455 questions)</option>`;
  STRIVER_DATA.forEach(s => {
    const doneC = doneStriverProbsForStep(s);
    const shortName = s.name.replace(/^Step\s*\d*:?\s*/, '');
    const isSel = String(currentActiveStriverStep) === String(s.id);
    h += `<option value="${s.id}"${isSel ? ' selected' : ''}>S${s.id}: ${shortName} (${doneC}/${s.problems.length})</option>`;
  });
  dropdown.innerHTML = h;
}

function jumpToStriverStep(id) {
  currentActiveStriverStep = id;
  if (id !== 'all') {
    delete striverState.collapsedSteps[id];
    saveStriverState();
  }
  const dd = document.getElementById('striverStepSelectDropdown');
  if (dd) dd.value = id;

  renderStriverContent();
  if (id !== 'all') {
    const el = document.getElementById('striver-step-' + id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
}

function setStriverFilter(f, btn) {
  currentStriverFilter = f;
  document.querySelectorAll('#view-striver .filter-pills .fpill, #view-striver .rb-pill').forEach(b => {
    b.classList.remove('active', 'active-done', 'active-overdue');
  });
  if (btn) btn.classList.add('active');
  renderStriverContent();
}

function setStriverCompany(co) {
  currentStriverCompany = co;
  renderStriverContent();
}

function toggleStriverProblemDone(n, checked) {
  const ps = getStriverProblemState(n);
  ps.done = checked;
  const today = getTodayKey();
  if (checked) {
    if (!ps.firstSolvedDate) ps.firstSolvedDate = today;
    ps.completedOn = today;
  }
  saveStriverState();
  updateStriverStats();
  renderStriverContent();
  updateHeaderStats();
}

function toggleStriverProblemStar(n) {
  const ps = getStriverProblemState(n);
  ps.starred = !ps.starred;
  saveStriverState();
  updateStriverStats();
  renderStriverContent();
}

function toggleStriverStepCollapse(id) {
  striverState.collapsedSteps[id] = !striverState.collapsedSteps[id];
  saveStriverState();
  renderStriverContent();
}

function expandAllStriverSteps(expand) {
  STRIVER_DATA.forEach(s => {
    if (expand) delete striverState.collapsedSteps[s.id];
    else striverState.collapsedSteps[s.id] = true;
  });
  saveStriverState();
  renderStriverContent();
}

function renderStriverContent() {
  const q = (document.getElementById('striverSearch')?.value || '').toLowerCase().trim();
  const content = document.getElementById('striverContent');
  if (!content) return;

  let html = '';
  let totalVisible = 0;

  STRIVER_DATA.forEach(step => {
    if (currentActiveStriverStep !== 'all' && String(step.id) !== String(currentActiveStriverStep)) return;

    const visibleProblems = step.problems.filter(p => {
      const ps = getStriverProblemState(p.n);
      const matchesSearch = !q || p.t.toLowerCase().includes(q) || ('#' + p.n).includes(q) || String(p.n) === q || step.name.toLowerCase().includes(q);

      let matchesFilter = true;
      if (currentStriverFilter === 'easy') matchesFilter = (p.diff === 'e');
      else if (currentStriverFilter === 'med') matchesFilter = (p.diff === 'm');
      else if (currentStriverFilter === 'hard') matchesFilter = (p.diff === 'h');
      else if (currentStriverFilter === 'pending') matchesFilter = !ps.done;
      else if (currentStriverFilter === 'done') matchesFilter = !!ps.done;
      else if (currentStriverFilter === 'starred') matchesFilter = !!ps.starred;
      else if (currentStriverFilter === 'due') matchesFilter = isProblemDue(ps);
      else if (currentStriverFilter === 'overdue') matchesFilter = isProblemOverdue(ps);
      else if (currentStriverFilter === 'never') matchesFilter = ps.done && (ps.revisionCount || 0) === 0;
      else if (currentStriverFilter === 'mastered') matchesFilter = (ps.revisionCount || 0) >= 3 || ps.status === 'MASTERED';

      let matchesCompany = true;
      if (currentStriverCompany !== 'all') {
        matchesCompany = Array.isArray(p.c) && p.c.includes(currentStriverCompany);
      }

      return matchesSearch && matchesFilter && matchesCompany;
    });

    if (visibleProblems.length === 0) return;
    totalVisible += visibleProblems.length;

    const doneC = doneStriverProbsForStep(step);
    const pct = Math.round((doneC / step.problems.length) * 100);
    const isCollapsed = !!striverState.collapsedSteps[step.id];

    html += `
      <div class="rb-pattern-card" id="striver-step-${step.id}">
        <div class="rb-pattern-header" onclick="toggleStriverStepCollapse(${step.id})">
          <div class="rb-pattern-header-left">
            <span class="rb-pat-badge">S${step.id}</span>
            <h3 class="rb-pattern-title">${step.name}</h3>
          </div>
          <div class="rb-pattern-header-right">
            <span class="rb-pattern-ratio">${doneC}/${step.problems.length} solved</span>
            <div class="rb-pat-mini-track">
              <div class="rb-pat-mini-fill" style="width:${pct}%;"></div>
            </div>
            <span class="rb-pat-pct-badge">${pct}%</span>
            <svg class="rb-accordion-chevron ${isCollapsed ? 'collapsed' : ''}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
          </div>
        </div>

        ${!isCollapsed ? `
          <div class="rb-pattern-body">
            <div class="rb-problems-table">
              ${visibleProblems.map(p => {
                const ps = getStriverProblemState(p.n);
                const isDone = !!ps.done;
                const isStarred = !!ps.starred;
                const diffClass = p.diff === 'e' ? 'diff-easy' : p.diff === 'm' ? 'diff-med' : 'diff-hard';
                const diffLabel = p.diff === 'e' ? 'Easy' : p.diff === 'm' ? 'Medium' : 'Hard';

                let linksHtml = '';
                if (p.l) {
                  linksHtml += `
                    <a class="rb-platform-link lc" href="${p.l}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Open on LeetCode: ${p.l}">
                      <span>LC</span>
                      <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
                }
                if (p.g) {
                  linksHtml += `
                    <a class="rb-platform-link gfg" href="${p.g}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Open on GeeksforGeeks: ${p.g}">
                      <span>GFG</span>
                      <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
                }
                if (p.v) {
                  linksHtml += `
                    <a class="rb-platform-link yt" href="${p.v}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Watch video solution: ${p.v}">
                      <span>▶ Video</span>
                      <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
                }
                if (p.d) {
                  linksHtml += `
                    <a class="rb-platform-link" href="${p.d}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Read article/tutorial: ${p.d}" style="background:rgba(99,102,241,0.12); color:#818cf8; border:1px solid rgba(99,102,241,0.3);">
                      <span>📖 Docs</span>
                      <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                    </a>
                  `;
                }

                let coTagsHtml = '';
                if (Array.isArray(p.c) && p.c.length > 0) {
                  const topCos = p.c.slice(0, 3).map(c => COMPANY_NAMES[c] || c);
                  const moreCount = p.c.length > 3 ? ` +${p.c.length - 3}` : '';
                  const allCos = p.c.map(c => COMPANY_NAMES[c] || c).join(', ');
                  coTagsHtml = `<span class="rb-company-chip" title="Asked in: ${allCos}">🏢 ${topCos.join(', ')}${moreCount}</span>`;
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
                  <div class="rb-prob-row ${isDone ? 'is-done' : ''}" id="striver-prob-${p.n}">
                    <div class="rb-col-check">
                      <label class="rb-custom-checkbox" title="Mark problem solved">
                        <input type="checkbox" ${isDone ? 'checked' : ''} onchange="toggleStriverProblemDone(${p.n}, this.checked)">
                        <span class="rb-checkmark"></span>
                      </label>
                      <button type="button" class="rb-star-btn ${isStarred ? 'starred' : ''}" onclick="toggleStriverProblemStar(${p.n})" title="${isStarred ? 'Unstar problem' : 'Star problem'}">${isStarred ? '★' : '☆'}</button>
                      <span class="rb-prob-index">#${p.n}</span>
                    </div>

                    <div class="rb-col-main">
                      <div class="rb-prob-title-line">
                        <span class="rb-ref-pill">S${step.id}</span>
                        <span class="rb-prob-name" title="${p.t}">${p.t}</span>
                        <span class="rb-diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>
                        ${dueTag}
                      </div>

                      <div class="rb-prob-sub-line">
                        <div class="rb-links-container">${linksHtml}</div>
                        ${coTagsHtml ? `<div class="rb-companies-container">${coTagsHtml}</div>` : ''}
                        <div class="rb-quick-chips">
                          <span class="rb-quick-chip" title="Revisions completed">🔁 ${ps.revisionCount || 0} revs</span>
                          ${isDone && ps.firstSolvedDate ? `<span class="rb-quick-chip mastered" title="First solved on ${formatDateDisplay(ps.firstSolvedDate)}">✓ ${formatDateDisplay(ps.firstSolvedDate)}</span>` : ''}
                          ${ps.lastRevisedDate ? `<span class="rb-quick-chip needsrev" title="Last revised on ${formatDateDisplay(ps.lastRevisedDate)}">Last: ${formatDateDisplay(ps.lastRevisedDate)}</span>` : ''}
                        </div>
                      </div>
                    </div>

                    <div class="rb-col-actions">
                      <button class="rb-rev-btn" onclick="openRevisionModal(${p.n}, 'striver')" title="Log revision or inspect notes">
                        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
                        <span>+1 Rev</span>
                        ${ps.revisionCount > 0 ? `<span class="rb-rev-badge">${ps.revisionCount}</span>` : ''}
                      </button>
                      <button class="rb-action-btn" onclick="openRevisionModal(${p.n}, 'striver')" title="Notes & History" style="padding:4px 8px; font-size:12px;">📝</button>
                    </div>
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  });

  if (totalVisible === 0) {
    html = `
      <div class="rb-empty-state">
        <div class="rb-empty-icon">🔍</div>
        <div class="rb-empty-title">No Matching Striver Problems Found</div>
        <div class="rb-empty-subtitle">We couldn't find any questions matching your current search query or filter combination.</div>
        <button class="rb-empty-reset-btn" onclick="resetAllStriverFilters()">Clear All Filters & Show 455 Problems</button>
      </div>
    `;
  }

  content.innerHTML = html;
  buildStriverSidebar();
  updateStriverStepDropdown();
}
"""

def assemble_triple_redesign():
    with open('/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace #view-dsa markup
    dsa_start = html.find('<section class="view-section" id="view-dsa">')
    if dsa_start == -1:
        dsa_start = html.find('<!-- VIEW 2: DSA PATTERNS -->')
    dsa_end = html.find('<!-- VIEW 2.5: STRIVER SHEET -->', dsa_start)
    if dsa_start == -1 or dsa_end == -1:
        print("ERROR: Could not locate #view-dsa bounds!")
        return False

    new_dsa_markup = generate_dsa_markup() + "\n\n    "
    html = html[:dsa_start] + new_dsa_markup + html[dsa_end:]
    print("✓ Replaced #view-dsa HTML markup!")

    # 2. Replace #view-striver markup
    striver_start = html.find('<section class="view-section" id="view-striver">')
    if striver_start == -1:
        striver_start = html.find('<!-- VIEW 2.5: STRIVER SHEET -->')
    striver_end = html.find('<!-- VIEW 2.7: RISINGBRAIN PATTERN-WISE SHEET -->', striver_start)
    if striver_start == -1 or striver_end == -1:
        print("ERROR: Could not locate #view-striver bounds!")
        return False

    new_striver_markup = generate_striver_markup() + "\n\n    "
    html = html[:striver_start] + new_striver_markup + html[striver_end:]
    print("✓ Replaced #view-striver HTML markup!")

    # 3. Replace DSA interactive JS functions
    dsa_js_start = html.find('function renderDsaContent() {')
    dsa_js_end = html.find('/* ==========================================================================\n   PROBLEM REVISION & NOTES MODAL')
    if dsa_js_start == -1 or dsa_js_end == -1:
        print("ERROR: Could not locate DSA JS bounds!")
        return False

    new_dsa_js = generate_upgraded_dsa_js() + "\n\n"
    html = html[:dsa_js_start] + new_dsa_js + html[dsa_js_end:]
    print("✓ Replaced DSA interactive JS controller!")

    # 4. Replace Striver interactive JS functions
    str_js_start = html.find('function renderStriverContent() {')
    str_js_end = html.find('function openRevisionModal(probNum, trackerType = \'dsa\') {')

    if str_js_start == -1 or str_js_end == -1:
        print("ERROR: Could not locate Striver JS bounds!")
        return False

    new_str_js = generate_upgraded_striver_js() + "\n\n"
    html = html[:str_js_start] + new_str_js + html[str_js_end:]
    print("✓ Replaced Striver interactive JS controller!")

    # 5. Ensure switchView updates DSA and Striver stats
    old_switch = """  if(viewName === 'dashboard') updateDashboard();
  else if(viewName === 'dsa') renderDsaContent();
  else if(viewName === 'striver') renderStriverContent();
  else if(viewName === 'risingbrain') { renderRisingBrainContent(); updateRisingBrainStats(); }"""

    new_switch = """  if(viewName === 'dashboard') updateDashboard();
  else if(viewName === 'dsa') { renderDsaContent(); updateDsaStats(); }
  else if(viewName === 'striver') { renderStriverContent(); updateStriverStats(); }
  else if(viewName === 'risingbrain') { renderRisingBrainContent(); updateRisingBrainStats(); }"""

    if old_switch in html:
        html = html.replace(old_switch, new_switch, 1)
        print("✓ Updated switchView to refresh tracker stats on tab change!")
    else:
        # Check if switchView was formatted with single-line or multi-line
        switch_pattern = re.compile(r'if\s*\(\s*viewName\s*===\s*[\'"]dashboard[\'"]\s*\)\s*updateDashboard\(\);\s*else if\s*\(\s*viewName\s*===\s*[\'"]dsa[\'"]\s*\)[^;]+;\s*else if\s*\(\s*viewName\s*===\s*[\'"]striver[\'"]\s*\)[^;]+;\s*else if\s*\(\s*viewName\s*===\s*[\'"]risingbrain[\'"]\s*\)[^;]+;')
        if switch_pattern.search(html):
            html = switch_pattern.sub(new_switch, html, 1)
            print("✓ Updated switchView via regex to refresh tracker stats on tab change!")

    # 6. Ensure init() calls updateDsaStats and updateStriverStats
    old_init_calls = """  updateHeaderStats();
  updateDashboard();
  populateRisingBrainNav();
  renderDsaContent();
  renderStriverContent();
  renderRisingBrainContent();
  updateRisingBrainStats();"""

    new_init_calls = """  updateHeaderStats();
  updateDashboard();
  populateRisingBrainNav();
  renderDsaContent();
  updateDsaStats();
  renderStriverContent();
  updateStriverStats();
  renderRisingBrainContent();
  updateRisingBrainStats();"""

    if old_init_calls in html:
        html = html.replace(old_init_calls, new_init_calls, 1)
        print("✓ Updated init() to initialize stats for all 3 trackers!")

    out_file = "/Users/devrajput/.gemini/antigravity-ide/scratch/test_triple_assembled.html"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"\n🎉 Successfully assembled test file: {out_file} ({len(html)} bytes)")
    return True

if __name__ == '__main__':
    assemble_triple_redesign()
