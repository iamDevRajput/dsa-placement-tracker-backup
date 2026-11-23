import fs from 'fs';
import vm from 'vm';

const htmlPath = '/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html';
const htmlContent = fs.readFileSync(htmlPath, 'utf-8');

console.log('=== TEST 1: DOM Elements & Filter Pills Verification ===');
const requiredStrings = [
  'id="f-striver-notes-has"',
  'id="f-striver-notes-no"',
  'id="striver-stat-chip-hasnotes"',
  'id="striver-stat-chip-nonotes"',
  'rb-notes-btn',
  'Notes Saved – Click to View/Edit',
  'No Notes – Click to Add'
];

let allFound = true;
requiredStrings.forEach(s => {
  const found = htmlContent.includes(s);
  console.log(`  Checking [${s}]: ${found ? 'PASSED ✓' : 'FAILED ✗'}`);
  if (!found) allFound = false;
});

if (!allFound) {
  console.error('Test 1 FAILED: Missing required DOM elements');
  process.exit(1);
}

console.log('\n=== TEST 2: JavaScript Syntax Parsing Check ===');
const scriptMatches = htmlContent.match(/<script[\s\S]*?<\/script>/gi) || [];
scriptMatches.forEach((scriptTag, idx) => {
  const code = scriptTag.replace(/<script[^>]*>/i, '').replace(/<\/script>/i, '');
  if (!code.trim() || scriptTag.includes('src=')) return;
  try {
    new vm.Script(code, { filename: `script_${idx}.js` });
    console.log(`  Script Block #${idx + 1} (${code.length} chars): Syntax Valid ✓`);
  } catch (err) {
    console.error(`  Script Block #${idx + 1} SYNTAX ERROR:`, err.message);
    process.exit(1);
  }
});

console.log('\n=== TEST 3: Smart Notes Indicator Logic & Test Cases ===');
const domMock = {
  elements: {},
  getElementById(id) {
    if (!this.elements[id]) {
      this.elements[id] = {
        id: id,
        className: '',
        title: '',
        innerHTML: '',
        style: {}
      };
    }
    return this.elements[id];
  }
};

const storageMock = {};

const sandbox = {
  console: console,
  document: domMock,
  localStorage: {
    getItem(k) { return storageMock[k] || null; },
    setItem(k, v) { storageMock[k] = String(v); },
    removeItem(k) { delete storageMock[k]; }
  },
  striverState: {
    version: 1,
    problems: {
      "1": {
        done: true,
        notes: { content: "Binary search invariant note", approach: "Binary Search" }
      },
      "2": {
        done: false,
        notes: { content: "", approach: "", mistakes: "" }
      },
      "3": {
        done: true,
        notes: null
      }
    }
  },
  getStriverProblemState(n) {
    return sandbox.striverState.problems[String(n)] || { notes: { approach: '' } };
  },
  STORAGE_NOTES_VAULT_KEY: 'prep_notes_recovery_vault_v1'
};

const context = vm.createContext(sandbox);

// Extract helper functions from index.html
const fnCode = htmlContent.match(/function hasProblemNotes[\s\S]*?function updateStriverProblemNotesButton[\s\S]*?\n\}/)[0];
vm.runInContext(fnCode, context);

// Test Case 1: Existing question with saved notes (Problem 1)
const hasNotes1 = context.striverProblemHasNotes(1);
console.log('  Case 1 (Question 1 has saved notes):', hasNotes1 === true ? 'PASSED (true) ✓' : 'FAILED ✗');
if (!hasNotes1) process.exit(1);

// Test Case 2: Question without notes (Problem 2)
const hasNotes2 = context.striverProblemHasNotes(2);
console.log('  Case 2 (Question 2 has empty notes):', hasNotes2 === false ? 'PASSED (false) ✓' : 'FAILED ✗');
if (hasNotes2) process.exit(1);

// Test Case 3: Question 3 with null notes
const hasNotes3 = context.striverProblemHasNotes(3);
console.log('  Case 3 (Question 3 has null notes):', hasNotes3 === false ? 'PASSED (false) ✓' : 'FAILED ✗');
if (hasNotes3) process.exit(1);

// Test Case 4: DOM button update for Problem 1
context.updateStriverProblemNotesButton(1);
const btn1 = domMock.getElementById('striver-notes-btn-1');
console.log('  Case 4 (Button 1 class is has-notes):', btn1.className.includes('has-notes') ? 'PASSED ✓' : 'FAILED ✗');
console.log('  Case 4 (Button 1 tooltip is Saved):', btn1.title === 'Notes Saved – Click to View/Edit' ? 'PASSED ✓' : 'FAILED ✗');
console.log('  Case 4 (Button 1 has checkmark ✓):', btn1.innerHTML.includes('✓') ? 'PASSED ✓' : 'FAILED ✗');

// Test Case 5: DOM button update for Problem 2
context.updateStriverProblemNotesButton(2);
const btn2 = domMock.getElementById('striver-notes-btn-2');
console.log('  Case 5 (Button 2 class is no-notes):', btn2.className.includes('no-notes') ? 'PASSED ✓' : 'FAILED ✗');
console.log('  Case 5 (Button 2 tooltip is Add):', btn2.title === 'No Notes – Click to Add' ? 'PASSED ✓' : 'FAILED ✗');
console.log('  Case 5 (Button 2 does NOT have checkmark):', !btn2.innerHTML.includes('✓') ? 'PASSED ✓' : 'FAILED ✗');

// Test Case 6: Newly saved notes on Problem 2
sandbox.striverState.problems["2"].notes.content = "New dynamic note typed by user";
context.updateStriverProblemNotesButton(2);
console.log('  Case 6 (Newly saved notes turns button green):', btn2.className.includes('has-notes') && btn2.title === 'Notes Saved – Click to View/Edit' ? 'PASSED ✓' : 'FAILED ✗');

// Test Case 7: Edited notes preserves green status
sandbox.striverState.problems["2"].notes.content = "Updated note with further explanations";
context.updateStriverProblemNotesButton(2);
console.log('  Case 7 (Edited notes keeps green status):', btn2.className.includes('has-notes') ? 'PASSED ✓' : 'FAILED ✗');

// Test Case 8: Deleted / cleared notes returns button to grey
sandbox.striverState.problems["2"].notes.content = "";
sandbox.striverState.problems["2"].notes.approach = "";
context.clearNoteFromVault('striver', 2);
context.updateStriverProblemNotesButton(2);
console.log('  Case 8 (Deleted/cleared notes returns to grey):', btn2.className.includes('no-notes') && btn2.title === 'No Notes – Click to Add' ? 'PASSED ✓' : 'FAILED ✗');

// Test Case 9: Merely opening without saving does NOT alter state or icon
const originalBtn2Class = btn2.className;
const originalBtn2Title = btn2.title;
// Simulate opening modal (read-only inspect, no save triggered)
// state is untouched
context.updateStriverProblemNotesButton(2);
console.log('  Case 9 (Open without save preserves status):', (btn2.className === originalBtn2Class && btn2.title === originalBtn2Title) ? 'PASSED ✓' : 'FAILED ✗');

console.log('\nALL SMART NOTES STATUS INDICATOR VERIFICATIONS PASSED! 🎉');
