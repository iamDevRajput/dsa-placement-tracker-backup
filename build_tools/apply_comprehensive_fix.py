import os
import re

INDEX_PATH = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# ------------------------------------------------------------------------------
# 1. ENSURE SCRIPT TAGS IN HEAD
# ------------------------------------------------------------------------------
scripts_block = """  <script src="data/mik_catalog.js"></script>
  <script src="data/mik_playlists.js"></script>
  <script src="data/mik_learning_order.js"></script>
  <script src="data/mik_patterns.js"></script>"""

if '<script src="data/mik_playlists.js"></script>' not in html:
    html = html.replace('<script src="data/mik_catalog.js"></script>', scripts_block)

# ------------------------------------------------------------------------------
# 2. INJECT ROBUST, PROPERLY SCOPED DARK-THEME MIK CSS
# ------------------------------------------------------------------------------
css_start = html.find("/* ==========================================================================\n   MIK INTERVIEW DSA SECTION STYLING")
css_end = html.find("</style>", css_start)

if css_start == -1 or css_end == -1:
    print(f"Error finding CSS markers: css_start={css_start}, css_end={css_end}")
    exit(1)

dark_mik_css = """/* ==========================================================================
   MIK INTERVIEW DSA SECTION STYLING (PROPERLY SCOPED DARK THEME)
   ========================================================================== */

/* Hero Header */
.mik-hero-header {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  gap: 1.5rem;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(15, 23, 42, 0.75) 100%);
  border: 1px solid rgba(239, 68, 68, 0.28);
  border-radius: var(--radius-lg, 16px);
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

button.mik-action-btn {
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
  transition: all 0.15s ease !important;
}

button.mik-action-btn:hover {
  background: rgba(255, 255, 255, 0.12) !important;
  border-color: rgba(255, 255, 255, 0.25) !important;
  color: #ffffff !important;
}

button.mik-action-btn.primary {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
  border-color: #ef4444 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 14px rgba(239, 68, 68, 0.35) !important;
}

button.mik-action-btn.primary:hover {
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

/* 5-Mode Tabs Bar */
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
print("Injected properly scoped dark-theme MIK CSS")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved index.html with dark CSS!")
