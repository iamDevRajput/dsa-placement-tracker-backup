import http from 'http';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const PORT = 8097;
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

  res.writeHead(200, {
    'Content-Type': mimeMap[ext] || 'text/plain',
    'Cache-Control': 'no-cache, no-store, must-revalidate'
  });
  fs.createReadStream(filePath).pipe(res);
});

server.listen(PORT, async () => {
  console.log(`Test server running on http://127.0.0.1:${PORT}`);
  await runTests();
});

async function runTests() {
  const cdpPort = 9226;
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const chromeProc = spawn(chromePath, [
    '--headless=new',
    `--remote-debugging-port=${cdpPort}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=/tmp/chrome-test-profile-' + Date.now()
  ]);

  let targets = null;
  for (let attempt = 0; attempt < 25; attempt++) {
    try {
      const resp = await fetch(`http://127.0.0.1:${cdpPort}/json`);
      targets = await resp.json();
      if (targets && targets.length > 0) break;
    } catch (e) {
      await new Promise(r => setTimeout(r, 400));
    }
  }

  if (!targets) {
    console.error('Could not connect to Chrome CDP endpoint');
    chromeProc.kill();
    server.close();
    process.exit(1);
  }

  const pageTarget = targets.find(t => t.type === 'page');
  if (!pageTarget || !pageTarget.webSocketDebuggerUrl) {
    console.error('Could not find page target debugger URL');
    chromeProc.kill();
    server.close();
    process.exit(1);
  }

  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

  let idCounter = 1;
  const pending = new Map();
  const jsErrors = [];

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.method === 'Runtime.exceptionThrown') {
      const desc = msg.params.exceptionDetails?.exception?.description || msg.params.exceptionDetails?.text;
      console.error('CDP JS Exception:', desc);
      jsErrors.push(desc);
    }
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(msg.error);
      else resolve(msg.result);
    }
  };

  function sendCommand(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = idCounter++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async function evaluate(expression) {
    const res = await sendCommand('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    if (res.exceptionDetails) {
      const text = res.exceptionDetails.exception?.description || res.exceptionDetails.text;
      throw new Error('Evaluation error: ' + text);
    }
    return res.result?.value;
  }

  async function captureScreenshot(filepath, clip = null) {
    const params = { format: 'png' };
    if (clip) params.clip = clip;
    const res = await sendCommand('Page.captureScreenshot', params);
    fs.writeFileSync(filepath, Buffer.from(res.data, 'base64'));
    console.log(`Saved screenshot to ${filepath}`);
  }

  try {
    await new Promise(resolve => ws.onopen = resolve);
    await sendCommand('Runtime.enable');
    await sendCommand('Page.enable');
    await sendCommand('Network.enable');
    await sendCommand('Network.setCacheDisabled', { cacheDisabled: true });
    await sendCommand('Network.setBypassServiceWorker', { bypass: true });

    // Set high-res desktop viewport
    await sendCommand('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 2,
      mobile: false
    });

    console.log('Navigating to http://127.0.0.1:' + PORT);
    await sendCommand('Page.navigate', { url: `http://127.0.0.1:${PORT}/` });
    await new Promise(r => setTimeout(r, 2000));

    // 1. Verify Sidebar Navigation
    console.log('--- Test 1: Sidebar Navigation Item ---');
    const navBtnInfo = await evaluate(`(() => {
      const btn = document.querySelector('.sidebar-nav button[onclick*="jobprep"]');
      const badge = document.getElementById('nav-jobprep-badge');
      return {
        exists: !!btn,
        text: btn ? btn.innerText.trim() : null,
        badgeText: badge ? badge.innerText.trim() : null
      };
    })()`);
    console.log('Nav button info:', navBtnInfo);
    if (!navBtnInfo.exists) throw new Error('Sidebar nav button for jobprep not found');

    // 2. Switch to Job Prep view
    console.log('--- Test 2: Switch to Job Prep View ---');
    const viewTitle = await evaluate(`(() => {
      switchView('jobprep');
      return document.getElementById('viewTitle').textContent;
    })()`);
    console.log('View title after switch:', viewTitle);

    await new Promise(r => setTimeout(r, 600));

    // 3. Verify Overview and Metrics Grid
    console.log('--- Test 3: Overview & Metrics Grid ---');
    const metricsInfo = await evaluate(`(() => {
      const hero = document.querySelector('.jp-hero-card');
      const metricsType = typeof window.calculateJobPrepMetrics;
      let metrics = null;
      let evalErr = null;
      try {
        if (typeof window.calculateJobPrepMetrics === 'function') {
          metrics = window.calculateJobPrepMetrics();
        }
      } catch (e) {
        evalErr = e.message;
      }
      const cards = document.querySelectorAll('.jp-metric-card');
      return {
        heroExists: !!hero,
        metricsType,
        evalErr,
        metricsPresent: !!metrics,
        cardCount: cards.length,
        eligibilityStatus: metrics ? metrics.eligibilityStatus : null,
        todayHours: metrics ? metrics.todayHours : null
      };
    })()`);
    console.log('Metrics info:', metricsInfo);
    if (!metricsInfo.heroExists || metricsInfo.cardCount < 5) {
      throw new Error('Hero card or metrics cards missing');
    }
    if (metricsInfo.eligibilityStatus !== 'needs_verification') {
      throw new Error('Expected default batch eligibility status to be needs_verification');
    }

    // Capture Desktop Overview screenshot
    const scDesktopOverview = path.join(ARTIFACTS_DIR, 'sc_jobprep_desktop_overview.png');
    await captureScreenshot(scDesktopOverview);

    // 4. Test Tab: Eligibility
    console.log('--- Test 4: Tab - Eligibility & Batch ---');
    await evaluate(`window.jobPrepController.setTab('eligibility')`);
    await new Promise(r => setTimeout(r, 400));
    const eligInfo = await evaluate(`(() => {
      const items = document.querySelectorAll('.jp-item-card');
      const table = document.querySelector('.jp-data-table');
      return {
        itemCount: items.length,
        hasTcsTable: !!table,
        batchSelectVal: document.querySelector('.jp-item-card select')?.value
      };
    })()`);
    console.log('Eligibility tab info:', eligInfo);
    if (eligInfo.itemCount !== 4 || !eligInfo.hasTcsTable) {
      throw new Error('Eligibility criteria or TCS table missing');
    }

    const scElig = path.join(ARTIFACTS_DIR, 'sc_jobprep_eligibility.png');
    await captureScreenshot(scElig);

    // 5. Test Tab: 3-Round Pipeline
    console.log('--- Test 5: Tab - 3-Round Pipeline ---');
    await evaluate(`window.jobPrepController.setTab('pipeline')`);
    await new Promise(r => setTimeout(r, 400));
    const pipelineInfo = await evaluate(`(() => {
      const rounds = document.querySelectorAll('.jp-pipeline-round-card');
      const dangerCallout = document.querySelector('.callout-danger');
      return {
        roundCount: rounds.length,
        has90PercentCallout: !!dangerCallout && dangerCallout.textContent.includes('90%')
      };
    })()`);
    console.log('Pipeline info:', pipelineInfo);
    if (pipelineInfo.roundCount !== 3 || !pipelineInfo.has90PercentCallout) {
      throw new Error('Pipeline rounds or 90% elimination callout missing');
    }

    // Toggle a checklist item in Round 1
    await evaluate(`(() => {
      const cb = document.querySelector('.jp-pipeline-checklist input[type="checkbox"]');
      if (cb) { cb.click(); }
    })()`);
    await new Promise(r => setTimeout(r, 200));

    // 6. Test Tab: Quants (35 topics in 6 groups)
    console.log('--- Test 6: Tab - Quants ---');
    await evaluate(`window.jobPrepController.setTab('quants')`);
    await new Promise(r => setTimeout(r, 400));
    const quantsInfo = await evaluate(`(() => {
      const groups = document.querySelectorAll('.jp-group-card');
      const topics = document.querySelectorAll('.jp-topic-card');
      const chips = document.querySelectorAll('.jp-chip');
      return {
        groupCount: groups.length,
        topicCount: topics.length,
        chipCount: chips.length
      };
    })()`);
    console.log('Quants info:', quantsInfo);
    if (quantsInfo.groupCount !== 6 || quantsInfo.topicCount !== 35) {
      throw new Error(`Expected 6 groups and 35 topics for Quants, found ${quantsInfo.groupCount} and ${quantsInfo.topicCount}`);
    }

    // Toggle 2 chips in Quants topic 1
    await evaluate(`window.jobPrepController.toggleChip('quants', 'q_num_sys', 'learn')`);
    await evaluate(`window.jobPrepController.toggleChip('quants', 'q_num_sys', 'examples')`);
    await new Promise(r => setTimeout(r, 200));

    const scQuants = path.join(ARTIFACTS_DIR, 'sc_jobprep_quants.png');
    await captureScreenshot(scQuants);

    // 7. Test Tab: Verbal (10 topics)
    console.log('--- Test 7: Tab - Verbal ---');
    await evaluate(`window.jobPrepController.setTab('verbal')`);
    await new Promise(r => setTimeout(r, 400));
    const verbalCount = await evaluate(`document.querySelectorAll('.jp-topic-card').length`);
    console.log('Verbal topic count:', verbalCount);
    if (verbalCount !== 10) throw new Error(`Expected 10 verbal topics, got ${verbalCount}`);

    // 8. Test Tab: Reasoning (19 topics in 7 groups, visual reasoning flagged)
    console.log('--- Test 8: Tab - Reasoning ---');
    await evaluate(`window.jobPrepController.setTab('reasoning')`);
    await new Promise(r => setTimeout(r, 400));
    const reasoningInfo = await evaluate(`(() => {
      const groups = document.querySelectorAll('.jp-group-card');
      const topics = document.querySelectorAll('.jp-topic-card');
      const highPriGroup = document.querySelector('.jp-high-priority-border');
      return {
        groupCount: groups.length,
        topicCount: topics.length,
        hasHighPriFlag: !!highPriGroup && highPriGroup.textContent.includes('HIGH OA FREQUENCY')
      };
    })()`);
    console.log('Reasoning info:', reasoningInfo);
    if (reasoningInfo.groupCount !== 7 || reasoningInfo.topicCount !== 19 || !reasoningInfo.hasHighPriFlag) {
      throw new Error('Reasoning structure or Visual Reasoning flag failed');
    }

    // 9. Test Tab: DSA Roadmap (8 Weeks + Extensions, 65+ problems, Sunday assignments)
    console.log('--- Test 9: Tab - DSA Roadmap ---');
    await evaluate(`window.jobPrepController.setTab('dsa')`);
    await new Promise(r => setTimeout(r, 400));
    const dsaInfo = await evaluate(`(() => {
      const weeks = document.querySelectorAll('.jp-week-card');
      const problems = document.querySelectorAll('tr[id^="prob-"]');
      const sundayBoxes = document.querySelectorAll('.jp-sunday-assignment-box');
      return {
        weekCount: weeks.length,
        problemCount: problems.length,
        sundayAssignmentCount: sundayBoxes.length
      };
    })()`);
    console.log('DSA Roadmap info:', dsaInfo);
    if (dsaInfo.weekCount < 10 || dsaInfo.problemCount < 60) {
      throw new Error(`Expected at least 10 week blocks (covering 11 weeks) and 60+ problems, found ${dsaInfo.weekCount} wks and ${dsaInfo.problemCount} problems`);
    }

    // Mark 1 problem solved
    await evaluate(`window.jobPrepController.updateDsaStatus('dsa_w2_p16', 'solved')`);
    await evaluate(`window.jobPrepController.updateDsaMinutes('dsa_w2_p16', '25')`);
    await new Promise(r => setTimeout(r, 200));

    const scDsa = path.join(ARTIFACTS_DIR, 'sc_jobprep_dsa.png');
    await captureScreenshot(scDsa);

    // 10. Test Tab: Technical Interview (6 subjects, custom subtopics, confidence stars)
    console.log('--- Test 10: Tab - Technical Interview ---');
    await evaluate(`window.jobPrepController.setTab('technical')`);
    await new Promise(r => setTimeout(r, 400));
    const techInfo = await evaluate(`(() => {
      const cards = document.querySelectorAll('.jp-tech-card');
      return {
        subjectCount: cards.length
      };
    })()`);
    console.log('Technical subjects info:', techInfo);
    if (techInfo.subjectCount !== 6) {
      throw new Error(`Expected 6 technical subjects, got ${techInfo.subjectCount}`);
    }

    // Add a custom subtopic to OOPS
    await evaluate(`(() => {
      const input = document.getElementById('inputCustomSub_tech_oops');
      if (input) {
        input.value = 'Explain vptr offset calculation in multi-inheritance';
        window.jobPrepController.addCustomTechSubtopic('tech_oops');
      }
    })()`);
    await evaluate(`window.jobPrepController.setTechConfidence('tech_oops', 4)`);
    await new Promise(r => setTimeout(r, 300));

    const oopsSubCount = await evaluate(`document.querySelectorAll('#tech-tech_oops .jp-checkbox-row').length`);
    console.log('OOPS subtopics count after custom add:', oopsSubCount);

    const scTech = path.join(ARTIFACTS_DIR, 'sc_jobprep_tech.png');
    await captureScreenshot(scTech);

    // 11. Test Tab: Daily 5-Hour Study Log
    console.log('--- Test 11: Tab - Daily 5-Hour Study Log ---');
    await evaluate(`window.jobPrepController.setTab('daily')`);
    await new Promise(r => setTimeout(r, 400));
    const dailyInfo = await evaluate(`(() => {
      const pillars = document.querySelectorAll('.jp-pillar-card');
      return {
        pillarCount: pillars.length
      };
    })()`);
    console.log('Daily study info:', dailyInfo);
    if (dailyInfo.pillarCount !== 3) {
      throw new Error(`Expected 3 study pillars (Aptitude, DSA, Core), got ${dailyInfo.pillarCount}`);
    }

    // Log study hours for today
    const todayStr = await evaluate(`getTodayDateString()`);
    await evaluate(`(() => {
      const date = getTodayDateString();
      window.jobPrepController.updateDailyLog(date, 'aptitudeHours', '2.0');
      window.jobPrepController.updateDailyLog(date, 'aptitudeDone', true);
      window.jobPrepController.updateDailyLog(date, 'aptitudeTopics', 'Time & Work 20 questions');
      window.jobPrepController.updateDailyLog(date, 'dsaHours', '2.0');
      window.jobPrepController.updateDailyLog(date, 'dsaDone', true);
      window.jobPrepController.updateDailyLog(date, 'dsaTopics', 'Kadane algorithm and Sort Colors');
      window.jobPrepController.updateDailyLog(date, 'coreHours', '1.0');
      window.jobPrepController.updateDailyLog(date, 'coreDone', true);
      window.jobPrepController.updateDailyLog(date, 'coreTopics', 'OOPS virtual functions and vtable');
    })()`);
    await new Promise(r => setTimeout(r, 400));

    const totalLogged = await evaluate(`(() => {
      const metrics = calculateJobPrepMetrics();
      return metrics.todayHours;
    })()`);
    console.log('Total hours logged for today:', totalLogged);
    if (totalLogged !== 5.0) {
      throw new Error(`Expected 5.0 hours logged, got ${totalLogged}`);
    }

    const scDaily = path.join(ARTIFACTS_DIR, 'sc_jobprep_daily_study.png');
    await captureScreenshot(scDaily);

    // 12. Test Search & Filter Toolbar
    console.log('--- Test 12: Search & Filter Toolbar ---');
    await evaluate(`window.jobPrepController.setTab('quants')`);
    await new Promise(r => setTimeout(r, 200));
    await evaluate(`window.jobPrepController.setSearch('Time')`);
    await new Promise(r => setTimeout(r, 300));
    const searchFilteredCount = await evaluate(`document.querySelectorAll('.jp-topic-card').length`);
    console.log('Topics matching "Time":', searchFilteredCount);
    if (searchFilteredCount === 0) throw new Error('Search filtering yielded 0 results for "Time"');
    await evaluate(`window.jobPrepController.setSearch('')`);

    // 13. Test Notes Modal
    console.log('--- Test 13: Notes Modal ---');
    await evaluate(`window.jobPrepController.openNotesModal('dsa', 'dsa_w2_p16', 'Maximum Subarray Sum')`);
    await new Promise(r => setTimeout(r, 300));
    const modalVisible = await evaluate(`document.getElementById('jpNotesModal').style.display !== 'none'`);
    if (!modalVisible) throw new Error('Notes modal did not open');

    await evaluate(`(() => {
      document.getElementById('jpNotesTextarea').value = '### Kadane Algorithm Notes\\n- Keep running sum\\n- If sum < 0, reset sum to 0\\n- Time: O(N), Space: O(1)';
      window.jobPrepController.saveNotesModal();
    })()`);
    await new Promise(r => setTimeout(r, 300));

    const savedNote = await evaluate(`window.jobPrepState.dsa['dsa_w2_p16'].notes`);
    console.log('Saved note preview:', savedNote.split('\\n')[0]);
    if (!savedNote.includes('Kadane')) throw new Error('Note was not saved into jobPrepState');

    // 14. Test Persistence Across Page Reload
    console.log('--- Test 14: Persistence Across Page Reload ---');
    await sendCommand('Page.reload');
    await new Promise(r => setTimeout(r, 2000));

    const reloadedState = await evaluate(`(() => {
      const raw = localStorage.getItem('job_prep_tracker_v1');
      const parsed = JSON.parse(raw || '{}');
      return {
        dsaKadaneStatus: parsed.dsa?.['dsa_w2_p16']?.status,
        dsaKadaneNote: parsed.dsa?.['dsa_w2_p16']?.notes,
        todayAptiDone: parsed.dailyLogs?.[getTodayDateString()]?.aptitudeDone,
        todayTotalH: parsed.dailyLogs?.[getTodayDateString()] ? (parseFloat(parsed.dailyLogs[getTodayDateString()].aptitudeHours) + parseFloat(parsed.dailyLogs[getTodayDateString()].dsaHours) + parseFloat(parsed.dailyLogs[getTodayDateString()].coreHours)) : 0
      };
    })()`);
    console.log('Reloaded state:', reloadedState);
    if (reloadedState.dsaKadaneStatus !== 'solved' || reloadedState.todayTotalH !== 5) {
      throw new Error('State failed to persist across page reload');
    }

    // 15. Test Backup & Restore Integration (Data & Storage Center)
    console.log('--- Test 15: Backup & Restore Integration ---');
    const backupBundleTest = await evaluate(`(() => {
      const bundle = buildComprehensiveBackupBundle();
      return {
        hasJobPrepInCategories: bundle.manifest.categories.includes('jobPrepTracker'),
        hasJobPrepCategoryData: !!bundle.categories.jobPrepTracker,
        hasJobPrepTopLevel: !!bundle.jobPrepState,
        todayHoursInBackup: bundle.categories.jobPrepTracker?.dailyLogs?.[getTodayDateString()]?.aptitudeHours
      };
    })()`);
    console.log('Backup bundle test:', backupBundleTest);
    if (!backupBundleTest.hasJobPrepInCategories || !backupBundleTest.hasJobPrepCategoryData || !backupBundleTest.hasJobPrepTopLevel) {
      throw new Error('Job prep tracker missing from comprehensive backup bundle');
    }

    const restoreChecklistTest = await evaluate(`(() => {
      const bundle = buildComprehensiveBackupBundle();
      renderRestoreCategoryChecklist(bundle);
      const cb = document.getElementById('scRestore_cat_jobprep');
      return {
        checkboxExists: !!cb,
        isChecked: cb ? cb.checked : false
      };
    })()`);
    console.log('Restore checklist test:', restoreChecklistTest);
    if (!restoreChecklistTest.checkboxExists || !restoreChecklistTest.isChecked) {
      throw new Error('Restore checklist does not contain checked cat_jobprep checkbox');
    }

    // 16. Mobile Viewport & Screenshot
    console.log('--- Test 16: Mobile Viewport Rendering ---');
    await sendCommand('Emulation.setDeviceMetricsOverride', {
      width: 375,
      height: 812,
      deviceScaleFactor: 2,
      mobile: true
    });
    await evaluate(`switchView('jobprep')`);
    await new Promise(r => setTimeout(r, 600));

    const scMobile = path.join(ARTIFACTS_DIR, 'sc_jobprep_mobile.png');
    await captureScreenshot(scMobile);

    // Check for JS exceptions
    if (jsErrors.length > 0) {
      console.error('FAIL: JS exceptions occurred during verification:', jsErrors);
      throw new Error('JS exceptions detected');
    }

    console.log('\n======================================================');
    console.log('✅ ALL 16 VERIFICATION TESTS PASSED SUCCESSFULLY!');
    console.log('======================================================\n');
  } catch (err) {
    console.error('TEST FAILED:', err);
    process.exit(1);
  } finally {
    ws.close();
    chromeProc.kill();
    server.close();
  }
}
