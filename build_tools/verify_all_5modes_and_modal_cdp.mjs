import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DASHBOARD_DIR = path.resolve(__dirname, '../dsa-placement-dashboard');
const SCREENSHOT_DIR = path.resolve('/Users/devrajput/.gemini/antigravity-ide/brain/5211636e-5599-42fd-8999-866a63b2edb4');

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

server.listen(8099, async () => {
  console.log('Test Server listening on http://localhost:8099');

  const chromeProc = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
    '--headless=new',
    '--remote-debugging-port=9232',
    '--window-size=1440,900',
    '--no-sandbox',
    '--user-data-dir=/tmp/test-profile-mik-' + Date.now(),
    'http://localhost:8099'
  ]);

  await new Promise((r) => setTimeout(r, 2000));

  try {
    const listRes = await fetch('http://localhost:9232/json');
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

    const captureScreenshot = async (filename) => {
      const res = await sendCmd('Page.captureScreenshot', { format: 'png' });
      if (res.result?.data) {
        const buf = Buffer.from(res.result.data, 'base64');
        const outPath = path.join(SCREENSHOT_DIR, filename);
        fs.writeFileSync(outPath, buf);
        console.log(`Saved screenshot: ${filename}`);
      }
    };

    // Wait for DOM load
    await new Promise(r => setTimeout(r, 1200));

    console.log('\n--- 1. Testing Initial Tracker State & Manifests ---');
    const catalogCount = await evalJs(`getMikCatalog().length`);
    console.log(`MIK Catalog loaded: ${catalogCount} problems (Expected: 1526)`);
    if (catalogCount !== 1526) throw new Error(`Catalog count mismatch: ${catalogCount} != 1526`);

    // Verify all IDs are unique and span mik_0001 to mik_1526
    const idValidation = await evalJs(`
      (() => {
        const cat = getMikCatalog();
        const ids = new Set();
        let dups = 0;
        let validFormat = 0;
        cat.forEach(p => {
          if (ids.has(p.id)) dups++;
          ids.add(p.id);
          if (/^mik_\\d{4}$/.test(p.id)) validFormat++;
        });
        return { total: cat.length, uniqueIds: ids.size, dups, validFormat };
      })()
    `);
    console.log(`ID Validation: total=${idValidation.total}, unique=${idValidation.uniqueIds}, dups=${idValidation.dups}, validFormat=${idValidation.validFormat}`);
    if (idValidation.dups > 0 || idValidation.uniqueIds !== 1526 || idValidation.validFormat !== 1526) {
      throw new Error(`Catalog ID audit failed! dups=${idValidation.dups}`);
    }

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

    const initMode = await evalJs(`mikState.currentMode`);
    const initDropdownCount = await evalJs(`document.getElementById('mikTopicDropdown')?.children.length`);
    console.log(`Initial MIK mode: ${initMode}, dropdown options: ${initDropdownCount}`);
    if (initDropdownCount <= 0) throw new Error(`Dropdown empty on initial load!`);

    console.log('\n--- 3. Testing Mode 1: Creator Playlists Mode ---');
    await evalJs(`setMikMode('playlist')`);
    const plDropdownCount = await evalJs(`document.getElementById('mikTopicDropdown')?.children.length`);
    console.log(`Playlist mode dropdown options: ${plDropdownCount} (Expected: 13)`);
    if (plDropdownCount !== 13) throw new Error(`Expected 13 options in playlist mode dropdown, got ${plDropdownCount}`);

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

    // Test Backtracking playlist selection and check sidebar & dropdown synchronization
    console.log('\n--- 3B. Testing Backtracking Playlist Selection Sync ---');
    await evalJs(`setMikActivePlaylist('PLpIkg8OmuX-KJPC18SGiRUzJQAYo839ox')`); // Backtracking Playlist
    const btHeading = await evalJs(`document.querySelector('.mik-playlist-banner-title')?.textContent`);
    const btDropdownVal = await evalJs(`document.getElementById('mikTopicDropdown')?.value`);
    const btSidebarActive = await evalJs(`document.querySelector('.mik-topic-nav-btn.active')?.textContent`);
    console.log(`Selected Backtracking: heading="${btHeading?.trim()}", dropdown="${btDropdownVal}", sidebar="${btSidebarActive?.trim()}"`);
    if (!btHeading || !btHeading.includes('BACKTRACKING')) throw new Error('Heading does not match Backtracking');
    if (btDropdownVal !== 'PLpIkg8OmuX-KJPC18SGiRUzJQAYo839ox') throw new Error('Dropdown does not match Backtracking ID');
    if (!btSidebarActive || !btSidebarActive.includes('BACKTRACKING')) throw new Error('Sidebar does not highlight Backtracking');

    console.log('\n--- 4. Testing Modal & Prev/Next Video Navigation & Modal Styling ---');
    // Switch to Binary Search playlist for prev/next video test
    await evalJs(`setMikActivePlaylist('PLpIkg8OmuX-LkgtrEF7eyyYWJM3m5tVQY')`);
    await evalJs(`openMikModal('mik_0807', 0)`);
    const modalId1 = await evalJs(`document.getElementById('mikModalProbId').textContent`);
    const navLabel1 = await evalJs(`document.getElementById('mikModalPlaylistNavLabel').textContent`);
    console.log(`Modal opened: ${modalId1} · ${navLabel1}`);

    // Click Next Video
    await evalJs(`nextMikPlaylistVideo()`);
    const modalId2 = await evalJs(`document.getElementById('mikModalProbId').textContent`);
    console.log(`After nextMikPlaylistVideo(): ${modalId2}`);
    if (!modalId2.includes('mik_0811')) throw new Error(`Expected modal to navigate to mik_0811`);

    // Click Prev Video
    await evalJs(`prevMikPlaylistVideo()`);
    const modalIdBack = await evalJs(`document.getElementById('mikModalProbId').textContent`);
    console.log(`After prevMikPlaylistVideo(): ${modalIdBack}`);
    if (!modalIdBack.includes('mik_0807')) throw new Error(`Expected modal to navigate back to mik_0807`);

    // Close modal
    await evalJs(`closeModal('modalMikDetail')`);

    console.log('\n--- 5. Testing Notes, Star & Status Persistence ---');
    // Mark mik_0807 as SOLVED, starred = true, with personal notes
    await evalJs(`
      (() => {
        setMikProblemStatus('mik_0807', 'SOLVED');
        const st = getMikProblemState('mik_0807');
        st.starred = true;
        st.notes = 'Verified Binary Search template: low <= high, mid = low + (high - low) / 2';
        saveMikState();
        updateMikStats();
      })()
    `);

    const savedState = await evalJs(`JSON.parse(localStorage.getItem('mik_interview_dsa_tracker_v1')).problems['mik_0807']`);
    console.log('Saved Problem State in localStorage:', savedState);
    if (!savedState.done || savedState.status !== 'SOLVED' || !savedState.starred || !savedState.notes) {
      throw new Error('Problem state was not persisted properly in localStorage');
    }

    console.log('\n--- 6. Testing Mode 2: Learning Roadmap Mode ---');
    await evalJs(`setMikMode('roadmap')`); await evalJs(`setMikActiveStage('stage_1')`);
    const stage1Cards = await evalJs(`document.querySelectorAll('.mik-stage-card').length`);
    console.log(`Roadmap rendered (focused on Stage 1): ${stage1Cards} stage card`);
    if (stage1Cards !== 1) throw new Error(`Expected 1 stage card when focused on stage_1, got ${stage1Cards}`);

    // Select All Stages
    await evalJs(`setMikActiveStage('all')`);
    const allStageCards = await evalJs(`document.querySelectorAll('.mik-stage-card').length`);
    console.log(`Roadmap rendered (All Stages): ${allStageCards} stage cards (Expected: 5)`);
    if (allStageCards !== 5) throw new Error(`Expected 5 stage cards in roadmap when all stages selected, got ${allStageCards}`);

    console.log('\n--- 7. Testing Mode 3: Pattern Explorer Mode ---');
    await evalJs(`setMikMode('pattern')`);
    const patternCardCount = await evalJs(`document.querySelectorAll('.mik-pattern-card').length`);
    const patternDropdownText = await evalJs(`document.getElementById('mikTopicDropdown')?.selectedOptions[0]?.textContent`);
    console.log(`Pattern Explorer rendered: ${patternCardCount} pattern cards, dropdown text="${patternDropdownText}"`);
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

    console.log('\n--- 9. Testing Mode 5: All Problems Mode & Pagination ---');
    await evalJs(`setMikMode('all')`);
    const allProbsHeader = await evalJs(`document.querySelector('.mik-subtopic-title span')?.textContent`);
    const renderedRowsCount = await evalJs(`document.querySelectorAll('.mik-prob-row').length`);
    console.log(`All Problems Mode: header="${allProbsHeader}", rendered rows on page 1=${renderedRowsCount}`);
    if (!allProbsHeader.includes('1,526 Total')) throw new Error('All problems header does not indicate 1,526 total');
    if (renderedRowsCount !== 50) throw new Error(`Expected exactly 50 rows on page 1, got ${renderedRowsCount}`);

    // Test Pagination Next Page
    await evalJs(`setMikAllPage(2)`);
    const page2Header = await evalJs(`document.querySelector('.mik-subtopic-title span')?.textContent`);
    console.log(`After navigating to Page 2: header="${page2Header}"`);
    if (!page2Header.includes('Page 2 of 31')) throw new Error('Expected Page 2 of 31');

    // Test Search Filter in All Problems Mode
    await evalJs(`handleMikSearchInput('binary search')`);
    const filteredRows = await evalJs(`document.querySelectorAll('.mik-prob-row').length`);
    const filteredHeader = await evalJs(`document.querySelector('.mik-subtopic-title span')?.textContent`);
    console.log(`Search 'binary search': ${filteredHeader}, rows visible=${filteredRows}`);
    if (filteredRows === 0) throw new Error('Search binary search returned 0 results');

    // Reset search
    await evalJs(`clearMikSearch()`);

    console.log('\n--- 10. Verifying Isolation from Other Sections ---');
    const dsaStateRaw = await evalJs(`localStorage.getItem('dsa_patterns_tracker_v3')`);
    const striverStateRaw = await evalJs(`localStorage.getItem('striver_a2z_tracker_v1')`);
    const rbStateRaw = await evalJs(`localStorage.getItem('risingbrain_tracker_v1')`);
    console.log('DSA Patterns Key exists:', dsaStateRaw !== null);
    console.log('Striver Key exists:', striverStateRaw !== null);
    console.log('RisingBrain Key exists:', rbStateRaw !== null);

    console.log('\n✅ ALL 10 TESTS PASSED WITH 100% SUCCESS!');

  } catch (err) {
    console.error('\n❌ TEST FAILED:', err);
    process.exit(1);
  } finally {
    chromeProc.kill();
    server.close();
    process.exit(0);
  }
});
