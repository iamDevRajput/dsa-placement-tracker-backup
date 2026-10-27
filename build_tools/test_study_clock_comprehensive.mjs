import http from 'http';
import { spawn } from 'child_process';

const CDP_PORT = 9222;
const TARGET_URL = 'file:///Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html';

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
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
      };
    });
  }

  async send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.callbacks.set(id, { res: resolve, rej: reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error(`Eval failed: ${JSON.stringify(res.exceptionDetails)}`);
    }
    return res.result ? res.result.value : undefined;
  }
}

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
          resolve(JSON.parse(data));
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

async function run() {
  console.log('--- Launching Headless Chrome for Minimal Study Clock Verification ---');
  const chromeProcess = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    `--remote-debugging-port=${CDP_PORT}`,
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=/tmp/chrome_test_profile_' + Date.now()
  ]);

  let portOpen = false;
  for (let i = 0; i < 30; i++) {
    try {
      await new Promise(r => setTimeout(r, 200));
      const res = await fetch(`http://127.0.0.1:${CDP_PORT}/json/version`);
      if (res.ok) { portOpen = true; break; }
    } catch (e) {}
  }
  if (!portOpen) throw new Error('Could not connect to Chrome debugging port.');

  const page = await createFreshCDPPage();
  const client = new CDPClient(page.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Page.enable');
  await client.send('Runtime.enable');

  console.log('Navigating to:', TARGET_URL);
  await client.send('Page.navigate', { url: TARGET_URL });
  await new Promise(r => setTimeout(r, 2000));

  console.log('\n======================================================');
  console.log('TEST SUITE: MINIMAL STUDY CLOCK VERIFICATION');
  console.log('======================================================');

  // Test 1: Switch to Study Clock
  await client.evaluate(`switchView('studyclock')`);
  await new Promise(r => setTimeout(r, 300));

  const initUI = await client.evaluate(`(() => {
    return {
      digits: document.getElementById('scClockDigits')?.textContent.trim(),
      btnStart: document.getElementById('scBtnStart')?.style.display,
      btnPause: document.getElementById('scBtnPause')?.style.display,
      btnResume: document.getElementById('scBtnResume')?.style.display,
      btnCorrect: document.getElementById('scBtnCorrect')?.style.display,
      btnStop: document.getElementById('scBtnStop')?.style.display,
      btnReset: document.getElementById('scBtnReset')?.style.display,
      noBanners: document.getElementById('scReviewBanner') === null,
      noPeriodTabs: document.querySelector('.sc-period-tabs') === null
    };
  })()`);

  console.log('[TEST 1] Initial Clean Layout Check:', initUI);
  if (!initUI.noBanners) throw new Error('Unnecessary banners should not exist');
  if (!initUI.noPeriodTabs) throw new Error('Unnecessary period tabs should not exist');
  if (initUI.btnStart === 'none') throw new Error('Start button should be visible when stopped');
  if (initUI.btnReset !== 'none') throw new Error('Reset button should be hidden when stopped');
  console.log('✓ Initial UI matches clean original layout with no extra banners or tabs.');

  // Test 2: Start session, verify Reset button is visible alongside existing controls
  console.log('\n[TEST 2] Starting session & testing Reset button on unlogged session...');
  await client.evaluate(`(() => {
    document.getElementById('scCategorySelect').value = 'Core Subjects';
    document.getElementById('scSessionNotesInput').value = 'OS Scheduling Algorithms';
    startStudyClock();
  })()`);
  await new Promise(r => setTimeout(r, 1500));

  const runningState = await client.evaluate(`(() => {
    return {
      status: studyClockActiveSession.status,
      elapsedSec: Math.floor(getStudyClockElapsedMs() / 1000),
      btnPause: document.getElementById('scBtnPause')?.style.display,
      btnStop: document.getElementById('scBtnStop')?.style.display,
      btnReset: document.getElementById('scBtnReset')?.style.display
    };
  })()`);
  console.log('Running state with Reset button:', runningState);
  if (runningState.status !== 'running') throw new Error('Expected status running');
  if (runningState.btnReset === 'none') throw new Error('Reset button should be visible during active session');

  // Add 1 completed mock session to history to verify Reset NEVER deletes completed records
  await client.evaluate(`(() => {
    studyClockHistory.sessions.push({
      id: 'sc_test_existing_record',
      date: getTodayKey(),
      startTime: '10:00',
      endTime: '11:00',
      durationSeconds: 3600,
      durationFormatted: '01:00:00',
      category: 'DSA',
      notes: 'Historical completed session'
    });
    saveStudyClockHistory();
  })()`);

  // Execute Reset (auto-confirm)
  await client.evaluate(`(() => {
    window.confirm = () => true;
    resetCurrentStudySession();
  })()`);
  await new Promise(r => setTimeout(r, 300));

  const postResetState = await client.evaluate(`(() => {
    return {
      status: studyClockActiveSession.status,
      accumulatedMs: studyClockActiveSession.accumulatedMs,
      digits: document.getElementById('scClockDigits')?.textContent.trim(),
      btnStart: document.getElementById('scBtnStart')?.style.display,
      btnReset: document.getElementById('scBtnReset')?.style.display,
      historyLength: studyClockHistory.sessions.length,
      historyFirstId: studyClockHistory.sessions[0].id
    };
  })()`);
  console.log('Post-Reset State:', postResetState);
  if (postResetState.status !== 'stopped') throw new Error('Session should be stopped after reset');
  if (postResetState.digits !== '00:00:00') throw new Error('Timer digits should reset to 00:00:00');
  if (postResetState.historyLength !== 1 || postResetState.historyFirstId !== 'sc_test_existing_record') {
    throw new Error('Reset affected historical completed records!');
  }
  console.log('✓ Reset button successfully resets ONLY unlogged session; preserves all completed sessions.');

  // Test 3: Start new session, pause, verify Correct Duration button appears beside Resume & Stop
  console.log('\n[TEST 3] Testing Pause & Correct Duration button...');
  await client.evaluate(`(() => {
    document.getElementById('scCategorySelect').value = 'Core Subjects';
    document.getElementById('scSessionNotesInput').value = 'OS Deadlocks & Bankers Algorithm';
    startStudyClock();
  })()`);
  await new Promise(r => setTimeout(r, 1500));

  // Pause
  await client.evaluate(`pauseStudyClock()`);
  await new Promise(r => setTimeout(r, 400));

  const pausedButtons = await client.evaluate(`(() => {
    return {
      status: studyClockActiveSession.status,
      btnResume: document.getElementById('scBtnResume')?.style.display,
      btnCorrect: document.getElementById('scBtnCorrect')?.style.display,
      btnStop: document.getElementById('scBtnStop')?.style.display,
      btnReset: document.getElementById('scBtnReset')?.style.display
    };
  })()`);
  console.log('Paused Controls:', pausedButtons);
  if (pausedButtons.btnResume === 'none') throw new Error('Resume button should be visible');
  if (pausedButtons.btnCorrect === 'none') throw new Error('Correct Duration button should be visible when paused');
  if (pausedButtons.btnStop === 'none') throw new Error('Stop button should be visible');
  if (pausedButtons.btnReset === 'none') throw new Error('Reset button should be visible');
  console.log('✓ Correct Duration and Reset buttons appear cleanly beside Resume & Stop.');

  // Test 4: Correct Duration Modal & Exclude idle/sleep helper
  console.log('\n[TEST 4] Testing Manual Correction & Idle Exclusion helper...');
  await client.evaluate(`openCorrectDurationModal()`);
  await new Promise(r => setTimeout(r, 300));

  // Verify modal is open and has actual duration inputs
  const modalOpen = await client.evaluate(`document.getElementById('modalCorrectStudySession')?.classList.contains('active')`);
  if (!modalOpen) throw new Error('Correction modal did not open');

  // Test idle exclusion deduction helper: simulate 3 hours total wall-clock, 1 hour idle to exclude
  await client.evaluate(`(() => {
    studyClockActiveSession.startedAt = Date.now() - (3 * 3600 * 1000); // 3 hours ago
    document.getElementById('scExcludeHours').value = '1';
    document.getElementById('scExcludeMinutes').value = '0';
    applyDeductionFromWallClock();
  })()`);

  const helperDeducted = await client.evaluate(`(() => {
    return {
      h: document.getElementById('scCorrectHours')?.value,
      m: document.getElementById('scCorrectMinutes')?.value,
      preview: document.getElementById('scCorrectPreviewDuration')?.textContent.trim()
    };
  })()`);
  console.log('Helper Deduction result (3h elapsed - 1h idle = 2h study):', helperDeducted);
  if (helperDeducted.h !== '2' || helperDeducted.m !== '0') {
    throw new Error('Helper deduction failed! Expected 2h 0m, got ' + helperDeducted.h + 'h ' + helperDeducted.m + 'm');
  }

  // Now test user manually overriding/entering actual duration directly: 1 hour 45 minutes
  // "The manually entered actual study duration must be the final value, with no double subtraction."
  await client.evaluate(`(() => {
    document.getElementById('scCorrectHours').value = '1';
    document.getElementById('scCorrectMinutes').value = '45';
    onCorrectDurationInputChange();
    submitCorrectDuration(false); // Save to timer
  })()`);
  await new Promise(r => setTimeout(r, 300));

  const activeTimerCorrected = await client.evaluate(`(() => {
    return {
      modalActive: document.getElementById('modalCorrectStudySession')?.classList.contains('active'),
      digits: document.getElementById('scClockDigits')?.textContent.trim(),
      accumulatedSec: Math.floor(studyClockActiveSession.accumulatedMs / 1000)
    };
  })()`);
  console.log('Active timer after manual correction:', activeTimerCorrected);
  if (activeTimerCorrected.modalActive) throw new Error('Modal should close after saving');
  if (activeTimerCorrected.digits !== '01:45:00') {
    throw new Error('Timer digits expected 01:45:00, got ' + activeTimerCorrected.digits);
  }
  if (activeTimerCorrected.accumulatedSec !== 105 * 60) {
    throw new Error('Double subtraction occurred or value incorrect! Expected 6300s, got ' + activeTimerCorrected.accumulatedSec);
  }
  console.log('✓ Manually entered actual duration is the exact final value with zero double subtraction.');

  // Test 5: Log the session and verify reports
  console.log('\n[TEST 5] Logging session & checking reports...');
  await client.evaluate(`stopAndLogStudySession()`);
  await new Promise(r => setTimeout(r, 500));

  const reportData = await client.evaluate(`(() => {
    const latest = studyClockHistory.sessions[0];
    const todayStat = document.getElementById('scStatTodayHours')?.textContent.trim();
    const metrics = calculateStudyClockMetrics();
    return {
      latest,
      todayStat,
      coreSec: metrics.categoryTotals['Core Subjects']
    };
  })()`);
  console.log('Logged Session Data:', reportData.latest);
  console.log('Today Stat:', reportData.todayStat);
  if (reportData.latest.durationSeconds !== 105 * 60) {
    throw new Error('Logged duration expected 6300s (1h 45m), got ' + reportData.latest.durationSeconds);
  }
  if (reportData.coreSec !== 105 * 60) {
    throw new Error('Category totals Core Subjects expected 6300s, got ' + reportData.coreSec);
  }
  console.log('✓ Logged session and report calculations 100% accurate.');

  // Test 6: Reload persistence and computer sleep protection
  console.log('\n[TEST 6] Testing reload persistence & sleep gap protection...');
  // Start a new session
  await client.evaluate(`startStudyClock()`);
  await new Promise(r => setTimeout(r, 1000));

  // Quick reload
  await client.send('Page.reload');
  await new Promise(r => setTimeout(r, 1500));
  await client.evaluate(`switchView('studyclock')`);

  const postReloadRunning = await client.evaluate(`studyClockActiveSession.status`);
  if (postReloadRunning !== 'running') throw new Error('Session should stay running after quick reload');
  console.log('✓ Quick reload persistence verified.');

  // Simulate computer sleep: gap > 5m in ticker
  await client.evaluate(`studyClockActiveSession.lastHeartbeat = Date.now() - (30 * 60 * 1000)`); // 30m ago
  await new Promise(r => setTimeout(r, 800));

  const postSleepState = await client.evaluate(`studyClockActiveSession.status`);
  if (postSleepState !== 'paused') throw new Error('Session should auto-pause when sleep gap is detected');
  console.log('✓ Sleep gap automatically freezes timer to prevent counting gap time.');

  // Test 7: Integrity of trackers
  console.log('\n[TEST 7] Verifying problem trackers & data integrity...');
  const integrity = await client.evaluate(`(() => {
    return {
      dsaProblems: typeof DATA !== 'undefined' ? DATA.reduce((acc, s) => acc + s.problems.length, 0) : 0,
      rbProblems: typeof RISINGBRAIN_DATA !== 'undefined' ? RISINGBRAIN_DATA.reduce((acc, t) => acc + t.patterns.reduce((a, p) => a + p.problems.length, 0), 0) : 0,
      striverProblems: typeof STRIVER_DATA !== 'undefined' ? STRIVER_DATA.reduce((acc, s) => acc + s.problems.length, 0) : 0,
      hasStudyState: typeof studyState !== 'undefined' && studyState.days !== undefined
    };
  })()`);
  console.log('Integrity check:', integrity);
  if (integrity.dsaProblems !== 184 || integrity.rbProblems !== 385 || integrity.striverProblems !== 455) {
    throw new Error('Problem trackers altered!');
  }
  console.log('✓ All 184 DSA, 385 RisingBrain, and 455 Striver problems 100% preserved.');

  await closeCDPPage(page.id);
  chromeProcess.kill('SIGTERM');

  console.log('\n======================================================');
  console.log('ALL TESTS PASSED WITH 100% SUCCESS!');
  console.log('======================================================\n');
}

run().catch(err => {
  console.error('\n❌ TEST FAILED:', err);
  process.exit(1);
});
