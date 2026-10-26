import os, re

print("Starting UI Repair for Daily Planner & Private Diary...")

source_path = "/Users/devrajput/@Resources/Tracker/integrated_master.html"
with open(source_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Load the modular CSS
with open("workspace_css.css", "r", encoding="utf-8") as f:
    workspace_css = f.read()

with open("scratch_diary_css.css", "r", encoding="utf-8") as f:
    diary_css = f.read()

combined_css = f"""{workspace_css}

{diary_css}
"""

pos_p_css = html.find('PLACEMENT PRODUCTIVITY WORKSPACE')
pos_m_css = html.find('VIEW 6: DAILY MOTIVATION')
if pos_p_css == -1 or pos_m_css == -1:
    print("ERROR: could not locate CSS boundaries")
    exit(1)

css_start = html.rfind('/*', 0, pos_p_css)
css_end = html.rfind('/*', 0, pos_m_css)

html = html[:css_start] + combined_css + "\n\n" + html[css_end:]
print("1. Injected combined Planner + Diary CSS.")

# 2. Load the modular HTML
with open("workspace_html.html", "r", encoding="utf-8") as f:
    workspace_html = f.read()

with open("scratch_diary_html.html", "r", encoding="utf-8") as f:
    diary_html = f.read()

combined_html = f"""{workspace_html}

{diary_html}
"""

planner_match = re.search(r'<section[^>]+id=\"view-planner\"[^>]*>', html)
motivation_match = re.search(r'<section[^>]+id=\"view-motivation\"[^>]*>', html)

if not planner_match or not motivation_match:
    print("ERROR: could not locate HTML section boundaries")
    exit(1)

h_start = html.rfind('<!--', 0, planner_match.start())
h_end = html.rfind('<!--', 0, motivation_match.start())

html = html[:h_start] + combined_html + "\n\n    " + html[h_end:]
print("2. Injected separate Planner and Diary HTML sections.")

# 3. Load the modular JS
with open("workspace_js.js", "r", encoding="utf-8") as f:
    workspace_js = f.read()

with open("scratch_diary_js.js", "r", encoding="utf-8") as f:
    diary_js = f.read()

combined_js = f"""/* ==========================================================================
   DAILY PLANNER & PRODUCTIVITY WORKSPACE ENGINE (OFFLINE)
   ========================================================================== */
{workspace_js}

{diary_js}
"""

script_pos = html.find('<script>')
pos_planner_js = html.find('PLACEMENT PRODUCTIVITY WORKSPACE ENGINE', script_pos)
pos_dsa_js = html.find('DSA PATTERNS RENDERING', script_pos)

if pos_planner_js == -1 or pos_dsa_js == -1:
    print("ERROR: could not locate JS boundaries in script")
    exit(1)

js_start = html.rfind('/*', 0, pos_planner_js)
js_end = html.rfind('/*', 0, pos_dsa_js)

html = html[:js_start] + combined_js + "\n\n" + html[js_end:]
print("3. Injected combined Planner + Diary JS engines.")

# 4. Repair switchView routing so diary opens view-diary and planner opens view-planner
old_switch_target = "const target = document.getElementById(viewName === 'diary' ? 'view-planner' : ('view-' + viewName));"
new_switch_target = "const target = document.getElementById('view-' + viewName);"
if old_switch_target in html:
    html = html.replace(old_switch_target, new_switch_target, 1)
    print("4. Repaired switchView target to correctly route 'diary' to view-diary.")

# 5. Output to test_repaired.html
with open("test_repaired.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"SUCCESS: Saved test_repaired.html ({len(html)} bytes)")
