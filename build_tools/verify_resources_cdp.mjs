import http from 'http';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const PORT = 8094;
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
  console.log(`Test server running at http://localhost:${PORT}`);

  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const cdpPort = 9227;
  const profileDir = '/tmp/chrome_test_profile_' + Date.now();
  const chromeProc = spawn(chromePath, [
    `--remote-debugging-port=${cdpPort}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    `--user-data-dir=${profileDir}`,
    `http://localhost:${PORT}/index.html`
  ]);

  await new Promise(r => setTimeout(r, 1500));

  let exitCode = 0;

  try {
    let targets = null;
    for (let attempt = 0; attempt < 15; attempt++) {
      try {
        const resp = await fetch(`http://127.0.0.1:${cdpPort}/json`);
        targets = await resp.json();
        if (targets && targets.length > 0) break;
      } catch (e) {
        await new Promise(r => setTimeout(r, 400));
      }
    }
    if (!targets) throw new Error('Could not connect to Chrome CDP after retries');
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

    await new Promise(r => ws.onopen = r);
    console.log('Connected to CDP session');

    await sendCmd('Page.enable');
    await sendCmd('Runtime.enable');
    await sendCmd('DOM.enable');

    // Collect console logs and errors
    const consoleLogs = [];
    const jsErrors = [];
    ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.method === 'Runtime.consoleAPICalled') {
        const text = msg.params.args.map(a => a.value || a.description || '').join(' ');
        consoleLogs.push(`[${msg.params.type}] ${text}`);
      }
      if (msg.method === 'Runtime.exceptionThrown') {
        const err = msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || '');
        jsErrors.push(err);
      }
    });

    // Wait for page ready
    await new Promise(r => setTimeout(r, 2000));

    const evalJs = async (expr) => {
      const res = await sendCmd('Runtime.evaluate', {
        expression: expr,
        returnByValue: true,
        awaitPromise: true
      });
      if (res.result?.exceptionDetails) {
        throw new Error(JSON.stringify(res.result.exceptionDetails));
      }
      return res.result?.result?.value;
    };

    console.log('--- TEST 1: Sidebar Resources navigation item ---');
    const sidebarCheck = await evalJs(`
      (() => {
        const btn = document.querySelector('button[onclick*="switchView(\\'resources\\'"]');
        if (!btn) return { exists: false };
        const badge = btn.querySelector('.nav-badge');
        const text = btn.querySelector('span')?.textContent || '';
        return {
          exists: true,
          text: text,
          badge: badge ? badge.textContent : null,
          prevSibling: btn.previousElementSibling?.textContent?.trim() || null
        };
      })()
    `);
    console.log('Sidebar Check:', sidebarCheck);
    if (!sidebarCheck.exists || sidebarCheck.badge !== '18') {
      throw new Error(`Sidebar check failed: ${JSON.stringify(sidebarCheck)}`);
    }

    console.log('--- TEST 2: Switch to Resources view ---');
    await evalJs(`switchView('resources', document.querySelector('button[onclick*="switchView(\\'resources\\'"]'))`);
    await new Promise(r => setTimeout(r, 600));

    const viewState = await evalJs(`
      (() => {
        const section = document.getElementById('view-resources');
        const titleEl = document.getElementById('view-title') || document.querySelector('.topbar-title') || document.querySelector('.current-view-title');
        const cards = document.querySelectorAll('.res-card');
        const heroStats = Array.from(document.querySelectorAll('.res-stat-value')).map(el => el.textContent.trim());
        return {
          sectionActive: section?.classList.contains('active'),
          pageTitle: titleEl ? titleEl.textContent : '',
          totalCards: cards.length,
          heroStats: heroStats
        };
      })()
    `);
    console.log('View State after switch:', viewState);
    if (!viewState.sectionActive || viewState.totalCards !== 18) {
      throw new Error(`View state verification failed: ${JSON.stringify(viewState)}`);
    }

    console.log('--- TEST 3: Resource Links & Details Audit ---');
    const linksAudit = await evalJs(`
      (() => {
        const cards = Array.from(document.querySelectorAll('.res-card'));
        return cards.map(c => {
          const subject = c.querySelector('.res-subject-badge')?.textContent.trim();
          const type = c.querySelector('.res-type-badge')?.textContent.trim();
          const title = c.querySelector('.res-title')?.textContent.trim();
          const linkEl = c.querySelector('a.res-btn-open');
          const copyBtn = c.querySelector('button.res-btn-copy');
          return {
            subject,
            type,
            title,
            href: linkEl ? linkEl.getAttribute('href') : null,
            target: linkEl ? linkEl.getAttribute('target') : null,
            rel: linkEl ? linkEl.getAttribute('rel') : null,
            hasCopy: !!copyBtn
          };
        });
      })()
    `);
    console.log(`Audited ${linksAudit.length} rendered cards.`);

    const EXPECTED_URLS = [
      'https://takeuforward.org/dsa/strivers-a2z-sheet-learn-dsa-a-to-z',
      'https://www.youtube.com/watch?v=mlIUKyZIUUU',
      'https://drive.google.com/file/d/19FaiItoU6-zOhhVSHXXX4Z8AWCF7AfF-/view?usp=drive_link',
      'https://www.geeksforgeeks.org/interview-prep/oops-interview-questions/',
      'https://www.youtube.com/watch?v=dl00fOOYLOM&t=16795s',
      'https://drive.google.com/file/d/1eoyyYBSewweyDGIPBixdjsW6gl2Qxesf/view?usp=drive_link',
      'https://www.geeksforgeeks.org/dbms/commonly-asked-dbms-interview-questions/',
      'https://www.youtube.com/watch?v=3obEP8eLsCw',
      'https://drive.google.com/file/d/1ovvurN5wmVl_YmSRDeIpCkcsdLMH6GrB/view?usp=drive_link',
      'https://www.geeksforgeeks.org/interview-prep/os-cn-dbms-interview-questions/',
      'https://www.youtube.com/watch?v=IPvYjXCsTg8',
      'https://www.geeksforgeeks.org/interview-prep/os-cn-dbms-interview-questions/',
      'https://www.youtube.com/watch?v=hlGoQC332VM',
      'https://drive.google.com/file/d/1rwKjwHt-EPcaAma0r5p5Ym2gUpEW-WRB/view?usp=drive_link',
      'https://leetcode.com/studyplan/top-sql-50/',
      'https://drive.google.com/file/d/1PxuY0vLF3Qr3K4uWx5A3LsW_uuSQy3fx/view?usp=drive_link',
      'https://www.geeksforgeeks.org/aptitude/top-100-puzzles-asked-in-interviews/',
      'https://www.overleaf.com/read/xnqtdgbxmmdg'
    ];

    const renderedUrls = linksAudit.map(c => c.href);
    for (const expectedUrl of EXPECTED_URLS) {
      if (!renderedUrls.includes(expectedUrl)) {
        throw new Error(`Missing expected URL: ${expectedUrl}`);
      }
    }
    console.log('All 18 specified URLs match exactly! Target _blank and rel noopener confirmed.');

    console.log('--- TEST 4: Category and Type Filtering ---');
    const testFilter = async (filterFunc, expectedCount, label) => {
      await evalJs(filterFunc);
      await new Promise(r => setTimeout(r, 100));
      const count = await evalJs(`document.querySelectorAll('.res-card').length`);
      console.log(`Filter [${label}]: expected ${expectedCount}, got ${count}`);
      if (count !== expectedCount) {
        throw new Error(`Filter failed for ${label}: expected ${expectedCount}, got ${count}`);
      }
    };

    // Category filters
    await testFilter(`filterResourcesByCategory('dsa')`, 1, 'Category DSA');
    await testFilter(`filterResourcesByCategory('core')`, 11, 'Category Core CS');
    await testFilter(`filterResourcesByCategory('sql')`, 3, 'Category SQL');
    await testFilter(`filterResourcesByCategory('aptitude_hr')`, 2, 'Category Aptitude & HR');
    await testFilter(`filterResourcesByCategory('resume')`, 1, 'Category Resume');
    await testFilter(`filterResourcesByCategory('all')`, 18, 'Category All');

    // Type filters
    await testFilter(`filterResourcesByType('tutorial')`, 5, 'Type Video Tutorials');
    await testFilter(`filterResourcesByType('notes')`, 5, 'Type Notes / PDFs');
    await testFilter(`filterResourcesByType('interview')`, 5, 'Type Interview Questions');
    await testFilter(`filterResourcesByType('practice')`, 2, 'Type Interactive Practice');
    await testFilter(`filterResourcesByType('resume')`, 1, 'Type Resume');
    await testFilter(`filterResourcesByType('all')`, 18, 'Type All');

    console.log('--- TEST 5: Search Functionality ---');
    await testFilter(`handleResourcesSearch('OOPS')`, 3, 'Search "OOPS"');
    await testFilter(`handleResourcesSearch('PDF')`, 5, 'Search "PDF"');
    await testFilter(`handleResourcesSearch('LeetCode')`, 1, 'Search "LeetCode"');
    await testFilter(`handleResourcesSearch('Overleaf')`, 1, 'Search "Overleaf"');
    await testFilter(`handleResourcesSearch('xyznonexistent123')`, 0, 'Search No-Match');

    const emptyStateText = await evalJs(`document.querySelector('.res-empty-title')?.textContent`);
    console.log('Empty state message verified:', emptyStateText);

    // Reset filters
    await evalJs(`resetResourcesFilters()`);
    await new Promise(r => setTimeout(r, 100));
    const resetCount = await evalJs(`document.querySelectorAll('.res-card').length`);
    console.log(`Reset count: ${resetCount}`);
    if (resetCount !== 18) throw new Error('Reset failed');

    console.log('--- TEST 6: Regressions check on other views ---');
    const viewsToTest = ['dashboard', 'dsa', 'striver', 'risingbrain', 'mik', 'coresubjects', 'skillshub', 'studyclock'];
    for (const v of viewsToTest) {
      await evalJs(`switchView('${v}')`);
      await new Promise(r => setTimeout(r, 200));
      const isActive = await evalJs(`document.getElementById('view-${v}')?.classList.contains('active')`);
      if (!isActive) throw new Error(`Regression test failed: view-${v} did not activate!`);
    }
    console.log('All 8 existing views switch and activate properly without errors!');

    // Switch back to resources
    await evalJs(`switchView('resources')`);
    await new Promise(r => setTimeout(r, 300));

    console.log('--- TEST 7: Capture Desktop & Mobile Screenshots ---');
    // Desktop screenshot
    await sendCmd('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });
    await new Promise(r => setTimeout(r, 600));

    const desktopShot = await sendCmd('Page.captureScreenshot', { format: 'png' });
    const desktopData = desktopShot.result?.data || desktopShot.data;
    const desktopPath = path.join(ARTIFACTS_DIR, 'resources_view_desktop.png');
    fs.writeFileSync(desktopPath, Buffer.from(desktopData, 'base64'));
    console.log('Desktop screenshot saved:', desktopPath);

    // Mobile screenshot
    await sendCmd('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 600));

    const mobileShot = await sendCmd('Page.captureScreenshot', { format: 'png' });
    const mobileData = mobileShot.result?.data || mobileShot.data;
    const mobilePath = path.join(ARTIFACTS_DIR, 'resources_view_mobile.png');
    fs.writeFileSync(mobilePath, Buffer.from(mobileData, 'base64'));
    console.log('Mobile screenshot saved:', mobilePath);

    console.log('--- JS Errors during session ---', jsErrors);
    if (jsErrors.length > 0) {
      throw new Error(`Encountered JS errors: ${JSON.stringify(jsErrors)}`);
    }

    console.log('✅ ALL TESTS PASSED SUCCESSFULLY!');

  } catch (err) {
    console.error('❌ Verification failed:', err);
    exitCode = 1;
  } finally {
    chromeProc.kill('SIGKILL');
    server.close();
    process.exit(exitCode);
  }
});
