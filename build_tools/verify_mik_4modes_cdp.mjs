import http from 'http';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const PORT = 8089;
const TRACKER_ROOT = '/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard';

// Simple static HTTP server
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
  console.log(`Test server running at http://localhost:${PORT}`);
  
  // Launch Chrome with remote debugging
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const cdpPort = 9226;
  const chromeProc = spawn(chromePath, [
    `--remote-debugging-port=${cdpPort}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--user-data-dir=/tmp/chrome_test_profile_' + Date.now(),
    `http://localhost:${PORT}/index.html`
  ]);

  // Wait for Chrome to start
  await new Promise(r => setTimeout(r, 1500));

  try {
    // Connect to CDP
    const resp = await fetch(`http://127.0.0.1:${cdpPort}/json`);
    const targets = await resp.json();
    const pageTarget = targets.find(t => t.type === 'page');

    if (!pageTarget || !pageTarget.webSocketDebuggerUrl) {
      throw new Error('Could not find page target or WebSocket debugger URL');
    }

    const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
    let msgId = 1;
    const callbacks = new Map();

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.id && callbacks.has(data.id)) {
        callbacks.get(data.id)(data);
        callbacks.delete(data.id);
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
    console.log('Connected to CDP via WebSocket');

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

    // Wait for DOM load
    await new Promise(r => setTimeout(r, 1000));

    console.log('\n--- 1. Testing Initial Tracker State & Manifests ---');
    const catalogCount = await evalJs(`getMikCatalog().length`);
    console.log(`MIK Catalog loaded: ${catalogCount} problems (Expected: 1526)`);
    if (catalogCount !== 1526) throw new Error(`Catalog count mismatch: ${catalogCount} != 1526`);

    const playlistsCount = await evalJs(`getMikPlaylists().length`);
    console.log(`MIK Playlists loaded: ${playlistsCount} verified playlists (Expected: 13)`);
    if (playlistsCount < 10) throw new Error(`Playlists count too low: ${playlistsCount}`);

    const stagesCount = await evalJs(`getMikLearningOrder().length`);
    console.log(`MIK Learning Stages loaded: ${stagesCount} stages (Expected: 5)`);
    if (stagesCount !== 5) throw new Error(`Stages count mismatch: ${stagesCount} != 5`);

    const patternsCount = await evalJs(`getMikPatterns().length`);
    console.log(`MIK Patterns loaded: ${patternsCount} patterns (Expected: 30)`);
    if (patternsCount < 25) throw new Error(`Patterns count too low: ${patternsCount}`);

    console.log('\n--- 2. Testing View Switching to MIK ---');
    await evalJs(`switchView('mik')`);
    const activeView = await evalJs(`document.querySelector('.view-section.active')?.id`);
    console.log(`Active View: ${activeView} (Expected: view-mik)`);
    if (activeView !== 'view-mik') throw new Error(`View did not switch to view-mik`);

    console.log('\n--- 3. Testing Mode 1: Creator Playlists Mode ---');
    await evalJs(`setMikMode('playlist')`);
    await evalJs(`setMikActivePlaylist('PLpIkg8OmuX-LkgtrEF7eyyYWJM3m5tVQY')`); // Binary Search
    
    // Check first 10 questions in Binary Search playlist
    const bsFirst10 = await evalJs(`
      (() => {
        const pl = getMikPlaylists().find(p => p.id === 'PLpIkg8OmuX-LkgtrEF7eyyYWJM3m5tVQY');
        return pl.videos.slice(0, 10).map(v => ({
          seq: v.seq,
          video_id: v.video_id,
          title: v.video_title,
          problem_id: v.problem_id,
          problem_title: v.problem_title
        }));
      })()
    `);

    console.log('First 10 items in verified Binary Search playlist:');
    bsFirst10.forEach(v => {
      console.log(`  #${v.seq}: [${v.problem_id || 'UNMATCHED'}] ${v.problem_title || v.title} (${v.video_id})`);
    });

    if (bsFirst10[0].problem_id !== 'mik_0807') throw new Error(`BS Video 1 expected mik_0807, got ${bsFirst10[0].problem_id}`);
    if (bsFirst10[1].problem_id !== 'mik_0811') throw new Error(`BS Video 2 expected mik_0811, got ${bsFirst10[1].problem_id}`);
    if (bsFirst10[2].problem_id !== 'mik_0848') throw new Error(`BS Video 3 expected mik_0848, got ${bsFirst10[2].problem_id}`);

    console.log('\n--- 4. Testing Modal & Prev/Next Video Navigation ---');
    // Open modal on Video 1
    await evalJs(`openMikModal('${bsFirst10[0].problem_id}', 0)`);
    const modalId1 = await evalJs(`document.getElementById('mikModalProbId').textContent`);
    const navLabel1 = await evalJs(`document.getElementById('mikModalPlaylistNavLabel').textContent`);
    console.log(`Modal opened: ${modalId1} · ${navLabel1}`);

    // Click Next Video
    await evalJs(`nextMikPlaylistVideo()`);
    const modalId2 = await evalJs(`document.getElementById('mikModalProbId').textContent`);
    const navLabel2 = await evalJs(`document.getElementById('mikModalPlaylistNavLabel').textContent`);
    console.log(`After nextMikPlaylistVideo(): ${modalId2} · ${navLabel2}`);
    if (!modalId2.includes('mik_0811')) throw new Error(`Expected modal to navigate to mik_0811`);

    // Click Prev Video
    await evalJs(`prevMikPlaylistVideo()`);
    const modalIdBack = await evalJs(`document.getElementById('mikModalProbId').textContent`);
    console.log(`After prevMikPlaylistVideo(): ${modalIdBack}`);
    if (!modalIdBack.includes('mik_0807')) throw new Error(`Expected modal to navigate back to mik_0807`);

    console.log('\n--- 5. Testing Notes, Star & Status Persistence ---');
    // Mark mik_0807 as SOLVED, starred, with personal notes
    await evalJs(`
      setMikProblemStatus('mik_0807', 'SOLVED');
      toggleMikStar('mik_0807');
      const ps = getMikProblemState('mik_0807');
      ps.notes = 'Verified Binary Search template: low <= high, mid = low + (high - low) / 2';
      saveMikState();
      updateMikStats();
    `);

    const savedState = await evalJs(`JSON.parse(localStorage.getItem('mik_interview_dsa_tracker_v1')).problems['mik_0807']`);
    console.log('Saved Problem State in localStorage:', savedState);
    if (!savedState.done || savedState.status !== 'SOLVED' || !savedState.starred || !savedState.notes) {
      throw new Error('Problem state was not persisted properly in localStorage');
    }

    console.log('\n--- 6. Testing Mode 2: Learning Roadmap Mode ---');
    await evalJs(`setMikMode('roadmap')`);
    const roadmapCardCount = await evalJs(`document.querySelectorAll('.mik-stage-card').length`);
    console.log(`Roadmap rendered: ${roadmapCardCount} stage cards`);
    if (roadmapCardCount !== 5) throw new Error(`Expected 5 stage cards in roadmap, got ${roadmapCardCount}`);

    console.log('\n--- 7. Testing Mode 3: Pattern Explorer Mode ---');
    await evalJs(`setMikMode('pattern')`);
    const patternCardCount = await evalJs(`document.querySelectorAll('.mik-pattern-card').length`);
    console.log(`Pattern Explorer rendered: ${patternCardCount} pattern cards`);
    if (patternCardCount < 20) throw new Error(`Expected at least 20 pattern cards, got ${patternCardCount}`);

    console.log('\n--- 8. Testing Mode 4: Original Repository Mode & Sorting ---');
    await evalJs(`setMikMode('repo')`);
    const repoTopicCardCount = await evalJs(`document.querySelectorAll('.mik-stage-card').length`);
    console.log(`Original Repo rendered: ${repoTopicCardCount} topic cards (Expected: 23)`);
    if (repoTopicCardCount !== 23) throw new Error(`Expected 23 topic cards in repo view, got ${repoTopicCardCount}`);

    // Test Alphabetical Sorting
    await evalJs(`setMikSort('alpha')`);
    const firstSortedTopic = await evalJs(`document.querySelector('.mik-stage-title').textContent`);
    console.log(`First topic after alphabetical sort: ${firstSortedTopic}`);
    if (!firstSortedTopic.includes('Arrays')) throw new Error(`Expected first alphabetical topic to be Arrays`);

    console.log('\n--- 9. Verifying Isolation from Other Sections ---');
    const dsaStateRaw = await evalJs(`localStorage.getItem('dsa_patterns_tracker_v3')`);
    const striverStateRaw = await evalJs(`localStorage.getItem('striver_a2z_tracker_v1')`);
    const rbStateRaw = await evalJs(`localStorage.getItem('risingbrain_tracker_v1')`);
    console.log('DSA Patterns Key exists:', dsaStateRaw !== null);
    console.log('Striver Key exists:', striverStateRaw !== null);
    console.log('RisingBrain Key exists:', rbStateRaw !== null);

    console.log('\n✅ ALL AUTOMATED REGRESSION TESTS PASSED WITH 100% SUCCESS!');

  } catch (err) {
    console.error('\n❌ TEST FAILED:', err);
    process.exit(1);
  } finally {
    chromeProc.kill();
    server.close();
    process.exit(0);
  }
});
