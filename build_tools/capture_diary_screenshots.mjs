import http from 'http';
import fs from 'fs';

const CDP_PORT = 9222;

async function getCDPPage() {
  return new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${CDP_PORT}/json`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const targets = JSON.parse(data);
        const page = targets.find(t => t.type === 'page');
        resolve(page);
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
    const res = await this.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    return res.result ? res.result.value : undefined;
  }

  async screenshot(outPath) {
    const res = await this.send('Page.captureScreenshot', { format: 'png', quality: 95 });
    fs.writeFileSync(outPath, Buffer.from(res.data, 'base64'));
    console.log(`Saved screenshot to ${outPath}`);
  }
}

async function capture() {
  const page = await getCDPPage();
  const client = new CDPClient(page.webSocketDebuggerUrl);
  await client.connect();
  await client.send('Page.enable');
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 960,
    deviceScaleFactor: 2,
    mobile: false
  });

  const fileUrl = 'file:///Users/devrajput/.gemini/antigravity-ide/scratch/test_diary_assembled.html';
  await client.send('Page.navigate', { url: fileUrl });
  await new Promise(r => setTimeout(r, 1200));

  // Populate some rich entries to showcase the UI in all its glory
  await client.evaluate(`
    switchView('diary');
    currentDiaryDate = getTodayKey();
    const entry = getDiaryEntry(currentDiaryDate);
    entry.mood = 'great';
    entry.focusRating = 5;
    entry.energyRating = 4;
    entry.accomplishments = '1. Solved 3 Sliding Window questions (Maximum Subarray, Minimum Window Substring, Longest Substring Without Repeating Characters).\\n2. Formulated strict mental rule for dynamic contraction: shrink window when condition invalidates, expand when seeking solution.\\n3. Reviewed Two Pointer vs Fast & Slow pointer tradeoffs.';
    entry.mistakes = '1. Initially forgot to restore frequency map counts when contracting left pointer in sliding window.\\n2. Missed edge case where target string is longer than source string. Now handling edge length early.\\n3. Complexity was O(N*K) due to slice check, optimized with hash table to strict O(N).';
    entry.distractions = 'Checked phone notifications once around 3 PM. Relocated device to study shelf for evening mock practice.';
    entry.freeform = 'Feeling significantly sharper on pattern identification. The Two Pointer and Sliding Window templates feel intuitive now.\\nReady to dive into Monotonic Stacks and Binary Search answer-space problems tomorrow.';
    entry.priorities = [
      'Solve 4 Monotonic Stack problems (Next Greater Element, Daily Temperatures, Largest Rectangle in Histogram)',
      'Revise Pattern 1: Two Pointers spaced repetition review queue',
      'Read 2 chapters on Database Indexing (B-Trees vs LSM Trees) for technical interview preparation'
    ];
    entry.priorityDone = [true, false, false];
    saveDiaryFromInputs();
    renderDiaryView();
  `);
  await new Promise(r => setTimeout(r, 600));

  // Screenshot 1: Desktop View
  await client.screenshot('/Users/devrajput/.gemini/antigravity-ide/brain/66b7e02f-986f-4cfd-b90f-8aa4c87db087/diary_redesigned_desktop.png');

  console.log('Diary screenshots captured successfully!');
  process.exit(0);
}

capture().catch(err => {
  console.error(err);
  process.exit(1);
});
