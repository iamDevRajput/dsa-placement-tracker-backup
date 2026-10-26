import http from 'http';
import fs from 'fs';

async function getPageTarget(url) {
  const encodedUrl = encodeURIComponent(url);
  const res = await fetch(`http://localhost:9222/json/new?${encodedUrl}`, { method: 'PUT' });
  const data = await res.json();
  return data;
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
      this.ws.onmessage = (msg) => {
        const data = JSON.parse(msg.data);
        if (data.method === 'Runtime.consoleAPICalled') {
          const type = data.params.type;
          const text = data.params.args.map(a => a.value || JSON.stringify(a)).join(' ');
          this.consoleLogs.push({ type, text });
          if (type === 'error') this.consoleErrors.push(text);
        } else if (data.method === 'Runtime.exceptionThrown') {
          this.consoleErrors.push(data.params.exceptionDetails.text + ' ' + (data.params.exceptionDetails.exception?.description || ''));
        }
        if (data.id && this.callbacks.has(data.id)) {
          const cb = this.callbacks.get(data.id);
          this.callbacks.delete(data.id);
          if (data.error) cb.reject(data.error);
          else cb.resolve(data.result);
        }
      };
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = this.id++;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async eval(expr) {
    const res = await this.send('Runtime.evaluate', {
      expression: expr,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      throw new Error(`Eval error: ${res.exceptionDetails.text} - ${JSON.stringify(res.exceptionDetails.exception)}`);
    }
    return res.result ? res.result.value : undefined;
  }
}

async function run() {
  console.log('===============================================================');
  console.log('🧪 RUNNING COMPREHENSIVE RISINGBRAIN INTEGRATION TEST SUITE');
  console.log('===============================================================\n');

  const fileUrl = 'file:///Users/devrajput/.gemini/antigravity-ide/scratch/integrated_v5_test.html';
  const target = await getPageTarget(fileUrl);
  const client = new CDPClient(target.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Page.enable');
  await client.send('Runtime.enable');
  await new Promise(r => setTimeout(r, 1500));

  const results = [];
  function assert(name, condition, details = "") {
    if (condition) {
      results.push({ name, passed: true, details });
      console.log(`  ✅ PASS: ${name} ${details ? '(' + details + ')' : ''}`);
    } else {
      results.push({ name, passed: false, details });
      console.error(`  ❌ FAIL: ${name} - ${details}`);
    }
  }

  // TEST 1: Question Dataset Counts
  const dsaCount = await client.eval(`DATA.reduce((acc, s) => acc + s.problems.length, 0)`);
  const striverCount = await client.eval(`STRIVER_DATA.reduce((acc, s) => acc + s.problems.length, 0)`);
  const rbCount = await client.eval(`totalRisingBrainProbs()`);
  const rbTopicsCount = await client.eval(`RISINGBRAIN_DATA.length`);
  const rbPatternsCount = await client.eval(`RISINGBRAIN_DATA.reduce((acc, t) => acc + t.patterns.length, 0)`);

  assert("DSA Patterns Count is 184", dsaCount === 184, `Got: ${dsaCount}`);
  assert("Striver A2Z Count is 455", striverCount === 455, `Got: ${striverCount}`);
  assert("RisingBrain Count is 385", rbCount === 385, `Got: ${rbCount}`);
  assert("RisingBrain Topics Count is 17", rbTopicsCount === 17, `Got: ${rbTopicsCount}`);
  assert("RisingBrain Patterns Count is 68", rbPatternsCount === 68, `Got: ${rbPatternsCount}`);

  // TEST 2: Switch View to RisingBrain
  await client.eval(`switchView('risingbrain')`);
  await new Promise(r => setTimeout(r, 300));
  const activeView = await client.eval(`document.querySelector('.view-section.active')?.id`);
  const viewHeading = await client.eval(`document.getElementById('viewTitle')?.textContent`);
  assert("Switches View to 'view-risingbrain'", activeView === 'view-risingbrain', `Active: ${activeView}`);
  assert("View Title Updates", viewHeading.includes('RisingBrain'), `Title: ${viewHeading}`);

  // TEST 3: Pattern Card Strategy & Recognition Clues Rendering
  const firstPatCard = await client.eval(`(() => {
    const pat1 = document.querySelector('#risingBrainContent .rb-pattern-card');
    return {
      hasStrategy: !!pat1.querySelector('.rb-strategy-box'),
      strategyText: pat1.querySelector('.rb-strategy-box span:nth-child(2)')?.textContent,
      hasClues: !!pat1.querySelector('.rb-clues-box'),
      cluesText: pat1.querySelector('.rb-clues-box span:nth-child(2)')?.textContent
    };
  })()`);

  assert("Pattern Card renders Strategy box", firstPatCard.hasStrategy && firstPatCard.strategyText.length > 5, firstPatCard.strategyText);
  assert("Pattern Card renders Recognition Clues box", firstPatCard.hasClues && firstPatCard.cluesText.length > 5, firstPatCard.cluesText);

  // TEST 4: Verified External Problem Links
  const prob1Links = await client.eval(`(() => {
    const p1 = document.getElementById('rb-prob-1');
    const lc = p1.querySelector('.lc-badge');
    const gfg = p1.querySelector('.gfg-badge');
    const yt = p1.querySelector('.yt-badge');
    return {
      title: p1.querySelector('.prob-title')?.textContent,
      lcHref: lc?.getAttribute('href'),
      lcTarget: lc?.getAttribute('target'),
      lcRel: lc?.getAttribute('rel'),
      gfgHref: gfg?.getAttribute('href'),
      ytHref: yt?.getAttribute('href')
    };
  })()`);

  assert("Problem #1 Title matches 'Two Sum II'", prob1Links.title === 'Two Sum II', prob1Links.title);
  assert("Problem #1 has verified LeetCode URL opening in new tab",
    prob1Links.lcHref.includes('leetcode.com/problems/two-sum-ii') && prob1Links.lcTarget === '_blank' && prob1Links.lcRel.includes('noopener'),
    prob1Links.lcHref
  );
  assert("Problem #1 has verified GeeksforGeeks link", prob1Links.gfgHref && prob1Links.gfgHref.includes('geeksforgeeks.org'), prob1Links.gfgHref);
  assert("Problem #1 has verified YouTube Video link", prob1Links.ytHref && prob1Links.ytHref.includes('youtube.com'), prob1Links.ytHref);

  // TEST 5: Cross-Reference Badges
  const crossRefSample = await client.eval(`(() => {
    const p1 = document.getElementById('rb-prob-1');
    const crossBadges = Array.from(p1.querySelectorAll('.cross-ref-badge')).map(b => ({
      text: b.textContent,
      title: b.getAttribute('title')
    }));
    return crossBadges;
  })()`);

  assert("Problem #1 shows cross-reference tags", crossRefSample.length >= 1, JSON.stringify(crossRefSample));

  // TEST 6: 6-State Status Tracking & Data Isolation
  // Mark Problem 1 as SOLVED_INDEPENDENT
  await client.eval(`setRisingBrainStatus(1, 'SOLVED_INDEPENDENT')`);
  // Mark Problem 2 as ATTEMPTED
  await client.eval(`setRisingBrainStatus(2, 'ATTEMPTED')`);
  // Mark Problem 3 as MASTERED
  await client.eval(`setRisingBrainStatus(3, 'MASTERED')`);

  const p1State = await client.eval(`getRisingBrainProblemState(1)`);
  const p2State = await client.eval(`getRisingBrainProblemState(2)`);
  const p3State = await client.eval(`getRisingBrainProblemState(3)`);

  assert("Status SOLVED_INDEPENDENT marks done: true", p1State.status === 'SOLVED_INDEPENDENT' && p1State.done === true);
  assert("Status ATTEMPTED keeps done: false", p2State.status === 'ATTEMPTED' && p2State.done === false);
  assert("Status MASTERED marks done: true", p3State.status === 'MASTERED' && p3State.done === true);

  // Check Data Isolation: Striver and DSA states must NOT be affected
  const dsaSolvedCount = await client.eval(`Object.values(state.problems).filter(p => p.done).length`);
  const striverSolvedCount = await client.eval(`Object.values(striverState.problems).filter(p => p.done).length`);
  const rbSolvedCount = await client.eval(`Object.values(risingBrainState.problems).filter(p => p.done).length`);

  assert("RisingBrain Solved Count is exactly 2", rbSolvedCount === 2, `RB Solved: ${rbSolvedCount}`);
  assert("DSA state is NOT modified (Zero contamination)", dsaSolvedCount === 1, `DSA Solved: ${dsaSolvedCount}`);
  assert("Striver state is NOT modified (Zero contamination)", striverSolvedCount === 1, `Striver Solved: ${striverSolvedCount}`);

  // TEST 7: Revision Center Integration for RisingBrain
  await client.eval(`addRevisionEvent(1, 'independent', 25, 'Mastered Two Sum II two-pointer approach', 'O(N) time, O(1) space', 'risingbrain')`);
  const p1RevCount = await client.eval(`getRisingBrainProblemState(1).revisionCount`);
  const p1NextDue = await client.eval(`getRisingBrainProblemState(1).nextDueDate`);
  assert("RisingBrain Revision logged successfully", p1RevCount >= 1, `Revisions: ${p1RevCount}, Next due: ${p1NextDue}`);

  // TEST 8: Search and Filter Functionality
  await client.eval(`
    document.getElementById('rbSearch').value = 'Sort Colors';
    renderRisingBrainContent();
  `);
  await new Promise(r => setTimeout(r, 200));
  const searchResultsCount = await client.eval(`document.querySelectorAll('#risingBrainContent .prob-item').length`);
  const searchTitle = await client.eval(`document.querySelector('#risingBrainContent .prob-title')?.textContent`);
  assert("Search Filter works correctly for 'Dutch National Flag'", searchResultsCount === 1 && searchTitle === 'Sort Colors', `Count: ${searchResultsCount}, Title: ${searchTitle}`);

  // Clear search and test difficulty filter: Easy
  await client.eval(`
    document.getElementById('rbSearch').value = '';
    setRbFilter('e', document.getElementById('f-rb-easy'));
  `);
  await new Promise(r => setTimeout(r, 200));
  const easyCount = await client.eval(`document.querySelectorAll('#risingBrainContent .prob-item').length`);
  assert("Difficulty Filter 'Easy' isolates 81 problems", easyCount === 81, `Easy count: ${easyCount}`);

  // Test difficulty filter: Hard
  await client.eval(`setRbFilter('h', document.getElementById('f-rb-hard'))`);
  await new Promise(r => setTimeout(r, 200));
  const hardCount = await client.eval(`document.querySelectorAll('#risingBrainContent .prob-item').length`);
  assert("Difficulty Filter 'Hard' isolates 53 problems", hardCount === 53, `Hard count: ${hardCount}`);

  // Reset filter to All
  await client.eval(`setRbFilter('all', document.getElementById('f-rb-all'))`);

  // TEST 9: Persistence Across Page Reload
  console.log('Testing persistence across page reload...');
  await client.send('Page.reload', {});
  await new Promise(r => setTimeout(r, 1200));

  const reloadedRbDone = await client.eval(`Object.values(risingBrainState.problems).filter(p => p.done).length`);
  const reloadedDsaDone = await client.eval(`Object.values(state.problems).filter(p => p.done).length`);
  const reloadedStriverDone = await client.eval(`Object.values(striverState.problems).filter(p => p.done).length`);
  const reloadedP1Status = await client.eval(`getRisingBrainProblemState(1).status`);
  const reloadedP1Revs = await client.eval(`getRisingBrainProblemState(1).revisionCount`);

  assert("RisingBrain progress survives page reload", reloadedRbDone === 2, `RB Done: ${reloadedRbDone}`);
  assert("DSA progress survives reload", reloadedDsaDone === 1, `DSA Done: ${reloadedDsaDone}`);
  assert("Striver progress survives reload", reloadedStriverDone === 1, `Striver Done: ${reloadedStriverDone}`);
  assert("Problem #1 status preserved after reload", reloadedP1Status === 'SOLVED_INDEPENDENT', reloadedP1Status);
  assert("Problem #1 revisions preserved after reload", reloadedP1Revs === p1RevCount, `Revs: ${reloadedP1Revs}`);

  // TEST 10: JSON Export & Backup Restore
  const backupBundle = await client.eval(`buildCompleteExportObject()`);
  assert("Export bundle contains all three sheets",
    backupBundle.dsaState && backupBundle.striverState && backupBundle.risingBrainState && backupBundle.version === 5,
    `Version: ${backupBundle.version}, RB Keys: ${Object.keys(backupBundle.risingBrainState?.problems || {}).length}`
  );

  // TEST 11: Zero Console Errors
  if (client.consoleErrors.length > 0) {
    console.error('Console errors detected:', client.consoleErrors);
    assert("Zero runtime console errors", false, client.consoleErrors.join(' | '));
  } else {
    assert("Zero runtime console errors detected", true);
  }

  await client.send('Page.close');

  const passed = results.filter(r => r.passed).length;
  console.log(`\n===============================================================`);
  console.log(`SUMMARY: ${passed} / ${results.length} TESTS PASSED`);
  console.log(`===============================================================`);

  if (passed === results.length) {
    console.log('🎉 ALL INTEGRATION TESTS PASSED 100% WITH ZERO ERRORS!\n');
    process.exit(0);
  } else {
    process.exit(1);
  }
}

run().catch(err => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
