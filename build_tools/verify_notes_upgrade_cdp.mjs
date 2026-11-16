import http from 'http';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';

const PORT = 8095;
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
  const cdpPort = 9228;
  const profileDir = '/tmp/chrome_test_profile_' + Date.now();
  const chromeProc = spawn(chromePath, [
    `--remote-debugging-port=${cdpPort}`,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    `--user-data-dir=${profileDir}`,
    `http://localhost:${PORT}/index.html`
  ]);

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

    const jsErrors = [];
    ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.method === 'Runtime.exceptionThrown') {
        const err = msg.params.exceptionDetails.text + ' ' + (msg.params.exceptionDetails.exception?.description || '');
        jsErrors.push(err);
      }
    });

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

    console.log('--- TEST 1: Open Revision Modal for Problem #1 & Verify Permanent Problem Notes Card ---');
    await evalJs(`openRevisionModal(1, 'dsa')`);
    await new Promise(r => setTimeout(r, 400));

    const revNotesCardCheck = await evalJs(`
      (() => {
        const editTab = document.getElementById('btnRevTabEdit');
        const prevTab = document.getElementById('btnRevTabPreview');
        const readerBtn = document.getElementById('btnViewProbNotes');
        const textarea = document.getElementById('probNoteContent');
        return {
          hasEditTab: !!editTab,
          hasPrevTab: !!prevTab,
          hasReaderBtn: !!readerBtn,
          hasTextarea: !!textarea,
          readerBtnText: readerBtn?.textContent?.trim()
        };
      })()
    `);
    console.log('Revision Notes Card:', revNotesCardCheck);
    if (!revNotesCardCheck.hasEditTab || !revNotesCardCheck.hasPrevTab || !revNotesCardCheck.hasReaderBtn) {
      throw new Error(`Revision notes card upgrade check failed: ${JSON.stringify(revNotesCardCheck)}`);
    }

    console.log('--- TEST 2: Paste ChatGPT Technical Notes with Headings, Lists, Tables, Callouts, and C++ Code ---');
    const chatGptNotes = `### Approach 1: Brute Force — O(N²)

**Idea:**
Generate all possible subarrays and maintain a running sum.

**Algorithm:**
1. Initialize \`count = 0\`.
2. Select the starting index \`i\` from 0 to \`n-1\`.
3. Traverse the remaining elements \`j\` from \`i\` to \`n-1\`:
   - Add \`nums[j]\` to running sum.
   - If \`sum == k\`, increment \`count\`.
4. Return \`count\`.

> [!NOTE]
> This approach takes $O(N^2)$ time and $O(1)$ space. We can optimize this using a Hash Map to achieve linear $O(N)$ time complexity.

### Approach 2: Prefix Sum + Hash Map — O(N) Optimal

**Key Invariant:**
If \`prefSum[j] - prefSum[i] = k\`, then \`prefSum[i] = prefSum[j] - k\`. We maintain a frequency map of seen prefix sums.

| Approach | Time Complexity | Space Complexity | Status |
| :--- | :---: | :---: | :--- |
| Brute Force | $O(N^2)$ | $O(1)$ | Time Limit Exceeded |
| Prefix Sum Map | $O(N)$ | $O(N)$ | Accepted (Optimal) |

**C++ Code:**
\`\`\`cpp
#include <vector>
#include <unordered_map>
using namespace std;

class Solution {
public:
    int subarraySum(vector<int>& nums, int k) {
        unordered_map<int, int> prefixCounts;
        prefixCounts[0] = 1; // Base case: prefix sum of 0 occurs once
        
        int currentSum = 0;
        int count = 0;
        
        for (int num : nums) {
            currentSum += num;
            int target = currentSum - k;
            
            // Check if (currentSum - k) was observed before
            if (prefixCounts.find(target) != prefixCounts.end()) {
                count += prefixCounts[target];
            }
            prefixCounts[currentSum]++;
        }
        
        return count;
    }
};
\`\`\`
`;

    // Set notes in textarea and save explicitly
    await evalJs(`
      (() => {
        const ta = document.getElementById('probNoteContent');
        ta.value = ${JSON.stringify(chatGptNotes)};
        saveProblemNotesExplicitly();
      })();
    `);
    await new Promise(r => setTimeout(r, 400));

    console.log('--- TEST 3: Inline Preview in Revision Modal ---');
    await evalJs(`switchRevNotesTab('preview')`);
    await new Promise(r => setTimeout(r, 200));

    const inlinePreviewCheck = await evalJs(`
      (() => {
        const group = document.getElementById('revNotesPreviewGroup');
        const content = document.getElementById('revNotesPreviewContent');
        return {
          visible: group && group.style.display !== 'none',
          hasH3: !!content.querySelector('.pnote-h3'),
          hasCodeWrapper: !!content.querySelector('.pnote-code-wrapper'),
          hasTable: !!content.querySelector('.pnote-table'),
          hasCallout: !!content.querySelector('.pnote-callout')
        };
      })()
    `);
    console.log('Inline Preview Check:', inlinePreviewCheck);
    if (!inlinePreviewCheck.visible || !inlinePreviewCheck.hasH3 || !inlinePreviewCheck.hasCodeWrapper) {
      throw new Error(`Inline preview check failed: ${JSON.stringify(inlinePreviewCheck)}`);
    }

    console.log('--- TEST 4: Open Upgraded Permanent Problem Notes Viewer (modalViewProblemNotes) ---');
    await evalJs(`openViewProblemNotesModal()`);
    await new Promise(r => setTimeout(r, 400));

    const modalReaderCheck = await evalJs(`
      (() => {
        const modal = document.getElementById('modalViewProblemNotes');
        const title = document.getElementById('viewNotesProbTitle')?.textContent;
        const trackerPill = document.getElementById('viewNotesTrackerBadge')?.textContent;
        const article = document.getElementById('viewNotesContentDisplay');
        const codeWrapper = article.querySelector('.pnote-code-wrapper');
        const langBadge = codeWrapper?.querySelector('.pnote-lang-badge')?.textContent;
        const copyBtn = codeWrapper?.querySelector('.pnote-copy-code-btn');
        const lineCount = codeWrapper?.querySelector('.pnote-line-count')?.textContent;
        const table = article.querySelector('.pnote-table');
        const callout = article.querySelector('.pnote-callout');
        const mathInline = article.querySelector('.pnote-math-inline');
        const nestedList = article.querySelector('.pnote-sublist');

        return {
          modalActive: modal?.classList.contains('active'),
          title: title,
          trackerPill: trackerPill,
          hasH3: article.querySelectorAll('.pnote-h3').length,
          hasCodeWrapper: !!codeWrapper,
          langBadge: langBadge,
          hasCopyBtn: !!copyBtn,
          lineCount: lineCount,
          hasTable: !!table,
          tableRows: table?.querySelectorAll('tr')?.length || 0,
          hasCallout: !!callout,
          hasMath: !!mathInline,
          hasNestedList: !!nestedList,
          hasGutter: !!codeWrapper?.querySelector('.pnote-code-gutter')
        };
      })()
    `);
    console.log('Modal Reader Check:', modalReaderCheck);
    if (!modalReaderCheck.modalActive || !modalReaderCheck.hasCodeWrapper || !modalReaderCheck.hasTable || !modalReaderCheck.hasCallout) {
      throw new Error(`Modal reader check failed: ${JSON.stringify(modalReaderCheck)}`);
    }

    console.log('--- TEST 5: Verify C++ Syntax Highlighting & Copy Code Functionality ---');
    const syntaxTokensCheck = await evalJs(`
      (() => {
        const code = document.querySelector('#viewNotesContentDisplay .pnote-code-inner');
        return {
          hasKeywords: code.querySelectorAll('.tok-kw').length > 0,
          hasTypes: code.querySelectorAll('.tok-type').length > 0,
          hasComments: code.querySelectorAll('.tok-comment').length > 0,
          hasMacros: code.querySelectorAll('.tok-macro').length > 0,
          hasNumbers: code.querySelectorAll('.tok-num').length > 0
        };
      })()
    `);
    console.log('Syntax Tokens Check:', syntaxTokensCheck);
    if (!syntaxTokensCheck.hasKeywords || !syntaxTokensCheck.hasTypes || !syntaxTokensCheck.hasComments || !syntaxTokensCheck.hasMacros) {
      throw new Error(`C++ syntax tokenization check failed: ${JSON.stringify(syntaxTokensCheck)}`);
    }

    console.log('--- TEST 6: Switch to Edit Mode & Verify Live Markdown Preview ---');
    await evalJs(`setPnoteMode('edit')`);
    await new Promise(r => setTimeout(r, 300));

    const editModeCheck = await evalJs(`
      (() => {
        const editView = document.getElementById('pnoteEditingView');
        const readView = document.getElementById('pnoteReadingView');
        const textarea = document.getElementById('pnoteEditTextarea');
        const livePreview = document.getElementById('pnoteLivePreviewContent');
        return {
          editVisible: editView && editView.style.display !== 'none',
          readHidden: readView && readView.style.display === 'none',
          textareaValueLen: textarea?.value?.length,
          previewHasCode: !!livePreview?.querySelector('.pnote-code-wrapper')
        };
      })()
    `);
    console.log('Edit Mode Check:', editModeCheck);
    if (!editModeCheck.editVisible || !editModeCheck.readHidden || !editModeCheck.previewHasCode) {
      throw new Error(`Edit mode switch failed: ${JSON.stringify(editModeCheck)}`);
    }

    // Type addition in textarea and verify live preview update
    await evalJs(`
      (() => {
        const ta = document.getElementById('pnoteEditTextarea');
        ta.value += '\\n\\n#### Live Edit Test Heading\\nLive edited paragraph successfully rendered.';
        handlePnoteEditorInput(ta.value);
      })();
    `);
    await new Promise(r => setTimeout(r, 200));

    const liveUpdateCheck = await evalJs(`
      (() => {
        const livePreview = document.getElementById('pnoteLivePreviewContent');
        const isDirty = isPnoteDirty;
        const dirtyBadge = document.getElementById('pnoteDirtyIndicator');
        return {
          isDirty: isDirty,
          dirtyBadgeVisible: dirtyBadge && dirtyBadge.style.display !== 'none',
          hasNewHeading: livePreview?.innerHTML.includes('Live Edit Test Heading')
        };
      })()
    `);
    console.log('Live Update & Dirty State Check:', liveUpdateCheck);
    if (!liveUpdateCheck.isDirty || !liveUpdateCheck.hasNewHeading) {
      throw new Error(`Live update check failed: ${JSON.stringify(liveUpdateCheck)}`);
    }

    console.log('--- TEST 7: Save Notes in Modal & Switch Back to Reading Mode ---');
    await evalJs(`savePnoteExplicitlyFromModal()`);
    await new Promise(r => setTimeout(r, 300));

    const savedCheck = await evalJs(`
      (() => {
        const isDirty = isPnoteDirty;
        const currentMode = pnoteCurrentMode;
        const display = document.getElementById('viewNotesContentDisplay');
        return {
          isDirty: isDirty,
          currentMode: currentMode,
          hasNewHeadingInReading: display?.innerHTML.includes('Live Edit Test Heading')
        };
      })()
    `);
    console.log('Saved State Check:', savedCheck);
    if (savedCheck.isDirty || savedCheck.currentMode !== 'read' || !savedCheck.hasNewHeadingInReading) {
      throw new Error(`Save state check failed: ${JSON.stringify(savedCheck)}`);
    }

    console.log('--- TEST 8: Fullscreen Mode Toggle ---');
    await evalJs(`togglePnoteFullscreen()`);
    await new Promise(r => setTimeout(r, 200));
    const isFullscreen = await evalJs(`document.getElementById('pnoteModalCard').classList.contains('fullscreen')`);
    console.log('Fullscreen Mode Active:', isFullscreen);
    if (!isFullscreen) throw new Error('Fullscreen toggle failed');

    // Switch back to normal
    await evalJs(`togglePnoteFullscreen()`);
    await new Promise(r => setTimeout(r, 200));

    console.log('--- TEST 9: Capture Screenshots for Artifacts ---');
    // Desktop Reading Mode Screenshot
    await sendCmd('Emulation.setDeviceMetricsOverride', {
      width: 1440,
      height: 900,
      deviceScaleFactor: 1,
      mobile: false
    });
    await new Promise(r => setTimeout(r, 500));

    const readingShot = await sendCmd('Page.captureScreenshot', { format: 'png' });
    const readingData = readingShot.result?.data || readingShot.data;
    const readingPath = path.join(ARTIFACTS_DIR, 'pnote_reading_mode_desktop.png');
    fs.writeFileSync(readingPath, Buffer.from(readingData, 'base64'));
    console.log('Reading mode screenshot saved:', readingPath);

    // Desktop Edit Mode Screenshot
    await evalJs(`setPnoteMode('edit')`);
    await new Promise(r => setTimeout(r, 500));
    const editingShot = await sendCmd('Page.captureScreenshot', { format: 'png' });
    const editingData = editingShot.result?.data || editingShot.data;
    const editingPath = path.join(ARTIFACTS_DIR, 'pnote_editing_mode_desktop.png');
    fs.writeFileSync(editingPath, Buffer.from(editingData, 'base64'));
    console.log('Editing mode screenshot saved:', editingPath);

    // Switch back to read mode for mobile screenshot
    await evalJs(`setPnoteMode('read')`);
    await new Promise(r => setTimeout(r, 300));

    // Mobile Reading Mode Screenshot
    await sendCmd('Emulation.setDeviceMetricsOverride', {
      width: 390,
      height: 844,
      deviceScaleFactor: 2,
      mobile: true
    });
    await new Promise(r => setTimeout(r, 500));
    const mobileShot = await sendCmd('Page.captureScreenshot', { format: 'png' });
    const mobileData = mobileShot.result?.data || mobileShot.data;
    const mobilePath = path.join(ARTIFACTS_DIR, 'pnote_reading_mode_mobile.png');
    fs.writeFileSync(mobilePath, Buffer.from(mobileData, 'base64'));
    console.log('Mobile reading screenshot saved:', mobilePath);

    // Check JS errors
    console.log('--- JS Errors during test session ---', jsErrors);
    if (jsErrors.length > 0) {
      throw new Error(`Encountered JS errors during test: ${JSON.stringify(jsErrors)}`);
    }

    console.log('✅ ALL PERMANENT PROBLEM NOTES TESTS PASSED SUCCESSFULLY!');

  } catch (err) {
    console.error('❌ Notes verification test failed:', err);
    exitCode = 1;
  } finally {
    chromeProc.kill('SIGKILL');
    server.close();
    process.exit(exitCode);
  }
});
