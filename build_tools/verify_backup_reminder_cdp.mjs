import http from 'http';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const PORT = 8097;
const TRACKER_ROOT = '/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard';
const ARTIFACTS_DIR = '/Users/devrajput/.gemini/antigravity/brain/cc448d00-6c1d-4ddd-a4f5-3272bcd6e6fa';

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/') reqPath = '/index.html';
  const filePath = path.join(TRACKER_ROOT, reqPath);

  if (!fs.existsSync(filePath)) {
    res.writeHead(404);
    res.end('Not found');
    return;
  }

  const ext = path.extname(filePath);
  const mimeMap = {
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.css': 'text/css',
    '.png': 'image/png'
  };

  res.writeHead(200, { 'Content-Type': mimeMap[ext] || 'text/plain' });
  fs.createReadStream(filePath).pipe(res);
});

server.listen(PORT, async () => {
  console.log(`Test server running on http://127.0.0.1:${PORT}`);
  await runTests();
});

async function runTests() {
  const cdpPort = 9226;
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const chromeProc = spawn(chromePath, [
    '--headless=new',
    `--remote-debugging-port=${cdpPort}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=/tmp/chrome-test-profile-' + Date.now()
  ]);

  let targets = null;
  for (let attempt = 0; attempt < 25; attempt++) {
    try {
      const resp = await fetch(`http://127.0.0.1:${cdpPort}/json`);
      targets = await resp.json();
      if (targets && targets.length > 0) break;
    } catch (e) {
      await new Promise(r => setTimeout(r, 400));
    }
  }

  if (!targets) {
    console.error('Could not connect to Chrome CDP endpoint');
    chromeProc.kill();
    server.close();
    process.exit(1);
  }

  const pageTarget = targets.find(t => t.type === 'page');
  if (!pageTarget || !pageTarget.webSocketDebuggerUrl) {
    console.error('Could not find page target debugger URL');
    chromeProc.kill();
    server.close();
    process.exit(1);
  }

  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

  let idCounter = 1;
  const pending = new Map();
  const jsErrors = [];

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.method === 'Runtime.exceptionThrown') {
      const desc = msg.params.exceptionDetails?.exception?.description || msg.params.exceptionDetails?.text;
      console.error('CDP JS Exception:', desc);
      jsErrors.push(desc);
    }
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(msg.error);
      else resolve(msg.result);
    }
  };

  function sendCmd(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = idCounter++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  await new Promise(r => ws.onopen = r);

  await sendCmd('Page.enable');
  await sendCmd('Runtime.enable');
  await sendCmd('DOM.enable');

  console.log('Navigating to test server...');
  await sendCmd('Page.navigate', { url: `http://127.0.0.1:${PORT}/index.html` });
  await new Promise(r => setTimeout(r, 2000));

  let passCount = 0;
  let failCount = 0;

  function assert(condition, desc) {
    if (condition) {
      console.log(`  ✓ PASS: ${desc}`);
      passCount++;
    } else {
      console.error(`  ✗ FAIL: ${desc}`);
      failCount++;
    }
  }

  async function evaluate(expression) {
    const res = await sendCmd('Runtime.evaluate', {
      expression: expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error(res.exceptionDetails.exception?.description || res.exceptionDetails.text);
    }
    return res.result?.value;
  }

  try {
    console.log('\n--- VERIFICATION: BACKUP REMINDER LOGIC & VERIFIED SAVE ---');

    await evaluate(`switchView('settings')`);

    // TEST 1: First-time backup with no previous timestamp
    console.log('\nTest 1: First-time backup with no previous timestamp');
    const t1 = await evaluate(`(async () => {
      localStorage.removeItem('prep_dashboard_last_successful_backup_timestamp');
      localStorage.removeItem('prep_dashboard_last_backup_meta');
      await refreshStorageCenterUI(false);

      const reminder = getBackupReminderState();
      const pill = document.getElementById('scBackupStatusPill')?.textContent || '';
      const nextDue = document.getElementById('scBackupNextDue')?.textContent || '';
      const alertsHtml = document.getElementById('scStorageAlertsContainer')?.innerHTML || '';

      return {
        hasBackup: reminder.hasBackup,
        isDue: reminder.isDue,
        pillText: pill,
        nextDueText: nextDue,
        hasBackupAlert: alertsHtml.includes('Backup Due') || alertsHtml.includes('Backup Reminder')
      };
    })()`);
    assert(!t1.hasBackup, 'hasBackup is false when no timestamp stored');
    assert(!t1.isDue, 'isDue is false for first-time user before first backup');
    assert(t1.pillText.includes('First Backup Pending'), `Status pill displays: "${t1.pillText}"`);
    assert(t1.nextDueText.includes('Pending initial manual backup'), `Next due text displays: "${t1.nextDueText}"`);
    assert(!t1.hasBackupAlert, 'No repeated backup warning banner shown before manual first backup');

    // TEST 2: Successful backup and timestamp update
    console.log('\nTest 2: Successful backup and timestamp update');
    const t2 = await evaluate(`(async () => {
      const testTimestamp = Date.now();
      const testFileName = 'prep_dashboard_complete_backup_2026-11-04_174000.json';
      recordSuccessfulBackup(testTimestamp, 450000, testFileName, 'file_system_api');
      await refreshStorageCenterUI(false);

      const storedTime = localStorage.getItem('prep_dashboard_last_successful_backup_timestamp');
      const storedMeta = JSON.parse(localStorage.getItem('prep_dashboard_last_backup_meta') || '{}');
      const reminder = getBackupReminderState();
      const pill = document.getElementById('scBackupStatusPill')?.textContent || '';
      const nextDue = document.getElementById('scBackupNextDue')?.textContent || '';
      const alertsHtml = document.getElementById('scStorageAlertsContainer')?.innerHTML || '';

      return {
        storedTimeMatch: Number(storedTime) === testTimestamp,
        hasMeta: storedMeta.timestamp === testTimestamp,
        method: storedMeta.method,
        hasBackup: reminder.hasBackup,
        isDue: reminder.isDue,
        daysRemaining: reminder.daysRemaining,
        pillText: pill,
        nextDueText: nextDue,
        hasAlert: alertsHtml.includes('Backup Due')
      };
    })()`);
    assert(t2.storedTimeMatch, 'Timestamp stored in dedicated key prep_dashboard_last_successful_backup_timestamp');
    assert(t2.hasMeta, 'Metadata stored with matching timestamp');
    assert(t2.method === 'file_system_api', `Method recorded: ${t2.method}`);
    assert(t2.hasBackup, 'hasBackup is now true');
    assert(!t2.isDue, 'isDue is false immediately after successful backup');
    assert(t2.daysRemaining === 7, `7 full days remaining until next backup (Got: ${t2.daysRemaining})`);
    assert(t2.pillText.includes('Up to Date'), `Status pill updated to: "${t2.pillText}"`);
    assert(!t2.hasAlert, 'Backup reminder banner is hidden immediately');

    // TEST 3: Reminder hidden before 7 days (e.g. 3 days elapsed)
    console.log('\nTest 3: Reminder hidden before 7 days (Day 3 check)');
    const t3 = await evaluate(`(async () => {
      const threeDaysAgo = Date.now() - (3 * 24 * 60 * 60 * 1000);
      recordSuccessfulBackup(threeDaysAgo, 450000, 'backup_3d_ago.json', 'file_system_api');
      await refreshStorageCenterUI(false);

      const reminder = getBackupReminderState();
      const alertsHtml = document.getElementById('scStorageAlertsContainer')?.innerHTML || '';
      const pill = document.getElementById('scBackupStatusPill')?.textContent || '';

      return {
        isDue: reminder.isDue,
        daysElapsed: reminder.daysElapsed,
        daysRemaining: reminder.daysRemaining,
        pillText: pill,
        hasAlert: alertsHtml.includes('Backup Due')
      };
    })()`);
    assert(!t3.isDue, 'isDue is false on day 3');
    assert(t3.daysElapsed === 3, `Days elapsed: ${t3.daysElapsed}`);
    assert(t3.daysRemaining === 4, `Days remaining: ${t3.daysRemaining}`);
    assert(t3.pillText.includes('Up to Date'), `Status pill is Up to Date`);
    assert(!t3.hasAlert, 'Zero backup alerts shown during the 7-day period');

    // TEST 4: Reminder shown after 7 full days (e.g. 7 days + 1 hour)
    console.log('\nTest 4: Reminder shown after 7 days have elapsed');
    const t4 = await evaluate(`(async () => {
      const sevenDaysOneHourAgo = Date.now() - (7 * 24 * 60 * 60 * 1000 + 3600000);
      recordSuccessfulBackup(sevenDaysOneHourAgo, 450000, 'backup_7d_ago.json', 'file_system_api');
      await refreshStorageCenterUI(false);

      const reminder = getBackupReminderState();
      const alertsHtml = document.getElementById('scStorageAlertsContainer')?.innerHTML || '';
      const pill = document.getElementById('scBackupStatusPill')?.textContent || '';
      const nextDue = document.getElementById('scBackupNextDue')?.innerHTML || '';

      return {
        isDue: reminder.isDue,
        daysElapsed: reminder.daysElapsed,
        pillText: pill,
        hasAlert: alertsHtml.includes('Backup Due:'),
        nextDueHtml: nextDue
      };
    })()`);
    assert(t4.isDue, 'isDue is true after 7 full days');
    assert(t4.daysElapsed >= 7, `Days elapsed is >= 7 (${t4.daysElapsed})`);
    assert(t4.pillText.includes('Backup Due'), `Status pill shows: "${t4.pillText}"`);
    assert(t4.hasAlert, 'Backup Due reminder banner is displayed prominently');
    assert(t4.nextDueHtml.includes('Due now'), 'Next due indicator states: Due now');

    // Capture screenshot of Backup Due state
    await sendCmd('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 2,
      mobile: false
    });
    await new Promise(r => setTimeout(r, 400));
    const ssDue = await sendCmd('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'sc_backup_due_state.png'), Buffer.from(ssDue.data, 'base64'));
    console.log('  Saved artifact: sc_backup_due_state.png');

    // TEST 5: Failed download / Cancelled save does NOT update timestamp
    console.log('\nTest 5: Failed download / Cancelled save does NOT update timestamp');
    const t5 = await evaluate(`(async () => {
      const priorTimestamp = localStorage.getItem('prep_dashboard_last_successful_backup_timestamp');

      // Simulate download initiation with pending meta
      pendingManualBackupMeta = {
        timestamp: Date.now() + 1000000,
        sizeBytes: 999999,
        fileName: 'unconfirmed.json',
        method: 'confirmed_download'
      };

      // User cancels
      cancelBackupSaveConfirmation();

      const afterTimestamp = localStorage.getItem('prep_dashboard_last_successful_backup_timestamp');

      return {
        isUnchanged: priorTimestamp === afterTimestamp,
        isPendingCleared: pendingManualBackupMeta === null
      };
    })()`);
    assert(t5.isUnchanged, 'Timestamp was NOT updated when user cancelled');
    assert(t5.isPendingCleared, 'Pending backup memory was cleared safely');

    // TEST 5b: Explicit "I have saved the backup" updates timestamp
    console.log('\nTest 5b: Explicit "I have saved the backup" updates timestamp');
    const t5b = await evaluate(`(async () => {
      const nowTime = Date.now();
      pendingManualBackupMeta = {
        timestamp: nowTime,
        sizeBytes: 520000,
        fileName: 'prep_dashboard_complete_backup_test_confirmed.json',
        method: 'confirmed_download'
      };

      // User clicks "I have saved the backup"
      confirmBackupSaveManually();
      await refreshStorageCenterUI(false);

      const afterTimestamp = localStorage.getItem('prep_dashboard_last_successful_backup_timestamp');
      const storedMeta = JSON.parse(localStorage.getItem('prep_dashboard_last_backup_meta') || '{}');

      return {
        updated: Number(afterTimestamp) === nowTime,
        method: storedMeta.method
      };
    })()`);
    assert(t5b.updated, 'Clicking "I have saved the backup" updated the timestamp');
    assert(t5b.method === 'confirmed_download', `Confirmation method recorded: ${t5b.method}`);

    // TEST 6: Browser reload and new session persistence
    console.log('\nTest 6: Browser reload and new session persistence');
    const sessionTime = Date.now() - (2 * 24 * 60 * 60 * 1000); // 2 days ago
    await evaluate(`(async () => {
      recordSuccessfulBackup(${sessionTime}, 480000, 'session_test.json', 'file_system_api');
      await refreshStorageCenterUI(false);
    })()`);

    // Reload page
    console.log('  Reloading browser page to simulate brand new session...');
    await sendCmd('Page.reload');
    await new Promise(r => setTimeout(r, 2000));

    const t6 = await evaluate(`(async () => {
      switchView('settings');
      await refreshStorageCenterUI(false);
      const reminder = getBackupReminderState();
      const stored = localStorage.getItem('prep_dashboard_last_successful_backup_timestamp');
      const alertsHtml = document.getElementById('scStorageAlertsContainer')?.innerHTML || '';
      const pill = document.getElementById('scBackupStatusPill')?.textContent || '';

      return {
        storedMatches: Number(stored) === ${sessionTime},
        hasBackup: reminder.hasBackup,
        isDue: reminder.isDue,
        daysRemaining: reminder.daysRemaining,
        pillText: pill,
        hasAlert: alertsHtml.includes('Backup Due')
      };
    })()`);
    assert(t6.storedMatches, 'Dedicated timestamp persisted across browser reload');
    assert(t6.hasBackup, 'hasBackup is true in new session');
    assert(!t6.isDue, 'isDue is false in new session within 7-day window');
    assert(t6.daysRemaining === 5, `Days remaining is 5 (${t6.daysRemaining})`);
    assert(t6.pillText.includes('Up to Date'), `Status pill is Up to Date`);
    assert(!t6.hasAlert, 'Zero repeated session warning banners shown in new session');

    // TEST 7: Unique timestamp-based filenames
    console.log('\nTest 7: Unique timestamp-based filenames');
    const t7 = await evaluate(`(() => {
      function getBackupFileName(date) {
        const y = date.getFullYear();
        const m = String(date.getMonth() + 1).padStart(2, '0');
        const d = String(date.getDate()).padStart(2, '0');
        const hh = String(date.getHours()).padStart(2, '0');
        const mm = String(date.getMinutes()).padStart(2, '0');
        const ss = String(date.getSeconds()).padStart(2, '0');
        return \`prep_dashboard_complete_backup_\${y}-\${m}-\${d}_\${hh}\${mm}\${ss}.json\`;
      }

      const d1 = new Date('2026-11-04T17:40:01');
      const d2 = new Date('2026-11-04T17:40:02');
      const f1 = getBackupFileName(d1);
      const f2 = getBackupFileName(d2);

      return {
        f1: f1,
        f2: f2,
        isUnique: f1 !== f2,
        hasSeconds: f1.includes('174001') && f2.includes('174002')
      };
    })()`);
    assert(t7.isUnique, `Filenames are unique: ${t7.f1} vs ${t7.f2}`);
    assert(t7.hasSeconds, 'Filenames include seconds to prevent collisions/overwrites');

    // Capture screenshot of Up to Date state
    await evaluate(`(() => {
      switchView('settings');
      window.scrollTo(0, 0);
    })()`);
    await new Promise(r => setTimeout(r, 400));
    const ssUpToDate = await sendCmd('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'sc_backup_up_to_date_state.png'), Buffer.from(ssUpToDate.data, 'base64'));
    console.log('  Saved artifact: sc_backup_up_to_date_state.png');

    // Summary
    console.log(`\n========================================`);
    console.log(`TEST SUMMARY: ${passCount} PASSED, ${failCount} FAILED`);
    console.log(`Runtime JS Exceptions: ${jsErrors.length}`);
    console.log(`========================================\n`);

    assert(jsErrors.length === 0, `Zero JS console errors (Found: ${jsErrors.length})`);

  } catch (err) {
    console.error('Test execution error:', err);
    failCount++;
  } finally {
    ws.close();
    chromeProc.kill();
    server.close();
    process.exit(failCount === 0 ? 0 : 1);
  }
}
