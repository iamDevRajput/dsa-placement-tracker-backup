import re
import os

INDEX_PATH = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Head Script Tags for Manifests
manifest_scripts = """  <script src="data/mik_catalog.js"></script>
  <script src="data/mik_playlists.js"></script>
  <script src="data/mik_learning_order.js"></script>
  <script src="data/mik_patterns.js"></script>"""

if '<script src="data/mik_playlists.js"></script>' not in html:
    html = html.replace('<script src="data/mik_catalog.js"></script>', manifest_scripts)
    print("Updated script tags in <head> for MIK manifests")

# 2. Upgrade CSS
# We will locate the start of MIK CSS and replace it with the comprehensive upgraded CSS
css_start = html.find("/* ==========================================================================\n   MIK INTERVIEW DSA SECTION STYLING")
css_end = html.find("/* ==========================================================================\n   REVISION CENTER / SPACED REPETITION")

if css_start != -1 and css_end != -1:
    upgraded_css = """/* ==========================================================================
   MIK INTERVIEW DSA SECTION STYLING (UPGRADED 4-MODE WORKSPACE)
   ========================================================================== */
.mik-hero-header {
  display: flex;
  justify-content: space-between;
  align-items: stretch;
  gap: 1.5rem;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(15, 23, 42, 0.6) 100%);
  border: 1px solid rgba(239, 68, 68, 0.25);
  border-radius: var(--radius-lg, 16px);
  padding: 1.75rem 2rem;
  margin-bottom: 1.25rem;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(12px);
}

.mik-hero-header::before {
  content: '';
  position: absolute;
  top: -50px;
  right: -50px;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(239, 68, 68, 0.15) 0%, transparent 70%);
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
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.3);
  padding: 0.3rem 0.75rem;
  border-radius: var(--radius-full, 9999px);
  font-size: 11.5px;
  font-weight: 700;
  color: #ef4444;
  letter-spacing: 0.05em;
  margin-bottom: 0.75rem;
  width: fit-content;
}

.mik-hero-title {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.025em;
  color: #ffffff;
  margin-bottom: 0.4rem;
}

.mik-hero-subtitle {
  font-size: 13.5px;
  color: var(--text-dim, #94a3b8);
  line-height: 1.5;
  margin-bottom: 1rem;
}

.mik-hero-attributions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.mik-attribution-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.25rem 0.65rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: var(--radius-sm, 6px);
  font-size: 11.5px;
  color: var(--text-muted, #64748b);
  text-decoration: none;
  transition: all var(--transition-fast, 0.15s);
}

.mik-attribution-pill:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text, #f8fafc);
  border-color: rgba(255, 255, 255, 0.2);
}

.mik-hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  align-items: center;
}

.mik-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.45rem 0.95rem;
  border-radius: var(--radius-sm, 6px);
  font-size: 12.5px;
  font-weight: 600;
  cursor: pointer;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: var(--text, #f8fafc);
  transition: all var(--transition-fast, 0.15s);
}

.mik-action-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.25);
}

.mik-action-btn.primary {
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border-color: #ef4444;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.mik-action-btn.primary:hover {
  box-shadow: 0 6px 16px rgba(239, 68, 68, 0.45);
  transform: translateY(-1px);
}

.mik-hero-dashboard {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-md, 12px);
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
  color: #ffffff;
}

.mik-gauge-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-dim, #94a3b8);
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
  color: var(--text-dim, #94a3b8);
}

.mik-metric-main-stat {
  font-size: 1.75rem;
  font-weight: 800;
  color: #ffffff;
  line-height: 1.1;
}

.mik-metric-denom {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-dim, #94a3b8);
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
  border-radius: var(--radius-sm, 6px);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* 4-MODE SWITCHER TABS */
.mik-mode-tabs-bar {
  display: flex;
  gap: 0.5rem;
  background: rgba(15, 23, 42, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md, 12px);
  padding: 0.35rem;
  margin-bottom: 1.25rem;
  overflow-x: auto;
}

.mik-mode-tab {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.65rem 1rem;
  border-radius: var(--radius-sm, 8px);
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-dim, #94a3b8);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all var(--transition-fast, 0.15s);
}

.mik-mode-tab:hover {
  color: var(--text, #f8fafc);
  background: rgba(255, 255, 255, 0.05);
}

.mik-mode-tab.active {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.4);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
}

.mik-mode-icon {
  font-size: 15px;
}

.mik-mode-badge {
  font-size: 10.5px;
  padding: 0.1rem 0.45rem;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.08);
  color: var(--text-muted, #94a3b8);
}

.mik-mode-tab.active .mik-mode-badge {
  background: rgba(239, 68, 68, 0.3);
  color: #fca5a5;
}

/* CONTROLS BAR */
.mik-controls-bar {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-md, 12px);
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
  color: var(--text-muted, #64748b);
  pointer-events: none;
}

.mik-search-input {
  width: 100%;
  padding: 0.55rem 2.2rem 0.55rem 2.3rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-sm, 6px);
  color: var(--text, #f8fafc);
  font-size: 13px;
  outline: none;
  transition: all var(--transition-fast, 0.15s);
}

.mik-search-input:focus {
  border-color: rgba(239, 68, 68, 0.5);
  background: rgba(255, 255, 255, 0.07);
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.15);
}

.mik-search-clear {
  position: absolute;
  right: 0.6rem;
  background: none;
  border: none;
  color: var(--text-muted, #64748b);
  cursor: pointer;
  font-size: 15px;
  padding: 0.2rem;
}

.mik-filter-selects {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.mik-select {
  padding: 0.5rem 2rem 0.5rem 0.75rem;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-sm, 6px);
  color: var(--text, #f8fafc);
  font-size: 12.5px;
  outline: none;
  cursor: pointer;
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

.mik-pill {
  padding: 0.3rem 0.65rem;
  border-radius: var(--radius-sm, 6px);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--text-dim, #94a3b8);
  font-size: 12px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  transition: all var(--transition-fast, 0.15s);
}

.mik-pill:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text, #f8fafc);
}

.mik-pill.active {
  background: rgba(239, 68, 68, 0.15);
  border-color: rgba(239, 68, 68, 0.35);
  color: #ffffff;
  font-weight: 600;
}

/* WORKSPACE LAYOUT */
.mik-main-workspace {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.25rem;
  align-items: start;
}

@media (max-width: 1024px) {
  .mik-main-workspace {
    grid-template-columns: 1fr;
  }
}

.mik-topic-sidebar {
  background: rgba(15, 23, 42, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-md, 12px);
  padding: 0.85rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
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
  color: var(--text-dim, #94a3b8);
  padding: 0.35rem 0.5rem;
  margin-top: 0.25rem;
}

.mik-topic-nav-btn {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-sm, 6px);
  background: transparent;
  border: 1px solid transparent;
  color: var(--text-dim, #94a3b8);
  font-size: 12.5px;
  font-weight: 500;
  cursor: pointer;
  text-align: left;
  transition: all var(--transition-fast, 0.15s);
  width: 100%;
}

.mik-topic-nav-btn:hover {
  background: rgba(255, 255, 255, 0.04);
  color: var(--text, #f8fafc);
}

.mik-topic-nav-btn.active {
  background: rgba(239, 68, 68, 0.12);
  border-color: rgba(239, 68, 68, 0.25);
  color: #ffffff;
  font-weight: 600;
}

.mik-topic-nav-badge {
  font-size: 11px;
  font-family: var(--font-mono, monospace);
  color: var(--text-muted, #64748b);
  background: rgba(255, 255, 255, 0.04);
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
}

.mik-topic-nav-btn.active .mik-topic-nav-badge {
  color: #fca5a5;
  background: rgba(239, 68, 68, 0.2);
}

/* CONTENT AREA CARDS */
.mik-content-area {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  min-width: 0;
}

/* PLAYLIST HEADER CARD */
.mik-playlist-banner {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.07) 0%, rgba(30, 41, 59, 0.5) 100%);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: var(--radius-md, 12px);
  padding: 1.25rem 1.5rem;
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
  font-size: 1.3rem;
  font-weight: 800;
  color: #ffffff;
  margin-bottom: 0.35rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.mik-playlist-banner-desc {
  font-size: 12.5px;
  color: var(--text-dim, #94a3b8);
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

/* ROADMAP STAGES */
.mik-stage-card {
  background: rgba(15, 23, 42, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: var(--radius-md, 12px);
  overflow: hidden;
}

.mik-stage-header {
  padding: 1rem 1.25rem;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.mik-stage-header:hover {
  background: rgba(255, 255, 255, 0.04);
}

.mik-stage-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.mik-stage-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #ffffff;
}

.mik-stage-desc {
  font-size: 12px;
  color: var(--text-dim, #94a3b8);
  margin-top: 0.15rem;
}

.mik-stage-body {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

/* PATTERN CARDS */
.mik-pattern-card {
  background: rgba(15, 23, 42, 0.45);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: var(--radius-md, 12px);
  overflow: hidden;
}

.mik-pattern-header {
  padding: 0.9rem 1.25rem;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.mik-pattern-header:hover {
  background: rgba(255, 255, 255, 0.04);
}

.mik-pattern-title {
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mik-pattern-desc {
  font-size: 12px;
  color: var(--text-dim, #94a3b8);
  margin-top: 0.2rem;
}

/* SUBTOPIC / GROUP CARDS */
.mik-subtopic-card {
  background: rgba(15, 23, 42, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-md, 10px);
  overflow: hidden;
}

.mik-subtopic-header {
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.02);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
}

.mik-subtopic-header:hover {
  background: rgba(255, 255, 255, 0.04);
}

.mik-subtopic-title {
  font-size: 13.5px;
  font-weight: 700;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* PROBLEM ROWS */
.mik-prob-list {
  display: flex;
  flex-direction: column;
  divide-y: 1px solid rgba(255, 255, 255, 0.04);
}

.mik-prob-row {
  display: grid;
  grid-template-columns: 48px 1fr auto auto auto auto 36px;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.04);
  transition: background var(--transition-fast, 0.15s);
}

@media (max-width: 900px) {
  .mik-prob-row {
    grid-template-columns: 40px 1fr auto auto;
    row-gap: 0.5rem;
  }
}

.mik-prob-row:hover {
  background: rgba(255, 255, 255, 0.03);
}

.mik-prob-row.solved {
  background: rgba(16, 185, 129, 0.02);
}

.mik-prob-seq {
  font-size: 11.5px;
  font-family: var(--font-mono, monospace);
  font-weight: 700;
  color: var(--text-dim, #94a3b8);
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.mik-prob-seq.playlist-seq {
  color: #ef4444;
}

.mik-prob-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 0;
}

.mik-prob-title-link {
  color: var(--text, #f8fafc);
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: inline-block;
}

.mik-prob-title-link:hover {
  color: #ef4444;
}

.mik-prob-tags {
  display: flex;
  gap: 0.35rem;
  flex-wrap: wrap;
  align-items: center;
}

.mik-tag {
  font-size: 10.5px;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.07);
  color: var(--text-dim, #94a3b8);
  white-space: nowrap;
}

.mik-tag.company {
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.08);
  border-color: rgba(56, 189, 248, 0.2);
}

.mik-tag.tc {
  font-family: var(--font-mono, monospace);
  color: #fbbf24;
  background: rgba(251, 191, 36, 0.08);
  border-color: rgba(251, 191, 36, 0.2);
}

.mik-links-group {
  display: flex;
  gap: 0.35rem;
  align-items: center;
}

.mik-link-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: var(--radius-sm, 6px);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--text-dim, #94a3b8);
  text-decoration: none;
  font-size: 12px;
  transition: all var(--transition-fast, 0.15s);
}

.mik-link-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.2);
}

.mik-link-btn.yt:hover {
  color: #ef4444;
  border-color: rgba(239, 68, 68, 0.4);
}

.mik-link-btn.lc:hover {
  color: #f59e0b;
  border-color: rgba(245, 158, 11, 0.4);
}

.mik-status-dropdown {
  padding: 0.25rem 0.5rem;
  font-size: 11.5px;
  font-weight: 600;
  border-radius: var(--radius-sm, 6px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text, #f8fafc);
  cursor: pointer;
  outline: none;
}

.mik-status-dropdown.status-SOLVED {
  background: rgba(16, 185, 129, 0.15);
  border-color: rgba(16, 185, 129, 0.4);
  color: #34d399;
}

.mik-status-dropdown.status-IN_PROGRESS {
  background: rgba(245, 158, 11, 0.15);
  border-color: rgba(245, 158, 11, 0.4);
  color: #fbbf24;
}

.mik-status-dropdown.status-REVISE {
  background: rgba(168, 85, 247, 0.15);
  border-color: rgba(168, 85, 247, 0.4);
  color: #c084fc;
}

.mik-notes-indicator-btn {
  background: transparent;
  border: none;
  color: var(--text-dim, #94a3b8);
  cursor: pointer;
  font-size: 14px;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all var(--transition-fast, 0.15s);
}

.mik-notes-indicator-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: var(--text, #f8fafc);
}

.mik-notes-indicator-btn.has-notes {
  color: #38bdf8;
}

.mik-star-toggle-btn {
  background: transparent;
  border: none;
  color: var(--text-dim, #64748b);
  cursor: pointer;
  font-size: 15px;
  padding: 0.2rem;
  transition: all var(--transition-fast, 0.15s);
}

.mik-star-toggle-btn:hover {
  color: #f59e0b;
}

.mik-star-toggle-btn.starred {
  color: #fbbf24;
}

/* UNMATCHED VIDEOS ACCORDION */
.mik-unmatched-card {
  margin-top: 1rem;
  background: rgba(245, 158, 11, 0.05);
  border: 1px dashed rgba(245, 158, 11, 0.3);
  border-radius: var(--radius-md, 10px);
  padding: 0.85rem 1.1rem;
}

.mik-unmatched-header {
  font-size: 13px;
  font-weight: 700;
  color: #fbbf24;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

/* MODAL PLAYLIST NAVIGATOR */
.mik-modal-playlist-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.6rem 0.85rem;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  border-radius: var(--radius-sm, 8px);
  margin-bottom: 1rem;
  font-size: 12px;
}

.mik-nav-step-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.3rem 0.65rem;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-sm, 6px);
  color: var(--text, #f8fafc);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
}

.mik-nav-step-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.12);
}

.mik-nav-step-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* EMPTY STATES */
.mik-empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
  background: rgba(15, 23, 42, 0.3);
  border: 1px dashed rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md, 12px);
  color: var(--text-dim, #94a3b8);
}

.mik-empty-icon {
  font-size: 2.2rem;
  margin-bottom: 0.75rem;
}

.mik-empty-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 0.35rem;
}

.mik-empty-desc {
  font-size: 13px;
  max-width: 420px;
  margin: 0 auto 1.25rem;
  line-height: 1.5;
}
"""
    html = html[:css_start] + upgraded_css + "\n" + html[css_end:]
    print("Replaced MIK CSS with upgraded 4-mode CSS")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated index.html with CSS")
