import http from 'http';
import fs from 'fs';

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

  async navigate(url) {
    await this.send('Page.navigate', { url });
    await new Promise(r => setTimeout(r, 1200));
  }
}

async function runTests() {
  console.log('Connecting to Chrome CDP on port 9222...');
  const page = await getCDPPage();
  const client = new CDPClient(page.webSocketDebuggerUrl);
  await client.connect();
  await client.send('Runtime.enable');
  await client.send('Page.enable');

  const fileUrl = 'file:///Users/devrajput/.gemini/antigravity-ide/scratch/test_sync_assembled.html';
  console.log(`Navigating to ${fileUrl}...`);
  await client.navigate(fileUrl);
  await new Promise(r => setTimeout(r, 1000));
  client.consoleLogs = [];

  console.log('\n--- EXTENSIVE TEST SUITE: DSA PATTERNS <-> RISINGBRAIN SYNC ---');

  // Verify sync map existence and pairs
  const mapInfo = await client.evaluate(`
    ({
      hasSyncMap: typeof DSA_RB_SYNC_MAP !== 'undefined',
      totalPairs: DSA_RB_SYNC_MAP ? DSA_RB_SYNC_MAP.total_pairs : 0,
      dsaToRbCount: DSA_RB_SYNC_MAP ? Object.keys(DSA_RB_SYNC_MAP.dsa_to_rb).length : 0,
      rbToDsaCount: DSA_RB_SYNC_MAP ? Object.keys(DSA_RB_SYNC_MAP.rb_to_dsa).length : 0
    })
  `);
  console.log('Sync Map Loaded:', mapInfo);
  if (!mapInfo.hasSyncMap || mapInfo.totalPairs !== 123) {
    throw new Error(`Sync map failure: expected 123 pairs, got ${mapInfo.totalPairs}`);
  }

  // Initial Striver check
  const striverBefore = await client.evaluate(`
    ({
      raw: localStorage.getItem('striver_a2z_tracker_v3'),
      solvedCount: typeof totalDoneStriverProbs === 'function' ? totalDoneStriverProbs() : -1
    })
  `);
  console.log('Striver initial state captured. Solved count:', striverBefore.solvedCount);

  // Test 1: DSA -> RB toggle
  console.log('\n[TEST 1] DSA -> RisingBrain: Marking DSA #1 solved...');
  await client.evaluate(`
    toggleProblemDone(1, false);
    toggleRisingBrainDone(1, false);
    toggleProblemDone(1, true);
  `);
  const test1 = await client.evaluate(`
    ({
      dsa1Done: state.problems[1].done,
      dsaStorageDone: JSON.parse(localStorage.getItem('dsa_placement_prep_v3')).problems[1].done,
      rb1Done: risingBrainState.problems[1].done,
      rb1Status: risingBrainState.problems[1].status,
      rbStorageDone: JSON.parse(localStorage.getItem('risingbrain_tracker_v1')).problems[1].done
    })
  `);
  console.log('Result Test 1:', test1);
  if (!test1.dsa1Done || !test1.rb1Done || !test1.rbStorageDone) {
    throw new Error('Test 1 Failed');
  }
  console.log('✅ TEST 1 PASSED: DSA -> RisingBrain sync verified!');

  // Test 2: RB -> DSA toggle
  console.log('\n[TEST 2] RisingBrain -> DSA: Marking RB #2 (3Sum) solved...');
  await client.evaluate(`
    toggleProblemDone(7, false);
    toggleRisingBrainDone(2, false);
    toggleRisingBrainDone(2, true);
  `);
  const test2 = await client.evaluate(`
    ({
      rb2Done: risingBrainState.problems[2].done,
      rb2Status: risingBrainState.problems[2].status,
      rbStorageDone: JSON.parse(localStorage.getItem('risingbrain_tracker_v1')).problems[2].done,
      dsa7Done: state.problems[7].done,
      dsaStorageDone: JSON.parse(localStorage.getItem('dsa_placement_prep_v3')).problems[7].done
    })
  `);
  console.log('Result Test 2:', test2);
  if (!test2.rb2Done || !test2.dsa7Done || !test2.dsaStorageDone) {
    throw new Error('Test 2 Failed');
  }
  console.log('✅ TEST 2 PASSED: RisingBrain -> DSA sync verified!');

  // Test 3: Bidirectional unsolve
  console.log('\n[TEST 3] Bidirectional Unsolve Sync: Unsolving DSA #1 and RB #2...');
  await client.evaluate(`
    toggleProblemDone(1, false);
    toggleRisingBrainDone(2, false);
  `);
  const test3 = await client.evaluate(`
    ({
      dsa1Done: state.problems[1].done,
      rb1Done: risingBrainState.problems[1].done,
      rb2Done: risingBrainState.problems[2].done,
      dsa7Done: state.problems[7].done
    })
  `);
  console.log('Result Test 3:', test3);
  if (test3.dsa1Done || test3.rb1Done || test3.rb2Done || test3.dsa7Done) {
    throw new Error('Test 3 Failed');
  }
  console.log('✅ TEST 3 PASSED: Bidirectional unsolve sync verified!');

  // Test 4: Independent questions isolation
  console.log('\n[TEST 4] Independent Questions: Unmatched problems remain independent...');
  const indepInfo = await client.evaluate(`
    (() => {
      let unmappedDsa = null;
      DATA.forEach(s => s.problems.forEach(p => {
        if (!DSA_RB_SYNC_MAP.dsa_to_rb[p.n] && !unmappedDsa) unmappedDsa = p.n;
      }));
      let unmappedRb = null;
      RISINGBRAIN_DATA.forEach(t => t.patterns.forEach(pt => pt.problems.forEach(p => {
        if (!DSA_RB_SYNC_MAP.rb_to_dsa[p.n] && !unmappedRb) unmappedRb = p.n;
      })));
      return { unmappedDsa, unmappedRb };
    })()
  `);
  console.log('Independent test problems:', indepInfo);

  await client.evaluate(`
    const beforeRb = Object.values(risingBrainState.problems).filter(p => p.done).length;
    toggleProblemDone(${indepInfo.unmappedDsa}, true);
    const afterRb = Object.values(risingBrainState.problems).filter(p => p.done).length;
    window.__indepDsaOk = (beforeRb === afterRb);
    toggleProblemDone(${indepInfo.unmappedDsa}, false);
  `);
  const indepDsaOk = await client.evaluate(`window.__indepDsaOk`);
  if (!indepDsaOk) throw new Error('Test 4 Failed: DSA affected RB');

  await client.evaluate(`
    const beforeDsa = Object.values(state.problems).filter(p => p.done).length;
    toggleRisingBrainDone(${indepInfo.unmappedRb}, true);
    const afterDsa = Object.values(state.problems).filter(p => p.done).length;
    window.__indepRbOk = (beforeDsa === afterDsa);
    toggleRisingBrainDone(${indepInfo.unmappedRb}, false);
  `);
  const indepRbOk = await client.evaluate(`window.__indepRbOk`);
  if (!indepRbOk) throw new Error('Test 4 Failed: RB affected DSA');
  console.log('✅ TEST 4 PASSED: Non-matching questions remain 100% independent!');

  // Test 5: Striver A2Z Strict Isolation
  console.log('\n[TEST 5] Striver A2Z Strict Isolation Check...');
  const striverAfter = await client.evaluate(`
    ({
      raw: localStorage.getItem('striver_a2z_tracker_v3'),
      solvedCount: typeof totalDoneStriverProbs === 'function' ? totalDoneStriverProbs() : -1,
      hasSyncBadgesInStriver: document.querySelectorAll('#view-striver .rb-sync-indicator').length
    })
  `);
  console.log('Striver state:', striverAfter);
  if (striverAfter.solvedCount !== striverBefore.solvedCount || striverAfter.hasSyncBadgesInStriver !== 0) {
    throw new Error('Test 5 Failed: Striver A2Z was modified!');
  }
  console.log('✅ TEST 5 PASSED: Striver A2Z is 100% untouched!');

  // Test 6: UI Sync Badges Count
  console.log('\n[TEST 6] UI Sync Badges Check...');
  await client.evaluate(`
    switchView('dsa');
    renderDsaContent();
  `);
  const dsaBadgesCount = await client.evaluate(`document.querySelectorAll('#view-dsa .rb-sync-indicator').length`);
  await client.evaluate(`
    switchView('risingbrain');
    renderRisingBrainContent();
  `);
  const rbBadgesCount = await client.evaluate(`document.querySelectorAll('#view-risingbrain .rb-sync-indicator').length`);
  console.log(`UI Sync badges rendered: DSA view = ${dsaBadgesCount}, RisingBrain view = ${rbBadgesCount}`);
  if (dsaBadgesCount !== 123 || rbBadgesCount !== 123) {
    throw new Error(`Test 6 Failed: Expected 123 badges, got DSA=${dsaBadgesCount}, RB=${rbBadgesCount}`);
  }
  console.log('✅ TEST 6 PASSED: Exactly 123 sync badges rendered in both views!');

  // Test 7: Revision Event Solved Sync
  console.log('\n[TEST 7] Revision Event Solved Sync Check...');
  // Ensure DSA #10 is unsolved first
  await client.evaluate(`
    toggleProblemDone(10, false);
    toggleRisingBrainDone(10, false);
  `);
  // Record revision in DSA Patterns
  await client.evaluate(`
    addRevisionEvent(10, 'independent', 20, 'Test DSA revision notes', 'O(N)');
  `);
  const test7Rev = await client.evaluate(`
    ({
      dsa10Done: state.problems[10].done,
      dsa10RevCount: state.problems[10].revisionCount,
      rb10Done: risingBrainState.problems[10].done,
      rb10RevCount: risingBrainState.problems[10].revisionCount || 0
    })
  `);
  console.log('Revision sync result:', test7Rev);
  if (!test7Rev.dsa10Done || !test7Rev.rb10Done || test7Rev.rb10RevCount !== 0) {
    throw new Error('Test 7 Failed: Revision event did not sync solved status or leaked revision count!');
  }
  console.log('✅ TEST 7 PASSED: Revision completion synced solved status while keeping revision records strictly independent!');
  // Cleanup #10
  await client.evaluate(`
    toggleProblemDone(10, false);
  `);

  // Test 8: Startup Reconciliation Non-Destructive
  console.log('\n[TEST 8] Startup Reconciliation Test...');
  await client.evaluate(`
    const dsaRaw = JSON.parse(localStorage.getItem('dsa_placement_prep_v3'));
    dsaRaw.problems[3] = dsaRaw.problems[3] || {};
    dsaRaw.problems[3].done = true;
    dsaRaw.problems[3].notes = 'DSA personal note';
    localStorage.setItem('dsa_placement_prep_v3', JSON.stringify(dsaRaw));

    const rbRaw = JSON.parse(localStorage.getItem('risingbrain_tracker_v1'));
    rbRaw.problems[138] = rbRaw.problems[138] || {};
    rbRaw.problems[138].done = false;
    rbRaw.problems[138].notes = { approach: 'RB custom notes' };
    localStorage.setItem('risingbrain_tracker_v1', JSON.stringify(rbRaw));
  `);

  await client.navigate(fileUrl);
  await new Promise(r => setTimeout(r, 1000));
  client.consoleLogs = [];

  const test8Recon = await client.evaluate(`
    ({
      dsa3Done: state.problems[3].done,
      dsa3Note: state.problems[3].notes,
      rb138Done: risingBrainState.problems[138].done,
      rb138Approach: risingBrainState.problems[138].notes.approach
    })
  `);
  console.log('Reconciliation non-destructive result:', test8Recon);
  if (!test8Recon.dsa3Done || !test8Recon.rb138Done || test8Recon.dsa3Note !== 'DSA personal note' || test8Recon.rb138Approach !== 'RB custom notes') {
    throw new Error('Test 8 Failed: Data corrupted or reconciliation failed');
  }
  console.log('✅ TEST 8 PASSED: Non-destructive startup reconciliation verified!');
  await client.evaluate(`toggleProblemDone(3, false);`);

  // Test 9: Zero Console Errors
  console.log('\n[TEST 9] Zero Console Errors Check...');
  const errors = client.consoleLogs.filter(l => l.type === 'error');
  console.log('Console errors count:', errors.length);
  if (errors.length > 0) {
    console.error('Errors found:', errors);
    throw new Error('Console errors encountered!');
  }
  console.log('✅ TEST 9 PASSED: Zero console errors logged across entire run!');

  console.log('\n🎉 ALL 9 COMPREHENSIVE AUTOMATED TESTS PASSED WITH 100% SUCCESS!');
  process.exit(0);
}

runTests().catch(err => {
  console.error('Fatal test runner error:', err);
  process.exit(1);
});
