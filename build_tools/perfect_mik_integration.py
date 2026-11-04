import os
import re

INDEX_PATH = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ------------------------------------------------------------------------------
# 1. HEAD SCRIPT TAGS
# ------------------------------------------------------------------------------
head_scripts = """  <script src="data/mik_catalog.js"></script>
  <script src="data/mik_playlists.js"></script>
  <script src="data/mik_learning_order.js"></script>
  <script src="data/mik_patterns.js"></script>"""

if '<script src="data/mik_playlists.js"></script>' not in html:
    html = html.replace('<script src="data/mik_catalog.js"></script>', head_scripts)

# ------------------------------------------------------------------------------
# 2. PROPERLY SCOPED DARK THEME CSS
# ------------------------------------------------------------------------------
css_start = html.find("/* ==========================================================================\n   MIK INTERVIEW DSA SECTION STYLING")
css_end = html.find("</style>", css_start)

if css_start == -1 or css_end == -1:
    print(f"Error finding CSS markers: css_start={css_start}, css_end={css_end}")
    exit(1)

dark_mik_css = """/* ==========================================================================
   MIK INTERVIEW DSA SECTION STYLING (PERFECT DARK THEME SYSTEM)
   ========================================================================== */

#view-mik {
  color: #f8fafc;
}

/* Hero Header */
.mik-hero-header {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  gap: 1.5rem;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(15, 23, 42, 0.75) 100%);
  border: 1px solid rgba(239, 68, 68, 0.28);
  border-radius: 16px;
  padding: 1.75rem 2rem;
  margin-bottom: 1.25rem;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(14px);
}

.mik-hero-header::before {
  content: '';
  position: absolute;
  top: -60px;
  right: -60px;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(239, 68, 68, 0.2) 0%, transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

.mik-hero-left {
  flex: 1;
  max-width: 680px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.mik-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(239, 68, 68, 0.15);
  border: 1px solid rgba(239, 68, 68, 0.35);
  padding: 0.3rem 0.8rem;
  border-radius: 9999px;
  font-size: 11.5px;
  font-weight: 700;
  color: #f87171;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
  width: fit-content;
}

.mik-hero-title {
  font-size: 1.85rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: #ffffff !important;
  margin-bottom: 0.4rem;
}

.mik-hero-subtitle {
  font-size: 13.5px;
  color: #94a3b8 !important;
  line-height: 1.55;
  margin-bottom: 1rem;
}

.mik-hero-attributions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

a.mik-attribution-pill {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.45rem !important;
  padding: 0.3rem 0.75rem !important;
  background: rgba(30, 41, 59, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 6px !important;
  font-size: 11.5px !important;
  color: #cbd5e1 !important;
  text-decoration: none !important;
  transition: all 0.15s ease !important;
}

a.mik-attribution-pill span {
  color: #cbd5e1 !important;
  text-decoration: none !important;
}

a.mik-attribution-pill:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
}

a.mik-attribution-pill:hover span {
  color: #ffffff !important;
}

.mik-hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  align-items: center;
}

button.mik-action-btn,
a.mik-action-btn {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.45rem !important;
  padding: 0.45rem 0.95rem !important;
  border-radius: 6px !important;
  font-size: 12.5px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  background: rgba(30, 41, 59, 0.7) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  color: #e2e8f0 !important;
  text-decoration: none !important;
  transition: all 0.15s ease !important;
}

button.mik-action-btn span,
a.mik-action-btn span {
  color: inherit !important;
  text-decoration: none !important;
}

button.mik-action-btn:hover,
a.mik-action-btn:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
}

button.mik-action-btn.primary,
a.mik-action-btn.primary {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  border-color: #ef4444 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35) !important;
}

button.mik-action-btn.primary:hover,
a.mik-action-btn.primary:hover {
  box-shadow: 0 6px 18px rgba(239, 68, 68, 0.5) !important;
  transform: translateY(-1px) !important;
}

.mik-hero-dashboard {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 1rem 1.5rem;
}

.mik-radial-gauge-container {
  position: relative;
  width: 90px;
  height: 90px;
  flex-shrink: 0;
}

.mik-radial-gauge {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

.mik-gauge-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.08);
  stroke-width: 8;
}

.mik-gauge-fill {
  fill: none;
  stroke: #ef4444;
  stroke-width: 8;
  stroke-linecap: round;
  stroke-dasharray: 263.89;
  stroke-dashoffset: 263.89;
  transition: stroke-dashoffset 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.mik-radial-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  display: flex;
  flex-direction: column;
}

.mik-gauge-pct {
  font-size: 1.25rem;
  font-weight: 800;
  color: #ffffff !important;
}

.mik-gauge-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8 !important;
}

.mik-metric-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.mik-metric-heading {
  font-size: 11.5px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8 !important;
}

.mik-metric-main-stat {
  font-size: 1.75rem;
  font-weight: 800;
  color: #ffffff !important;
  line-height: 1.1;
}

.mik-metric-denom {
  font-size: 13px;
  font-weight: 500;
  color: #94a3b8 !important;
}

.mik-quick-chips {
  display: flex;
  gap: 0.4rem;
  margin-top: 0.35rem;
}

.mik-quick-chip {
  font-size: 11px;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* 5-Mode Switcher Tabs */
.mik-mode-tabs-bar {
  display: flex;
  gap: 0.45rem;
  background: rgba(15, 23, 42, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 0.4rem;
  margin-bottom: 1.25rem;
  overflow-x: auto;
}

button.mik-mode-tab {
  flex: 1;
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 0.5rem !important;
  padding: 0.65rem 0.95rem !important;
  border-radius: 8px !important;
  border: 1px solid transparent !important;
  background: transparent !important;
  color: #94a3b8 !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  transition: all 0.15s ease !important;
}

button.mik-mode-tab:hover {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.06) !important;
}

button.mik-mode-tab.active {
  background: rgba(239, 68, 68, 0.18) !important;
  border-color: rgba(239, 68, 68, 0.45) !important;
  color: #ffffff !important;
  box-shadow: 0 2px 10px rgba(239, 68, 68, 0.25) !important;
}

.mik-mode-badge {
  font-size: 10.5px;
  padding: 0.1rem 0.45rem;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.08);
  color: #94a3b8;
}

button.mik-mode-tab.active .mik-mode-badge {
  background: rgba(239, 68, 68, 0.35);
  color: #fca5a5;
}

/* Controls Bar */
.mik-controls-bar {
  background: rgba(15, 23, 42, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 12px;
  padding: 0.9rem 1.1rem;
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.mik-controls-top {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.mik-search-wrapper {
  flex: 1;
  min-width: 240px;
  position: relative;
  display: flex;
  align-items: center;
}

.mik-search-icon {
  position: absolute;
  left: 0.85rem;
  color: #64748b;
  pointer-events: none;
}

.mik-search-input {
  width: 100%;
  padding: 0.55rem 2.2rem 0.55rem 2.3rem;
  background: rgba(15, 23, 42, 0.7) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 6px !important;
  color: #f8fafc !important;
  font-size: 13px !important;
  outline: none;
  transition: all 0.15s ease;
}

.mik-search-input:focus {
  border-color: rgba(239, 68, 68, 0.55) !important;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15) !important;
}

.mik-search-clear {
  position: absolute;
  right: 0.6rem;
  background: none;
  border: none;
  color: #64748b;
  cursor: pointer;
  font-size: 15px;
  padding: 0.2rem;
}

.mik-filter-selects {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

select.mik-select {
  padding: 0.5rem 1.75rem 0.5rem 0.75rem !important;
  background-color: #0f172a !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 6px !important;
  color: #f8fafc !important;
  font-size: 12.5px !important;
  outline: none !important;
  cursor: pointer !important;
}

select.mik-select option {
  background-color: #0f172a !important;
  color: #f8fafc !important;
}

.mik-filter-pills-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.mik-pill-group {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
}

button.mik-pill {
  padding: 0.32rem 0.7rem !important;
  border-radius: 6px !important;
  background: rgba(30, 41, 59, 0.5) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: #94a3b8 !important;
  font-size: 12px !important;
  cursor: pointer !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.35rem !important;
  transition: all 0.15s ease !important;
}

button.mik-pill:hover {
  background: rgba(255, 255, 255, 0.08) !important;
  color: #ffffff !important;
}

button.mik-pill.active {
  background: rgba(239, 68, 68, 0.18) !important;
  border-color: rgba(239, 68, 68, 0.4) !important;
  color: #ffffff !important;
  font-weight: 600 !important;
}

/* Main Workspace */
.mik-main-workspace {
  display: grid;
  grid-template-columns: 290px 1fr;
  gap: 1.25rem;
  align-items: start;
}

@media (max-width: 1024px) {
  .mik-main-workspace {
    grid-template-columns: 1fr;
  }
}

.mik-topic-sidebar {
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 12px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
  position: sticky;
  top: 80px;
  max-height: calc(100vh - 100px);
  overflow-y: auto;
}

.mik-sidebar-heading {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #94a3b8 !important;
  padding: 0.35rem 0.5rem;
  margin-top: 0.25rem;
}

button.mik-topic-nav-btn {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 0.5rem !important;
  padding: 0.55rem 0.75rem !important;
  border-radius: 6px !important;
  background: transparent !important;
  border: 1px solid transparent !important;
  color: #cbd5e1 !important;
  font-size: 12.5px !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  text-align: left !important;
  transition: all 0.15s ease !important;
  width: 100% !important;
}

button.mik-topic-nav-btn:hover {
  background: rgba(255, 255, 255, 0.06) !important;
  color: #ffffff !important;
}

button.mik-topic-nav-btn.active {
  background: rgba(239, 68, 68, 0.16) !important;
  border-color: rgba(239, 68, 68, 0.35) !important;
  color: #ffffff !important;
  font-weight: 600 !important;
}

.mik-topic-nav-badge {
  font-size: 11px;
  font-family: monospace;
  color: #94a3b8;
  background: rgba(255, 255, 255, 0.05);
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
}

button.mik-topic-nav-btn.active .mik-topic-nav-badge {
  color: #fca5a5;
  background: rgba(239, 68, 68, 0.25);
}

/* Content Area */
.mik-content-area {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  min-width: 0;
}

/* Playlist Banner Card */
.mik-playlist-banner {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.09) 0%, rgba(30, 41, 59, 0.65) 100%);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: 12px;
  padding: 1.35rem 1.6rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.mik-playlist-banner-left {
  flex: 1;
  min-width: 280px;
}

.mik-playlist-banner-title {
  font-size: 1.35rem;
  font-weight: 800;
  color: #ffffff !important;
  margin-bottom: 0.35rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.mik-playlist-banner-desc {
  font-size: 12.5px;
  color: #94a3b8 !important;
  line-height: 1.5;
  margin-bottom: 0.6rem;
}

.mik-playlist-progress-bar-wrap {
  background: rgba(255, 255, 255, 0.08);
  height: 6px;
  border-radius: 3px;
  overflow: hidden;
  margin-top: 0.5rem;
  max-width: 380px;
}

.mik-playlist-progress-bar {
  background: linear-gradient(90deg, #ef4444, #f87171);
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}

/* Cards (Stages, Patterns, Subtopics) */
.mik-stage-card,
.mik-pattern-card,
.mik-subtopic-card {
  background: rgba(15, 23, 42, 0.5) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
}

.mik-stage-header,
.mik-pattern-header,
.mik-subtopic-header {
  padding: 0.85rem 1.15rem !important;
  background: rgba(30, 41, 59, 0.4) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  cursor: pointer !important;
  user-select: none !important;
}

.mik-stage-header:hover,
.mik-pattern-header:hover,
.mik-subtopic-header:hover {
  background: rgba(255, 255, 255, 0.04) !important;
}

.mik-stage-title,
.mik-pattern-title,
.mik-subtopic-title {
  font-size: 13.5px !important;
  font-weight: 700 !important;
  color: #ffffff !important;
  display: flex !important;
  align-items: center !important;
  gap: 0.5rem !important;
}

.mik-stage-desc,
.mik-pattern-desc {
  font-size: 12px;
  color: #94a3b8 !important;
  margin-top: 0.15rem;
}

.mik-stage-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

/* Problem List & Row */
.mik-prob-list {
  display: flex;
  flex-direction: column;
}

.mik-prob-row {
  display: grid !important;
  grid-template-columns: 50px minmax(200px, 1fr) auto 130px 36px 36px !important;
  align-items: center !important;
  gap: 0.75rem !important;
  padding: 0.65rem 1rem !important;
  border-top: 1px solid rgba(255, 255, 255, 0.04) !important;
  background: rgba(15, 23, 42, 0.3) !important;
  transition: background 0.15s ease !important;
}

.mik-prob-row:hover {
  background: rgba(255, 255, 255, 0.04) !important;
}

.mik-prob-row.solved {
  background: rgba(16, 185, 129, 0.04) !important;
}

@media (max-width: 900px) {
  .mik-prob-row {
    grid-template-columns: 40px 1fr auto auto !important;
    row-gap: 0.5rem !important;
  }
}

.mik-prob-seq {
  font-size: 12px !important;
  font-family: monospace !important;
  font-weight: 700 !important;
  color: #94a3b8 !important;
}

.mik-prob-seq.playlist-seq {
  color: #f87171 !important;
}

.mik-prob-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.mik-prob-title-link {
  color: #f8fafc !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
  white-space: nowrap !important;
  overflow: hidden !important;
  text-overflow: ellipsis !important;
}

.mik-prob-title-link:hover {
  color: #ef4444 !important;
}

.mik-prob-tags {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
  align-items: center;
}

.mik-tag {
  font-size: 10.5px !important;
  padding: 0.1rem 0.4rem !important;
  border-radius: 4px !important;
  background: rgba(255, 255, 255, 0.05) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  color: #94a3b8 !important;
  white-space: nowrap !important;
}

.mik-tag.company {
  color: #38bdf8 !important;
  background: rgba(56, 189, 248, 0.09) !important;
  border-color: rgba(56, 189, 248, 0.22) !important;
}

.mik-tag.tc {
  font-family: monospace !important;
  color: #fbbf24 !important;
  background: rgba(251, 191, 36, 0.09) !important;
  border-color: rgba(251, 191, 36, 0.22) !important;
}

.mik-links-group {
  display: flex;
  gap: 0.35rem;
  align-items: center;
}

a.mik-link-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  width: 26px !important;
  height: 26px !important;
  border-radius: 6px !important;
  background: rgba(30, 41, 59, 0.6) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #cbd5e1 !important;
  text-decoration: none !important;
  font-size: 12px !important;
  transition: all 0.15s ease !important;
}

a.mik-link-btn:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  color: #ffffff !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
}

a.mik-link-btn.yt:hover {
  color: #ef4444 !important;
  border-color: rgba(239, 68, 68, 0.45) !important;
}

a.mik-link-btn.lc:hover {
  color: #f59e0b !important;
  border-color: rgba(245, 158, 11, 0.45) !important;
}

select.mik-status-dropdown {
  padding: 0.3rem 0.55rem !important;
  font-size: 11.5px !important;
  font-weight: 600 !important;
  border-radius: 6px !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  background-color: #0f172a !important;
  color: #f8fafc !important;
  cursor: pointer !important;
  outline: none !important;
}

select.mik-status-dropdown.status-SOLVED {
  background: rgba(16, 185, 129, 0.15) !important;
  border-color: rgba(16, 185, 129, 0.4) !important;
  color: #34d399 !important;
}

select.mik-status-dropdown.status-IN_PROGRESS {
  background: rgba(245, 158, 11, 0.15) !important;
  border-color: rgba(245, 158, 11, 0.4) !important;
  color: #fbbf24 !important;
}

select.mik-status-dropdown.status-REVISE {
  background: rgba(168, 85, 247, 0.15) !important;
  border-color: rgba(168, 85, 247, 0.4) !important;
  color: #c084fc !important;
}

button.mik-notes-indicator-btn {
  background: transparent !important;
  border: none !important;
  color: #94a3b8 !important;
  cursor: pointer !important;
  font-size: 14px !important;
  padding: 0.25rem !important;
  border-radius: 4px !important;
}

button.mik-notes-indicator-btn:hover {
  background: rgba(255, 255, 255, 0.08) !important;
  color: #ffffff !important;
}

button.mik-notes-indicator-btn.has-notes {
  color: #38bdf8 !important;
}

button.mik-star-toggle-btn {
  background: transparent !important;
  border: none !important;
  color: #64748b !important;
  cursor: pointer !important;
  font-size: 15px !important;
  padding: 0.2rem !important;
}

button.mik-star-toggle-btn:hover {
  color: #f59e0b !important;
}

button.mik-star-toggle-btn.starred {
  color: #fbbf24 !important;
}

/* Unmatched Card */
.mik-unmatched-card {
  margin-top: 1rem;
  background: rgba(245, 158, 11, 0.06);
  border: 1px dashed rgba(245, 158, 11, 0.35);
  border-radius: 10px;
  padding: 0.85rem 1.15rem;
}

.mik-unmatched-header {
  font-size: 13px;
  font-weight: 700;
  color: #fbbf24 !important;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

/* Modal Enhancements */
.mik-modal-card {
  background: #0f172a !important;
  border: 1px solid rgba(239, 68, 68, 0.3) !important;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.8), 0 0 20px rgba(239, 68, 68, 0.15) !important;
  border-radius: 14px !important;
  max-width: 680px !important;
  width: 90% !important;
  max-height: 90vh !important;
  overflow-y: auto !important;
  padding: 1.5rem !important;
}

.mik-modal-playlist-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.65rem 0.95rem;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 12px;
}

button.mik-nav-step-btn {
  display: inline-flex !important;
  align-items: center !important;
  gap: 0.4rem !important;
  padding: 0.35rem 0.75rem !important;
  background: rgba(30, 41, 59, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.15) !important;
  border-radius: 6px !important;
  color: #f8fafc !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  cursor: pointer !important;
}

button.mik-nav-step-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.15) !important;
}

button.mik-nav-step-btn:disabled {
  opacity: 0.35 !important;
  cursor: not-allowed !important;
}

.mik-notes-textarea {
  width: 100%;
  min-height: 140px;
  padding: 0.75rem;
  background: rgba(15, 23, 42, 0.8) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  border-radius: 6px !important;
  color: #f8fafc !important;
  font-size: 13px !important;
  line-height: 1.5 !important;
  font-family: var(--font-mono, monospace) !important;
  outline: none !important;
}

.mik-notes-textarea:focus {
  border-color: rgba(239, 68, 68, 0.5) !important;
}

/* Pagination bar for All Problems mode */
.mik-pagination-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 8px;
  margin-top: 1rem;
  font-size: 12.5px;
  color: #94a3b8;
}

.mik-pagination-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}
"""

html = html[:css_start] + dark_mik_css + "\n" + html[css_end:]

# ------------------------------------------------------------------------------
# 3. HTML MODE TABS (Adding 5th Tab: All Problems)
# ------------------------------------------------------------------------------
old_tabs_bar = html.find('<div class="mik-mode-tabs-bar">')
tabs_end = html.find('</div>', old_tabs_bar) + 6

new_tabs_html = """<div class="mik-mode-tabs-bar">
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
        <button class="mik-mode-tab" id="mikModeTab-all" onclick="setMikMode('all')">
          <span class="mik-mode-icon">📚</span>
          <span class="mik-mode-text">All Problems</span>
          <span class="mik-mode-badge">1,526</span>
        </button>
      </div>"""

if old_tabs_bar != -1:
    html = html[:old_tabs_bar] + new_tabs_html + html[tabs_end:]

# ------------------------------------------------------------------------------
# 4. JAVASCRIPT ENGINE (FULLY SYNCHRONIZED SELECTIONS + ALL PROBLEMS VIEW)
# ------------------------------------------------------------------------------
js_start = html.find('/* ==========================================================================\n   MIK INTERVIEW DSA STATE & ENGINE')
js_end = html.find('function switchView(viewName, navEl) {')

if js_start == -1 or js_end == -1:
    print(f"Error finding JS markers: js_start={js_start}, js_end={js_end}")
    exit(1)

upgraded_js = """/* ==========================================================================
   MIK INTERVIEW DSA STATE & ENGINE (FULLY SYNCHRONIZED 5-MODE WORKSPACE)
   ========================================================================== */
const STORAGE_MIK_KEY = 'mik_interview_dsa_tracker_v1';

let mikState = {
  version: 1,
  problems: {},
  collapsedTopics: {},
  collapsedSubtopics: {},
  currentMode: 'playlist',
  activePlaylistId: 'PLpIkg8OmuX-LkgtrEF7eyyYWJM3m5tVQY', // Binary Search by default
  activeStageId: 'stage_1',
  activePatternCategory: 'all',
  allProbsPage: 1
};

let mikFilter = {
  topic: 'all',
  company: 'all',
  status: 'all',
  search: '',
  sort: 'default'
};

let activeMikModalProbId = null;
let activeMikModalPlaylistVideoIndex = -1;
let mikNotesSaveTimeout = null;

function loadMikState() {
  try {
    const raw = localStorage.getItem(STORAGE_MIK_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed === 'object') {
        mikState = {
          version: 1,
          problems: parsed.problems || {},
          collapsedTopics: parsed.collapsedTopics || {},
          collapsedSubtopics: parsed.collapsedSubtopics || {},
          currentMode: parsed.currentMode || 'playlist',
          activePlaylistId: parsed.activePlaylistId || 'PLpIkg8OmuX-LkgtrEF7eyyYWJM3m5tVQY',
          activeStageId: parsed.activeStageId || 'stage_1',
          activePatternCategory: parsed.activePatternCategory || 'all',
          allProbsPage: parsed.allProbsPage || 1
        };
        return;
      }
    }
  } catch (e) {
    console.error('Error loading MIK state:', e);
  }
  mikState = {
    version: 1,
    problems: {},
    collapsedTopics: {},
    collapsedSubtopics: {},
    currentMode: 'playlist',
    activePlaylistId: 'PLpIkg8OmuX-LkgtrEF7eyyYWJM3m5tVQY',
    activeStageId: 'stage_1',
    activePatternCategory: 'all',
    allProbsPage: 1
  };
}

function saveMikState() {
  try {
    localStorage.setItem(STORAGE_MIK_KEY, JSON.stringify(mikState));
    if (typeof mirrorToIndexedDB === 'function') mirrorToIndexedDB();
    if (typeof recordSnapshot === 'function') recordSnapshot('auto-mik-state-save');
  } catch (e) {
    console.error('Error saving MIK state:', e);
  }
}

function getMikProblemState(probId) {
  if (!mikState.problems[probId]) {
    mikState.problems[probId] = {
      status: 'NOT_STARTED',
      done: false,
      starred: false,
      notes: '',
      lastRevised: null
    };
  }
  return mikState.problems[probId];
}

function getMikCatalog() {
  if (window.MIK_CATALOG && Array.isArray(window.MIK_CATALOG)) return window.MIK_CATALOG;
  if (window.MIK_CATALOG_DATA && Array.isArray(window.MIK_CATALOG_DATA)) return window.MIK_CATALOG_DATA;
  return [];
}

function getMikPlaylists() {
  if (window.MIK_PLAYLISTS && Array.isArray(window.MIK_PLAYLISTS)) return window.MIK_PLAYLISTS;
  return [];
}

function getMikLearningOrder() {
  if (window.MIK_LEARNING_ORDER && Array.isArray(window.MIK_LEARNING_ORDER)) return window.MIK_LEARNING_ORDER;
  return [];
}

function getMikPatterns() {
  if (window.MIK_PATTERNS && Array.isArray(window.MIK_PATTERNS)) return window.MIK_PATTERNS;
  return [];
}

function getMikDoneCount() {
  const cat = getMikCatalog();
  let count = 0;
  cat.forEach(p => {
    const ps = mikState.problems[p.id];
    if (ps && ps.done) count++;
  });
  return count;
}

function getMikTotalCount() {
  const cat = getMikCatalog();
  return cat.length || 1526;
}

function updateMikStats() {
  const cat = getMikCatalog();
  const total = cat.length || 1526;
  let solved = 0;
  let inprog = 0;
  let revise = 0;
  let starred = 0;
  let hasNotes = 0;

  cat.forEach(p => {
    const ps = mikState.problems[p.id];
    if (ps) {
      if (ps.done) solved++;
      if (ps.status === 'IN_PROGRESS') inprog++;
      if (ps.status === 'REVISE') revise++;
      if (ps.starred) starred++;
      if (ps.notes && ps.notes.trim()) hasNotes++;
    }
  });

  const pct = total > 0 ? Math.round((solved / total) * 100) : 0;

  const pctEl = document.getElementById('mikRadialPct');
  if (pctEl) pctEl.textContent = `${pct}%`;

  const gauge = document.getElementById('mikGaugeCircle');
  if (gauge) {
    const circumference = 2 * Math.PI * 42; // ~263.89
    const offset = circumference - (pct / 100) * circumference;
    gauge.style.strokeDashoffset = offset;
  }

  const hdrCount = document.getElementById('mikHeaderSolvedCount');
  if (hdrCount) hdrCount.innerHTML = `${solved} <span class="mik-metric-denom">/ ${total}</span>`;

  const badge = document.getElementById('nav-mik-badge');
  if (badge) badge.textContent = `${solved}/${total}`;

  const chipSolved = document.getElementById('mikChipSolved');
  if (chipSolved) chipSolved.textContent = `🟢 ${solved}`;

  const chipInProg = document.getElementById('mikChipInProgress');
  if (chipInProg) chipInProg.textContent = `🟡 ${inprog}`;

  const chipRevise = document.getElementById('mikChipRevise');
  if (chipRevise) chipRevise.textContent = `🟣 ${revise}`;

  const chipStarred = document.getElementById('mikChipStarred');
  if (chipStarred) chipStarred.textContent = `⭐ ${starred}`;

  const pillAll = document.getElementById('mikPillAllCnt');
  if (pillAll) pillAll.textContent = total;

  const pillSolved = document.getElementById('mikPillSolvedCnt');
  if (pillSolved) pillSolved.textContent = solved;

  const pillInProg = document.getElementById('mikPillInProgCnt');
  if (pillInProg) pillInProg.textContent = inprog;

  const pillRevise = document.getElementById('mikPillReviseCnt');
  if (pillRevise) pillRevise.textContent = revise;

  const pillStarred = document.getElementById('mikPillStarredCnt');
  if (pillStarred) pillStarred.textContent = starred;

  const pillNotes = document.getElementById('mikPillNotesCnt');
  if (pillNotes) pillNotes.textContent = hasNotes;
}

// --------------------------------------------------------------------------
// MODE MANAGEMENT (5 Complementary Views)
// --------------------------------------------------------------------------
function setMikMode(mode) {
  mikState.currentMode = mode;
  saveMikState();

  document.querySelectorAll('.mik-mode-tab').forEach(tab => {
    tab.classList.toggle('active', tab.id === `mikModeTab-${mode}`);
  });

  updateMikDropdownForMode();
  populateMikNav();
  renderMikContent();
}

function setMikActivePlaylist(playlistId) {
  mikState.activePlaylistId = playlistId;
  saveMikState();

  // Sync topic dropdown
  const pl = getMikPlaylists().find(p => p.id === playlistId);
  const select = document.getElementById('mikTopicDropdown');
  if (select && pl) {
    select.value = playlistId;
  }

  populateMikNav();
  renderMikContent();
}

function setMikActiveStage(stageId) {
  mikState.activeStageId = stageId;
  saveMikState();
  populateMikNav();
  renderMikContent();
}

function setMikActivePatternCategory(catName) {
  mikState.activePatternCategory = catName;
  saveMikState();
  populateMikNav();
  renderMikContent();
}

// --------------------------------------------------------------------------
// CONTEXT-AWARE DROPDOWN SYNCHRONIZATION
// --------------------------------------------------------------------------
function updateMikDropdownForMode() {
  const select = document.getElementById('mikTopicDropdown');
  if (!select) return;

  const mode = mikState.currentMode || 'playlist';
  select.innerHTML = '';

  if (mode === 'playlist') {
    const playlists = getMikPlaylists();
    playlists.forEach(pl => {
      const opt = document.createElement('option');
      opt.value = pl.id;
      opt.textContent = `🎬 ${pl.title.replace(': Popular Interview Problems', '').replace(': Convert Story To Code', '')}`;
      if (pl.id === mikState.activePlaylistId) opt.selected = true;
      select.appendChild(opt);
    });
  } else if (mode === 'pattern') {
    const patterns = getMikPatterns();
    const categories = Array.from(new Set(patterns.map(p => p.category)));
    const optAll = document.createElement('option');
    optAll.value = 'all';
    optAll.textContent = '🧩 All Pattern Categories';
    select.appendChild(optAll);
    categories.forEach(c => {
      const opt = document.createElement('option');
      opt.value = c;
      opt.textContent = `🧩 ${c}`;
      if (mikState.activePatternCategory === c) opt.selected = true;
      select.appendChild(opt);
    });
  } else if (mode === 'roadmap') {
    const stages = getMikLearningOrder();
    const optAll = document.createElement('option');
    optAll.value = 'all';
    optAll.textContent = '🗺️ All 5 Stages';
    select.appendChild(optAll);
    stages.forEach(st => {
      const opt = document.createElement('option');
      opt.value = st.stage_id;
      opt.textContent = `🗺️ ${st.stage_title.split(':')[0]}`;
      if (mikState.activeStageId === st.stage_id) opt.selected = true;
      select.appendChild(opt);
    });
  } else {
    // Repo and All Problems modes
    const cat = getMikCatalog();
    const topics = Array.from(new Set(cat.map(p => p.topic))).sort();
    const optAll = document.createElement('option');
    optAll.value = 'all';
    optAll.textContent = '📂 All 23 Topics';
    select.appendChild(optAll);
    topics.forEach(t => {
      const opt = document.createElement('option');
      opt.value = t;
      opt.textContent = `📂 ${t}`;
      if (mikFilter.topic === t) opt.selected = true;
      select.appendChild(opt);
    });
  }
}

// --------------------------------------------------------------------------
// FILTER CONTROLS
// --------------------------------------------------------------------------
function handleMikSearchInput(val) {
  mikFilter.search = (val || '').trim().toLowerCase();
  const clearBtn = document.getElementById('mikSearchClearBtn');
  if (clearBtn) clearBtn.style.display = mikFilter.search ? 'block' : 'none';
  mikState.allProbsPage = 1;
  renderMikContent();
}

function clearMikSearch() {
  const input = document.getElementById('mikSearchInput');
  if (input) input.value = '';
  handleMikSearchInput('');
}

function setMikTopic(val) {
  const mode = mikState.currentMode || 'playlist';
  if (mode === 'playlist') {
    // In playlist mode, selecting dropdown switches active playlist
    setMikActivePlaylist(val);
  } else if (mode === 'pattern') {
    setMikActivePatternCategory(val);
  } else if (mode === 'roadmap') {
    setMikActiveStage(val);
  } else {
    // Repo or All mode
    mikFilter.topic = val;
    mikState.allProbsPage = 1;
    populateMikNav();
    renderMikContent();
  }
}

function setMikCompany(company) {
  mikFilter.company = company;
  mikState.allProbsPage = 1;
  renderMikContent();
}

function setMikSort(sortOrder) {
  mikFilter.sort = sortOrder;
  renderMikContent();
}

function setMikStatusFilter(status, btn) {
  mikFilter.status = status;
  mikState.allProbsPage = 1;
  document.querySelectorAll('.mik-pill').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderMikContent();
}

function resetAllMikFilters() {
  mikFilter = { topic: 'all', company: 'all', status: 'all', search: '', sort: 'default' };
  mikState.allProbsPage = 1;

  const searchInput = document.getElementById('mikSearchInput');
  if (searchInput) searchInput.value = '';
  const clearBtn = document.getElementById('mikSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';

  const companyDropdown = document.getElementById('mikCompanyDropdown');
  if (companyDropdown) companyDropdown.value = 'all';

  const sortDropdown = document.getElementById('mikSortDropdown');
  if (sortDropdown) sortDropdown.value = 'default';

  document.querySelectorAll('.mik-pill').forEach(b => b.classList.remove('active'));
  const allPill = document.getElementById('f-mik-all');
  if (allPill) allPill.classList.add('active');

  updateMikDropdownForMode();
  populateMikNav();
  renderMikContent();
  if (typeof showToast === 'function') showToast('Filters reset to default');
}

function toggleMikSubtopicCollapse(groupKey) {
  mikState.collapsedSubtopics[groupKey] = !mikState.collapsedSubtopics[groupKey];
  saveMikState();
  renderMikContent();
}

function expandAllMikSubtopics(expand) {
  if (expand) {
    mikState.collapsedSubtopics = {};
  } else {
    const cat = getMikCatalog();
    cat.forEach(p => {
      const k = `${p.topic}__${p.subtopic || 'General'}`;
      mikState.collapsedSubtopics[k] = true;
    });
  }
  saveMikState();
  renderMikContent();
}

// --------------------------------------------------------------------------
// PROBLEM STATUS & ACTIONS
// --------------------------------------------------------------------------
function setMikProblemStatus(probId, newStatus) {
  const ps = getMikProblemState(probId);
  ps.status = newStatus;
  ps.done = (newStatus === 'SOLVED');
  if (newStatus === 'SOLVED' || newStatus === 'REVISE') {
    ps.lastRevised = new Date().toISOString();
  }
  saveMikState();
  updateMikStats();
  renderMikContent();
}

function toggleMikStar(probId) {
  const ps = getMikProblemState(probId);
  ps.starred = !ps.starred;
  saveMikState();
  updateMikStats();
  renderMikContent();
}

function jumpToNextUnsolvedMikProblem() {
  const cat = getMikCatalog();
  const playlists = getMikPlaylists();
  let candidate = null;

  // In playlist mode, find first unsolved in active playlist
  if (mikState.currentMode === 'playlist') {
    const pl = playlists.find(p => p.id === mikState.activePlaylistId);
    if (pl) {
      for (let i = 0; i < pl.videos.length; i++) {
        const v = pl.videos[i];
        if (v.problem_id) {
          const ps = getMikProblemState(v.problem_id);
          if (!ps.done) {
            candidate = { probId: v.problem_id, videoIndex: i };
            break;
          }
        }
      }
    }
  }

  // Fallback to first unsolved in entire catalog
  if (!candidate) {
    for (let i = 0; i < cat.length; i++) {
      const p = cat[i];
      const ps = mikState.problems[p.id];
      if (!ps || !ps.done) {
        candidate = { probId: p.id, videoIndex: -1 };
        break;
      }
    }
  }

  if (candidate) {
    openMikModal(candidate.probId, candidate.videoIndex);
    if (typeof showToast === 'function') showToast('Resumed next unattempted problem!');
  } else {
    if (typeof showToast === 'function') showToast('🎉 All problems are marked solved!');
  }
}

// --------------------------------------------------------------------------
// MODAL DETAILS & PLAYLIST SEQUENTIAL NAVIGATION
// --------------------------------------------------------------------------
function openMikModal(probId, contextVideoIndex = -1) {
  activeMikModalProbId = probId;
  activeMikModalPlaylistVideoIndex = contextVideoIndex;

  const cat = getMikCatalog();
  const p = cat.find(item => item.id === probId);
  if (!p) return;

  const ps = getMikProblemState(probId);

  // Set ID and Titles
  const idEl = document.getElementById('mikModalProbId');
  if (idEl) idEl.textContent = `MIK #${p.n} (${p.id})`;

  const titleEl = document.getElementById('mikModalTitle');
  if (titleEl) titleEl.textContent = p.title;

  const tsEl = document.getElementById('mikModalTopicSubtopic');
  if (tsEl) tsEl.textContent = `${p.topic} > ${p.subtopic || 'General'}`;

  // Star Button
  const starBtn = document.getElementById('mikModalStarBtn');
  if (starBtn) {
    starBtn.textContent = ps.starred ? '★' : '☆';
    starBtn.classList.toggle('starred', ps.starred);
  }

  // Playlist Context Bar
  const plNav = document.getElementById('mikModalPlaylistNav');
  if (plNav) {
    const playlists = getMikPlaylists();
    const activePl = playlists.find(pl => pl.id === mikState.activePlaylistId);
    if (mikState.currentMode === 'playlist' && activePl && contextVideoIndex >= 0) {
      plNav.style.display = 'flex';
      const label = document.getElementById('mikModalPlaylistNavLabel');
      if (label) {
        label.textContent = `🎬 Video ${contextVideoIndex + 1} of ${activePl.videos.length} · ${activePl.title.replace(': Popular Interview Problems', '')}`;
      }
      const prevBtn = document.getElementById('mikModalPrevVideoBtn');
      if (prevBtn) prevBtn.disabled = (contextVideoIndex <= 0);
      const nextBtn = document.getElementById('mikModalNextVideoBtn');
      if (nextBtn) nextBtn.disabled = (contextVideoIndex >= activePl.videos.length - 1);
    } else {
      plNav.style.display = 'none';
    }
  }

  // Quick Links Bar
  const linksBar = document.getElementById('mikModalLinksBar');
  if (linksBar) {
    let linksHtml = '';
    if (p.youtube_url) {
      linksHtml += `<a href="${p.youtube_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge yt">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="#ef4444"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
        <span>Watch Video</span>
      </a>`;
    }
    if (p.leetcode_url) {
      linksHtml += `<a href="${p.leetcode_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge lc">
        <span style="color:#f59e0b; font-weight:800;">LC</span>
        <span>Practice Problem</span>
      </a>`;
    }
    if (p.github_url) {
      linksHtml += `<a href="${p.github_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge gh">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
        <span>GitHub C++</span>
      </a>`;
    }
    linksBar.innerHTML = linksHtml || '<span style="color:var(--text-muted); font-size:12px;">No external links recorded.</span>';
  }

  // Complexity & Metadata
  const tcEl = document.getElementById('mikModalTc');
  if (tcEl) tcEl.textContent = p.tc || '-';

  const scEl = document.getElementById('mikModalSc');
  if (scEl) scEl.textContent = p.sc || '-';

  const freqEl = document.getElementById('mikModalFreq');
  if (freqEl) freqEl.textContent = p.frequency || '-';

  const compEl = document.getElementById('mikModalCompanies');
  if (compEl) {
    if (p.companies && p.companies.length > 0) {
      compEl.innerHTML = p.companies.map(c => `<span class="mik-tag company">${c}</span>`).join(' ');
    } else {
      compEl.textContent = '-';
    }
  }

  // Approach Box
  const appBox = document.getElementById('mikModalApproachBox');
  const appText = document.getElementById('mikModalApproachText');
  if (appBox && appText) {
    if (p.approaches && p.approaches.length > 0) {
      appBox.style.display = 'block';
      appText.innerHTML = p.approaches.map(a => `<div>• ${a}</div>`).join('');
    } else {
      appBox.style.display = 'none';
      appText.innerHTML = '';
    }
  }

  // Status Buttons
  updateMikModalStatusButtons(ps.status || 'NOT_STARTED');

  // Notes
  const notesTextarea = document.getElementById('mikModalNotesTextarea');
  if (notesTextarea) {
    notesTextarea.value = ps.notes || '';
    updateMikNotesCharCount(ps.notes || '');
  }

  const indicator = document.getElementById('mikNotesSaveIndicator');
  if (indicator) indicator.textContent = 'Auto-saved locally ✓';

  if (typeof openModal === 'function') openModal('modalMikDetail');
}

function prevMikPlaylistVideo() {
  const playlists = getMikPlaylists();
  const pl = playlists.find(p => p.id === mikState.activePlaylistId);
  if (!pl || activeMikModalPlaylistVideoIndex <= 0) return;

  const targetIdx = activeMikModalPlaylistVideoIndex - 1;
  const targetVideo = pl.videos[targetIdx];
  if (targetVideo && targetVideo.problem_id) {
    openMikModal(targetVideo.problem_id, targetIdx);
  }
}

function nextMikPlaylistVideo() {
  const playlists = getMikPlaylists();
  const pl = playlists.find(p => p.id === mikState.activePlaylistId);
  if (!pl || activeMikModalPlaylistVideoIndex < 0 || activeMikModalPlaylistVideoIndex >= pl.videos.length - 1) return;

  const targetIdx = activeMikModalPlaylistVideoIndex + 1;
  const targetVideo = pl.videos[targetIdx];
  if (targetVideo && targetVideo.problem_id) {
    openMikModal(targetVideo.problem_id, targetIdx);
  }
}

function updateMikModalStatusButtons(status) {
  document.querySelectorAll('#mikModalStatusGroup .mik-status-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-status') === status);
  });
}

function setMikModalStatus(status) {
  if (!activeMikModalProbId) return;
  setMikProblemStatus(activeMikModalProbId, status);
  updateMikModalStatusButtons(status);
}

function toggleMikModalStar() {
  if (!activeMikModalProbId) return;
  toggleMikStar(activeMikModalProbId);
  const ps = getMikProblemState(activeMikModalProbId);
  const starBtn = document.getElementById('mikModalStarBtn');
  if (starBtn) {
    starBtn.textContent = ps.starred ? '★' : '☆';
    starBtn.classList.toggle('starred', ps.starred);
  }
}

function updateMikNotesCharCount(val) {
  const el = document.getElementById('mikNotesCharCount');
  if (el) el.textContent = `${(val || '').length} chars`;
}

function handleMikModalNotesInput(val) {
  updateMikNotesCharCount(val);
  const indicator = document.getElementById('mikNotesSaveIndicator');
  if (indicator) indicator.textContent = 'Saving...';

  clearTimeout(mikNotesSaveTimeout);
  mikNotesSaveTimeout = setTimeout(() => {
    if (activeMikModalProbId) {
      const ps = getMikProblemState(activeMikModalProbId);
      ps.notes = val;
      saveMikState();
      updateMikStats();
      if (indicator) indicator.textContent = 'Auto-saved locally ✓';
    }
  }, 400);
}

function saveMikModalNotesExplicitly() {
  if (!activeMikModalProbId) return;
  const textarea = document.getElementById('mikModalNotesTextarea');
  const val = textarea ? textarea.value : '';
  const ps = getMikProblemState(activeMikModalProbId);
  ps.notes = val;
  saveMikState();
  updateMikStats();
  renderMikContent();
  const indicator = document.getElementById('mikNotesSaveIndicator');
  if (indicator) {
    indicator.textContent = 'Saved successfully ✓';
    setTimeout(() => { indicator.textContent = 'Auto-saved locally'; }, 2000);
  }
  if (typeof showToast === 'function') showToast('Notes saved!');
}

function copyMikNotesToClipboard() {
  const textarea = document.getElementById('mikModalNotesTextarea');
  const text = textarea ? textarea.value : '';
  if (!text) {
    if (typeof showToast === 'function') showToast('No notes to copy');
    return;
  }
  navigator.clipboard.writeText(text).then(() => {
    if (typeof showToast === 'function') showToast('Notes copied to clipboard!');
  }).catch(() => {
    if (typeof showToast === 'function') showToast('Failed to copy notes');
  });
}

// --------------------------------------------------------------------------
// FILTER EVALUATION HELPER
// --------------------------------------------------------------------------
function matchesMikFilter(p) {
  const ps = mikState.problems[p.id] || { status: 'NOT_STARTED', done: false, starred: false, notes: '' };

  // Topic filter (applies only in repo and all mode, or when explicitly set)
  if (mikState.currentMode === 'repo' || mikState.currentMode === 'all') {
    if (mikFilter.topic !== 'all' && p.topic !== mikFilter.topic) return false;
  }

  // Company filter
  if (mikFilter.company !== 'all') {
    if (!p.companies || !p.companies.some(c => c.toLowerCase() === mikFilter.company.toLowerCase())) {
      return false;
    }
  }

  // Status filter
  if (mikFilter.status === 'solved' && !ps.done) return false;
  if (mikFilter.status === 'inprogress' && ps.status !== 'IN_PROGRESS') return false;
  if (mikFilter.status === 'revise' && ps.status !== 'REVISE') return false;
  if (mikFilter.status === 'unsolved' && ps.done) return false;
  if (mikFilter.status === 'starred' && !ps.starred) return false;
  if (mikFilter.status === 'notes' && (!ps.notes || !ps.notes.trim())) return false;

  // Search filter
  if (mikFilter.search) {
    const q = mikFilter.search;
    const inTitle = p.title.toLowerCase().includes(q);
    const inTopic = p.topic.toLowerCase().includes(q);
    const inSubtopic = (p.subtopic || '').toLowerCase().includes(q);
    const inCompanies = p.companies ? p.companies.some(c => c.toLowerCase().includes(q)) : false;
    const inApproaches = p.approaches ? p.approaches.some(a => a.toLowerCase().includes(q)) : false;
    const inNotes = ps.notes ? ps.notes.toLowerCase().includes(q) : false;
    if (!inTitle && !inTopic && !inSubtopic && !inCompanies && !inApproaches && !inNotes) {
      return false;
    }
  }

  return true;
}

// --------------------------------------------------------------------------
// ROW GENERATOR HELPER
// --------------------------------------------------------------------------
function renderMikProblemRow(p, seqBadge = null, contextIndex = -1) {
  const ps = mikState.problems[p.id] || { status: 'NOT_STARTED', done: false, starred: false, notes: '' };
  const isSolved = ps.done;
  const isStarred = ps.starred;
  const hasNotes = ps.notes && ps.notes.trim();

  const seqDisplay = seqBadge !== null ? seqBadge : `#${p.n}`;
  const isPlaylistSeq = seqBadge !== null && seqBadge.toString().startsWith('#');

  // Tags
  let tagsHtml = '';
  if (p.companies && p.companies.length > 0) {
    tagsHtml += p.companies.slice(0, 2).map(c => `<span class="mik-tag company">${c}</span>`).join('');
    if (p.companies.length > 2) tagsHtml += `<span class="mik-tag">+${p.companies.length - 2}</span>`;
  }
  if (p.tc) {
    tagsHtml += `<span class="mik-tag tc" title="Time: ${p.tc}">${p.tc}</span>`;
  }

  // Links
  let linksHtml = '';
  if (p.youtube_url) {
    linksHtml += `<a href="${p.youtube_url}" target="_blank" rel="noopener noreferrer" class="mik-link-btn yt" title="Watch Video Tutorial">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="#ef4444"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
    </a>`;
  }
  if (p.leetcode_url) {
    linksHtml += `<a href="${p.leetcode_url}" target="_blank" rel="noopener noreferrer" class="mik-link-btn lc" title="Practice on LeetCode">
      <span style="font-weight:700; font-size:10px;">LC</span>
    </a>`;
  }
  if (p.github_url) {
    linksHtml += `<a href="${p.github_url}" target="_blank" rel="noopener noreferrer" class="mik-link-btn gh" title="View Source on GitHub">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
    </a>`;
  }

  return `
    <div class="mik-prob-row ${isSolved ? 'solved' : ''}" id="mik-row-${p.id}">
      <div class="mik-prob-seq ${isPlaylistSeq ? 'playlist-seq' : ''}">${seqDisplay}</div>
      <div class="mik-prob-title-group">
        <span class="mik-prob-title-link" onclick="openMikModal('${p.id}', ${contextIndex})" title="${p.title}">
          ${p.title}
        </span>
        <div class="mik-prob-tags">
          ${tagsHtml}
        </div>
      </div>
      <div class="mik-links-group">
        ${linksHtml}
      </div>
      <div>
        <select class="mik-status-dropdown status-${ps.status || 'NOT_STARTED'}" onchange="setMikProblemStatus('${p.id}', this.value)">
          <option value="NOT_STARTED" ${ps.status === 'NOT_STARTED' ? 'selected' : ''}>⚪ Not Started</option>
          <option value="IN_PROGRESS" ${ps.status === 'IN_PROGRESS' ? 'selected' : ''}>🟡 In Progress</option>
          <option value="SOLVED" ${ps.status === 'SOLVED' ? 'selected' : ''}>🟢 Solved</option>
          <option value="REVISE" ${ps.status === 'REVISE' ? 'selected' : ''}>🟣 Revise</option>
        </select>
      </div>
      <div>
        <button class="mik-notes-indicator-btn ${hasNotes ? 'has-notes' : ''}" onclick="openMikModal('${p.id}', ${contextIndex})" title="${hasNotes ? 'Edit Notes (Notes Saved)' : 'Add Notes'}">
          ${hasNotes ? '📝' : '🗒️'}
        </button>
      </div>
      <div>
        <button class="mik-star-toggle-btn ${isStarred ? 'starred' : ''}" onclick="toggleMikStar('${p.id}')" title="Toggle Star">
          ${isStarred ? '★' : '☆'}
        </button>
      </div>
    </div>
  `;
}

// --------------------------------------------------------------------------
// RENDER VIEW 1: CREATOR PLAYLISTS MODE
// --------------------------------------------------------------------------
function renderMikPlaylistView() {
  const container = document.getElementById('mikContentArea');
  if (!container) return;

  const playlists = getMikPlaylists();
  const cat = getMikCatalog();
  const catMap = {};
  cat.forEach(p => catMap[p.id] = p);

  if (!playlists || playlists.length === 0) {
    container.innerHTML = `
      <div class="mik-empty-state">
        <div class="mik-empty-icon">🎬</div>
        <div class="mik-empty-title">Loading Creator Playlists...</div>
        <p class="mik-empty-desc">Verified playlist manifests are synchronizing.</p>
      </div>`;
    return;
  }

  const activePl = playlists.find(p => p.id === mikState.activePlaylistId) || playlists[0];

  // Calculate stats for active playlist
  let plSolved = 0;
  let plMatched = 0;
  activePl.videos.forEach(v => {
    if (v.problem_id) {
      plMatched++;
      const ps = mikState.problems[v.problem_id];
      if (ps && ps.done) plSolved++;
    }
  });

  const plPct = plMatched > 0 ? Math.round((plSolved / plMatched) * 100) : 0;

  // Filter videos (respects status, search, company)
  const filteredVideos = activePl.videos.filter(v => {
    if (!v.problem_id) return (mikFilter.status === 'all' && !mikFilter.search && mikFilter.company === 'all');
    const p = catMap[v.problem_id];
    if (!p) return false;
    return matchesMikFilter(p);
  });

  let videosHtml = '';
  filteredVideos.forEach((v) => {
    if (v.problem_id && catMap[v.problem_id]) {
      const p = catMap[v.problem_id];
      videosHtml += renderMikProblemRow(p, `#${v.seq}`, v.seq - 1);
    } else {
      // Unmatched or conceptual video row
      videosHtml += `
        <div class="mik-prob-row">
          <div class="mik-prob-seq playlist-seq">#${v.seq}</div>
          <div class="mik-prob-title-group">
            <span class="mik-prob-title-link" style="color:#94a3b8;">
              🎬 ${v.video_title}
            </span>
            <div class="mik-prob-tags">
              <span class="mik-tag" style="color:#fbbf24;">Playlist Video (Concept / Roadmap)</span>
            </div>
          </div>
          <div class="mik-links-group">
            <a href="${v.video_url}" target="_blank" rel="noopener noreferrer" class="mik-link-btn yt" title="Watch on YouTube">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="#ef4444"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
            </a>
          </div>
          <div><span class="mik-tag">Video Only</span></div>
          <div></div>
          <div></div>
        </div>`;
    }
  });

  // Unmatched videos accordion
  let unmatchedHtml = '';
  if (activePl.unmatched_videos && activePl.unmatched_videos.length > 0) {
    unmatchedHtml = `
      <div class="mik-unmatched-card">
        <div class="mik-unmatched-header" onclick="this.nextElementSibling.classList.toggle('hidden')">
          <span>⚠️ Unmatched Playlist Videos (${activePl.unmatched_videos.length}) — Click to Inspect</span>
          <span>▾</span>
        </div>
        <div class="mik-prob-list" style="margin-top:0.75rem;">
          ${activePl.unmatched_videos.map(uv => `
            <div style="padding:0.55rem 0; font-size:12px; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items:center;">
              <div>
                <span style="font-weight:700; color:#fbbf24; margin-right:0.5rem;">#${uv.seq}</span>
                <span style="color:#f8fafc;">${uv.video_title}</span>
                <div style="font-size:11px; color:#94a3b8; margin-top:2px;">${uv.reason}</div>
              </div>
              <a href="${uv.video_url}" target="_blank" rel="noopener noreferrer" class="mik-action-btn" style="font-size:11px; padding:0.25rem 0.6rem;">Watch on YouTube</a>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    <div class="mik-playlist-banner">
      <div class="mik-playlist-banner-left">
        <div class="mik-playlist-banner-title">
          <span>🎬 ${activePl.title}</span>
          <span class="mik-tag" style="background:rgba(239,68,68,0.18); color:#fca5a5; border-color:rgba(239,68,68,0.4);">
            codestorywithMIK Verified
          </span>
        </div>
        <div class="mik-playlist-banner-desc">${activePl.description || ''}</div>
        <div style="font-size:12px; color:#94a3b8; display:flex; gap:1.2rem; align-items:center; flex-wrap:wrap;">
          <span>Progress: <strong style="color:#ffffff;">${plSolved} / ${plMatched} Solved</strong> (${plPct}%)</span>
          <span>Verified Sequence: <strong style="color:#ffffff;">${activePl.total_videos} Videos</strong></span>
        </div>
        <div class="mik-playlist-progress-bar-wrap">
          <div class="mik-playlist-progress-bar" style="width: ${plPct}%;"></div>
        </div>
      </div>
      <div style="display:flex; flex-direction:column; gap:0.5rem; align-items:flex-end;">
        <button class="mik-action-btn primary" onclick="jumpToNextUnsolvedMikProblem()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
          <span>Resume Learning</span>
        </button>
        <a href="https://www.youtube.com/playlist?list=${activePl.id}" target="_blank" rel="noopener noreferrer" class="mik-action-btn" title="Open Playlist on YouTube">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="#ef4444"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
          <span>Open on YouTube</span>
        </a>
      </div>
    </div>

    <div class="mik-subtopic-card">
      <div class="mik-subtopic-header">
        <div class="mik-subtopic-title">
          <span>📋 Exact Video Sequence Order (${filteredVideos.length} Items)</span>
        </div>
      </div>
      <div class="mik-prob-list">
        ${videosHtml || '<div style="padding:1.5rem; text-align:center; color:#94a3b8; font-size:13px;">No problems match current filters.</div>'}
      </div>
    </div>

    ${unmatchedHtml}
  `;
}

// --------------------------------------------------------------------------
// RENDER VIEW 2: LEARNING ROADMAP MODE (Striver-Style 5 Stages)
// --------------------------------------------------------------------------
function renderMikRoadmapView() {
  const container = document.getElementById('mikContentArea');
  if (!container) return;

  const stages = getMikLearningOrder();
  const cat = getMikCatalog();
  const catMap = {};
  cat.forEach(p => catMap[p.id] = p);

  let stagesHtml = '';

  stages.forEach(st => {
    // If activeStageId is set and not 'all', filter
    if (mikState.activeStageId && mikState.activeStageId !== 'all' && st.stage_id !== mikState.activeStageId) {
      return;
    }

    let stageSolved = 0;
    let stageTotal = 0;

    st.topics.forEach(t => {
      t.subtopics.forEach(sub => {
        sub.problem_ids.forEach(pid => {
          stageTotal++;
          const ps = mikState.problems[pid];
          if (ps && ps.done) stageSolved++;
        });
      });
    });

    const stagePct = stageTotal > 0 ? Math.round((stageSolved / stageTotal) * 100) : 0;
    const isCollapsed = !!mikState.collapsedTopics[st.stage_id];

    let topicsHtml = '';
    st.topics.forEach(t => {
      if (mikFilter.topic !== 'all' && t.topic !== mikFilter.topic) return;

      let subtopicsHtml = '';
      t.subtopics.forEach(sub => {
        const groupKey = `${t.topic}__${sub.subtopic}`;
        const isSubCollapsed = !!mikState.collapsedSubtopics[groupKey];

        const matchedProbs = sub.problem_ids
          .map(pid => catMap[pid])
          .filter(p => p && matchesMikFilter(p));

        if (matchedProbs.length === 0 && (mikFilter.status !== 'all' || mikFilter.search || mikFilter.company !== 'all')) {
          return;
        }

        let subSolved = 0;
        sub.problem_ids.forEach(pid => {
          if (mikState.problems[pid]?.done) subSolved++;
        });

        subtopicsHtml += `
          <div class="mik-subtopic-card">
            <div class="mik-subtopic-header" onclick="toggleMikSubtopicCollapse('${groupKey}')">
              <div class="mik-subtopic-title">
                <span style="font-size:12px; color:#94a3b8;">${isSubCollapsed ? '▶' : '▼'}</span>
                <span>${sub.subtopic}</span>
              </div>
              <div style="font-size:11.5px; color:#94a3b8; display:flex; gap:0.5rem; align-items:center;">
                <span class="mik-topic-nav-badge">${subSolved}/${sub.problem_count}</span>
              </div>
            </div>
            ${!isSubCollapsed ? `
              <div class="mik-prob-list">
                ${matchedProbs.map((p, idx) => renderMikProblemRow(p, idx + 1)).join('') || '<div style="padding:1rem; font-size:12px; color:#94a3b8; text-align:center;">No matching problems in this subtopic.</div>'}
              </div>
            ` : ''}
          </div>
        `;
      });

      if (subtopicsHtml) {
        topicsHtml += `
          <div style="margin-bottom:1rem;">
            <div style="font-size:13px; font-weight:700; color:#f8fafc; margin-bottom:0.4rem; display:flex; justify-content:space-between;">
              <span>📂 ${t.topic}</span>
              <span style="font-size:11px; color:#94a3b8;">${t.problem_count} problems</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:0.6rem;">
              ${subtopicsHtml}
            </div>
          </div>
        `;
      }
    });

    stagesHtml += `
      <div class="mik-stage-card" id="mik-stage-${st.stage_id}">
        <div class="mik-stage-header" onclick="toggleMikStageCollapse('${st.stage_id}')">
          <div class="mik-stage-title-wrap">
            <span style="font-size:13px; color:#94a3b8;">${isCollapsed ? '▶' : '▼'}</span>
            <div>
              <div class="mik-stage-title">${st.stage_title}</div>
              <div class="mik-stage-desc">${st.stage_description}</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:0.85rem;">
            <div style="text-align:right;">
              <div style="font-size:12px; font-weight:700; color:#ffffff;">${stageSolved} / ${stageTotal}</div>
              <div style="font-size:10.5px; color:#94a3b8;">${stagePct}% Done</div>
            </div>
          </div>
        </div>
        ${!isCollapsed ? `
          <div class="mik-stage-body">
            ${topicsHtml || '<div style="text-align:center; padding:1.5rem; color:#94a3b8;">No problems match active filters in this stage.</div>'}
          </div>
        ` : ''}
      </div>
    `;
  });

  container.innerHTML = stagesHtml || `
    <div class="mik-empty-state">
      <div class="mik-empty-icon">🗺️</div>
      <div class="mik-empty-title">No Problems Found</div>
      <p class="mik-empty-desc">Try resetting your topic, company, or status filters.</p>
      <button class="mik-action-btn primary" onclick="resetAllMikFilters()">Reset Filters</button>
    </div>
  `;
}

function toggleMikStageCollapse(stageId) {
  mikState.collapsedTopics[stageId] = !mikState.collapsedTopics[stageId];
  saveMikState();
  renderMikContent();
}

// --------------------------------------------------------------------------
// RENDER VIEW 3: PATTERN EXPLORER MODE (RisingBrain-Style)
// --------------------------------------------------------------------------
function renderMikPatternView() {
  const container = document.getElementById('mikContentArea');
  if (!container) return;

  const patterns = getMikPatterns();
  const cat = getMikCatalog();
  const catMap = {};
  cat.forEach(p => catMap[p.id] = p);

  // Group patterns by category
  const categories = {};
  patterns.forEach(pat => {
    if (!categories[pat.category]) categories[pat.category] = [];
    categories[pat.category].push(pat);
  });

  let htmlOutput = '';

  Object.entries(categories).forEach(([catName, patList]) => {
    if (mikState.activePatternCategory !== 'all' && mikState.activePatternCategory !== catName) {
      return;
    }

    let patCardsHtml = '';

    patList.forEach(pat => {
      let patSolved = 0;
      pat.problem_ids.forEach(pid => {
        if (mikState.problems[pid]?.done) patSolved++;
      });

      const patPct = pat.problem_count > 0 ? Math.round((patSolved / pat.problem_count) * 100) : 0;
      const isCollapsed = !!mikState.collapsedSubtopics[pat.id];

      const matchedProbs = pat.problem_ids
        .map(pid => catMap[pid])
        .filter(p => p && matchesMikFilter(p));

      if (matchedProbs.length === 0 && (mikFilter.status !== 'all' || mikFilter.search || mikFilter.company !== 'all')) {
        return;
      }

      patCardsHtml += `
        <div class="mik-pattern-card">
          <div class="mik-pattern-header" onclick="toggleMikSubtopicCollapse('${pat.id}')">
            <div>
              <div class="mik-pattern-title">
                <span style="font-size:12px; color:#94a3b8;">${isCollapsed ? '▶' : '▼'}</span>
                <span>🧩 ${pat.name}</span>
                <span class="mik-tag" style="font-size:10.5px;">${patSolved}/${pat.problem_count}</span>
              </div>
              <div class="mik-pattern-desc">${pat.description}</div>
            </div>
            <div style="text-align:right;">
              <span style="font-size:12px; font-weight:700; color:#38bdf8;">${patPct}%</span>
            </div>
          </div>
          ${!isCollapsed ? `
            <div class="mik-prob-list">
              ${matchedProbs.map((p, idx) => renderMikProblemRow(p, idx + 1)).join('') || '<div style="padding:1rem; font-size:12px; color:#94a3b8; text-align:center;">No matching problems in this pattern.</div>'}
            </div>
          ` : ''}
        </div>
      `;
    });

    if (patCardsHtml) {
      htmlOutput += `
        <div style="margin-bottom:1.5rem;">
          <div style="font-size:1.1rem; font-weight:800; color:#ffffff; margin-bottom:0.6rem; display:flex; align-items:center; gap:0.5rem;">
            <span>${catName}</span>
          </div>
          <div style="display:flex; flex-direction:column; gap:0.85rem;">
            ${patCardsHtml}
          </div>
        </div>
      `;
    }
  });

  container.innerHTML = htmlOutput || `
    <div class="mik-empty-state">
      <div class="mik-empty-icon">🧩</div>
      <div class="mik-empty-title">No Matching Patterns</div>
      <p class="mik-empty-desc">No problems matched your current filter criteria.</p>
      <button class="mik-action-btn primary" onclick="resetAllMikFilters()">Reset Filters</button>
    </div>
  `;
}

// --------------------------------------------------------------------------
// RENDER VIEW 4: ORIGINAL REPOSITORY MODE
// --------------------------------------------------------------------------
function renderMikRepoView() {
  const container = document.getElementById('mikContentArea');
  if (!container) return;

  const cat = getMikCatalog();

  // Group by topic and subtopic
  const grouped = {};
  cat.forEach(p => {
    if (!matchesMikFilter(p)) return;

    if (!grouped[p.topic]) grouped[p.topic] = {};
    const sub = p.subtopic || 'General';
    if (!grouped[p.topic][sub]) grouped[p.topic][sub] = [];
    grouped[p.topic][sub].push(p);
  });

  const topicsList = Object.keys(grouped);
  if (topicsList.length === 0) {
    container.innerHTML = `
      <div class="mik-empty-state">
        <div class="mik-empty-icon">🔍</div>
        <div class="mik-empty-title">No Problems Found</div>
        <p class="mik-empty-desc">No problems matched your active search or filter selection.</p>
        <button class="mik-action-btn primary" onclick="resetAllMikFilters()">Reset Filters</button>
      </div>`;
    return;
  }

  // Sort topics alphabetically or keep natural order
  if (mikFilter.sort === 'alpha') {
    topicsList.sort();
  }

  let htmlOutput = '';

  topicsList.forEach(topic => {
    let topicSolved = 0;
    let topicTotal = 0;
    const subtopics = grouped[topic];

    Object.values(subtopics).forEach(probs => {
      probs.forEach(p => {
        topicTotal++;
        if (mikState.problems[p.id]?.done) topicSolved++;
      });
    });

    const isTopicCollapsed = !!mikState.collapsedTopics[topic];

    let subtopicsHtml = '';
    Object.keys(subtopics).forEach(subName => {
      const groupKey = `${topic}__${subName}`;
      const isSubCollapsed = !!mikState.collapsedSubtopics[groupKey];
      let probs = subtopics[subName];

      // Sorting within subtopic
      if (mikFilter.sort === 'alpha') {
        probs = [...probs].sort((a, b) => a.title.localeCompare(b.title));
      }

      let subSolved = 0;
      probs.forEach(p => {
        if (mikState.problems[p.id]?.done) subSolved++;
      });

      subtopicsHtml += `
        <div class="mik-subtopic-card">
          <div class="mik-subtopic-header" onclick="toggleMikSubtopicCollapse('${groupKey}')">
            <div class="mik-subtopic-title">
              <span style="font-size:12px; color:#94a3b8;">${isSubCollapsed ? '▶' : '▼'}</span>
              <span>📁 ${subName}</span>
            </div>
            <div style="font-size:11.5px; color:#94a3b8; display:flex; gap:0.5rem; align-items:center;">
              <span class="mik-topic-nav-badge">${subSolved}/${probs.length}</span>
            </div>
          </div>
          ${!isSubCollapsed ? `
            <div class="mik-prob-list">
              ${probs.map(p => renderMikProblemRow(p)).join('')}
            </div>
          ` : ''}
        </div>
      `;
    });

    htmlOutput += `
      <div class="mik-stage-card" id="mik-topic-${encodeURIComponent(topic)}">
        <div class="mik-stage-header" onclick="toggleMikTopicCollapse('${topic}')">
          <div class="mik-stage-title-wrap">
            <span style="font-size:13px; color:#94a3b8;">${isTopicCollapsed ? '▶' : '▼'}</span>
            <div>
              <div class="mik-stage-title">📂 ${topic}</div>
              <div class="mik-stage-desc">Original source folder from MAZHARMIK / Interview_DS_Algo</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:0.75rem;">
            <div style="text-align:right;">
              <div style="font-size:12px; font-weight:700; color:#ffffff;">${topicSolved} / ${topicTotal}</div>
              <div style="font-size:10.5px; color:#94a3b8;">${topicTotal > 0 ? Math.round((topicSolved / topicTotal) * 100) : 0}% Done</div>
            </div>
          </div>
        </div>
        ${!isTopicCollapsed ? `
          <div class="mik-stage-body">
            ${subtopicsHtml}
          </div>
        ` : ''}
      </div>
    `;
  });

  container.innerHTML = htmlOutput;
}

function toggleMikTopicCollapse(topic) {
  mikState.collapsedTopics[topic] = !mikState.collapsedTopics[topic];
  saveMikState();
  renderMikContent();
}

// --------------------------------------------------------------------------
// RENDER VIEW 5: ALL PROBLEMS VIEW (1,526 Browseable with Pagination)
// --------------------------------------------------------------------------
function renderMikAllProblemsView() {
  const container = document.getElementById('mikContentArea');
  if (!container) return;

  const cat = getMikCatalog();
  let filtered = cat.filter(p => matchesMikFilter(p));

  // Sorting
  if (mikFilter.sort === 'alpha') {
    filtered.sort((a, b) => a.title.localeCompare(b.title));
  } else if (mikFilter.sort === 'roadmap') {
    // Keep roadmap ordering if possible
    filtered.sort((a, b) => a.n - b.n);
  }

  const PAGE_SIZE = 50;
  const totalMatches = filtered.length;
  const totalPages = Math.max(1, Math.ceil(totalMatches / PAGE_SIZE));
  if (mikState.allProbsPage > totalPages) mikState.allProbsPage = totalPages;
  if (mikState.allProbsPage < 1) mikState.allProbsPage = 1;

  const startIdx = (mikState.allProbsPage - 1) * PAGE_SIZE;
  const endIdx = Math.min(startIdx + PAGE_SIZE, totalMatches);
  const pageItems = filtered.slice(startIdx, endIdx);

  let listHtml = '';
  pageItems.forEach(p => {
    listHtml += renderMikProblemRow(p);
  });

  const paginationHtml = `
    <div class="mik-pagination-bar">
      <div>
        Showing <strong>${totalMatches > 0 ? startIdx + 1 : 0} - ${endIdx}</strong> of <strong>${totalMatches}</strong> problems (Total Catalog: 1,526)
      </div>
      <div class="mik-pagination-controls">
        <button class="mik-action-btn" onclick="setMikAllPage(1)" ${mikState.allProbsPage <= 1 ? 'disabled' : ''}>« First</button>
        <button class="mik-action-btn" onclick="setMikAllPage(${mikState.allProbsPage - 1})" ${mikState.allProbsPage <= 1 ? 'disabled' : ''}>‹ Prev</button>
        <span style="font-weight:600; color:#ffffff; padding:0 0.5rem;">Page ${mikState.allProbsPage} of ${totalPages}</span>
        <button class="mik-action-btn" onclick="setMikAllPage(${mikState.allProbsPage + 1})" ${mikState.allProbsPage >= totalPages ? 'disabled' : ''}>Next ›</button>
        <button class="mik-action-btn" onclick="setMikAllPage(${totalPages})" ${mikState.allProbsPage >= totalPages ? 'disabled' : ''}>Last »</button>
      </div>
    </div>
  `;

  container.innerHTML = `
    <div class="mik-subtopic-card">
      <div class="mik-subtopic-header">
        <div class="mik-subtopic-title">
          <span>📚 All Problems Catalog (1,526 Total · Showing Page ${mikState.allProbsPage} of ${totalPages})</span>
        </div>
      </div>
      <div class="mik-prob-list">
        ${listHtml || '<div style="padding:1.5rem; text-align:center; color:#94a3b8; font-size:13px;">No problems match current filters.</div>'}
      </div>
    </div>
    ${paginationHtml}
  `;
}

function setMikAllPage(page) {
  mikState.allProbsPage = page;
  saveMikState();
  renderMikContent();
  window.scrollTo({ top: 380, behavior: 'smooth' });
}

// --------------------------------------------------------------------------
// MAIN CONTENT ROUTER
// --------------------------------------------------------------------------
function renderMikContent() {
  const mode = mikState.currentMode || 'playlist';
  if (mode === 'playlist') {
    renderMikPlaylistView();
  } else if (mode === 'roadmap') {
    renderMikRoadmapView();
  } else if (mode === 'pattern') {
    renderMikPatternView();
  } else if (mode === 'repo') {
    renderMikRepoView();
  } else {
    renderMikAllProblemsView();
  }
}

// --------------------------------------------------------------------------
// SIDEBAR POPULATION (Context-Aware & Synchronized)
// --------------------------------------------------------------------------
function populateMikNav() {
  const sidebar = document.getElementById('mikTopicNavSidebar');
  if (!sidebar) return;

  const mode = mikState.currentMode || 'playlist';
  let html = '';

  if (mode === 'playlist') {
    const playlists = getMikPlaylists();
    html += `<div class="mik-sidebar-heading">Verified Playlists (${playlists.length})</div>`;
    playlists.forEach(pl => {
      let solved = 0;
      let matched = 0;
      pl.videos.forEach(v => {
        if (v.problem_id) {
          matched++;
          if (mikState.problems[v.problem_id]?.done) solved++;
        }
      });
      const isActive = pl.id === mikState.activePlaylistId;
      html += `
        <button class="mik-topic-nav-btn ${isActive ? 'active' : ''}" onclick="setMikActivePlaylist('${pl.id}')" title="${pl.title}">
          <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">🎬 ${pl.title.replace(': Popular Interview Problems', '').replace(': Convert Story To Code', '')}</span>
          <span class="mik-topic-nav-badge">${solved}/${matched}</span>
        </button>
      `;
    });
  } else if (mode === 'roadmap') {
    const stages = getMikLearningOrder();
    html += `<div class="mik-sidebar-heading">Roadmap (5 Stages)</div>`;
    html += `
      <button class="mik-topic-nav-btn ${(!mikState.activeStageId || mikState.activeStageId === 'all') ? 'active' : ''}" onclick="setMikActiveStage('all')">
        <span>🗺️ All 5 Stages</span>
        <span class="mik-topic-nav-badge">1526</span>
      </button>
    `;
    stages.forEach(st => {
      let solved = 0;
      let total = 0;
      st.topics.forEach(t => {
        t.subtopics.forEach(sub => {
          sub.problem_ids.forEach(pid => {
            total++;
            if (mikState.problems[pid]?.done) solved++;
          });
        });
      });
      const isActive = st.stage_id === mikState.activeStageId;
      html += `
        <button class="mik-topic-nav-btn ${isActive ? 'active' : ''}" onclick="setMikActiveStage('${st.stage_id}')">
          <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">🗺️ ${st.stage_title.split(':')[0]}</span>
          <span class="mik-topic-nav-badge">${solved}/${total}</span>
        </button>
      `;
    });
  } else if (mode === 'pattern') {
    const patterns = getMikPatterns();
    const categories = Array.from(new Set(patterns.map(p => p.category)));
    html += `<div class="mik-sidebar-heading">Pattern Categories</div>`;
    html += `
      <button class="mik-topic-nav-btn ${mikState.activePatternCategory === 'all' ? 'active' : ''}" onclick="setMikActivePatternCategory('all')">
        <span>🧩 All Patterns</span>
        <span class="mik-topic-nav-badge">${patterns.length}</span>
      </button>
    `;
    categories.forEach(catName => {
      const count = patterns.filter(p => p.category === catName).length;
      const isActive = mikState.activePatternCategory === catName;
      html += `
        <button class="mik-topic-nav-btn ${isActive ? 'active' : ''}" onclick="setMikActivePatternCategory('${catName}')">
          <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">• ${catName}</span>
          <span class="mik-topic-nav-badge">${count}</span>
        </button>
      `;
    });
  } else {
    // Repo and All Problems modes: 23 Topics
    const cat = getMikCatalog();
    const topicsMap = {};
    cat.forEach(p => {
      if (!topicsMap[p.topic]) topicsMap[p.topic] = { total: 0, solved: 0 };
      topicsMap[p.topic].total++;
      if (mikState.problems[p.id]?.done) topicsMap[p.topic].solved++;
    });

    html += `<div class="mik-sidebar-heading">${mode === 'all' ? 'Filter by Topic' : 'Original Topics (23)'}</div>`;
    html += `
      <button class="mik-topic-nav-btn ${mikFilter.topic === 'all' ? 'active' : ''}" onclick="setMikTopic('all')">
        <span>📂 All Topics</span>
        <span class="mik-topic-nav-badge">${cat.length}</span>
      </button>
    `;
    Object.keys(topicsMap).sort().forEach(t => {
      const data = topicsMap[t];
      const isActive = mikFilter.topic === t;
      html += `
        <button class="mik-topic-nav-btn ${isActive ? 'active' : ''}" onclick="setMikTopic('${t}')">
          <span style="overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${t}</span>
          <span class="mik-topic-nav-badge">${data.solved}/${data.total}</span>
        </button>
      `;
    });
  }

  sidebar.innerHTML = html;
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  loadMikState();
  updateMikStats();
});
"""

html = html[:js_start] + upgraded_js + "\n\n" + html[js_end:]

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved index.html with completely synchronized 5-mode workspace!")
