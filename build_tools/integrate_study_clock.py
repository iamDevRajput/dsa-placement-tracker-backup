import os
import re

MASTER_FILE = '/Users/devrajput/@Resources/Tracker/integrated_master.html'
SCRATCH_DIR = '/Users/devrajput/.gemini/antigravity-ide/scratch'

with open(MASTER_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

with open(os.path.join(SCRATCH_DIR, 'study_clock_css.css'), 'r', encoding='utf-8') as f:
    css_content = f.read()

with open(os.path.join(SCRATCH_DIR, 'study_clock_html.html'), 'r', encoding='utf-8') as f:
    html_content = f.read()

with open(os.path.join(SCRATCH_DIR, 'study_clock_js.js'), 'r', encoding='utf-8') as f:
    js_content = f.read()

# 1. Add Sidebar Navigation Item
nav_target = """    <button class="nav-item" onclick="switchView('revisions', this)">"""
nav_replacement = """    <button class="nav-item" onclick="switchView('studyclock', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      <span>Study Clock</span>
      <span class="nav-badge" id="nav-studyclock-badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3); font-family:var(--font-mono); font-size:10px;">0m</span>
    </button>
    <button class="nav-item" onclick="switchView('revisions', this)">"""

if nav_target in content:
    content = content.replace(nav_target, nav_replacement, 1)
    print("1. Injected Study Clock sidebar item.")
else:
    print("WARNING: nav_target not found!")

# 2. Update Header Timer Widget
hdr_target = """      <!-- Focus Timer Mini Widget -->
      <div class="header-timer" id="headerTimerWidget">
        <button class="header-timer-btn" onclick="toggleTimerRunning()">
          <span id="hdr-timer-btn-icon">▶</span>
        </button>
        <span id="hdr-timer-display">25:00</span>
      </div>"""

hdr_replacement = """      <!-- Focus Timer Mini Widget -->
      <div class="header-timer" id="headerTimerWidget" onclick="switchView('studyclock')" style="cursor:pointer;" title="Click to open Study Clock">
        <button class="header-timer-btn" onclick="event.stopPropagation(); toggleStudyClockFromHeader()" title="Start / Pause Study Clock">
          <span id="hdr-timer-btn-icon">▶</span>
        </button>
        <span id="hdr-timer-display">00:00:00</span>
      </div>"""

if hdr_target in content:
    content = content.replace(hdr_target, hdr_replacement, 1)
    print("2. Injected header timer updates.")
else:
    print("WARNING: hdr_target not found!")

# Also make hdr-study clickable
hdr_study_old = """<div class="stat-pill" title="Today Study Time">⏱️ <span class="num" id="hdr-study">0m</span></div>"""
hdr_study_new = """<div class="stat-pill" title="Today Study Time • Click to open Study Clock" onclick="switchView('studyclock')" style="cursor:pointer;">⏱️ <span class="num" id="hdr-study">0m</span></div>"""
if hdr_study_old in content:
    content = content.replace(hdr_study_old, hdr_study_new, 1)
    print("2b. Made hdr-study pill clickable.")

# 3. Inject CSS right before </style>
css_target = "</style>"
css_injection = f"\n{css_content}\n</style>"
content = content.replace(css_target, css_injection, 1)
print("3. Injected Study Clock CSS.")

# 4. Inject View Section HTML right after </section> of view-diary
diary_end_target = """    </section>

    <!-- VIEW 6: DAILY MOTIVATION -->"""

html_injection = f"""    </section>

{html_content}

    <!-- VIEW 6: DAILY MOTIVATION -->"""

if diary_end_target in content:
    content = content.replace(diary_end_target, html_injection, 1)
    print("4. Injected Study Clock View HTML.")
else:
    print("WARNING: diary_end_target not found!")

# 5. Update switchView function
switchview_title_target = """    diary: 'Private Placement Journal',
    motivation: 'Daily Motivation & Mindset',"""
switchview_title_new = """    diary: 'Private Placement Journal',
    studyclock: 'Study Clock & Time Tracker',
    motivation: 'Daily Motivation & Mindset',"""

if switchview_title_target in content:
    content = content.replace(switchview_title_target, switchview_title_new, 1)
    print("5a. Updated switchView titleMap.")
else:
    print("WARNING: switchview_title_target not found!")

switchview_render_target = """  else if(viewName === 'diary') renderDiaryView();
  else if(viewName === 'motivation') renderMotivationView();"""
switchview_render_new = """  else if(viewName === 'diary') renderDiaryView();
  else if(viewName === 'studyclock') renderStudyClockView();
  else if(viewName === 'motivation') renderMotivationView();"""

if switchview_render_target in content:
    content = content.replace(switchview_render_target, switchview_render_new, 1)
    print("5b. Updated switchView router.")
else:
    print("WARNING: switchview_render_target not found!")

# 6. Inject JS Code and init call
js_target = "function init() {"
js_injection = f"""
{js_content}

function toggleTimerRunning() {{
  toggleStudyClockFromHeader();
}}

function init() {{"""

if js_target in content:
    content = content.replace(js_target, js_injection, 1)
    print("6a. Injected Study Clock JS engine.")
else:
    print("WARNING: js_target not found!")

# 7. Add initStudyClockEngine() and renderStudyClockView() to init()
init_call_target = """  renderRevisionCenterView();
  renderPlannerView();
  renderDiaryView();
  renderMotivationView();"""

init_call_new = """  renderRevisionCenterView();
  renderPlannerView();
  renderDiaryView();
  renderMotivationView();
  initStudyClockEngine();
  renderStudyClockView();"""

if init_call_target in content:
    content = content.replace(init_call_target, init_call_new, 1)
    print("7. Injected Study Clock init calls.")
else:
    print("WARNING: init_call_target not found!")

# Write to scratch test file first
scratch_test_file = os.path.join(SCRATCH_DIR, 'test_study_clock_master.html')
with open(scratch_test_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Assembly completed successfully! Saved to {scratch_test_file} ({len(content)} bytes)")
