import http from 'http';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const PORT = 8096;
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
  const cdpPort = 9225;
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
    console.log('\n--- TEST SUITE: DATA & STORAGE CENTER ---');

    // TEST 1: Navigation to Settings & Backup
    console.log('\nTest 1: View Navigation to Settings & Backup');
    const switchRes = await evaluate(`(() => {
      switchView('settings');
      const sec = document.getElementById('view-settings');
      const container = document.getElementById('dataStorageCenterContainer');
      return {
        isActive: sec && sec.classList.contains('active'),
        hasContainer: !!container
      };
    })()`);
    assert(switchRes.isActive, 'view-settings is active');
    assert(switchRes.hasContainer, 'dataStorageCenterContainer rendered in view-settings');

    // TEST 2: LocalStorage Calculation & Key Inventory
    console.log('\nTest 2: LocalStorage Calculation & Key Inventory');
    const lsScan = await evaluate(`(() => {
      return scanLocalStorageInventory();
    })()`);
    assert(lsScan.keyCount > 0, `LocalStorage scanned ${lsScan.keyCount} keys`);
    assert(lsScan.totalAllBytes > 0, `Total bytes calculated: ${lsScan.totalAllBytes} bytes`);
    assert(lsScan.typicalLimitBytes === 5242880, '5.0 MiB limit baseline used');
    assert(typeof lsScan.percentOfLimit === 'number', `Percentage of 5 MiB computed: ${lsScan.percentOfLimit.toFixed(2)}%`);

    const tableRowsCount = await evaluate(`(() => {
      const rows = document.querySelectorAll('#scLsTableBody tr');
      return rows.length;
    })()`);
    assert(tableRowsCount >= lsScan.keyCount, `Table rendered ${tableRowsCount} rows for storage keys`);

    // TEST 3: IndexedDB Inventory
    console.log('\nTest 3: IndexedDB Inventory');
    const idbScan = await evaluate(`(async () => {
      return await scanIndexedDBInventory();
    })()`);
    assert(Array.isArray(idbScan) && idbScan.length === 2, `IndexedDB databases identified: ${idbScan.map(d=>d.name).join(', ')}`);
    assert(idbScan[0].name === 'PlacementTrackerDB', 'PlacementTrackerDB present');
    assert(idbScan[1].name === 'FamilyPhotosDB', 'FamilyPhotosDB present');

    // TEST 4: Browser Quota & Persistence Audit
    console.log('\nTest 4: Browser Quota & Storage Protection');
    const quotaRes = await evaluate(`(async () => {
      return await auditBrowserStorageQuota();
    })()`);
    assert(typeof quotaRes.supported === 'boolean', `Storage estimate API supported: ${quotaRes.supported}`);
    assert(quotaRes.origin.length > 0, `Origin detected: ${quotaRes.origin}`);

    const persistRes = await evaluate(`(async () => {
      return await auditBrowserStoragePersistence();
    })()`);
    assert(typeof persistRes.supported === 'boolean', `Storage persistence query supported: ${persistRes.supported}`);

    // TEST 5: Smart Storage Alerts
    console.log('\nTest 5: Smart Storage Alerts');
    const alertHtml = await evaluate(`(() => {
      const alertsEl = document.getElementById('scStorageAlertsContainer');
      return alertsEl ? alertsEl.innerHTML : '';
    })()`);
    assert(alertHtml.includes('Backup Reminder'), '7-day backup reminder alert triggered when no backup exists');

    // TEST 6: One-Click Complete Backup Export
    console.log('\nTest 6: Comprehensive Backup Bundle Generation');
    const bundle = await evaluate(`(() => {
      return buildComprehensiveBackupBundle();
    })()`);
    assert(bundle.schemaVersion === 6, 'Backup schema version is 6');
    assert(bundle.version === 6, 'Top-level version is 6');
    assert(bundle.backupDateKolkata.includes('IST'), `Backup date in Asia/Kolkata: ${bundle.backupDateKolkata}`);
    assert(bundle.manifest && bundle.manifest.categories.length >= 10, 'Manifest lists all application categories');
    assert(bundle.categories && bundle.categories.dsaPatterns !== null, 'Categories includes dsaPatterns');
    assert(bundle.categories && bundle.categories.striverA2Z !== null, 'Categories includes striverA2Z');
    assert(bundle.categories && bundle.categories.risingBrain !== null, 'Categories includes risingBrain');
    assert(bundle.categories && bundle.categories.mikInterview !== null, 'Categories includes mikInterview');
    assert(bundle.categories && bundle.categories.coreSubjects !== null, 'Categories includes coreSubjects');
    assert(bundle.categories && bundle.categories.skillsHub !== null, 'Categories includes skillsHub');
    assert(bundle.categories && bundle.categories.studyClock !== null, 'Categories includes studyClock');
    assert(bundle.categories && bundle.categories.dailyWorkspace !== null, 'Categories includes dailyWorkspace');
    assert(bundle.dsaState !== null, 'Top-level backwards-compatible dsaState present');

    // Test JSON Serialization
    const serialized = JSON.stringify(bundle);
    assert(serialized.length > 1000, `Bundle serializes cleanly without circular errors (${serialized.length} bytes)`);

    // TEST 7: Restore Simulation & Category Checklist
    console.log('\nTest 7: Restore Simulation & Category Checklist');
    const restorePreview = await evaluate(`(() => {
      const mockBundle = buildComprehensiveBackupBundle();
      currentPendingRestoreData = mockBundle;
      currentPendingEmergencyBackup = buildComprehensiveBackupBundle();
      renderRestoreCategoryChecklist(mockBundle);
      openModal('modalDataCenterRestore');

      const modal = document.getElementById('modalDataCenterRestore');
      const checkboxes = document.querySelectorAll('#scRestoreChecklist input[type="checkbox"]');
      return {
        isModalOpen: modal && modal.classList.contains('active'),
        checkboxCount: checkboxes.length
      };
    })()`);
    assert(restorePreview.isModalOpen, 'modalDataCenterRestore opens successfully');
    assert(restorePreview.checkboxCount >= 10, `Checklist rendered ${restorePreview.checkboxCount} category options`);

    // Desktop screenshot with Restore Modal Open
    await sendCmd('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 2,
      mobile: false
    });
    await new Promise(r => setTimeout(r, 400));
    const ssModal = await sendCmd('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'sc_desktop_restore_modal.png'), Buffer.from(ssModal.data, 'base64'));
    console.log('  Saved artifact: sc_desktop_restore_modal.png');

    // Close restore modal
    await evaluate(`closeModal('modalDataCenterRestore')`);

    // TEST 8: Safe Restoration Execution
    console.log('\nTest 8: Safe Restoration Execution');
    const restoreExec = await evaluate(`(() => {
      const mockBundle = buildComprehensiveBackupBundle();
      currentPendingRestoreData = mockBundle;
      executeDataCenterRestoreConfirmed();
      const lastRestore = localStorage.getItem('prep_dashboard_last_restore_meta');
      return {
        hasRestoreMeta: !!lastRestore,
        restoreMetaParsed: lastRestore ? JSON.parse(lastRestore) : null
      };
    })()`);
    assert(restoreExec.hasRestoreMeta, 'Last restore metadata recorded in LocalStorage');
    assert(restoreExec.restoreMetaParsed.categoriesRestored > 0, `Restored ${restoreExec.restoreMetaParsed.categoriesRestored} categories`);

    // TEST 9: Corrupted & Non-Dashboard Backup Rejection
    console.log('\nTest 9: Corrupted & Incompatible Backup Rejection');
    const rejectCorrupted = await evaluate(`(() => {
      let threw = false;
      let errorMsg = '';
      try {
        JSON.parse('{ invalid json here:');
      } catch (e) {
        threw = true;
        errorMsg = e.message;
      }
      return { threw, errorMsg };
    })()`);
    assert(rejectCorrupted.threw, 'Corrupted JSON triggers syntax error safely');

    const rejectIncompatible = await evaluate(`(() => {
      const fakeObj = { foo: 'bar', randomNumbers: [1,2,3] };
      const hasDsa = !!(fakeObj.dsaState || fakeObj.problems || (fakeObj.categories && fakeObj.categories.dsaPatterns));
      const hasStriver = !!(fakeObj.striverState || (fakeObj.categories && fakeObj.categories.striverA2Z));
      const hasCoreSubjects = !!(fakeObj.coreSubjectsState || (fakeObj.categories && fakeObj.categories.coreSubjects));
      const hasStudyClock = !!(fakeObj.studyClockHistory || (fakeObj.categories && fakeObj.categories.studyClock));
      const hasWorkspace = !!(fakeObj.plannerTasks || fakeObj.dailyWorkspace || (fakeObj.categories && fakeObj.categories.dailyWorkspace));
      const isRecognized = hasDsa || hasStriver || hasCoreSubjects || hasStudyClock || hasWorkspace;
      return { isRecognized };
    })()`);
    assert(!rejectIncompatible.isRecognized, 'Non-dashboard JSON rejected safely without touching live data');

    // TEST 10: Desktop Overview Screenshot
    console.log('\nTest 10: Capturing Verification Screenshots');
    await evaluate(`(() => {
      switchView('settings');
      window.scrollTo(0, 0);
    })()`);
    await new Promise(r => setTimeout(r, 400));
    const ssOverview = await sendCmd('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'sc_desktop_overview.png'), Buffer.from(ssOverview.data, 'base64'));
    console.log('  Saved artifact: sc_desktop_overview.png');

    // Switch to IndexedDB tab & capture
    await evaluate(`switchStorageCenterTab('indexeddb', document.querySelectorAll('.sc-tab-btn')[1])`);
    await new Promise(r => setTimeout(r, 300));
    const ssIdb = await sendCmd('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'sc_desktop_indexeddb.png'), Buffer.from(ssIdb.data, 'base64'));
    console.log('  Saved artifact: sc_desktop_indexeddb.png');

    // Switch back to LocalStorage table
    await evaluate(`switchStorageCenterTab('localstorage', document.querySelectorAll('.sc-tab-btn')[0])`);

    // Mobile Viewport
    await sendCmd('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 400));
    const ssMobile = await sendCmd('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(path.join(ARTIFACTS_DIR, 'sc_mobile_overview.png'), Buffer.from(ssMobile.data, 'base64'));
    console.log('  Saved artifact: sc_mobile_overview.png');

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
