/**
 * JOB PREPARATION TRACKER — ENGINE & UI CONTROLLER
 * 
 * Provides interactive checklist, persistent state via 'job_prep_tracker_v1',
 * daily 5-hour study tracking, filtering, search, and notes modal.
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'job_prep_tracker_v1';

  // Global state container
  window.jobPrepState = null;

  // Initialize or load state
  function initJobPrepState() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        window.jobPrepState = JSON.parse(raw);
      }
    } catch (e) {
      console.error('Failed to load Job Prep Tracker state from storage:', e);
    }

    if (!window.jobPrepState || typeof window.jobPrepState !== 'object') {
      window.jobPrepState = {};
    }

    const s = window.jobPrepState;
    s.version = s.version || 1;
    s.activeTab = s.activeTab || 'overview';
    s.filter = s.filter || 'all';
    s.searchQuery = s.searchQuery || '';

    // Eligibility state
    if (!s.eligibility) {
      s.eligibility = {
        elig_cgpa: { status: 'eligible', tenth: '', twelfth: '', grad: '' },
        elig_batch: { status: 'needs_verification', batchYear: '2027', driveBatch: '2026/2027' },
        elig_backlogs: { status: 'eligible', activeBacklogs: '0', clearedBacklogs: '0' },
        elig_gap: { status: 'eligible', gapMonths: '0' }
      };
    }

    // Pipeline checklist
    if (!s.pipeline) {
      s.pipeline = {
        checks: {},
        notes: {}
      };
    }

    // Quants state
    if (!s.quants) s.quants = {};

    // Verbal state
    if (!s.verbal) s.verbal = {};

    // Reasoning state
    if (!s.reasoning) s.reasoning = {};

    // DSA state
    if (!s.dsa) s.dsa = {};
    if (!s.dsaAssignments) s.dsaAssignments = {};

    // Technical subjects state
    if (!s.technical) s.technical = {};

    // Daily study logs
    if (!s.dailyLogs) s.dailyLogs = {};

    // Today's date in YYYY-MM-DD
    const todayStr = getTodayDateString();
    if (!s.currentStudyDate) s.currentStudyDate = todayStr;

    saveJobPrepState();
  }

  function getTodayDateString() {
    const d = new Date();
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  function saveJobPrepState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(window.jobPrepState));
      updateJobPrepSidebarBadge();
    } catch (e) {
      console.error('Failed to persist Job Prep Tracker state:', e);
    }
  }

  // Update sidebar badge
  function updateJobPrepSidebarBadge() {
    const badge = document.getElementById('nav-jobprep-badge');
    if (!badge || !window.jobPrepState) return;

    const metrics = calculateJobPrepMetrics();
    badge.textContent = `${metrics.overallPercent}%`;
    if (metrics.overallPercent === 100) {
      badge.style.background = 'rgba(16, 185, 129, 0.2)';
      badge.style.color = '#10b981';
      badge.style.borderColor = 'rgba(16, 185, 129, 0.4)';
    } else {
      badge.style.background = 'rgba(245, 158, 11, 0.15)';
      badge.style.color = '#f59e0b';
      badge.style.borderColor = 'rgba(245, 158, 11, 0.3)';
    }
  }

  // Calculate comprehensive metrics
  function calculateJobPrepMetrics() {
    if (!window.JOB_PREP_DATA || !window.jobPrepState) {
      return {
        totalItems: 0,
        completedItems: 0,
        overallPercent: 0,
        aptitudeTotal: 0,
        aptitudeDone: 0,
        aptitudePercent: 0,
        dsaTotal: 0,
        dsaDone: 0,
        dsaPercent: 0,
        techTotal: 0,
        techDone: 0,
        techPercent: 0,
        todayHours: 0,
        todayTargetPercent: 0,
        eligibilityStatus: 'needs_verification'
      };
    }

    const s = window.jobPrepState;
    const d = window.JOB_PREP_DATA;

    // 1. Quants calculation (35 topics * 4 steps = 140 points)
    let quantsStepsTotal = 0;
    let quantsStepsDone = 0;
    d.quants.groups.forEach(g => {
      g.topics.forEach(t => {
        quantsStepsTotal += 4;
        const state = s.quants[t.id] || {};
        if (state.learn) quantsStepsDone++;
        if (state.examples) quantsStepsDone++;
        if (state.practice) quantsStepsDone++;
        if (state.mock) quantsStepsDone++;
      });
    });

    // 2. Verbal calculation (10 topics * 3 completion steps = 30 points)
    let verbalStepsTotal = 0;
    let verbalStepsDone = 0;
    d.verbal.topics.forEach(t => {
      verbalStepsTotal += 3;
      const state = s.verbal[t.id] || {};
      if (state.learned) verbalStepsDone++;
      if (state.practiced) verbalStepsDone++;
      if (state.revised) verbalStepsDone++;
    });

    // 3. Reasoning calculation (19 topics * 3 completion steps = 57 points)
    let reasoningStepsTotal = 0;
    let reasoningStepsDone = 0;
    d.reasoning.groups.forEach(g => {
      g.topics.forEach(t => {
        reasoningStepsTotal += 3;
        const state = s.reasoning[t.id] || {};
        if (state.learned) reasoningStepsDone++;
        if (state.examples) reasoningStepsDone++;
        if (state.practice) reasoningStepsDone++;
      });
    });

    const aptiTotal = quantsStepsTotal + verbalStepsTotal + reasoningStepsTotal;
    const aptiDone = quantsStepsDone + verbalStepsDone + reasoningStepsDone;
    const aptiPercent = aptiTotal > 0 ? Math.round((aptiDone / aptiTotal) * 100) : 0;

    // 4. DSA calculation (All problems across weeks)
    let dsaTotal = 0;
    let dsaDone = 0;
    d.dsaWeeks.forEach(w => {
      w.problems.forEach(p => {
        dsaTotal++;
        const state = s.dsa[p.id] || {};
        if (state.status === 'solved' || state.status === 'completed') {
          dsaDone++;
        }
      });
    });
    const dsaPercent = dsaTotal > 0 ? Math.round((dsaDone / dsaTotal) * 100) : 0;

    // 5. Technical Interview calculation (subtopics + custom subtopics)
    let techSubtopicsTotal = 0;
    let techSubtopicsDone = 0;
    d.technicalSubjects.forEach(subj => {
      const state = s.technical[subj.id] || {};
      const subDoneMap = state.subDone || {};
      subj.defaultSubtopics.forEach((_, idx) => {
        techSubtopicsTotal++;
        if (subDoneMap[idx]) techSubtopicsDone++;
      });
      if (Array.isArray(state.customSubtopics)) {
        state.customSubtopics.forEach(c => {
          techSubtopicsTotal++;
          if (c.done) techSubtopicsDone++;
        });
      }
    });
    const techPercent = techSubtopicsTotal > 0 ? Math.round((techSubtopicsDone / techSubtopicsTotal) * 100) : 0;

    // 6. Overall totals
    const grandTotal = aptiTotal + dsaTotal + techSubtopicsTotal;
    const grandDone = aptiDone + dsaDone + techSubtopicsDone;
    const overallPercent = grandTotal > 0 ? Math.round((grandDone / grandTotal) * 100) : 0;

    // 7. Today's study hours
    const todayDate = s.currentStudyDate || getTodayDateString();
    const todayLog = s.dailyLogs[todayDate] || {};
    const aptiH = parseFloat(todayLog.aptitudeHours) || 0;
    const dsaH = parseFloat(todayLog.dsaHours) || 0;
    const coreH = parseFloat(todayLog.coreHours) || 0;
    const todayHours = Math.round((aptiH + dsaH + coreH) * 10) / 10;
    const todayTargetPercent = Math.min(100, Math.round((todayHours / 5) * 100));

    // 8. Eligibility status
    let eligStatus = 'eligible';
    const batchStat = s.eligibility?.elig_batch?.status;
    if (batchStat === 'needs_verification') {
      eligStatus = 'needs_verification';
    } else if (Object.values(s.eligibility || {}).some(e => e.status === 'not_eligible')) {
      eligStatus = 'not_eligible';
    }

    return {
      totalItems: grandTotal,
      completedItems: grandDone,
      overallPercent,
      aptitudeTotal: aptiTotal,
      aptitudeDone: aptiDone,
      aptitudePercent: aptiPercent,
      dsaTotal,
      dsaDone,
      dsaPercent,
      techTotal: techSubtopicsTotal,
      techDone: techSubtopicsDone,
      techPercent,
      todayHours,
      todayTargetPercent,
      eligibilityStatus: eligStatus
    };
  }

  // Find next pending topic
  function findNextPendingTopic() {
    if (!window.JOB_PREP_DATA || !window.jobPrepState) return null;
    const s = window.jobPrepState;
    const d = window.JOB_PREP_DATA;

    // First check DSA
    for (const week of d.dsaWeeks) {
      for (const p of week.problems) {
        const pState = s.dsa[p.id] || {};
        if (pState.status !== 'solved' && pState.status !== 'completed') {
          return {
            type: 'dsa',
            tab: 'dsa',
            week: week.weekNumber,
            id: p.id,
            title: p.title,
            subtitle: `${week.title} · ${p.difficulty}`,
            link: p.link
          };
        }
      }
    }

    // Then check Quants
    for (const group of d.quants.groups) {
      for (const t of group.topics) {
        const qState = s.quants[t.id] || {};
        if (!qState.practice || !qState.mock) {
          return {
            type: 'quants',
            tab: 'quants',
            id: t.id,
            title: t.name,
            subtitle: `${group.name}`
          };
        }
      }
    }

    // Then check Reasoning
    for (const group of d.reasoning.groups) {
      for (const t of group.topics) {
        const rState = s.reasoning[t.id] || {};
        if (!rState.practice) {
          return {
            type: 'reasoning',
            tab: 'reasoning',
            id: t.id,
            title: t.name,
            subtitle: `${group.name}`
          };
        }
      }
    }

    return null;
  }

  // Main render dispatcher
  function renderJobPrepView() {
    initJobPrepState();
    const container = document.getElementById('view-jobprep');
    if (!container) return;

    const s = window.jobPrepState;
    const metrics = calculateJobPrepMetrics();
    const nextTopic = findNextPendingTopic();

    let nextTopicHtml = '';
    if (nextTopic) {
      nextTopicHtml = `
        <div class="jp-next-callout">
          <div class="jp-next-left">
            <span class="jp-next-badge">🎯 NEXT RECOMMENDED TARGET</span>
            <div class="jp-next-title">${escapeHtml(nextTopic.title)}</div>
            <div class="jp-next-sub">${escapeHtml(nextTopic.subtitle)}</div>
          </div>
          <button class="jp-btn jp-btn-primary" onclick="window.jobPrepController.jumpToTab('${nextTopic.tab}', '${nextTopic.id}')">
            Continue Topic ➔
          </button>
        </div>
      `;
    }

    container.innerHTML = `
      <div class="jp-container">
        <!-- HERO CARD -->
        <div class="jp-hero-card">
          <div class="jp-hero-top">
            <div class="jp-title-box">
              <div class="jp-title-icon">🚀</div>
              <div>
                <h2 class="jp-title">Job Preparation Command Center</h2>
                <p class="jp-subtitle">10-Week Placement Roadmap · OA Elimination Shield · DSA & CS Interview Mastery</p>
              </div>
            </div>
            <div class="jp-quick-actions">
              <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.jumpToTab('daily')">
                ⏱️ Log Daily Study
              </button>
              <button class="jp-btn jp-btn-secondary" onclick="switchView('settings')">
                💾 Storage & Backup
              </button>
            </div>
          </div>

          <!-- METRICS GRID -->
          <div class="jp-metrics-grid">
            <div class="jp-metric-card">
              <div class="jp-metric-header">
                <span class="jp-metric-label">Overall Preparation</span>
                <span class="jp-metric-badge">${metrics.completedItems}/${metrics.totalItems} done</span>
              </div>
              <div class="jp-metric-val">${metrics.overallPercent}%</div>
              <div class="jp-progress-track">
                <div class="jp-progress-bar" style="width: ${metrics.overallPercent}%;"></div>
              </div>
            </div>

            <div class="jp-metric-card">
              <div class="jp-metric-header">
                <span class="jp-metric-label">Aptitude & Reasoning</span>
                <span class="jp-metric-badge">64 Topics</span>
              </div>
              <div class="jp-metric-val" style="color: #f59e0b;">${metrics.aptitudePercent}%</div>
              <div class="jp-progress-track">
                <div class="jp-progress-bar" style="width: ${metrics.aptitudePercent}%; background: linear-gradient(90deg, #f59e0b, #fbbf24);"></div>
              </div>
            </div>

            <div class="jp-metric-card">
              <div class="jp-metric-header">
                <span class="jp-metric-label">DSA Core Roadmap</span>
                <span class="jp-metric-badge">${metrics.dsaDone}/${metrics.dsaTotal} Solved</span>
              </div>
              <div class="jp-metric-val" style="color: #3b82f6;">${metrics.dsaPercent}%</div>
              <div class="jp-progress-track">
                <div class="jp-progress-bar" style="width: ${metrics.dsaPercent}%; background: linear-gradient(90deg, #3b82f6, #60a5fa);"></div>
              </div>
            </div>

            <div class="jp-metric-card">
              <div class="jp-metric-header">
                <span class="jp-metric-label">Technical Interview</span>
                <span class="jp-metric-badge">6 CS Domains</span>
              </div>
              <div class="jp-metric-val" style="color: #10b981;">${metrics.techPercent}%</div>
              <div class="jp-progress-track">
                <div class="jp-progress-bar" style="width: ${metrics.techPercent}%; background: linear-gradient(90deg, #10b981, #34d399);"></div>
              </div>
            </div>

            <div class="jp-metric-card">
              <div class="jp-metric-header">
                <span class="jp-metric-label">Today's Study (Target: 5h)</span>
                <span class="jp-metric-badge">${metrics.todayHours}h logged</span>
              </div>
              <div class="jp-metric-val" style="color: ${metrics.todayHours >= 5 ? '#10b981' : '#a855f7'};">${metrics.todayTargetPercent}%</div>
              <div class="jp-progress-track">
                <div class="jp-progress-bar" style="width: ${metrics.todayTargetPercent}%; background: linear-gradient(90deg, #a855f7, #c084fc);"></div>
              </div>
            </div>

            <div class="jp-metric-card">
              <div class="jp-metric-header">
                <span class="jp-metric-label">Batch Eligibility</span>
                <span class="jp-metric-badge">User: 2027</span>
              </div>
              <div class="jp-metric-val" style="font-size: 16px; font-weight: 600; color: ${metrics.eligibilityStatus === 'eligible' ? '#10b981' : metrics.eligibilityStatus === 'needs_verification' ? '#f59e0b' : '#ef4444'};">
                ${metrics.eligibilityStatus === 'eligible' ? '✅ Verified Eligible' : metrics.eligibilityStatus === 'needs_verification' ? '⚠️ Check Company JD' : '❌ Not Eligible'}
              </div>
              <div style="font-size: 11px; color: var(--text-muted, #94a3b8); margin-top: 4px;">
                2026 slides vs 2027 user batch
              </div>
            </div>
          </div>

          ${nextTopicHtml}
        </div>

        <!-- TABS NAVIGATOR -->
        <div class="jp-tabs-bar">
          <button class="jp-tab-btn ${s.activeTab === 'overview' ? 'active' : ''}" onclick="window.jobPrepController.setTab('overview')">
            📌 Overview
          </button>
          <button class="jp-tab-btn ${s.activeTab === 'eligibility' ? 'active' : ''}" onclick="window.jobPrepController.setTab('eligibility')">
            🎓 Eligibility & Batch
          </button>
          <button class="jp-tab-btn ${s.activeTab === 'pipeline' ? 'active' : ''}" onclick="window.jobPrepController.setTab('pipeline')">
            🏢 3-Round Pipeline
          </button>
          <button class="jp-tab-btn ${s.activeTab === 'quants' ? 'active' : ''}" onclick="window.jobPrepController.setTab('quants')">
            🧮 Quants (35)
          </button>
          <button class="jp-tab-btn ${s.activeTab === 'verbal' ? 'active' : ''}" onclick="window.jobPrepController.setTab('verbal')">
            🗣️ Verbal (10)
          </button>
          <button class="jp-tab-btn ${s.activeTab === 'reasoning' ? 'active' : ''}" onclick="window.jobPrepController.setTab('reasoning')">
            🧩 Reasoning (19)
          </button>
          <button class="jp-tab-btn ${s.activeTab === 'dsa' ? 'active' : ''}" onclick="window.jobPrepController.setTab('dsa')">
            ⚡ DSA (8+3 Wks)
          </button>
          <button class="jp-tab-btn ${s.activeTab === 'technical' ? 'active' : ''}" onclick="window.jobPrepController.setTab('technical')">
            💻 Tech Subjects (6)
          </button>
          <button class="jp-tab-btn ${s.activeTab === 'daily' ? 'active' : ''}" onclick="window.jobPrepController.setTab('daily')">
            ⏱️ Daily 5h Study Log
          </button>
        </div>

        <!-- SEARCH & FILTER TOOLBAR (for list tabs) -->
        ${['quants', 'verbal', 'reasoning', 'dsa', 'technical'].includes(s.activeTab) ? `
          <div class="jp-filter-toolbar">
            <div class="jp-search-box">
              <span class="jp-search-icon">🔍</span>
              <input type="text" class="jp-search-input" placeholder="Search topics, problems, keywords..." value="${escapeHtml(s.searchQuery)}" oninput="window.jobPrepController.setSearch(this.value)" />
              ${s.searchQuery ? `<button class="jp-search-clear" onclick="window.jobPrepController.setSearch('')">×</button>` : ''}
            </div>
            <div class="jp-filter-pills">
              <button class="jp-filter-pill ${s.filter === 'all' ? 'active' : ''}" onclick="window.jobPrepController.setFilter('all')">All</button>
              <button class="jp-filter-pill ${s.filter === 'pending' ? 'active' : ''}" onclick="window.jobPrepController.setFilter('pending')">Pending</button>
              <button class="jp-filter-pill ${s.filter === 'completed' ? 'active' : ''}" onclick="window.jobPrepController.setFilter('completed')">Completed</button>
              ${s.activeTab === 'dsa' ? `<button class="jp-filter-pill ${s.filter === 'revision' ? 'active' : ''}" onclick="window.jobPrepController.setFilter('revision')">Revision Needed</button>` : ''}
            </div>
          </div>
        ` : ''}

        <!-- TAB CONTENT CONTAINER -->
        <div class="jp-tab-content">
          ${renderActiveTabContent(s.activeTab)}
        </div>
      </div>

      <!-- NOTES MODAL -->
      <div id="jpNotesModal" class="jp-modal-overlay" style="display:none;" onclick="if(event.target === this) window.jobPrepController.closeNotesModal()">
        <div class="jp-modal-card">
          <div class="jp-modal-header">
            <div>
              <div class="jp-modal-title" id="jpNotesModalTitle">Topic Notes & Mistakes</div>
              <div class="jp-modal-sub" id="jpNotesModalSub">Record key tricks, time complexity & edge cases</div>
            </div>
            <button class="jp-modal-close" onclick="window.jobPrepController.closeNotesModal()">×</button>
          </div>
          <div class="jp-modal-body">
            <textarea id="jpNotesTextarea" class="jp-notes-editor" placeholder="Write markdown notes, edge cases, formulas, or tricky mistakes..."></textarea>
          </div>
          <div class="jp-modal-footer">
            <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.closeNotesModal()">Cancel</button>
            <button class="jp-btn jp-btn-primary" onclick="window.jobPrepController.saveNotesModal()">Save Notes</button>
          </div>
        </div>
      </div>
    `;

    updateJobPrepSidebarBadge();
  }

  // Active tab renderer router
  function renderActiveTabContent(tab) {
    switch (tab) {
      case 'overview':
        return renderOverviewTab();
      case 'eligibility':
        return renderEligibilityTab();
      case 'pipeline':
        return renderPipelineTab();
      case 'quants':
        return renderQuantsTab();
      case 'verbal':
        return renderVerbalTab();
      case 'reasoning':
        return renderReasoningTab();
      case 'dsa':
        return renderDsaTab();
      case 'technical':
        return renderTechnicalTab();
      case 'daily':
        return renderDailyStudyTab();
      default:
        return renderOverviewTab();
    }
  }

  /* --- 1. OVERVIEW TAB --- */
  function renderOverviewTab() {
    const d = window.JOB_PREP_DATA;
    const s = window.jobPrepState;
    const metrics = calculateJobPrepMetrics();

    return `
      <div class="jp-overview-grid">
        <!-- STRATEGY BANNER -->
        <div class="jp-section-card jp-col-12" style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.9));">
          <div style="display: flex; gap: 1rem; align-items: flex-start;">
            <div style="font-size: 32px;">🛡️</div>
            <div>
              <h3 style="margin: 0 0 0.4rem 0; font-size: 17px; font-weight: 700; color: #f8fafc;">
                Placement Strategy: The 10-Week Master Blueprint
              </h3>
              <p style="margin: 0; font-size: 13px; color: #94a3b8; line-height: 1.5;">
                Every placement round is an elimination filter. Round 1 Online Assessment wipes out ~90% of applicants through timed speed math, tricky reasoning, and boundary test cases. Round 2 tests core CS clarity and live problem explanation. Follow the <strong>Daily 5-Hour Rule</strong> (2h Aptitude + 2h DSA + 1h Core) to systematically build placement readiness.
              </p>
            </div>
          </div>
        </div>

        <!-- 3-PILLAR SUMMARY CARDS -->
        <div class="jp-section-card">
          <div class="jp-card-header">
            <div>
              <h4 class="jp-card-title">🧮 Aptitude & Reasoning Foundation</h4>
              <p class="jp-card-sub">35 Quants · 10 Verbal · 19 Logical</p>
            </div>
            <span class="jp-status-pill ${metrics.aptitudePercent === 100 ? 'status-completed' : 'status-pending'}">
              ${metrics.aptitudePercent}% Ready
            </span>
          </div>
          <p style="font-size: 12.5px; color: #94a3b8; margin: 0 0 1rem 0;">
            Includes Group 7 Visual Reasoning (high frequency in TCS, Capgemini, Accenture), 4-step Quant mastery, and 1-week Verbal sprint.
          </p>
          <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
            <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.setTab('quants')">Quants (35) ➔</button>
            <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.setTab('verbal')">Verbal (10) ➔</button>
            <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.setTab('reasoning')">Reasoning (19) ➔</button>
          </div>
        </div>

        <div class="jp-section-card">
          <div class="jp-card-header">
            <div>
              <h4 class="jp-card-title">⚡ DSA 8-Week Core + Extension</h4>
              <p class="jp-card-sub">65+ Curated Placement Problems & Sunday Tests</p>
            </div>
            <span class="jp-status-pill ${metrics.dsaPercent === 100 ? 'status-completed' : 'status-in-progress'}">
              ${metrics.dsaDone}/${metrics.dsaTotal} Solved
            </span>
          </div>
          <p style="font-size: 12.5px; color: #94a3b8; margin: 0 0 1rem 0;">
            From Week 1 Math & Complexity to Arrays (Dutch Flag, Kadane), Strings, Sorting, Binary Search, Recursion, Linked Lists, and Weeks 9-11 Extensions.
          </p>
          <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.setTab('dsa')">
            Open DSA Roadmap ➔
          </button>
        </div>

        <div class="jp-section-card">
          <div class="jp-card-header">
            <div>
              <h4 class="jp-card-title">💻 Technical Interview & Resume Defense</h4>
              <p class="jp-card-sub">OOPS, DBMS/SQL, OS, CN, Major Projects & Resume</p>
            </div>
            <span class="jp-status-pill ${metrics.techPercent === 100 ? 'status-completed' : 'status-pending'}">
              ${metrics.techPercent}% Mastered
            </span>
          </div>
          <p style="font-size: 12.5px; color: #94a3b8; margin: 0 0 1rem 0;">
            Deep-dive concepts, live SQL query drills, architecture defenses, customizable subtopics, and confidence ratings.
          </p>
          <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.setTab('technical')">
            Open Tech Subjects ➔
          </button>
        </div>

        <div class="jp-section-card">
          <div class="jp-card-header">
            <div>
              <h4 class="jp-card-title">⏱️ Today's 5-Hour Study Tracker</h4>
              <p class="jp-card-sub">2h Aptitude + 2h DSA + 1h Core</p>
            </div>
            <span class="jp-status-pill ${metrics.todayHours >= 5 ? 'status-completed' : 'status-in-progress'}">
              ${metrics.todayHours}/5 Hours
            </span>
          </div>
          <div class="jp-progress-track" style="margin-bottom: 1rem;">
            <div class="jp-progress-bar" style="width: ${metrics.todayTargetPercent}%; background: linear-gradient(90deg, #a855f7, #3b82f6);"></div>
          </div>
          <button class="jp-btn jp-btn-primary" onclick="window.jobPrepController.setTab('daily')">
            Log Today's Hours ➔
          </button>
        </div>
      </div>
    `;
  }

  /* --- 2. ELIGIBILITY TAB --- */
  function renderEligibilityTab() {
    const d = window.JOB_PREP_DATA.eligibility;
    const s = window.jobPrepState.eligibility || {};

    let criteriaHtml = d.criteria.map(c => {
      const state = s[c.id] || { status: c.defaultStatus };
      const statusPill = state.status === 'eligible'
        ? `<span class="jp-status-pill status-completed">✅ Eligible</span>`
        : state.status === 'needs_verification'
        ? `<span class="jp-status-pill status-needs-revision">⚠️ Needs Verification</span>`
        : `<span class="jp-status-pill status-not-started">❌ Not Eligible</span>`;

      return `
        <div class="jp-item-card">
          <div class="jp-item-top">
            <div>
              <div class="jp-item-title">${escapeHtml(c.title)}</div>
              <div class="jp-item-sub">${escapeHtml(c.desc)}</div>
            </div>
            <div style="display: flex; gap: 0.5rem; align-items: center;">
              <select class="jp-select" onchange="window.jobPrepController.updateEligibilityStatus('${c.id}', this.value)">
                <option value="eligible" ${state.status === 'eligible' ? 'selected' : ''}>Eligible</option>
                <option value="needs_verification" ${state.status === 'needs_verification' ? 'selected' : ''}>Needs Verification</option>
                <option value="not_eligible" ${state.status === 'not_eligible' ? 'selected' : ''}>Not Eligible</option>
              </select>
              ${statusPill}
            </div>
          </div>
          <div class="jp-fields-row">
            ${c.fields.map(f => `
              <div class="jp-field-group">
                <label class="jp-field-label">${escapeHtml(f.label)}</label>
                <input type="text" class="jp-field-input" placeholder="${escapeHtml(f.placeholder)}" value="${escapeHtml(state[f.key] || '')}" onchange="window.jobPrepController.updateEligibilityField('${c.id}', '${f.key}', this.value)" />
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }).join('');

    let tcsHtml = `
      <div class="jp-section-card" style="margin-top: 1.5rem;">
        <h4 class="jp-card-title" style="margin-bottom: 0.25rem;">${escapeHtml(d.tcsReference.title)}</h4>
        <p class="jp-card-sub" style="margin-bottom: 1rem;">Reference comparison of roles, salary packages, and selection focus based on degree stream.</p>
        <div class="jp-table-wrapper">
          <table class="jp-data-table">
            <thead>
              <tr>
                <th>Eligible Stream</th>
                <th>Drive / Role</th>
                <th>Package (CTC)</th>
                <th>Selection Focus</th>
              </tr>
            </thead>
            <tbody>
              ${d.tcsReference.items.map(t => `
                <tr>
                  <td><strong>${escapeHtml(t.stream)}</strong></td>
                  <td><span class="jp-tag">${escapeHtml(t.role)}</span></td>
                  <td style="color: #10b981; font-weight: 600;">${escapeHtml(t.package)}</td>
                  <td style="font-size: 12px; color: #94a3b8;">${escapeHtml(t.focus)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    return `
      <div>
        <div class="jp-section-card" style="margin-bottom: 1.25rem;">
          <h3 class="jp-card-title">${escapeHtml(d.title)}</h3>
          <p class="jp-card-sub">${escapeHtml(d.note)}</p>
        </div>
        <div class="jp-items-list">
          ${criteriaHtml}
        </div>
        ${tcsHtml}
      </div>
    `;
  }

  /* --- 3. PIPELINE TAB --- */
  function renderPipelineTab() {
    const pipeline = window.JOB_PREP_DATA.hiringPipeline;
    const s = window.jobPrepState.pipeline || { checks: {}, notes: {} };

    return `
      <div class="jp-pipeline-container">
        ${pipeline.map(round => `
          <div class="jp-section-card jp-pipeline-round-card">
            <div class="jp-pipeline-badge">ROUND ${round.roundNumber}</div>
            <h3 class="jp-card-title" style="margin-top: 0.5rem; font-size: 18px;">${escapeHtml(round.title)}</h3>
            <p class="jp-card-sub" style="margin-bottom: 1rem;">${escapeHtml(round.subtitle)}</p>

            <div class="jp-callout-box ${round.roundNumber === 1 ? 'callout-danger' : 'callout-info'}">
              ${escapeHtml(round.dangerCallout)}
            </div>

            <!-- ROUND COMPONENTS -->
            <div class="jp-round-components-grid">
              ${round.components.map(comp => `
                <div class="jp-component-box">
                  <div class="jp-component-name">${escapeHtml(comp.name)}</div>
                  <div class="jp-component-desc">${escapeHtml(comp.desc)}</div>
                </div>
              `).join('')}
            </div>

            <!-- CHECKLIST ITEMS -->
            <div class="jp-pipeline-checklist">
              <div style="font-size: 12px; font-weight: 600; color: #cbd5e1; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                Round ${round.roundNumber} Readiness Checklist
              </div>
              ${round.checklist.map(item => {
                const checked = !!s.checks[item.id];
                return `
                  <label class="jp-checkbox-row">
                    <input type="checkbox" class="jp-checkbox" ${checked ? 'checked' : ''} onchange="window.jobPrepController.togglePipelineCheck('${item.id}', this.checked)" />
                    <span class="${checked ? 'jp-text-done' : ''}">${escapeHtml(item.label)}</span>
                  </label>
                `;
              }).join('')}
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }

  /* --- 4. QUANTS TAB --- */
  function renderQuantsTab() {
    const quants = window.JOB_PREP_DATA.quants;
    const s = window.jobPrepState;
    const query = (s.searchQuery || '').toLowerCase();
    const filter = s.filter || 'all';

    return `
      <div>
        <div class="jp-section-card" style="margin-bottom: 1.25rem;">
          <h3 class="jp-card-title">${escapeHtml(quants.title)}</h3>
          <p class="jp-card-sub">${escapeHtml(quants.methodology)}</p>
        </div>

        <div class="jp-groups-container">
          ${quants.groups.map(g => {
            const matchingTopics = g.topics.filter(t => {
              if (query && !t.name.toLowerCase().includes(query)) return false;
              const state = s.quants[t.id] || {};
              const isDone = state.learn && state.examples && state.practice && state.mock;
              if (filter === 'completed' && !isDone) return false;
              if (filter === 'pending' && isDone) return false;
              return true;
            });

            if (matchingTopics.length === 0 && (query || filter !== 'all')) return '';

            return `
              <div class="jp-section-card jp-group-card">
                <div class="jp-group-header">
                  <h4 class="jp-group-title">${escapeHtml(g.name)}</h4>
                  <span class="jp-tag">${matchingTopics.length} Topics</span>
                </div>

                <div class="jp-topics-grid">
                  ${matchingTopics.map(t => {
                    const state = s.quants[t.id] || {};
                    const isAllDone = state.learn && state.examples && state.practice && state.mock;

                    return `
                      <div class="jp-topic-card ${isAllDone ? 'topic-completed' : ''}" id="topic-${t.id}">
                        <div class="jp-topic-top">
                          <span class="jp-topic-title">${escapeHtml(t.name)}</span>
                          <button class="jp-btn-icon" title="Topic Notes" onclick="window.jobPrepController.openNotesModal('quants', '${t.id}', '${escapeJs(t.name)}')">
                            ${state.notes ? '📝' : '📄'}
                          </button>
                        </div>
                        <div class="jp-chips-row">
                          <button class="jp-chip ${state.learn ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('quants', '${t.id}', 'learn')">
                            1. Learn Concept
                          </button>
                          <button class="jp-chip ${state.examples ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('quants', '${t.id}', 'examples')">
                            2. 10-15 Examples
                          </button>
                          <button class="jp-chip ${state.practice ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('quants', '${t.id}', 'practice')">
                            3. 20-30 Practice
                          </button>
                          <button class="jp-chip ${state.mock ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('quants', '${t.id}', 'mock')">
                            4. Timed Mock
                          </button>
                        </div>
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  /* --- 5. VERBAL TAB --- */
  function renderVerbalTab() {
    const verbal = window.JOB_PREP_DATA.verbal;
    const s = window.jobPrepState;
    const query = (s.searchQuery || '').toLowerCase();
    const filter = s.filter || 'all';

    const matchingTopics = verbal.topics.filter(t => {
      if (query && !t.name.toLowerCase().includes(query)) return false;
      const state = s.verbal[t.id] || {};
      const isDone = state.learned && state.practiced && state.revised;
      if (filter === 'completed' && !isDone) return false;
      if (filter === 'pending' && isDone) return false;
      return true;
    });

    return `
      <div>
        <div class="jp-section-card" style="margin-bottom: 1.25rem;">
          <h3 class="jp-card-title">${escapeHtml(verbal.title)}</h3>
          <p class="jp-card-sub">${escapeHtml(verbal.roadmapNote)}</p>
        </div>

        <div class="jp-topics-grid">
          ${matchingTopics.map(t => {
            const state = s.verbal[t.id] || {};
            const isAllDone = state.learned && state.practiced && state.revised;

            return `
              <div class="jp-topic-card ${isAllDone ? 'topic-completed' : ''}" id="topic-${t.id}">
                <div class="jp-topic-top">
                  <div>
                    <span class="jp-tag" style="margin-bottom: 4px; display: inline-block;">${escapeHtml(t.days)}</span>
                    <div class="jp-topic-title">${escapeHtml(t.name)}</div>
                  </div>
                  <button class="jp-btn-icon" title="Verbal Notes" onclick="window.jobPrepController.openNotesModal('verbal', '${t.id}', '${escapeJs(t.name)}')">
                    ${state.notes ? '📝' : '📄'}
                  </button>
                </div>
                <div class="jp-chips-row">
                  <button class="jp-chip ${state.learned ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('verbal', '${t.id}', 'learned')">
                    Rules & Theory
                  </button>
                  <button class="jp-chip ${state.practiced ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('verbal', '${t.id}', 'practiced')">
                    Practice (${t.count})
                  </button>
                  <button class="jp-chip ${state.revised ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('verbal', '${t.id}', 'revised')">
                    Revision
                  </button>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  /* --- 6. REASONING TAB --- */
  function renderReasoningTab() {
    const reasoning = window.JOB_PREP_DATA.reasoning;
    const s = window.jobPrepState;
    const query = (s.searchQuery || '').toLowerCase();
    const filter = s.filter || 'all';

    return `
      <div>
        <div class="jp-section-card" style="margin-bottom: 1.25rem;">
          <h3 class="jp-card-title">${escapeHtml(reasoning.title)}</h3>
          <p class="jp-card-sub">${escapeHtml(reasoning.visualNote)}</p>
        </div>

        <div class="jp-groups-container">
          ${reasoning.groups.map(g => {
            const matchingTopics = g.topics.filter(t => {
              if (query && !t.name.toLowerCase().includes(query)) return false;
              const state = s.reasoning[t.id] || {};
              const isDone = state.learned && state.examples && state.practice;
              if (filter === 'completed' && !isDone) return false;
              if (filter === 'pending' && isDone) return false;
              return true;
            });

            if (matchingTopics.length === 0 && (query || filter !== 'all')) return '';

            return `
              <div class="jp-section-card jp-group-card ${g.isHighPriority ? 'jp-high-priority-border' : ''}">
                <div class="jp-group-header">
                  <div style="display: flex; gap: 0.5rem; align-items: center;">
                    <h4 class="jp-group-title">${escapeHtml(g.name)}</h4>
                    ${g.isHighPriority ? `<span class="jp-status-pill status-needs-revision">🔥 HIGH OA FREQUENCY</span>` : ''}
                  </div>
                  <span class="jp-tag">${matchingTopics.length} Topics</span>
                </div>

                <div class="jp-topics-grid">
                  ${matchingTopics.map(t => {
                    const state = s.reasoning[t.id] || {};
                    const isAllDone = state.learned && state.examples && state.practice;

                    return `
                      <div class="jp-topic-card ${isAllDone ? 'topic-completed' : ''}" id="topic-${t.id}">
                        <div class="jp-topic-top">
                          <span class="jp-topic-title">${escapeHtml(t.name)}</span>
                          <button class="jp-btn-icon" title="Reasoning Notes" onclick="window.jobPrepController.openNotesModal('reasoning', '${t.id}', '${escapeJs(t.name)}')">
                            ${state.notes ? '📝' : '📄'}
                          </button>
                        </div>
                        <div class="jp-chips-row">
                          <button class="jp-chip ${state.learned ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('reasoning', '${t.id}', 'learned')">
                            1. Concept
                          </button>
                          <button class="jp-chip ${state.examples ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('reasoning', '${t.id}', 'examples')">
                            2. Examples
                          </button>
                          <button class="jp-chip ${state.practice ? 'active' : ''}" onclick="window.jobPrepController.toggleChip('reasoning', '${t.id}', 'practice')">
                            3. Practice Drill
                          </button>
                        </div>
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  /* --- 7. DSA ROADMAP TAB --- */
  function renderDsaTab() {
    const weeks = window.JOB_PREP_DATA.dsaWeeks;
    const s = window.jobPrepState;
    const query = (s.searchQuery || '').toLowerCase();
    const filter = s.filter || 'all';

    return `
      <div>
        <div class="jp-section-card" style="margin-bottom: 1.25rem;">
          <h3 class="jp-card-title">Complete DSA Placement Roadmap (Weeks 1 to 8 + Extensions)</h3>
          <p class="jp-card-sub">Curated placement coding questions, difficulty tags, practice links, and Sunday assignments.</p>
        </div>

        <div class="jp-weeks-container">
          ${weeks.map(week => {
            const matchingProblems = week.problems.filter(p => {
              if (query && !p.title.toLowerCase().includes(query)) return false;
              const pState = s.dsa[p.id] || {};
              const status = pState.status || 'not_started';
              if (filter === 'completed' && (status !== 'solved' && status !== 'completed')) return false;
              if (filter === 'pending' && (status === 'solved' || status === 'completed')) return false;
              if (filter === 'revision' && status !== 'revision') return false;
              return true;
            });

            if (matchingProblems.length === 0 && (query || filter !== 'all')) return '';

            const assignmentState = s.dsaAssignments[week.weekNumber] || {};

            return `
              <div class="jp-section-card jp-week-card">
                <div class="jp-week-header">
                  <div>
                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                      <h4 class="jp-week-title">${escapeHtml(week.title)}</h4>
                      ${week.isExtension ? `<span class="jp-tag" style="background: rgba(168, 85, 247, 0.15); color: #c084fc;">Extension</span>` : ''}
                    </div>
                    <p class="jp-card-sub" style="margin: 0.25rem 0 0 0;">${escapeHtml(week.goal)}</p>
                  </div>
                  <span class="jp-tag">${matchingProblems.length} Problems</span>
                </div>

                <div class="jp-problems-table-wrap">
                  <table class="jp-data-table">
                    <thead>
                      <tr>
                        <th style="width: 40px;">#</th>
                        <th>Problem Statement</th>
                        <th style="width: 90px;">Difficulty</th>
                        <th style="width: 140px;">Status</th>
                        <th style="width: 80px;">Time</th>
                        <th style="width: 110px;">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      ${matchingProblems.map((p, pIdx) => {
                        const pState = s.dsa[p.id] || {};
                        const status = pState.status || 'not_started';
                        const diffBadge = p.difficulty === 'Easy'
                          ? `<span class="jp-diff-badge diff-easy">Easy</span>`
                          : p.difficulty === 'Medium'
                          ? `<span class="jp-diff-badge diff-medium">Medium</span>`
                          : `<span class="jp-diff-badge diff-hard">Hard</span>`;

                        return `
                          <tr class="${status === 'solved' || status === 'completed' ? 'tr-done' : ''}" id="prob-${p.id}">
                            <td style="color: #64748b; font-size: 11px;">${pIdx + 1}</td>
                            <td>
                              <div style="font-weight: 500; color: #f1f5f9;">
                                ${escapeHtml(p.title)}
                              </div>
                            </td>
                            <td>${diffBadge}</td>
                            <td>
                              <select class="jp-select" onchange="window.jobPrepController.updateDsaStatus('${p.id}', this.value)">
                                <option value="not_started" ${status === 'not_started' ? 'selected' : ''}>Not Started</option>
                                <option value="attempted" ${status === 'attempted' ? 'selected' : ''}>Attempted</option>
                                <option value="solved" ${status === 'solved' ? 'selected' : ''}>Solved Independently</option>
                                <option value="revision" ${status === 'revision' ? 'selected' : ''}>Needs Revision</option>
                                <option value="completed" ${status === 'completed' ? 'selected' : ''}>Completed</option>
                              </select>
                            </td>
                            <td>
                              <input type="number" class="jp-field-input" style="width: 65px; padding: 4px 6px; font-size: 11px;" placeholder="min" value="${pState.minutes || ''}" onchange="window.jobPrepController.updateDsaMinutes('${p.id}', this.value)" />
                            </td>
                            <td>
                              <div style="display: flex; gap: 0.35rem; align-items: center;">
                                <a href="${p.link}" target="_blank" rel="noopener noreferrer" class="jp-btn-icon" title="Open Problem Sheet / LeetCode">🔗</a>
                                <button class="jp-btn-icon" title="Notes & Mistakes" onclick="window.jobPrepController.openNotesModal('dsa', '${p.id}', '${escapeJs(p.title)}')">
                                  ${pState.notes ? '📝' : '📄'}
                                </button>
                              </div>
                            </td>
                          </tr>
                        `;
                      }).join('')}
                    </tbody>
                  </table>
                </div>

                <!-- SUNDAY ASSIGNMENT -->
                ${week.sundayAssignment ? `
                  <div class="jp-sunday-assignment-box">
                    <label class="jp-checkbox-row">
                      <input type="checkbox" class="jp-checkbox" ${assignmentState.done ? 'checked' : ''} onchange="window.jobPrepController.toggleDsaAssignment(${week.weekNumber}, this.checked)" />
                      <div>
                        <strong style="color: #f59e0b;">${escapeHtml(week.sundayAssignment.title)}:</strong>
                        <span style="font-size: 13px; color: #cbd5e1; margin-left: 4px;">${escapeHtml(week.sundayAssignment.desc)}</span>
                      </div>
                    </label>
                  </div>
                ` : ''}
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  /* --- 8. TECHNICAL INTERVIEW TAB --- */
  function renderTechnicalTab() {
    const subjects = window.JOB_PREP_DATA.technicalSubjects;
    const s = window.jobPrepState;
    const query = (s.searchQuery || '').toLowerCase();

    return `
      <div>
        <div class="jp-section-card" style="margin-bottom: 1.25rem;">
          <h3 class="jp-card-title">Technical Interview Preparation (6 Core Categories)</h3>
          <p class="jp-card-sub">In-depth subtopic checklists, confidence star ratings, personal notes, and custom subtopic capability.</p>
        </div>

        <div class="jp-tech-grid">
          ${subjects.map(subj => {
            const state = s.technical[subj.id] || { confidence: 0, status: 'not_revised', subDone: {}, customSubtopics: [], notes: '' };
            const subDoneMap = state.subDone || {};
            const customSubtopics = Array.isArray(state.customSubtopics) ? state.customSubtopics : [];

            const totalSub = subj.defaultSubtopics.length + customSubtopics.length;
            let doneSub = Object.values(subDoneMap).filter(Boolean).length;
            customSubtopics.forEach(c => { if (c.done) doneSub++; });

            const starsHtml = [1, 2, 3, 4, 5].map(star => `
              <span class="jp-star ${star <= (state.confidence || 0) ? 'filled' : ''}" onclick="window.jobPrepController.setTechConfidence('${subj.id}', ${star})">★</span>
            `).join('');

            return `
              <div class="jp-section-card jp-tech-card" id="tech-${subj.id}">
                <div class="jp-tech-header">
                  <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
                    <span style="font-size: 26px;">${subj.icon}</span>
                    <div>
                      <h4 class="jp-card-title">${escapeHtml(subj.title)}</h4>
                      <p class="jp-card-sub">${escapeHtml(subj.subtitle)}</p>
                    </div>
                  </div>
                  <div style="text-align: right;">
                    <div class="jp-stars-box">${starsHtml}</div>
                    <span class="jp-tag" style="margin-top: 4px;">${doneSub}/${totalSub} Ready</span>
                  </div>
                </div>

                <div class="jp-tech-controls-row">
                  <select class="jp-select" onchange="window.jobPrepController.updateTechStatus('${subj.id}', this.value)">
                    <option value="not_revised" ${state.status === 'not_revised' ? 'selected' : ''}>Not Revised</option>
                    <option value="in_progress" ${state.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                    <option value="mastered" ${state.status === 'mastered' ? 'selected' : ''}>Mastered & Ready</option>
                  </select>
                  <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.openNotesModal('technical', '${subj.id}', '${escapeJs(subj.title)}')">
                    ${state.notes ? '📝 Edit Notes' : '📄 Add Notes'}
                  </button>
                </div>

                <!-- SUBTOPICS CHECKLIST -->
                <div class="jp-subtopics-list">
                  ${subj.defaultSubtopics.map((st, idx) => {
                    if (query && !st.toLowerCase().includes(query)) return '';
                    const checked = !!subDoneMap[idx];
                    return `
                      <label class="jp-checkbox-row">
                        <input type="checkbox" class="jp-checkbox" ${checked ? 'checked' : ''} onchange="window.jobPrepController.toggleTechSubtopic('${subj.id}', ${idx}, this.checked)" />
                        <span class="${checked ? 'jp-text-done' : ''}">${escapeHtml(st)}</span>
                      </label>
                    `;
                  }).join('')}

                  <!-- CUSTOM SUBTOPICS -->
                  ${customSubtopics.map((cs, cIdx) => `
                    <label class="jp-checkbox-row" style="background: rgba(99, 102, 241, 0.05); padding: 4px 6px; border-radius: 4px;">
                      <input type="checkbox" class="jp-checkbox" ${cs.done ? 'checked' : ''} onchange="window.jobPrepController.toggleCustomTechSubtopic('${subj.id}', ${cIdx}, this.checked)" />
                      <span class="${cs.done ? 'jp-text-done' : ''}" style="flex: 1;">${escapeHtml(cs.text)}</span>
                      <button class="jp-btn-icon" style="font-size: 11px;" title="Remove" onclick="window.jobPrepController.removeCustomTechSubtopic('${subj.id}', ${cIdx})">✕</button>
                    </label>
                  `).join('')}
                </div>

                <!-- ADD CUSTOM SUBTOPIC -->
                <div class="jp-add-subtopic-row">
                  <input type="text" class="jp-field-input" id="inputCustomSub_${subj.id}" placeholder="Add custom interview question / subtopic..." onkeydown="if(event.key==='Enter') window.jobPrepController.addCustomTechSubtopic('${subj.id}')" />
                  <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.addCustomTechSubtopic('${subj.id}')">Add</button>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  /* --- 9. DAILY 5-HOUR STUDY LOG TAB --- */
  function renderDailyStudyTab() {
    const s = window.jobPrepState;
    const currentDate = s.currentStudyDate || getTodayDateString();
    const log = s.dailyLogs[currentDate] || {
      aptitudeHours: '',
      aptitudeTopics: '',
      aptitudeDone: false,
      dsaHours: '',
      dsaTopics: '',
      dsaDone: false,
      coreHours: '',
      coreTopics: '',
      coreDone: false,
      notes: ''
    };

    const aptiH = parseFloat(log.aptitudeHours) || 0;
    const dsaH = parseFloat(log.dsaHours) || 0;
    const coreH = parseFloat(log.coreHours) || 0;
    const totalH = Math.round((aptiH + dsaH + coreH) * 10) / 10;
    const targetPercent = Math.min(100, Math.round((totalH / 5) * 100));

    // List of past log dates for history table
    const loggedDates = Object.keys(s.dailyLogs).sort().reverse();

    return `
      <div>
        <!-- DATE NAVIGATOR & GOAL HEADER -->
        <div class="jp-section-card" style="margin-bottom: 1.25rem;">
          <div class="jp-daily-header-row">
            <div>
              <h3 class="jp-card-title">10 Weeks Daily Study Target: 5 Hours Routine</h3>
              <p class="jp-card-sub">Daily split: 2 Hours Aptitude + 2 Hours DSA + 1 Hour Core CS / Technical.</p>
            </div>
            <div class="jp-date-stepper">
              <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.stepDailyDate(-1)">◀ Yesterday</button>
              <input type="date" class="jp-field-input" style="width: 140px; font-weight: 600;" value="${currentDate}" onchange="window.jobPrepController.setDailyDate(this.value)" />
              <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.stepDailyDate(1)">Tomorrow ▶</button>
              <button class="jp-btn jp-btn-secondary" onclick="window.jobPrepController.setDailyDate('${getTodayDateString()}')">Today</button>
            </div>
          </div>

          <!-- DAILY PROGRESS METER -->
          <div class="jp-daily-meter-box">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
              <span style="font-weight: 600; font-size: 14px; color: #f8fafc;">
                Study Completed for ${currentDate}: <strong style="color: ${totalH >= 5 ? '#10b981' : '#f59e0b'};">${totalH} / 5.0 Hours</strong>
              </span>
              <span class="jp-status-pill ${totalH >= 5 ? 'status-completed' : 'status-in-progress'}">
                ${totalH >= 5 ? '🎉 Daily Goal Achieved' : `${Math.round(5 - totalH > 0 ? (5 - totalH) * 10 : 0) / 10}h Remaining`}
              </span>
            </div>
            <div class="jp-progress-track" style="height: 10px;">
              <div class="jp-progress-bar" style="width: ${targetPercent}%; background: linear-gradient(90deg, #3b82f6, #10b981);"></div>
            </div>
          </div>
        </div>

        <!-- 3 DAILY PILLARS CARDS -->
        <div class="jp-pillars-grid">
          <!-- PILLAR 1: APTITUDE -->
          <div class="jp-pillar-card" style="border-top: 3px solid #f59e0b;">
            <div class="jp-pillar-header">
              <div>
                <div class="jp-pillar-badge" style="background: rgba(245, 158, 11, 0.15); color: #f59e0b;">TARGET: 2 HOURS</div>
                <h4 class="jp-pillar-title">🧠 Aptitude & Reasoning</h4>
              </div>
              <input type="checkbox" class="jp-checkbox" ${log.aptitudeDone ? 'checked' : ''} onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'aptitudeDone', this.checked)" />
            </div>
            <div class="jp-pillar-body">
              <div class="jp-field-group">
                <label class="jp-field-label">Hours Logged</label>
                <input type="number" step="0.5" class="jp-field-input" placeholder="e.g. 2.0" value="${log.aptitudeHours || ''}" onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'aptitudeHours', this.value)" />
              </div>
              <div class="jp-field-group">
                <label class="jp-field-label">Topics / Tests Solved</label>
                <textarea class="jp-field-input" rows="2" placeholder="e.g. Time & Work 25 Qs, Blood Relations" onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'aptitudeTopics', this.value)">${escapeHtml(log.aptitudeTopics || '')}</textarea>
              </div>
            </div>
          </div>

          <!-- PILLAR 2: DSA -->
          <div class="jp-pillar-card" style="border-top: 3px solid #3b82f6;">
            <div class="jp-pillar-header">
              <div>
                <div class="jp-pillar-badge" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa;">TARGET: 2 HOURS</div>
                <h4 class="jp-pillar-title">⚡ DSA Coding & Practice</h4>
              </div>
              <input type="checkbox" class="jp-checkbox" ${log.dsaDone ? 'checked' : ''} onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'dsaDone', this.checked)" />
            </div>
            <div class="jp-pillar-body">
              <div class="jp-field-group">
                <label class="jp-field-label">Hours Logged</label>
                <input type="number" step="0.5" class="jp-field-input" placeholder="e.g. 2.0" value="${log.dsaHours || ''}" onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'dsaHours', this.value)" />
              </div>
              <div class="jp-field-group">
                <label class="jp-field-label">Problems Solved</label>
                <textarea class="jp-field-input" rows="2" placeholder="e.g. Kadane's algorithm, Sort Colors, Dutch National Flag" onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'dsaTopics', this.value)">${escapeHtml(log.dsaTopics || '')}</textarea>
              </div>
            </div>
          </div>

          <!-- PILLAR 3: CORE CS -->
          <div class="jp-pillar-card" style="border-top: 3px solid #10b981;">
            <div class="jp-pillar-header">
              <div>
                <div class="jp-pillar-badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">TARGET: 1 HOUR</div>
                <h4 class="jp-pillar-title">📚 Core CS / Interview</h4>
              </div>
              <input type="checkbox" class="jp-checkbox" ${log.coreDone ? 'checked' : ''} onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'coreDone', this.checked)" />
            </div>
            <div class="jp-pillar-body">
              <div class="jp-field-group">
                <label class="jp-field-label">Hours Logged</label>
                <input type="number" step="0.5" class="jp-field-input" placeholder="e.g. 1.0" value="${log.coreHours || ''}" onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'coreHours', this.value)" />
              </div>
              <div class="jp-field-group">
                <label class="jp-field-label">Core Concepts Revised</label>
                <textarea class="jp-field-input" rows="2" placeholder="e.g. OOPS virtual functions & vtable, DBMS 3NF" onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'coreTopics', this.value)">${escapeHtml(log.coreTopics || '')}</textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- DAILY NOTES / REFLECTIONS -->
        <div class="jp-section-card" style="margin-top: 1.25rem;">
          <h4 class="jp-card-title">Daily Reflection & Tricky Mistakes (${currentDate})</h4>
          <p class="jp-card-sub" style="margin-bottom: 0.75rem;">What did you struggle with today? What needs revision tomorrow?</p>
          <textarea class="jp-field-input" rows="3" placeholder="Write mistakes, silly errors, or tomorrow's first priority topic..." onchange="window.jobPrepController.updateDailyLog('${currentDate}', 'notes', this.value)">${escapeHtml(log.notes || '')}</textarea>
        </div>

        <!-- RECENT STUDY LOGS HISTORY TABLE -->
        ${loggedDates.length > 0 ? `
          <div class="jp-section-card" style="margin-top: 1.25rem;">
            <h4 class="jp-card-title" style="margin-bottom: 0.25rem;">Study Logs History (Date-Wise)</h4>
            <p class="jp-card-sub" style="margin-bottom: 1rem;">Persistent record of logged preparation days.</p>
            <div class="jp-table-wrapper">
              <table class="jp-data-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Aptitude (2h)</th>
                    <th>DSA (2h)</th>
                    <th>Core (1h)</th>
                    <th>Total Hours</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  ${loggedDates.map(dateKey => {
                    const dLog = s.dailyLogs[dateKey] || {};
                    const aH = parseFloat(dLog.aptitudeHours) || 0;
                    const dH = parseFloat(dLog.dsaHours) || 0;
                    const cH = parseFloat(dLog.coreHours) || 0;
                    const tot = Math.round((aH + dH + cH) * 10) / 10;
                    return `
                      <tr>
                        <td><strong>${dateKey}</strong></td>
                        <td>${aH}h ${dLog.aptitudeDone ? '✅' : ''}</td>
                        <td>${dH}h ${dLog.dsaDone ? '✅' : ''}</td>
                        <td>${cH}h ${dLog.coreDone ? '✅' : ''}</td>
                        <td><strong>${tot}h</strong></td>
                        <td>
                          <span class="jp-status-pill ${tot >= 5 ? 'status-completed' : 'status-in-progress'}">
                            ${tot >= 5 ? 'Target Met' : 'Partial'}
                          </span>
                        </td>
                        <td>
                          <button class="jp-btn-icon" title="View / Edit Date" onclick="window.jobPrepController.setDailyDate('${dateKey}')">✏️</button>
                        </td>
                      </tr>
                    `;
                  }).join('')}
                </tbody>
              </table>
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }

  /* --- CONTROLLER ACTIONS --- */
  window.jobPrepController = {
    setTab: function (tab) {
      if (!window.jobPrepState) initJobPrepState();
      window.jobPrepState.activeTab = tab;
      saveJobPrepState();
      renderJobPrepView();
    },

    setFilter: function (filter) {
      if (!window.jobPrepState) initJobPrepState();
      window.jobPrepState.filter = filter;
      saveJobPrepState();
      renderJobPrepView();
    },

    setSearch: function (query) {
      if (!window.jobPrepState) initJobPrepState();
      window.jobPrepState.searchQuery = query;
      saveJobPrepState();
      renderJobPrepView();
    },

    jumpToTab: function (tab, elementId) {
      this.setTab(tab);
      if (elementId) {
        setTimeout(() => {
          const el = document.getElementById(elementId) || document.getElementById(`prob-${elementId}`) || document.getElementById(`topic-${elementId}`) || document.getElementById(`tech-${elementId}`);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            el.classList.add('jp-highlight-pulse');
            setTimeout(() => el.classList.remove('jp-highlight-pulse'), 2500);
          }
        }, 150);
      }
    },

    // Eligibility updates
    updateEligibilityStatus: function (id, status) {
      if (!window.jobPrepState.eligibility) window.jobPrepState.eligibility = {};
      if (!window.jobPrepState.eligibility[id]) window.jobPrepState.eligibility[id] = {};
      window.jobPrepState.eligibility[id].status = status;
      saveJobPrepState();
      renderJobPrepView();
    },

    updateEligibilityField: function (id, field, value) {
      if (!window.jobPrepState.eligibility) window.jobPrepState.eligibility = {};
      if (!window.jobPrepState.eligibility[id]) window.jobPrepState.eligibility[id] = {};
      window.jobPrepState.eligibility[id][field] = value;
      saveJobPrepState();
    },

    // Pipeline
    togglePipelineCheck: function (id, checked) {
      if (!window.jobPrepState.pipeline) window.jobPrepState.pipeline = { checks: {}, notes: {} };
      window.jobPrepState.pipeline.checks[id] = checked;
      saveJobPrepState();
      renderJobPrepView();
    },

    // Chips (Quants, Verbal, Reasoning)
    toggleChip: function (section, topicId, chipKey) {
      if (!window.jobPrepState[section]) window.jobPrepState[section] = {};
      if (!window.jobPrepState[section][topicId]) window.jobPrepState[section][topicId] = {};
      const current = !!window.jobPrepState[section][topicId][chipKey];
      window.jobPrepState[section][topicId][chipKey] = !current;
      saveJobPrepState();
      renderJobPrepView();
    },

    // DSA problem updates
    updateDsaStatus: function (problemId, status) {
      if (!window.jobPrepState.dsa) window.jobPrepState.dsa = {};
      if (!window.jobPrepState.dsa[problemId]) window.jobPrepState.dsa[problemId] = {};
      window.jobPrepState.dsa[problemId].status = status;
      window.jobPrepState.dsa[problemId].lastPracticed = getTodayDateString();
      saveJobPrepState();
      renderJobPrepView();
    },

    updateDsaMinutes: function (problemId, minutes) {
      if (!window.jobPrepState.dsa) window.jobPrepState.dsa = {};
      if (!window.jobPrepState.dsa[problemId]) window.jobPrepState.dsa[problemId] = {};
      window.jobPrepState.dsa[problemId].minutes = parseInt(minutes, 10) || 0;
      saveJobPrepState();
    },

    toggleDsaAssignment: function (weekNumber, checked) {
      if (!window.jobPrepState.dsaAssignments) window.jobPrepState.dsaAssignments = {};
      if (!window.jobPrepState.dsaAssignments[weekNumber]) window.jobPrepState.dsaAssignments[weekNumber] = {};
      window.jobPrepState.dsaAssignments[weekNumber].done = checked;
      saveJobPrepState();
      renderJobPrepView();
    },

    // Technical interview updates
    updateTechStatus: function (subjId, status) {
      if (!window.jobPrepState.technical) window.jobPrepState.technical = {};
      if (!window.jobPrepState.technical[subjId]) window.jobPrepState.technical[subjId] = {};
      window.jobPrepState.technical[subjId].status = status;
      saveJobPrepState();
      renderJobPrepView();
    },

    setTechConfidence: function (subjId, star) {
      if (!window.jobPrepState.technical) window.jobPrepState.technical = {};
      if (!window.jobPrepState.technical[subjId]) window.jobPrepState.technical[subjId] = {};
      window.jobPrepState.technical[subjId].confidence = star;
      saveJobPrepState();
      renderJobPrepView();
    },

    toggleTechSubtopic: function (subjId, idx, checked) {
      if (!window.jobPrepState.technical) window.jobPrepState.technical = {};
      if (!window.jobPrepState.technical[subjId]) window.jobPrepState.technical[subjId] = {};
      if (!window.jobPrepState.technical[subjId].subDone) window.jobPrepState.technical[subjId].subDone = {};
      window.jobPrepState.technical[subjId].subDone[idx] = checked;
      saveJobPrepState();
      renderJobPrepView();
    },

    addCustomTechSubtopic: function (subjId) {
      const input = document.getElementById(`inputCustomSub_${subjId}`);
      if (!input || !input.value.trim()) return;
      const text = input.value.trim();

      if (!window.jobPrepState.technical) window.jobPrepState.technical = {};
      if (!window.jobPrepState.technical[subjId]) window.jobPrepState.technical[subjId] = {};
      if (!Array.isArray(window.jobPrepState.technical[subjId].customSubtopics)) {
        window.jobPrepState.technical[subjId].customSubtopics = [];
      }
      window.jobPrepState.technical[subjId].customSubtopics.push({ text, done: false });
      input.value = '';
      saveJobPrepState();
      renderJobPrepView();
    },

    toggleCustomTechSubtopic: function (subjId, cIdx, checked) {
      if (window.jobPrepState.technical?.[subjId]?.customSubtopics?.[cIdx]) {
        window.jobPrepState.technical[subjId].customSubtopics[cIdx].done = checked;
        saveJobPrepState();
        renderJobPrepView();
      }
    },

    removeCustomTechSubtopic: function (subjId, cIdx) {
      if (window.jobPrepState.technical?.[subjId]?.customSubtopics) {
        window.jobPrepState.technical[subjId].customSubtopics.splice(cIdx, 1);
        saveJobPrepState();
        renderJobPrepView();
      }
    },

    // Daily study updates
    setDailyDate: function (dateStr) {
      if (!window.jobPrepState) initJobPrepState();
      window.jobPrepState.currentStudyDate = dateStr;
      saveJobPrepState();
      renderJobPrepView();
    },

    stepDailyDate: function (days) {
      const current = window.jobPrepState.currentStudyDate || getTodayDateString();
      const parts = current.split('-').map(Number);
      const d = new Date(parts[0], parts[1] - 1, parts[2]);
      d.setDate(d.getDate() + days);

      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      this.setDailyDate(`${year}-${month}-${day}`);
    },

    updateDailyLog: function (dateKey, field, value) {
      if (!window.jobPrepState.dailyLogs) window.jobPrepState.dailyLogs = {};
      if (!window.jobPrepState.dailyLogs[dateKey]) window.jobPrepState.dailyLogs[dateKey] = {};
      window.jobPrepState.dailyLogs[dateKey][field] = value;
      saveJobPrepState();
      renderJobPrepView();
    },

    // Notes modal
    activeNotesContext: null,
    openNotesModal: function (section, id, title) {
      this.activeNotesContext = { section, id, title };
      const modal = document.getElementById('jpNotesModal');
      const titleEl = document.getElementById('jpNotesModalTitle');
      const subEl = document.getElementById('jpNotesModalSub');
      const textarea = document.getElementById('jpNotesTextarea');

      if (!modal || !textarea) return;

      titleEl.textContent = `Notes: ${title}`;
      subEl.textContent = `Section: ${section.toUpperCase()} · Key tricks, time/space complexity, and mistakes`;

      let existing = '';
      if (window.jobPrepState[section]?.[id]?.notes) {
        existing = window.jobPrepState[section][id].notes;
      }
      textarea.value = existing;
      modal.style.display = 'flex';
      textarea.focus();
    },

    closeNotesModal: function () {
      const modal = document.getElementById('jpNotesModal');
      if (modal) modal.style.display = 'none';
      this.activeNotesContext = null;
    },

    saveNotesModal: function () {
      if (!this.activeNotesContext) return;
      const { section, id } = this.activeNotesContext;
      const textarea = document.getElementById('jpNotesTextarea');
      const noteText = textarea ? textarea.value : '';

      if (!window.jobPrepState[section]) window.jobPrepState[section] = {};
      if (!window.jobPrepState[section][id]) window.jobPrepState[section][id] = {};
      window.jobPrepState[section][id].notes = noteText;

      saveJobPrepState();
      this.closeNotesModal();
      renderJobPrepView();
    }
  };

  // Helper escape functions
  function escapeHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function escapeJs(str) {
    if (!str) return '';
    return String(str).replace(/'/g, "\\'").replace(/"/g, '\\"');
  }

  // Export renderer to window
  window.renderJobPrepView = renderJobPrepView;
  window.initJobPrepState = initJobPrepState;
  window.updateJobPrepSidebarBadge = updateJobPrepSidebarBadge;
  window.calculateJobPrepMetrics = calculateJobPrepMetrics;
  window.getTodayDateString = getTodayDateString;

  // Initialize on DOMContentLoaded or immediate if loaded later
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initJobPrepState();
      updateJobPrepSidebarBadge();
    });
  } else {
    initJobPrepState();
    updateJobPrepSidebarBadge();
  }
})();
