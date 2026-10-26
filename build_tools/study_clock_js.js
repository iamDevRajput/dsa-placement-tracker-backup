/* ==========================================================================
   STUDY CLOCK & TIME TRACKER — PRECISION JAVASCRIPT ENGINE
   ========================================================================== */

const STORAGE_STUDY_CLOCK_SESSION_KEY = 'study_clock_active_session_v1';
const STORAGE_STUDY_CLOCK_HISTORY_KEY = 'study_clock_sessions_v1';

let studyClockActiveSession = {
  status: 'stopped', // 'running' | 'paused' | 'stopped'
  startedAt: null,
  lastSegmentStart: null,
  accumulatedMs: 0,
  category: 'DSA',
  notes: ''
};

let studyClockHistory = {
  version: 1,
  sessions: []
};

let studyClockTickerInterval = null;
let currentStudyHistoryCatFilter = 'all';
let currentStudyHistorySearch = '';

/* --- INITIALIZATION & RECOVERY --- */
function initStudyClockEngine() {
  // 1. Load history
  try {
    const rawHist = localStorage.getItem(STORAGE_STUDY_CLOCK_HISTORY_KEY);
    if (rawHist) {
      const parsed = JSON.parse(rawHist);
      if (parsed && Array.isArray(parsed.sessions)) {
        studyClockHistory = parsed;
      }
    }
  } catch (err) {
    console.error('Failed to parse studyClockHistory:', err);
  }

  // 2. Load active session
  try {
    const rawSession = localStorage.getItem(STORAGE_STUDY_CLOCK_SESSION_KEY);
    if (rawSession) {
      const parsed = JSON.parse(rawSession);
      if (parsed && typeof parsed === 'object') {
        studyClockActiveSession = {
          status: parsed.status || 'stopped',
          startedAt: parsed.startedAt || null,
          lastSegmentStart: parsed.lastSegmentStart || null,
          accumulatedMs: Number(parsed.accumulatedMs) || 0,
          category: parsed.category || 'DSA',
          notes: parsed.notes || ''
        };
      }
    }
  } catch (err) {
    console.error('Failed to parse studyClockActiveSession:', err);
  }

  // 3. Restore running state if session was actively running before refresh
  if (studyClockActiveSession.status === 'running') {
    startStudyClockTicker();
  }

  // 4. Update Header and Sidebar badges immediately
  updateStudyClockUI();
  updateStudyClockHeaderAndBadges();
}

function saveStudyClockActiveSession() {
  try {
    localStorage.setItem(STORAGE_STUDY_CLOCK_SESSION_KEY, JSON.stringify(studyClockActiveSession));
  } catch (e) {
    console.error('Failed to save studyClockActiveSession:', e);
  }
}

function saveStudyClockHistory() {
  try {
    localStorage.setItem(STORAGE_STUDY_CLOCK_HISTORY_KEY, JSON.stringify(studyClockHistory));
  } catch (e) {
    console.error('Failed to save studyClockHistory:', e);
  }
}

/* --- LIVE ELAPSED CALCULATION (TIMESTAMP-DRIVEN) --- */
function getStudyClockElapsedMs() {
  let elapsed = studyClockActiveSession.accumulatedMs || 0;
  if (studyClockActiveSession.status === 'running' && studyClockActiveSession.lastSegmentStart) {
    const segment = Date.now() - studyClockActiveSession.lastSegmentStart;
    elapsed += Math.max(0, segment);
  }
  return elapsed;
}

function formatDurationHms(totalSec) {
  const s = Math.max(0, Math.floor(totalSec));
  const hrs = Math.floor(s / 3600);
  const mins = Math.floor((s % 3600) / 60);
  const secs = s % 60;
  return `${String(hrs).padStart(2, '0')}:${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

function formatDurationHuman(totalSec) {
  const s = Math.max(0, Math.floor(totalSec));
  const hrs = Math.floor(s / 3600);
  const mins = Math.floor((s % 3600) / 60);
  if (hrs > 0) return `${hrs}h ${String(mins).padStart(2, '0')}m`;
  return `${mins}m`;
}

/* --- TICKER & UI UPDATES --- */
function startStudyClockTicker() {
  if (studyClockTickerInterval) clearInterval(studyClockTickerInterval);
  studyClockTickerInterval = setInterval(() => {
    updateStudyClockUI();
    updateStudyClockHeaderAndBadges();
  }, 250);
}

function stopStudyClockTicker() {
  if (studyClockTickerInterval) {
    clearInterval(studyClockTickerInterval);
    studyClockTickerInterval = null;
  }
}

function updateStudyClockUI() {
  const elapsedMs = getStudyClockElapsedMs();
  const elapsedSec = Math.floor(elapsedMs / 1000);
  const timeFormatted = formatDurationHms(elapsedSec);

  // 1. Giant Digits
  const digitsEl = document.getElementById('scClockDigits');
  if (digitsEl) digitsEl.textContent = timeFormatted;

  // 2. Card styling & Status Pill
  const clockCard = document.getElementById('scClockCard');
  const statusPill = document.getElementById('scStatusPill');
  const statusText = document.getElementById('scStatusText');

  const status = studyClockActiveSession.status;
  if (clockCard) {
    clockCard.classList.remove('running', 'paused', 'stopped');
    clockCard.classList.add(status);
  }
  if (statusPill) {
    statusPill.classList.remove('running', 'paused', 'stopped');
    statusPill.classList.add(status);
  }
  if (statusText) {
    if (status === 'running') statusText.textContent = 'Live Session In Progress';
    else if (status === 'paused') statusText.textContent = 'Session Paused';
    else statusText.textContent = 'Ready to Focus';
  }

  // 3. Meta start time display
  const startMetaEl = document.getElementById('scSessionStartTimeDisplay');
  if (startMetaEl) {
    if (status === 'stopped' || !studyClockActiveSession.startedAt) {
      startMetaEl.textContent = 'Session idle';
    } else {
      const d = new Date(studyClockActiveSession.startedAt);
      const timeStr = d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      startMetaEl.textContent = `Started at ${timeStr}`;
    }
  }

  // 4. Control buttons display
  const btnStart = document.getElementById('scBtnStart');
  const btnPause = document.getElementById('scBtnPause');
  const btnResume = document.getElementById('scBtnResume');
  const btnStop = document.getElementById('scBtnStop');

  if (btnStart && btnPause && btnResume && btnStop) {
    if (status === 'stopped') {
      btnStart.style.display = 'inline-flex';
      btnPause.style.display = 'none';
      btnResume.style.display = 'none';
      btnStop.style.display = 'none';
    } else if (status === 'running') {
      btnStart.style.display = 'none';
      btnPause.style.display = 'inline-flex';
      btnResume.style.display = 'none';
      btnStop.style.display = 'inline-flex';
    } else if (status === 'paused') {
      btnStart.style.display = 'none';
      btnPause.style.display = 'none';
      btnResume.style.display = 'inline-flex';
      btnStop.style.display = 'inline-flex';
    }
  }

  // 5. Config inputs sync (Category & Notes)
  const catSel = document.getElementById('scCategorySelect');
  if (catSel && studyClockActiveSession.category && catSel.value !== studyClockActiveSession.category) {
    catSel.value = studyClockActiveSession.category;
  }
  const notesInput = document.getElementById('scSessionNotesInput');
  if (notesInput && document.activeElement !== notesInput) {
    notesInput.value = studyClockActiveSession.notes || '';
  }
}

function updateStudyClockHeaderAndBadges() {
  const elapsedMs = getStudyClockElapsedMs();
  const elapsedSec = Math.floor(elapsedMs / 1000);
  const timeFormatted = formatDurationHms(elapsedSec);

  // 1. Top Header Timer Widget
  const hdrTimerDisplay = document.getElementById('hdr-timer-display');
  const hdrTimerBtnIcon = document.getElementById('hdr-timer-btn-icon');
  if (hdrTimerDisplay) {
    hdrTimerDisplay.textContent = timeFormatted;
  }
  if (hdrTimerBtnIcon) {
    if (studyClockActiveSession.status === 'running') hdrTimerBtnIcon.textContent = '❚❚';
    else hdrTimerBtnIcon.textContent = '▶';
  }

  // 2. Today's Accumulated Study Time (including currently ticking session)
  const todayKey = getTodayKey();
  const completedTodaySec = studyClockHistory.sessions
    .filter(s => s.date === todayKey)
    .reduce((acc, s) => acc + (Number(s.durationSeconds) || 0), 0);

  const activeRunningSec = (studyClockActiveSession.status !== 'stopped') ? elapsedSec : 0;
  const totalTodaySec = completedTodaySec + activeRunningSec;

  const todayDisplayStr = formatDurationHuman(totalTodaySec);

  // Header pill
  const hdrStudyPill = document.getElementById('hdr-study');
  if (hdrStudyPill) hdrStudyPill.textContent = todayDisplayStr;

  // Study clock sub-display
  const scTodayAccum = document.getElementById('scTodayAccumulatedDisplay');
  if (scTodayAccum) scTodayAccum.textContent = `Today: ${todayDisplayStr}`;

  // Sidebar badge
  const sbBadge = document.getElementById('nav-studyclock-badge');
  if (sbBadge) sbBadge.textContent = todayDisplayStr;

  // Also sync to legacy planner widget if visible
  const focusTodayEl = document.getElementById('pwFocusTimerToday');
  if (focusTodayEl) focusTodayEl.textContent = todayDisplayStr;
}

/* --- CLOCK CONTROL ACTIONS --- */
function startStudyClock() {
  const catSel = document.getElementById('scCategorySelect');
  const notesInput = document.getElementById('scSessionNotesInput');

  studyClockActiveSession.status = 'running';
  studyClockActiveSession.startedAt = Date.now();
  studyClockActiveSession.lastSegmentStart = Date.now();
  studyClockActiveSession.accumulatedMs = 0;
  studyClockActiveSession.category = catSel ? catSel.value : 'DSA';
  studyClockActiveSession.notes = notesInput ? notesInput.value.trim() : '';

  saveStudyClockActiveSession();
  startStudyClockTicker();
  updateStudyClockUI();
  updateStudyClockHeaderAndBadges();

  if (typeof showToast === 'function') {
    showToast(`Study clock started for ${studyClockActiveSession.category} ⏱️`);
  }
}

function pauseStudyClock() {
  if (studyClockActiveSession.status !== 'running') return;

  const now = Date.now();
  if (studyClockActiveSession.lastSegmentStart) {
    studyClockActiveSession.accumulatedMs += Math.max(0, now - studyClockActiveSession.lastSegmentStart);
  }
  studyClockActiveSession.status = 'paused';
  studyClockActiveSession.lastSegmentStart = null;

  saveStudyClockActiveSession();
  stopStudyClockTicker();
  updateStudyClockUI();
  updateStudyClockHeaderAndBadges();

  if (typeof showToast === 'function') {
    showToast('Study clock paused ❚❚');
  }
}

function resumeStudyClock() {
  if (studyClockActiveSession.status !== 'paused') return;

  studyClockActiveSession.status = 'running';
  studyClockActiveSession.lastSegmentStart = Date.now();

  saveStudyClockActiveSession();
  startStudyClockTicker();
  updateStudyClockUI();
  updateStudyClockHeaderAndBadges();

  if (typeof showToast === 'function') {
    showToast('Study clock resumed ▶');
  }
}

function stopAndLogStudySession() {
  const elapsedMs = getStudyClockElapsedMs();
  const elapsedSec = Math.floor(elapsedMs / 1000);

  if (elapsedSec < 10) {
    if (!confirm('Session duration is under 10 seconds. Stop without logging?')) {
      return;
    }
    // Discard short accident
    resetActiveSessionState();
    return;
  }

  const startDateObj = studyClockActiveSession.startedAt ? new Date(studyClockActiveSession.startedAt) : new Date(Date.now() - elapsedMs);
  const endDateObj = new Date();

  const newSession = {
    id: 'sc_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6),
    date: dateKeyFromDate(startDateObj),
    startTime: startDateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    endTime: endDateObj.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    startTimestamp: startDateObj.getTime(),
    endTimestamp: endDateObj.getTime(),
    durationSeconds: elapsedSec,
    durationFormatted: formatDurationHms(elapsedSec),
    category: studyClockActiveSession.category || 'DSA',
    notes: studyClockActiveSession.notes || ''
  };

  studyClockHistory.sessions.unshift(newSession);
  saveStudyClockHistory();

  // Also bridge into studyState.days so existing heatmap/calendar reflects it
  try {
    const dKey = newSession.date;
    if (!studyState.days[dKey]) studyState.days[dKey] = { totalSeconds: 0 };
    studyState.days[dKey].totalSeconds += elapsedSec;
    localStorage.setItem(STORAGE_STUDY_KEY, JSON.stringify(studyState));
  } catch (err) {
    console.warn('Bridge to studyState failed:', err);
  }

  // Reset active session
  resetActiveSessionState();

  // Re-render UI
  renderStudyClockView();

  if (typeof showToast === 'function') {
    showToast(`Study session saved: ${formatDurationHuman(elapsedSec)} logged ✓`);
  }
}

function resetActiveSessionState() {
  stopStudyClockTicker();
  studyClockActiveSession = {
    status: 'stopped',
    startedAt: null,
    lastSegmentStart: null,
    accumulatedMs: 0,
    category: studyClockActiveSession.category || 'DSA',
    notes: ''
  };
  saveStudyClockActiveSession();
  updateStudyClockUI();
  updateStudyClockHeaderAndBadges();
}

function toggleStudyClockFromHeader() {
  if (studyClockActiveSession.status === 'running') {
    pauseStudyClock();
  } else if (studyClockActiveSession.status === 'paused') {
    resumeStudyClock();
  } else {
    // If stopped, start
    startStudyClock();
  }
}

function onStudyCategoryChange(cat) {
  studyClockActiveSession.category = cat;
  saveStudyClockActiveSession();
}

function onStudyNotesInput(notes) {
  studyClockActiveSession.notes = notes;
  saveStudyClockActiveSession();
}

/* --- ANALYTICS & AGGREGATIONS --- */
function calculateStudyClockMetrics() {
  const todayKey = getTodayKey();
  const sessions = studyClockHistory.sessions;

  // 1. Today
  const todaySessions = sessions.filter(s => s.date === todayKey);
  const todaySec = todaySessions.reduce((acc, s) => acc + (Number(s.durationSeconds) || 0), 0);

  // 2. Week (last 7 days)
  const now = new Date();
  const weekStart = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 6);
  const weekKeyMin = dateKeyFromDate(weekStart);
  const weekSessions = sessions.filter(s => s.date >= weekKeyMin && s.date <= todayKey);
  const weekSec = weekSessions.reduce((acc, s) => acc + (Number(s.durationSeconds) || 0), 0);
  const weekDailyAvgSec = Math.round(weekSec / 7);

  // 3. Month (current calendar month)
  const monthPrefix = todayKey.substring(0, 7); // YYYY-MM
  const monthSessions = sessions.filter(s => s.date.startsWith(monthPrefix));
  const monthSec = monthSessions.reduce((acc, s) => acc + (Number(s.durationSeconds) || 0), 0);

  // 4. All-time
  const allTimeSec = sessions.reduce((acc, s) => acc + (Number(s.durationSeconds) || 0), 0);

  // 5. Category breakdown
  const categoryTotals = {
    'DSA': 0,
    'Core Subjects': 0,
    'Development': 0,
    'Aptitude': 0,
    'System Design': 0,
    'Mock Interview': 0,
    'Other': 0
  };

  sessions.forEach(s => {
    const c = s.category || 'Other';
    const dur = Number(s.durationSeconds) || 0;
    if (categoryTotals.hasOwnProperty(c)) {
      categoryTotals[c] += dur;
    } else {
      categoryTotals['Other'] += dur;
    }
  });

  return {
    todaySec,
    todayCount: todaySessions.length,
    weekSec,
    weekDailyAvgSec,
    monthSec,
    monthCount: monthSessions.length,
    allTimeSec,
    allTimeCount: sessions.length,
    categoryTotals
  };
}

/* --- RENDER VIEW --- */
function renderStudyClockView() {
  updateStudyClockUI();
  updateStudyClockHeaderAndBadges();

  const metrics = calculateStudyClockMetrics();

  // Metrics cards
  const elTodayH = document.getElementById('scStatTodayHours');
  const elTodaySub = document.getElementById('scStatTodaySessions');
  const elWeekH = document.getElementById('scStatWeekHours');
  const elWeekAvg = document.getElementById('scStatWeekAvg');
  const elMonthH = document.getElementById('scStatMonthHours');
  const elMonthSub = document.getElementById('scStatMonthSessions');
  const elAllH = document.getElementById('scStatAllTimeHours');
  const elAllSub = document.getElementById('scStatAllTimeSessions');

  if (elTodayH) elTodayH.textContent = formatDurationHuman(metrics.todaySec);
  if (elTodaySub) elTodaySub.textContent = `${metrics.todayCount} completed session${metrics.todayCount === 1 ? '' : 's'}`;

  if (elWeekH) elWeekH.textContent = formatDurationHuman(metrics.weekSec);
  if (elWeekAvg) elWeekAvg.textContent = `Daily avg: ${formatDurationHuman(metrics.weekDailyAvgSec)}`;

  if (elMonthH) elMonthH.textContent = formatDurationHuman(metrics.monthSec);
  if (elMonthSub) elMonthSub.textContent = `${metrics.monthCount} monthly session${metrics.monthCount === 1 ? '' : 's'}`;

  if (elAllH) elAllH.textContent = formatDurationHuman(metrics.allTimeSec);
  if (elAllSub) elAllSub.textContent = `${metrics.allTimeCount} total session${metrics.allTimeCount === 1 ? '' : 's'}`;

  // Category bars
  renderCategoryBars(metrics.categoryTotals, metrics.allTimeSec);

  // History table
  renderStudySessionsTable();
}

function renderCategoryBars(catTotals, allTimeSec) {
  const container = document.getElementById('scCategoryBarsContainer');
  if (!container) return;

  const catMeta = [
    { key: 'DSA', name: 'DSA & Algorithms', badgeClass: 'cat-badge-dsa', fillClass: 'cat-fill-dsa' },
    { key: 'Core Subjects', name: 'Core CS (OS/DBMS/CN)', badgeClass: 'cat-badge-core', fillClass: 'cat-fill-core' },
    { key: 'Development', name: 'Development & Projects', badgeClass: 'cat-badge-dev', fillClass: 'cat-fill-dev' },
    { key: 'Aptitude', name: 'Aptitude & Quant', badgeClass: 'cat-badge-aptitude', fillClass: 'cat-fill-aptitude' },
    { key: 'System Design', name: 'System Design', badgeClass: 'cat-badge-sysdesign', fillClass: 'cat-fill-sysdesign' },
    { key: 'Mock Interview', name: 'Mock Interviews', badgeClass: 'cat-badge-interview', fillClass: 'cat-fill-interview' },
    { key: 'Other', name: 'Other Learning', badgeClass: 'cat-badge-other', fillClass: 'cat-fill-other' }
  ];

  let html = '';
  catMeta.forEach(cat => {
    const sec = catTotals[cat.key] || 0;
    const pct = allTimeSec > 0 ? Math.round((sec / allTimeSec) * 100) : 0;
    const timeStr = formatDurationHuman(sec);

    html += `
      <div class="sc-cat-bar-item">
        <div class="sc-cat-bar-header">
          <span class="sc-cat-bar-name">
            <span class="sc-cat-bar-badge ${cat.badgeClass}">${cat.key}</span>
            <span>${cat.name}</span>
          </span>
          <span class="sc-cat-bar-time">${timeStr} (${pct}%)</span>
        </div>
        <div class="sc-cat-progress-track">
          <div class="sc-cat-progress-fill ${cat.fillClass}" style="width:${pct}%;"></div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function renderStudySessionsTable() {
  const tbody = document.getElementById('scSessionsTableBody');
  if (!tbody) return;

  let filtered = [...studyClockHistory.sessions];

  // 1. Category Filter
  if (currentStudyHistoryCatFilter !== 'all') {
    filtered = filtered.filter(s => s.category === currentStudyHistoryCatFilter);
  }

  // 2. Search Filter
  if (currentStudyHistorySearch) {
    const q = currentStudyHistorySearch.toLowerCase().trim();
    filtered = filtered.filter(s => {
      const notesMatch = (s.notes || '').toLowerCase().includes(q);
      const catMatch = (s.category || '').toLowerCase().includes(q);
      const dateMatch = (s.date || '').toLowerCase().includes(q);
      return notesMatch || catMatch || dateMatch;
    });
  }

  if (filtered.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="5" class="sc-empty-state">
          <div class="sc-empty-icon">⏱️</div>
          <div>No study sessions found matching current filters.</div>
          <div style="font-size:0.75rem; color:#64748b; margin-top:0.3rem;">Start the study clock or log a past session to track your placement prep.</div>
        </td>
      </tr>
    `;
    return;
  }

  const catBadgeMap = {
    'DSA': 'cat-badge-dsa',
    'Core Subjects': 'cat-badge-core',
    'Development': 'cat-badge-dev',
    'Aptitude': 'cat-badge-aptitude',
    'System Design': 'cat-badge-sysdesign',
    'Mock Interview': 'cat-badge-interview',
    'Other': 'cat-badge-other'
  };

  let html = '';
  filtered.forEach(session => {
    const dateFormatted = formatDateDisplay(session.date);
    const badgeClass = catBadgeMap[session.category] || 'cat-badge-other';
    const notesText = session.notes && session.notes.trim() ? escapeHtml(session.notes.trim()) : '<span style="color:#64748b; font-style:italic;">No notes logged</span>';

    html += `
      <tr>
        <td>
          <div style="font-weight:600; color:#f8fafc;">${dateFormatted}</div>
          <div style="font-size:0.75rem; color:var(--text-muted,#94a3b8); font-family:var(--font-mono);">${session.startTime || ''} – ${session.endTime || ''}</div>
        </td>
        <td>
          <span class="sc-cat-bar-badge ${badgeClass}">${session.category}</span>
        </td>
        <td>
          <div class="sc-row-time">${formatDurationHuman(session.durationSeconds)}</div>
          <div style="font-size:0.72rem; color:#64748b; font-family:var(--font-mono);">${session.durationFormatted || ''}</div>
        </td>
        <td style="max-width: 380px;">
          <div style="font-size:0.83rem; line-height:1.4;">${notesText}</div>
        </td>
        <td>
          <div class="sc-row-actions">
            <button type="button" class="sc-row-btn" onclick="openEditStudySessionModal('${session.id}')" title="Edit Session">✏️ Edit</button>
            <button type="button" class="sc-row-btn delete" onclick="confirmDeleteStudySession('${session.id}')" title="Delete Session">🗑️</button>
          </div>
        </td>
      </tr>
    `;
  });

  tbody.innerHTML = html;
}

function setStudyHistoryCatFilter(cat, btn) {
  currentStudyHistoryCatFilter = cat;
  document.querySelectorAll('.sc-filter-pill').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderStudySessionsTable();
}

function onStudyHistorySearch(query) {
  currentStudyHistorySearch = query;
  renderStudySessionsTable();
}

/* --- MANUAL ENTRY & EDIT MODALS --- */
function openManualStudyModal() {
  const dateInput = document.getElementById('scManualDate');
  const timeInput = document.getElementById('scManualStartTime');
  const durInput = document.getElementById('scManualDurationMinutes');
  const notesInput = document.getElementById('scManualNotes');

  if (dateInput) dateInput.value = getTodayKey();
  if (timeInput) {
    const d = new Date();
    timeInput.value = `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
  }
  if (durInput) durInput.value = '60';
  if (notesInput) notesInput.value = '';

  const modal = document.getElementById('modalManualStudySession');
  if (modal) modal.classList.add('active');
}

function submitManualStudySession() {
  const dateVal = document.getElementById('scManualDate')?.value || getTodayKey();
  const startTimeVal = document.getElementById('scManualStartTime')?.value || '12:00';
  const durMinsVal = parseInt(document.getElementById('scManualDurationMinutes')?.value, 10);
  const catVal = document.getElementById('scManualCategory')?.value || 'DSA';
  const notesVal = document.getElementById('scManualNotes')?.value || '';

  if (isNaN(durMinsVal) || durMinsVal <= 0) {
    alert('Please enter a valid duration in minutes.');
    return;
  }

  const durationSeconds = durMinsVal * 60;

  // Calculate end time
  const [sh, sm] = startTimeVal.split(':').map(Number);
  const startDt = new Date();
  startDt.setHours(sh || 0, sm || 0, 0, 0);
  const endDt = new Date(startDt.getTime() + durationSeconds * 1000);

  const formatHhMm = d => d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  const newSession = {
    id: 'sc_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6),
    date: dateVal,
    startTime: formatHhMm(startDt),
    endTime: formatHhMm(endDt),
    startTimestamp: startDt.getTime(),
    endTimestamp: endDt.getTime(),
    durationSeconds: durationSeconds,
    durationFormatted: formatDurationHms(durationSeconds),
    category: catVal,
    notes: notesVal.trim()
  };

  studyClockHistory.sessions.unshift(newSession);
  saveStudyClockHistory();

  // Bridge to studyState
  try {
    if (!studyState.days[dateVal]) studyState.days[dateVal] = { totalSeconds: 0 };
    studyState.days[dateVal].totalSeconds += durationSeconds;
    localStorage.setItem(STORAGE_STUDY_KEY, JSON.stringify(studyState));
  } catch (e) {}

  closeModal('modalManualStudySession');
  renderStudyClockView();

  if (typeof showToast === 'function') {
    showToast(`Manual study session logged (${durMinsVal}m) ✓`);
  }
}

function openEditStudySessionModal(sessionId) {
  const session = studyClockHistory.sessions.find(s => s.id === sessionId);
  if (!session) return;

  const idInput = document.getElementById('scEditSessionId');
  const dateInput = document.getElementById('scEditDate');
  const timeInput = document.getElementById('scEditStartTime');
  const durInput = document.getElementById('scEditDurationMinutes');
  const catInput = document.getElementById('scEditCategory');
  const notesInput = document.getElementById('scEditNotes');

  if (idInput) idInput.value = session.id;
  if (dateInput) dateInput.value = session.date || getTodayKey();
  if (timeInput) timeInput.value = session.startTime || '12:00';
  if (durInput) durInput.value = Math.max(1, Math.round((session.durationSeconds || 60) / 60));
  if (catInput) catInput.value = session.category || 'DSA';
  if (notesInput) notesInput.value = session.notes || '';

  const modal = document.getElementById('modalEditStudySession');
  if (modal) modal.classList.add('active');
}

function submitEditStudySession() {
  const sessionId = document.getElementById('scEditSessionId')?.value;
  const session = studyClockHistory.sessions.find(s => s.id === sessionId);
  if (!session) return;

  const dateVal = document.getElementById('scEditDate')?.value || session.date;
  const startTimeVal = document.getElementById('scEditStartTime')?.value || session.startTime;
  const durMinsVal = parseInt(document.getElementById('scEditDurationMinutes')?.value, 10);
  const catVal = document.getElementById('scEditCategory')?.value || session.category;
  const notesVal = document.getElementById('scEditNotes')?.value || '';

  if (isNaN(durMinsVal) || durMinsVal <= 0) {
    alert('Please enter a valid duration in minutes.');
    return;
  }

  const durationSeconds = durMinsVal * 60;
  session.date = dateVal;
  session.startTime = startTimeVal;
  session.durationSeconds = durationSeconds;
  session.durationFormatted = formatDurationHms(durationSeconds);
  session.category = catVal;
  session.notes = notesVal.trim();

  saveStudyClockHistory();
  closeModal('modalEditStudySession');
  renderStudyClockView();

  if (typeof showToast === 'function') {
    showToast('Study session updated ✓');
  }
}

/* --- DELETE CONFIRMATION & EXECUTION --- */
function confirmDeleteStudySession(sessionId) {
  const inputEl = document.getElementById('scDeleteSessionId');
  if (inputEl) inputEl.value = sessionId;
  const modal = document.getElementById('modalConfirmDeleteStudySession');
  if (modal) modal.classList.add('active');
}

function executeDeleteStudySession() {
  const sessionId = document.getElementById('scDeleteSessionId')?.value;
  if (!sessionId) return;

  const index = studyClockHistory.sessions.findIndex(s => s.id === sessionId);
  if (index !== -1) {
    studyClockHistory.sessions.splice(index, 1);
    saveStudyClockHistory();
  }

  closeModal('modalConfirmDeleteStudySession');
  renderStudyClockView();

  if (typeof showToast === 'function') {
    showToast('Study session deleted');
  }
}

/* --- EXPORT CSV & JSON BACKUP --- */
function exportStudySessionsCSV() {
  const sessions = studyClockHistory.sessions;
  if (sessions.length === 0) {
    alert('No study sessions available to export.');
    return;
  }

  let csv = 'ID,Date,Start Time,End Time,Duration (Seconds),Duration (Formatted),Category,Notes\n';
  sessions.forEach(s => {
    const cleanNotes = (s.notes || '').replace(/"/g, '""');
    csv += `"${s.id}","${s.date}","${s.startTime || ''}","${s.endTime || ''}",${s.durationSeconds || 0},"${s.durationFormatted || ''}","${s.category || ''}","${cleanNotes}"\n`;
  });

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `study_sessions_${getTodayKey()}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  if (typeof showToast === 'function') {
    showToast('Study sessions exported as CSV ✓');
  }
}

function exportStudySessionsJSON() {
  const dataStr = JSON.stringify({
    version: 1,
    exportedAt: new Date().toISOString(),
    sessions: studyClockHistory.sessions
  }, null, 2);

  const blob = new Blob([dataStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `study_clock_backup_${getTodayKey()}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  if (typeof showToast === 'function') {
    showToast('Study Clock JSON backup downloaded ✓');
  }
}

function openStudyClockBackupModal() {
  const modal = document.getElementById('modalExportImportStudyClock');
  if (modal) modal.classList.add('active');
}

function handleStudyClockImportFile() {
  const fileInput = document.getElementById('scImportFileInput');
  if (!fileInput || !fileInput.files || fileInput.files.length === 0) {
    alert('Please choose a valid JSON backup file.');
    return;
  }

  const file = fileInput.files[0];
  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const parsed = JSON.parse(e.target.result);
      if (!parsed || !Array.isArray(parsed.sessions)) {
        alert('Invalid backup file format. Expected a "sessions" array.');
        return;
      }

      // Safe non-destructive merge: preserve existing, add non-duplicate IDs
      let added = 0;
      const existingIds = new Set(studyClockHistory.sessions.map(s => s.id));
      parsed.sessions.forEach(s => {
        if (s && s.id && !existingIds.has(s.id)) {
          studyClockHistory.sessions.push(s);
          existingIds.add(s.id);
          added++;
        }
      });

      // Sort by date descending
      studyClockHistory.sessions.sort((a, b) => (b.date || '').localeCompare(a.date || ''));

      saveStudyClockHistory();
      closeModal('modalExportImportStudyClock');
      renderStudyClockView();

      alert(`Backup restored successfully! Merged ${added} new study sessions.`);
    } catch (err) {
      alert('Error parsing JSON backup file: ' + err.message);
    }
  };
  reader.readAsText(file);
}
