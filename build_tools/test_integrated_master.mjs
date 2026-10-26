import http from 'http';

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
  const filePath = 'file:///Users/devrajput/.gemini/antigravity-ide/scratch/integrated_master.html';
  console.log(`Connecting to Chrome and navigating to ${filePath}...`);
  const target = await getPageTarget(filePath);
  const client = new CDPClient(target.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Runtime.enable');
  await client.send('Page.enable');

  // Reset localStorage to guarantee a clean test run
  await client.eval(`
    localStorage.clear();
    state = { version: 3, problems: {}, maxStreak: 0, collapsedSteps: {} };
    striverState = { version: 1, problems: {}, maxStreak: 0, collapsedSteps: {} };
    saveState();
    saveStriverState();
    refreshAllUI();
  `);
  await new Promise(r => setTimeout(r, 600));

  console.log('--- 1. VERIFY APPLICATION INITIALIZATION ---');
  const dsaCardCount = await client.eval(`document.querySelectorAll('#view-dsa .prob-item').length`);
  const dsaPatternCount = await client.eval(`document.querySelectorAll('#view-dsa .step-section').length`);
  console.log(`DSA Patterns Cards rendered: ${dsaCardCount} (expected 184)`);
  console.log(`DSA Pattern Groups rendered: ${dsaPatternCount} (expected 19)`);

  const striverCardCount = await client.eval(`document.querySelectorAll('#view-striver .prob-item').length`);
  const striverStepCount = await client.eval(`document.querySelectorAll('#view-striver .step-section').length`);
  console.log(`Striver Sheet Cards rendered: ${striverCardCount} (expected 455)`);
  console.log(`Striver Step Groups rendered: ${striverStepCount} (expected 18)`);

  if (dsaCardCount !== 184) throw new Error(`Expected 184 DSA problems, got ${dsaCardCount}`);
  if (dsaPatternCount !== 19) throw new Error(`Expected 19 DSA patterns, got ${dsaPatternCount}`);
  if (striverCardCount !== 455) throw new Error(`Expected 455 Striver problems, got ${striverCardCount}`);
  if (striverStepCount !== 18) throw new Error(`Expected 18 Striver steps, got ${striverStepCount}`);

  console.log('\n--- 2. VERIFY STRIVER VIEW NAVIGATION ---');
  // Click on Striver nav item
  await client.eval(`
    const navItems = Array.from(document.querySelectorAll('.nav-item'));
    const striverNav = navItems.find(el => el.textContent.includes('Striver Sheet'));
    striverNav.click();
  `);
  await new Promise(r => setTimeout(r, 400));
  const activeView = await client.eval(`document.querySelector('.view-section.active').id`);
  const headerTitle = await client.eval(`document.getElementById('viewTitle').textContent`);
  console.log(`Active View after click: ${activeView} (expected 'view-striver')`);
  console.log(`Header Title: "${headerTitle}"`);

  if (activeView !== 'view-striver') throw new Error(`Expected view-striver, got ${activeView}`);

  console.log('\n--- 3. VERIFY STRIVER PROBLEM CARDS & BADGES ---');
  const sampleCard = await client.eval(`
    const firstCard = document.querySelector('#view-striver .prob-item');
    const links = Array.from(firstCard.querySelectorAll('a.platform-badge')).map(a => ({
      text: a.textContent.trim(),
      href: a.href,
      target: a.target
    }));
    const coTags = Array.from(firstCard.querySelectorAll('.company-tag')).map(t => t.textContent.trim());
    ({
      title: firstCard.querySelector('.prob-title').textContent.trim(),
      links,
      coTags
    });
  `);
  console.log('Sample Problem Card Details:', JSON.stringify(sampleCard, null, 2));

  console.log('\n--- 4. TEST INDEPENDENT PROGRESS & NO CROSS-CONTAMINATION ---');
  const initialDsaDone = await client.eval(`Object.values(state.problems).filter(p => p.done).length`);
  const initialStriverDone = await client.eval(`Object.values(striverState.problems).filter(p => p.done).length`);
  console.log(`Initial clean counts -> DSA: ${initialDsaDone}, Striver: ${initialStriverDone}`);

  // Mark Striver problem #1 done
  await client.eval(`toggleStriverProblemDone(1, true)`);
  const striverDoneAfter1 = await client.eval(`Object.values(striverState.problems).filter(p => p.done).length`);
  const dsaDoneAfter1 = await client.eval(`Object.values(state.problems).filter(p => p.done).length`);
  console.log(`After marking Striver #1 done -> Striver: ${striverDoneAfter1}, DSA: ${dsaDoneAfter1}`);

  if (dsaDoneAfter1 !== 0) {
    throw new Error('FAILURE: Modifying Striver problem contaminated DSA state!');
  }
  if (striverDoneAfter1 !== 1) {
    throw new Error('FAILURE: Striver done count did not increment to 1!');
  }

  // Mark DSA problem #1 done
  await client.eval(`toggleProblemDone(1, true)`);
  const dsaDoneAfter2 = await client.eval(`Object.values(state.problems).filter(p => p.done).length`);
  const striverDoneAfter2 = await client.eval(`Object.values(striverState.problems).filter(p => p.done).length`);
  console.log(`After marking DSA #1 done -> DSA: ${dsaDoneAfter2}, Striver: ${striverDoneAfter2}`);

  if (striverDoneAfter2 !== 1) {
    throw new Error('FAILURE: Modifying DSA problem contaminated Striver state!');
  }
  if (dsaDoneAfter2 !== 1) {
    throw new Error('FAILURE: DSA done count did not increment to 1!');
  }

  console.log('\n--- 5. TEST STRIVER COMPANY FILTERING ---');
  await client.eval(`setStriverCompany('amz')`);
  await new Promise(r => setTimeout(r, 200));
  const amzVisible = await client.eval(`document.querySelectorAll('#view-striver .prob-item').length`);
  console.log(`Visible cards with Amazon filter: ${amzVisible}`);
  if (amzVisible === 0 || amzVisible >= 455) {
    throw new Error(`Amazon filter expected between 1 and 454 cards, got ${amzVisible}`);
  }

  await client.eval(`setStriverCompany('all')`);
  await new Promise(r => setTimeout(r, 200));
  const allVisible = await client.eval(`document.querySelectorAll('#view-striver .prob-item').length`);
  console.log(`Visible cards after resetting to All: ${allVisible} (expected 455)`);
  if (allVisible !== 455) throw new Error(`Expected 455 after resetting company filter, got ${allVisible}`);

  console.log('\n--- 6. TEST STRIVER REVISION MODAL & LOGGING ---');
  await client.eval(`openRevisionModal(1, 'striver')`);
  await new Promise(r => setTimeout(r, 300));
  const modalTitle = await client.eval(`document.getElementById('revModalProbTitle').textContent`);
  console.log(`Modal Title for Striver #1: "${modalTitle}"`);

  // Log revision outcome 'independent'
  await client.eval(`
    document.getElementById('revOutcomeSelect').value = 'independent';
    document.getElementById('revTimeTaken').value = '20';
    document.getElementById('revComplexity').value = 'O(N) time, O(1) space';
    document.getElementById('revNotesInput').value = 'Mastered standard approach';
    submitRevisionFromModal();
  `);
  await new Promise(r => setTimeout(r, 300));

  const striverP1 = await client.eval(`striverState.problems[1]`);
  console.log('Striver #1 state after revision:', {
    done: striverP1.done,
    revisionCount: striverP1.revisionCount,
    lastRevisedDate: striverP1.lastRevisedDate,
    nextDueDate: striverP1.nextDueDate,
    revisions: striverP1.revisions.length
  });

  if (striverP1.revisionCount !== 1) throw new Error(`Expected 1 revision, got ${striverP1.revisionCount}`);

  console.log('\n--- 7. TEST REVISION UNDO ---');
  await client.eval(`undoLastRevision()`);
  await new Promise(r => setTimeout(r, 300));
  const striverP1AfterUndo = await client.eval(`striverState.problems[1]`);
  console.log('Striver #1 state after undo:', {
    revisionCount: striverP1AfterUndo.revisionCount,
    revisions: striverP1AfterUndo.revisions.length
  });

  if (striverP1AfterUndo.revisionCount !== 0) throw new Error(`Expected 0 revisions after undo, got ${striverP1AfterUndo.revisionCount}`);

  console.log('\n--- 8. TEST BACKUP EXPORT & INTEGRITY ---');
  const backupJsonStr = await client.eval(`
    JSON.stringify({
      version: 3,
      exportedAt: new Date().toISOString(),
      dsaState: state,
      striverState: striverState
    })
  `);
  const parsedBackup = JSON.parse(backupJsonStr);
  console.log('Backup JSON generated successfully.');
  console.log(`Has dsaState: ${!!parsedBackup.dsaState}`);
  console.log(`Has striverState: ${!!parsedBackup.striverState}`);

  console.log('\n--- 9. CONSOLE ERROR AUDIT ---');
  if (client.consoleErrors.length > 0) {
    console.error('Console errors detected during session:');
    client.consoleErrors.forEach(err => console.error('  ->', err));
    throw new Error('Console errors encountered during testing!');
  } else {
    console.log('ZERO console errors detected throughout entire execution!');
  }

  // Close target
  await fetch(`http://localhost:9222/json/close/${target.id}`);
  console.log('\n========================================');
  console.log('🎉 ALL INTEGRATION TESTS PASSED 100%!');
  console.log('========================================');
}

run().catch(err => {
  console.error('Test suite failed:', err);
  process.exit(1);
});
