import http from 'http';
import fs from 'fs';

async function getPageTarget(url, port = 9222) {
  const encodedUrl = encodeURIComponent(url);
  const res = await fetch(`http://localhost:${port}/json/new?${encodedUrl}`, { method: 'PUT' });
  return await res.json();
}

async function closeTarget(targetId, port = 9222) {
  try {
    await fetch(`http://localhost:${port}/json/close/${targetId}`, { method: 'PUT' });
  } catch(e) {}
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
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
        if (msg.id && this.callbacks.has(msg.id)) {
          const { resolve, reject } = this.callbacks.get(msg.id);
          this.callbacks.delete(msg.id);
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
    const id = this.id++;
    return new Promise((resolve, reject) => {
      this.callbacks.set(id, { resolve, reject });
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
  console.log('================================================================');
  console.log('🚀 COMPREHENSIVE AUTOMATED VERIFICATION: ALL 3 DSA TRACKERS');
  console.log('================================================================');

  const targetUrl = 'file:///Users/devrajput/.gemini/antigravity-ide/scratch/test_triple_assembled.html';
  const target = await getPageTarget(targetUrl);
  console.log('Created CDP Target:', target.id);

  const client = new CDPClient(target.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Page.enable');
  await client.send('Runtime.enable');
  await client.send('Network.enable');

  await new Promise(r => setTimeout(r, 1200));

  try {
    // ==============================================================
    // PART 1: DSA PATTERNS TRACKER (184 QUESTIONS)
    // ==============================================================
    console.log('\n--- [1/3] VERIFYING DSA PATTERNS TRACKER ---');
    await client.evaluate(`switchView('dsa')`);
    await new Promise(r => setTimeout(r, 400));

    const dsaHero = await client.evaluate(`
      (() => {
        const view = document.getElementById('view-dsa');
        const title = view.querySelector('.rb-hero-title')?.textContent?.trim();
        const stat = document.getElementById('dsa-header-solved-count')?.textContent?.trim();
        const eRatio = document.getElementById('dsa-easy-ratio')?.textContent?.trim();
        const mRatio = document.getElementById('dsa-med-ratio')?.textContent?.trim();
        const hRatio = document.getElementById('dsa-hard-ratio')?.textContent?.trim();
        return {
          visible: view && window.getComputedStyle(view).display !== 'none',
          title,
          stat,
          eRatio,
          mRatio,
          hRatio
        };
      })()
    `);
    console.log('✓ DSA Hero Header:', dsaHero);
    if (!dsaHero.title.includes('DSA Patterns Tracker') || !dsaHero.eRatio.includes('/ 56') || !dsaHero.mRatio.includes('/ 93') || !dsaHero.hRatio.includes('/ 35')) {
      throw new Error('DSA Hero Header verification failed: ' + JSON.stringify(dsaHero));
    }

    const dsaSidebar = await client.evaluate(`
      (() => {
        const items = document.querySelectorAll('#patternNavSidebar .rb-topic-nav-item');
        const titles = Array.from(items).map(i => i.querySelector('.rb-nav-topic-title')?.textContent?.trim());
        const badges = Array.from(items).map(i => i.querySelector('.rb-nav-icon-badge')?.textContent?.trim());
        return {
          itemCount: items.length,
          sampleTitles: titles.slice(0, 4),
          sampleBadges: badges.slice(0, 4)
        };
      })()
    `);
    console.log('✓ DSA Sidebar (19 Patterns + ALL):', dsaSidebar);
    if (dsaSidebar.itemCount !== 20) {
      throw new Error(`Expected 20 sidebar items for DSA (19 + ALL), found: ${dsaSidebar.itemCount}`);
    }

    const dsaRows = await client.evaluate(`
      (() => {
        const rows = document.querySelectorAll('#dsaContent .rb-prob-row');
        const first = rows[0];
        return {
          rowCount: rows.length,
          firstTitle: first?.querySelector('.rb-prob-name')?.textContent?.trim(),
          firstBadge: first?.querySelector('.rb-ref-pill')?.textContent?.trim(),
          hasLcLink: !!first?.querySelector('.rb-platform-link.lc'),
          revBtn: first?.querySelector('.rb-rev-btn')?.textContent?.trim()
        };
      })()
    `);
    console.log('✓ DSA Problems Rendered:', dsaRows);
    if (dsaRows.rowCount !== 184) {
      throw new Error(`Expected 184 DSA problem rows, found: ${dsaRows.rowCount}`);
    }

    // DSA Search & Clear test
    const dsaSearch = await client.evaluate(`
      (() => {
        const input = document.getElementById('search');
        input.value = 'Pair with Target Sum';
        handleDsaSearchInput('Pair with Target Sum');
        const count = document.querySelectorAll('#dsaContent .rb-prob-row').length;
        const clearVisible = document.getElementById('dsaSearchClearBtn').style.display !== 'none';
        clearDsaSearch();
        const restored = document.querySelectorAll('#dsaContent .rb-prob-row').length;
        return { count, clearVisible, restored };
      })()
    `);
    console.log('✓ DSA Search & Clear:', dsaSearch);
    if (dsaSearch.count < 1 || !dsaSearch.clearVisible || dsaSearch.restored !== 184) {
      throw new Error('DSA search/clear test failed: ' + JSON.stringify(dsaSearch));
    }

    // DSA Solved Toggle & Stats Update
    const dsaSolved = await client.evaluate(`
      (() => {
        toggleProblemDone(1, true);
        const p1 = getProblemState(1);
        const headerCount = document.getElementById('dsa-header-solved-count')?.textContent?.trim();
        const topHeader = document.getElementById('hdr-done')?.textContent?.trim();
        return {
          done: p1.done,
          headerCount,
          topHeader
        };
      })()
    `);
    console.log('✓ DSA Problem Solved Toggle & Stats:', dsaSolved);
    if (!dsaSolved.done || !dsaSolved.headerCount.startsWith('1')) {
      throw new Error('DSA solved toggle failed: ' + JSON.stringify(dsaSolved));
    }

    // ==============================================================
    // PART 2: STRIVER A2Z TRACKER (455 QUESTIONS)
    // ==============================================================
    console.log('\n--- [2/3] VERIFYING STRIVER A2Z TRACKER ---');
    await client.evaluate(`switchView('striver')`);
    await new Promise(r => setTimeout(r, 400));

    const striverHero = await client.evaluate(`
      (() => {
        const view = document.getElementById('view-striver');
        const title = view.querySelector('.rb-hero-title')?.textContent?.trim();
        const stat = document.getElementById('striver-header-solved-count')?.textContent?.trim();
        const eRatio = document.getElementById('striver-easy-ratio')?.textContent?.trim();
        const mRatio = document.getElementById('striver-med-ratio')?.textContent?.trim();
        const hRatio = document.getElementById('striver-hard-ratio')?.textContent?.trim();
        const topHeader = document.getElementById('hdr-done')?.textContent?.trim();
        const topTotal = document.getElementById('hdr-total')?.textContent?.trim();
        return {
          visible: view && window.getComputedStyle(view).display !== 'none',
          title,
          stat,
          eRatio,
          mRatio,
          hRatio,
          topHeader,
          topTotal
        };
      })()
    `);
    console.log('✓ Striver Hero Header:', striverHero);
    if (!striverHero.title.includes('Striver A2Z') || !striverHero.eRatio.includes('/ 125') || !striverHero.mRatio.includes('/ 255') || !striverHero.hRatio.includes('/ 75') || striverHero.topTotal !== '455') {
      throw new Error('Striver Hero Header verification failed: ' + JSON.stringify(striverHero));
    }

    const striverSidebar = await client.evaluate(`
      (() => {
        const items = document.querySelectorAll('#striverStepNavSidebar .rb-topic-nav-item');
        const titles = Array.from(items).map(i => i.querySelector('.rb-nav-topic-title')?.textContent?.trim());
        const badges = Array.from(items).map(i => i.querySelector('.rb-nav-icon-badge')?.textContent?.trim());
        return {
          itemCount: items.length,
          sampleTitles: titles.slice(0, 4),
          sampleBadges: badges.slice(0, 4)
        };
      })()
    `);
    console.log('✓ Striver Sidebar (18 Steps + ALL):', striverSidebar);
    if (striverSidebar.itemCount !== 19) {
      throw new Error(`Expected 19 sidebar items for Striver (18 + ALL), found: ${striverSidebar.itemCount}`);
    }

    const striverRows = await client.evaluate(`
      (() => {
        const rows = document.querySelectorAll('#striverContent .rb-prob-row');
        const first = rows[0];
        return {
          rowCount: rows.length,
          firstTitle: first?.querySelector('.rb-prob-name')?.textContent?.trim(),
          firstBadge: first?.querySelector('.rb-ref-pill')?.textContent?.trim(),
          hasVideoLink: !!first?.querySelector('.rb-platform-link.yt'),
          revBtn: first?.querySelector('.rb-rev-btn')?.textContent?.trim()
        };
      })()
    `);
    console.log('✓ Striver Problems Rendered:', striverRows);
    if (striverRows.rowCount !== 455) {
      throw new Error(`Expected 455 Striver problem rows, found: ${striverRows.rowCount}`);
    }

    // Striver Search & Clear test
    const striverSearch = await client.evaluate(`
      (() => {
        const input = document.getElementById('striverSearch');
        input.value = 'User Input';
        handleStriverSearchInput('User Input');
        const count = document.querySelectorAll('#striverContent .rb-prob-row').length;
        const clearVisible = document.getElementById('striverSearchClearBtn').style.display !== 'none';
        clearStriverSearch();
        const restored = document.querySelectorAll('#striverContent .rb-prob-row').length;
        return { count, clearVisible, restored };
      })()
    `);
    console.log('✓ Striver Search & Clear:', striverSearch);
    if (striverSearch.count < 1 || !striverSearch.clearVisible || striverSearch.restored !== 455) {
      throw new Error('Striver search/clear test failed: ' + JSON.stringify(striverSearch));
    }

    // Striver Solved Toggle & Stats Update
    const striverSolved = await client.evaluate(`
      (() => {
        toggleStriverProblemDone(1, true);
        const p1 = getStriverProblemState(1);
        const headerCount = document.getElementById('striver-header-solved-count')?.textContent?.trim();
        const topHeader = document.getElementById('hdr-done')?.textContent?.trim();
        return {
          done: p1.done,
          headerCount,
          topHeader
        };
      })()
    `);
    console.log('✓ Striver Problem Solved Toggle & Stats:', striverSolved);
    if (!striverSolved.done || !striverSolved.headerCount.startsWith('1') || striverSolved.topHeader !== '1') {
      throw new Error('Striver solved toggle failed: ' + JSON.stringify(striverSolved));
    }

    // ==============================================================
    // PART 3: RISINGBRAIN PATTERN-WISE (385 QUESTIONS)
    // ==============================================================
    console.log('\n--- [3/3] VERIFYING RISINGBRAIN PATTERN-WISE TRACKER ---');
    await client.evaluate(`switchView('risingbrain')`);
    await new Promise(r => setTimeout(r, 400));

    const rbHero = await client.evaluate(`
      (() => {
        const view = document.getElementById('view-risingbrain');
        const title = view.querySelector('.rb-hero-title')?.textContent?.trim();
        const stat = document.getElementById('rb-header-solved-count')?.textContent?.trim();
        const rows = document.querySelectorAll('#risingBrainContent .rb-prob-row').length;
        const topHeader = document.getElementById('hdr-done')?.textContent?.trim();
        const topTotal = document.getElementById('hdr-total')?.textContent?.trim();
        return {
          visible: view && window.getComputedStyle(view).display !== 'none',
          title,
          stat,
          rows,
          topHeader,
          topTotal
        };
      })()
    `);
    console.log('✓ RisingBrain Health & Data Preservation:', rbHero);
    if (!rbHero.title.includes('RisingBrain Pattern Wise') || rbHero.rows !== 385 || rbHero.topTotal !== '385') {
      throw new Error('RisingBrain verification failed: ' + JSON.stringify(rbHero));
    }

    // ==============================================================
    // PART 4: DATA ISOLATION & STORAGE KEYS
    // ==============================================================
    console.log('\n--- VERIFYING STORAGE KEYS & DATA ISOLATION ---');
    const storageCheck = await client.evaluate(`
      (() => {
        const dsaRaw = localStorage.getItem('dsa_placement_prep_v3');
        const strRaw = localStorage.getItem('striver_a2z_tracker_v3');
        const rbRaw = localStorage.getItem('risingbrain_tracker_v1');

        const dsaP1 = getProblemState(1);
        const strP1 = getStriverProblemState(1);
        const rbP1 = getRisingBrainProblemState(1);

        return {
          hasDsaStorage: !!dsaRaw,
          hasStriverStorage: !!strRaw,
          hasRbStorage: !!rbRaw,
          dsaP1Done: dsaP1.done,
          strP1Done: strP1.done,
          rbP1Done: rbP1.done
        };
      })()
    `);
    console.log('✓ Storage Keys & State Isolation:', storageCheck);
    if (!storageCheck.hasDsaStorage || !storageCheck.hasStriverStorage || !storageCheck.hasRbStorage) {
      throw new Error('Storage keys validation failed: ' + JSON.stringify(storageCheck));
    }

    // ==============================================================
    // PART 5: OFFLINE NETWORK EMULATION & RELOAD PERSISTENCE
    // ==============================================================
    console.log('\n--- EMULATING COMPLETE OFFLINE MODE AND RELOADING ---');
    await client.send('Network.emulateNetworkConditions', {
      offline: true,
      latency: 0,
      downloadThroughput: 0,
      uploadThroughput: 0
    });

    await client.send('Page.reload');
    await new Promise(r => setTimeout(r, 1500));

    const offlineCheck = await client.evaluate(`
      (() => {
        const dsaDone = Object.values(state.problems).filter(p => p.done).length;
        const strDone = Object.values(striverState.problems).filter(p => p.done).length;
        const rbDone = Object.values(risingBrainState.problems).filter(p => p.done).length;

        return {
          dsaDone,
          strDone,
          rbDone
        };
      })()
    `);
    console.log('✓ Reload Persistence Under Offline Mode:', offlineCheck);
    if (offlineCheck.dsaDone !== 1 || offlineCheck.strDone !== 1) {
      throw new Error('Offline persistence verification failed: ' + JSON.stringify(offlineCheck));
    }

    // Console Errors
    console.log('\nConsole Errors count:', client.consoleErrors.length);
    if (client.consoleErrors.length > 0) {
      console.log('Errors:', client.consoleErrors);
      throw new Error('Console errors encountered during testing!');
    }

    console.log('\n================================================================');
    console.log('🎉 ALL 3 TRACKERS FULLY VERIFIED WITH 100% PASS RATE & 0 ERRORS!');
    console.log('================================================================\n');

  } finally {
    client.close();
    await closeTarget(target.id);
  }
}

run().catch(err => {
  console.error('TEST FAILED:', err);
  process.exit(1);
});
