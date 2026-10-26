import json, os, subprocess

# 1. Read base files
with open("/Users/devrajput/@Resources/Tracker/index.html", "r", encoding="utf-8") as f:
    html = f.read()

with open("/Users/devrajput/.gemini/antigravity-ide/scratch/striver_data.js", "r", encoding="utf-8") as f:
    striver_data_js = f.read()

with open("/Users/devrajput/.gemini/antigravity-ide/scratch/striver_js_clean.js", "r", encoding="utf-8") as f:
    striver_js = f.read()

# Verify if STRIVER_DATA is already in html
if "const STRIVER_DATA =" not in html:
    idx_script = html.find("<script>") + 8
    html = html[:idx_script] + "\n/* STRIVER A2Z 455 QUESTIONS DATA */\n" + striver_data_js + "\n\n" + html[idx_script:]

# Verify CSS
striver_css = """
/* Striver Badges & Company Tags */
.platform-badge.yt-badge {
  background: rgba(255, 68, 68, 0.14);
  color: #ff5252;
  border: 1px solid rgba(255, 68, 68, 0.35);
}
.platform-badge.yt-badge:hover {
  background: rgba(255, 68, 68, 0.25);
  border-color: #ff5252;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(255, 68, 68, 0.25);
}
.platform-badge.doc-badge {
  background: rgba(56, 189, 248, 0.14);
  color: #38bdf8;
  border: 1px solid rgba(56, 189, 248, 0.35);
}
.platform-badge.doc-badge:hover {
  background: rgba(56, 189, 248, 0.25);
  border-color: #38bdf8;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(56, 189, 248, 0.25);
}
.company-tag {
  font-size: 9.5px;
  font-family: var(--font-mono);
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 4px;
  background: var(--surface3);
  color: var(--text-dim);
  border: 1px solid var(--border-subtle);
  display: inline-block;
  line-height: 1.2;
}
.company-tags-container {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  flex-wrap: wrap;
}
"""

if ".platform-badge.yt-badge" not in html:
    html = html.replace("</style>", striver_css + "\n</style>")

# Sidebar Striver Nav Button
sidebar_btn = """    <button class="nav-item" onclick="switchView('striver', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>
      <span>Striver Sheet</span>
      <span class="nav-badge accent" id="nav-striver-badge">0/455</span>
    </button>"""

if "switchView('striver'" not in html:
    dsa_btn_end = html.find("</button>", html.find("switchView('dsa'")) + 9
    html = html[:dsa_btn_end] + "\n" + sidebar_btn + html[dsa_btn_end:]

# View Section #view-striver
view_striver_html = """    <!-- VIEW 2.5: STRIVER SHEET -->
    <section class="view-section" id="view-striver">
      <div class="dsa-controls">
        <div class="search-and-actions">
          <div class="search-box">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="text" id="striverSearch" placeholder="Search 455 Striver A2Z problems by title or problem #...">
          </div>
          <select class="form-select pattern-dropdown-select" id="striverStepSelectDropdown" onchange="jumpToStriverStep(this.value)">
            <!-- Populated dynamically -->
          </select>
          <select class="form-select" id="striverCoFilter" onchange="setStriverCompany(this.value)" style="min-width:160px; font-weight:600;">
            <option value="all">🏢 All Companies</option>
            <option value="amz">🛒 Amazon</option>
            <option value="ggl">🔍 Google</option>
            <option value="msft">🪟 Microsoft</option>
            <option value="meta">👤 Meta</option>
            <option value="fk">🛍️ Flipkart</option>
            <option value="adobe">🎨 Adobe</option>
            <option value="sam">📱 Samsung</option>
            <option disabled>── Mass Recruiters ──</option>
            <option value="tcs">🔵 TCS</option>
            <option value="wipro">🟣 Wipro</option>
            <option value="infy">🟡 Infosys</option>
            <option value="cog">🟠 Cognizant</option>
            <option value="cap">🔴 Capgemini</option>
            <option value="hcl">🟢 HCL</option>
            <option value="acc">⚫ Accenture</option>
            <option value="techm">🔷 Tech Mahindra</option>
          </select>
          <button class="btn btn-secondary" onclick="expandAllStriverSteps(true)">Expand All</button>
          <button class="btn btn-secondary" onclick="expandAllStriverSteps(false)">Collapse All</button>
        </div>

        <div class="filter-pills">
          <button class="fpill active" id="f-striver-all" onclick="setStriverFilter('all', this)">All (455)</button>
          <button class="fpill" id="f-striver-pending" onclick="setStriverFilter('pending', this)">Pending</button>
          <button class="fpill" id="f-striver-done" onclick="setStriverFilter('done', this)">Done</button>
          <button class="fpill" id="f-striver-starred" onclick="setStriverFilter('starred', this)">⭐ Starred</button>
          <button class="fpill" id="f-striver-due" onclick="setStriverFilter('due', this)">⏰ Due Today</button>
          <button class="fpill" id="f-striver-overdue" onclick="setStriverFilter('overdue', this)">⚠️ Overdue</button>
          <button class="fpill" id="f-striver-never" onclick="setStriverFilter('never', this)">Never Revised</button>
          <button class="fpill" id="f-striver-mastered" onclick="setStriverFilter('mastered', this)">👑 Mastered</button>
        </div>
      </div>

      <div class="dsa-layout">
        <!-- Sidebar Jump To Step -->
        <aside class="pattern-nav-sidebar" id="striverStepNavSidebar">
          <!-- Populated dynamically -->
        </aside>

        <!-- Main Step Sections -->
        <div class="pattern-content-area" id="striverContent">
          <!-- 18 Steps & 455 problems -->
        </div>
      </div>
    </section>"""

if 'id="view-striver"' not in html:
    dsa_sec_end = html.find("</section>", html.find('id="view-dsa"')) + 10
    html = html[:dsa_sec_end] + "\n\n" + view_striver_html + html[dsa_sec_end:]

# Check where modal functions are and replace them with unified versions from striver_js
# In html, replace from `function openRevisionModal` up to `/* ==========================================================================\n   REVISION CENTER VIEW`
m_start = html.find("function openRevisionModal(")
m_end = html.find("/* ==========================================================================\n   REVISION CENTER VIEW")

# We will put all striver_js functions here!
# Note: striver_js contains Striver state management, rendering, filters, AND unified modals!
html = html[:m_start] + striver_js + "\n\n" + html[m_end:]

# Now update the hooks:
# 1. switchView
html = html.replace(
    "dsa: 'DSA Patterns Cheat Sheet',",
    "dsa: 'DSA Patterns Cheat Sheet',\n    striver: 'Striver A2Z DSA Sheet (455 Problems)',"
)
html = html.replace(
    "else if(viewName === 'dsa') renderDsaContent();",
    "else if(viewName === 'dsa') renderDsaContent();\n  else if(viewName === 'striver') renderStriverContent();"
)

# 2. init()
html = html.replace(
    "loadState();",
    "loadState();\n  loadStriverState();"
)
html = html.replace(
    "renderDsaContent();",
    "renderDsaContent();\n  renderStriverContent();"
)
html = html.replace(
    "document.getElementById('search')?.addEventListener('input', renderDsaContent);",
    "document.getElementById('search')?.addEventListener('input', renderDsaContent);\n  document.getElementById('striverSearch')?.addEventListener('input', renderStriverContent);"
)

# 3. exportCompleteBackup & executeImportConfirmed
html = html.replace(
    "dsaState: state,",
    "dsaState: state,\n    striverState: striverState,"
)
html = html.replace(
    "if(pendingImportData.dsaState) state = pendingImportData.dsaState;",
    "if(pendingImportData.dsaState) state = pendingImportData.dsaState;\n    if(pendingImportData.striverState) { striverState = pendingImportData.striverState; saveStriverState(); }"
)

# 4. updateHeaderStats to update Striver badge count
hdr_snippet = """
  const sDone = Object.values(striverState.problems).filter(p => p.done).length;
  const sBadge = document.getElementById('nav-striver-badge');
  if(sBadge) sBadge.textContent = `${sDone}/455`;
"""
html = html.replace("document.getElementById('hdr-done').textContent = d;", hdr_snippet + "\n  document.getElementById('hdr-done').textContent = d;")

# Clean up any literal '\n' that might have been accidentally introduced
# (Check if literal backslash-n appears outside strings)

with open("/Users/devrajput/.gemini/antigravity-ide/scratch/assembled_final.html", "w", encoding="utf-8") as out:
    out.write(html)

# Extract <script> and test with node -c
script_start = html.find("<script>") + 8
script_end = html.rfind("</script>")
script_content = html[script_start:script_end]

with open("/Users/devrajput/.gemini/antigravity-ide/scratch/assembled_script.js", "w", encoding="utf-8") as out:
    out.write(script_content)

print("Assembled HTML length:", len(html))
print("Extracted script length:", len(script_content))

cmd = subprocess.run(["node", "-c", "/Users/devrajput/.gemini/antigravity-ide/scratch/assembled_script.js"], capture_output=True, text=True)
if cmd.returncode == 0:
    print("SUCCESS: node -c passed with 0 errors!")
else:
    print("SYNTAX ERROR in assembled_script.js:")
    print(cmd.stderr)
