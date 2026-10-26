import http from 'http';
import fs from 'fs';
import path from 'path';

const CDP_PORT = 9222;
const ARTIFACT_DIR = '/Users/devrajput/.gemini/antigravity-ide/brain/66b7e02f-986f-4cfd-b90f-8aa4c87db087';
const TEST_URL = "file:///Users/devrajput/@Resources/Tracker/integrated_master.html";

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
            console.error('[BROWSER ERROR]:', text);
          }
        }
        if (parsed.method === 'Runtime.exceptionThrown') {
          const text = parsed.params.exceptionDetails.text + ' ' + (parsed.params.exceptionDetails.exception?.description || '');
          this.consoleErrors.push(text);
          console.error('[BROWSER EXCEPTION]:', text);
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
  const page = await createFreshCDPPage();
  const client = new CDPClient(page.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Runtime.enable');
  await client.send('Page.enable');
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 960,
    deviceScaleFactor: 2,
    mobile: false
  });

  console.log('Navigating to test file:', TEST_URL);
  await client.send('Page.navigate', { url: TEST_URL });
  await new Promise(r => setTimeout(r, 2000));

  console.log('\n--- 1. Page Load & Initial Console Errors ---');
  console.log('Console Errors count:', client.consoleErrors.length);

  console.log('\n--- 2. Switch to Study Clock View ---');
  await client.evaluate(`switchView('studyclock')`);
  await new Promise(r => setTimeout(r, 500));

  const viewData = await client.evaluate(`(() => {
    const sec = document.getElementById('view-studyclock');
    const title = document.getElementById('viewTitle')?.textContent.trim();
    const digits = document.getElementById('scClockDigits')?.textContent.trim();
    const isVisible = sec && sec.classList.contains('active');
    const navItem = Array.from(document.querySelectorAll('.sidebar-nav .nav-item')).find(el => el.textContent.includes('Study Clock'));
    return {
      isVisible,
      title,
      digits,
      hasNavItem: !!navItem,
      navBadge: navItem ? navItem.querySelector('.nav-badge')?.textContent.trim() : null
    };
  })()`);

  console.log('Study Clock View Visible:', viewData.isVisible);
  console.log('View Title:', viewData.title);
  console.log('Clock Digits:', viewData.digits);
  console.log('Sidebar Nav Item exists:', viewData.hasNavItem, 'Badge:', viewData.navBadge);

  console.log('\n--- 3. Starting Study Session ---');
  await client.evaluate(`(() => {
    const catSel = document.getElementById('scCategorySelect');
    if (catSel) catSel.value = 'DSA';
    const notes = document.getElementById('scSessionNotesInput');
    if (notes) notes.value = 'Graph BFS Practice';
    startStudyClock();
  })()`);

  // Wait 3.5 seconds
  console.log('Waiting 3.5 seconds for live timer tick...');
  await new Promise(r => setTimeout(r, 3500));

  const tickingData = await client.evaluate(`(() => {
    const digits = document.getElementById('scClockDigits')?.textContent.trim();
    const hdrDigits = document.getElementById('hdr-timer-display')?.textContent.trim();
    const hdrIcon = document.getElementById('hdr-timer-btn-icon')?.textContent.trim();
    const cardRunning = document.getElementById('scClockCard')?.classList.contains('running');
    const elapsedSec = Math.floor(getStudyClockElapsedMs() / 1000);
    return {
      digits,
      hdrDigits,
      hdrIcon,
      cardRunning,
      elapsedSec,
      sessionStatus: studyClockActiveSession.status
    };
  })()`);

  console.log('Ticking State:');
  console.log('  Elapsed Seconds:', tickingData.elapsedSec);
  console.log('  Hero Digits:', tickingData.digits);
  console.log('  Header Mini Widget:', tickingData.hdrDigits, 'Icon:', tickingData.hdrIcon);
  console.log('  Card Running Class:', tickingData.cardRunning);
  console.log('  Active Session Status:', tickingData.sessionStatus);

  console.log('\n--- 4. Testing HARD PAGE RELOAD / RECOVERY WHILE RUNNING ---');
  console.log('Triggering Page.reload()...');
  await client.send('Page.reload');
  await new Promise(r => setTimeout(r, 2000));

  // Re-switch to study clock view
  await client.evaluate(`switchView('studyclock')`);
  await new Promise(r => setTimeout(r, 500));

  const postReloadData = await client.evaluate(`(() => {
    const digits = document.getElementById('scClockDigits')?.textContent.trim();
    const cardRunning = document.getElementById('scClockCard')?.classList.contains('running');
    const elapsedSec = Math.floor(getStudyClockElapsedMs() / 1000);
    return {
      digits,
      cardRunning,
      elapsedSec,
      status: studyClockActiveSession.status,
      category: studyClockActiveSession.category,
      notes: studyClockActiveSession.notes
    };
  })()`);

  console.log('Post-Reload Recovery Data:');
  console.log('  Status Recovered:', postReloadData.status);
  console.log('  Card Still Running:', postReloadData.cardRunning);
  console.log('  Elapsed Seconds Preserved & Continued:', postReloadData.elapsedSec);
  console.log('  Hero Digits Post-Reload:', postReloadData.digits);
  console.log('  Category & Notes Preserved:', postReloadData.category, '|', postReloadData.notes);

  console.log('\n--- 5. Testing Pause & Second Reload ---');
  await client.evaluate(`pauseStudyClock()`);
  await new Promise(r => setTimeout(r, 500));

  const pausedData = await client.evaluate(`(() => {
    return {
      status: studyClockActiveSession.status,
      pausedSec: Math.floor(getStudyClockElapsedMs() / 1000),
      cardPaused: document.getElementById('scClockCard')?.classList.contains('paused'),
      resumeBtnVisible: document.getElementById('scBtnResume')?.style.display !== 'none'
    };
  })()`);
  console.log('Paused State:', pausedData);

  console.log('Reloading while paused...');
  await client.send('Page.reload');
  await new Promise(r => setTimeout(r, 2000));

  await client.evaluate(`switchView('studyclock')`);
  await new Promise(r => setTimeout(r, 500));

  const postPausedReload = await client.evaluate(`(() => {
    return {
      status: studyClockActiveSession.status,
      sec: Math.floor(getStudyClockElapsedMs() / 1000),
      cardPaused: document.getElementById('scClockCard')?.classList.contains('paused')
    };
  })()`);
  console.log('Post-Reload Paused State:', postPausedReload);

  console.log('\n--- 6. Resuming and Logging Session ---');
  await client.evaluate(`resumeStudyClock()`);
  await new Promise(r => setTimeout(r, 1000));

  // Manually ensure session duration is >= 12s so it doesn't prompt for short session discard
  await client.evaluate(`(() => {
    studyClockActiveSession.accumulatedMs += 45 * 60 * 1000; // simulate 45 min
    stopAndLogStudySession();
  })()`);
  await new Promise(r => setTimeout(r, 500));

  const postSaveStats = await client.evaluate(`(() => {
    const totalSessions = studyClockHistory.sessions.length;
    const latest = studyClockHistory.sessions[0];
    const todayStat = document.getElementById('scStatTodayHours')?.textContent.trim();
    const tableRows = document.querySelectorAll('#scSessionsTableBody tr').length;
    return {
      totalSessions,
      latest,
      todayStat,
      tableRows
    };
  })()`);

  console.log('Saved Session Data:');
  console.log('  Total Sessions:', postSaveStats.totalSessions);
  console.log('  Latest Session:', postSaveStats.latest.category, postSaveStats.latest.durationFormatted, postSaveStats.latest.notes);
  console.log('  Today Stat Card:', postSaveStats.todayStat);
  console.log('  History Table Rows:', postSaveStats.tableRows);

  console.log('\n--- 7. Manual Entry & Edit & Delete Testing ---');
  // Manual Entry
  await client.evaluate(`(() => {
    document.getElementById('scManualDurationMinutes').value = '30';
    document.getElementById('scManualCategory').value = 'Core Subjects';
    document.getElementById('scManualNotes').value = 'OS Virtual Memory & Paging';
    submitManualStudySession();
  })()`);
  await new Promise(r => setTimeout(r, 300));

  const manualStats = await client.evaluate(`(() => {
    return {
      totalSessions: studyClockHistory.sessions.length,
      latestCat: studyClockHistory.sessions[0].category,
      latestNotes: studyClockHistory.sessions[0].notes
    };
  })()`);
  console.log('Manual Entry Result: Total sessions:', manualStats.totalSessions, '| Category:', manualStats.latestCat, '| Notes:', manualStats.latestNotes);

  // Edit the latest session
  await client.evaluate(`(() => {
    const sId = studyClockHistory.sessions[0].id;
    document.getElementById('scEditSessionId').value = sId;
    document.getElementById('scEditDurationMinutes').value = '35';
    document.getElementById('scEditCategory').value = 'Core Subjects';
    document.getElementById('scEditNotes').value = 'OS Virtual Memory & Paging (Deep Dive)';
    submitEditStudySession();
  })()`);
  await new Promise(r => setTimeout(r, 300));

  const editStats = await client.evaluate(`studyClockHistory.sessions[0].notes`);
  console.log('Edited Session Notes:', editStats);

  // Delete with confirmation execution
  await client.evaluate(`(() => {
    const sId = studyClockHistory.sessions[0].id;
    confirmDeleteStudySession(sId);
    executeDeleteStudySession();
  })()`);
  await new Promise(r => setTimeout(r, 300));

  const deleteStats = await client.evaluate(`studyClockHistory.sessions.length`);
  console.log('Total sessions after delete:', deleteStats);

  console.log('\n--- 8. Preserving Trackers & Sync Integrity ---');
  const trackerIntegrity = await client.evaluate(`(() => {
    return {
      dsaCount: typeof DATA !== 'undefined' ? DATA.reduce((acc, s) => acc + s.problems.length, 0) : 0,
      rbCount: typeof RISINGBRAIN_DATA !== 'undefined' ? RISINGBRAIN_DATA.reduce((acc, t) => acc + t.patterns.reduce((a, p) => a + p.problems.length, 0), 0) : 0,
      striverCount: typeof STRIVER_DATA !== 'undefined' ? STRIVER_DATA.reduce((acc, s) => acc + s.problems.length, 0) : 0,
      syncMapActive: typeof DSA_RB_SYNC_MAP !== 'undefined' && Object.keys(DSA_RB_SYNC_MAP).length > 0
    };
  })()`);
  console.log('DSA Problems (184):', trackerIntegrity.dsaCount);
  console.log('RisingBrain Problems (385):', trackerIntegrity.rbCount);
  console.log('Striver Problems (455):', trackerIntegrity.striverCount);
  console.log('Sync Map Active:', trackerIntegrity.syncMapActive);

  console.log('\n--- 9. Capturing Screenshot of Restored Study Clock Page ---');
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'study_clock_page_verified.png'));

  if (client.ws) client.ws.close();
  await closeCDPPage(page.id);
  console.log('\nCDP Test for Study Clock completed successfully!');
}

run().catch(err => {
  console.error('Test error:', err);
  process.exit(1);
});
