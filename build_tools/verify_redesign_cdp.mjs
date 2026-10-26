import http from 'http';
import { spawn } from 'child_process';
import fs from 'fs';

// Helper to interact with Chrome CDP
async function getWebSocketDebuggerUrl(port = 9222) {
  return new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${port}/json/version`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json.webSocketDebuggerUrl);
        } catch (e) {
          reject(e);
        }
      });
    }).on('error', reject);
  });
}

async function createTarget(port = 9222, url = 'about:blank') {
  const encodedUrl = encodeURIComponent(url);
  const res = await fetch(`http://localhost:${port}/json/new?${encodedUrl}`, { method: 'PUT' });
  return await res.json();
}

async function closeTarget(port = 9222, targetId) {
  try {
    await fetch(`http://localhost:${port}/json/close/${targetId}`, { method: 'PUT' });
  } catch(e) {}
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.msgId = 1;
    this.pending = new Map();
    this.events = [];
    this.consoleLogs = [];
    this.consoleErrors = [];
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.id && this.pending.has(msg.id)) {
          const { resolve, reject } = this.pending.get(msg.id);
          this.pending.delete(msg.id);
          if (msg.error) reject(msg.error);
          else resolve(msg.result);
        } else if (msg.method) {
          if (msg.method === 'Runtime.consoleAPICalled') {
            const text = msg.params.args.map(a => a.value || JSON.stringify(a)).join(' ');
            this.consoleLogs.push({ type: msg.params.type, text });
            if (msg.params.type === 'error') {
              this.consoleErrors.push(text);
            }
          } else if (msg.method === 'Runtime.exceptionThrown') {
            this.consoleErrors.push(msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || ''));
          }
        }
      };
    });
  }

  async send(method, params = {}) {
    const id = this.msgId++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
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
      throw new Error('Evaluation error: ' + (res.exceptionDetails.exception?.description || res.exceptionDetails.text));
    }
    return res.result?.value;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function run() {
  console.log('=== VERIFYING RISINGBRAIN REDESIGNED UI VIA CHROME CDP ===');
  const targetUrl = 'file:///Users/devrajput/.gemini/antigravity-ide/scratch/test_redesign_assembled.html';

  let chromeProc = null;
  let target = null;
  let client = null;

  try {
    // Check if chrome port 9222 is open
    let wsUrl = null;
    try {
      wsUrl = await getWebSocketDebuggerUrl(9222);
    } catch (e) {
      console.log('Launching headless Chrome on 9222...');
      chromeProc = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
        '--remote-debugging-port=9222',
        '--headless=new',
        '--no-sandbox',
        '--disable-gpu',
        'about:blank'
      ]);
      await new Promise(r => setTimeout(r, 1200));
      wsUrl = await getWebSocketDebuggerUrl(9222);
    }

    target = await createTarget(9222, targetUrl);
    console.log('Created Target:', target.id);
    client = new CDPClient(target.webSocketDebuggerUrl);
    await client.connect();

    await client.send('Page.enable');
    await client.send('Runtime.enable');
    await client.send('Network.enable');

    await new Promise(r => setTimeout(r, 1500));

    // Switch to RisingBrain view
    await client.evaluate(`switchView('risingbrain')`);
    await new Promise(r => setTimeout(r, 500));

    // 1. Verify View Section Visibility & Hero Header
    const heroCheck = await client.evaluate(`
      (() => {
        const view = document.getElementById('view-risingbrain');
        const heroTitle = document.querySelector('.rb-hero-title')?.textContent?.trim();
        const heroSubtitle = document.querySelector('.rb-hero-subtitle')?.textContent?.trim();
        const totalStat = document.getElementById('rb-header-solved-count')?.textContent?.trim();
        const radialPct = document.getElementById('rb-radial-pct')?.textContent?.trim();
        return {
          viewVisible: view && window.getComputedStyle(view).display !== 'none',
          heroTitle,
          heroSubtitle,
          totalStat,
          radialPct
        };
      })()
    `);
    console.log('✓ Hero Header Check:', heroCheck);
    if (!heroCheck.viewVisible || !heroCheck.heroTitle.includes('RisingBrain Pattern Wise')) {
      throw new Error('Hero Header validation failed: ' + JSON.stringify(heroCheck));
    }

    // 2. Verify Difficulty Breakdown Bars
    const diffBars = await client.evaluate(`
      (() => {
        const eRatio = document.getElementById('rb-easy-ratio')?.textContent?.trim();
        const mRatio = document.getElementById('rb-med-ratio')?.textContent?.trim();
        const hRatio = document.getElementById('rb-hard-ratio')?.textContent?.trim();
        return { eRatio, mRatio, hRatio };
      })()
    `);
    console.log('✓ Difficulty Bars Check:', diffBars);
    if (!diffBars.eRatio.includes('/ 81') || !diffBars.mRatio.includes('/ 251') || !diffBars.hRatio.includes('/ 53')) {
      throw new Error('Difficulty bars ratio validation failed: ' + JSON.stringify(diffBars));
    }

    // 3. Verify Topic Navigation Sidebar
    const sidebarCheck = await client.evaluate(`
      (() => {
        const items = document.querySelectorAll('.rb-topic-nav-item');
        const titles = Array.from(items).map(i => i.querySelector('.rb-nav-topic-title')?.textContent?.trim());
        const badges = Array.from(items).map(i => i.querySelector('.rb-nav-icon-badge')?.textContent?.trim());
        return {
          itemCount: items.length,
          firstFew: titles.slice(0, 5),
          badgeSample: badges.slice(0, 5)
        };
      })()
    `);
    console.log('✓ Sidebar Check:', sidebarCheck);
    if (sidebarCheck.itemCount < 18) { // ALL + 17 topics = 18
      throw new Error('Topic navigation sidebar did not render all 17 topics: ' + sidebarCheck.itemCount);
    }

    // 4. Verify Pattern Cards & Clues
    const patternCards = await client.evaluate(`
      (() => {
        const cards = document.querySelectorAll('.rb-pattern-card');
        const firstCardTitle = cards[0]?.querySelector('.rb-pattern-title')?.textContent?.trim();
        const strategyBox = cards[0]?.querySelector('.rb-pattern-strategy-box')?.textContent?.trim();
        const cluesBox = cards[0]?.querySelector('.rb-pattern-clues-box')?.textContent?.trim();
        return {
          cardCount: cards.length,
          firstCardTitle,
          hasStrategy: !!strategyBox,
          hasClues: !!cluesBox
        };
      })()
    `);
    console.log('✓ Pattern Cards Check:', patternCards);
    if (patternCards.cardCount === 0 || !patternCards.hasStrategy) {
      throw new Error('Pattern cards validation failed: ' + JSON.stringify(patternCards));
    }

    // 5. Verify Problem Rows Details
    const problemRowCheck = await client.evaluate(`
      (() => {
        const rows = document.querySelectorAll('.rb-prob-row');
        const firstRow = rows[0];
        const index = firstRow?.querySelector('.rb-prob-index')?.textContent?.trim();
        const name = firstRow?.querySelector('.rb-prob-name')?.textContent?.trim();
        const diff = firstRow?.querySelector('.rb-diff-badge')?.textContent?.trim();
        const lcLink = firstRow?.querySelector('.rb-platform-link.lc')?.getAttribute('href');
        const statusVal = firstRow?.querySelector('.rb-status-dropdown')?.value;
        const revBtn = firstRow?.querySelector('.rb-rev-btn')?.textContent?.trim();
        return {
          totalRowsRendered: rows.length,
          index,
          name,
          diff,
          hasLcLink: !!lcLink,
          statusVal,
          revBtn
        };
      })()
    `);
    console.log('✓ Problem Rows Check:', problemRowCheck);
    if (problemRowCheck.totalRowsRendered !== 385) {
      throw new Error('Expected 385 problem rows rendered, found: ' + problemRowCheck.totalRowsRendered);
    }

    // 6. Test Interactive Search & Clear Button
    const searchCheck = await client.evaluate(`
      (() => {
        const input = document.getElementById('rbSearch');
        input.value = 'Two Sum';
        handleRbSearchInput('Two Sum');
        const visibleRows = document.querySelectorAll('.rb-prob-row').length;
        const clearBtnVisible = document.getElementById('rbSearchClearBtn').style.display !== 'none';
        
        // Clear search
        clearRbSearch();
        const restoredRows = document.querySelectorAll('.rb-prob-row').length;
        return {
          visibleRows,
          clearBtnVisible,
          restoredRows
        };
      })()
    `);
    console.log('✓ Search & Clear Check:', searchCheck);
    if (searchCheck.visibleRows < 1 || !searchCheck.clearBtnVisible || searchCheck.restoredRows !== 385) {
      throw new Error('Search and clear verification failed: ' + JSON.stringify(searchCheck));
    }

    // 7. Test Empty State
    const emptyStateCheck = await client.evaluate(`
      (() => {
        const input = document.getElementById('rbSearch');
        input.value = 'XYZNONEXISTENTQUERY999';
        handleRbSearchInput('XYZNONEXISTENTQUERY999');
        const emptyState = document.querySelector('.rb-empty-state');
        const resetBtn = document.querySelector('.rb-empty-reset-btn');
        const visible = emptyState && window.getComputedStyle(emptyState).display !== 'none';
        
        // Test clicking reset
        resetAllRbFilters();
        const restoredRows = document.querySelectorAll('.rb-prob-row').length;
        return {
          emptyStateVisible: visible,
          restoredRows
        };
      })()
    `);
    console.log('✓ Empty State Check:', emptyStateCheck);
    if (!emptyStateCheck.emptyStateVisible || emptyStateCheck.restoredRows !== 385) {
      throw new Error('Empty state test failed: ' + JSON.stringify(emptyStateCheck));
    }

    // 8. Test Solved Checkbox & Radial Gauge Update
    const solveCheck = await client.evaluate(`
      (() => {
        // Toggle solved on problem 1
        toggleRisingBrainDone(1, true);
        const p1DoneAfterToggle = getRisingBrainProblemState(1).done;
        const radialPct = document.getElementById('rb-radial-pct')?.textContent?.trim();
        const headerSolved = document.getElementById('rb-header-solved-count')?.textContent?.trim();
        
        return {
          p1DoneAfterToggle,
          radialPct,
          headerSolved
        };
      })()
    `);
    console.log('✓ Solved Toggle & Stats Update Check:', solveCheck);
    if (!solveCheck.p1DoneAfterToggle || !solveCheck.headerSolved.startsWith('1')) {
      throw new Error('Solved toggle test failed: ' + JSON.stringify(solveCheck));
    }

    // 9. Test Next Unsolved Jump
    const jumpCheck = await client.evaluate(`
      (() => {
        jumpToNextUnsolvedRbProblem();
        return true;
      })()
    `);
    console.log('✓ Next Unsolved Jump Check:', jumpCheck);

    // 10. Test Revision Modal with RisingBrain Notes
    const modalCheck = await client.evaluate(`
      (async () => {
        openRevisionModal(1, 'risingbrain');
        const modal = document.getElementById('modalRevision');
        const title = document.getElementById('revModalProbTitle')?.textContent?.trim();
        const num = document.getElementById('revModalProbNum')?.textContent?.trim();
        const approachInput = document.getElementById('probNoteApproach');
        if (approachInput) approachInput.value = 'Two pointers approaching from both ends with sorted array.';
        saveProblemNotesDebounced();
        await new Promise(r => setTimeout(r, 650));
        closeModal('modalRevision');
        
        const ps = getRisingBrainProblemState(1);
        return {
          title,
          num,
          savedNote: ps.notes?.approach
        };
      })()
    `);
    console.log('✓ Revision Modal Check:', modalCheck);
    if (!modalCheck.title.includes('[RisingBrain]') || !modalCheck.savedNote) {
      throw new Error('Revision modal validation failed: ' + JSON.stringify(modalCheck));
    }

    // 11. Emulate Offline Mode and Test Persistence
    console.log('Emulating complete offline network conditions...');
    await client.send('Network.emulateNetworkConditions', {
      offline: true,
      latency: 0,
      downloadThroughput: 0,
      uploadThroughput: 0
    });

    // Reload page under offline conditions
    await client.send('Page.reload');
    await new Promise(r => setTimeout(r, 1500));

    const offlineReloadCheck = await client.evaluate(`
      (() => {
        switchView('risingbrain');
        const p1 = getRisingBrainProblemState(1);
        const totalRows = document.querySelectorAll('.rb-prob-row').length;
        const totalTopics = document.querySelectorAll('.rb-topic-section').length;
        return {
          savedNotePreserved: p1.notes?.approach === 'Two pointers approaching from both ends with sorted array.',
          totalRows,
          totalTopics
        };
      })()
    `);
    console.log('✓ Offline Reload Persistence Check:', offlineReloadCheck);
    if (!offlineReloadCheck.savedNotePreserved || offlineReloadCheck.totalRows !== 385) {
      throw new Error('Offline persistence test failed: ' + JSON.stringify(offlineReloadCheck));
    }

    // 12. Check Console Errors
    console.log('Console Errors count:', client.consoleErrors.length);
    if (client.consoleErrors.length > 0) {
      console.log('Errors:', client.consoleErrors);
      throw new Error('Found console errors during execution!');
    }

    console.log('\n======================================================');
    console.log('🎉 ALL 12 VERIFICATION CHECKS PASSED WITH 0 ERRORS!');
    console.log('======================================================\n');

  } finally {
    if (client) client.close();
    if (target) await closeTarget(9222, target.id);
  }
}

run().catch(err => {
  console.error('TEST FAILED:', err);
  process.exit(1);
});
