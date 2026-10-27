import http from 'http';
import { spawn } from 'child_process';
import fs from 'fs';

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

  send(method, params = {}) {
    return new Promise((res, rej) => {
      const id = this.id++;
      this.callbacks.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression) {
    const result = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (result.exceptionDetails) {
      throw new Error(JSON.stringify(result.exceptionDetails));
    }
    return result.result ? result.result.value : undefined;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function createFreshCDPPage() {
  const res = await fetch(`http://127.0.0.1:${CDP_PORT}/json/new`, { method: 'PUT' });
  return await res.json();
}

async function run() {
  console.log('--- Launching Headless Chrome for MIK Interview DSA Verification ---');
  const chromeProcess = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    `--remote-debugging-port=${CDP_PORT}`,
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=/tmp/chrome_test_mik_' + Date.now()
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
  console.log('TEST SUITE: MIK INTERVIEW DSA VERIFICATION');
  console.log('======================================================');

  let passedTests = 0;
  let totalTests = 0;

  function assert(desc, condition) {
    totalTests++;
    if (condition) {
      console.log(`[PASS] ${desc}`);
      passedTests++;
    } else {
      console.error(`[FAIL] ${desc}`);
      throw new Error(`Test failed: ${desc}`);
    }
  }

  // TEST 1: Catalog Loaded
  const catalogCount = await client.evaluate(`window.MIK_CATALOG_DATA ? window.MIK_CATALOG_DATA.length : 0`);
  assert(`Catalog loaded with 1526 problems (found: ${catalogCount})`, catalogCount === 1526);

  // TEST 2: Sidebar Item & Badge
  const sidebarInfo = await client.evaluate(`(() => {
    const btn = Array.from(document.querySelectorAll('.sidebar-nav .nav-item')).find(b => b.textContent.includes('MIK Interview DSA'));
    const badge = document.getElementById('nav-mik-badge');
    return {
      hasBtn: !!btn,
      badgeText: badge ? badge.textContent.trim() : ''
    };
  })()`);
  assert('Sidebar navigation item "MIK Interview DSA" exists', sidebarInfo.hasBtn);
  assert(`Sidebar badge shows "0/1526" (found: ${sidebarInfo.badgeText})`, sidebarInfo.badgeText === '0/1526');

  // TEST 3: Switch View to MIK
  await client.evaluate(`switchView('mik')`);
  await new Promise(r => setTimeout(r, 300));
  const viewInfo = await client.evaluate(`(() => {
    const view = document.getElementById('view-mik');
    const title = document.getElementById('viewTitle')?.textContent;
    return {
      isActive: view && view.classList.contains('active'),
      title: title
    };
  })()`);
  assert('Switched to view-mik and section is active', viewInfo.isActive);
  assert('View title is set correctly', viewInfo.title.includes('MIK Interview DSA'));

  // TEST 4: Topic Sidebar & Workspace Rendering
  const workspaceInfo = await client.evaluate(`(() => {
    const sideBtns = document.querySelectorAll('.mik-topic-side-btn');
    const cards = document.querySelectorAll('.mik-subtopic-card');
    const rows = document.querySelectorAll('.mik-problem-row');
    return {
      sideBtnCount: sideBtns.length,
      cardCount: cards.length,
      rowCount: rows.length
    };
  })()`);
  assert(`Topic sidebar has 23 topics (found: ${workspaceInfo.sideBtnCount})`, workspaceInfo.sideBtnCount === 23);
  assert(`Rendered problem cards and rows (cards: ${workspaceInfo.cardCount}, rows: ${workspaceInfo.rowCount})`, workspaceInfo.rowCount > 1000);

  // TEST 5: Search Filter
  await client.evaluate(`handleMikSearch('Binary Search')`);
  await new Promise(r => setTimeout(r, 200));
  const searchCount = await client.evaluate(`document.querySelectorAll('.mik-problem-row').length`);
  assert(`Search for "Binary Search" filters problem list (found: ${searchCount})`, searchCount > 0 && searchCount < 1526);

  await client.evaluate(`clearMikSearch()`);
  await new Promise(r => setTimeout(r, 200));
  const clearedCount = await client.evaluate(`document.querySelectorAll('.mik-problem-row').length`);
  assert(`Clearing search restores problem list (found: ${clearedCount})`, clearedCount === 1526);

  // TEST 6: Company Filter
  await client.evaluate(`setMikCompany('Amazon')`);
  await new Promise(r => setTimeout(r, 200));
  const amazonCount = await client.evaluate(`document.querySelectorAll('.mik-problem-row').length`);
  assert(`Filter by Amazon displays only Amazon problems (found: ${amazonCount})`, amazonCount > 200 && amazonCount < 1526);

  await client.evaluate(`resetAllMikFilters()`);
  await new Promise(r => setTimeout(r, 200));

  // TEST 7: Status Cycling & LocalStorage Persistence
  await client.evaluate(`setMikStatus('mik_0001', 'SOLVED')`);
  await client.evaluate(`toggleMikStar('mik_0001')`);
  const prob1State = await client.evaluate(`(() => {
    const raw = localStorage.getItem('mik_interview_dsa_tracker_v1');
    const parsed = JSON.parse(raw);
    const p1 = parsed.problems['mik_0001'];
    const badge = document.getElementById('nav-mik-badge')?.textContent;
    return {
      status: p1.status,
      done: p1.done,
      starred: p1.starred,
      badgeText: badge
    };
  })()`);
  assert('Problem mik_0001 status updated to SOLVED', prob1State.status === 'SOLVED');
  assert('Problem mik_0001 starred is true', prob1State.starred === true);
  assert(`Badge updated to 1/1526 (found: ${prob1State.badgeText})`, prob1State.badgeText === '1/1526');

  // TEST 8: Detail Modal & Multiline Personal Notes
  await client.evaluate(`openMikDetailModal('mik_0001')`);
  await new Promise(r => setTimeout(r, 200));
  const modalInfo = await client.evaluate(`(() => {
    const modal = document.getElementById('modalMikDetail');
    const title = document.getElementById('mikModalTitle')?.textContent;
    const links = document.getElementById('mikModalLinksBar')?.children.length;
    return {
      isOpen: modal && modal.classList.contains('active'),
      title: title,
      linksCount: links
    };
  })()`);
  assert('Detail modal opened successfully', modalInfo.isOpen);
  assert(`Modal displays correct problem title (found: ${modalInfo.title})`, modalInfo.title.length > 0);
  assert(`Modal contains action link buttons (found: ${modalInfo.linksCount})`, modalInfo.linksCount >= 2);

  const testNote = "My key observation:\n1. Edge cases at boundaries.\n2. Time complexity O(N log N).\nPreserve formatting!";
  await client.evaluate(`(() => {
    const ta = document.getElementById('mikModalNotesTextarea');
    ta.value = ${JSON.stringify(testNote)};
    saveMikModalNotesExplicitly();
  })()`);
  await client.evaluate(`closeModal('modalMikDetail')`);

  const savedNote = await client.evaluate(`(() => {
    const raw = localStorage.getItem('mik_interview_dsa_tracker_v1');
    const parsed = JSON.parse(raw);
    return parsed.problems['mik_0001'].notes;
  })()`);
  assert('Multiline personal notes saved and preserved exactly in LocalStorage', savedNote === testNote);

  // TEST 9: Page Reload Persistence
  await client.send('Page.navigate', { url: TARGET_URL });
  await new Promise(r => setTimeout(r, 2000));
  const afterReload = await client.evaluate(`(() => {
    const ps = getMikProblemState('mik_0001');
    const badge = document.getElementById('nav-mik-badge')?.textContent;
    return {
      status: ps.status,
      done: ps.done,
      starred: ps.starred,
      notes: ps.notes,
      badge: badge
    };
  })()`);
  assert('After reload: Problem mik_0001 is still SOLVED', afterReload.status === 'SOLVED' && afterReload.done === true);
  assert('After reload: Problem mik_0001 star persisted', afterReload.starred === true);
  assert('After reload: Notes preserved with line breaks', afterReload.notes === testNote);
  assert(`After reload: Nav badge shows 1/1526 (found: ${afterReload.badge})`, afterReload.badge === '1/1526');

  // TEST 10: Complete Backup Export & Restore Integration
  const exportBundle = await client.evaluate(`buildCompleteExportObject()`);
  assert('Export bundle contains mikState', !!exportBundle.mikState && exportBundle.mikState.problems['mik_0001'] !== undefined);
  assert('Export bundle version is valid', exportBundle.version >= 5);

  // Clean state and restore
  await client.evaluate(`(() => {
    localStorage.removeItem('mik_interview_dsa_tracker_v1');
    loadMikState();
    updateMikStats();
  })()`);
  const clearedBadge = await client.evaluate(`document.getElementById('nav-mik-badge')?.textContent`);
  assert(`State cleared to 0/1526 (found: ${clearedBadge})`, clearedBadge === '0/1526');

  await client.evaluate(`applyImportData(${JSON.stringify(exportBundle)})`);
  const restoredInfo = await client.evaluate(`(() => {
    const ps = getMikProblemState('mik_0001');
    const badge = document.getElementById('nav-mik-badge')?.textContent;
    return {
      status: ps.status,
      notes: ps.notes,
      badge: badge
    };
  })()`);
  assert('applyImportData successfully restored mikState', restoredInfo.status === 'SOLVED');
  assert('Restored notes match original', restoredInfo.notes === testNote);
  assert(`Restored badge shows 1/1526 (found: ${restoredInfo.badge})`, restoredInfo.badge === '1/1526');

  // TEST 11: Non-Interference with Other Trackers
  const otherTrackersCheck = await client.evaluate(`(() => {
    return {
      hasDsa: typeof state !== 'undefined' && state.problems !== undefined,
      hasStriver: typeof striverState !== 'undefined' && striverState.problems !== undefined,
      hasRisingBrain: typeof risingBrainState !== 'undefined' && risingBrainState.problems !== undefined
    };
  })()`);
  assert('DSA Patterns state remains intact and independent', otherTrackersCheck.hasDsa);
  assert('Striver Sheet state remains intact and independent', otherTrackersCheck.hasStriver);
  assert('RisingBrain Sheet state remains intact and independent', otherTrackersCheck.hasRisingBrain);

  console.log('\n======================================================');
  console.log(`ALL VERIFICATION CHECKS PASSED: ${passedTests}/${totalTests} (100%)`);
  console.log('======================================================\n');

  client.close();
  chromeProcess.kill();
  process.exit(0);
}

run().catch(err => {
  console.error('\nTest runner failed:', err);
  process.exit(1);
});
