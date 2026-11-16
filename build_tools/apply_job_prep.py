#!/usr/bin/env python3
"""
Apply Job Preparation Tracker to dsa-placement-dashboard/index.html
"""

import os
import sys
import shutil

ROOT_DIR = '/Users/devrajput/@Resources/Tracker'
DASHBOARD_DIR = os.path.join(ROOT_DIR, 'dsa-placement-dashboard')
INDEX_PATH = os.path.join(DASHBOARD_DIR, 'index.html')
BUILD_TOOLS = os.path.join(ROOT_DIR, 'build_tools')

CSS_PATH = os.path.join(BUILD_TOOLS, 'job_prep_tracker.css')
DATA_PATH = os.path.join(BUILD_TOOLS, 'job_prep_tracker_data.js')
JS_PATH = os.path.join(BUILD_TOOLS, 'job_prep_tracker.js')

def main():
    if not os.path.exists(INDEX_PATH):
        print(f"Error: {INDEX_PATH} not found.")
        sys.exit(1)

    with open(CSS_PATH, 'r', encoding='utf-8') as f:
        css_content = f.read()

    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data_content = f.read()

    with open(JS_PATH, 'r', encoding='utf-8') as f:
        js_content = f.read()

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # Backup if not already backed up
    bak_path = os.path.join(BUILD_TOOLS, 'index.html.pre_jobprep_bak')
    if not os.path.exists(bak_path):
        with open(bak_path, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Created backup at {bak_path}")

    # 1. Inject CSS before </head>
    css_injection = f"\n<style id=\"job-prep-tracker-styles\">\n{css_content}\n</style>\n"
    if 'id="job-prep-tracker-styles"' in html:
        # replace existing
        import re
        html = re.sub(r'<style id="job-prep-tracker-styles">.*?</style>', css_injection.strip(), html, flags=re.DOTALL)
        print("Updated existing job-prep-tracker-styles.")
    else:
        html = html.replace('</head>', f"{css_injection}</head>")
        print("Injected job-prep-tracker-styles into <head>.")

    # 2. Inject Data and JS Engine before </body>
    scripts_injection = f"""
<!-- ==========================================================================
     JOB PREPARATION TRACKER SCRIPTS
     ========================================================================== -->
<script id="job-prep-tracker-data">
{data_content}
</script>
<script id="job-prep-tracker-engine">
{js_content}
</script>
"""
    if 'id="job-prep-tracker-engine"' in html:
        import re
        html = re.sub(r'<script id="job-prep-tracker-data">.*?</script>\s*<script id="job-prep-tracker-engine">.*?</script>', 
                      f'<script id="job-prep-tracker-data">\n{data_content}\n</script>\n<script id="job-prep-tracker-engine">\n{js_content}\n</script>',
                      html, flags=re.DOTALL)
        print("Updated existing job-prep-tracker scripts.")
    else:
        html = html.replace('</body>', f"{scripts_injection}\n</body>")
        print("Injected job-prep-tracker scripts before </body>.")

    # 3. Sidebar Navigation Button
    nav_btn_html = """    <button class="nav-item" onclick="switchView('jobprep', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
      <span>Job Prep Tracker</span>
      <span class="nav-badge" style="background:rgba(245,158,11,0.15); color:#f59e0b; border:1px solid rgba(245,158,11,0.3);" id="nav-jobprep-badge">0%</span>
    </button>"""

    if "switchView('jobprep', this)" not in html:
        # Locate resources button and place jobprep immediately after it
        target_marker = "</button>\n<button class=\"nav-item\" onclick=\"switchView('revisions', this)\">"
        alt_marker = "</button>\n    <button class=\"nav-item\" onclick=\"switchView('revisions', this)\">"
        
        # Check resources nav button
        import re
        res_pattern = r'(<button class="nav-item" onclick="switchView\(\'resources\', this\)">.*?</button>)'
        match = re.search(res_pattern, html, re.DOTALL)
        if match:
            old_res_btn = match.group(1)
            new_res_btn = f"{old_res_btn}\n{nav_btn_html}"
            html = html.replace(old_res_btn, new_res_btn, 1)
            print("Injected Job Prep Tracker button into sidebar nav after Resources.")
        else:
            print("Warning: Could not find Resources nav item in sidebar.")

    # 4. View Container Section
    view_section_html = """<!-- JOB PREPARATION TRACKER VIEW -->
<section class="view-section" id="view-jobprep">
  <!-- Populated by window.renderJobPrepView() -->
</section>
"""
    if 'id="view-jobprep"' not in html:
        res_view_marker = '<section class="view-section" id="view-revisions">'
        if res_view_marker in html:
            html = html.replace(res_view_marker, f"{view_section_html}\n{res_view_marker}", 1)
            print("Injected view-jobprep section right before view-revisions.")
        else:
            print("Warning: Could not find view-revisions marker to place view-jobprep.")

    # 5. Update switchView function
    if "jobprep: 'Job Preparation Command Center (10 Weeks)'" not in html:
        html = html.replace(
            "resources: 'Placement Preparation Resource Library',",
            "resources: 'Placement Preparation Resource Library',\n    jobprep: 'Job Preparation Command Center (10 Weeks)',"
        )
        print("Added jobprep to titleMap in switchView.")

    if "else if(viewName === 'jobprep')" not in html:
        html = html.replace(
            "else if(viewName === 'resources') renderResourcesView();",
            "else if(viewName === 'resources') renderResourcesView();\n  else if(viewName === 'jobprep') {\n    if (typeof renderJobPrepView === 'function') renderJobPrepView();\n  }"
        )
        print("Added viewName === 'jobprep' handler in switchView.")

    # 6. DASHBOARD_STORAGE_KEY_MAP integration
    if "'job_prep_tracker_v1':" not in html:
        html = html.replace(
            "'skills_learning_hub_v1': { name: 'Skills Learning Hub', cat: 'Skills Hub', desc: 'Learning tracks, completed lessons and lesson notes' },",
            "'skills_learning_hub_v1': { name: 'Skills Learning Hub', cat: 'Skills Hub', desc: 'Learning tracks, completed lessons and lesson notes' },\n  'job_prep_tracker_v1': { name: 'Job Prep Tracker (10 Weeks)', cat: 'Job Prep', desc: 'Eligibility, 3 hiring rounds, 35 quants, 10 verbal, 19 reasoning, 8+3 wks DSA, 6 tech categories, and daily 5h study log' },"
        )
        print("Added job_prep_tracker_v1 to DASHBOARD_STORAGE_KEY_MAP.")

    # 7. buildComprehensiveBackupBundle integration
    if "'jobPrepTracker'" not in html:
        html = html.replace(
            "'diary', 'planner', 'studyLogs', 'settings', 'motivation', 'personalNotes'",
            "'diary', 'planner', 'studyLogs', 'settings', 'motivation', 'personalNotes', 'jobPrepTracker'"
        )
        print("Added jobPrepTracker to manifest categories.")

    if "jobPrepTracker:" not in html:
        target_cat = "personalNotes: localStorage.getItem(MP_STORAGE_KEY_NOTE) || ''\n    },"
        replacement_cat = """personalNotes: localStorage.getItem(MP_STORAGE_KEY_NOTE) || '',
      jobPrepTracker: (typeof window !== 'undefined' && window.jobPrepState) ? window.jobPrepState : (JSON.parse(localStorage.getItem('job_prep_tracker_v1') || 'null'))
    },"""
        html = html.replace(target_cat, replacement_cat, 1)
        print("Added jobPrepTracker to categories in buildComprehensiveBackupBundle.")

    if "jobPrepState:" not in html:
        target_top = "routineTemplates: typeof routineTemplates !== 'undefined' ? routineTemplates : null\n  };"
        replacement_top = """routineTemplates: typeof routineTemplates !== 'undefined' ? routineTemplates : null,
    jobPrepState: (typeof window !== 'undefined' && window.jobPrepState) ? window.jobPrepState : (JSON.parse(localStorage.getItem('job_prep_tracker_v1') || 'null'))
  };"""
        html = html.replace(target_top, replacement_top, 1)
        print("Added jobPrepState to backwards-compatible top keys in backup bundle.")

    # 8. renderRestoreCategoryChecklist integration
    if "const jobPrepData = parsed.categories?.jobPrepTracker" not in html:
        target_p = "const diaryData = parsed.categories?.dailyWorkspace?.diary || parsed.diaryState;"
        replacement_p = f"{target_p}\n  const jobPrepData = parsed.categories?.jobPrepTracker || parsed.jobPrepState;"
        html = html.replace(target_p, replacement_p, 1)

        target_cats = "{ id: 'cat_motivation', label: 'Motivation Library', desc: 'Custom quotes & resources', present: !!motivationData }\n  ];"
        replacement_cats = """{ id: 'cat_motivation', label: 'Motivation Library', desc: 'Custom quotes & resources', present: !!motivationData },
    { id: 'cat_jobprep', label: 'Job Prep Tracker (10 Weeks)', desc: 'Roadmap, 35 quants, 8+3 wks DSA, tech categories & daily study logs', present: !!jobPrepData }
  ];"""
        html = html.replace(target_cats, replacement_cats, 1)
        print("Added cat_jobprep to renderRestoreCategoryChecklist.")

    # 9. executeDataCenterRestoreConfirmed integration
    if "const cbJobPrep = document.getElementById('scRestore_cat_jobprep');" not in html:
        target_restore = "// 12. Personal Notes"
        jobprep_restore_logic = """    // 11b. Job Prep Tracker
    const cbJobPrep = document.getElementById('scRestore_cat_jobprep');
    if (cbJobPrep && cbJobPrep.checked) {
      const jpData = parsed.categories?.jobPrepTracker || parsed.jobPrepState;
      if (jpData) {
        localStorage.setItem('job_prep_tracker_v1', JSON.stringify(jpData));
        window.jobPrepState = jpData;
        if (typeof updateJobPrepSidebarBadge === 'function') updateJobPrepSidebarBadge();
        if (typeof renderJobPrepView === 'function' && document.getElementById('view-jobprep')?.classList.contains('active')) renderJobPrepView();
        restoredCount++;
      }
    }

    // 12. Personal Notes"""
        html = html.replace(target_restore, jobprep_restore_logic, 1)
        print("Added Job Prep Tracker handling in executeDataCenterRestoreConfirmed.")

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Successfully applied Job Prep Tracker to index.html!")

if __name__ == '__main__':
    main()

