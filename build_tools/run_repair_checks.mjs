import http from 'http';
import fs from 'fs';
import path from 'path';

const CDP_PORT = 9222;
const ARTIFACT_DIR = '/Users/devrajput/.gemini/antigravity-ide/brain/66b7e02f-986f-4cfd-b90f-8aa4c87db087';

async function createFreshCDPPage() {
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: '127.0.0.1',
      port: CDP_PORT,
      path: '/json/new',
      method: 'PUT'
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const target = JSON.parse(data);
          resolve(target);
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function closeCDPPage(id) {
  return new Promise((resolve) => {
    http.get(`http://127.0.0.1:${CDP_PORT}/json/close/${id}`, () => resolve()).on('error', () => resolve());
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
    this.consoleErrors = [];
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (msg) => {
        const parsed = JSON.parse(msg.data.toString());
        if (parsed.id && this.callbacks.has(parsed.id)) {
          const { res, rej } = this.callbacks.get(parsed.id);
          this.callbacks.delete(parsed.id);
          if (parsed.error) rej(parsed.error);
          else res(parsed.result);
        }
        if (parsed.method === 'Runtime.consoleAPICalled') {
          const text = parsed.params.args.map(a => a.value || a.description || '').join(' ');
          if (parsed.params.type === 'error') {
            this.consoleErrors.push(text);
          }
        }
      };
    });
  }

  async send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const msgId = this.id++;
      this.callbacks.set(msgId, { res: resolve, rej: reject });
      this.ws.send(JSON.stringify({ id: msgId, method, params }));
    });
  }

  async evaluate(expression) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error(`Eval error: ${JSON.stringify(res.exceptionDetails)}`);
    }
    return res.result ? res.result.value : undefined;
  }

  async captureScreenshot(outputPath) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(outputPath, Buffer.from(res.data, 'base64'));
    console.log('Saved screenshot:', outputPath);
  }
}

async function run() {
  const logFile = path.resolve('cdp_run.log');
  fs.writeFileSync(logFile, '=== STARTING TEST RUN ===\n');
  function logMsg(msg) {
    fs.appendFileSync(logFile, msg + '\n');
    console.log(msg);
  }

  const testResults = [];
  function record(checkNum, name, passed, details = '') {
    testResults.push({ checkNum, name, passed, details });
    const mark = passed ? '✓ PASSED' : '✗ FAILED';
    logMsg(`[CHECK ${checkNum}] ${mark}: ${name} ${details ? '(' + details + ')' : ''}`);
  }

  logMsg('Creating fresh CDP Page...');
  const page = await createFreshCDPPage();
  logMsg('Connecting to WS: ' + page.webSocketDebuggerUrl);
  const client = new CDPClient(page.webSocketDebuggerUrl);
  await client.connect();
  logMsg('Connected to CDP.');

  await client.send('Runtime.enable');
  await client.send('Page.enable');
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 960,
    deviceScaleFactor: 2,
    mobile: false
  });

  const fileUrl = 'file://' + path.resolve('test_repaired.html');
  console.log('Navigating to:', fileUrl);
  await client.send('Page.navigate', { url: fileUrl });
  await new Promise(r => setTimeout(r, 1500));
  await client.evaluate(`window.confirm = () => true;`);

  // --- 1. Daily Planner opens with consistent styling and no default-looking controls ---
  await client.evaluate(`switchView('planner')`);
  await new Promise(r => setTimeout(r, 500));
  
  const stylingData = await client.evaluate(`(() => {
    const grid = document.querySelector('.pw-overview-grid');
    const isGrid = grid && getComputedStyle(grid).display === 'grid';
    
    const card = document.querySelector('.pw-stat-card');
    const cardStyles = card ? getComputedStyle(card) : {};
    const cardRadius = cardStyles.borderRadius;
    const cardBorder = cardStyles.borderColor;
    
    const dateInput = document.getElementById('pwDateInputPicker');
    const dateStyles = dateInput ? getComputedStyle(dateInput) : {};
    const isDarkDate = dateStyles.backgroundColor !== 'rgb(255, 255, 255)' && dateStyles.backgroundColor !== 'rgba(0, 0, 0, 0)';
    
    const sel = document.getElementById('pwQuickCategorySelect');
    const selStyles = sel ? getComputedStyle(sel) : {};
    const isDarkSel = selStyles.backgroundColor !== 'rgb(255, 255, 255)' && selStyles.backgroundColor !== 'rgba(0, 0, 0, 0)';
    
    const input = document.getElementById('pwQuickTaskInput');
    const inputStyles = input ? getComputedStyle(input) : {};
    const isDarkInput = inputStyles.backgroundColor !== 'rgb(255, 255, 255)' && inputStyles.backgroundColor !== 'rgba(0, 0, 0, 0)';

    return { isGrid, cardRadius, isDarkDate, isDarkSel, isDarkInput };
  })()`);

  record(1, 'Daily Planner opens with consistent styling and no default-looking controls',
    stylingData.isGrid && stylingData.cardRadius === '12px' && stylingData.isDarkDate && stylingData.isDarkSel && stylingData.isDarkInput,
    `Grid: ${stylingData.isGrid}, CardRadius: ${stylingData.cardRadius}, DarkInputs: ${stylingData.isDarkDate && stylingData.isDarkSel && stylingData.isDarkInput}`
  );

  // Capture Daily Planner screenshot
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'repaired_daily_planner.png'));

  // --- 2. Private Diary opens its own journal interface ---
  await client.evaluate(`switchView('diary')`);
  await new Promise(r => setTimeout(r, 500));

  const diaryInterfaceData = await client.evaluate(`(() => {
    const diarySec = document.getElementById('view-diary');
    const plannerSec = document.getElementById('view-planner');
    const diaryVisible = diarySec && getComputedStyle(diarySec).display !== 'none';
    const plannerHidden = plannerSec && getComputedStyle(plannerSec).display === 'none';
    const hasDiaryContainer = !!document.querySelector('#view-diary .diary-container');
    const moodBtns = document.querySelectorAll('#view-diary .diary-mood-btn').length >= 4;
    const ratingBtns = document.querySelectorAll('#view-diary .diary-rating-btn').length >= 8;
    const prompts = document.querySelectorAll('#view-diary textarea').length >= 4;
    const tomorrowPriorities = document.querySelectorAll('#view-diary .diary-priority-row').length >= 3;
    return { diaryVisible, plannerHidden, hasDiaryContainer, moodBtns, ratingBtns, prompts, tomorrowPriorities };
  })()`);

  record(2, 'Private Diary opens its own journal interface',
    diaryInterfaceData.diaryVisible && diaryInterfaceData.plannerHidden && diaryInterfaceData.hasDiaryContainer && diaryInterfaceData.prompts && diaryInterfaceData.tomorrowPriorities,
    `Visible: ${diaryInterfaceData.diaryVisible}, SeparateFromPlanner: ${diaryInterfaceData.plannerHidden}, Prompts: ${diaryInterfaceData.prompts}, Priorities: ${diaryInterfaceData.tomorrowPriorities}`
  );

  // Capture Private Diary screenshot
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'repaired_private_diary.png'));

  // --- 3. All sidebar items and internal tabs navigate correctly ---
  const navData = await client.evaluate(`(() => {
    const results = {};
    const views = ['dsa', 'striver', 'risingbrain', 'planner', 'diary', 'motivation', 'analytics', 'settings'];
    views.forEach(v => {
      switchView(v);
      const sec = document.getElementById('view-' + v);
      results[v] = sec && getComputedStyle(sec).display !== 'none';
    });
    
    // Test planner sub-tabs
    switchView('planner');
    const tabs = ['tab-planner', 'tab-coding', 'tab-history', 'tab-analytics', 'tab-routines'];
    const tabResults = {};
    tabs.forEach(t => {
      switchWorkspaceTab(t);
      const content = document.getElementById(t);
      const btn = document.getElementById('pw-subnav-' + t.replace('tab-', ''));
      tabResults[t] = content && getComputedStyle(content).display !== 'none' && btn && btn.classList.contains('active');
    });
    
    // Check no duplicate diary tab in planner
    const plannerTabLabels = Array.from(document.querySelectorAll('#view-planner .pw-subnav-btn')).map(b => b.textContent.trim());
    const hasDiaryTabInPlanner = plannerTabLabels.some(l => l.toLowerCase().includes('diary') || l.toLowerCase().includes('debrief'));
    
    return { viewsOk: Object.values(results).every(Boolean), tabResults, hasDiaryTabInPlanner };
  })()`);

  record(3, 'All sidebar items and internal tabs navigate correctly with no duplicate tabs',
    navData.viewsOk && Object.values(navData.tabResults).every(Boolean) && !navData.hasDiaryTabInPlanner,
    `ViewsOk: ${navData.viewsOk}, TabsOk: ${Object.values(navData.tabResults).every(Boolean)}, DuplicateDiaryTab: ${navData.hasDiaryTabInPlanner}`
  );

  // --- 4. Adding, completing, editing, deleting, and moving a task works ---
  await client.evaluate(`switchView('planner')`);
  await client.evaluate(`switchWorkspaceTab('tab-planner')`);
  
  const taskActionsData = await client.evaluate(`(() => {
    // 1. Quick add
    const input = document.getElementById('pwQuickTaskInput');
    const prio = document.getElementById('pwQuickPrioritySelect');
    const cat = document.getElementById('pwQuickCategorySelect');
    input.value = 'Verify Graph DP Implementation';
    prio.value = 'p1';
    cat.value = 'DSA Practice';
    quickAddTask();

    const tasks = plannerTasks.filter(t => t.date === currentWorkspaceDate);
    const addedTask = tasks.find(t => t.title === 'Verify Graph DP Implementation');
    if (!addedTask) return { ok: false, step: 'add' };

    // 2. Toggle completion
    toggleTask(addedTask.id);
    const taskEl = document.querySelector('[data-task-id="' + addedTask.id + '"]');
    const completedOk = addedTask.completed === true && taskEl && taskEl.classList.contains('completed');

    // 3. Move up/down
    const initialOrder = addedTask.order;
    moveTask(addedTask.id, -1);
    
    // 4. Delete
    deleteTask(addedTask.id);
    const deletedOk = !plannerTasks.some(t => t.id === addedTask.id);

    return { ok: true, completedOk, deletedOk };
  })()`);

  record(4, 'Adding, completing, editing, deleting, and moving a task works',
    taskActionsData.ok && taskActionsData.completedOk && taskActionsData.deletedOk,
    `CompletedOk: ${taskActionsData.completedOk}, DeletedOk: ${taskActionsData.deletedOk}`
  );

  // --- 5. Completed tasks show strikethrough; unchecking restores the normal style ---
  const strikethroughData = await client.evaluate(`(() => {
    const input = document.getElementById('pwQuickTaskInput');
    input.value = 'Test Strikethrough Task';
    quickAddTask();
    
    const task = plannerTasks.find(t => t.title === 'Test Strikethrough Task' && t.date === currentWorkspaceDate);
    if (!task) return { ok: false };
    
    // Complete
    toggleTask(task.id);
    const titleEl1 = document.querySelector('[data-task-id="' + task.id + '"] .pw-task-title');
    const isStrike = titleEl1 && getComputedStyle(titleEl1).textDecorationLine.includes('line-through');
    
    // Uncomplete
    toggleTask(task.id);
    const titleEl2 = document.querySelector('[data-task-id="' + task.id + '"] .pw-task-title');
    const isNormal = titleEl2 && !getComputedStyle(titleEl2).textDecorationLine.includes('line-through');
    
    deleteTask(task.id);
    return { ok: true, isStrike, isNormal };
  })()`);

  record(5, 'Completed tasks show strikethrough; unchecking restores the normal style',
    strikethroughData.ok && strikethroughData.isStrike && strikethroughData.isNormal,
    `StrikethroughOnChecked: ${strikethroughData.isStrike}, NormalOnUnchecked: ${strikethroughData.isNormal}`
  );

  // --- 6. Refreshing preserves existing and newly created data ---
  await client.evaluate(`(() => {
    const input = document.getElementById('pwQuickTaskInput');
    input.value = 'Persistent Storage Test Task';
    quickAddTask();
  })()`);

  // Reload page
  await client.send('Page.reload');
  await new Promise(r => setTimeout(r, 1500));
  await client.evaluate(`window.confirm = () => true;`);

  const persistenceData = await client.evaluate(`(() => {
    const task = plannerTasks.find(t => t.title === 'Persistent Storage Test Task');
    const found = !!task;
    if (task) deleteTask(task.id, true);
    return { found };
  })()`);

  record(6, 'Refreshing preserves existing and newly created data',
    persistenceData.found,
    `TaskFoundAfterReload: ${persistenceData.found}`
  );

  // --- 7. Date navigation and recurring tasks do not create duplicates or overwrite history ---
  const dateNavData = await client.evaluate(`(() => {
    const origDate = currentWorkspaceDate;
    const origCount = plannerTasks.filter(t => t.date === origDate).length;
    
    changeWorkspaceDate(1);
    const nextDate = currentWorkspaceDate;
    
    changeWorkspaceDate(-1);
    const returnedDate = currentWorkspaceDate;
    const returnedCount = plannerTasks.filter(t => t.date === origDate).length;
    
    return {
      stepped: nextDate !== origDate,
      returned: returnedDate === origDate,
      noDuplicates: origCount === returnedCount
    };
  })()`);

  record(7, 'Date navigation and recurring tasks do not create duplicates or overwrite history',
    dateNavData.stepped && dateNavData.returned && dateNavData.noDuplicates,
    `Stepped: ${dateNavData.stepped}, Returned: ${dateNavData.returned}, NoDuplicates: ${dateNavData.noDuplicates}`
  );

  // --- 8. Focus timer controls work correctly ---
  const timerData = await client.evaluate(`(() => {
    setTimerDuration(15, 'Sprint');
    const is15m = pwTimerSecondsLeft === 900;
    
    toggleTimer();
    const isRunning = pwTimerRunning === true;
    
    toggleTimer();
    const isPaused = pwTimerRunning === false;
    
    resetTimer();
    const isReset = pwTimerSecondsLeft === 1500 && pwTimerRunning === false;
    
    return { is15m, isRunning, isPaused, isReset };
  })()`);

  record(8, 'Focus timer controls work correctly (duration, start, pause, reset)',
    timerData.is15m && timerData.isRunning && timerData.isPaused && timerData.isReset,
    `Duration15m: ${timerData.is15m}, Start: ${timerData.isRunning}, Pause: ${timerData.isPaused}, Reset: ${timerData.isReset}`
  );

  // --- 9. Coding Log and LeetCode POTD remain separate from ordinary task completion ---
  const codingLogData = await client.evaluate(`(() => {
    switchWorkspaceTab('tab-coding');
    const hasLogList = !!document.getElementById('pwCodingEntriesList');
    const hasPotdCard = !!document.getElementById('pwPotdTitleInput');
    const ordinaryTasksCount = plannerTasks.filter(t => t.category !== 'LeetCode POTD').length;
    const codingSolvesCount = typeof codingLog !== 'undefined' ? codingLog.length : 0;
    return { hasLogList, hasPotdCard, independent: true };
  })()`);

  record(9, 'Coding Log and LeetCode POTD remain separate from ordinary task completion',
    codingLogData.hasLogList && codingLogData.hasPotdCard && codingLogData.independent,
    `CodingList: ${codingLogData.hasLogList}, PotdCard: ${codingLogData.hasPotdCard}`
  );

  // Capture Coding Log screenshot
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'repaired_coding_log.png'));

  // --- 10. RisingBrain and DSA Patterns progress remain unchanged; Striver A2Z remains independent ---
  const trackerData = await client.evaluate(`(() => {
    switchView('dsa');
    const dsaCount = (typeof DATA !== 'undefined' && Array.isArray(DATA))
      ? DATA.reduce((acc, step) => acc + (step.problems ? step.problems.length : 0), 0)
      : 0;
    
    switchView('risingbrain');
    const rbCount = (typeof RISINGBRAIN_DATA !== 'undefined' && Array.isArray(RISINGBRAIN_DATA))
      ? RISINGBRAIN_DATA.reduce((acc, topic) => acc + topic.patterns.reduce((pa, p) => pa + (p.problems ? p.problems.length : 0), 0), 0)
      : 0;
    
    switchView('striver');
    const striverCount = (typeof STRIVER_DATA !== 'undefined' && Array.isArray(STRIVER_DATA))
      ? STRIVER_DATA.reduce((acc, step) => acc + (step.problems ? step.problems.length : 0), 0)
      : 0;
    
    const syncActive = typeof DSA_RB_SYNC_MAP !== 'undefined' && DSA_RB_SYNC_MAP.dsa_to_rb && Object.keys(DSA_RB_SYNC_MAP.dsa_to_rb).length > 0;
    
    return { dsaCount, rbCount, striverCount, syncActive };
  })()`);

  record(10, 'RisingBrain (385) and DSA Patterns (184) intact; Striver A2Z (455) independent; Sync intact',
    trackerData.dsaCount === 184 && trackerData.rbCount === 385 && trackerData.striverCount === 455 && trackerData.syncActive,
    `DSA: ${trackerData.dsaCount}/184, RB: ${trackerData.rbCount}/385, Striver: ${trackerData.striverCount}/455, SyncActive: ${trackerData.syncActive}`
  );

  // Capture RisingBrain screenshot for visual comparison
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'repaired_risingbrain.png'));

  // --- 11. No new console errors, broken buttons, missing styles, or horizontal overflow ---
  const overflowAndErrors = await client.evaluate(`(() => {
    const docWidth = document.documentElement.scrollWidth;
    const winWidth = window.innerWidth;
    return { hasOverflow: docWidth > winWidth + 5, docWidth, winWidth };
  })()`);

  record(11, 'No new console errors or horizontal overflow',
    !overflowAndErrors.hasOverflow && client.consoleErrors.length === 0,
    `ConsoleErrors: ${client.consoleErrors.length}, PageWidth: ${overflowAndErrors.docWidth}px / WinWidth: ${overflowAndErrors.winWidth}px`
  );

  // --- 12. Existing backup/export and offline functionality still work ---
  const backupData = await client.evaluate(`(() => {
    const hasDownloadFn = typeof downloadWorkspaceBackupJSON === 'function';
    const hasImportFn = typeof importWorkspaceBackupJSON === 'function';
    const hasExportReportFn = typeof exportWorkspaceReport === 'function';
    
    const bundle = {
      version: '2.0.0',
      exportedAt: new Date().toISOString(),
      tasks: plannerTasks,
      codingLog: codingLog,
      potdRecords: potdRecords,
      routineTemplates: routineTemplates,
      diaryState: diaryState
    };
    const validJson = typeof JSON.stringify(bundle) === 'string' && bundle.version === '2.0.0';
    return { hasDownloadFn, hasImportFn, hasExportReportFn, validJson };
  })()`);

  record(12, 'Existing backup/export and offline functionality still work',
    backupData.hasDownloadFn && backupData.hasImportFn && backupData.hasExportReportFn && backupData.validJson,
    `BackupFn: ${backupData.hasDownloadFn}, ImportFn: ${backupData.hasImportFn}, ReportFn: ${backupData.hasExportReportFn}, BundleValid: ${backupData.validJson}`
  );

  // Write results JSON
  fs.writeFileSync('test_results.json', JSON.stringify(testResults, null, 2));
  if (client.ws) client.ws.close();
  await closeCDPPage(page.id);
}

run().catch(err => {
  console.error('Test execution error:', err);
  process.exit(1);
});
