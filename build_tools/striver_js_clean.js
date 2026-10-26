/* ==========================================================================
   STRIVER SHEET STATE & NAMESPACED PERSISTENCE
   ========================================================================== */
const STORAGE_STRIVER_KEY = 'striver_a2z_tracker_v3';

let striverState = { version: 1, problems: {}, maxStreak: 0, collapsedSteps: {} };
let currentStriverFilter = 'all';
let currentActiveStriverStep = 'all';
let currentStriverCompany = 'all';
let activeModalTracker = 'dsa'; // 'dsa' or 'striver'

const COMPANY_NAMES = {
  amz: 'Amazon',
  ggl: 'Google',
  msft: 'Microsoft',
  meta: 'Meta',
  fk: 'Flipkart',
  adobe: 'Adobe',
  sam: 'Samsung',
  tcs: 'TCS',
  wipro: 'Wipro',
  infy: 'Infosys',
  cog: 'Cognizant',
  cap: 'Capgemini',
  hcl: 'HCL',
  acc: 'Accenture',
  techm: 'Tech Mahindra'
};

function emptyStriverProblemState() {
  return {
    done: false,
    firstSolvedDate: null,
    completedOn: null,
    starred: false,
    revisions: [],
    revisionCount: 0,
    lastRevisedDate: null,
    nextDueDate: null,
    spacedIntervalLevel: 0,
    notes: {
      approach: '',
      mistakes: '',
      complexity: ''
    }
  };
}

function saveStriverState() {
  try {
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
  } catch (e) {
    console.error('Storage error in saveStriverState:', e);
  }
}

function loadStriverState() {
  try {
    const raw = localStorage.getItem(STORAGE_STRIVER_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && parsed.problems) {
        striverState = {
          version: 1,
          problems: parsed.problems || {},
          maxStreak: parsed.maxStreak || 0,
          collapsedSteps: parsed.collapsedSteps || {}
        };
        STRIVER_DATA.forEach(step => {
          step.problems.forEach(p => {
            if (!striverState.problems[p.n]) {
              striverState.problems[p.n] = emptyStriverProblemState();
            } else {
              const ps = striverState.problems[p.n];
              if (!Array.isArray(ps.revisions)) ps.revisions = [];
              ps.revisionCount = ps.revisions.length;
              if (!ps.notes) ps.notes = { approach: '', mistakes: '', complexity: '' };
            }
          });
        });
        return;
      }
    }

    const rawDone = localStorage.getItem('a2z_v2');
    if (rawDone) {
      const oldDone = JSON.parse(rawDone) || {};
      const oldStarred = JSON.parse(localStorage.getItem('a2z_starred') || '{}');
      const oldNotes = JSON.parse(localStorage.getItem('a2z_notes') || '{}');
      const oldDates = JSON.parse(localStorage.getItem('a2z_dates') || '{}');
      const oldStreak = parseInt(localStorage.getItem('a2z_maxstreak') || '0', 10);

      striverState = {
        version: 1,
        problems: {},
        maxStreak: oldStreak || 0,
        collapsedSteps: {}
      };

      STRIVER_DATA.forEach(step => {
        step.problems.forEach(p => {
          const isDone = !!oldDone[p.n];
          const cd = oldDates[p.n] || {};
          const noteText = oldNotes[p.n] || '';
          striverState.problems[p.n] = {
            done: isDone,
            firstSolvedDate: cd.firstSolvedDate || (isDone ? getTodayKey() : null),
            completedOn: cd.completedOn || (isDone ? getTodayKey() : null),
            starred: !!oldStarred[p.n],
            revisions: [],
            revisionCount: 0,
            lastRevisedDate: null,
            nextDueDate: null,
            spacedIntervalLevel: 0,
            notes: { approach: noteText, mistakes: '', complexity: '' }
          };
        });
      });
      saveStriverState();
      return;
    }

    striverState = { version: 1, problems: {}, maxStreak: 0, collapsedSteps: {} };
    STRIVER_DATA.forEach(step => {
      step.problems.forEach(p => {
        striverState.problems[p.n] = emptyStriverProblemState();
      });
    });
  } catch (e) {
    console.error('Error in loadStriverState:', e);
  }
}

function getStriverProblemState(n) {
  if (!striverState.problems[n]) striverState.problems[n] = emptyStriverProblemState();
  return striverState.problems[n];
}

function totalStriverProbs() {
  let cnt = 0;
  STRIVER_DATA.forEach(s => cnt += s.problems.length);
  return cnt;
}

function doneStriverProbsForStep(step) {
  return step.problems.filter(p => getStriverProblemState(p.n).done).length;
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
      const matchesSearch = !q || p.t.toLowerCase().includes(q) || String(p.n).includes(q) || step.name.toLowerCase().includes(q);

      let matchesFilter = true;
      if (currentStriverFilter === 'pending') matchesFilter = !ps.done;
      else if (currentStriverFilter === 'done') matchesFilter = ps.done;
      else if (currentStriverFilter === 'starred') matchesFilter = ps.starred;
      else if (currentStriverFilter === 'due') matchesFilter = isProblemDue(ps);
      else if (currentStriverFilter === 'overdue') matchesFilter = isProblemOverdue(ps);
      else if (currentStriverFilter === 'never') matchesFilter = ps.done && ps.revisionCount === 0;
      else if (currentStriverFilter === 'mastered') matchesFilter = ps.revisionCount >= 3;

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
    const shortStepName = step.name.replace(/^Step\s*\d*:?\s*/, '');

    html += `
      <div class="step-section${isCollapsed ? ' collapsed' : ''}" id="striver-step-${step.id}">
        <div class="step-header" onclick="toggleStriverStepCollapse(${step.id})">
          <span class="step-badge" style="color:var(--accent4); background:var(--accent4-bg);">S${step.id}</span>
          <span class="step-title">${step.name}</span>
          <span class="step-progress-text">${doneC}/${step.problems.length}</span>
          <div class="step-mini-bar"><div class="step-mini-fill" style="width:${pct}%; background:var(--accent4);"></div></div>
          <svg class="step-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m6 9 6 6 6-6"/></svg>
        </div>
        <div class="problems-list">
    `;

    visibleProblems.forEach(p => {
      const ps = getStriverProblemState(p.n);
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
      if (p.d) {
        linksHtml += `
          <a class="platform-badge doc-badge" href="${p.d}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Read article/tutorial: ${p.d}">
            <span class="platform-brand">📖</span>
            <span>Docs</span>
            <svg class="ext-icon" viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          </a>
        `;
      }

      let coTagsHtml = '';
      if (Array.isArray(p.c) && p.c.length > 0) {
        const topCos = p.c.slice(0, 3).map(c => COMPANY_NAMES[c] || c);
        const moreCount = p.c.length > 3 ? ` +${p.c.length - 3}` : '';
        const allCos = p.c.map(c => COMPANY_NAMES[c] || c).join(', ');
        coTagsHtml = `<span class="company-tag" title="Asked in: ${allCos}">🏢 ${topCos.join(', ')}${moreCount}</span>`;
      }

      let dueTag = '';
      if (isProblemOverdue(ps)) {
        dueTag = `<span class="due-badge overdue">⚠️ Overdue</span>`;
      } else if (isProblemDue(ps)) {
        dueTag = `<span class="due-badge today">⏰ Due Today</span>`;
      } else if (ps.nextDueDate) {
        dueTag = `<span class="due-badge future">Due: ${formatDateDisplay(ps.nextDueDate)}</span>`;
      }

      html += `
        <div class="prob-item${isDone ? ' done' : ''}" id="striver-prob-${p.n}">
          <div class="prob-left-col">
            <input type="checkbox" class="prob-cb" ${isDone ? 'checked' : ''} onchange="toggleStriverProblemDone(${p.n}, this.checked)" title="Mark Striver Problem #${p.n} as ${isDone ? 'Pending' : 'Solved'}">
            <button type="button" class="star-btn${isStarred ? ' starred' : ''}" onclick="toggleStriverProblemStar(${p.n})" title="${isStarred ? 'Unstar problem' : 'Star problem #${p.n}'}">${isStarred ? '★' : '☆'}</button>
            <span class="prob-num">#${p.n}</span>
          </div>

          <div class="prob-info">
            <div class="prob-title-row">
              <span class="prob-pattern-tag" style="color:var(--accent4); background:var(--accent4-bg);" title="Step ${step.id}: ${step.name}">S${step.id}: ${shortStepName}</span>
              <span class="prob-title">${p.t}</span>
              <span class="diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>
              ${coTagsHtml}
              <div class="prob-links-container">${linksHtml}</div>
            </div>

            <div class="prob-meta-row">
              <span class="rev-badge" title="Total spaced revisions completed">🔁 ${ps.revisionCount || 0} revs</span>
              ${dueTag}
              ${isDone && ps.firstSolvedDate ? `<span class="solved-tag" title="First solved on ${formatDateDisplay(ps.firstSolvedDate)}">✓ Solved ${formatDateDisplay(ps.firstSolvedDate)}</span>` : ''}
              ${ps.lastRevisedDate ? `<span class="revised-tag" title="Last revised on ${formatDateDisplay(ps.lastRevisedDate)}">Last rev: ${formatDateDisplay(ps.lastRevisedDate)}</span>` : ''}
            </div>
          </div>

          <div class="prob-actions">
            <button class="btn-rev" onclick="openRevisionModal(${p.n}, 'striver')" title="Log a revision for Striver Problem #${p.n}">+1 Rev</button>
            <button class="btn-icon" style="width:28px; height:28px; font-size:12px;" onclick="openRevisionModal(${p.n}, 'striver')" title="View history, approach, and notes for Striver Problem #${p.n}">📝</button>
          </div>
        </div>
      `;
    });

    html += `</div></div>`;
  });

  if (totalVisible === 0) {
    html = `<div style="text-align:center; padding:3rem; color:var(--text-dim); background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-lg);">
      <div style="font-size:24px; margin-bottom:0.5rem;">🔍</div>
      <p style="font-size:14px; font-weight:600;">No Striver problems match your current search or company filter.</p>
      <button class="btn btn-secondary btn-sm" style="margin-top:1rem;" onclick="resetStriverFilters()">Reset Search & Filters</button>
    </div>`;
  }

  content.innerHTML = html;
  buildStriverSidebar();
  updateStriverStepDropdown();
}

function resetStriverFilters() {
  const sInput = document.getElementById('striverSearch');
  if (sInput) sInput.value = '';
  const coSel = document.getElementById('striverCoFilter');
  if (coSel) coSel.value = 'all';
  currentStriverFilter = 'all';
  currentActiveStriverStep = 'all';
  currentStriverCompany = 'all';
  document.querySelectorAll('#view-striver .filter-pills .fpill').forEach(b => b.classList.remove('active', 'active-done', 'active-overdue'));
  const allBtn = document.getElementById('f-striver-all');
  if (allBtn) allBtn.classList.add('active');
  renderStriverContent();
}

function buildStriverSidebar() {
  const sb = document.getElementById('striverStepNavSidebar');
  if (!sb) return;

  let h = `<div style="font-family:var(--font-mono); font-size:11px; color:var(--text-dim); margin-bottom:0.5rem; text-transform:uppercase;">Striver Steps</div>`;
  h += `<button class="pattern-nav-item${currentActiveStriverStep === 'all' ? ' active' : ''}" onclick="jumpToStriverStep('all')"><span>All 18 Steps</span><span style="font-family:var(--font-mono);">${totalStriverProbs()}</span></button>`;

  STRIVER_DATA.forEach(s => {
    const doneC = doneStriverProbsForStep(s);
    const shortName = s.name.replace(/^Step\s*\d*:?\s*/, '');
    const isActive = String(currentActiveStriverStep) === String(s.id);
    h += `<button class="pattern-nav-item${isActive ? ' active' : ''}" onclick="jumpToStriverStep(${s.id})"><span>${shortName}</span><span style="font-family:var(--font-mono);">${doneC}/${s.problems.length}</span></button>`;
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
  document.querySelectorAll('#view-striver .filter-pills .fpill').forEach(b => b.classList.remove('active', 'active-done', 'active-overdue'));
  if (btn) {
    if (f === 'done') btn.classList.add('active-done');
    else if (f === 'overdue') btn.classList.add('active-overdue');
    else btn.classList.add('active');
  }
  renderStriverContent();
}

function setStriverCompany(val) {
  currentStriverCompany = val;
  renderStriverContent();
}

function toggleStriverStepCollapse(id) {
  const el = document.getElementById('striver-step-' + id);
  if (!el) return;
  el.classList.toggle('collapsed');
  if (el.classList.contains('collapsed')) {
    striverState.collapsedSteps[id] = true;
  } else {
    delete striverState.collapsedSteps[id];
  }
  saveStriverState();
}

function expandAllStriverSteps(expand) {
  STRIVER_DATA.forEach(s => {
    const el = document.getElementById('striver-step-' + s.id);
    if (expand) {
      delete striverState.collapsedSteps[s.id];
      if (el) el.classList.remove('collapsed');
    } else {
      striverState.collapsedSteps[s.id] = true;
      if (el) el.classList.add('collapsed');
    }
  });
  saveStriverState();
}

function toggleStriverProblemDone(n, checked) {
  const ps = getStriverProblemState(n);
  const today = getTodayKey();
  const isDone = typeof checked === 'boolean' ? checked : !ps.done;
  if (isDone) {
    ps.done = true;
    if (!ps.firstSolvedDate) ps.firstSolvedDate = today;
    ps.completedOn = today;
    if (!ps.nextDueDate) {
      const { nextDueDate } = calculateNextDueDate('independent', 0);
      ps.nextDueDate = nextDueDate;
    }
  } else {
    ps.done = false;
    ps.completedOn = null;
  }
  striverState.problems[n] = ps;
  saveStriverState();
  renderStriverContent();
  updateHeaderStats();
}

function toggleStriverProblemStar(n) {
  const ps = getStriverProblemState(n);
  ps.starred = !ps.starred;
  striverState.problems[n] = ps;
  saveStriverState();
  renderStriverContent();
}

function openRevisionModal(probNum, trackerType = 'dsa') {
  activeModalProbNum = probNum;
  activeModalTracker = trackerType;

  let ps, pObj = null, stepName = '';
  if (trackerType === 'striver') {
    ps = getStriverProblemState(probNum);
    STRIVER_DATA.forEach(s => {
      const found = s.problems.find(p => p.n === probNum);
      if (found) { pObj = found; stepName = s.name; }
    });
  } else {
    ps = getProblemState(probNum);
    DATA.forEach(s => {
      const found = s.problems.find(p => p.n === probNum);
      if (found) { pObj = found; stepName = s.name; }
    });
  }

  const titleEl = document.getElementById('revModalProbTitle');
  const numEl = document.getElementById('revModalProbNum');
  const countEl = document.getElementById('revModalCount');
  const undoBtn = document.getElementById('btnUndoRevision');

  const trackerTag = trackerType === 'striver' ? '[Striver A2Z]' : '[DSA Patterns]';
  if (titleEl) titleEl.textContent = pObj ? `${trackerTag} ${pObj.t}` : `Problem #${probNum}`;
  if (numEl) numEl.textContent = `${stepName} · Problem #${probNum} · ${pObj && pObj.diff === 'e' ? 'Easy' : pObj && pObj.diff === 'm' ? 'Medium' : 'Hard'}`;
  if (countEl) countEl.textContent = ps.revisionCount || 0;
  if (undoBtn) undoBtn.style.display = (ps.revisions && ps.revisions.length > 0) ? 'inline-flex' : 'none';

  const appEl = document.getElementById('probNoteApproach');
  const mistEl = document.getElementById('probNoteMistakes');
  if (appEl) appEl.value = (ps.notes && ps.notes.approach) || '';
  if (mistEl) mistEl.value = (ps.notes && ps.notes.mistakes) || '';

  renderRevisionTimeline(ps);
  openModal('modalRevision');
}

function renderRevisionTimeline(ps) {
  const container = document.getElementById('revTimelineContainer');
  if(!container) return;

  if(!ps.revisions || ps.revisions.length === 0) {
    container.innerHTML = `<div style="font-size:12.5px; color:var(--text-dim); padding:0.5rem 0;">No revisions recorded yet. Add your first revision session above.</div>`;
    return;
  }

  let html = '';
  ps.revisions.slice().reverse().forEach((r, idx) => {
    const outcomeLabel = {
      independent: '🟢 Solved Independently',
      hint: '🟡 Needed Hint',
      solution: '🟠 Viewed Solution',
      unsolved: '🔴 Could Not Solve'
    }[r.outcome] || r.outcome;

    html += `
      <div class="timeline-entry">
        <div class="entry-header">
          <span style="font-size:12px; font-weight:700;">${outcomeLabel}</span>
          <span style="font-size:11px; font-family:var(--font-mono); color:var(--text-dim);">${formatDateDisplay(r.date)} ${r.timeStr || ''} (${r.timeTakenMinutes || 15}m)</span>
        </div>
        ${r.notes ? `<div style="font-size:12px; color:var(--text-muted); margin-top:2px;"><b>Notes:</b> ${r.notes}</div>` : ''}
        ${r.complexity ? `<div style="font-size:11.5px; font-family:var(--font-mono); color:var(--accent-light);">⚡ ${r.complexity}</div>` : ''}
      </div>
    `;
  });

  container.innerHTML = html;
}


function submitRevisionFromModal() {
  if (!activeModalProbNum) return;
  const outcome = document.getElementById('revOutcomeSelect').value;
  const timeTaken = document.getElementById('revTimeTaken').value;
  const complexity = document.getElementById('revComplexity').value.trim();
  const notes = document.getElementById('revNotesInput').value.trim();

  addRevisionEvent(activeModalProbNum, outcome, timeTaken, notes, complexity, activeModalTracker);
  openRevisionModal(activeModalProbNum, activeModalTracker);
}

function addRevisionEvent(probNum, outcome, timeTakenMinutes, notes, complexity, trackerType = 'dsa') {
  const isStriver = trackerType === 'striver';
  const ps = isStriver ? getStriverProblemState(probNum) : getProblemState(probNum);
  const today = getTodayKey();
  const now = new Date();

  const { nextDueDate, nextLevel } = calculateNextDueDate(outcome, ps.spacedIntervalLevel);

  const revEvent = {
    id: 'rev_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
    timestamp: Date.now(),
    date: today,
    timeStr: formatTime(now),
    outcome: outcome,
    timeTakenMinutes: Number(timeTakenMinutes) || 15,
    notes: notes || '',
    complexity: complexity || ''
  };

  if (!Array.isArray(ps.revisions)) ps.revisions = [];
  ps.revisions.push(revEvent);
  ps.revisionCount = ps.revisions.length;
  ps.lastRevisedDate = today;
  ps.nextDueDate = nextDueDate;
  ps.spacedIntervalLevel = nextLevel;

  if (!ps.done && (outcome === 'independent' || outcome === 'hint')) {
    ps.done = true;
    if (!ps.firstSolvedDate) ps.firstSolvedDate = today;
    ps.completedOn = today;
  }

  if (isStriver) {
    striverState.problems[probNum] = ps;
    saveStriverState();
    renderStriverContent();
  } else {
    state.problems[probNum] = ps;
    saveState();
    refreshAllUI();
  }

  logStudySession(Number(timeTakenMinutes) || 15, isStriver ? 'striver' : 'dsa', `Revision: ${isStriver ? 'Striver' : 'DSA'} #${probNum}`);
  showToast(`Logged revision for ${isStriver ? 'Striver' : 'DSA'} #${probNum} (${outcome}). Next due: ${formatDateDisplay(nextDueDate)}`);
  updateHeaderStats();
}

function undoLastRevision() {
  if (!activeModalProbNum) return;
  const isStriver = activeModalTracker === 'striver';
  const ps = isStriver ? getStriverProblemState(activeModalProbNum) : getProblemState(activeModalProbNum);
  if (!ps.revisions || ps.revisions.length === 0) return;

  const removed = ps.revisions.pop();
  ps.revisionCount = ps.revisions.length;

  if (ps.revisions.length > 0) {
    const last = ps.revisions[ps.revisions.length - 1];
    ps.lastRevisedDate = last.date;
    const { nextDueDate, nextLevel } = calculateNextDueDate(last.outcome, Math.max(0, ps.spacedIntervalLevel - 1));
    ps.nextDueDate = nextDueDate;
    ps.spacedIntervalLevel = nextLevel;
  } else {
    ps.lastRevisedDate = null;
    ps.nextDueDate = null;
    ps.spacedIntervalLevel = 0;
  }

  if (isStriver) {
    striverState.problems[activeModalProbNum] = ps;
    saveStriverState();
    renderStriverContent();
  } else {
    state.problems[activeModalProbNum] = ps;
    saveState();
    refreshAllUI();
  }

  showToast(`Reverted revision event from ${removed.date}`);
  openRevisionModal(activeModalProbNum, activeModalTracker);
  updateHeaderStats();
}

function saveProblemNotesDebounced() {
  clearTimeout(problemNotesAutosaveTimeout);
  problemNotesAutosaveTimeout = setTimeout(() => {
    if (!activeModalProbNum) return;
    const isStriver = activeModalTracker === 'striver';
    const ps = isStriver ? getStriverProblemState(activeModalProbNum) : getProblemState(activeModalProbNum);
    if (!ps.notes) ps.notes = { approach: '', mistakes: '', complexity: '' };
    ps.notes.approach = document.getElementById('probNoteApproach').value;
    ps.notes.mistakes = document.getElementById('probNoteMistakes').value;
    if (isStriver) {
      striverState.problems[activeModalProbNum] = ps;
      saveStriverState();
    } else {
      state.problems[activeModalProbNum] = ps;
      saveState();
    }
  }, 500);
}
