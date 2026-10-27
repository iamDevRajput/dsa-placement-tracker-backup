import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DASHBOARD_DIR = path.resolve(__dirname, '../dsa-placement-dashboard');

const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'application/javascript',
  '.json': 'application/json',
  '.css': 'text/css',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml'
};

const server = http.createServer((req, res) => {
  let reqPath = req.url.split('?')[0];
  if (reqPath === '/') reqPath = '/index.html';
  const filePath = path.join(DASHBOARD_DIR, reqPath);

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
    res.end(data);
  });
});

const PORT = 8105;
const CDP_PORT = 9235;

server.listen(PORT, async () => {
  console.log(`Sentinel Test Server listening on http://localhost:${PORT}`);

  const testDir = '/tmp/test-profile-mik-sentinel-' + Date.now();
  const chromeProc = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    `--remote-debugging-port=${CDP_PORT}`,
    '--window-size=1440,900',
    '--no-sandbox',
    `--user-data-dir=${testDir}`,
    `http://localhost:${PORT}`
  ]);

  await new Promise((r) => setTimeout(r, 2000));

  try {
    const listRes = await fetch(`http://localhost:${CDP_PORT}/json`);
    const targets = await listRes.json();
    const pageTarget = targets.find((t) => t.type === 'page');

    if (!pageTarget || !pageTarget.webSocketDebuggerUrl) {
      throw new Error('No page WebSocket URL found');
    }

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    let msgId = 1;
    const callbacks = new Map();

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id && callbacks.has(msg.id)) {
        callbacks.get(msg.id)(msg);
        callbacks.delete(msg.id);
      }
    };

    const sendCmd = (method, params = {}) => {
      return new Promise((resolve) => {
        const id = msgId++;
        callbacks.set(id, resolve);
        ws.send(JSON.stringify({ id, method, params }));
      });
    };

    await new Promise((r) => (ws.onopen = r));
    console.log('Connected to isolated CDP via WebSocket');

    await sendCmd('Runtime.enable');
    await sendCmd('Page.enable');

    const evalJs = async (expr) => {
      const res = await sendCmd('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
      if (res.result?.exceptionDetails) {
        console.error('CDP Eval Exception:', res.result.exceptionDetails);
        throw new Error(res.result.exceptionDetails.text || 'Eval failed');
      }
      return res.result?.result?.value;
    };

    await new Promise(r => setTimeout(r, 1200));

    console.log('\n--- 1. Seeding Sentinel Data for Other Trackers ---');
    const sentinels = {
      dsa_placement_prep_v3: JSON.stringify({
        sentinel_token: 'DSA_SENTINEL_TOKEN_ALPHA_999',
        verified_date: '2026-10-27T18:59:00.000Z',
        topics: { 'Arrays': { solved: [1, 2, 3] }, 'DP': { solved: [10, 11] } }
      }),
      striver_a2z_tracker_v3: JSON.stringify({
        sentinel_token: 'STRIVER_SENTINEL_TOKEN_BETA_888',
        verified_date: '2026-10-27T18:59:00.000Z',
        completedSteps: [1, 2, 3, 4]
      }),
      risingbrain_tracker_v1: JSON.stringify({
        sentinel_token: 'RISING_BRAIN_SENTINEL_GAMMA_777',
        verified_date: '2026-10-27T18:59:00.000Z',
        patternsCompleted: ['Sliding Window', 'Two Pointers']
      })
    };

    await evalJs(`
      localStorage.setItem('dsa_placement_prep_v3', ${JSON.stringify(sentinels.dsa_placement_prep_v3)});
      localStorage.setItem('striver_a2z_tracker_v3', ${JSON.stringify(sentinels.striver_a2z_tracker_v3)});
      localStorage.setItem('risingbrain_tracker_v1', ${JSON.stringify(sentinels.risingbrain_tracker_v1)});
    `);

    console.log('Successfully seeded 3 sentinel keys into isolated localStorage.');

    console.log('\n--- 2. Exercising MIK View, Modes, Problem Status, Stars & Notes ---');
    // Switch to MIK view
    await evalJs(`switchView('mik')`);

    // Switch across all 5 modes
    console.log('Exercising Mode 1: playlist');
    await evalJs(`setMikMode('playlist')`);
    await evalJs(`setMikActivePlaylist('PLpIkg8OmuX-KJPC18SGiRUzJQAYo839ox')`);

    console.log('Exercising Mode 2: roadmap');
    await evalJs(`setMikMode('roadmap')`);
    await evalJs(`setMikActiveStage('stage_2')`);

    console.log('Exercising Mode 3: pattern');
    await evalJs(`setMikMode('pattern')`);
    await evalJs(`setMikActivePatternCategory('Dynamic Programming')`);

    console.log('Exercising Mode 4: repo');
    await evalJs(`setMikMode('repo')`);
    await evalJs(`setMikSort('alpha')`);

    console.log('Exercising Mode 5: all');
    await evalJs(`setMikMode('all')`);
    await evalJs(`setMikAllPage(3)`);
    await evalJs(`handleMikSearchInput('tree')`);
    await evalJs(`clearMikSearch()`);

    // Modify multiple MIK problems (status, star, notes)
    console.log('Modifying MIK problems...');
    await evalJs(`
      (() => {
        // Problem 1: mik_0807 (Binary Search)
        setMikProblemStatus('mik_0807', 'SOLVED');
        toggleMikStar('mik_0807');
        const st1 = getMikProblemState('mik_0807');
        st1.notes = 'Sentinel Test Note for mik_0807: Binary Search Boundary Template';

        // Problem 2: mik_0361 (Word Search - Backtracking)
        setMikProblemStatus('mik_0361', 'IN_PROGRESS');
        toggleMikStar('mik_0361');
        const st2 = getMikProblemState('mik_0361');
        st2.notes = 'Sentinel Test Note for mik_0361: DFS grid search with backtracking visited marker';

        // Problem 3: mik_0001
        setMikProblemStatus('mik_0001', 'REVISE');
        const st3 = getMikProblemState('mik_0001');
        st3.notes = 'Sentinel Test Note for mik_0001: Review logic';

        saveMikState();
        updateMikStats();
      })()
    `);

    console.log('\n--- 3. Verifying Sentinel Integrity ---');
    const dsaCheck = await evalJs(`localStorage.getItem('dsa_placement_prep_v3')`);
    const striverCheck = await evalJs(`localStorage.getItem('striver_a2z_tracker_v3')`);
    const rbCheck = await evalJs(`localStorage.getItem('risingbrain_tracker_v1')`);

    if (dsaCheck !== sentinels.dsa_placement_prep_v3) {
      throw new Error('dsa_placement_prep_v3 sentinel was modified or corrupted!');
    }
    console.log('✓ dsa_placement_prep_v3 sentinel matches 100% exactly.');

    if (striverCheck !== sentinels.striver_a2z_tracker_v3) {
      throw new Error('striver_a2z_tracker_v3 sentinel was modified or corrupted!');
    }
    console.log('✓ striver_a2z_tracker_v3 sentinel matches 100% exactly.');

    if (rbCheck !== sentinels.risingbrain_tracker_v1) {
      throw new Error('risingbrain_tracker_v1 sentinel was modified or corrupted!');
    }
    console.log('✓ risingbrain_tracker_v1 sentinel matches 100% exactly.');

    console.log('\n--- 4. Verifying MIK State Was Properly Saved Under Its Own Key ---');
    const mikStateRaw = await evalJs(`localStorage.getItem('mik_interview_dsa_tracker_v1')`);
    if (!mikStateRaw) throw new Error('mik_interview_dsa_tracker_v1 not found in localStorage!');
    const mikParsed = JSON.parse(mikStateRaw);
    console.log(`MIK Problems tracked: ${Object.keys(mikParsed.problems).length}`);
    console.log('mik_0807 status:', mikParsed.problems['mik_0807']?.status, 'notes:', mikParsed.problems['mik_0807']?.notes?.slice(0, 30) + '...');
    console.log('mik_0361 status:', mikParsed.problems['mik_0361']?.status, 'notes:', mikParsed.problems['mik_0361']?.notes?.slice(0, 30) + '...');
    console.log('mik_0001 status:', mikParsed.problems['mik_0001']?.status, 'notes:', mikParsed.problems['mik_0001']?.notes?.slice(0, 30) + '...');

    if (mikParsed.problems['mik_0807']?.status !== 'SOLVED' || !mikParsed.problems['mik_0807']?.notes) {
      throw new Error('mik_0807 state was not properly persisted');
    }
    if (mikParsed.problems['mik_0361']?.status !== 'IN_PROGRESS' || !mikParsed.problems['mik_0361']?.notes) {
      throw new Error('mik_0361 state was not properly persisted');
    }

    console.log('\n✅ SENTINEL ISOLATION TEST PASSED: ALL EXISTING TRACKERS REMAIN 100% UNTOUCHED!');

  } catch (err) {
    console.error('\n❌ SENTINEL TEST FAILED:', err);
    process.exit(1);
  } finally {
    chromeProc.kill();
    server.close();
    process.exit(0);
  }
});
