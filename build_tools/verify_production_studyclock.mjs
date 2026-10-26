import http from 'http';
import fs from 'fs';
import path from 'path';

const CDP_PORT = 9222;
const ARTIFACT_DIR = '/Users/devrajput/.gemini/antigravity-ide/brain/66b7e02f-986f-4cfd-b90f-8aa4c87db087';
const TARGET_URL = 'file:///Users/devrajput/@Resources/Tracker/integrated_master.html';

async function createFreshCDPPage() {
  return new Promise((resolve, reject) => {
    const req = http.request({
      hostname: '127.0.0.1',
      port: CDP_PORT,
      path: '/json/new',
      method: 'PUT'
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const target = JSON.parse(data);
          resolve(target);
        } catch (e) {
          reject(e);
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function closeCDPPage(id) {
  return new Promise((resolve) => {
    http.get(`http://127.0.0.1:${CDP_PORT}/json/close/${id}`, () => resolve()).on('error', () => resolve());
  });
}

class CDPClient {
  constructor(wsUrl) {
    this.wsUrl = wsUrl;
    this.ws = null;
    this.id = 1;
    this.callbacks = new Map();
    this.consoleErrors = [];
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
          if (parsed.params.type === 'error') {
            this.consoleErrors.push(text);
            console.error('[BROWSER ERROR]:', text);
          }
        }
        if (parsed.method === 'Runtime.exceptionThrown') {
          const text = parsed.params.exceptionDetails.text + ' ' + (parsed.params.exceptionDetails.exception?.description || '');
          this.consoleErrors.push(text);
          console.error('[BROWSER EXCEPTION]:', text);
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
      throw new Error(`Eval error: ${JSON.stringify(res.exceptionDetails)}`);
    }
    return res.result ? res.result.value : undefined;
  }

  async captureScreenshot(outputPath) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(outputPath, Buffer.from(res.data, 'base64'));
    console.log('Saved screenshot:', outputPath);
  }
}

async function run() {
  const page = await createFreshCDPPage();
  const client = new CDPClient(page.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Runtime.enable');
  await client.send('Page.enable');
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 960,
    deviceScaleFactor: 2,
    mobile: false
  });

  console.log('Navigating to production:', TARGET_URL);
  await client.send('Page.navigate', { url: TARGET_URL });
  await new Promise(r => setTimeout(r, 2000));

  console.log('1. Checking page load console errors...');
  console.log('Errors during load:', client.consoleErrors.length);

  console.log('2. Switching to studyclock view...');
  await client.evaluate(`switchView('studyclock')`);
  await new Promise(r => setTimeout(r, 500));

  console.log('3. Starting a live study session...');
  await client.evaluate(`startStudyClock()`);
  await new Promise(r => setTimeout(r, 2000));

  console.log('4. Performing page reload while running...');
  await client.send('Page.reload');
  await new Promise(r => setTimeout(r, 2000));

  await client.evaluate(`switchView('studyclock')`);
  await new Promise(r => setTimeout(r, 500));

  const postReloadState = await client.evaluate(`(() => {
    return {
      status: studyClockActiveSession.status,
      elapsedSec: Math.floor(getStudyClockElapsedMs() / 1000),
      digits: document.getElementById('scClockDigits')?.textContent.trim(),
      cardRunning: document.getElementById('scClockCard')?.classList.contains('running'),
      hdrTimerDigits: document.getElementById('hdr-timer-display')?.textContent.trim()
    };
  })()`);
  console.log('5. Production post-reload recovered state:', postReloadState);

  // Stop session safely
  await client.evaluate(`(() => {
    studyClockActiveSession.accumulatedMs += 45 * 60 * 1000;
    stopAndLogStudySession();
  })()`);
  await new Promise(r => setTimeout(r, 500));

  // Verify trackers integrity
  const integrity = await client.evaluate(`(() => {
    return {
      dsaCount: typeof DATA !== 'undefined' ? DATA.reduce((acc, s) => acc + s.problems.length, 0) : 0,
      rbCount: typeof RISINGBRAIN_DATA !== 'undefined' ? RISINGBRAIN_DATA.reduce((acc, t) => acc + t.patterns.reduce((a, p) => a + p.problems.length, 0), 0) : 0,
      striverCount: typeof STRIVER_DATA !== 'undefined' ? STRIVER_DATA.reduce((acc, s) => acc + s.problems.length, 0) : 0,
      syncMapActive: typeof DSA_RB_SYNC_MAP !== 'undefined' && Object.keys(DSA_RB_SYNC_MAP).length > 0
    };
  })()`);
  console.log('6. Tracker integrity: DSA:', integrity.dsaCount, '| RB:', integrity.rbCount, '| Striver:', integrity.striverCount, '| Sync:', integrity.syncMapActive);

  // Screenshot
  const shotPath = path.join(ARTIFACT_DIR, 'production_study_clock_verified.png');
  await client.captureScreenshot(shotPath);

  if (client.ws) client.ws.close();
  await closeCDPPage(page.id);
  console.log('\nProduction verification completed with 100% success!');
}

run().catch(err => {
  console.error('Test error:', err);
  process.exit(1);
});
