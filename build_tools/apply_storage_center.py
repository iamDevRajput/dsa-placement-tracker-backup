import os

SOURCE_HTML = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"
CSS_FILE = "/Users/devrajput/@Resources/Tracker/build_tools/storage_center.css"
JS_FILE = "/Users/devrajput/@Resources/Tracker/build_tools/storage_center.js"
UI_FILE = "/Users/devrajput/@Resources/Tracker/build_tools/storage_center_ui.html"

with open(SOURCE_HTML, "r", encoding="utf-8") as f:
    html = f.read()

with open(CSS_FILE, "r", encoding="utf-8") as f:
    sc_css = f.read()

with open(JS_FILE, "r", encoding="utf-8") as f:
    sc_js = f.read()

with open(UI_FILE, "r", encoding="utf-8") as f:
    sc_ui = f.read()

print(f"Original index.html size: {len(html)} bytes")

# 1. SPLIT UI AND MODALS
modal_marker = "<!-- BACKUP DOWNLOAD VERIFICATION MODAL -->"
assert modal_marker in sc_ui, "Modal marker missing in UI file"
main_ui_part, modals_part = sc_ui.split(modal_marker, 1)
modals_part = modal_marker + "\n\n" + modals_part.strip()

# 2. UI REPLACEMENT
ui_start = html.find('<!-- DATA & STORAGE CENTER MAIN SECTION -->')
ui_end_marker = '      <div class="settings-group">\n        <h3 style="font-family:var(--font-heading); font-size:18px; margin-bottom:1rem;">⚙️ Spaced Repetition Configuration</h3>'
ui_end = html.find(ui_end_marker, ui_start)
assert ui_start != -1 and ui_end != -1, "UI slice not found"

replacement_ui = main_ui_part.strip() + """\n      <div style="margin-top:-0.5rem; margin-bottom:1.5rem; display:flex; justify-content:flex-end;">
        <button class="btn btn-secondary btn-sm" onclick="exportDiary('md')" title="Export diary journal in markdown">📓 Export Placement Diary (Markdown)</button>
      </div>\n\n"""

html = html[:ui_start] + replacement_ui + html[ui_end:]
print("✓ Updated Data & Storage Center UI")

# 3. MODALS REPLACEMENT
# Check if modal starts with modal_marker or upgraded restore
if '<!-- BACKUP DOWNLOAD VERIFICATION MODAL -->' in html:
    modal_start = html.find('<!-- BACKUP DOWNLOAD VERIFICATION MODAL -->')
else:
    modal_start = html.find('<!-- UPGRADED RESTORE BACKUP MODAL -->')

modal_end = html.find('<!-- IMPORT CONFIRMATION MODAL -->', modal_start)
assert modal_start != -1 and modal_end != -1, "Modal slice not found"

html = html[:modal_start] + modals_part + "\n\n" + html[modal_end:]
print("✓ Updated Modals (Download Verification + Restore Checklist)")

# 4. JS REPLACEMENT
js_start = html.find('/* ==========================================================================\n   SETTINGS, DATA & STORAGE CENTER, EXPORT, IMPORT & BACKUP')
js_end = html.find('function saveIntervalSettings()', js_start)
assert js_start != -1 and js_end != -1, "JS slice not found"

replacement_js = "/* ==========================================================================\n   SETTINGS, DATA & STORAGE CENTER, EXPORT, IMPORT & BACKUP\n   ========================================================================== */\n" + sc_js.strip() + "\n\n"

html = html[:js_start] + replacement_js + html[js_end:]
print("✓ Updated Storage Center JS Engine")

# Save updated HTML
with open(SOURCE_HTML, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nSuccessfully updated {SOURCE_HTML} (New size: {len(html)} bytes)")
