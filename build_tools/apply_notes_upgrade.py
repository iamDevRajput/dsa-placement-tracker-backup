import os

SOURCE_HTML = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"
CSS_FILE = "/Users/devrajput/@Resources/Tracker/build_tools/notes_upgrade.css"
JS_FILE = "/Users/devrajput/@Resources/Tracker/build_tools/notes_upgrade.js"
MODAL_FILE = "/Users/devrajput/@Resources/Tracker/build_tools/notes_upgrade_modal.html"

with open(SOURCE_HTML, "r", encoding="utf-8") as f:
    html = f.read()

with open(CSS_FILE, "r", encoding="utf-8") as f:
    notes_css = f.read()

with open(JS_FILE, "r", encoding="utf-8") as f:
    notes_js = f.read()

with open(MODAL_FILE, "r", encoding="utf-8") as f:
    upgraded_modal_html = f.read()

print(f"Original index.html size: {len(html)} bytes")

# 1. CSS INJECTION
css_target = """/* ==========================================================================
   PLACEMENT RESOURCES LIBRARY — CURATED PLACEMENT PREPARATION
   ========================================================================== */"""

if ".pnote-modal-card" not in html:
    assert css_target in html, "CSS target not found"
    html = html.replace(css_target, notes_css + "\n\n" + css_target, 1)
    print("✓ Injected Notes CSS styling")

# 2. MODAL REVISION INLINE NOTES UPGRADE
rev_notes_target = """    <!-- PERMANENT PROBLEM NOTES -->
    <div class="prob-notes-container" style="background:var(--surface2); border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:1.25rem; margin-bottom:1.5rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
        <div style="display:flex; align-items:center; gap:0.5rem;">
          <span style="font-size:1.05rem;">📓</span>
          <span style="font-weight:700; font-size:14px; color:#f8fafc;">Permanent Problem Notes</span>
          <span class="diary-save-badge" id="probNotesSavedIndicator" style="display:none; padding:2px 8px; font-size:11px;">Saved ✓</span>
        </div>
        <div style="display:flex; gap:0.45rem; align-items:center;">
          <button type="button" class="btn btn-secondary btn-sm" id="btnEditProbNotes" onclick="focusProblemNotesTextarea()" title="Focus & edit notes">
            ✏️ Edit Notes
          </button>
          <button type="button" class="btn btn-primary btn-sm" id="btnSaveProbNotes" onclick="saveProblemNotesExplicitly()" style="background:var(--rb-emerald,#10b981); border-color:var(--rb-emerald,#10b981);" title="Save notes to storage">
            💾 Save Notes
          </button>
          <button type="button" class="btn btn-secondary btn-sm" id="btnViewProbNotes" onclick="openViewProblemNotesModal()" title="View full notes in spacious modal">
            👁️ View Notes
          </button>
        </div>
      </div>

      <div class="form-group" style="margin-bottom:0;">
        <textarea class="form-textarea" id="probNoteContent"
          placeholder="Paste or write complete notes here (e.g. from ChatGPT, LeetCode discussions, algorithmic invariants, edge cases, Java/C++/Python solution code)..."
          style="width:100%; min-height:190px; height:200px; resize:vertical; font-family:var(--font-mono,'Space Mono',monospace); font-size:12.5px; line-height:1.55; tab-size:2; white-space:pre-wrap; word-wrap:break-word; background:var(--surface); border:1px solid var(--border-subtle); color:#f1f2f9; padding:0.85rem;"
          oninput="saveProblemNotesDebounced()"></textarea>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.5rem; font-size:11px; color:var(--text-muted);">
        <span id="probNoteCharCount">0 characters · 0 lines</span>
        <span>Line breaks, bullets, headings & code preserved</span>
      </div>
    </div>"""

rev_notes_replacement = """    <!-- PERMANENT PROBLEM NOTES -->
    <div class="prob-notes-container" style="background:var(--surface2); border:1px solid var(--border-subtle); border-radius:var(--radius-md); padding:1.25rem; margin-bottom:1.5rem;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.75rem; flex-wrap:wrap; gap:0.5rem;">
        <div style="display:flex; align-items:center; gap:0.5rem;">
          <span style="font-size:1.05rem;">📓</span>
          <span style="font-weight:700; font-size:14px; color:#f8fafc;">Permanent Problem Notes</span>
          <span class="diary-save-badge" id="probNotesSavedIndicator" style="display:none; padding:2px 8px; font-size:11px;">Saved ✓</span>
        </div>
        <div style="display:flex; gap:0.45rem; align-items:center;">
          <div class="pnote-mini-tabs">
            <button type="button" class="btn btn-sm pnote-mini-tab active" id="btnRevTabEdit" onclick="switchRevNotesTab('edit')">
              ✏️ Edit
            </button>
            <button type="button" class="btn btn-sm pnote-mini-tab" id="btnRevTabPreview" onclick="switchRevNotesTab('preview')">
              👁️ Preview
            </button>
          </div>
          <button type="button" class="btn btn-primary btn-sm" id="btnSaveProbNotes" onclick="saveProblemNotesExplicitly()" style="background:var(--rb-emerald,#10b981); border-color:var(--rb-emerald,#10b981); font-size:11.5px;" title="Save notes to storage">
            💾 Save Notes
          </button>
          <button type="button" class="btn btn-secondary btn-sm" id="btnViewProbNotes" onclick="openViewProblemNotesModal()" style="font-size:11.5px;" title="Open spacious ChatGPT-style documentation reader">
            📖 Fullscreen Reader
          </button>
        </div>
      </div>

      <div class="form-group" id="revNotesEditGroup" style="margin-bottom:0;">
        <textarea class="form-textarea" id="probNoteContent"
          placeholder="Paste or write complete notes here (e.g. from ChatGPT, LeetCode discussions, algorithmic invariants, edge cases, Java/C++/Python solution code)..."
          style="width:100%; min-height:190px; height:200px; resize:vertical; font-family:var(--font-mono,'Space Mono',monospace); font-size:12.5px; line-height:1.55; tab-size:2; white-space:pre-wrap; word-wrap:break-word; background:var(--surface); border:1px solid var(--border-subtle); color:#f1f2f9; padding:0.85rem;"
          oninput="saveProblemNotesDebounced()"></textarea>
      </div>

      <div id="revNotesPreviewGroup" style="display:none; max-height:360px; overflow-y:auto; background:var(--surface); border:1px solid var(--border-subtle); border-radius:8px; padding:1.25rem;">
        <article class="pnote-article" id="revNotesPreviewContent"></article>
      </div>

      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.5rem; font-size:11px; color:var(--text-muted);">
        <span id="probNoteCharCount">0 characters · 0 lines</span>
        <span>Formatted Markdown &amp; C++ Syntax Highlighting preserved</span>
      </div>
    </div>"""

if "btnRevTabPreview" not in html:
    assert rev_notes_target in html, "rev_notes_target not found"
    html = html.replace(rev_notes_target, rev_notes_replacement, 1)
    print("✓ Upgraded modalRevision Permanent Problem Notes card")

# 3. UPGRADE MODALVIEWPROBLEMNOTES HTML
view_modal_target = """<!-- VIEW PROBLEM NOTES MODAL (SPACIOUS READER) -->
<div class="modal-overlay" id="modalViewProblemNotes" style="z-index: 1100;">
  <div class="modal-card" style="max-width: 840px; width: 94%; max-height: 88vh; display: flex; flex-direction: column;">
    <div class="modal-header" style="border-bottom: 1px solid var(--border-subtle); padding-bottom: 1rem; margin-bottom: 0;">
      <div>
        <div style="font-family: var(--font-mono); font-size: 11px; color: var(--rb-emerald, #10b981);" id="viewNotesProbNum">Problem #1</div>
        <h2 style="font-family: var(--font-heading); font-size: 18px; font-weight: 700; color: #f8fafc;" id="viewNotesProbTitle">Problem Title</h2>
      </div>
      <div style="display: flex; gap: 0.5rem; align-items: center;">
        <button type="button" class="btn btn-secondary btn-sm" onclick="copyProblemNotesToClipboard()" title="Copy notes to clipboard">
          📋 Copy Notes
        </button>
        <button type="button" class="btn btn-secondary btn-sm" onclick="editNotesFromViewer()" title="Switch back to edit mode">
          ✏️ Edit Notes
        </button>
        <button class="modal-close" onclick="closeModal('modalViewProblemNotes')">✕</button>
      </div>
    </div>

    <div style="flex: 1; overflow-y: auto; padding: 1.25rem 0.25rem; margin: 0.5rem 0;">
      <div id="viewNotesContentDisplay" style="background: var(--surface2, #1b1c2e); border: 1px solid var(--border-subtle, #1e2033); border-radius: 10px; padding: 1.5rem; font-family: var(--font-mono, 'Space Mono', monospace); font-size: 13px; line-height: 1.65; white-space: pre-wrap; word-break: break-word; color: #e2e8f0;">
        <!-- Notes text rendered here -->
      </div>
    </div>

    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border-subtle); padding-top: 0.85rem; font-size: 11.5px; color: var(--text-muted);">
      <span id="viewNotesFooterMeta">DSA Permanent Notes</span>
      <button type="button" class="btn btn-secondary btn-sm" onclick="closeModal('modalViewProblemNotes')">Close</button>
    </div>
  </div>
</div>"""

if 'id="pnoteModalCard"' not in html:
    assert view_modal_target in html, "view_modal_target not found"
    html = html.replace(view_modal_target, upgraded_modal_html.strip(), 1)
    print("✓ Replaced modalViewProblemNotes with upgraded reader & editor modal")

# 4. JAVASCRIPT ENGINE & LOGIC
js_target = """/* ==========================================================================
   PLACEMENT RESOURCES LIBRARY — JAVASCRIPT ENGINE & CURATED DATA
   ========================================================================== */"""

if "renderMarkdownToHtml" not in html:
    assert js_target in html, "JS target not found"
    html = html.replace(js_target, notes_js + "\n\n" + js_target, 1)
    print("✓ Injected Notes JavaScript Engine & Offline Markdown Renderer")

# 5. CORE SUBJECTS & SKILLS HUB MARKDOWN RENDERING EXTENSION
cs_target = "displayEl.textContent = text;"
cs_replacement = "displayEl.innerHTML = renderMarkdownToHtml(text);"

if cs_target in html:
    html = html.replace(cs_target, cs_replacement, 1)
    print("✓ Upgraded Core Subjects notes viewer to Markdown renderer")

sk_target = "contentEl.textContent = notesText;"
sk_replacement = "contentEl.innerHTML = renderMarkdownToHtml(notesText);"

if sk_target in html:
    html = html.replace(sk_target, sk_replacement, 1)
    print("✓ Upgraded Skills Learning Hub notes viewer to Markdown renderer")

# 6. ESCAPE KEY SHORTCUT SAFETY FOR NOTES MODAL
escape_target = """/* Keyboard shortcuts */
document.addEventListener('keydown', (e) => {
  if(e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
  }
});"""

escape_replacement = """/* Keyboard shortcuts */
document.addEventListener('keydown', (e) => {
  if(e.key === 'Escape') {
    const pnoteModal = document.getElementById('modalViewProblemNotes');
    if (pnoteModal && pnoteModal.classList.contains('active')) {
      if (typeof requestClosePnoteModal === 'function') {
        requestClosePnoteModal();
        return;
      }
    }
    document.querySelectorAll('.modal-overlay').forEach(m => m.classList.remove('active'));
  }
});"""

if "requestClosePnoteModal" not in html:
    assert escape_target in html, "Escape key target not found"
    html = html.replace(escape_target, escape_replacement, 1)
    print("✓ Updated Escape key handler with unsaved changes safety check")

# 7. WRITE UPDATED HTML
with open(SOURCE_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated index.html written successfully! New size: {len(html)} bytes")
