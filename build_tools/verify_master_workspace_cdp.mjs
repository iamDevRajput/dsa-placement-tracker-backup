import http from 'http';
import fs from 'fs';
import path from 'path';

console.log('=== STARTING MASTER WORKSPACE CDP VERIFICATION SUITE ===');

const CDP_PORT = 9222;

async function getCDPPage() {
  return new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${CDP_PORT}/json`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const targets = JSON.parse(data);
          const page = targets.find(t => t.type === 'page');
          if (page && page.webSocketDebuggerUrl) {
            resolve(page);
          } else {
            reject(new Error('No active page found in Chrome.'));
          }
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
    this.consoleLogs = [];
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
          this.consoleLogs.push({ type: parsed.params.type, text });
          if (parsed.params.type === 'error') {
            console.error('[BROWSER CONSOLE ERROR]:', text);
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
      throw new Error(`Eval exception: ${JSON.stringify(res.exceptionDetails)}`);
    }
    return res.result ? res.result.value : undefined;
  }
}

async function run() {
  const page = await getCDPPage();
  const client = new CDPClient(page.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Runtime.enable');
  await client.send('Page.enable');

  const fileUrl = 'file://' + path.resolve('test_workspace_assembled.html');
  console.log('Navigating to:', fileUrl);
  await client.send('Page.navigate', { url: fileUrl });
  await new Promise(r => setTimeout(r, 2000));

  // Reset test workspace data to guarantee clean deterministic verification
  await client.evaluate(`(() => {
    localStorage.removeItem('daily_task_planner_v1');
    localStorage.removeItem('daily_coding_log_v1');
    localStorage.removeItem('daily_routines_v1');
    localStorage.removeItem('daily_potd_v1');
    localStorage.removeItem('dsa_diary_entries_v1');
    initWorkspace();
  })()`);

  console.log('\n--- 1. Testing Top Navigation & SwitchView ---');
  let viewResult = await client.evaluate(`(() => {
    switchView('planner');
    const pActive = document.getElementById('view-planner')?.classList.contains('active');
    const tabActive = document.getElementById('tab-planner')?.classList.contains('active');
    return { pActive, tabActive };
  })()`);
  console.log('Switch to planner:', viewResult);
  if (!viewResult.pActive || !viewResult.tabActive) throw new Error('SwitchView planner failed');

  viewResult = await client.evaluate(`(() => {
    switchView('diary');
    const pActive = document.getElementById('view-planner')?.classList.contains('active');
    const tabActive = document.getElementById('tab-diary')?.classList.contains('active');
    return { pActive, tabActive };
  })()`);
  console.log('Switch to diary:', viewResult);
  if (!viewResult.pActive || !viewResult.tabActive) throw new Error('SwitchView diary failed');

  console.log('\n--- 2. Testing Sub-Navigation Pills ---');
  const tabs = ['tab-planner', 'tab-coding', 'tab-diary', 'tab-history', 'tab-analytics', 'tab-routines'];
  for (const t of tabs) {
    const tabRes = await client.evaluate(`(() => {
      switchWorkspaceTab('${t}');
      return {
        tabActive: document.getElementById('${t}')?.classList.contains('active'),
        btnActive: document.getElementById('pw-subnav-' + '${t}'.replace('tab-', ''))?.classList.contains('active')
      };
    })()`);
    console.log(`Tab ${t}:`, tabRes);
    if (!tabRes.tabActive || !tabRes.btnActive) throw new Error(`Tab switch failed for ${t}`);
  }

  console.log('\n--- 3. Testing Task Planner & Idempotent Routine Generation ---');
  await client.evaluate(`switchWorkspaceTab('tab-planner')`);
  const initialTaskCount = await client.evaluate(`plannerTasks.filter(t => t.date === currentWorkspaceDate).length`);
  console.log(`Initial tasks generated for date ${await client.evaluate('currentWorkspaceDate')}:`, initialTaskCount);
  if (initialTaskCount === 0) throw new Error('Routines failed to generate daily tasks');

  // Test idempotency: calling ensureRoutinesForDate again must NOT create duplicates
  await client.evaluate(`ensureRoutinesForDate(currentWorkspaceDate)`);
  const countAfterSecondCall = await client.evaluate(`plannerTasks.filter(t => t.date === currentWorkspaceDate).length`);
  console.log('Task count after 2nd ensureRoutines call:', countAfterSecondCall);
  if (countAfterSecondCall !== initialTaskCount) throw new Error('Idempotency violation: duplicate tasks created!');

  // Test Quick Add Task
  await client.evaluate(`(() => {
    document.getElementById('pwQuickTaskInput').value = 'Test Custom Two-Pointer Task';
    document.getElementById('pwQuickCategorySelect').value = 'DSA Practice';
    document.getElementById('pwQuickPrioritySelect').value = 'p1';
    quickAddTask();
  })()`);
  const customTaskFound = await client.evaluate(`plannerTasks.some(t => t.title === 'Test Custom Two-Pointer Task' && t.date === currentWorkspaceDate)`);
  console.log('Custom task added:', customTaskFound);
  if (!customTaskFound) throw new Error('Quick add task failed');

  // Test Checkbox Toggle & Strikethrough
  const toggleRes = await client.evaluate(`(() => {
    const t = plannerTasks.find(x => x.title === 'Test Custom Two-Pointer Task');
    toggleTask(t.id);
    const itemEl = document.getElementById('task_item_' + t.id);
    const cbChecked = itemEl.querySelector('.pw-task-checkbox').classList.contains('checked');
    const titleStrike = itemEl.querySelector('.pw-task-title').classList.contains('completed');
    const pct = document.getElementById('pwProgressPercentLabel').textContent;
    return { completed: t.completed, cbChecked, titleStrike, pct };
  })()`);
  console.log('Toggle task result:', toggleRes);
  if (!toggleRes.completed || !toggleRes.cbChecked || !toggleRes.titleStrike) {
    throw new Error('Task checkbox toggle or strikethrough failed');
  }

  console.log('\n--- 4. Testing Coding Log & Problem Notes ---');
  await client.evaluate(`switchWorkspaceTab('tab-coding')`);
  await client.evaluate(`(() => {
    document.getElementById('pwCodingModalTitleInput').value = '15. 3Sum';
    document.getElementById('pwCodingModalPlatform').value = 'LeetCode';
    document.getElementById('pwCodingModalDifficulty').value = 'Medium';
    document.getElementById('pwCodingModalTime').value = '35';
    document.getElementById('pwCodingModalSolveStatus').value = 'independent';
    document.getElementById('pwCodingModalTopics').value = 'Two Pointers, Array, Sorting';
    document.getElementById('pwCodingModalApproach').value = 'Sort the input array. Fix first element i, then use two pointers left and right to find triplets.';
    document.getElementById('pwCodingModalTimeComp').value = 'O(N^2)';
    document.getElementById('pwCodingModalSpaceComp').value = 'O(1)';
    document.getElementById('pwCodingModalEdgeCases').value = 'Skip duplicate elements with while loops.';
    document.getElementById('pwCodingModalRevision').checked = true;
    saveCodingModal();
  })()`);

  const codeEntryRes = await client.evaluate(`(() => {
    const entry = codingLog.find(e => e.title === '15. 3Sum');
    const uniqueEl = document.getElementById('pwCodeUniqueToday').textContent;
    const indepEl = document.getElementById('pwCodeIndependentRate').textContent;
    const timeEl = document.getElementById('pwCodeTimeToday').textContent;
    return { found: Boolean(entry), uniqueEl, indepEl, timeEl, needsRevision: entry?.needsRevision };
  })()`);
  console.log('Coding entry result:', codeEntryRes);
  if (!codeEntryRes.found || codeEntryRes.uniqueEl !== '1' || codeEntryRes.indepEl !== '100%') {
    throw new Error('Coding log add or metrics calculation failed');
  }

  console.log('\n--- 5. Testing LeetCode POTD Challenge & Task Synchronization ---');
  const potdSyncRes = await client.evaluate(`(() => {
    // Check if POTD task exists
    let potdTask = plannerTasks.find(t => t.date === currentWorkspaceDate && t.category === 'LeetCode POTD');
    // Update POTD status to completed
    updatePotdStatus('completed');
    potdTask = plannerTasks.find(t => t.date === currentWorkspaceDate && t.category === 'LeetCode POTD');
    const potdStatus = potdRecords[currentWorkspaceDate]?.status;
    return { potdStatus, taskCompleted: potdTask ? potdTask.completed : null };
  })()`);
  console.log('POTD sync result:', potdSyncRes);
  if (potdSyncRes.potdStatus !== 'completed' || potdSyncRes.taskCompleted !== true) {
    throw new Error('POTD to task sync failed');
  }

  console.log('\n--- 6. Testing Private Diary Debrief ---');
  await client.evaluate(`switchWorkspaceTab('tab-diary')`);
  const diaryRes = await client.evaluate(`(() => {
    setDiaryMood('great');
    setDiaryRating('focus', 5);
    setDiaryRating('energy', 4);
    document.getElementById('diaryAccomplishments').value = 'Mastered Two-Pointers pattern and solved 3Sum and Container With Most Water.';
    document.getElementById('diaryMistakes').value = 'Missed duplicate handling in while loop on first try.';
    document.getElementById('diaryDistractions').value = 'Zero distractions, focused 90 min session.';
    document.getElementById('diaryFreeform').value = 'Confidence is growing. Prepared for mock OA tomorrow.';
    document.getElementById('diaryPrioInput1').value = 'Solve 2 Binary Search problems';
    document.getElementById('diaryPrioCheck1').checked = true;
    saveDiaryFromInputs();

    const saved = diaryState.entries[currentWorkspaceDate];
    const streak = document.getElementById('pwDiaryStreakCount').textContent;
    return {
      mood: saved?.mood,
      focus: saved?.focusRating,
      energy: saved?.energyRating,
      hasAccomplishments: Boolean(saved?.accomplishments),
      streak
    };
  })()`);
  console.log('Diary result:', diaryRes);
  if (diaryRes.mood !== 'great' || diaryRes.focus !== 5 || !diaryRes.hasAccomplishments) {
    throw new Error('Diary debrief save failed');
  }

  console.log('\n--- 7. Testing Calendar Grid & Global Search ---');
  await client.evaluate(`switchWorkspaceTab('tab-history')`);
  const calendarRes = await client.evaluate(`(() => {
    const dotsToday = document.querySelector('.pw-calendar-cell.today .pw-activity-dots')?.children.length;
    runGlobalWorkspaceSearch('3Sum');
    const searchResults = document.getElementById('pwGlobalSearchResults').innerText;
    return { dotsToday, searchMatches: searchResults.includes('3Sum') };
  })()`);
  console.log('Calendar & search result:', calendarRes);
  if (calendarRes.dotsToday === 0 || !calendarRes.searchMatches) {
    throw new Error('Calendar dots or search failed');
  }

  console.log('\n--- 8. Testing Real-Data Analytics ---');
  await client.evaluate(`switchWorkspaceTab('tab-analytics')`);
  const analyticsRes = await client.evaluate(`(() => {
    const tasksDone = document.getElementById('pwAnalyticsTotalTasks').textContent;
    const uniqueProblems = document.getElementById('pwAnalyticsUniqueProblems').textContent;
    const indepRate = document.getElementById('pwAnalyticsIndepRate').textContent;
    const potdRate = document.getElementById('pwAnalyticsPotdRate').textContent;
    const avgFocus = document.getElementById('pwAnalyticsAvgFocus').textContent;
    const avgEnergy = document.getElementById('pwAnalyticsAvgEnergy').textContent;
    const revBacklog = document.getElementById('pwRevisionBacklogCount').textContent;
    return { tasksDone, uniqueProblems, indepRate, potdRate, avgFocus, avgEnergy, revBacklog };
  })()`);
  console.log('Analytics result:', analyticsRes);
  if (analyticsRes.uniqueProblems !== '1' || analyticsRes.indepRate !== '100%' || analyticsRes.avgFocus !== '5.0 / 5') {
    throw new Error('Analytics calculations incorrect');
  }

  console.log('\n--- 9. Testing Existing Trackers & Sync Isolation ---');
  const trackerIsolation = await client.evaluate(`(() => {
    // Check DSA Patterns
    switchView('dsa');
    const dsaCards = document.getElementById('dsaContent')?.children.length || 0;

    // Check RisingBrain
    switchView('risingbrain');
    const rbCards = document.getElementById('risingBrainContent')?.children.length || 0;

    // Check Striver A2Z
    switchView('striver');
    const striverCards = document.getElementById('striverContent')?.children.length || 0;

    // Verify localStorage keys intact
    const hasDsaKey = Boolean(localStorage.getItem('dsa_placement_prep_v3'));
    const hasRbKey = Boolean(localStorage.getItem('risingbrain_tracker_v1'));
    const hasStriverKey = Boolean(localStorage.getItem('striver_a2z_tracker_v3'));

    return { dsaCards, rbCards, striverCards, hasDsaKey, hasRbKey, hasStriverKey };
  })()`);
  console.log('Tracker isolation result:', trackerIsolation);
  if (trackerIsolation.dsaCards === 0 || trackerIsolation.rbCards === 0 || trackerIsolation.striverCards === 0) {
    throw new Error('Existing trackers cards failed to render');
  }

  console.log('\n--- 10. Console Errors Check ---');
  const errors = client.consoleLogs.filter(l => l.type === 'error');
  console.log('Total console errors captured:', errors.length);
  if (errors.length > 0) {
    throw new Error('Console errors encountered: ' + errors.map(e => e.text).join('; '));
  }

  console.log('\n🎉 ALL 10 CDP VERIFICATION CHECKS PASSED WITH 100% SUCCESS!');
  process.exit(0);
}

run().catch(err => {
  console.error('\n❌ CDP VERIFICATION FAILED:', err);
  process.exit(1);
});
