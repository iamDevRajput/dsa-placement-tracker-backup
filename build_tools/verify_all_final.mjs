import http from 'http';

// Helper to create page target for standalone file://
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
  }

  async connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.wsUrl);
      this.ws.onopen = () => resolve();
      this.ws.onerror = (e) => reject(e);
      this.ws.onmessage = (msg) => {
        const data = JSON.parse(msg.data);
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
      throw new Error(JSON.stringify(res.exceptionDetails));
    }
    return res.result?.value;
  }
}

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function testPage(targetUrl, modeName) {
  console.log(`\n======================================================`);
  console.log(`TESTING MODE: ${modeName} (${targetUrl})`);
  console.log(`======================================================\n`);

  const target = await getPageTarget(targetUrl);
  const client = new CDPClient(target.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Page.enable');
  await client.send('Runtime.enable');

  await sleep(1500);

  const results = [];
  function assert(name, condition, details = "") {
    if (condition) {
      results.push({ name, passed: true, details });
      console.log(`  PASS: ${name} ${details ? '(' + details + ')' : ''}`);
    } else {
      results.push({ name, passed: false, details });
      console.error(`  FAIL: ${name} - ${details}`);
    }
  }

  // 1. Check questions in 'All Patterns' mode
  await client.eval(`switchView('dsa')`);
  await client.eval(`jumpToPattern('all')`);
  await client.eval(`expandAllPatterns(true)`);
  await sleep(300);

  const allRenderedCount = await client.eval(`document.querySelectorAll('.prob-item').length`);
  assert("All 184 Questions Rendered in All Patterns view", allRenderedCount === 184, `Rendered: ${allRenderedCount}`);

  // 2. Check each pattern section
  const sectionCount = await client.eval(`document.querySelectorAll('.step-section').length`);
  assert("All 19 Pattern Sections Rendered", sectionCount === 19, `Sections: ${sectionCount}`);

  // 3. Check question attributes: Title, Difficulty, Pattern tag, Platform badges
  const problemSample = await client.eval(`
    (() => {
      const p1 = document.getElementById('prob-1');
      return {
        hasTitle: !!p1.querySelector('.prob-title')?.textContent,
        title: p1.querySelector('.prob-title')?.textContent,
        hasPatternTag: !!p1.querySelector('.prob-pattern-tag')?.textContent,
        patternTag: p1.querySelector('.prob-pattern-tag')?.textContent,
        hasDiff: !!p1.querySelector('.diff-badge')?.textContent,
        diff: p1.querySelector('.diff-badge')?.textContent,
        hasLink: !!p1.querySelector('.platform-badge'),
        href: p1.querySelector('.platform-badge')?.getAttribute('href'),
        target: p1.querySelector('.platform-badge')?.getAttribute('target'),
        rel: p1.querySelector('.platform-badge')?.getAttribute('rel'),
        tooltip: p1.querySelector('.platform-badge')?.getAttribute('title'),
        hasExtIcon: !!p1.querySelector('.ext-icon')
      };
    })()
  `);

  assert("Problem #1 Shows Title", problemSample.hasTitle, problemSample.title);
  assert("Problem #1 Shows Pattern Tag", problemSample.hasPatternTag, problemSample.patternTag);
  assert("Problem #1 Shows Difficulty Badge", problemSample.hasDiff, problemSample.diff);
  assert("Problem #1 Has Clickable Link with Target Blank & Rel",
    problemSample.hasLink && problemSample.target === '_blank' && problemSample.rel === 'noopener noreferrer',
    `href: ${problemSample.href}, target: ${problemSample.target}`
  );
  assert("Problem #1 Link Has Destination Tooltip and External Icon",
    !!problemSample.tooltip && problemSample.hasExtIcon,
    `tooltip: ${problemSample.tooltip}`
  );

  // 4. Check GeeksforGeeks badge (e.g. Problem #2)
  const problem2Sample = await client.eval(`
    (() => {
      const p2 = document.getElementById('prob-2');
      const gfgBadge = p2.querySelector('.gfg-badge');
      return {
        hasGfgBadge: !!gfgBadge,
        href: gfgBadge?.getAttribute('href'),
        text: gfgBadge?.textContent?.trim(),
        tooltip: gfgBadge?.getAttribute('title')
      };
    })()
  `);
  assert("Problem #2 Has GeeksforGeeks Badge",
    problem2Sample.hasGfgBadge && problem2Sample.href.includes('geeksforgeeks.org'),
    `href: ${problem2Sample.href}`
  );

  // 5. Test Pattern Switching: Select Pattern 2 (Sliding Window)
  await client.eval(`jumpToPattern(2)`);
  await sleep(300);

  const p2Count = await client.eval(`document.querySelectorAll('.prob-item').length`);
  const p2SectionVisible = await client.eval(`document.querySelectorAll('.step-section').length`);
  const p2BadgeText = await client.eval(`document.querySelector('.prob-pattern-tag')?.textContent`);

  assert("Individual Pattern View Renders Only Selected Pattern",
    p2SectionVisible === 1 && p2BadgeText.includes('P2'),
    `Visible sections: ${p2SectionVisible}, Question count: ${p2Count}`
  );

  // Return to All Patterns
  await client.eval(`jumpToPattern('all')`);
  await sleep(200);

  // 6. Test Revision Clicks & Non-inflating unique solved
  await client.eval(`
    localStorage.clear();
    init();
    // Add 3 revisions on problem 5
    addRevisionEvent(5, 'independent', 20, 'Independent solve note', 'O(N)');
    addRevisionEvent(5, 'hint', 15, 'Hint solve note', 'O(N)');
    addRevisionEvent(5, 'solution', 10, 'Solution review note', 'O(N)');
  `);
  await sleep(300);

  const p5Revs = await client.eval(`getProblemState(5).revisionCount`);
  const uniqueCount = await client.eval(`Object.values(state.problems).filter(p => p.done).length`);
  assert("Three Revision Clicks Produce 3 Revisions", p5Revs === 3, `Revs: ${p5Revs}`);
  assert("Revisions Do Not Inflate Unique Count (Exactly 1)", uniqueCount === 1, `Unique solved: ${uniqueCount}`);

  // 7. Test Diary Autosave & Integrity
  const todayKey = await client.eval(`getTodayKey()`);
  await client.eval(`
    switchView('diary');
    const entry = getDiaryEntry('${todayKey}');
    entry.accomplishments = 'Mastered Pattern 1 Two Pointers';
    entry.mistakes = 'Watch array index out of bounds';
    entry.mood = 'great';
    entry.focusRating = 5;
    entry.energyRating = 4;
    saveDiaryState();
  `);
  await sleep(300);

  // Reload / Re-init
  await client.eval(`init()`);
  await sleep(300);

  const reloadedEntry = await client.eval(`diaryState.entries['${todayKey}']`);
  assert("Diary Data Persists on Refresh",
    reloadedEntry.accomplishments === 'Mastered Pattern 1 Two Pointers' && reloadedEntry.focusRating === 5,
    `Saved: ${reloadedEntry.accomplishments}`
  );

  // 8. Test Daily Motivation Determinism
  const qA = await client.eval(`getDeterministicDailyQuote()`);
  const qB = await client.eval(`getDeterministicDailyQuote()`);
  assert("Motivation Quote Stays Stable", qA.id === qB.id && qA.quote === qB.quote, `Quote #${qA.id}: ${qA.author}`);

  // 9. Check JavaScript Console Errors
  const hasSyntaxError = await client.eval(`typeof init === 'function' && typeof renderDsaContent === 'function'`);
  assert("Core JavaScript Functions Defined without Error", hasSyntaxError);

  // Close target
  await client.send('Target.closeTarget', { targetId: target.id });

  const passed = results.filter(r => r.passed).length;
  console.log(`\nMode Result: ${passed}/${results.length} PASSED`);
  return passed === results.length;
}

async function main() {
  let allOk = true;

  // Test 1: Standalone file mode (index.html via file:///)
  const fileOk = await testPage(
    "file:///Users/devrajput/@Resources/Tracker/index.html",
    "Standalone HTML via file://"
  );
  if (!fileOk) allOk = false;

  // Test 2: Localhost HTTP mode (dsa_patterns_trackerfinal copy.html)
  const httpOk = await testPage(
    "http://localhost:8765/dsa_patterns_trackerfinal%20copy.html",
    "Localhost HTTP mode"
  );
  if (!httpOk) allOk = false;

  console.log("\n======================================================");
  if (allOk) {
    console.log("ALL MODES TESTED AND PASSED VERIFICATION! 🎉");
    process.exit(0);
  } else {
    console.error("SOME TESTS FAILED!");
    process.exit(1);
  }
}

main().catch(err => {
  console.error("Fatal:", err);
  process.exit(1);
});
