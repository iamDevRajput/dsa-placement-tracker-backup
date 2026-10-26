import os, re, json

print("Starting Master Build V2...")

source_path = "/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html"
with open(source_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Load the CSS, HTML, and JS
with open("workspace_css.css", "r", encoding="utf-8") as f:
    workspace_css = f.read()

with open("workspace_html.html", "r", encoding="utf-8") as f:
    workspace_html = f.read()

with open("workspace_js.js", "r", encoding="utf-8") as f:
    workspace_js = f.read()

# Append backward-compatibility wrappers to workspace_js
compat_js = """
// Backward compatibility bridge for switchView
function renderPlannerView() {
  const plannerSec = document.getElementById('view-planner');
  if (plannerSec && !plannerSec.classList.contains('active')) {
    document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
    plannerSec.classList.add('active');
  }
  if (typeof switchWorkspaceTab === 'function') switchWorkspaceTab('tab-planner');
}

function renderDiaryView() {
  const plannerSec = document.getElementById('view-planner');
  if (plannerSec && !plannerSec.classList.contains('active')) {
    document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
    plannerSec.classList.add('active');
  }
  if (typeof switchWorkspaceTab === 'function') switchWorkspaceTab('tab-diary');
}
"""
workspace_js += "\n\n" + compat_js

# 2. Replace CSS
pos_p_css = html.find('VIEW 4: DAILY PLANNER')
pos_m_css = html.find('VIEW 6: DAILY MOTIVATION')
if pos_p_css == -1 or pos_m_css == -1:
    print("ERROR: could not locate CSS boundaries")
    exit(1)

css_start = html.rfind('/*', 0, pos_p_css)
css_end = html.rfind('/*', 0, pos_m_css)

html = html[:css_start] + workspace_css + "\n\n" + html[css_end:]
print("1. Replaced CSS successfully.")

# 3. Replace HTML section
planner_match = re.search(r'<section[^>]+id=\"view-planner\"[^>]*>', html)
diary_match = re.search(r'<section[^>]+id=\"view-diary\"[^>]*>', html)
motivation_match = re.search(r'<section[^>]+id=\"view-motivation\"[^>]*>', html)

if not planner_match or not diary_match or not motivation_match:
    print("ERROR: could not locate HTML section boundaries")
    exit(1)

h_start = html.rfind('<!--', 0, planner_match.start())
h_end = html.rfind('</section>', diary_match.start(), motivation_match.start()) + len('</section>')

new_html_block = f"""    <!-- ======================================================================
         PLACEMENT PRODUCTIVITY WORKSPACE (MASTER BUILD V2)
         ====================================================================== -->
{workspace_html}
    <!-- Legacy compatibility placeholder for view-diary -->
    <section class="view-section" id="view-diary" style="display:none;"></section>
"""

html = html[:h_start] + new_html_block + "\n\n" + html[h_end:]
print("2. Replaced HTML sections successfully.")

# 4. Replace JS section
pos_planner_js = html.find('DAILY PLANNER & 5 TRACKS')
pos_dsa_js = html.find('DSA PATTERNS RENDERING')
if pos_planner_js == -1 or pos_dsa_js == -1:
    print("ERROR: could not locate JS boundaries")
    exit(1)

js_start = html.rfind('/*', 0, pos_planner_js)
js_end = html.rfind('/*', 0, pos_dsa_js)

html = html[:js_start] + workspace_js + "\n\n" + html[js_end:]
print("3. Replaced JS engine successfully.")

# 5. Patch switchView to gracefully map 'diary' to view-planner with tab-diary
switch_view_pos = html.find('function switchView(viewName, navEl)')
if switch_view_pos != -1:
    old_target_str = "const target = document.getElementById('view-' + viewName);"
    new_target_str = "const target = document.getElementById(viewName === 'diary' ? 'view-planner' : ('view-' + viewName));"
    if old_target_str in html:
        html = html.replace(old_target_str, new_target_str, 1)
        print("4. Patched switchView target selection for diary.")

# 6. Write to test_workspace_assembled.html
output_test = "test_workspace_assembled.html"
with open(output_test, "w", encoding="utf-8") as f:
    f.write(html)

print(f"SUCCESS: Assembled {output_test} (Size: {len(html)} bytes)")
