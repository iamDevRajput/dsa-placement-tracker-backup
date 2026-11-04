import re
import os

INDEX_PATH = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ==============================================================================
# 1. UPGRADE VIEW-MIK HTML
# ==============================================================================
view_start = html.find('<section class="view-section" id="view-mik">')
view_end = html.find('<!-- VIEW 3: REVISION CENTER -->')

if view_start != -1 and view_end != -1:
    upgraded_view_html = """<section class="view-section" id="view-mik">
      <!-- 1. HERO HEADER WITH DASHBOARD STATS -->
      <div class="mik-hero-header">
        <div class="mik-hero-left">
          <div class="mik-hero-badge">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            <span>PEDAGOGICAL DSA CURRICULUM</span>
          </div>
          <h1 class="mik-hero-title">MIK Interview DSA</h1>
          <p class="mik-hero-subtitle">
            1,526 curated problems across 23 topics with 4 complementary learning modes: Creator Playlists with exact video sequence, Striver-style Learning Roadmap, RisingBrain-style Pattern Explorer, and Original Repository structure.
          </p>
          <div class="mik-hero-attributions">
            <a href="https://github.com/MAZHARMIK/Interview_DS_Algo" target="_blank" rel="noopener noreferrer" class="mik-attribution-pill" title="View Mazhar's Original Repository">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
              <span>Source: MAZHARMIK / Interview_DS_Algo</span>
            </a>
            <a href="https://www.youtube.com/@codestorywithMIK" target="_blank" rel="noopener noreferrer" class="mik-attribution-pill" title="codestorywithMIK YouTube Channel">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="#ef4444"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span>YouTube: codestorywithMIK</span>
            </a>
          </div>
          <div class="mik-hero-actions">
            <button class="mik-action-btn primary" onclick="jumpToNextUnsolvedMikProblem()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <span>Resume Learning</span>
            </button>
            <button class="mik-action-btn" onclick="expandAllMikSubtopics(true)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="7 13 12 18 17 13"/><polyline points="7 6 12 11 17 6"/></svg>
              <span>Expand All</span>
            </button>
            <button class="mik-action-btn" onclick="expandAllMikSubtopics(false)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="17 11 12 6 7 11"/><polyline points="17 18 12 13 7 18"/></svg>
              <span>Collapse All</span>
            </button>
            <button class="mik-action-btn" onclick="resetAllMikFilters()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              <span>Reset Filters</span>
            </button>
          </div>
        </div>

        <div class="mik-hero-dashboard">
          <div class="mik-radial-gauge-container">
            <svg class="mik-radial-gauge" viewBox="0 0 100 100">
              <circle class="mik-gauge-bg" cx="50" cy="50" r="42" />
              <circle class="mik-gauge-fill" id="mikGaugeCircle" cx="50" cy="50" r="42" />
            </svg>
            <div class="mik-radial-content">
              <span class="mik-gauge-pct" id="mikRadialPct">0%</span>
              <span class="mik-gauge-label">Done</span>
            </div>
          </div>
          <div class="mik-metric-info">
            <div class="mik-metric-heading">Overall Solved</div>
            <div class="mik-metric-main-stat" id="mikHeaderSolvedCount">0 <span class="mik-metric-denom">/ 1526</span></div>
            <div class="mik-quick-chips">
              <span class="mik-quick-chip solved" id="mikChipSolved" title="Solved problems">🟢 0</span>
              <span class="mik-quick-chip inprogress" id="mikChipInProgress" title="In progress">🟡 0</span>
              <span class="mik-quick-chip revise" id="mikChipRevise" title="Needs revision">🟣 0</span>
              <span class="mik-quick-chip starred" id="mikChipStarred" title="Starred problems">⭐ 0</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. WORKSPACE 4-MODE SWITCHER TABS -->
      <div class="mik-mode-tabs-bar">
        <button class="mik-mode-tab active" id="mikModeTab-playlist" onclick="setMikMode('playlist')">
          <span class="mik-mode-icon">🎬</span>
          <span class="mik-mode-text">Creator Playlists</span>
          <span class="mik-mode-badge" id="mikModeBadgePlaylist">13 Verified</span>
        </button>
        <button class="mik-mode-tab" id="mikModeTab-roadmap" onclick="setMikMode('roadmap')">
          <span class="mik-mode-icon">🗺️</span>
          <span class="mik-mode-text">Learning Roadmap</span>
          <span class="mik-mode-badge">5 Stages</span>
        </button>
        <button class="mik-mode-tab" id="mikModeTab-pattern" onclick="setMikMode('pattern')">
          <span class="mik-mode-icon">🧩</span>
          <span class="mik-mode-text">Pattern Explorer</span>
          <span class="mik-mode-badge">30 Patterns</span>
        </button>
        <button class="mik-mode-tab" id="mikModeTab-repo" onclick="setMikMode('repo')">
          <span class="mik-mode-icon">📁</span>
          <span class="mik-mode-text">Original Repository</span>
          <span class="mik-mode-badge">23 Topics</span>
        </button>
      </div>

      <!-- 3. SEARCH & ADVANCED FILTER CONTROLS -->
      <div class="mik-controls-bar">
        <div class="mik-controls-top">
          <div class="mik-search-wrapper">
            <svg class="mik-search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input type="text" id="mikSearchInput" class="mik-search-input" placeholder="Search 1,526 problems, companies, approaches, patterns..." oninput="handleMikSearchInput(this.value)">
            <button id="mikSearchClearBtn" class="mik-search-clear" onclick="clearMikSearch()" title="Clear search" style="display:none;">&times;</button>
          </div>

          <div class="mik-filter-selects">
            <select class="form-select mik-select" id="mikTopicDropdown" onchange="setMikTopic(this.value)">
              <option value="all">📂 All 23 Topics</option>
            </select>

            <select class="form-select mik-select" id="mikCompanyDropdown" onchange="setMikCompany(this.value)">
              <option value="all">🏢 All Companies</option>
              <option value="Amazon">🛒 Amazon</option>
              <option value="Google">🔍 Google</option>
              <option value="Microsoft">🪟 Microsoft</option>
              <option value="Meta">👤 Meta</option>
              <option value="Adobe">🎨 Adobe</option>
              <option value="Apple">🍎 Apple</option>
              <option value="Flipkart">🛍️ Flipkart</option>
              <option value="Samsung">📱 Samsung</option>
              <option value="Uber">🚗 Uber</option>
              <option value="Goldman Sachs">🏦 Goldman Sachs</option>
              <option value="MakeMyTrip">✈️ MakeMyTrip</option>
              <option value="Paytm">💳 Paytm</option>
              <option value="LinkedIn">💼 LinkedIn</option>
              <option value="Twitter">🐦 Twitter</option>
              <option value="Oracle">💾 Oracle</option>
              <option value="Zoho">⚡ Zoho</option>
            </select>

            <select class="form-select mik-select" id="mikSortDropdown" onchange="setMikSort(this.value)">
              <option value="default">↕️ Default Ordering</option>
              <option value="playlist">🎬 Creator Playlist Order</option>
              <option value="roadmap">🗺️ Recommended Learning Order</option>
              <option value="pattern">🧩 Pattern Grouping</option>
              <option value="repo">📁 Original Repo Order</option>
              <option value="alpha">🔤 Alphabetical (A-Z)</option>
            </select>
          </div>
        </div>

        <div class="mik-filter-pills-row">
          <div class="mik-pill-group">
            <button class="mik-pill active" id="f-mik-all" onclick="setMikStatusFilter('all', this)">All <span class="mik-badge-num" id="mikPillAllCnt">1526</span></button>
            <button class="mik-pill" id="f-mik-solved" onclick="setMikStatusFilter('solved', this)">🟢 Solved <span class="mik-badge-num" id="mikPillSolvedCnt">0</span></button>
            <button class="mik-pill" id="f-mik-inprogress" onclick="setMikStatusFilter('inprogress', this)">🟡 In Progress <span class="mik-badge-num" id="mikPillInProgCnt">0</span></button>
            <button class="mik-pill" id="f-mik-revise" onclick="setMikStatusFilter('revise', this)">🟣 Needs Revise <span class="mik-badge-num" id="mikPillReviseCnt">0</span></button>
            <button class="mik-pill" id="f-mik-unsolved" onclick="setMikStatusFilter('unsolved', this)">Unattempted</button>
            <button class="mik-pill" id="f-mik-starred" onclick="setMikStatusFilter('starred', this)">⭐ Starred <span class="mik-badge-num" id="mikPillStarredCnt">0</span></button>
            <button class="mik-pill" id="f-mik-notes" onclick="setMikStatusFilter('notes', this)">📝 With Notes <span class="mik-badge-num" id="mikPillNotesCnt">0</span></button>
          </div>
        </div>
      </div>

      <!-- 4. MAIN WORKSPACE: SIDEBAR & DYNAMIC CONTENT -->
      <div class="mik-main-workspace">
        <aside class="mik-topic-sidebar" id="mikTopicNavSidebar">
          <!-- Populated dynamically based on active mode -->
        </aside>

        <div class="mik-content-area" id="mikContentArea">
          <!-- Populated dynamically based on active mode -->
        </div>
      </div>
    </section>
"""
    html = html[:view_start] + upgraded_view_html + "\n\n    " + html[view_end:]
    print("Replaced view-mik HTML with 4-mode workspace HTML")

# ==============================================================================
# 2. UPGRADE MODAL TO INCLUDE PLAYLIST PREV/NEXT NAVIGATOR
# ==============================================================================
modal_nav_placeholder = '<div class="mik-modal-header">'
upgraded_modal_nav = """<!-- Playlist Context Navigator -->
    <div class="mik-modal-playlist-nav" id="mikModalPlaylistNav" style="display:none;">
      <button class="mik-nav-step-btn" id="mikModalPrevVideoBtn" onclick="prevMikPlaylistVideo()">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="19 20 9 12 19 4 19 20"/><line x1="5" y1="19" x2="5" y2="5"/></svg>
        <span>Previous Video</span>
      </button>
      <span style="font-weight:600; color:var(--text); text-align:center;" id="mikModalPlaylistNavLabel">Video 1 of 50</span>
      <button class="mik-nav-step-btn" id="mikModalNextVideoBtn" onclick="nextMikPlaylistVideo()">
        <span>Next Video</span>
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 4 15 12 5 20 5 4"/><line x1="19" y1="5" x2="19" y2="19"/></svg>
      </button>
    </div>

    <div class="mik-modal-header">"""

if 'id="mikModalPlaylistNav"' not in html:
    html = html.replace(modal_nav_placeholder, upgraded_modal_nav, 1)
    print("Added Playlist Context Navigator to modal")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated index.html with HTML changes")
