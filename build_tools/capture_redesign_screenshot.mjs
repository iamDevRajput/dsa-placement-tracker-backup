import fs from 'fs';

async function getPageTarget(url) {
  const encodedUrl = encodeURIComponent(url);
  const res = await fetch(`http://localhost:9222/json/new?${encodedUrl}`, { method: 'PUT' });
  return await res.json();
}

async function closeTarget(targetId) {
  try {
    await fetch(`http://localhost:9222/json/close/${targetId}`, { method: 'PUT' });
  } catch(e) {}
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
      this.ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        if (msg.id && this.callbacks.has(msg.id)) {
          const { resolve, reject } = this.callbacks.get(msg.id);
          this.callbacks.delete(msg.id);
          if (msg.error) reject(msg.error);
          else resolve(msg.result);
        }
      };
    });
  }

  async send(method, params = {}) {
    const id = this.id++;
    return new Promise((resolve, reject) => {
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression) {
    const res = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true
    });
    return res.result?.value;
  }

  close() {
    if (this.ws) this.ws.close();
  }
}

async function capture() {
  const targetUrl = 'file:///Users/devrajput/.gemini/antigravity-ide/scratch/test_redesign_assembled.html';
  const target = await getPageTarget(targetUrl);
  const client = new CDPClient(target.webSocketDebuggerUrl);
  await client.connect();

  await client.send('Page.enable');
  await client.send('Runtime.enable');
  await client.send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });

  await new Promise(r => setTimeout(r, 1200));
  await client.evaluate(`switchView('risingbrain')`);
  await new Promise(r => setTimeout(r, 800));

  const screenshot = await client.send('Page.captureScreenshot', {
    format: 'webp',
    quality: 85
  });

  const outPath = '/Users/devrajput/.gemini/antigravity-ide/brain/66b7e02f-986f-4cfd-b90f-8aa4c87db087/risingbrain_redesigned_ui.webp';
  fs.writeFileSync(outPath, Buffer.from(screenshot.data, 'base64'));
  console.log('Saved screenshot to:', outPath);

  client.close();
  await closeTarget(target.id);
}

capture().catch(err => {
  console.error(err);
  process.exit(1);
});
