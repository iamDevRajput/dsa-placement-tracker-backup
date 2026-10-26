/* ==========================================================================
   PLACEMENT PRODUCTIVITY WORKSPACE ENGINE (MASTER BUILD V2)
   Offline-first, Zero-dependency, Production-grade Vanilla JS
   ========================================================================== */

// --- 1. LOCAL STORAGE KEYS ---
const WORKSPACE_KEYS = {
  TASKS: 'daily_task_planner_v1',
  LEGACY_TASKS: 'dsa_planner_tasks_v1',
  CODING: 'daily_coding_log_v1',
  ROUTINES: 'daily_routines_v1',
  POTD: 'daily_potd_v1',
  DIARY: 'dsa_diary_entries_v1'
};

// --- 2. GLOBAL WORKSPACE STATE ---
let currentWorkspaceDate = getTodayDateKey();
let currentWorkspaceTab = 'tab-planner';
let plannerTasks = [];
let codingLog = [];
let potdRecords = {};
let routineTemplates = [];

// Reuse existing global diaryState if already declared
if (typeof diaryState === 'undefined' || !diaryState) {
  diaryState = { entries: {} };
}

let taskFilterState = {
  status: 'all',
  category: 'all',
  priority: 'all',
  search: ''
};

let calendarYear = new Date().getFullYear();
let calendarMonth = new Date().getMonth(); // 0-indexed
let globalSearchFilter = 'all';
let isPotdSyncing = false; // Guard to prevent infinite sync loops

// Focus Timer State (prefixed to avoid collision with legacy timer globals)
let pwTimerSecondsLeft = 25 * 60;
let pwTimerRunning = false;
let pwTimerInterval = null;
let pwTimerCurrentMode = 'Pomodoro';
let todayFocusMinutes = 0;

// Debounce timer for diary auto-save
let diarySaveTimeout = null;

// --- 3. HELPER FUNCTIONS ---
function getTodayDateKey() {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

function formatDateDisplay(dateStr) {
  if (!dateStr) return 'Today';
  const parts = dateStr.split('-');
  if (parts.length !== 3) return dateStr;
  const d = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
  const options = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
  return d.toLocaleDateString('en-US', options);
}

function getDayOfWeek(dateStr) {
  const parts = dateStr.split('-');
  const d = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
  return d.getDay(); // 0 = Sun, 1 = Mon, ..., 6 = Sat
}

function showWorkspaceSaveStatus(text, isSaving = false) {
  const badge = document.getElementById('pwGlobalSaveStatus');
  if (!badge) return;
  badge.textContent = text;
  if (isSaving) {
    badge.classList.add('saving');
  } else {
    badge.classList.remove('saving');
  }
}

// Download file helper (used for export)
function downloadWorkspaceFile(content, fileName, contentType) {
  const a = document.createElement('a');
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(a.href);
  }, 100);
}

// --- 4. INITIALIZATION & DATA MIGRATION ---
function initWorkspace() {
  plannerTasks = [];
  codingLog = [];
  potdRecords = {};
  routineTemplates = [];

  // 1. Load Tasks (with non-destructive legacy fallback)
  try {
    const rawTasks = localStorage.getItem(WORKSPACE_KEYS.TASKS);
    if (rawTasks) {
      const parsed = JSON.parse(rawTasks);
      plannerTasks = Array.isArray(parsed) ? parsed : (parsed.tasks || []);
    } else {
      // Check legacy planner tasks
      const legacyRaw = localStorage.getItem(WORKSPACE_KEYS.LEGACY_TASKS);
      if (legacyRaw) {
        const legacyParsed = JSON.parse(legacyRaw);
        const legacyList = Array.isArray(legacyParsed) ? legacyParsed : (legacyParsed.tasks || []);
        if (legacyList.length > 0) {
          plannerTasks = legacyList.map((t, idx) => ({
            id: t.id || 'task_leg_' + Date.now() + '_' + idx,
            date: t.date || getTodayDateKey(),
            title: t.title || t.text || 'Task',
            category: t.category || 'DSA Practice',
            priority: t.priority || 'p2',
            completed: Boolean(t.completed || t.done),
            routineTemplateId: null,
            order: idx,
            createdAt: t.createdAt || new Date().toISOString(),
            completedAt: t.completedAt || null
          }));
          saveTasks();
        }
      }
    }
  } catch (e) {
    console.error('Error loading workspace tasks:', e);
    plannerTasks = [];
  }

  // 2. Load Coding Logs
  try {
    const rawCoding = localStorage.getItem(WORKSPACE_KEYS.CODING);
    if (rawCoding) {
      const parsed = JSON.parse(rawCoding);
      codingLog = Array.isArray(parsed) ? parsed : (parsed.entries || []);
    } else {
      codingLog = [];
    }
  } catch (e) {
    console.error('Error loading coding log:', e);
    codingLog = [];
  }

  // 3. Load POTD records
  try {
    const rawPotd = localStorage.getItem(WORKSPACE_KEYS.POTD);
    potdRecords = rawPotd ? JSON.parse(rawPotd) : {};
  } catch (e) {
    console.error('Error loading POTD records:', e);
    potdRecords = {};
  }

  // 4. Load Routines (initialize default templates if empty)
  try {
    const rawRoutines = localStorage.getItem(WORKSPACE_KEYS.ROUTINES);
    if (rawRoutines) {
      const parsed = JSON.parse(rawRoutines);
      routineTemplates = Array.isArray(parsed) ? parsed : (parsed.routines || []);
    }
    if (!routineTemplates || routineTemplates.length === 0) {
      routineTemplates = [
        {
          id: 'routine_potd',
          title: 'Daily LeetCode POTD',
          category: 'LeetCode POTD',
          priority: 'p1',
          durationMins: 45,
          daysOfWeek: [0, 1, 2, 3, 4, 5, 6], // Daily
          enabled: true
        },
        {
          id: 'routine_dsa',
          title: 'DSA Pattern Practice (2 Problems)',
          category: 'DSA Practice',
          priority: 'p1',
          durationMins: 60,
          daysOfWeek: [0, 1, 2, 3, 4, 5, 6], // Daily
          enabled: true
        },
        {
          id: 'routine_cs_funds',
          title: 'CS Fundamentals Revision (OS/DBMS/CN)',
          category: 'CS Fundamentals',
          priority: 'p2',
          durationMins: 30,
          daysOfWeek: [1, 2, 3, 4, 5], // Mon-Fri
          enabled: true
        },
        {
          id: 'routine_sys_design',
          title: 'System Design / Architecture Reading',
          category: 'System Design',
          priority: 'p3',
          durationMins: 45,
          daysOfWeek: [0, 6], // Weekends
          enabled: true
        },
        {
          id: 'routine_debrief',
          title: 'Evening Debrief & Tomorrow\'s Planning',
          category: 'Other',
          priority: 'p2',
          durationMins: 15,
          daysOfWeek: [0, 1, 2, 3, 4, 5, 6], // Daily
          enabled: true
        }
      ];
      saveRoutines();
    }
  } catch (e) {
    console.error('Error loading routines:', e);
    routineTemplates = [];
  }

  // 5. Load Diary State (preserve existing schema strictly)
  try {
    const rawDiary = localStorage.getItem(WORKSPACE_KEYS.DIARY);
    if (rawDiary) {
      diaryState = JSON.parse(rawDiary);
      if (!diaryState.entries) diaryState = { entries: diaryState };
    } else {
      diaryState = { entries: {} };
    }
  } catch (e) {
    console.error('Error loading diary entries:', e);
    diaryState = { entries: {} };
  }

  // Generate routines for current date idempotently
  ensureRoutinesForDate(currentWorkspaceDate);

  // Render everything for today
  updateWorkspaceDateHeaders();
  renderPlannerTasks();
  renderCodingLog();
  renderDiaryForDate(currentWorkspaceDate);
  renderCalendarGrid();
  renderRoutineTemplates();
  renderWorkspaceAnalytics();
}

// --- 5. WORKSPACE DATE NAVIGATION ---
function setWorkspaceDate(dateStr) {
  if (!dateStr) return;
  // If diary has uncommitted text, save before switching
  saveDiaryFromInputs();

  currentWorkspaceDate = dateStr;
  ensureRoutinesForDate(currentWorkspaceDate);
  updateWorkspaceDateHeaders();

  // Re-render views
  renderPlannerTasks();
  renderCodingLog();
  renderDiaryForDate(currentWorkspaceDate);
  renderCalendarGrid();
}

function changeWorkspaceDate(deltaDays) {
  const parts = currentWorkspaceDate.split('-');
  const d = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
  d.setDate(d.getDate() + deltaDays);

  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  setWorkspaceDate(`${y}-${m}-${day}`);
}

function jumpWorkspaceDate(val) {
  if (val) setWorkspaceDate(val);
}

function jumpWorkspaceToToday() {
  setWorkspaceDate(getTodayDateKey());
}

function updateWorkspaceDateHeaders() {
  const displayEl = document.getElementById('pwCurrentDateDisplay');
  const tagEl = document.getElementById('pwCurrentDateTag');
  const inputEl = document.getElementById('pwDateInputPicker');
  const todayKey = getTodayDateKey();

  if (displayEl) displayEl.textContent = formatDateDisplay(currentWorkspaceDate);
  if (inputEl) inputEl.value = currentWorkspaceDate;

  if (tagEl) {
    if (currentWorkspaceDate === todayKey) {
      tagEl.textContent = 'Today';
      tagEl.className = 'pw-date-tag';
    } else if (currentWorkspaceDate < todayKey) {
      tagEl.textContent = 'Past';
      tagEl.className = 'pw-date-tag past';
    } else {
      tagEl.textContent = 'Upcoming';
      tagEl.className = 'pw-date-tag';
    }
  }

  const potdDateDisplay = document.getElementById('pwPotdDateDisplay');
  if (potdDateDisplay) potdDateDisplay.textContent = formatDateDisplay(currentWorkspaceDate);
}

// --- 6. SUB-NAVIGATION TAB SWITCHING ---
function switchWorkspaceTab(tabId) {
  // If leaving diary, flush uncommitted inputs
  if (currentWorkspaceTab === 'tab-diary') {
    saveDiaryFromInputs();
  }

  currentWorkspaceTab = tabId;

  // Update sub-nav button classes
  document.querySelectorAll('.pw-subnav-btn').forEach(btn => btn.classList.remove('active'));
  const activeBtn = document.getElementById('pw-subnav-' + tabId.replace('tab-', ''));
  if (activeBtn) activeBtn.classList.add('active');

  // Update tab content displays
  document.querySelectorAll('.pw-tab-content').forEach(c => c.classList.remove('active'));
  const targetContent = document.getElementById(tabId);
  if (targetContent) targetContent.classList.add('active');

  // Tab-specific refreshes
  if (tabId === 'tab-planner') {
    renderPlannerTasks();
  } else if (tabId === 'tab-coding') {
    renderCodingLog();
  } else if (tabId === 'tab-diary') {
    renderDiaryForDate(currentWorkspaceDate);
  } else if (tabId === 'tab-history') {
    renderCalendarGrid();
  } else if (tabId === 'tab-analytics') {
    renderWorkspaceAnalytics();
  } else if (tabId === 'tab-routines') {
    renderRoutineTemplates();
  }
}

// --- 7. IDEMPOTENT ROUTINE ENGINE ---
function ensureRoutinesForDate(dateKey) {
  if (!routineTemplates || routineTemplates.length === 0) return;
  const dayOfWeek = getDayOfWeek(dateKey);
  let hasChanges = false;

  routineTemplates.forEach(tpl => {
    if (tpl.enabled && Array.isArray(tpl.daysOfWeek) && tpl.daysOfWeek.includes(dayOfWeek)) {
      // Idempotency rule: Check if task already exists for this template and date
      const exists = plannerTasks.some(t => t.routineTemplateId === tpl.id && t.date === dateKey);
      if (!exists) {
        plannerTasks.push({
          id: 'task_rt_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
          date: dateKey,
          title: tpl.title,
          category: tpl.category,
          priority: tpl.priority,
          completed: false,
          routineTemplateId: tpl.id,
          order: plannerTasks.filter(t => t.date === dateKey).length,
          createdAt: new Date().toISOString(),
          completedAt: null
        });
        hasChanges = true;
      }
    }
  });

  if (hasChanges) {
    saveTasks();
  }
}

function saveRoutines() {
  localStorage.setItem(WORKSPACE_KEYS.ROUTINES, JSON.stringify(routineTemplates));
}

function renderRoutineTemplates() {
  const container = document.getElementById('pwRoutineTemplatesList');
  if (!container) return;

  if (routineTemplates.length === 0) {
    container.innerHTML = '<div style="font-size:12px; color:#64748b; padding:1rem 0;">No routine templates configured yet. Add one to automate daily tasks!</div>';
    return;
  }

  const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  container.innerHTML = routineTemplates.map(r => {
    const daysLabel = (r.daysOfWeek.length === 7)
      ? 'Every day'
      : (r.daysOfWeek.length === 5 && !r.daysOfWeek.includes(0) && !r.daysOfWeek.includes(6))
        ? 'Weekdays (Mon-Fri)'
        : (r.daysOfWeek.length === 2 && r.daysOfWeek.includes(0) && r.daysOfWeek.includes(6))
          ? 'Weekends (Sat-Sun)'
          : r.daysOfWeek.map(d => dayNames[d]).join(', ');

    return `
      <div style="display:flex; align-items:center; justify-content:space-between; gap:1rem; padding:0.85rem 1rem; background:rgba(20,27,36,0.85); border:1px solid rgba(255,255,255,0.06); border-radius:10px;">
        <div style="display:flex; align-items:center; gap:0.75rem;">
          <input type="checkbox" ${r.enabled ? 'checked' : ''} onchange="toggleRoutineEnabled('${r.id}')" style="width:17px; height:17px; accent-color:var(--accent); cursor:pointer;">
          <div>
            <div style="display:flex; align-items:center; gap:6px;">
              <span style="font-weight:700; font-size:13px; color:#f1f5f9;">${r.title}</span>
              <span class="pw-priority-badge ${r.priority}">${r.priority.toUpperCase()}</span>
              <span class="pw-category-tag">${r.category}</span>
            </div>
            <div style="font-size:11px; color:#94a3b8; margin-top:2px;">
              Schedule: <span style="color:#cbd5e1;">${daysLabel}</span> • Est: ${r.durationMins || 30} mins
            </div>
          </div>
        </div>
        <div style="display:flex; gap:0.4rem;">
          <button class="pw-btn" style="padding:4px 8px; font-size:11px;" onclick="openAddRoutineModal('${r.id}')">Edit</button>
          <button class="pw-btn pw-btn-danger" style="padding:4px 8px; font-size:11px;" onclick="deleteRoutine('${r.id}')">Delete</button>
        </div>
      </div>
    `;
  }).join('');
}

function toggleRoutineEnabled(id) {
  const r = routineTemplates.find(x => x.id === id);
  if (r) {
    r.enabled = !r.enabled;
    saveRoutines();
    renderRoutineTemplates();
    ensureRoutinesForDate(currentWorkspaceDate);
    renderPlannerTasks();
  }
}

function deleteRoutine(id) {
  if (confirm('Delete this routine template? Existing tasks already created will not be affected.')) {
    routineTemplates = routineTemplates.filter(x => x.id !== id);
    saveRoutines();
    renderRoutineTemplates();
  }
}

function openAddRoutineModal(routineId = null) {
  const modal = document.getElementById('pwRoutineModalBackdrop');
  const titleEl = document.getElementById('pwRoutineModalTitle');
  const idEl = document.getElementById('pwRoutineModalId');
  const titleInput = document.getElementById('pwRoutineModalTitleInput');
  const catInput = document.getElementById('pwRoutineModalCategory');
  const prioInput = document.getElementById('pwRoutineModalPriority');

  if (routineId) {
    const r = routineTemplates.find(x => x.id === routineId);
    if (!r) return;
    titleEl.textContent = 'Edit Routine Template';
    idEl.value = r.id;
    titleInput.value = r.title;
    catInput.value = r.category;
    prioInput.value = r.priority;
    for (let d = 0; d < 7; d++) {
      const cb = document.getElementById('pwRoutineDay' + d);
      if (cb) cb.checked = r.daysOfWeek.includes(d);
    }
  } else {
    titleEl.textContent = 'Add Routine Template';
    idEl.value = '';
    titleInput.value = '';
    catInput.value = 'DSA Practice';
    prioInput.value = 'p2';
    for (let d = 0; d < 7; d++) {
      const cb = document.getElementById('pwRoutineDay' + d);
      if (cb) cb.checked = d >= 1 && d <= 5; // default weekdays
    }
  }

  modal.style.display = 'flex';
  titleInput.focus();
}

function closeRoutineModal() {
  document.getElementById('pwRoutineModalBackdrop').style.display = 'none';
}

function saveRoutineModal() {
  const id = document.getElementById('pwRoutineModalId').value;
  const title = document.getElementById('pwRoutineModalTitleInput').value.trim();
  const category = document.getElementById('pwRoutineModalCategory').value;
  const priority = document.getElementById('pwRoutineModalPriority').value;

  if (!title) {
    alert('Please enter a routine title');
    return;
  }

  const daysOfWeek = [];
  for (let d = 0; d < 7; d++) {
    const cb = document.getElementById('pwRoutineDay' + d);
    if (cb && cb.checked) daysOfWeek.push(d);
  }

  if (daysOfWeek.length === 0) {
    alert('Please select at least one day of the week for this routine');
    return;
  }

  if (id) {
    const r = routineTemplates.find(x => x.id === id);
    if (r) {
      r.title = title;
      r.category = category;
      r.priority = priority;
      r.daysOfWeek = daysOfWeek;
    }
  } else {
    routineTemplates.push({
      id: 'routine_' + Date.now(),
      title,
      category,
      priority,
      durationMins: 30,
      daysOfWeek,
      enabled: true
    });
  }

  saveRoutines();
  closeRoutineModal();
  renderRoutineTemplates();
  ensureRoutinesForDate(currentWorkspaceDate);
  renderPlannerTasks();
}

// --- 8. DAILY TASK PLANNER ENGINE ---
function saveTasks() {
  localStorage.setItem(WORKSPACE_KEYS.TASKS, JSON.stringify(plannerTasks));
  showWorkspaceSaveStatus('● All changes saved');
}

function renderPlannerTasks() {
  const container = document.getElementById('pwTaskListContainer');
  if (!container) return;

  // Filter tasks for current date
  let dayTasks = plannerTasks.filter(t => t.date === currentWorkspaceDate);

  // Update Summary Metrics
  const total = dayTasks.length;
  const completed = dayTasks.filter(t => t.completed).length;
  const pending = total - completed;
  const p1Count = dayTasks.filter(t => !t.completed && t.priority === 'p1').length;
  const pct = total === 0 ? 0 : Math.round((completed / total) * 100);

  const pctEl = document.getElementById('pwTaskPct');
  const countsEl = document.getElementById('pwTaskCounts');
  const pendingEl = document.getElementById('pwTaskPending');
  const p1El = document.getElementById('pwTaskP1Count');
  const barFill = document.getElementById('pwProgressBarFill');
  const barLabel = document.getElementById('pwProgressPercentLabel');

  if (pctEl) pctEl.textContent = pct + '%';
  if (countsEl) countsEl.textContent = `${completed} of ${total} tasks completed`;
  if (pendingEl) pendingEl.textContent = pending;
  if (p1El) p1El.textContent = p1Count;
  if (barFill) barFill.style.width = pct + '%';
  if (barLabel) barLabel.textContent = pct + '%';

  // Apply filters
  let filtered = dayTasks;
  if (taskFilterState.status === 'pending') {
    filtered = filtered.filter(t => !t.completed);
  } else if (taskFilterState.status === 'completed') {
    filtered = filtered.filter(t => t.completed);
  }

  if (taskFilterState.category !== 'all') {
    filtered = filtered.filter(t => t.category === taskFilterState.category);
  }

  if (taskFilterState.priority !== 'all') {
    filtered = filtered.filter(t => t.priority === taskFilterState.priority);
  }

  if (taskFilterState.search.trim()) {
    const q = taskFilterState.search.toLowerCase();
    filtered = filtered.filter(t => t.title.toLowerCase().includes(q) || t.category.toLowerCase().includes(q));
  }

  // Sort by order or creation
  filtered.sort((a, b) => (a.order || 0) - (b.order || 0));

  if (filtered.length === 0) {
    if (dayTasks.length === 0) {
      container.innerHTML = `
        <div style="text-align:center; padding:2.5rem 1rem; color:#64748b;">
          <div style="font-size:2rem; margin-bottom:0.5rem;">🎯</div>
          <div style="font-size:13px; font-weight:600; color:#cbd5e1; margin-bottom:4px;">No tasks planned for this day</div>
          <div style="font-size:11px;">Add tasks using the quick add bar below or click "+ Add Task" to set your goals.</div>
        </div>
      `;
    } else {
      container.innerHTML = `
        <div style="text-align:center; padding:1.5rem 1rem; color:#64748b; font-size:12px;">
          No tasks match the active filters.
        </div>
      `;
    }
    return;
  }

  container.innerHTML = filtered.map(t => {
    const isCompleted = Boolean(t.completed);
    const checkedClass = isCompleted ? 'checked' : '';
    const titleCompletedClass = isCompleted ? 'completed' : '';
    const checkmark = isCompleted ? '✓' : '';

    return `
      <div class="pw-task-item" id="task_item_${t.id}">
        <div class="pw-task-checkbox ${checkedClass}" onclick="toggleTask('${t.id}')" title="${isCompleted ? 'Mark pending' : 'Mark completed'}">
          ${checkmark}
        </div>
        <div class="pw-task-main">
          <div class="pw-task-title ${titleCompletedClass}" onclick="toggleTask('${t.id}')">
            ${escapeHtml(t.title)}
          </div>
          <div class="pw-task-meta">
            <span class="pw-priority-badge ${t.priority}">${t.priority.toUpperCase()}</span>
            <span class="pw-category-tag">${t.category}</span>
            ${t.routineTemplateId ? '<span style="color:#64748b; font-size:10px;">• Recurring</span>' : ''}
          </div>
        </div>
        <div class="pw-task-actions">
          <button class="pw-task-btn" onclick="moveTask('${t.id}', -1)" title="Move Up">↑</button>
          <button class="pw-task-btn" onclick="moveTask('${t.id}', 1)" title="Move Down">↓</button>
          <button class="pw-task-btn" onclick="copyTaskToTomorrow('${t.id}')" title="Copy to Tomorrow">📋 Tomorrow</button>
          <button class="pw-task-btn" onclick="openAddTaskModal('${t.id}')" title="Edit">✏️</button>
          <button class="pw-task-btn delete" onclick="deleteTask('${t.id}')" title="Delete">🗑️</button>
        </div>
      </div>
    `;
  }).join('');
}

function toggleTask(taskId) {
  const task = plannerTasks.find(t => t.id === taskId);
  if (!task) return;

  task.completed = !task.completed;
  task.completedAt = task.completed ? new Date().toISOString() : null;

  // Check POTD Task Synchronization
  if (task.category === 'LeetCode POTD' && !isPotdSyncing) {
    isPotdSyncing = true;
    const todayPotd = potdRecords[task.date] || { status: 'unstarted' };
    if (task.completed) {
      todayPotd.status = 'completed';
      todayPotd.completedAt = task.completedAt;
    } else {
      if (todayPotd.status === 'completed') todayPotd.status = 'attempting';
    }
    potdRecords[task.date] = todayPotd;
    localStorage.setItem(WORKSPACE_KEYS.POTD, JSON.stringify(potdRecords));
    updatePotdUi();
    isPotdSyncing = false;
  }

  saveTasks();
  renderPlannerTasks();
  renderCalendarGrid();
  renderWorkspaceAnalytics();
}

function quickAddTask() {
  const input = document.getElementById('pwQuickTaskInput');
  const catSelect = document.getElementById('pwQuickCategorySelect');
  const prioSelect = document.getElementById('pwQuickPrioritySelect');

  const title = input.value.trim();
  if (!title) return;

  const category = catSelect.value;
  const priority = prioSelect.value;

  const dayTasks = plannerTasks.filter(t => t.date === currentWorkspaceDate);
  const newTask = {
    id: 'task_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
    date: currentWorkspaceDate,
    title,
    category,
    priority,
    completed: false,
    routineTemplateId: null,
    order: dayTasks.length,
    createdAt: new Date().toISOString(),
    completedAt: null
  };

  plannerTasks.push(newTask);
  saveTasks();
  input.value = '';
  renderPlannerTasks();
  renderCalendarGrid();
  renderWorkspaceAnalytics();
}

function openAddTaskModal(taskId = null) {
  const modal = document.getElementById('pwTaskModalBackdrop');
  const titleEl = document.getElementById('pwTaskModalTitle');
  const idEl = document.getElementById('pwTaskModalId');
  const titleInput = document.getElementById('pwTaskModalTitleInput');
  const catInput = document.getElementById('pwTaskModalCategory');
  const prioInput = document.getElementById('pwTaskModalPriority');
  const dateInput = document.getElementById('pwTaskModalDate');

  if (taskId) {
    const t = plannerTasks.find(x => x.id === taskId);
    if (!t) return;
    titleEl.textContent = 'Edit Task';
    idEl.value = t.id;
    titleInput.value = t.title;
    catInput.value = t.category;
    prioInput.value = t.priority;
    dateInput.value = t.date;
  } else {
    titleEl.textContent = 'Add Task';
    idEl.value = '';
    titleInput.value = '';
    catInput.value = 'DSA Practice';
    prioInput.value = 'p2';
    dateInput.value = currentWorkspaceDate;
  }

  modal.style.display = 'flex';
  titleInput.focus();
}

function closeTaskModal() {
  document.getElementById('pwTaskModalBackdrop').style.display = 'none';
}

function saveTaskModal() {
  const id = document.getElementById('pwTaskModalId').value;
  const title = document.getElementById('pwTaskModalTitleInput').value.trim();
  const category = document.getElementById('pwTaskModalCategory').value;
  const priority = document.getElementById('pwTaskModalPriority').value;
  const date = document.getElementById('pwTaskModalDate').value;

  if (!title) {
    alert('Please enter a task title');
    return;
  }

  if (id) {
    const t = plannerTasks.find(x => x.id === id);
    if (t) {
      t.title = title;
      t.category = category;
      t.priority = priority;
      t.date = date || currentWorkspaceDate;
    }
  } else {
    const dayTasks = plannerTasks.filter(t => t.date === (date || currentWorkspaceDate));
    plannerTasks.push({
      id: 'task_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
      date: date || currentWorkspaceDate,
      title,
      category,
      priority,
      completed: false,
      routineTemplateId: null,
      order: dayTasks.length,
      createdAt: new Date().toISOString(),
      completedAt: null
    });
  }

  saveTasks();
  closeTaskModal();
  renderPlannerTasks();
  renderCalendarGrid();
  renderWorkspaceAnalytics();
}

function deleteTask(taskId) {
  if (confirm('Delete this task?')) {
    plannerTasks = plannerTasks.filter(t => t.id !== taskId);
    saveTasks();
    renderPlannerTasks();
    renderCalendarGrid();
    renderWorkspaceAnalytics();
  }
}

function moveTask(taskId, dir) {
  const dayTasks = plannerTasks.filter(t => t.date === currentWorkspaceDate)
                               .sort((a, b) => (a.order || 0) - (b.order || 0));
  const idx = dayTasks.findIndex(t => t.id === taskId);
  if (idx < 0) return;
  const newIdx = idx + dir;
  if (newIdx < 0 || newIdx >= dayTasks.length) return;

  const temp = dayTasks[idx];
  dayTasks[idx] = dayTasks[newIdx];
  dayTasks[newIdx] = temp;

  dayTasks.forEach((t, i) => { t.order = i; });
  saveTasks();
  renderPlannerTasks();
}

function copyTaskToTomorrow(taskId) {
  const t = plannerTasks.find(x => x.id === taskId);
  if (!t) return;

  const parts = t.date.split('-');
  const d = new Date(parseInt(parts[0], 10), parseInt(parts[1], 10) - 1, parseInt(parts[2], 10));
  d.setDate(d.getDate() + 1);
  const tomorrowKey = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

  const tomorrowTasks = plannerTasks.filter(x => x.date === tomorrowKey);
  plannerTasks.push({
    id: 'task_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
    date: tomorrowKey,
    title: t.title,
    category: t.category,
    priority: t.priority,
    completed: false,
    routineTemplateId: null,
    order: tomorrowTasks.length,
    createdAt: new Date().toISOString(),
    completedAt: null
  });

  saveTasks();
  if (typeof showToast === 'function') {
    showToast(`Task copied to ${formatDateDisplay(tomorrowKey)} ✓`);
  }
}

function setTaskFilter(type, val, btnEl) {
  taskFilterState[type] = val;
  if (btnEl && btnEl.parentElement) {
    btnEl.parentElement.querySelectorAll('.pw-filter-chip').forEach(b => b.classList.remove('active'));
    btnEl.classList.add('active');
  }
  renderPlannerTasks();
}

// --- 9. CODING LOG & LEETCODE POTD ENGINE ---
function saveCodingLog() {
  localStorage.setItem(WORKSPACE_KEYS.CODING, JSON.stringify(codingLog));
}

function savePotdRecords() {
  localStorage.setItem(WORKSPACE_KEYS.POTD, JSON.stringify(potdRecords));
}

function updatePotdUi() {
  const potd = potdRecords[currentWorkspaceDate] || {
    title: '',
    difficulty: 'Medium',
    url: '',
    status: 'unstarted',
    solveStatus: 'independent',
    notes: ''
  };

  const titleDisp = document.getElementById('pwPotdTitleDisplay');
  const titleInput = document.getElementById('pwPotdTitleInput');
  const diffBadge = document.getElementById('pwPotdDifficultyBadge');
  const extLink = document.getElementById('pwPotdExternalLink');
  const statusSel = document.getElementById('pwPotdStatusSelect');
  const solveSel = document.getElementById('pwPotdSolveModeSelect');
  const notesInput = document.getElementById('pwPotdNotesInput');
  const bannerStatus = document.getElementById('pwPotdBannerStatus');
  const taskNotice = document.getElementById('pwPotdLinkedTaskNotice');

  if (titleDisp) titleDisp.textContent = potd.title || 'LeetCode Problem of the Day';
  if (titleInput) titleInput.value = potd.title || '';
  if (notesInput) notesInput.value = potd.notes || '';
  if (statusSel) statusSel.value = potd.status || 'unstarted';
  if (solveSel) solveSel.value = potd.solveStatus || 'independent';

  if (diffBadge) {
    diffBadge.textContent = potd.difficulty || 'Medium';
    diffBadge.className = `pw-diff-badge ${(potd.difficulty || 'medium').toLowerCase()}`;
  }

  if (extLink) {
    if (potd.url) {
      extLink.href = potd.url;
      extLink.style.display = 'inline-flex';
    } else {
      extLink.href = 'https://leetcode.com/problemset/all/';
    }
  }

  if (bannerStatus) {
    if (potd.status === 'completed') {
      bannerStatus.textContent = 'Completed ✓';
      bannerStatus.style.color = '#10b981';
    } else if (potd.status === 'attempting') {
      bannerStatus.textContent = 'In Progress ⏳';
      bannerStatus.style.color = '#fbbf24';
    } else {
      bannerStatus.textContent = 'Unsolved ⭕';
      bannerStatus.style.color = '#94a3b8';
    }
  }

  // Check if linked task exists
  const linkedTask = plannerTasks.find(t => t.date === currentWorkspaceDate && t.category === 'LeetCode POTD');
  if (taskNotice) {
    taskNotice.style.display = linkedTask ? 'inline-block' : 'none';
  }
}

function updatePotdStatus(val) {
  if (!potdRecords[currentWorkspaceDate]) {
    potdRecords[currentWorkspaceDate] = {
      title: '',
      difficulty: 'Medium',
      url: '',
      status: val,
      solveStatus: 'independent',
      notes: ''
    };
  }
  potdRecords[currentWorkspaceDate].status = val;
  if (val === 'completed') {
    potdRecords[currentWorkspaceDate].completedAt = new Date().toISOString();
  } else {
    potdRecords[currentWorkspaceDate].completedAt = null;
  }

  // Synchronize with linked task
  if (!isPotdSyncing) {
    isPotdSyncing = true;
    const task = plannerTasks.find(t => t.date === currentWorkspaceDate && t.category === 'LeetCode POTD');
    if (task) {
      task.completed = (val === 'completed');
      task.completedAt = task.completed ? new Date().toISOString() : null;
      saveTasks();
      renderPlannerTasks();
    }
    isPotdSyncing = false;
  }

  savePotdRecords();
  updatePotdUi();
  renderCalendarGrid();
  renderWorkspaceAnalytics();
}

function updatePotdSolveMode(val) {
  if (!potdRecords[currentWorkspaceDate]) {
    potdRecords[currentWorkspaceDate] = { status: 'unstarted' };
  }
  potdRecords[currentWorkspaceDate].solveStatus = val;
  savePotdRecords();
}

function savePotdMeta() {
  const title = document.getElementById('pwPotdTitleInput')?.value.trim() || '';
  const notes = document.getElementById('pwPotdNotesInput')?.value.trim() || '';

  if (!potdRecords[currentWorkspaceDate]) {
    potdRecords[currentWorkspaceDate] = { status: 'unstarted' };
  }

  potdRecords[currentWorkspaceDate].title = title;
  potdRecords[currentWorkspaceDate].notes = notes;
  savePotdRecords();
  updatePotdUi();
}

function renderCodingLog() {
  updatePotdUi();

  const container = document.getElementById('pwCodingEntriesList');
  if (!container) return;

  const dayEntries = codingLog.filter(e => e.date === currentWorkspaceDate);

  // Coding Statistics Banner
  const totalLogged = dayEntries.length;
  const uniqueTitles = new Set(dayEntries.map(e => e.title.trim().toLowerCase())).size;
  const indepCount = dayEntries.filter(e => e.solveStatus === 'independent').length;
  const edCount = dayEntries.filter(e => e.solveStatus === 'editorial').length;
  const totalTimeMins = dayEntries.reduce((sum, e) => sum + (parseInt(e.timeSpentMinutes, 10) || 0), 0);
  const indepRate = totalLogged === 0 ? 0 : Math.round((indepCount / totalLogged) * 100);

  const solvesEl = document.getElementById('pwCodeSolvesToday');
  const uniqueEl = document.getElementById('pwCodeUniqueToday');
  const rateEl = document.getElementById('pwCodeIndependentRate');
  const indepEl = document.getElementById('pwCodeIndepCount');
  const edEl = document.getElementById('pwCodeEdCount');
  const timeEl = document.getElementById('pwCodeTimeToday');
  const bannerTimeSub = document.getElementById('pwCodingTodaySub');
  const bannerTodayCount = document.getElementById('pwCodingTodayCount');

  if (solvesEl) solvesEl.textContent = totalLogged;
  if (uniqueEl) uniqueEl.textContent = uniqueTitles;
  if (rateEl) rateEl.textContent = indepRate + '%';
  if (indepEl) indepEl.textContent = indepCount;
  if (edEl) edEl.textContent = edCount;
  if (timeEl) timeEl.textContent = totalTimeMins + 'm';
  if (bannerTimeSub) bannerTimeSub.textContent = totalTimeMins + ' mins practice logged';
  if (bannerTodayCount) bannerTodayCount.textContent = totalLogged;

  if (dayEntries.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:2rem 1rem; color:#64748b; background:rgba(20,27,36,0.6); border:1px solid rgba(255,255,255,0.06); border-radius:12px;">
        <div style="font-size:1.8rem; margin-bottom:0.4rem;">💡</div>
        <div style="font-size:13px; font-weight:600; color:#cbd5e1; margin-bottom:4px;">No problem solutions recorded today</div>
        <div style="font-size:11px;">Click "+ Log Problem Solution" to write down your approach, edge cases, and complexities.</div>
      </div>
    `;
    return;
  }

  container.innerHTML = dayEntries.map(e => {
    const diffClass = (e.difficulty || 'medium').toLowerCase();
    const solveStatusText = e.solveStatus === 'independent' ? '🎯 Independent' : (e.solveStatus === 'editorial' ? '📖 Editorial' : '⚠️ Stuck');
    const solveStatusColor = e.solveStatus === 'independent' ? '#10b981' : (e.solveStatus === 'editorial' ? '#fbbf24' : '#f87171');
    const topics = Array.isArray(e.topics) ? e.topics : (e.topics ? String(e.topics).split(',').map(s => s.trim()) : []);

    return `
      <div class="pw-card" style="padding:1.25rem;">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:1rem; flex-wrap:wrap;">
          <div>
            <div style="display:flex; align-items:center; gap:6px; margin-bottom:4px; flex-wrap:wrap;">
              <span class="pw-diff-badge ${diffClass}">${e.difficulty || 'Medium'}</span>
              <span class="pw-tag">${e.platform || 'LeetCode'}</span>
              <span class="pw-tag" style="color:${solveStatusColor}; font-weight:600;">${solveStatusText}</span>
              ${e.timeSpentMinutes ? `<span style="font-size:11px; color:#94a3b8; font-family:var(--font-mono);">${e.timeSpentMinutes} mins</span>` : ''}
              ${e.needsRevision ? '<span class="pw-tag" style="background:rgba(239,68,68,0.12); color:#f87171; border-color:rgba(239,68,68,0.25);">Needs Revision</span>' : ''}
            </div>
            <h4 style="font-size:1.1rem; font-weight:700; color:#f8fafc; margin:2px 0 6px 0;">
              ${escapeHtml(e.title)}
            </h4>
            ${e.url ? `<a href="${e.url}" target="_blank" style="font-size:11px; color:#38bdf8; text-decoration:none;">Problem Link ↗</a>` : ''}
            <div style="display:flex; gap:4px; margin-top:6px; flex-wrap:wrap;">
              ${topics.map(t => `<span class="pw-tag" style="font-size:10px;">${t}</span>`).join('')}
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:0.4rem;">
            <button class="pw-btn" style="padding:4px 8px; font-size:11px;" onclick="toggleProblemDrawer('${e.id}')">Approach & Notes ▾</button>
            <button class="pw-btn" style="padding:4px 8px; font-size:11px;" onclick="toggleRevisionFlag('${e.id}')" title="Toggle Revision Flag">
              ${e.needsRevision ? '★ Flagged' : '☆ Revise'}
            </button>
            <button class="pw-btn" style="padding:4px 8px; font-size:11px;" onclick="openAddCodingModal('${e.id}')">Edit</button>
            <button class="pw-btn pw-btn-danger" style="padding:4px 8px; font-size:11px;" onclick="deleteCodingEntry('${e.id}')">Delete</button>
          </div>
        </div>

        <!-- Expandable Drawer for Problem Approach & Notes -->
        <div id="drawer_${e.id}" style="display:none; margin-top:1rem; padding-top:1rem; border-top:1px solid rgba(255,255,255,0.08); font-size:12px; color:#cbd5e1; line-height:1.5;">
          ${e.approach ? `<div style="margin-bottom:0.6rem;"><strong style="color:#10b981;">Approach & Intuition:</strong><div style="margin-top:2px; white-space:pre-wrap;">${escapeHtml(e.approach)}</div></div>` : ''}
          <div style="display:flex; gap:1.5rem; margin-bottom:0.6rem; flex-wrap:wrap;">
            ${e.timeComplexity ? `<div><strong style="color:#94a3b8;">Time Complexity:</strong> <span style="font-family:var(--font-mono); color:#f1f5f9;">${escapeHtml(e.timeComplexity)}</span></div>` : ''}
            ${e.spaceComplexity ? `<div><strong style="color:#94a3b8;">Space Complexity:</strong> <span style="font-family:var(--font-mono); color:#f1f5f9;">${escapeHtml(e.spaceComplexity)}</span></div>` : ''}
          </div>
          ${e.edgeCases ? `<div><strong style="color:#fbbf24;">Edge Cases & Pitfalls:</strong> <span style="color:#f1f5f9;">${escapeHtml(e.edgeCases)}</span></div>` : ''}
        </div>
      </div>
    `;
  }).join('');
}

function toggleProblemDrawer(id) {
  const el = document.getElementById('drawer_' + id);
  if (el) {
    el.style.display = el.style.display === 'none' ? 'block' : 'none';
  }
}

function toggleRevisionFlag(id) {
  const entry = codingLog.find(e => e.id === id);
  if (entry) {
    entry.needsRevision = !entry.needsRevision;
    saveCodingLog();
    renderCodingLog();
    renderWorkspaceAnalytics();
  }
}

function openAddCodingModal(entryId = null) {
  const modal = document.getElementById('pwCodingModalBackdrop');
  const titleEl = document.getElementById('pwCodingModalTitle');
  const idEl = document.getElementById('pwCodingModalId');
  const titleInput = document.getElementById('pwCodingModalTitleInput');
  const platform = document.getElementById('pwCodingModalPlatform');
  const diff = document.getElementById('pwCodingModalDifficulty');
  const url = document.getElementById('pwCodingModalUrl');
  const time = document.getElementById('pwCodingModalTime');
  const solveStatus = document.getElementById('pwCodingModalSolveStatus');
  const topics = document.getElementById('pwCodingModalTopics');
  const approach = document.getElementById('pwCodingModalApproach');
  const timeComp = document.getElementById('pwCodingModalTimeComp');
  const spaceComp = document.getElementById('pwCodingModalSpaceComp');
  const edgeCases = document.getElementById('pwCodingModalEdgeCases');
  const rev = document.getElementById('pwCodingModalRevision');

  if (entryId) {
    const e = codingLog.find(x => x.id === entryId);
    if (!e) return;
    titleEl.textContent = 'Edit Problem Solution';
    idEl.value = e.id;
    titleInput.value = e.title;
    platform.value = e.platform || 'LeetCode';
    diff.value = e.difficulty || 'Medium';
    url.value = e.url || '';
    time.value = e.timeSpentMinutes || '';
    solveStatus.value = e.solveStatus || 'independent';
    topics.value = Array.isArray(e.topics) ? e.topics.join(', ') : (e.topics || '');
    approach.value = e.approach || '';
    timeComp.value = e.timeComplexity || '';
    spaceComp.value = e.spaceComplexity || '';
    edgeCases.value = e.edgeCases || '';
    rev.checked = Boolean(e.needsRevision);
  } else {
    titleEl.textContent = 'Log Problem Solution';
    idEl.value = '';
    titleInput.value = '';
    platform.value = 'LeetCode';
    diff.value = 'Medium';
    url.value = '';
    time.value = '30';
    solveStatus.value = 'independent';
    topics.value = '';
    approach.value = '';
    timeComp.value = 'O(N)';
    spaceComp.value = 'O(1)';
    edgeCases.value = '';
    rev.checked = false;
  }

  modal.style.display = 'flex';
  titleInput.focus();
}

function closeCodingModal() {
  document.getElementById('pwCodingModalBackdrop').style.display = 'none';
}

function saveCodingModal() {
  const id = document.getElementById('pwCodingModalId').value;
  const title = document.getElementById('pwCodingModalTitleInput').value.trim();
  const platform = document.getElementById('pwCodingModalPlatform').value;
  const difficulty = document.getElementById('pwCodingModalDifficulty').value;
  const url = document.getElementById('pwCodingModalUrl').value.trim();
  const timeSpentMinutes = parseInt(document.getElementById('pwCodingModalTime').value, 10) || 0;
  const solveStatus = document.getElementById('pwCodingModalSolveStatus').value;
  const topicsRaw = document.getElementById('pwCodingModalTopics').value.trim();
  const approach = document.getElementById('pwCodingModalApproach').value.trim();
  const timeComplexity = document.getElementById('pwCodingModalTimeComp').value.trim();
  const spaceComplexity = document.getElementById('pwCodingModalSpaceComp').value.trim();
  const edgeCases = document.getElementById('pwCodingModalEdgeCases').value.trim();
  const needsRevision = document.getElementById('pwCodingModalRevision').checked;

  if (!title) {
    alert('Please enter a problem title');
    return;
  }

  const topics = topicsRaw ? topicsRaw.split(',').map(s => s.trim()).filter(Boolean) : [];

  if (id) {
    const entry = codingLog.find(x => x.id === id);
    if (entry) {
      entry.title = title;
      entry.platform = platform;
      entry.difficulty = difficulty;
      entry.url = url;
      entry.timeSpentMinutes = timeSpentMinutes;
      entry.solveStatus = solveStatus;
      entry.topics = topics;
      entry.approach = approach;
      entry.timeComplexity = timeComplexity;
      entry.spaceComplexity = spaceComplexity;
      entry.edgeCases = edgeCases;
      entry.needsRevision = needsRevision;
    }
  } else {
    codingLog.push({
      id: 'code_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
      date: currentWorkspaceDate,
      title,
      platform,
      difficulty,
      url,
      timeSpentMinutes,
      solveStatus,
      topics,
      approach,
      timeComplexity,
      spaceComplexity,
      edgeCases,
      needsRevision,
      createdAt: new Date().toISOString()
    });
  }

  saveCodingLog();
  closeCodingModal();
  renderCodingLog();
  renderCalendarGrid();
  renderWorkspaceAnalytics();
}

function deleteCodingEntry(id) {
  if (confirm('Delete this problem entry?')) {
    codingLog = codingLog.filter(e => e.id !== id);
    saveCodingLog();
    renderCodingLog();
    renderCalendarGrid();
    renderWorkspaceAnalytics();
  }
}

// --- 10. PRIVATE DIARY / DAILY DEBRIEF ENGINE ---
function renderDiaryForDate(dateKey) {
  const entry = diaryState.entries[dateKey] || {
    mood: 'good',
    focusRating: 3,
    energyRating: 3,
    accomplishments: '',
    mistakes: '',
    distractions: '',
    freeform: '',
    priorities: ['', '', ''],
    priorityDone: [false, false, false]
  };

  // 1. Mood Active State
  document.querySelectorAll('.diary-mood-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-mood') === entry.mood);
  });

  // 2. Focus & Energy Displays & Pills
  const focusVal = entry.focusRating || 3;
  const energyVal = entry.energyRating || 3;

  const fDisp = document.getElementById('pwDiaryFocusValDisplay');
  const eDisp = document.getElementById('pwDiaryEnergyValDisplay');
  if (fDisp) fDisp.textContent = `${focusVal} / 5`;
  if (eDisp) eDisp.textContent = `${energyVal} / 5`;

  const fPills = document.getElementById('pwDiaryFocusPills');
  if (fPills) {
    fPills.querySelectorAll('.diary-pill-btn').forEach((btn, idx) => {
      btn.classList.toggle('active', (idx + 1) === focusVal);
    });
  }

  const ePills = document.getElementById('pwDiaryEnergyPills');
  if (ePills) {
    ePills.querySelectorAll('.diary-pill-btn').forEach((btn, idx) => {
      btn.classList.toggle('active', (idx + 1) === energyVal);
    });
  }

  // 3. Text Areas
  const acc = document.getElementById('diaryAccomplishments');
  const mis = document.getElementById('diaryMistakes');
  const dis = document.getElementById('diaryDistractions');
  const fre = document.getElementById('diaryFreeform');

  if (acc) acc.value = entry.accomplishments || '';
  if (mis) mis.value = entry.mistakes || '';
  if (dis) dis.value = entry.distractions || '';
  if (fre) fre.value = entry.freeform || '';

  // 4. Tomorrow Priorities
  const priorities = entry.priorities || ['', '', ''];
  const priorityDone = entry.priorityDone || [false, false, false];

  for (let i = 1; i <= 3; i++) {
    const input = document.getElementById('diaryPrioInput' + i);
    const check = document.getElementById('diaryPrioCheck1' + i);
    if (input) input.value = priorities[i - 1] || '';
    if (check) check.checked = Boolean(priorityDone[i - 1]);
  }

  // 5. Sidebar Recent Debriefs & Streak
  renderDiarySidebar();
}

function setDiaryMood(mood) {
  saveDiaryFromInputs();
  if (!diaryState.entries[currentWorkspaceDate]) {
    diaryState.entries[currentWorkspaceDate] = {};
  }
  diaryState.entries[currentWorkspaceDate].mood = mood;
  saveDiaryToStorage();
  renderDiaryForDate(currentWorkspaceDate);
  renderWorkspaceAnalytics();
}

function setDiaryRating(type, val) {
  saveDiaryFromInputs();
  if (!diaryState.entries[currentWorkspaceDate]) {
    diaryState.entries[currentWorkspaceDate] = {};
  }
  if (type === 'focus') diaryState.entries[currentWorkspaceDate].focusRating = val;
  if (type === 'energy') diaryState.entries[currentWorkspaceDate].energyRating = val;
  saveDiaryToStorage();
  renderDiaryForDate(currentWorkspaceDate);
  renderWorkspaceAnalytics();
}

function handleDiaryInput() {
  showWorkspaceSaveStatus('● Saving changes...', true);
  clearTimeout(diarySaveTimeout);
  diarySaveTimeout = setTimeout(() => {
    saveDiaryFromInputs();
    renderCalendarGrid();
    renderWorkspaceAnalytics();
  }, 600);
}

function saveDiaryFromInputs() {
  const acc = document.getElementById('diaryAccomplishments')?.value || '';
  const mis = document.getElementById('diaryMistakes')?.value || '';
  const dis = document.getElementById('diaryDistractions')?.value || '';
  const fre = document.getElementById('diaryFreeform')?.value || '';

  const prios = [
    document.getElementById('diaryPrioInput1')?.value || '',
    document.getElementById('diaryPrioInput2')?.value || '',
    document.getElementById('diaryPrioInput3')?.value || ''
  ];

  const prioDone = [
    Boolean(document.getElementById('diaryPrioCheck1')?.checked),
    Boolean(document.getElementById('diaryPrioCheck2')?.checked),
    Boolean(document.getElementById('diaryPrioCheck3')?.checked)
  ];

  if (!diaryState.entries[currentWorkspaceDate]) {
    diaryState.entries[currentWorkspaceDate] = {
      mood: 'good',
      focusRating: 3,
      energyRating: 3
    };
  }

  const e = diaryState.entries[currentWorkspaceDate];
  e.accomplishments = acc;
  e.mistakes = mis;
  e.distractions = dis;
  e.freeform = fre;
  e.priorities = prios;
  e.priorityDone = prioDone;
  e.updatedAt = new Date().toISOString();

  saveDiaryToStorage();
}

function saveDiaryToStorage() {
  localStorage.setItem(WORKSPACE_KEYS.DIARY, JSON.stringify(diaryState));
  showWorkspaceSaveStatus('● All changes saved');
}

function renderDiarySidebar() {
  const streakEl = document.getElementById('pwDiaryStreakCount');
  const recentList = document.getElementById('pwDiaryRecentEntriesList');

  // Calculate Streak
  let streak = 0;
  const todayParts = getTodayDateKey().split('-');
  let checkDate = new Date(parseInt(todayParts[0], 10), parseInt(todayParts[1], 10) - 1, parseInt(todayParts[2], 10));

  while (true) {
    const k = `${checkDate.getFullYear()}-${String(checkDate.getMonth() + 1).padStart(2, '0')}-${String(checkDate.getDate()).padStart(2, '0')}`;
    const ent = diaryState.entries[k];
    const hasContent = ent && (ent.accomplishments?.trim() || ent.mistakes?.trim() || ent.freeform?.trim());
    if (hasContent) {
      streak++;
      checkDate.setDate(checkDate.getDate() - 1);
    } else {
      // If today is empty, check yesterday before breaking streak
      if (streak === 0 && k === getTodayDateKey()) {
        checkDate.setDate(checkDate.getDate() - 1);
        continue;
      }
      break;
    }
  }

  if (streakEl) streakEl.textContent = `${streak} ${streak === 1 ? 'Day' : 'Days'}`;

  // Recent Entries List
  if (recentList) {
    const keys = Object.keys(diaryState.entries).sort().reverse();
    const withContent = keys.filter(k => {
      const ent = diaryState.entries[k];
      return ent && (ent.accomplishments?.trim() || ent.mistakes?.trim() || ent.freeform?.trim());
    }).slice(0, 10);

    if (withContent.length === 0) {
      recentList.innerHTML = '<div style="font-size:11px; color:#64748b; padding:0.5rem 0;">No written debriefs recorded yet.</div>';
    } else {
      const moodEmoji = { great: '🤩', good: '😊', neutral: '😐', low: '😔', stressed: '😫' };
      recentList.innerHTML = withContent.map(k => {
        const ent = diaryState.entries[k];
        const isCurrent = k === currentWorkspaceDate;
        return `
          <div style="padding:6px 10px; border-radius:8px; background:${isCurrent ? 'rgba(16,185,129,0.1)' : 'rgba(255,255,255,0.03)'}; border:1px solid ${isCurrent ? 'rgba(16,185,129,0.3)' : 'rgba(255,255,255,0.06)'}; cursor:pointer; display:flex; justify-content:space-between; align-items:center;" onclick="setWorkspaceDate('${k}')">
            <span style="font-size:11px; font-weight:600; color:${isCurrent ? '#10b981' : '#cbd5e1'}; font-family:var(--font-mono);">${k}</span>
            <span style="font-size:12px;">${moodEmoji[ent.mood] || '📝'}</span>
          </div>
        `;
      }).join('');
    }
  }
}

// --- 11. CALENDAR & HISTORY ENGINE ---
function renderCalendarGrid() {
  const container = document.getElementById('pwCalendarGridContainer');
  const titleEl = document.getElementById('pwCalendarMonthTitle');
  if (!container) return;

  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
  if (titleEl) titleEl.textContent = `${monthNames[calendarMonth]} ${calendarYear}`;

  const firstDay = new Date(calendarYear, calendarMonth, 1).getDay(); // 0 = Sun
  const daysInMonth = new Date(calendarYear, calendarMonth + 1, 0).getDate();

  const dayHeaders = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  let html = dayHeaders.map(h => `<div class="pw-calendar-day-header">${h}</div>`).join('');

  // Blank cells before first day
  for (let i = 0; i < firstDay; i++) {
    html += '<div class="pw-calendar-cell empty"></div>';
  }

  const todayKey = getTodayDateKey();

  for (let day = 1; day <= daysInMonth; day++) {
    const mStr = String(calendarMonth + 1).padStart(2, '0');
    const dStr = String(day).padStart(2, '0');
    const cellDateKey = `${calendarYear}-${mStr}-${dStr}`;

    const isToday = cellDateKey === todayKey;
    const isSelected = cellDateKey === currentWorkspaceDate;

    // Check activity dots
    const hasCompletedTask = plannerTasks.some(t => t.date === cellDateKey && t.completed);
    const hasCoding = codingLog.some(e => e.date === cellDateKey);
    const potd = potdRecords[cellDateKey];
    const hasPotd = potd && potd.status === 'completed';
    const diary = diaryState.entries[cellDateKey];
    const hasDiary = diary && (diary.accomplishments?.trim() || diary.mistakes?.trim() || diary.freeform?.trim());

    let classes = 'pw-calendar-cell';
    if (isToday) classes += ' today';
    if (isSelected) classes += ' selected';

    html += `
      <div class="${classes}" onclick="setWorkspaceDate('${cellDateKey}')">
        <span class="pw-calendar-date-num">${day}</span>
        <div class="pw-activity-dots">
          ${hasCompletedTask ? '<span class="pw-dot task" title="Tasks completed"></span>' : ''}
          ${hasCoding ? '<span class="pw-dot code" title="Coding problem logged"></span>' : ''}
          ${hasPotd ? '<span class="pw-dot potd" title="LeetCode POTD solved"></span>' : ''}
          ${hasDiary ? '<span class="pw-dot diary" title="Debrief logged"></span>' : ''}
        </div>
      </div>
    `;
  }

  container.innerHTML = html;
}

function changeCalendarMonth(delta) {
  calendarMonth += delta;
  if (calendarMonth < 0) {
    calendarMonth = 11;
    calendarYear--;
  } else if (calendarMonth > 11) {
    calendarMonth = 0;
    calendarYear++;
  }
  renderCalendarGrid();
}

function runGlobalWorkspaceSearch(query) {
  const container = document.getElementById('pwGlobalSearchResults');
  if (!container) return;

  const q = query.trim().toLowerCase();
  if (!q) {
    container.innerHTML = '<div style="font-size:11px; color:#64748b; text-align:center; padding:1.5rem 0;">Type a keyword above or click any calendar date to jump directly to it.</div>';
    return;
  }

  const results = [];

  // Search Tasks
  if (globalSearchFilter === 'all' || globalSearchFilter === 'tasks') {
    plannerTasks.forEach(t => {
      if (t.title.toLowerCase().includes(q) || t.category.toLowerCase().includes(q)) {
        results.push({
          type: 'Task',
          date: t.date,
          title: t.title,
          badge: t.category,
          color: '#10b981'
        });
      }
    });
  }

  // Search Coding Logs
  if (globalSearchFilter === 'all' || globalSearchFilter === 'coding') {
    codingLog.forEach(e => {
      const approachStr = e.approach || '';
      const edgeStr = e.edgeCases || '';
      if (e.title.toLowerCase().includes(q) || approachStr.toLowerCase().includes(q) || edgeStr.toLowerCase().includes(q)) {
        results.push({
          type: 'Code',
          date: e.date,
          title: e.title,
          badge: `${e.platform || 'LeetCode'} • ${e.difficulty || 'Medium'}`,
          color: '#38bdf8'
        });
      }
    });
  }

  // Search Diary
  if (globalSearchFilter === 'all' || globalSearchFilter === 'diary') {
    Object.keys(diaryState.entries).forEach(dateKey => {
      const ent = diaryState.entries[dateKey];
      const acc = ent.accomplishments || '';
      const mis = ent.mistakes || '';
      const fre = ent.freeform || '';
      if (acc.toLowerCase().includes(q) || mis.toLowerCase().includes(q) || fre.toLowerCase().includes(q)) {
        results.push({
          type: 'Debrief',
          date: dateKey,
          title: acc.slice(0, 70) || mis.slice(0, 70) || 'Debrief reflection',
          badge: `Mood: ${ent.mood || 'good'}`,
          color: '#fbbf24'
        });
      }
    });
  }

  if (results.length === 0) {
    container.innerHTML = `<div style="font-size:11px; color:#94a3b8; text-align:center; padding:1.5rem 0;">No matching records found for "${escapeHtml(q)}".</div>`;
    return;
  }

  // Sort latest first
  results.sort((a, b) => b.date.localeCompare(a.date));

  container.innerHTML = results.slice(0, 25).map(r => `
    <div style="padding:8px 12px; background:rgba(20,27,36,0.85); border:1px solid rgba(255,255,255,0.06); border-radius:8px; cursor:pointer;" onclick="setWorkspaceDate('${r.date}')">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
        <span style="font-size:10px; font-weight:700; text-transform:uppercase; color:${r.color};">${r.type}</span>
        <span style="font-size:10px; color:#94a3b8; font-family:var(--font-mono);">${r.date}</span>
      </div>
      <div style="font-size:12px; font-weight:600; color:#f1f5f9; overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">
        ${escapeHtml(r.title)}
      </div>
      <div style="font-size:10px; color:#64748b; margin-top:2px;">${r.badge}</div>
    </div>
  `).join('');
}

function setGlobalSearchFilter(type, btnEl) {
  globalSearchFilter = type;
  if (btnEl && btnEl.parentElement) {
    btnEl.parentElement.querySelectorAll('.pw-filter-chip').forEach(b => b.classList.remove('active'));
    btnEl.classList.add('active');
  }
  const input = document.getElementById('pwGlobalSearchInput');
  if (input) runGlobalWorkspaceSearch(input.value);
}

// --- 12. REAL-DATA ANALYTICS ENGINE ---
function renderWorkspaceAnalytics() {
  // 1. Task Metrics
  const totalTasks = plannerTasks.length;
  const completedTasks = plannerTasks.filter(t => t.completed).length;
  const taskRate = totalTasks === 0 ? 0 : Math.round((completedTasks / totalTasks) * 100);

  const tTotalEl = document.getElementById('pwAnalyticsTotalTasks');
  const tRateEl = document.getElementById('pwAnalyticsTaskRate');
  if (tTotalEl) tTotalEl.textContent = completedTasks;
  if (tRateEl) tRateEl.textContent = taskRate + '%';

  // 2. Coding Metrics
  const totalAttempts = codingLog.length;
  const uniqueProblems = new Set(codingLog.map(e => e.title.trim().toLowerCase())).size;
  const indepCount = codingLog.filter(e => e.solveStatus === 'independent').length;
  const indepRate = totalAttempts === 0 ? 0 : Math.round((indepCount / totalAttempts) * 100);

  const cUniqueEl = document.getElementById('pwAnalyticsUniqueProblems');
  const cAttemptsEl = document.getElementById('pwAnalyticsTotalAttempts');
  const cIndepEl = document.getElementById('pwAnalyticsIndepRate');
  if (cUniqueEl) cUniqueEl.textContent = uniqueProblems;
  if (cAttemptsEl) cAttemptsEl.textContent = totalAttempts;
  if (cIndepEl) cIndepEl.textContent = indepRate + '%';

  // 3. POTD Metrics
  const potdDates = Object.keys(potdRecords);
  const completedPotds = potdDates.filter(k => potdRecords[k]?.status === 'completed').length;
  const potdRate = potdDates.length === 0 ? 0 : Math.round((completedPotds / potdDates.length) * 100);

  const pCountEl = document.getElementById('pwAnalyticsPotdCount');
  const pRateEl = document.getElementById('pwAnalyticsPotdRate');
  if (pCountEl) pCountEl.textContent = completedPotds;
  if (pRateEl) pRateEl.textContent = potdRate + '%';

  // 4. Problem Difficulty Breakdown
  const diffCounts = { Easy: 0, Medium: 0, Hard: 0 };
  codingLog.forEach(e => {
    const d = e.difficulty || 'Medium';
    if (diffCounts[d] !== undefined) diffCounts[d]++;
    else diffCounts.Medium++;
  });

  const diffListEl = document.getElementById('pwAnalyticsDifficultyList');
  if (diffListEl) {
    diffListEl.innerHTML = ['Easy', 'Medium', 'Hard'].map(d => {
      const count = diffCounts[d];
      const pct = totalAttempts === 0 ? 0 : Math.round((count / totalAttempts) * 100);
      const color = d === 'Easy' ? '#10b981' : (d === 'Medium' ? '#f59e0b' : '#ef4444');
      return `
        <div>
          <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
            <span style="font-weight:600; color:${color};">${d}</span>
            <span style="font-family:var(--font-mono); color:#cbd5e1;">${count} (${pct}%)</span>
          </div>
          <div style="height:6px; background:rgba(255,255,255,0.08); border-radius:9999px; overflow:hidden;">
            <div style="height:100%; width:${pct}%; background:${color}; border-radius:9999px;"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  // 5. Revision Backlog
  const revisionProblems = codingLog.filter(e => e.needsRevision);
  const revCountEl = document.getElementById('pwRevisionBacklogCount');
  const revListEl = document.getElementById('pwAnalyticsRevisionList');

  if (revCountEl) revCountEl.textContent = `${revisionProblems.length} problems flagged`;
  if (revListEl) {
    if (revisionProblems.length === 0) {
      revListEl.innerHTML = '<div style="font-size:11px; color:#64748b; padding:0.5rem 0;">No problems in revision backlog. Mark tricky questions to review here.</div>';
    } else {
      revListEl.innerHTML = revisionProblems.map(e => `
        <div style="display:flex; justify-content:space-between; align-items:center; padding:6px 10px; background:rgba(20,27,36,0.85); border:1px solid rgba(255,255,255,0.06); border-radius:8px;">
          <div>
            <div style="font-size:12px; font-weight:600; color:#f1f5f9;">${escapeHtml(e.title)}</div>
            <div style="font-size:10px; color:#94a3b8;">${e.platform || 'LeetCode'} • ${e.difficulty || 'Medium'}</div>
          </div>
          <button class="pw-btn" style="padding:2px 8px; font-size:10px;" onclick="toggleRevisionFlag('${e.id}')">Resolved ✓</button>
        </div>
      `).join('');
    }
  }

  // 6. Diary & Consistency Insights
  const diaryDates = Object.keys(diaryState.entries).filter(k => {
    const ent = diaryState.entries[k];
    return ent && (ent.accomplishments?.trim() || ent.mistakes?.trim() || ent.freeform?.trim());
  });

  const dCountEl = document.getElementById('pwAnalyticsDiaryCount');
  const dFocusEl = document.getElementById('pwAnalyticsAvgFocus');
  const dEnergyEl = document.getElementById('pwAnalyticsAvgEnergy');
  const dMoodEl = document.getElementById('pwAnalyticsTopMood');

  if (dCountEl) dCountEl.textContent = diaryDates.length;

  if (diaryDates.length > 0) {
    let sumFocus = 0;
    let sumEnergy = 0;
    const moodCounts = {};

    diaryDates.forEach(k => {
      const ent = diaryState.entries[k];
      sumFocus += (ent.focusRating || 3);
      sumEnergy += (ent.energyRating || 3);
      const m = ent.mood || 'good';
      moodCounts[m] = (moodCounts[m] || 0) + 1;
    });

    const avgF = (sumFocus / diaryDates.length).toFixed(1);
    const avgE = (sumEnergy / diaryDates.length).toFixed(1);

    let topMood = 'good';
    let topCount = 0;
    Object.keys(moodCounts).forEach(m => {
      if (moodCounts[m] > topCount) {
        topCount = moodCounts[m];
        topMood = m;
      }
    });

    const moodEmoji = { great: '🤩 Great', good: '😊 Good', neutral: '😐 Neutral', low: '😔 Low', stressed: '😫 Tired' };

    if (dFocusEl) dFocusEl.textContent = `${avgF} / 5`;
    if (dEnergyEl) dEnergyEl.textContent = `${avgE} / 5`;
    if (dMoodEl) dMoodEl.textContent = moodEmoji[topMood] || topMood;
  } else {
    if (dFocusEl) dFocusEl.textContent = '0.0 / 5';
    if (dEnergyEl) dEnergyEl.textContent = '0.0 / 5';
    if (dMoodEl) dMoodEl.textContent = 'None logged';
  }
}

// --- 13. FOCUS TIMER ENGINE ---
function setTimerDuration(mins, mode) {
  pwTimerSecondsLeft = mins * 60;
  pwTimerCurrentMode = mode;
  updateTimerDisplay();
}

function updateTimerDisplay() {
  const mins = Math.floor(pwTimerSecondsLeft / 60);
  const secs = pwTimerSecondsLeft % 60;
  const timeStr = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  const digits = document.getElementById('pwTimerDigits');
  const modeLabel = document.getElementById('pwTimerModeLabel');
  if (digits) digits.textContent = timeStr;
  if (modeLabel) modeLabel.textContent = pwTimerCurrentMode;
}

function toggleTimer() {
  const btn = document.getElementById('pwTimerToggleBtn');
  if (pwTimerRunning) {
    clearInterval(pwTimerInterval);
    pwTimerRunning = false;
    if (btn) btn.textContent = 'Resume Focus';
  } else {
    pwTimerRunning = true;
    if (btn) btn.textContent = 'Pause Focus';
    pwTimerInterval = setInterval(() => {
      if (pwTimerSecondsLeft > 0) {
        pwTimerSecondsLeft--;
        todayFocusMinutes += (1 / 60);
        updateTimerDisplay();
        const focusTodayEl = document.getElementById('pwFocusTimerToday');
        if (focusTodayEl) focusTodayEl.textContent = Math.round(todayFocusMinutes) + 'm';
      } else {
        clearInterval(pwTimerInterval);
        pwTimerRunning = false;
        if (btn) btn.textContent = 'Start Focus';
        alert(`Focus Session Completed! Take a quick break.`);
      }
    }, 1000);
  }
}

function resetTimer() {
  clearInterval(pwTimerInterval);
  pwTimerRunning = false;
  pwTimerSecondsLeft = 25 * 60;
  pwTimerCurrentMode = 'Pomodoro';
  const btn = document.getElementById('pwTimerToggleBtn');
  if (btn) btn.textContent = 'Start Focus';
  updateTimerDisplay();
}

// --- 14. EXPORT & BACKUP ENGINE ---
function openExportModal() {
  document.getElementById('pwExportModalBackdrop').style.display = 'flex';
}

function closeExportModal() {
  document.getElementById('pwExportModalBackdrop').style.display = 'none';
}

function exportWorkspaceReport(scope = 'day') {
  let md = '# 🚀 Placement Preparation Engineering Log\n\n';
  const exportedOn = formatDateDisplay(getTodayDateKey());
  md += `*Exported on ${exportedOn} • Scope: ${scope === 'day' ? formatDateDisplay(currentWorkspaceDate) : 'Full History'}*\n\n---\n\n`;

  const datesToExport = (scope === 'day')
    ? [currentWorkspaceDate]
    : Array.from(new Set([
        ...plannerTasks.map(t => t.date),
        ...codingLog.map(e => e.date),
        ...Object.keys(potdRecords),
        ...Object.keys(diaryState.entries)
      ])).sort().reverse();

  datesToExport.forEach(dateKey => {
    md += `## 📅 Date: ${formatDateDisplay(dateKey)} (${dateKey})\n\n`;

    // Tasks for day
    const dayTasks = plannerTasks.filter(t => t.date === dateKey);
    if (dayTasks.length > 0) {
      md += `### 📋 Daily Planned Tasks\n`;
      dayTasks.forEach(t => {
        const check = t.completed ? '[x]' : '[ ]';
        md += `- ${check} [${t.priority.toUpperCase()}] **${t.title}** *(${t.category})*\n`;
      });
      md += '\n';
    }

    // LeetCode POTD
    const potd = potdRecords[dateKey];
    if (potd && potd.title) {
      md += `### ⚡ Daily LeetCode Challenge\n`;
      md += `- **Problem:** ${potd.title} (${potd.difficulty || 'Medium'})\n`;
      md += `- **Status:** ${potd.status === 'completed' ? 'Completed ✓' : potd.status}\n`;
      if (potd.notes) md += `- **Notes:** ${potd.notes}\n`;
      md += '\n';
    }

    // Coding Problems Logged
    const dayCode = codingLog.filter(e => e.date === dateKey);
    if (dayCode.length > 0) {
      md += `### 💻 Detailed Coding Solutions & Notes\n`;
      dayCode.forEach(e => {
        md += `#### ${e.title} (${e.platform || 'LeetCode'} • ${e.difficulty || 'Medium'})\n`;
        md += `- **Solve Mode:** ${e.solveStatus === 'independent' ? 'Independent' : 'With Editorial'} • **Time:** ${e.timeSpentMinutes || 0}m\n`;
        if (e.approach) md += `- **Approach:** ${e.approach}\n`;
        if (e.timeComplexity || e.spaceComplexity) md += `- **Complexity:** Time: ${e.timeComplexity || 'N/A'} | Space: ${e.spaceComplexity || 'N/A'}\n`;
        if (e.edgeCases) md += `- **Edge Cases:** ${e.edgeCases}\n`;
        md += '\n';
      });
    }

    // Diary Debrief
    const diary = diaryState.entries[dateKey];
    if (diary && (diary.accomplishments?.trim() || diary.mistakes?.trim() || diary.freeform?.trim())) {
      const moodEmoji = { great: '🤩', good: '😊', neutral: '😐', low: '😔', stressed: '😫' }[diary.mood] || '📝';
      md += `### 📓 Daily Reflection & Debrief\n`;
      md += `**State:** ${moodEmoji} ${diary.mood || 'good'} | **Focus:** ${diary.focusRating || 3}/5 | **Energy:** ${diary.energyRating || 3}/5\n\n`;
      if (diary.accomplishments) md += `**Accomplishments:**\n${diary.accomplishments}\n\n`;
      if (diary.mistakes) md += `**Mistakes & Lessons:**\n${diary.mistakes}\n\n`;
      if (diary.distractions) md += `**Distractions:**\n${diary.distractions}\n\n`;
      if (diary.freeform) md += `**Notes:**\n${diary.freeform}\n\n`;
      if (diary.priorities && diary.priorities.some(Boolean)) {
        md += `**Tomorrow's Priorities:**\n`;
        diary.priorities.forEach((p, idx) => {
          if (p.trim()) {
            const ch = diary.priorityDone?.[idx] ? '[x]' : '[ ]';
            md += `- ${ch} P${idx + 1}: ${p.trim()}\n`;
          }
        });
        md += '\n';
      }
    }

    md += '---\n\n';
  });

  const fileName = `placement_prep_log_${scope === 'day' ? currentWorkspaceDate : 'full_history'}.md`;
  downloadWorkspaceFile(md, fileName, 'text/markdown');
}

function downloadWorkspaceBackupJSON() {
  const bundle = {
    version: '2.0.0',
    exportedAt: new Date().toISOString(),
    tasks: plannerTasks,
    codingLog: codingLog,
    potdRecords: potdRecords,
    routineTemplates: routineTemplates,
    diaryState: diaryState
  };

  const jsonStr = JSON.stringify(bundle, null, 2);
  downloadWorkspaceFile(jsonStr, `workspace_backup_${getTodayDateKey()}.json`, 'application/json');
}

function importWorkspaceBackupJSON(fileInput) {
  const file = fileInput.files?.[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function(e) {
    try {
      const data = JSON.parse(e.target.result);
      if (!data || typeof data !== 'object') {
        alert('Invalid JSON backup file.');
        return;
      }

      // Safe non-corrupting merge
      if (Array.isArray(data.tasks)) {
        plannerTasks = data.tasks;
        saveTasks();
      }
      if (Array.isArray(data.codingLog)) {
        codingLog = data.codingLog;
        saveCodingLog();
      }
      if (data.potdRecords && typeof data.potdRecords === 'object') {
        potdRecords = data.potdRecords;
        savePotdRecords();
      }
      if (Array.isArray(data.routineTemplates)) {
        routineTemplates = data.routineTemplates;
        saveRoutines();
      }
      if (data.diaryState && typeof data.diaryState === 'object') {
        diaryState = data.diaryState;
        saveDiaryToStorage();
      }

      initWorkspace();
      closeExportModal();
      alert('Workspace backup restored successfully ✓');
    } catch (err) {
      alert('Failed to parse backup JSON: ' + err.message);
    }
  };
  reader.readAsText(file);
}

// Utility: Escape HTML
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// --- 15. KEYBOARD SHORTCUTS & EVENT LISTENERS ---
document.addEventListener('keydown', function(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 's') {
    const isPlannerActive = document.getElementById('view-planner')?.classList.contains('active');
    const isDiaryActive = document.getElementById('view-diary')?.classList.contains('active');
    if (isPlannerActive || isDiaryActive) {
      e.preventDefault();
      saveDiaryFromInputs();
      showWorkspaceSaveStatus('● Saved via shortcut ✓');
      setTimeout(() => showWorkspaceSaveStatus('● All changes saved'), 2000);
    }
  }
});

// Auto-initialize workspace when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initWorkspace);
} else {
  initWorkspace();
}
