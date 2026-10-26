import http from 'http';
import fs from 'fs';
import path from 'path';

const CDP_PORT = 9222;
const ARTIFACT_DIR = '/Users/devrajput/.gemini/antigravity-ide/brain/66b7e02f-986f-4cfd-b90f-8aa4c87db087';

async function getCDPPage() {
  return new Promise((resolve, reject) => {
    http.get(`http://127.0.0.1:${CDP_PORT}/json`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        const targets = JSON.parse(data);
        const page = targets.find(t => t.type === 'page');
        if (page && page.webSocketDebuggerUrl) resolve(page);
        else reject(new Error('No active page found'));
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
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    return res.result ? res.result.value : undefined;
  }

  async captureScreenshot(outputPath) {
    const res = await this.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(outputPath, Buffer.from(res.data, 'base64'));
    console.log('Saved screenshot:', outputPath);
  }
}

async function run() {
  const page = await getCDPPage();
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

  const fileUrl = 'file://' + path.resolve('test_workspace_assembled.html');
  await client.send('Page.navigate', { url: fileUrl });
  await new Promise(r => setTimeout(r, 1500));

  // 1. Planner Tab Screenshot
  await client.evaluate(`switchView('planner')`);
  await client.evaluate(`switchWorkspaceTab('tab-planner')`);
  await new Promise(r => setTimeout(r, 600));
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'workspace_v2_planner.png'));

  // 2. Coding Log Tab Screenshot
  await client.evaluate(`switchWorkspaceTab('tab-coding')`);
  await new Promise(r => setTimeout(r, 600));
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'workspace_v2_coding_log.png'));

  // 3. Private Diary Tab Screenshot
  await client.evaluate(`switchWorkspaceTab('tab-diary')`);
  await new Promise(r => setTimeout(r, 600));
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'workspace_v2_diary.png'));

  // 4. Calendar & History Tab Screenshot
  await client.evaluate(`switchWorkspaceTab('tab-history')`);
  await new Promise(r => setTimeout(r, 600));
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'workspace_v2_calendar.png'));

  // 5. Analytics Tab Screenshot
  await client.evaluate(`switchWorkspaceTab('tab-analytics')`);
  await new Promise(r => setTimeout(r, 600));
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'workspace_v2_analytics.png'));

  // 6. Routine Settings Tab Screenshot
  await client.evaluate(`switchWorkspaceTab('tab-routines')`);
  await new Promise(r => setTimeout(r, 600));
  await client.captureScreenshot(path.join(ARTIFACT_DIR, 'workspace_v2_routines.png'));

  console.log('All 6 workspace screenshots captured successfully!');
  process.exit(0);
}

run().catch(err => {
  console.error('Screenshot capture failed:', err);
  process.exit(1);
});
