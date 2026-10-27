# Integration script for MIK Interview DSA Section
import os
import re

INDEX_PATH = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add script tag in head if not present
if '<script src="data/mik_catalog.js"></script>' not in html:
    html = html.replace('</head>', '  <script src="data/mik_catalog.js"></script>\n</head>')
    print("Added data/mik_catalog.js script tag to head")

# 2. Add Sidebar Navigation Item
sidebar_target = '<span class="nav-badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3);" id="nav-risingbrain-badge">0/385</span>\n    </button>'
mik_nav_button = """<span class="nav-badge" style="background:rgba(16,185,129,0.15); color:#10b981; border:1px solid rgba(16,185,129,0.3);" id="nav-risingbrain-badge">0/385</span>
    </button>
    <button class="nav-item" onclick="switchView('mik', this)">
      <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
      <span>MIK Interview DSA</span>
      <span class="nav-badge" style="background:rgba(239,68,68,0.15); color:#ef4444; border:1px solid rgba(239,68,68,0.3);" id="nav-mik-badge">0/1526</span>
    </button>"""

if 'switchView(\'mik\', this)' not in html:
    if sidebar_target in html:
        html = html.replace(sidebar_target, mik_nav_button)
        print("Inserted MIK Interview DSA sidebar button")
    else:
        print("Warning: sidebar_target not found!")
else:
    print("Sidebar button already present")

# 3. Add CSS Styles
mik_css = """
/* ==========================================================================
   MIK INTERVIEW DSA SECTION STYLING
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
  margin-bottom: 1.5rem;
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
  border-radius: 9999px;
  font-size: 11.5px;
  font-weight: 600;
  color: #fca5a5;
  margin-bottom: 0.75rem;
  width: fit-content;
}

.mik-pulse-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #ef4444;
  box-shadow: 0 0 8px #ef4444;
  animation: mikPulse 2s infinite ease-in-out;
}

@keyframes mikPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.mik-hero-title {
  font-family: var(--font-heading);
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: #ffffff;
  margin-bottom: 0.4rem;
}

.mik-hero-subtitle {
  font-size: 13px;
  line-height: 1.55;
  color: #94a3b8;
  margin-bottom: 1.15rem;
}

.mik-hero-attribution {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  margin-bottom: 1.15rem;
  font-size: 12px;
}

.mik-attr-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  color: #cbd5e1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 0.25rem 0.65rem;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s ease;
}

.mik-attr-link:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.4);
  color: #ffffff;
}

.mik-hero-actions {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.mik-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #e2e8f0;
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius-md, 8px);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mik-action-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-1px);
}

.mik-action-btn.primary {
  background: #ef4444;
  border-color: #dc2626;
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
}

.mik-action-btn.primary:hover {
  background: #dc2626;
}

.mik-hero-dashboard {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  background: rgba(15, 23, 42, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: var(--radius-md, 12px);
  padding: 1.25rem 1.75rem;
  min-width: 380px;
}

.mik-radial-gauge-container {
  position: relative;
  width: 96px;
  height: 96px;
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
  stroke-dasharray: 264;
  stroke-dashoffset: 264;
  transition: stroke-dashoffset 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.mik-radial-content {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.mik-gauge-pct {
  font-family: var(--font-heading);
  font-size: 20px;
  font-weight: 800;
  color: #ffffff;
}

.mik-gauge-label {
  font-size: 10px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.mik-metric-info {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.mik-metric-heading {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #94a3b8;
}

.mik-metric-main-stat {
  font-family: var(--font-heading);
  font-size: 24px;
  font-weight: 800;
  color: #ffffff;
}

.mik-metric-denom {
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
}

.mik-quick-chips {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
  margin-top: 0.35rem;
}

.mik-quick-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 11px;
  font-weight: 600;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: #cbd5e1;
}

.mik-quick-chip.solved { background: rgba(16, 185, 129, 0.12); color: #34d399; border-color: rgba(16, 185, 129, 0.25); }
.mik-quick-chip.inprogress { background: rgba(245, 158, 11, 0.12); color: #fbbf24; border-color: rgba(245, 158, 11, 0.25); }
.mik-quick-chip.revise { background: rgba(139, 92, 246, 0.12); color: #c084fc; border-color: rgba(139, 92, 246, 0.25); }
.mik-quick-chip.starred { background: rgba(251, 191, 36, 0.12); color: #fde047; border-color: rgba(251, 191, 36, 0.25); }

/* CONTROLS BAR */
.mik-controls-bar {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg, 12px);
  padding: 1rem 1.25rem;
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
}

.mik-controls-top {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.mik-search-wrapper {
  position: relative;
  flex: 1;
  min-width: 280px;
}

.mik-search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-dim, #64748b);
  pointer-events: none;
}

.mik-search-input {
  width: 100%;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius-md, 8px);
  padding: 0.55rem 2.2rem 0.55rem 2.25rem;
  color: var(--text);
  font-size: 13px;
  outline: none;
  transition: all 0.2s ease;
}

.mik-search-input:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.15);
}

.mik-search-clear {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-dim, #64748b);
  cursor: pointer;
  font-size: 13px;
}

.mik-filter-selects {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.mik-select {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius-md, 8px);
  padding: 0.55rem 1rem;
  color: var(--text);
  font-size: 12.5px;
  outline: none;
  cursor: pointer;
}

.mik-select:focus {
  border-color: #ef4444;
}

.mik-filter-pills-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.mik-pill-group {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.mik-pill {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 9999px;
  padding: 0.35rem 0.85rem;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.mik-pill:hover {
  background: var(--surface3);
  color: var(--text);
}

.mik-pill.active {
  background: #ef4444;
  border-color: #ef4444;
  color: #ffffff;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.25);
}

.mik-pill-count {
  font-size: 10px;
  padding: 0.1rem 0.4rem;
  border-radius: 9999px;
  background: rgba(0, 0, 0, 0.15);
}

.mik-pill.active .mik-pill-count {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

/* WORKSPACE */
.mik-main-workspace {
  display: flex;
  gap: 1.5rem;
  align-items: flex-start;
}

.mik-topic-sidebar {
  width: 250px;
  flex-shrink: 0;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg, 12px);
  padding: 0.75rem;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
  position: sticky;
  top: 85px;
}

.mik-topic-side-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.55rem 0.75rem;
  border-radius: var(--radius-md, 8px);
  background: transparent;
  border: none;
  color: var(--text-muted);
  font-size: 12.5px;
  text-align: left;
  cursor: pointer;
  transition: all 0.15s ease;
  margin-bottom: 2px;
}

.mik-topic-side-btn:hover {
  background: var(--surface2);
  color: var(--text);
}

.mik-topic-side-btn.active {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
  font-weight: 600;
  border-left: 3px solid #ef4444;
}

.mik-topic-side-badge {
  font-size: 10.5px;
  font-family: var(--font-mono);
  color: var(--text-dim);
}

.mik-content-area {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* SUBTOPIC CARDS */
.mik-subtopic-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg, 12px);
  overflow: hidden;
  transition: border-color 0.2s ease;
}

.mik-subtopic-card:hover {
  border-color: rgba(239, 68, 68, 0.35);
}

.mik-subtopic-header {
  padding: 0.9rem 1.25rem;
  background: var(--surface2);
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
}

.mik-subtopic-title-group {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.mik-subtopic-chevron {
  transition: transform 0.2s ease;
  color: var(--text-dim);
}

.mik-subtopic-card.collapsed .mik-subtopic-chevron {
  transform: rotate(-90deg);
}

.mik-subtopic-card.collapsed .mik-problems-list {
  display: none;
}

.mik-subtopic-title {
  font-family: var(--font-heading);
  font-size: 14.5px;
  font-weight: 700;
  color: var(--text);
}

.mik-subtopic-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.mik-subtopic-progress-wrap {
  width: 90px;
  height: 6px;
  background: var(--surface3);
  border-radius: 9999px;
  overflow: hidden;
}

.mik-subtopic-progress-fill {
  height: 100%;
  background: #ef4444;
  border-radius: 9999px;
  transition: width 0.3s ease;
}

.mik-subtopic-ratio {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-dim);
}

/* PROBLEM ROWS */
.mik-problems-list {
  display: flex;
  flex-direction: column;
}

.mik-problem-row {
  display: grid;
  grid-template-columns: 36px 32px 1fr auto auto auto;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  border-bottom: 1px solid var(--border-subtle);
  transition: background 0.15s ease;
}

.mik-problem-row:last-child {
  border-bottom: none;
}

.mik-problem-row:hover {
  background: var(--surface2);
}

.mik-status-toggle {
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 1.5px solid var(--border);
  background: transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.mik-status-toggle.done {
  background: #10b981;
  border-color: #10b981;
  color: #ffffff;
}

.mik-status-toggle.inprogress {
  background: #f59e0b;
  border-color: #f59e0b;
  color: #ffffff;
}

.mik-status-toggle.revise {
  background: #8b5cf6;
  border-color: #8b5cf6;
  color: #ffffff;
}

.mik-star-btn {
  background: none;
  border: none;
  color: var(--text-dim);
  cursor: pointer;
  font-size: 15px;
  transition: transform 0.15s ease, color 0.15s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mik-star-btn:hover {
  transform: scale(1.15);
  color: #f59e0b;
}

.mik-star-btn.starred {
  color: #f59e0b;
}

.mik-prob-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.mik-prob-title-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.mik-prob-title {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text);
  text-decoration: none;
  word-break: break-word;
}

.mik-prob-sub-badge {
  font-size: 10.5px;
  padding: 0.1rem 0.45rem;
  border-radius: 4px;
  background: var(--surface3);
  color: var(--text-muted);
}

.mik-prob-tags-row {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: wrap;
}

.mik-company-tag {
  font-size: 10px;
  padding: 0.08rem 0.4rem;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  color: var(--text-muted);
}

.mik-comp-chip {
  font-size: 10px;
  font-weight: 500;
  padding: 0.08rem 0.38rem;
  border-radius: 4px;
  background: rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
  color: #fca5a5;
}

.mik-complexity-chip {
  font-family: var(--font-mono);
  font-size: 10px;
  padding: 0.08rem 0.38rem;
  border-radius: 4px;
  background: rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.2);
  color: #93c5fd;
}

.mik-links-group {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.mik-link-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 11px;
  font-weight: 600;
  padding: 0.25rem 0.55rem;
  border-radius: 6px;
  text-decoration: none;
  transition: all 0.2s ease;
}

.mik-link-badge.yt {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.mik-link-badge.yt:hover {
  background: #ef4444;
  color: #ffffff;
}

.mik-link-badge.lc {
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: #f59e0b;
}

.mik-link-badge.lc:hover {
  background: #f59e0b;
  color: #ffffff;
}

.mik-link-badge.gfg {
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: #10b981;
}

.mik-link-badge.gfg:hover {
  background: #10b981;
  color: #ffffff;
}

.mik-link-badge.code {
  background: rgba(148, 163, 184, 0.1);
  border: 1px solid rgba(148, 163, 184, 0.2);
  color: #cbd5e1;
}

.mik-link-badge.code:hover {
  background: rgba(148, 163, 184, 0.25);
  color: #ffffff;
}

.mik-notes-btn {
  background: var(--surface2);
  border: 1px solid var(--border);
  color: var(--text-muted);
  border-radius: 6px;
  padding: 0.3rem 0.55rem;
  font-size: 11.5px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  transition: all 0.2s ease;
  position: relative;
}

.mik-notes-btn:hover {
  background: var(--surface3);
  color: var(--text);
}

.mik-notes-btn.has-notes {
  background: rgba(139, 92, 246, 0.12);
  border-color: rgba(139, 92, 246, 0.3);
  color: #c084fc;
}

.mik-notes-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #a855f7;
}

.mik-details-btn {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-dim);
  border-radius: 6px;
  padding: 0.3rem 0.5rem;
  font-size: 11px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mik-details-btn:hover {
  background: var(--surface2);
  color: var(--text);
  border-color: rgba(255, 255, 255, 0.2);
}

/* DETAIL MODAL */
.mik-modal-card {
  max-width: 650px;
  width: 95%;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg, 16px);
  padding: 1.75rem;
  box-shadow: var(--shadow-lg);
  max-height: 90vh;
  overflow-y: auto;
}

.mik-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border);
}

.mik-modal-prob-id {
  font-family: var(--font-mono);
  font-size: 11px;
  color: #ef4444;
  margin-bottom: 0.25rem;
}

.mik-modal-title {
  font-family: var(--font-heading);
  font-size: 19px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.35;
}

.mik-modal-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.mik-meta-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 0.75rem;
  background: var(--surface2);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md, 8px);
  padding: 0.9rem 1rem;
  margin-bottom: 1.25rem;
}

.mik-meta-item {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.mik-meta-label {
  font-size: 10px;
  text-transform: uppercase;
  color: var(--text-dim);
  font-weight: 600;
  letter-spacing: 0.5px;
}

.mik-meta-value {
  font-size: 12.5px;
  color: var(--text);
  font-family: var(--font-mono);
  word-break: break-word;
}

.mik-links-bar {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
  margin-bottom: 1.25rem;
}

.mik-approach-box {
  background: var(--surface2);
  border-left: 3px solid #ef4444;
  border-radius: 4px;
  padding: 0.75rem 1rem;
  margin-bottom: 1.25rem;
  font-size: 12.5px;
  color: var(--text-muted);
  line-height: 1.5;
}

.mik-notes-editor-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.mik-notes-textarea {
  width: 100%;
  min-height: 140px;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: var(--radius-md, 8px);
  padding: 0.75rem 1rem;
  color: var(--text);
  font-family: inherit;
  font-size: 13px;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s ease;
}

.mik-notes-textarea:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 2px rgba(239, 68, 68, 0.15);
}

.mik-status-select-btn-group {
  display: flex;
  gap: 0.4rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}

.mik-status-btn {
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface2);
  color: var(--text-muted);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.mik-status-btn.active {
  color: #ffffff;
  font-weight: 600;
}

.mik-status-btn[data-status="NOT_STARTED"].active { background: #64748b; border-color: #64748b; }
.mik-status-btn[data-status="IN_PROGRESS"].active { background: #f59e0b; border-color: #f59e0b; }
.mik-status-btn[data-status="SOLVED"].active { background: #10b981; border-color: #10b981; }
.mik-status-btn[data-status="REVISE"].active { background: #8b5cf6; border-color: #8b5cf6; }
"""

if 'MIK INTERVIEW DSA SECTION STYLING' not in html:
    html = html.replace('</style>', mik_css + '\n</style>')
    print("Added MIK CSS styles")

# 4. Add HTML Section <section class="view-section" id="view-mik">
view_mik_html = """
    <!-- VIEW: MIK INTERVIEW DSA -->
    <section class="view-section" id="view-mik">
      <!-- 1. HERO BANNER & COMPACT DASHBOARD -->
      <div class="mik-hero-header">
        <div class="mik-hero-left">
          <div class="mik-hero-badge">
            <span class="mik-pulse-dot"></span>
            <span>codestorywithMIK Curriculum</span>
            <span class="mik-badge-tag">1526 Problems · 74 Subtopics · 23 Topics</span>
          </div>
          <h1 class="mik-hero-title">MIK Interview DSA</h1>
          <p class="mik-hero-subtitle">
            Curated from Mazhar Imam Khan's (codestorywithMIK) battle-tested repository. Features video explanations, company tags, LeetCode & GFG problems, and direct links to original C++ solutions.
          </p>
          <div class="mik-hero-attribution">
            <a href="https://github.com/MAZHARMIK/Interview_DS_Algo" target="_blank" rel="noopener noreferrer" class="mik-attr-link">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/></svg>
              <span>Source: MAZHARMIK / Interview_DS_Algo</span>
            </a>
            <a href="https://www.youtube.com/@codestorywithMIK" target="_blank" rel="noopener noreferrer" class="mik-attr-link">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="#ef4444"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
              <span>YouTube: codestorywithMIK</span>
            </a>
          </div>
          <div class="mik-hero-actions">
            <button class="mik-action-btn primary" onclick="jumpToNextUnsolvedMikProblem()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <span>Resume Next Problem</span>
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

      <!-- 2. SEARCH & ADVANCED FILTER CONTROLS -->
      <div class="mik-controls-bar">
        <div class="mik-controls-top">
          <div class="mik-search-wrapper">
            <svg class="mik-search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="text" id="mikSearchInput" class="mik-search-input" placeholder="Search 1526 problems, company (e.g. Amazon), topic, approaches, complexity..." oninput="handleMikSearch(this.value)">
            <button id="mikSearchClearBtn" class="mik-search-clear" onclick="clearMikSearch()" title="Clear search" style="display:none;">✕</button>
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
          </div>
        </div>

        <div class="mik-filter-pills-row">
          <div class="mik-pill-group">
            <button class="mik-pill active" id="f-mik-all" onclick="setMikStatusFilter('all', this)">All <span class="mik-pill-count" id="mikPillAllCnt">1526</span></button>
            <button class="mik-pill" id="f-mik-solved" onclick="setMikStatusFilter('solved', this)">🟢 Solved <span class="mik-pill-count" id="mikPillSolvedCnt">0</span></button>
            <button class="mik-pill" id="f-mik-inprogress" onclick="setMikStatusFilter('inprogress', this)">🟡 In Progress <span class="mik-pill-count" id="mikPillInProgCnt">0</span></button>
            <button class="mik-pill" id="f-mik-revise" onclick="setMikStatusFilter('revise', this)">🟣 Needs Revise <span class="mik-pill-count" id="mikPillReviseCnt">0</span></button>
            <button class="mik-pill" id="f-mik-unsolved" onclick="setMikStatusFilter('unsolved', this)">Unattempted</button>
            <button class="mik-pill" id="f-mik-starred" onclick="setMikStatusFilter('starred', this)">⭐ Starred <span class="mik-pill-count" id="mikPillStarredCnt">0</span></button>
            <button class="mik-pill" id="f-mik-notes" onclick="setMikStatusFilter('notes', this)">📝 With Notes <span class="mik-pill-count" id="mikPillNotesCnt">0</span></button>
          </div>
        </div>
      </div>

      <!-- 3. MAIN WORKSPACE: TOPIC SIDEBAR & CONTENT -->
      <div class="mik-main-workspace">
        <aside class="mik-topic-sidebar" id="mikTopicNavSidebar">
          <!-- Populated dynamically with all 23 topics -->
        </aside>

        <div class="mik-content-area" id="mikContentArea">
          <!-- Populated dynamically with subtopic cards and problem rows -->
        </div>
      </div>
    </section>
"""

risingbrain_end = '</section>\n\n    <!-- VIEW 3: REVISION CENTER -->'
if 'id="view-mik"' not in html:
    if risingbrain_end in html:
        html = html.replace(risingbrain_end, '</section>\n' + view_mik_html + '\n    <!-- VIEW 3: REVISION CENTER -->')
        print("Inserted view-mik section HTML")
    else:
        # Fallback before coresubjects
        cs_target = '<section class="view-section" id="view-coresubjects">'
        if cs_target in html:
            html = html.replace(cs_target, view_mik_html + '\n' + cs_target)
            print("Inserted view-mik section HTML before coresubjects")
        else:
            print("Warning: could not locate insertion target for view-mik!")

# 5. Add Modal Detail View for MIK Problem
modal_mik_html = """
<!-- MIK PROBLEM DETAIL & NOTES MODAL -->
<div class="modal-overlay" id="modalMikDetail">
  <div class="mik-modal-card">
    <div class="mik-modal-header">
      <div>
        <div class="mik-modal-prob-id" id="mikModalProbId">MIK #0001</div>
        <h2 class="mik-modal-title" id="mikModalTitle">Problem Title</h2>
        <div style="font-size:12px; color:var(--text-muted); margin-top:2px;" id="mikModalTopicSubtopic">Topic > Subtopic</div>
      </div>
      <div class="mik-modal-actions">
        <button class="mik-star-btn" id="mikModalStarBtn" onclick="toggleMikModalStar()" title="Toggle Star">⭐</button>
        <button class="modal-close" onclick="closeModal('modalMikDetail')">&times;</button>
      </div>
    </div>

    <!-- Quick Links Bar -->
    <div class="mik-links-bar" id="mikModalLinksBar">
      <!-- Populated dynamically with YouTube, LeetCode, GFG, GitHub links -->
    </div>

    <!-- Metadata Grid -->
    <div class="mik-meta-grid" id="mikModalMetaGrid">
      <div class="mik-meta-item">
        <span class="mik-meta-label">Time Complexity</span>
        <span class="mik-meta-value" id="mikModalTc">-</span>
      </div>
      <div class="mik-meta-item">
        <span class="mik-meta-label">Space Complexity</span>
        <span class="mik-meta-value" id="mikModalSc">-</span>
      </div>
      <div class="mik-meta-item">
        <span class="mik-meta-label">Frequency</span>
        <span class="mik-meta-value" id="mikModalFreq">-</span>
      </div>
      <div class="mik-meta-item" style="grid-column: 1 / -1;">
        <span class="mik-meta-label">Companies</span>
        <span class="mik-meta-value" id="mikModalCompanies" style="font-family:inherit;">-</span>
      </div>
    </div>

    <!-- Approach Box -->
    <div class="mik-approach-box" id="mikModalApproachBox" style="display:none;">
      <div style="font-weight:700; color:var(--text); margin-bottom:0.25rem;">Approach &amp; Method Clues</div>
      <div id="mikModalApproachText"></div>
    </div>

    <!-- Status Selector -->
    <div style="margin-bottom:1.25rem;">
      <div style="font-size:11.5px; font-weight:600; text-transform:uppercase; color:var(--text-dim); margin-bottom:0.35rem;">Status</div>
      <div class="mik-status-select-btn-group" id="mikModalStatusGroup">
        <button class="mik-status-btn" data-status="NOT_STARTED" onclick="setMikModalStatus('NOT_STARTED')">⚪ Not Started</button>
        <button class="mik-status-btn" data-status="IN_PROGRESS" onclick="setMikModalStatus('IN_PROGRESS')">🟡 In Progress</button>
        <button class="mik-status-btn" data-status="SOLVED" onclick="setMikModalStatus('SOLVED')">🟢 Solved</button>
        <button class="mik-status-btn" data-status="REVISE" onclick="setMikModalStatus('REVISE')">🟣 Needs Revise</button>
      </div>
    </div>

    <!-- Personal Notes Editor -->
    <div class="mik-notes-editor-wrap">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <label style="font-size:12px; font-weight:600; color:var(--text);">Personal Multiline Notes</label>
        <div style="display:flex; gap:0.5rem; align-items:center;">
          <span style="font-size:11px; font-family:var(--font-mono); color:var(--text-dim);" id="mikNotesCharCount">0 chars</span>
          <button class="btn btn-secondary" style="padding:0.25rem 0.6rem; font-size:11px;" onclick="copyMikNotesToClipboard()">📋 Copy</button>
        </div>
      </div>
      <textarea id="mikModalNotesTextarea" class="mik-notes-textarea" placeholder="Write or paste your personal approach notes, key observations, edge cases, mistakes to avoid, code snippets..." oninput="handleMikModalNotesInput(this.value)"></textarea>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.35rem;">
        <span style="font-size:11.5px; color:#10b981;" id="mikNotesSaveIndicator">Auto-saved locally</span>
        <button class="btn btn-primary" style="padding:0.35rem 0.85rem; font-size:12px;" onclick="saveMikModalNotesExplicitly()">Save Notes</button>
      </div>
    </div>
  </div>
</div>
"""

if 'id="modalMikDetail"' not in html:
    toast_pos = '<div class="toast-container" id="toastContainer"></div>'
    if toast_pos in html:
        html = html.replace(toast_pos, modal_mik_html + '\n' + toast_pos)
        print("Inserted modalMikDetail HTML")

# 6. Add JavaScript Engine for MIK Interview DSA
mik_js = """
/* ==========================================================================
   MIK INTERVIEW DSA STATE & ENGINE
   ========================================================================== */
const STORAGE_MIK_KEY = 'mik_interview_dsa_tracker_v1';

let mikState = {
  version: 1,
  problems: {},
  collapsedTopics: {},
  collapsedSubtopics: {}
};

let mikFilter = {
  topic: 'all',
  company: 'all',
  status: 'all',
  search: ''
};

let activeMikModalProbId = null;
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
          collapsedSubtopics: parsed.collapsedSubtopics || {}
        };
        return;
      }
    }
  } catch (e) {
    console.error('Error loading MIK state:', e);
  }
  mikState = { version: 1, problems: {}, collapsedTopics: {}, collapsedSubtopics: {} };
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
  if (window.MIK_CATALOG_DATA && Array.isArray(window.MIK_CATALOG_DATA)) {
    return window.MIK_CATALOG_DATA;
  }
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

  const pct = Math.round((solved / total) * 100);

  const pctEl = document.getElementById('mikRadialPct');
  if (pctEl) pctEl.textContent = `${pct}%`;

  const gauge = document.getElementById('mikGaugeCircle');
  if (gauge) {
    const circumference = 2 * Math.PI * 42; // ~264
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

function populateMikNav() {
  const cat = getMikCatalog();
  const topicMap = {};

  cat.forEach(p => {
    if (!topicMap[p.topic]) {
      topicMap[p.topic] = { total: 0, solved: 0 };
    }
    topicMap[p.topic].total++;
    const ps = mikState.problems[p.id];
    if (ps && ps.done) topicMap[p.topic].solved++;
  });

  const sidebar = document.getElementById('mikTopicNavSidebar');
  const dropdown = document.getElementById('mikTopicDropdown');

  if (sidebar) {
    let sideHtml = '';
    Object.keys(topicMap).sort().forEach(t => {
      const info = topicMap[t];
      const isActive = mikFilter.topic === t ? ' active' : '';
      sideHtml += `
        <button class="mik-topic-side-btn${isActive}" onclick="setMikTopic('${t.replace(/'/g, "\\'")}')">
          <span>${t}</span>
          <span class="mik-topic-side-badge">${info.solved}/${info.total}</span>
        </button>
      `;
    });
    sidebar.innerHTML = sideHtml;
  }

  if (dropdown && dropdown.options.length <= 1) {
    let optHtml = '<option value="all">📂 All 23 Topics (' + cat.length + ')</option>';
    Object.keys(topicMap).sort().forEach(t => {
      optHtml += `<option value="${t}">${t} (${topicMap[t].total})</option>`;
    });
    dropdown.innerHTML = optHtml;
  }
}

function renderMikContent() {
  const cat = getMikCatalog();
  const container = document.getElementById('mikContentArea');
  if (!container) return;

  const q = mikFilter.search.toLowerCase().trim();

  // Filter problems
  const filtered = cat.filter(p => {
    if (mikFilter.topic !== 'all' && p.topic !== mikFilter.topic) return false;
    if (mikFilter.company !== 'all') {
      const matchComp = p.companies.some(c => c.toLowerCase() === mikFilter.company.toLowerCase());
      if (!matchComp) return false;
    }
    const ps = getMikProblemState(p.id);
    if (mikFilter.status === 'solved' && !ps.done) return false;
    if (mikFilter.status === 'inprogress' && ps.status !== 'IN_PROGRESS') return false;
    if (mikFilter.status === 'revise' && ps.status !== 'REVISE') return false;
    if (mikFilter.status === 'unsolved' && ps.done) return false;
    if (mikFilter.status === 'starred' && !ps.starred) return false;
    if (mikFilter.status === 'notes' && (!ps.notes || !ps.notes.trim())) return false;

    if (q) {
      const inTitle = p.title.toLowerCase().includes(q);
      const inTopic = p.topic.toLowerCase().includes(q);
      const inSubtopic = p.subtopic.toLowerCase().includes(q);
      const inComp = p.companies.some(c => c.toLowerCase().includes(q));
      const inApp = p.approaches.some(a => a.toLowerCase().includes(q));
      if (!inTitle && !inTopic && !inSubtopic && !inComp && !inApp) return false;
    }
    return true;
  });

  if (filtered.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:3rem 1rem; color:var(--text-dim); background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-lg);">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:0.75rem; opacity:0.6;"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <div style="font-size:16px; font-weight:600; color:var(--text); margin-bottom:0.25rem;">No matching problems found</div>
        <p style="font-size:13px; margin-bottom:1rem;">Try clearing search keywords or resetting filters.</p>
        <button class="btn btn-secondary" onclick="resetAllMikFilters()">Reset All Filters</button>
      </div>
    `;
    return;
  }

  // Group by topic, then subtopic
  const groups = {};
  filtered.forEach(p => {
    if (!groups[p.topic]) groups[p.topic] = {};
    if (!groups[p.topic][p.subtopic]) groups[p.topic][p.subtopic] = [];
    groups[p.topic][p.subtopic].push(p);
  });

  let html = '';
  Object.keys(groups).sort().forEach(topic => {
    html += `
      <div class="mik-topic-group" id="mik-topic-anchor-${encodeURIComponent(topic)}">
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.75rem;">
          <h2 style="font-family:var(--font-heading); font-size:18px; font-weight:800; color:var(--text); display:flex; align-items:center; gap:0.5rem;">
            <span>📁 ${topic}</span>
          </h2>
        </div>
    `;

    Object.keys(groups[topic]).sort().forEach(subtopic => {
      const probs = groups[topic][subtopic];
      const subKey = `${topic}__${subtopic}`;
      const isCollapsed = mikState.collapsedSubtopics[subKey];
      const solvedInSub = probs.filter(p => {
        const ps = mikState.problems[p.id];
        return ps && ps.done;
      }).length;
      const subPct = Math.round((solvedInSub / probs.length) * 100);

      html += `
        <div class="mik-subtopic-card${isCollapsed ? ' collapsed' : ''}" id="subcard-${encodeURIComponent(subKey)}" style="margin-bottom:1rem;">
          <div class="mik-subtopic-header" onclick="toggleMikSubtopicCollapse('${topic.replace(/'/g, "\\'")}', '${subtopic.replace(/'/g, "\\'")}')">
            <div class="mik-subtopic-title-group">
              <svg class="mik-subtopic-chevron" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
              <span class="mik-subtopic-title">${subtopic}</span>
              <span class="badge" style="font-size:11px; font-weight:600; background:var(--surface3); color:var(--text-muted);">${probs.length} problems</span>
            </div>
            <div class="mik-subtopic-meta">
              <div class="mik-subtopic-progress-wrap">
                <div class="mik-subtopic-progress-fill" style="width:${subPct}%;"></div>
              </div>
              <span class="mik-subtopic-ratio">${solvedInSub}/${probs.length}</span>
            </div>
          </div>

          <div class="mik-problems-list">
      `;

      probs.forEach(p => {
        const ps = getMikProblemState(p.id);
        const isDone = ps.done;
        const statusClass = ps.status === 'SOLVED' ? 'done' : ps.status === 'IN_PROGRESS' ? 'inprogress' : ps.status === 'REVISE' ? 'revise' : '';
        const starClass = ps.starred ? ' starred' : '';
        const hasNotes = ps.notes && ps.notes.trim();

        // Platform link
        let platLink = '';
        if (p.leetcode_url) {
          platLink = `<a href="${p.leetcode_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge lc" title="Open on LeetCode">LC ↗</a>`;
        } else if (p.gfg_url) {
          platLink = `<a href="${p.gfg_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge gfg" title="Open on GeeksforGeeks">GFG ↗</a>`;
        } else if (p.other_url) {
          platLink = `<a href="${p.other_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge code" title="Open Problem Link">Link ↗</a>`;
        }

        // YouTube link
        let ytLink = '';
        if (p.youtube_url) {
          ytLink = `<a href="${p.youtube_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge yt" title="Watch Video Explanation on YouTube">▶ YT</a>`;
        }

        // GitHub link
        const ghLink = `<a href="${p.github_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge code" title="View C++ Solution on GitHub">&lt;/&gt; Code</a>`;

        // Top 2 companies
        let compBadges = '';
        if (p.companies && p.companies.length > 0) {
          p.companies.slice(0, 3).forEach(c => {
            compBadges += `<span class="mik-comp-chip">${c}</span>`;
          });
          if (p.companies.length > 3) {
            compBadges += `<span class="mik-company-tag" title="${p.companies.slice(3).join(', ')}">+${p.companies.length - 3}</span>`;
          }
        }

        // Complexity chips
        let compChips = '';
        if (p.tc) compChips += `<span class="mik-complexity-chip" title="Time Complexity: ${p.tc}">${p.tc}</span>`;
        if (p.sc) compChips += `<span class="mik-complexity-chip" title="Space Complexity: ${p.sc}">${p.sc}</span>`;

        html += `
          <div class="mik-problem-row" id="row-${p.id}">
            <button class="mik-status-toggle ${statusClass}" onclick="cycleMikStatus('${p.id}')" title="Status: ${ps.status} (Click to change)">
              ${isDone ? '✓' : ps.status === 'IN_PROGRESS' ? '⏳' : ps.status === 'REVISE' ? '↻' : ''}
            </button>
            <button class="mik-star-btn${starClass}" onclick="toggleMikStar('${p.id}')" title="Star problem">
              ${ps.starred ? '★' : '☆'}
            </button>
            <div class="mik-prob-info">
              <div class="mik-prob-title-row">
                <span style="font-family:var(--font-mono); font-size:11px; color:var(--text-dim);">#${p.n}</span>
                <span class="mik-prob-title">${p.title}</span>
              </div>
              <div class="mik-prob-tags-row">
                ${compBadges}
                ${compChips}
              </div>
            </div>
            <div class="mik-links-group">
              ${ytLink}
              ${platLink}
              ${ghLink}
            </div>
            <button class="mik-notes-btn${hasNotes ? ' has-notes' : ''}" onclick="openMikDetailModal('${p.id}')" title="Personal Notes">
              ${hasNotes ? '<span class="mik-notes-dot"></span>' : ''}
              <span>Notes</span>
            </button>
            <button class="mik-details-btn" onclick="openMikDetailModal('${p.id}')" title="View Problem Details">
              Details
            </button>
          </div>
        `;
      });

      html += `
          </div>
        </div>
      `;
    });

    html += `</div>`;
  });

  container.innerHTML = html;
}

function cycleMikStatus(probId) {
  const ps = getMikProblemState(probId);
  const cycle = {
    'NOT_STARTED': 'IN_PROGRESS',
    'IN_PROGRESS': 'SOLVED',
    'SOLVED': 'REVISE',
    'REVISE': 'NOT_STARTED'
  };
  const next = cycle[ps.status] || 'SOLVED';
  setMikStatus(probId, next);
}

function setMikStatus(probId, status) {
  const ps = getMikProblemState(probId);
  ps.status = status;
  ps.done = (status === 'SOLVED');
  if (ps.done) ps.lastRevised = Date.now();
  saveMikState();
  updateMikStats();
  renderMikContent();
  updateHeaderStats();
}

function toggleMikStar(probId) {
  const ps = getMikProblemState(probId);
  ps.starred = !ps.starred;
  saveMikState();
  updateMikStats();
  renderMikContent();
}

function toggleMikSubtopicCollapse(topic, subtopic) {
  const subKey = `${topic}__${subtopic}`;
  mikState.collapsedSubtopics[subKey] = !mikState.collapsedSubtopics[subKey];
  saveMikState();
  renderMikContent();
}

function expandAllMikSubtopics(expand) {
  const cat = getMikCatalog();
  cat.forEach(p => {
    const subKey = `${p.topic}__${p.subtopic}`;
    mikState.collapsedSubtopics[subKey] = !expand;
  });
  saveMikState();
  renderMikContent();
}

function setMikTopic(topic) {
  mikFilter.topic = topic;
  const select = document.getElementById('mikTopicDropdown');
  if (select) select.value = topic;
  populateMikNav();
  renderMikContent();
}

function setMikCompany(company) {
  mikFilter.company = company;
  renderMikContent();
}

function setMikStatusFilter(status, btn) {
  mikFilter.status = status;
  document.querySelectorAll('.mik-pill-group .mik-pill').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderMikContent();
}

function handleMikSearch(val) {
  mikFilter.search = val;
  const clearBtn = document.getElementById('mikSearchClearBtn');
  if (clearBtn) clearBtn.style.display = val ? 'block' : 'none';
  renderMikContent();
}

function clearMikSearch() {
  const input = document.getElementById('mikSearchInput');
  if (input) input.value = '';
  handleMikSearch('');
}

function resetAllMikFilters() {
  mikFilter = { topic: 'all', company: 'all', status: 'all', search: '' };
  const input = document.getElementById('mikSearchInput');
  if (input) input.value = '';
  const topSel = document.getElementById('mikTopicDropdown');
  if (topSel) topSel.value = 'all';
  const compSel = document.getElementById('mikCompanyDropdown');
  if (compSel) compSel.value = 'all';
  const clearBtn = document.getElementById('mikSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';

  document.querySelectorAll('.mik-pill-group .mik-pill').forEach(b => b.classList.remove('active'));
  const allBtn = document.getElementById('f-mik-all');
  if (allBtn) allBtn.classList.add('active');

  populateMikNav();
  renderMikContent();
}

function jumpToNextUnsolvedMikProblem() {
  const cat = getMikCatalog();
  const next = cat.find(p => {
    const ps = mikState.problems[p.id];
    return !ps || !ps.done;
  });
  if (next) {
    resetAllMikFilters();
    setMikTopic(next.topic);
    setTimeout(() => {
      const row = document.getElementById(`row-${next.id}`);
      if (row) {
        row.scrollIntoView({ behavior: 'smooth', block: 'center' });
        row.style.outline = '2px solid #ef4444';
        setTimeout(() => { row.style.outline = 'none'; }, 2000);
      }
    }, 150);
  } else {
    if (typeof showToast === 'function') showToast('🎉 All 1526 MIK problems solved!');
  }
}

/* DETAIL MODAL LOGIC */
function openMikDetailModal(probId) {
  activeMikModalProbId = probId;
  const cat = getMikCatalog();
  const p = cat.find(x => x.id === probId);
  if (!p) return;

  const ps = getMikProblemState(probId);

  const idEl = document.getElementById('mikModalProbId');
  if (idEl) idEl.textContent = `Problem #${p.n} · ${p.id.toUpperCase()}`;

  const titleEl = document.getElementById('mikModalTitle');
  if (titleEl) titleEl.textContent = p.title;

  const pathEl = document.getElementById('mikModalTopicSubtopic');
  if (pathEl) pathEl.textContent = `${p.topic} > ${p.subtopic}`;

  // Star button
  const starBtn = document.getElementById('mikModalStarBtn');
  if (starBtn) {
    starBtn.textContent = ps.starred ? '★' : '☆';
    starBtn.classList.toggle('starred', ps.starred);
  }

  // Links
  const linksBar = document.getElementById('mikModalLinksBar');
  if (linksBar) {
    let lHtml = '';
    if (p.youtube_url) {
      lHtml += `<a href="${p.youtube_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge yt" style="font-size:12px; padding:0.4rem 0.8rem;">▶ Watch Video Explanation</a>`;
    }
    if (p.leetcode_url) {
      lHtml += `<a href="${p.leetcode_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge lc" style="font-size:12px; padding:0.4rem 0.8rem;">Practice on LeetCode ↗</a>`;
    } else if (p.gfg_url) {
      lHtml += `<a href="${p.gfg_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge gfg" style="font-size:12px; padding:0.4rem 0.8rem;">Practice on GeeksforGeeks ↗</a>`;
    } else if (p.other_url) {
      lHtml += `<a href="${p.other_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge code" style="font-size:12px; padding:0.4rem 0.8rem;">Problem Link ↗</a>`;
    }
    lHtml += `<a href="${p.github_url}" target="_blank" rel="noopener noreferrer" class="mik-link-badge code" style="font-size:12px; padding:0.4rem 0.8rem;">&lt;/&gt; Original C++ Code on GitHub ↗</a>`;
    linksBar.innerHTML = lHtml;
  }

  // Complexity & Companies
  const tcEl = document.getElementById('mikModalTc');
  if (tcEl) tcEl.textContent = p.tc || 'Not specified';

  const scEl = document.getElementById('mikModalSc');
  if (scEl) scEl.textContent = p.sc || 'Not specified';

  const freqEl = document.getElementById('mikModalFreq');
  if (freqEl) freqEl.textContent = p.frequency || 'Standard';

  const compEl = document.getElementById('mikModalCompanies');
  if (compEl) {
    if (p.companies && p.companies.length > 0) {
      compEl.innerHTML = p.companies.map(c => `<span class="mik-comp-chip" style="font-size:11px; margin-right:4px;">${c}</span>`).join('');
    } else {
      compEl.textContent = 'None tagged';
    }
  }

  // Approaches
  const appBox = document.getElementById('mikModalApproachBox');
  const appText = document.getElementById('mikModalApproachText');
  if (appBox && appText) {
    if (p.approaches && p.approaches.length > 0) {
      appBox.style.display = 'block';
      appText.innerHTML = p.approaches.map(a => `<div>• ${a}</div>`).join('');
    } else {
      appBox.style.display = 'none';
    }
  }

  // Status button group
  updateMikModalStatusButtons(ps.status);

  // Notes
  const notesText = document.getElementById('mikModalNotesTextarea');
  if (notesText) {
    notesText.value = ps.notes || '';
    updateMikNotesCharCount(notesText.value);
  }

  openModal('modalMikDetail');
}

function updateMikModalStatusButtons(status) {
  document.querySelectorAll('#mikModalStatusGroup .mik-status-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-status') === status);
  });
}

function setMikModalStatus(status) {
  if (!activeMikModalProbId) return;
  setMikStatus(activeMikModalProbId, status);
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
"""

if 'MIK INTERVIEW DSA STATE & ENGINE' not in html:
    # Insert right before function switchView
    sv_pos = html.find('function switchView(viewName, navEl)')
    if sv_pos != -1:
        html = html[:sv_pos] + mik_js + '\n\n' + html[sv_pos:]
        print("Inserted MIK JS engine")
    else:
        print("Warning: could not find function switchView to insert MIK JS!")

# 7. Update switchView function
old_switch_view = """    risingbrain: 'RisingBrain Pattern Wise (385 Problems · 17 Topics)',
    revisions: 'Spaced Repetition Revision Center',"""

new_switch_view = """    risingbrain: 'RisingBrain Pattern Wise (385 Problems · 17 Topics)',
    mik: 'MIK Interview DSA (1526 Problems · 23 Topics)',
    revisions: 'Spaced Repetition Revision Center',"""

if 'mik: \'MIK Interview DSA (1526 Problems · 23 Topics)\'' not in html:
    html = html.replace(old_switch_view, new_switch_view)
    print("Updated switchView titleMap")

old_sv_hook = """  else if(viewName === 'risingbrain') { populateRisingBrainNav(); renderRisingBrainContent(); updateRisingBrainStats(); }
  else if(viewName === 'revisions') renderRevisionCenterView();"""

new_sv_hook = """  else if(viewName === 'risingbrain') { populateRisingBrainNav(); renderRisingBrainContent(); updateRisingBrainStats(); }
  else if(viewName === 'mik') { populateMikNav(); renderMikContent(); updateMikStats(); }
  else if(viewName === 'revisions') renderRevisionCenterView();"""

if 'else if(viewName === \'mik\')' not in html:
    html = html.replace(old_sv_hook, new_sv_hook)
    print("Updated switchView handler hook for MIK")

# 8. Update updateHeaderStats
old_hdr = """  const rbDone = Object.values(risingBrainState.problems).filter(p => p.done).length;

  const dsaTotal = 184;
  const striverTotal = 455;
  const rbTotal = totalRisingBrainProbs();"""

new_hdr = """  const rbDone = Object.values(risingBrainState.problems).filter(p => p.done).length;
  const mikDone = typeof getMikDoneCount === 'function' ? getMikDoneCount() : 0;

  const dsaTotal = 184;
  const striverTotal = 455;
  const rbTotal = totalRisingBrainProbs();
  const mikTotal = typeof getMikTotalCount === 'function' ? getMikTotalCount() : 1526;"""

if 'mikDone = typeof getMikDoneCount' not in html:
    html = html.replace(old_hdr, new_hdr)
    print("Updated updateHeaderStats counts")

old_hdr_badge = """  const rbBadge = document.getElementById('nav-risingbrain-badge');
  if (rbBadge) rbBadge.textContent = `${rbDone}/${rbTotal}`;"""

new_hdr_badge = """  const rbBadge = document.getElementById('nav-risingbrain-badge');
  if (rbBadge) rbBadge.textContent = `${rbDone}/${rbTotal}`;

  const mikBadge = document.getElementById('nav-mik-badge');
  if (mikBadge) mikBadge.textContent = `${mikDone}/${mikTotal}`;"""

if 'const mikBadge = document.getElementById(\'nav-mik-badge\');' not in html:
    html = html.replace(old_hdr_badge, new_hdr_badge)
    print("Updated updateHeaderStats badge")

old_active_view = """  } else if (activeView === 'view-risingbrain') {
    curDone = rbDone;
    curTotal = rbTotal;
  }"""

new_active_view = """  } else if (activeView === 'view-risingbrain') {
    curDone = rbDone;
    curTotal = rbTotal;
  } else if (activeView === 'view-mik') {
    curDone = mikDone;
    curTotal = mikTotal;
  }"""

if 'activeView === \'view-mik\'' not in html:
    html = html.replace(old_active_view, new_active_view)
    print("Updated activeView check in updateHeaderStats")

# 9. Update init function
old_init = """  loadState();
  loadStriverState();
  loadRisingBrainState();
  loadOtherStates();"""

new_init = """  loadState();
  loadStriverState();
  loadRisingBrainState();
  if (typeof loadMikState === 'function') loadMikState();
  loadOtherStates();"""

if 'if (typeof loadMikState === \'function\') loadMikState();' not in html:
    html = html.replace(old_init, new_init)
    print("Updated init() to loadMikState()")

# 10. Update window storage listener
old_storage_listener = """  } else if (e.key === STORAGE_RISINGBRAIN_KEY) {
    loadRisingBrainState();
    if (isViewActive('risingbrain')) renderRisingBrainContent();
    updateRisingBrainStats();
    updateHeaderStats();
  }"""

new_storage_listener = """  } else if (e.key === STORAGE_RISINGBRAIN_KEY) {
    loadRisingBrainState();
    if (isViewActive('risingbrain')) renderRisingBrainContent();
    updateRisingBrainStats();
    updateHeaderStats();
  } else if (e.key === STORAGE_MIK_KEY) {
    if (typeof loadMikState === 'function') loadMikState();
    if (isViewActive('mik')) renderMikContent();
    if (typeof updateMikStats === 'function') updateMikStats();
    updateHeaderStats();
  }"""

if 'e.key === STORAGE_MIK_KEY' not in html:
    html = html.replace(old_storage_listener, new_storage_listener)
    print("Updated window storage listener for STORAGE_MIK_KEY")

# 11. Update refreshAllUI
old_refresh = """  renderRisingBrainContent();
  updateRisingBrainStats();
  renderRevisionCenterView();"""

new_refresh = """  renderRisingBrainContent();
  updateRisingBrainStats();
  if (typeof populateMikNav === 'function') populateMikNav();
  if (typeof renderMikContent === 'function') renderMikContent();
  if (typeof updateMikStats === 'function') updateMikStats();
  renderRevisionCenterView();"""

if 'renderMikContent === \'function\'' not in html:
    html = html.replace(old_refresh, new_refresh)
    print("Updated refreshAllUI() with MIK render calls")

# 12. Update buildCompleteExportObject & applyImportData
old_export = """    risingBrainState: risingBrainState,
    diaryState: diaryState,"""

new_export = """    risingBrainState: risingBrainState,
    mikState: typeof mikState !== 'undefined' ? mikState : {},
    diaryState: diaryState,"""

if 'mikState: typeof mikState' not in html:
    html = html.replace(old_export, new_export)
    print("Updated buildCompleteExportObject() to include mikState")

old_apply_import = """  if (parsed.diaryState) diaryState = parsed.diaryState;"""

new_apply_import = """  if (parsed.risingBrainState) {
    risingBrainState = parsed.risingBrainState;
    if (typeof saveRisingBrainState === 'function') saveRisingBrainState();
  }
  if (parsed.mikState) {
    mikState = parsed.mikState;
    if (typeof saveMikState === 'function') saveMikState();
  }
  if (parsed.diaryState) diaryState = parsed.diaryState;"""

if 'if (parsed.mikState)' not in html:
    html = html.replace(old_apply_import, new_apply_import)
    print("Updated applyImportData() to restore mikState and risingBrainState")

# 13. Update recordSnapshot
old_snapshot = """    const dsaDone = Object.values(state.problems).filter(p => p.done).length;
    const striverDone = Object.values(striverState.problems).filter(p => p.done).length;"""

new_snapshot = """    const dsaDone = Object.values(state.problems).filter(p => p.done).length;
    const striverDone = Object.values(striverState.problems).filter(p => p.done).length;
    const rbDone = typeof risingBrainState !== 'undefined' && risingBrainState.problems ? Object.values(risingBrainState.problems).filter(p => p.done).length : 0;
    const mikDone = typeof mikState !== 'undefined' && mikState.problems ? Object.values(mikState.problems).filter(p => p.done).length : 0;"""

if 'rbDone = typeof risingBrainState' not in html:
    html = html.replace(old_snapshot, new_snapshot)
    print("Updated recordSnapshot() with rbDone and mikDone")

old_hist_entry = """      dsaSolved: dsaDone,
      striverSolved: striverDone
    });"""

new_hist_entry = """      dsaSolved: dsaDone,
      striverSolved: striverDone,
      rbSolved: rbDone,
      mikSolved: mikDone
    });"""

if 'mikSolved: mikDone' not in html:
    html = html.replace(old_hist_entry, new_hist_entry)
    print("Updated snapshot history entry with mikSolved")

# 14. Update handleImportFile preview
old_import_preview = """      let rbCount = 0;
      if (parsed.risingBrainState && parsed.risingBrainState.problems) {
        Object.values(parsed.risingBrainState.problems).forEach(p => { if (p.done) rbCount++; });
      }
      const diaryCount = parsed.diaryState && parsed.diaryState.entries ? Object.keys(parsed.diaryState.entries).length : 0;"""

new_import_preview = """      let rbCount = 0;
      if (parsed.risingBrainState && parsed.risingBrainState.problems) {
        Object.values(parsed.risingBrainState.problems).forEach(p => { if (p.done) rbCount++; });
      }
      let mikCount = 0;
      if (parsed.mikState && parsed.mikState.problems) {
        Object.values(parsed.mikState.problems).forEach(p => { if (p.done) mikCount++; });
      }
      const diaryCount = parsed.diaryState && parsed.diaryState.entries ? Object.keys(parsed.diaryState.entries).length : 0;"""

if 'let mikCount = 0;' not in html:
    html = html.replace(old_import_preview, new_import_preview)
    print("Updated handleImportFile with mikCount calculation")

old_preview_str = """• RisingBrain Solved: ${rbCount} / 385 problems\\n"""
new_preview_str = """• RisingBrain Solved: ${rbCount} / 385 problems\\n• MIK Interview DSA Solved: ${mikCount} / 1526 problems\\n"""

if '• MIK Interview DSA Solved:' not in html:
    html = html.replace(old_preview_str, new_preview_str)
    print("Updated importStatsPreview text with MIK count")

# Save updated file
with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Successfully updated {INDEX_PATH} (Length: {len(html)} bytes)")
