import os
import re

SOURCE_HTML = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"

with open(SOURCE_HTML, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Original index.html size: {len(html)} bytes")

# 1. SIDEBAR BUTTON
sidebar_target = """    <button class="nav-item" onclick="switchView('skillshub', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
      <span>Skills Learning Hub</span>
      <span class="nav-badge" id="nav-skillshub-badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3);">0/31</span>
    </button>"""

sidebar_replacement = sidebar_target + """
    <button class="nav-item" onclick="switchView('resources', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/><line x1="12" y1="7" x2="12" y2="13"/><line x1="9" y1="10" x2="15" y2="10"/></svg>
      <span>Resources</span>
      <span class="nav-badge" style="background:rgba(99,102,241,0.15); color:#818cf8; border:1px solid rgba(99,102,241,0.3);" id="nav-resources-badge">18</span>
    </button>"""

if "switchView('resources', this)" not in html:
    assert sidebar_target in html, "Sidebar target not found"
    html = html.replace(sidebar_target, sidebar_replacement, 1)
    print("Added Resources button to sidebar")

# 2. VIEW SECTION HTML
view_target = """<!-- VIEW: SKILLS LEARNING HUB -->
<section class="view-section" id="view-skillshub">"""

view_end_target = """    <!-- 4. Dynamic Sections & Lessons Container -->
    <div id="skSectionsContainer">
      <!-- Injected via JavaScript -->
    </div>

  </div>
</section>"""

resources_view_html = """

<!-- VIEW: PLACEMENT PREPARATION RESOURCES LIBRARY -->
<section class="view-section" id="view-resources">
  <div class="res-container">

    <!-- 1. Hero Header Card -->
    <div class="res-hero-card">
      <div class="res-hero-title-group">
        <div class="res-pretitle-pill">
          <span>📖 Curated Placement Preparation Library</span>
        </div>
        <h2 class="res-hero-title">Placement Resources & Quick Revision</h2>
        <p class="res-hero-subtitle">
          Essential tutorials, handwritten revision notes, LeetCode practice plans, core CS questions, and HR interview guides curated for software engineering campus and off-campus placements.
        </p>

        <!-- Personal advice banner from Excel sheet -->
        <div class="res-quote-box">
          <span style="font-size:16px; flex-shrink:0;">💡</span>
          <div>
            <b>A quick personal reminder:</b> <i>"Honestly, it’s not about the resource — it’s about how seriously you follow it. Don’t try to do everything at once. Pick one path, stay consistent, trust the process, and most importantly — don’t keep switching resources."</i>
          </div>
        </div>
      </div>

      <div class="res-hero-stats">
        <div class="res-stat-box">
          <span class="res-stat-value" id="resTotalCountDisplay">18</span>
          <span class="res-stat-label">Total Links</span>
        </div>
        <div class="res-stat-box">
          <span class="res-stat-value" style="color:var(--accent4, #f59e0b);">5</span>
          <span class="res-stat-label">PDF Notes</span>
        </div>
        <div class="res-stat-box">
          <span class="res-stat-value" style="color:#ef4444;">5</span>
          <span class="res-stat-label">Tutorials</span>
        </div>
        <div class="res-stat-box">
          <span class="res-stat-value" style="color:var(--accent3, #10b981);">8</span>
          <span class="res-stat-label">Subjects</span>
        </div>
      </div>
    </div>

    <!-- 2. Toolbar: Search Bar and Category/Type Filter Pills -->
    <div class="res-toolbar">
      <div class="res-toolbar-top">
        <div class="res-search-wrap">
          <svg class="res-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input type="text" class="res-search-input" id="resSearchInput" placeholder="Search by subject, title, or type (e.g., OOPS, DBMS, PDF, LeetCode, GFG)..." oninput="handleResourcesSearch(this.value)">
        </div>
        <div id="resMatchCountLabel" style="font-size:12px; font-family:var(--font-mono, monospace); color:var(--text-muted); white-space:nowrap;">Showing 18 resources</div>
      </div>

      <!-- Category Filter Pills -->
      <div class="res-filter-row" style="border-top:1px solid var(--border-subtle, #1e2033); padding-top:0.75rem;">
        <span style="font-size:11px; font-weight:700; color:var(--text-dim, #636682); text-transform:uppercase; letter-spacing:0.05em; margin-right:0.25rem;">Category:</span>
        <button type="button" class="res-pill-btn active" id="resCat-all" onclick="filterResourcesByCategory('all')">All (18)</button>
        <button type="button" class="res-pill-btn" id="resCat-dsa" onclick="filterResourcesByCategory('dsa')">⚡ DSA</button>
        <button type="button" class="res-pill-btn" id="resCat-core" onclick="filterResourcesByCategory('core')">🧠 Core CS (OS, DBMS, CN, OOPS)</button>
        <button type="button" class="res-pill-btn" id="resCat-sql" onclick="filterResourcesByCategory('sql')">📊 SQL</button>
        <button type="button" class="res-pill-btn" id="resCat-aptitude_hr" onclick="filterResourcesByCategory('aptitude_hr')">🎯 Aptitude & HR</button>
        <button type="button" class="res-pill-btn" id="resCat-resume" onclick="filterResourcesByCategory('resume')">📝 Resume</button>
      </div>

      <!-- Type Filter Pills -->
      <div class="res-filter-row" style="border-top:1px solid var(--border-subtle, #1e2033); padding-top:0.6rem;">
        <span style="font-size:11px; font-weight:700; color:var(--text-dim, #636682); text-transform:uppercase; letter-spacing:0.05em; margin-right:0.25rem;">Type:</span>
        <button type="button" class="res-pill-btn active" id="resType-all" onclick="filterResourcesByType('all')">All Types</button>
        <button type="button" class="res-pill-btn" id="resType-tutorial" onclick="filterResourcesByType('tutorial')">▶️ Video Tutorials (5)</button>
        <button type="button" class="res-pill-btn" id="resType-notes" onclick="filterResourcesByType('notes')">📄 Notes / PDFs (5)</button>
        <button type="button" class="res-pill-btn" id="resType-interview" onclick="filterResourcesByType('interview')">❓ Interview Q&A (5)</button>
        <button type="button" class="res-pill-btn" id="resType-practice" onclick="filterResourcesByType('practice')">💻 Practice (2)</button>
        <button type="button" class="res-pill-btn" id="resType-resume" onclick="filterResourcesByType('resume')">📝 Resume (1)</button>
      </div>
    </div>

    <!-- 3. Dynamic Resources Grid Container -->
    <div class="res-grid" id="resGridContainer">
      <!-- Populated via renderResourcesView() -->
    </div>

  </div>
</section>
"""

if 'id="view-resources"' not in html:
    assert view_end_target in html, "Skills hub end target not found"
    html = html.replace(view_end_target, view_end_target + resources_view_html, 1)
    print("Added view-resources HTML section")

# 3. CSS SECTION
css_target = """/* ==========================================================================
   PERSONAL MOTIVATION CENTER V2 — EMERALD-DARK THEME & INSPIRATION LIBRARY
   ========================================================================== */"""

resources_css = """/* ==========================================================================
   PLACEMENT RESOURCES LIBRARY — CURATED PLACEMENT PREPARATION
   ========================================================================== */

.res-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 1.5rem 1.75rem 3.5rem;
  max-width: 1560px;
  margin: 0 auto;
  width: 100%;
}

.res-hero-card {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(15, 23, 42, 0.85) 50%, rgba(16, 185, 129, 0.08) 100%);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: var(--radius-lg, 16px);
  padding: 1.75rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1.5rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
  position: relative;
  overflow: hidden;
}

.res-hero-card::after {
  content: '';
  position: absolute;
  top: -60px;
  right: -60px;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(99, 102, 241, 0.18) 0%, transparent 70%);
  pointer-events: none;
}

.res-hero-title-group {
  max-width: 720px;
}

.res-pretitle-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.25rem 0.75rem;
  background: rgba(99, 102, 241, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.35);
  border-radius: 999px;
  font-family: var(--font-mono, monospace);
  font-size: 11px;
  font-weight: 600;
  color: var(--accent-light, #818cf8);
  margin-bottom: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.res-hero-title {
  font-family: var(--font-heading, sans-serif);
  font-size: 1.75rem;
  font-weight: 800;
  color: #f8fafc;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.02em;
}

.res-hero-subtitle {
  font-size: 13.5px;
  color: var(--text-muted, #9497b0);
  line-height: 1.55;
  margin: 0;
}

.res-quote-box {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(99, 102, 241, 0.25);
  border-left: 3px solid var(--accent, #6366f1);
  border-radius: var(--radius-md, 10px);
  padding: 0.75rem 1rem;
  font-size: 12.5px;
  color: #cbd5e1;
  line-height: 1.5;
  margin-top: 0.85rem;
  display: flex;
  align-items: flex-start;
  gap: 0.6rem;
}

.res-hero-stats {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.res-stat-box {
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid var(--border-subtle, #1e2033);
  border-radius: var(--radius-md, 10px);
  padding: 0.85rem 1.15rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 105px;
}

.res-stat-value {
  font-family: var(--font-mono, monospace);
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--accent-light, #818cf8);
}

.res-stat-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-dim, #636682);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-top: 0.2rem;
}

/* Toolbar */
.res-toolbar {
  background: var(--surface, #141522);
  border: 1px solid var(--border, #282a42);
  border-radius: var(--radius-lg, 16px);
  padding: 1.1rem 1.4rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
}

.res-toolbar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.res-search-wrap {
  position: relative;
  flex: 1;
  min-width: 260px;
}

.res-search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim, #636682);
  pointer-events: none;
}

.res-search-input {
  width: 100%;
  padding: 0.65rem 0.85rem 0.65rem 2.25rem;
  background: var(--surface2, #1b1c2e);
  border: 1px solid var(--border-subtle, #1e2033);
  border-radius: var(--radius-md, 10px);
  color: var(--text, #f1f2f9);
  font-family: var(--font-body, sans-serif);
  font-size: 13px;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.res-search-input:focus {
  outline: none;
  border-color: var(--accent, #6366f1);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.18);
}

.res-filter-row {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  flex-wrap: wrap;
}

.res-pill-btn {
  background: var(--surface2, #1b1c2e);
  border: 1px solid var(--border-subtle, #1e2033);
  color: var(--text-muted, #9497b0);
  border-radius: 999px;
  padding: 0.35rem 0.85rem;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-family: var(--font-body, sans-serif);
}

.res-pill-btn:hover {
  color: var(--text, #f1f2f9);
  border-color: var(--border, #282a42);
  background: var(--surface3, #24253d);
}

.res-pill-btn.active {
  background: rgba(99, 102, 241, 0.2);
  border-color: var(--accent, #6366f1);
  color: var(--accent-light, #818cf8);
  font-weight: 600;
}

/* Resources Grid & Cards */
.res-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 1.25rem;
}

.res-card {
  background: var(--surface, #141522);
  border: 1px solid var(--border, #282a42);
  border-radius: var(--radius-lg, 16px);
  padding: 1.35rem 1.45rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 1rem;
  transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
  position: relative;
}

.res-card:hover {
  transform: translateY(-2px);
  border-color: rgba(99, 102, 241, 0.45);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}

.res-card-top {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.res-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.res-subject-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 11px;
  font-weight: 700;
  font-family: var(--font-mono, monospace);
  padding: 0.2rem 0.55rem;
  border-radius: 6px;
  background: var(--surface2, #1b1c2e);
  color: var(--text, #f1f2f9);
  border: 1px solid var(--border-subtle, #1e2033);
}

.res-type-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 10.5px;
  font-weight: 600;
  font-family: var(--font-mono, monospace);
  padding: 0.2rem 0.6rem;
  border-radius: 999px;
}

.res-type-tutorial {
  background: rgba(239, 68, 68, 0.14);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.res-type-notes {
  background: rgba(245, 158, 11, 0.14);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.res-type-interview {
  background: rgba(16, 185, 129, 0.14);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.res-type-practice {
  background: rgba(6, 182, 212, 0.14);
  color: #38bdf8;
  border: 1px solid rgba(6, 182, 212, 0.3);
}

.res-type-resume {
  background: rgba(168, 85, 247, 0.14);
  color: #c084fc;
  border: 1px solid rgba(168, 85, 247, 0.3);
}

.res-title {
  font-family: var(--font-heading, sans-serif);
  font-size: 15px;
  font-weight: 700;
  color: #f8fafc;
  line-height: 1.35;
  margin: 0;
}

.res-desc {
  font-size: 12.5px;
  color: var(--text-muted, #9497b0);
  line-height: 1.5;
  margin: 0;
}

.res-provider-strip {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  font-size: 11.5px;
  color: var(--text-dim, #636682);
  font-family: var(--font-mono, monospace);
}

.res-provider-name {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.res-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  border-top: 1px solid var(--border-subtle, #1e2033);
  padding-top: 0.85rem;
}

.res-btn-open {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  padding: 0.55rem 1rem;
  background: var(--surface2, #1b1c2e);
  border: 1px solid var(--border, #282a42);
  border-radius: var(--radius-sm, 6px);
  color: #f8fafc;
  font-size: 12.5px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: var(--font-body, sans-serif);
}

.res-btn-open:hover {
  background: var(--accent, #6366f1);
  border-color: var(--accent, #6366f1);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
}

.res-btn-copy {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.55rem 0.75rem;
  background: var(--surface2, #1b1c2e);
  border: 1px solid var(--border-subtle, #1e2033);
  border-radius: var(--radius-sm, 6px);
  color: var(--text-muted, #9497b0);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: var(--font-body, sans-serif);
}

.res-btn-copy:hover {
  color: var(--text, #f1f2f9);
  border-color: var(--border, #282a42);
  background: var(--surface3, #24253d);
}

/* Empty state */
.res-empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 3.5rem 1.5rem;
  background: var(--surface, #141522);
  border: 1px dashed var(--border, #282a42);
  border-radius: var(--radius-lg, 16px);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}

.res-empty-icon {
  font-size: 2.25rem;
  opacity: 0.7;
}

.res-empty-title {
  font-family: var(--font-heading, sans-serif);
  font-size: 16px;
  font-weight: 700;
  color: #f8fafc;
}

.res-empty-desc {
  font-size: 13px;
  color: var(--text-muted, #9497b0);
  max-width: 420px;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .res-container {
    padding: 1rem 1rem 3rem;
  }
  .res-hero-card {
    padding: 1.25rem;
  }
  .res-grid {
    grid-template-columns: 1fr;
  }
}

"""

if ".res-container" not in html:
    assert css_target in html, "CSS target not found"
    html = html.replace(css_target, resources_css + css_target, 1)
    print("Added Resources CSS styling")

# 4. SWITCHVIEW TITLEMAP & DISPATCHER
switch_title_target = "skillshub: 'Skills Learning Hub',"
switch_title_replacement = """skillshub: 'Skills Learning Hub',
    resources: 'Placement Preparation Resource Library',"""

if "resources: 'Placement Preparation Resource Library'," not in html:
    assert switch_title_target in html, "switchView title target not found"
    html = html.replace(switch_title_target, switch_title_replacement, 1)
    print("Added resources to titleMap")

switch_dispatcher_target = "else if(viewName === 'skillshub') renderSkillsHubView();"
switch_dispatcher_replacement = """else if(viewName === 'skillshub') renderSkillsHubView();
  else if(viewName === 'resources') renderResourcesView();"""

if "else if(viewName === 'resources') renderResourcesView();" not in html:
    assert switch_dispatcher_target in html, "switchView dispatcher target not found"
    html = html.replace(switch_dispatcher_target, switch_dispatcher_replacement, 1)
    print("Added resources to switchView dispatcher")

# 5. INIT CALL
init_target = "initSkillsHubEngine();\n  renderSkillsHubView();"
init_replacement = """initSkillsHubEngine();
  renderSkillsHubView();
  if (typeof initResourcesEngine === 'function') initResourcesEngine();
  if (typeof renderResourcesView === 'function') renderResourcesView();"""

if "initResourcesEngine" not in html:
    assert init_target in html, "init target not found"
    html = html.replace(init_target, init_replacement, 1)
    print("Added initResourcesEngine to init()")

# 6. JAVASCRIPT ENGINE
js_target = """/* ==========================================================================
   PERSONAL MOTIVATION CENTER V2 — JAVASCRIPT ENGINE
   ========================================================================== */"""

resources_js = """/* ==========================================================================
   PLACEMENT RESOURCES LIBRARY — JAVASCRIPT ENGINE & CURATED DATA
   ========================================================================== */

const PLACEMENT_RESOURCES_DATA = [
  {
    id: 'res_dsa_striver',
    subject: 'DSA',
    subjectLabel: 'Data Structures & Algorithms',
    subjectIcon: '⚡',
    title: "Striver's A2Z DSA Sheet",
    type: 'practice',
    typeLabel: 'Complete Sheet',
    typeIcon: '💻',
    provider: 'takeUforward',
    providerIcon: '🌐',
    url: 'https://takeuforward.org/dsa/strivers-a2z-sheet-learn-dsa-a-to-z',
    desc: 'Comprehensive step-by-step DSA course & sheet covering 455 problems from basic arrays to advanced graphs and dynamic programming.',
    category: 'dsa',
    badge: 'Core Sheet'
  },
  {
    id: 'res_oops_tutorial',
    subject: 'OOPS',
    subjectLabel: 'Object Oriented Programming',
    subjectIcon: '🧩',
    title: 'OOPs Tutorial in One Shot (C++ Language) for Placement Interviews',
    type: 'tutorial',
    typeLabel: 'Video Tutorial',
    typeIcon: '▶️',
    provider: 'YouTube · CodeHelp (Love Babbar)',
    providerIcon: '▶️',
    url: 'https://www.youtube.com/watch?v=mlIUKyZIUUU',
    desc: 'Complete Object Oriented Programming in one shot for campus placements: Classes, Objects, 4 Pillars (Encapsulation, Abstraction, Inheritance, Polymorphism), and Virtual functions.',
    category: 'core',
    badge: 'One-Shot'
  },
  {
    id: 'res_oops_notes',
    subject: 'OOPS',
    subjectLabel: 'Object Oriented Programming',
    subjectIcon: '🧩',
    title: '4.OOP.pdf — Comprehensive OOPS Placement Notes',
    type: 'notes',
    typeLabel: 'Notes / PDF',
    typeIcon: '📄',
    provider: 'Google Drive',
    providerIcon: '📂',
    url: 'https://drive.google.com/file/d/19FaiItoU6-zOhhVSHXXX4Z8AWCF7AfF-/view?usp=drive_link',
    desc: 'Concise, high-yield PDF revision handbook on OOP concepts, memory layout, constructors, destructors, dynamic polymorphism, and interview quick sheets.',
    category: 'core',
    badge: 'PDF Notes'
  },
  {
    id: 'res_oops_interview',
    subject: 'OOPS',
    subjectLabel: 'Object Oriented Programming',
    subjectIcon: '🧩',
    title: 'OOP Interview Questions and Answers',
    type: 'interview',
    typeLabel: 'Interview Questions',
    typeIcon: '❓',
    provider: 'GeeksforGeeks',
    providerIcon: '🌐',
    url: 'https://www.geeksforgeeks.org/interview-prep/oops-interview-questions/',
    desc: 'Most frequently asked OOPS interview questions for software engineering campus and off-campus placements with code examples.',
    category: 'core',
    badge: 'Interview Q&A'
  },
  {
    id: 'res_dbms_tutorial',
    subject: 'DBMS',
    subjectLabel: 'Database Management Systems',
    subjectIcon: '🗄️',
    title: 'Complete DBMS in 1 Video (With Notes) for Placement Interviews',
    type: 'tutorial',
    typeLabel: 'Video Tutorial',
    typeIcon: '▶️',
    provider: 'YouTube · Knowledge Gate',
    providerIcon: '▶️',
    url: 'https://www.youtube.com/watch?v=dl00fOOYLOM&t=16795s',
    desc: 'Complete database theory: ER models, Relational Algebra, Functional Dependencies, Normal Forms (1NF, 2NF, 3NF, BCNF), and Transactions & Concurrency Control.',
    category: 'core',
    badge: 'One-Shot'
  },
  {
    id: 'res_dbms_notes',
    subject: 'DBMS',
    subjectLabel: 'Database Management Systems',
    subjectIcon: '🗄️',
    title: '1.DBMS.pdf — Handwritten Placement Notes',
    type: 'notes',
    typeLabel: 'Notes / PDF',
    typeIcon: '📄',
    provider: 'Google Drive',
    providerIcon: '📂',
    url: 'https://drive.google.com/file/d/1eoyyYBSewweyDGIPBixdjsW6gl2Qxesf/view?usp=drive_link',
    desc: 'Clean handwritten placement revision notes covering SQL commands, ACID properties, serializability, two-phase locking, and B/B+ trees.',
    category: 'core',
    badge: 'PDF Notes'
  },
  {
    id: 'res_dbms_interview',
    subject: 'DBMS',
    subjectLabel: 'Database Management Systems',
    subjectIcon: '🗄️',
    title: 'Commonly Asked DBMS Interview Questions',
    type: 'interview',
    typeLabel: 'Interview Questions',
    typeIcon: '❓',
    provider: 'GeeksforGeeks',
    providerIcon: '🌐',
    url: 'https://www.geeksforgeeks.org/dbms/commonly-asked-dbms-interview-questions/',
    desc: 'Curated list of standard DBMS technical interview questions with crisp definitions and diagram explanations.',
    category: 'core',
    badge: 'Interview Q&A'
  },
  {
    id: 'res_os_tutorial',
    subject: 'OS',
    subjectLabel: 'Operating Systems',
    subjectIcon: '⚡',
    title: 'Complete Operating Systems in 1 Shot (With Notes) for Placement Interviews',
    type: 'tutorial',
    typeLabel: 'Video Tutorial',
    typeIcon: '▶️',
    provider: 'YouTube · Knowledge Gate',
    providerIcon: '▶️',
    url: 'https://www.youtube.com/watch?v=3obEP8eLsCw',
    desc: 'Comprehensive OS syllabus: Process Lifecycle, CPU Scheduling Algorithms, Synchronization (Mutex, Semaphores), Deadlocks, Paging, and Virtual Memory.',
    category: 'core',
    badge: 'One-Shot'
  },
  {
    id: 'res_os_notes',
    subject: 'OS',
    subjectLabel: 'Operating Systems',
    subjectIcon: '⚡',
    title: '2.Operating System.pdf — OS Placement Notes',
    type: 'notes',
    typeLabel: 'Notes / PDF',
    typeIcon: '📄',
    provider: 'Google Drive',
    providerIcon: '📂',
    url: 'https://drive.google.com/file/d/1ovvurN5wmVl_YmSRDeIpCkcsdLMH6GrB/view?usp=drive_link',
    desc: 'Essential OS handbook with memory management diagrams, page replacement formulas, deadlock handling techniques, and disk scheduling algorithms.',
    category: 'core',
    badge: 'PDF Notes'
  },
  {
    id: 'res_os_interview',
    subject: 'OS',
    subjectLabel: 'Operating Systems',
    subjectIcon: '⚡',
    title: '50+ OS, DBMS, CN Interview Questions [Updated]',
    type: 'interview',
    typeLabel: 'Interview Questions',
    typeIcon: '❓',
    provider: 'GeeksforGeeks',
    providerIcon: '🌐',
    url: 'https://www.geeksforgeeks.org/interview-prep/os-cn-dbms-interview-questions/',
    desc: 'Top 50+ core CS interview questions frequently asked by top product-based companies and FAANG recruiters.',
    category: 'core',
    badge: 'Interview Q&A'
  },
  {
    id: 'res_cn_tutorial',
    subject: 'CN',
    subjectLabel: 'Computer Networks',
    subjectIcon: '🌐',
    title: 'Computer Networking Full Course — OSI Model Deep Dive with Real Life Examples',
    type: 'tutorial',
    typeLabel: 'Video Tutorial',
    typeIcon: '▶️',
    provider: 'YouTube · NetworkChuck',
    providerIcon: '▶️',
    url: 'https://www.youtube.com/watch?v=IPvYjXCsTg8',
    desc: 'In-depth visual walkthrough of the OSI 7-layer model, TCP/IP stack, IP addressing, Subnetting, DNS resolution, and packet routing.',
    category: 'core',
    badge: 'Full Course'
  },
  {
    id: 'res_cn_interview',
    subject: 'CN',
    subjectLabel: 'Computer Networks',
    subjectIcon: '🌐',
    title: '50+ OS, DBMS, CN Interview Questions [Updated]',
    type: 'interview',
    typeLabel: 'Interview Questions',
    typeIcon: '❓',
    provider: 'GeeksforGeeks',
    providerIcon: '🌐',
    url: 'https://www.geeksforgeeks.org/interview-prep/os-cn-dbms-interview-questions/',
    desc: 'Core Computer Networks questions: TCP 3-way handshake, UDP vs TCP, HTTP vs HTTPS, SSL/TLS, Congestion control, and IP routing.',
    category: 'core',
    badge: 'Interview Q&A'
  },
  {
    id: 'res_sql_tutorial',
    subject: 'SQL',
    subjectLabel: 'SQL & Database Queries',
    subjectIcon: '📊',
    title: 'Complete SQL Course in 3 Hours | SQL One Shot using MySQL',
    type: 'tutorial',
    typeLabel: 'Video Tutorial',
    typeIcon: '▶️',
    provider: 'YouTube · Apna College',
    providerIcon: '▶️',
    url: 'https://www.youtube.com/watch?v=hlGoQC332VM',
    desc: 'From basic SELECT and WHERE to complex GROUP BY, HAVING, Joins, Subqueries, Constraints, and schema creation in MySQL.',
    category: 'sql',
    badge: 'One-Shot'
  },
  {
    id: 'res_sql_notes',
    subject: 'SQL',
    subjectLabel: 'SQL & Database Queries',
    subjectIcon: '📊',
    title: '5.SQL.pdf — SQL Revision Cheat Sheet & Notes',
    type: 'notes',
    typeLabel: 'Notes / PDF',
    typeIcon: '📄',
    provider: 'Google Drive',
    providerIcon: '📂',
    url: 'https://drive.google.com/file/d/1rwKjwHt-EPcaAma0r5p5Ym2gUpEW-WRB/view?usp=drive_link',
    desc: 'Quick SQL syntax cheat sheet, window functions (ROW_NUMBER, RANK, DENSE_RANK), joins comparison table, and aggregate queries.',
    category: 'sql',
    badge: 'PDF Notes'
  },
  {
    id: 'res_sql_practice',
    subject: 'SQL',
    subjectLabel: 'SQL & Database Queries',
    subjectIcon: '📊',
    title: 'Top SQL 50 Study Plan — LeetCode',
    type: 'practice',
    typeLabel: 'Interactive Practice',
    typeIcon: '💻',
    provider: 'LeetCode',
    providerIcon: '🟠',
    url: 'https://leetcode.com/studyplan/top-sql-50/',
    desc: 'The official LeetCode 50 SQL problem set curated specifically to crack technical interview database rounds.',
    category: 'sql',
    badge: 'LeetCode 50'
  },
  {
    id: 'res_hr_questions',
    subject: 'HR Questions',
    subjectLabel: 'HR & Behavioral Interview',
    subjectIcon: '🤝',
    title: 'How to Answer the 64 Toughest Interview Questions (PDF)',
    type: 'notes',
    typeLabel: 'Guide / PDF',
    typeIcon: '📄',
    provider: 'Google Drive',
    providerIcon: '📂',
    url: 'https://drive.google.com/file/d/1PxuY0vLF3Qr3K4uWx5A3LsW_uuSQy3fx/view?usp=drive_link',
    desc: 'The definitive executive guide to answering behavioral, situational, strengths/weaknesses, and compensation questions with the STAR technique.',
    category: 'aptitude_hr',
    badge: 'HR Guide'
  },
  {
    id: 'res_puzzles',
    subject: 'Puzzles',
    subjectLabel: 'Puzzles & Brainteasers',
    subjectIcon: '🧩',
    title: 'Top 100 Puzzles Asked in Interviews',
    type: 'interview',
    typeLabel: 'Interview Questions',
    typeIcon: '❓',
    provider: 'GeeksforGeeks',
    providerIcon: '🌐',
    url: 'https://www.geeksforgeeks.org/aptitude/top-100-puzzles-asked-in-interviews/',
    desc: '100 classic interview puzzles, logic brainteasers, probability riddles, and mathematical trick questions with step-by-step solutions.',
    category: 'aptitude_hr',
    badge: 'Top 100'
  },
  {
    id: 'res_resume_template',
    subject: 'My Resume Template',
    subjectLabel: 'Placement Resume',
    subjectIcon: '📄',
    title: 'Placement Resume Template (Overleaf / LaTeX)',
    type: 'resume',
    typeLabel: 'Overleaf Template',
    typeIcon: '📝',
    provider: 'Overleaf',
    providerIcon: '🍃',
    url: 'https://www.overleaf.com/read/xnqtdgbxmmdg',
    desc: 'Clean, ATS-friendly single-page LaTeX software engineering resume template hosted on Overleaf. Ready to clone and customize.',
    category: 'resume',
    badge: 'Overleaf'
  }
];

let resActiveCategory = 'all';
let resActiveType = 'all';
let resSearchQuery = '';

function initResourcesEngine() {
  const badge = document.getElementById('nav-resources-badge');
  if (badge) badge.textContent = PLACEMENT_RESOURCES_DATA.length;
}

function filterResourcesByCategory(cat) {
  resActiveCategory = cat;
  document.querySelectorAll('.res-filter-row:first-of-type .res-pill-btn').forEach(btn => {
    btn.classList.toggle('active', btn.id === 'resCat-' + cat);
  });
  renderResourcesView();
}

function filterResourcesByType(type) {
  resActiveType = type;
  document.querySelectorAll('.res-filter-row:last-of-type .res-pill-btn').forEach(btn => {
    btn.classList.toggle('active', btn.id === 'resType-' + type);
  });
  renderResourcesView();
}

function handleResourcesSearch(query) {
  resSearchQuery = (query || '').trim().toLowerCase();
  renderResourcesView();
}

function resetResourcesFilters() {
  resActiveCategory = 'all';
  resActiveType = 'all';
  resSearchQuery = '';
  const searchInput = document.getElementById('resSearchInput');
  if (searchInput) searchInput.value = '';
  document.querySelectorAll('.res-filter-row .res-pill-btn').forEach(btn => {
    btn.classList.toggle('active', btn.id === 'resCat-all' || btn.id === 'resType-all');
  });
  renderResourcesView();
}

function copyResourceById(id, btn) {
  const item = PLACEMENT_RESOURCES_DATA.find(r => r.id === id);
  if (!item || !item.url) return;
  const url = item.url;
  const originalHtml = btn.innerHTML;
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(() => {
      btn.innerHTML = '<span>✓ Copied</span>';
      btn.style.color = '#10b981';
      btn.style.borderColor = '#10b981';
      setTimeout(() => {
        btn.innerHTML = originalHtml;
        btn.style.color = '';
        btn.style.borderColor = '';
      }, 1600);
    }).catch(() => fallbackCopyText(url, btn, originalHtml));
  } else {
    fallbackCopyText(url, btn, originalHtml);
  }
}

function fallbackCopyText(text, btn, originalHtml) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.select();
  try {
    document.execCommand('copy');
    btn.innerHTML = '<span>✓ Copied</span>';
    setTimeout(() => { btn.innerHTML = originalHtml; }, 1600);
  } catch(e) {
    prompt('Copy resource URL:', text);
  }
  document.body.removeChild(ta);
}

function renderResourcesView() {
  const container = document.getElementById('resGridContainer');
  if (!container) return;

  const filtered = PLACEMENT_RESOURCES_DATA.filter(item => {
    // 1. Category filter
    if (resActiveCategory !== 'all' && item.category !== resActiveCategory) {
      return false;
    }
    // 2. Type filter
    if (resActiveType !== 'all' && item.type !== resActiveType) {
      return false;
    }
    // 3. Search query
    if (resSearchQuery) {
      const matchSubject = item.subject.toLowerCase().includes(resSearchQuery);
      const matchLabel = item.subjectLabel.toLowerCase().includes(resSearchQuery);
      const matchTitle = item.title.toLowerCase().includes(resSearchQuery);
      const matchDesc = item.desc.toLowerCase().includes(resSearchQuery);
      const matchProvider = item.provider.toLowerCase().includes(resSearchQuery);
      const matchType = item.typeLabel.toLowerCase().includes(resSearchQuery);
      if (!matchSubject && !matchLabel && !matchTitle && !matchDesc && !matchProvider && !matchType) {
        return false;
      }
    }
    return true;
  });

  // Update counter label
  const matchLabel = document.getElementById('resMatchCountLabel');
  if (matchLabel) {
    matchLabel.textContent = `Showing ${filtered.length} of ${PLACEMENT_RESOURCES_DATA.length} resources`;
  }

  if (filtered.length === 0) {
    container.innerHTML = `
      <div class="res-empty-state">
        <div class="res-empty-icon">🔍</div>
        <div class="res-empty-title">No matching resources found</div>
        <div class="res-empty-desc">
          No resources matched your search "${escapeHtmlRes(resSearchQuery)}" in the selected category/type filters.
        </div>
        <button type="button" class="btn btn-secondary" onclick="resetResourcesFilters()" style="margin-top:0.5rem;">Reset All Filters</button>
      </div>
    `;
    return;
  }

  container.innerHTML = filtered.map(res => {
    return `
      <div class="res-card">
        <div class="res-card-top">
          <div class="res-header">
            <span class="res-subject-badge">
              <span>${res.subjectIcon}</span>
              <span>${escapeHtmlRes(res.subject)}</span>
            </span>
            <span class="res-type-badge res-type-${res.type}">
              <span>${res.typeIcon}</span>
              <span>${escapeHtmlRes(res.typeLabel)}</span>
            </span>
          </div>

          <h3 class="res-title">${escapeHtmlRes(res.title)}</h3>
          <p class="res-desc">${escapeHtmlRes(res.desc)}</p>
        </div>

        <div>
          <div class="res-provider-strip">
            <span class="res-provider-name">${res.providerIcon} ${escapeHtmlRes(res.provider)}</span>
            <span style="font-size:10.5px; color:var(--text-dim);">${escapeHtmlRes(res.badge)}</span>
          </div>

          <div class="res-actions">
            <a href="${res.url}" target="_blank" rel="noopener noreferrer" class="res-btn-open">
              <span>Open Resource</span>
              <span style="font-size:13px;">↗</span>
            </a>
            <button type="button" class="res-btn-copy" onclick="copyResourceById('${res.id}', this)" title="Copy direct link to clipboard">
              <span>📋 Copy</span>
            </button>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function escapeHtmlRes(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

"""

if "PLACEMENT_RESOURCES_DATA" not in html:
    assert js_target in html, "JS target not found"
    html = html.replace(js_target, resources_js + js_target, 1)
    print("Added Resources JavaScript engine and dataset")

with open(SOURCE_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Updated index.html written! New size: {len(html)} bytes")
