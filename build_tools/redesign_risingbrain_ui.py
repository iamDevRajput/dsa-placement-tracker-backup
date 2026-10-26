import re
import json

def generate_redesigned_css():
    return """
/* ==========================================================================
   RISINGBRAIN PREMIUM UI/UX DESIGN SYSTEM (Emerald Theme)
   ========================================================================== */
:root {
  --rb-emerald: #10b981;
  --rb-emerald-hover: #059669;
  --rb-emerald-active: #047857;
  --rb-emerald-glow: rgba(16, 185, 129, 0.25);
  --rb-emerald-tint: rgba(16, 185, 129, 0.1);
  --rb-emerald-border: rgba(16, 185, 129, 0.25);
  --rb-card-radius: 12px;
  --rb-row-radius: 8px;
}

/* --- Hero Header & Compact Dashboard --- */
.rb-hero-header {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(99, 102, 241, 0.04) 50%, rgba(20, 21, 34, 0.6) 100%);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: var(--rb-card-radius);
  padding: 1.5rem 1.75rem;
  margin-bottom: 1.25rem;
  display: grid;
  grid-template-columns: 1fr 420px;
  gap: 1.5rem;
  align-items: center;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.25);
  position: relative;
  overflow: hidden;
}
.rb-hero-header::before {
  content: '';
  position: absolute;
  top: -60px;
  right: -60px;
  width: 220px;
  height: 220px;
  background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, transparent 70%);
  pointer-events: none;
}

.rb-hero-left {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  z-index: 1;
}
.rb-hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: var(--rb-emerald);
  width: fit-content;
}
.rb-pulse-dot {
  width: 8px;
  height: 8px;
  background: var(--rb-emerald);
  border-radius: 50%;
  box-shadow: 0 0 10px var(--rb-emerald);
  animation: rbPulse 2s infinite ease-in-out;
}
@keyframes rbPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.85); }
}
.rb-badge-tag {
  background: rgba(16, 185, 129, 0.14);
  color: var(--rb-emerald);
  border: 1px solid rgba(16, 185, 129, 0.3);
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 10.5px;
  font-weight: 700;
}
.rb-hero-title {
  font-size: 1.75rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  color: #ffffff;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.rb-hero-subtitle {
  font-size: 13.5px;
  line-height: 1.5;
  color: var(--text-muted);
  max-width: 620px;
  margin: 0;
}
.rb-hero-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  margin-top: 0.5rem;
  flex-wrap: wrap;
}
.rb-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  padding: 6px 13px;
  border-radius: 7px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
  background: var(--surface2);
  color: var(--text);
  border: 1px solid var(--border-subtle);
  user-select: none;
}
.rb-action-btn:hover {
  background: var(--surface3);
  border-color: rgba(255, 255, 255, 0.15);
  color: #ffffff;
  transform: translateY(-1px);
}
.rb-action-btn.primary {
  background: var(--rb-emerald);
  color: #062b1e;
  border: 1px solid var(--rb-emerald);
  font-weight: 700;
  box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
}
.rb-action-btn.primary:hover {
  background: var(--rb-emerald-hover);
  color: #ffffff;
  box-shadow: 0 4px 14px rgba(16, 185, 129, 0.4);
}

/* Compact Dashboard Widget */
.rb-hero-dashboard {
  background: rgba(14, 15, 25, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 1rem 1.15rem;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  backdrop-filter: blur(8px);
  z-index: 1;
}
.rb-metric-card {
  display: flex;
  align-items: center;
  gap: 1.15rem;
}
.rb-radial-gauge-container {
  position: relative;
  width: 68px;
  height: 68px;
  flex-shrink: 0;
}
.rb-radial-gauge {
  width: 68px;
  height: 68px;
  transform: rotate(-90deg);
}
.rb-gauge-bg {
  fill: none;
  stroke: rgba(255, 255, 255, 0.06);
  stroke-width: 8;
}
.rb-gauge-fill {
  fill: none;
  stroke: var(--rb-emerald);
  stroke-width: 8;
  stroke-linecap: round;
  stroke-dasharray: 264;
  stroke-dashoffset: 264;
  transition: stroke-dashoffset 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
.rb-radial-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.rb-gauge-pct {
  font-size: 14px;
  font-weight: 800;
  font-family: var(--font-mono);
  color: #ffffff;
  line-height: 1;
}
.rb-gauge-label {
  font-size: 9px;
  font-weight: 700;
  color: var(--text-dim);
  text-transform: uppercase;
  margin-top: 2px;
}
.rb-metric-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}
.rb-metric-heading {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-dim);
  letter-spacing: 0.04em;
}
.rb-metric-main-stat {
  font-size: 1.35rem;
  font-weight: 800;
  font-family: var(--font-mono);
  color: #ffffff;
  line-height: 1.1;
}
.rb-metric-denom {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-dim);
}
.rb-quick-chips {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.2rem;
}
.rb-quick-chip {
  font-size: 10px;
  font-family: var(--font-mono);
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
}
.rb-quick-chip.starred { background: rgba(255, 213, 74, 0.12); color: #ffd54a; border: 1px solid rgba(255, 213, 74, 0.25); }
.rb-quick-chip.mastered { background: rgba(234, 179, 8, 0.12); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.25); }
.rb-quick-chip.needsrev { background: rgba(168, 85, 247, 0.12); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.25); }

/* Difficulty Progress Bars */
.rb-diff-bars-card {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 0.65rem;
}
.rb-diff-bar-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
.rb-diff-bar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
}
.rb-diff-bar-numbers {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
}
.rb-prog-track {
  height: 5px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 3px;
  overflow: hidden;
  position: relative;
}
.rb-prog-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.4s ease;
}
.rb-prog-fill.easy { background: linear-gradient(90deg, #10b981, #34d399); }
.rb-prog-fill.med { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.rb-prog-fill.hard { background: linear-gradient(90deg, #ef4444, #f87171); }

/* --- Search & Controls Bar --- */
.rb-controls-bar {
  background: var(--surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--rb-card-radius);
  padding: 0.85rem 1.15rem;
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  box-shadow: var(--shadow-sm);
}
.rb-controls-top {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}
.rb-search-wrapper {
  position: relative;
  flex: 1;
  min-width: 280px;
  display: flex;
  align-items: center;
}
.rb-search-icon {
  position: absolute;
  left: 12px;
  color: var(--text-dim);
  pointer-events: none;
}
.rb-search-input {
  width: 100%;
  background: var(--surface2);
  border: 1px solid var(--border-subtle);
  border-radius: 8px;
  padding: 8px 36px 8px 36px;
  color: var(--text);
  font-size: 13px;
  font-family: var(--font-body);
  transition: all var(--transition-fast);
}
.rb-search-input:focus {
  outline: none;
  border-color: var(--rb-emerald);
  box-shadow: 0 0 0 3px var(--rb-emerald-glow);
  background: var(--surface);
}
.rb-search-clear {
  position: absolute;
  right: 10px;
  background: transparent;
  border: none;
  color: var(--text-dim);
  font-size: 14px;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: color var(--transition-fast);
}
.rb-search-clear:hover {
  color: #ffffff;
}
.rb-filter-selects {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.rb-select {
  height: 36px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  padding: 0 10px;
  background: var(--surface2);
  border: 1px solid var(--border-subtle);
  color: var(--text);
}
.rb-select:focus {
  border-color: var(--rb-emerald);
}

.rb-filter-pills-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  padding-top: 0.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}
.rb-pill-group {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  flex-wrap: wrap;
}
.rb-pill-divider {
  width: 1px;
  height: 18px;
  background: var(--border-subtle);
  margin: 0 0.35rem;
}
.rb-pill {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  background: var(--surface2);
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: all var(--transition-fast);
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  user-select: none;
}
.rb-pill:hover {
  color: var(--text);
  border-color: rgba(255, 255, 255, 0.15);
  background: var(--surface3);
}
.rb-pill.active {
  background: var(--rb-emerald);
  color: #062b1e;
  border-color: var(--rb-emerald);
  font-weight: 700;
  box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}
.rb-pill.diff-e.active { background: #10b981; color: #042417; }
.rb-pill.diff-m.active { background: #f59e0b; color: #351a02; }
.rb-pill.diff-h.active { background: #ef4444; color: #320505; }
.rb-pill-count {
  font-family: var(--font-mono);
  font-size: 10px;
  padding: 1px 4px;
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.2);
}
.rb-pill.active .rb-pill-count {
  background: rgba(0, 0, 0, 0.25);
  color: inherit;
}

/* --- Main Layout Grid --- */
.rb-main-workspace {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 1.25rem;
  align-items: start;
}

/* --- Topic Navigation Sidebar --- */
.rb-topic-sidebar {
  position: sticky;
  top: 1rem;
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  background: var(--surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--rb-card-radius);
  padding: 0.75rem 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  box-shadow: var(--shadow-sm);
}
.rb-sidebar-heading {
  padding: 0.4rem 0.65rem 0.6rem 0.65rem;
  font-size: 10.5px;
  font-weight: 800;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--text-dim);
  border-bottom: 1px solid var(--border-subtle);
  margin-bottom: 0.25rem;
}
.rb-topic-nav-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.55rem 0.65rem;
  border-radius: 7px;
  cursor: pointer;
  transition: all var(--transition-fast);
  border-left: 3px solid transparent;
  user-select: none;
}
.rb-topic-nav-item:hover {
  background: var(--surface2);
  transform: translateX(2px);
}
.rb-topic-nav-item.active {
  background: rgba(16, 185, 129, 0.08);
  border-left-color: var(--rb-emerald);
}
.rb-topic-nav-item.active .rb-nav-icon-badge {
  background: var(--rb-emerald);
  color: #062b1e;
  font-weight: 800;
}
.rb-topic-nav-item.active .rb-nav-topic-title {
  color: #ffffff;
  font-weight: 700;
}
.rb-nav-icon-badge {
  width: 24px;
  height: 24px;
  border-radius: 5px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-muted);
  font-size: 10px;
  font-weight: 800;
  font-family: var(--font-mono);
  display: grid;
  place-items: center;
  flex-shrink: 0;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all var(--transition-fast);
}
.rb-nav-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.rb-nav-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.rb-nav-topic-title {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.rb-nav-fraction {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: var(--text-dim);
}
.rb-nav-track {
  height: 3px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 2px;
  overflow: hidden;
}
.rb-nav-fill {
  height: 100%;
  background: var(--rb-emerald);
  border-radius: 2px;
}

/* --- Content Area & Topic Sections --- */
.rb-content-area {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}
.rb-topic-section {
  background: var(--surface2);
  border: 1px solid var(--border-subtle);
  border-radius: var(--rb-card-radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  transition: border-color var(--transition-fast);
}
.rb-topic-section:hover {
  border-color: rgba(16, 185, 129, 0.25);
}
.rb-topic-header {
  padding: 0.9rem 1.25rem;
  background: var(--surface3);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.rb-topic-title-wrap {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.rb-topic-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: rgba(16, 185, 129, 0.15);
  color: var(--rb-emerald);
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 12.5px;
  font-family: var(--font-mono);
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.rb-topic-name {
  font-size: 1.05rem;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.01em;
}
.rb-topic-desc {
  font-size: 11.5px;
  color: var(--text-muted);
  margin-top: 1px;
}
.rb-topic-stats-wrap {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}
.rb-topic-ratio {
  font-size: 12px;
  font-family: var(--font-mono);
  color: var(--text-muted);
}
.rb-topic-toggle-btn {
  background: var(--surface2);
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
  padding: 3px 9px;
  border-radius: 6px;
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.rb-topic-toggle-btn:hover {
  background: var(--surface);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.15);
}

/* --- Pattern Cards --- */
.rb-pattern-card {
  margin: 0.85rem 1rem;
  background: var(--surface);
  border: 1px solid var(--border-subtle);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  transition: all var(--transition-fast);
}
.rb-pattern-card:hover {
  border-color: rgba(16, 185, 129, 0.3);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.rb-pattern-header {
  padding: 0.85rem 1.15rem;
  background: rgba(255, 255, 255, 0.015);
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
  transition: background var(--transition-fast);
}
.rb-pattern-header:hover {
  background: rgba(16, 185, 129, 0.04);
}
.rb-pattern-header-left {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}
.rb-pat-badge {
  font-size: 10.5px;
  font-weight: 800;
  font-family: var(--font-mono);
  padding: 2px 7px;
  border-radius: 4px;
  background: rgba(16, 185, 129, 0.14);
  color: var(--rb-emerald);
  border: 1px solid rgba(16, 185, 129, 0.3);
}
.rb-pattern-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}
.rb-pattern-header-right {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.rb-pattern-ratio {
  font-size: 11.5px;
  font-family: var(--font-mono);
  color: var(--text-dim);
}
.rb-pat-mini-track {
  width: 65px;
  height: 5px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 3px;
  overflow: hidden;
}
.rb-pat-mini-fill {
  height: 100%;
  background: var(--rb-emerald);
  border-radius: 3px;
}
.rb-pat-pct-badge {
  font-size: 11px;
  font-family: var(--font-mono);
  font-weight: 700;
  color: var(--text-muted);
  min-width: 32px;
  text-align: right;
}
.rb-accordion-chevron {
  color: var(--text-dim);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}
.rb-accordion-chevron.collapsed {
  transform: rotate(-90deg);
}

.rb-pattern-body {
  border-top: 1px solid var(--border-subtle);
  padding: 0.75rem 1rem 1rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  background: rgba(0, 0, 0, 0.08);
}
.rb-pattern-strategy-box {
  background: rgba(56, 189, 248, 0.04);
  border: 1px solid rgba(56, 189, 248, 0.2);
  border-left: 3px solid #38bdf8;
  border-radius: 6px;
  padding: 0.65rem 0.85rem;
}
.rb-pattern-clues-box {
  background: rgba(245, 158, 11, 0.04);
  border: 1px solid rgba(245, 158, 11, 0.2);
  border-left: 3px solid #f59e0b;
  border-radius: 6px;
  padding: 0.65rem 0.85rem;
}
.rb-callout-header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.03em;
  margin-bottom: 0.3rem;
}
.rb-pattern-strategy-box .rb-callout-header { color: #38bdf8; }
.rb-pattern-clues-box .rb-callout-header { color: #f59e0b; }
.rb-callout-text {
  font-size: 12.5px;
  line-height: 1.5;
  color: var(--text-muted);
}

/* --- Problem Rows Table --- */
.rb-problems-table {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}
.rb-prob-row {
  background: var(--surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--rb-row-radius);
  padding: 0.65rem 0.85rem;
  display: grid;
  grid-template-columns: 85px 1fr auto;
  align-items: center;
  gap: 0.85rem;
  transition: all var(--transition-fast);
}
.rb-prob-row:hover {
  background: rgba(255, 255, 255, 0.02);
  border-color: rgba(16, 185, 129, 0.3);
  transform: translateY(-1px);
}
.rb-prob-row.is-done {
  border-left: 3px solid var(--rb-emerald);
}

/* Left Checkbox / Star / ID */
.rb-col-check {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}
.rb-custom-checkbox {
  position: relative;
  display: inline-block;
  width: 18px;
  height: 18px;
  cursor: pointer;
}
.rb-custom-checkbox input {
  opacity: 0;
  width: 0;
  height: 0;
  position: absolute;
}
.rb-checkmark {
  position: absolute;
  top: 0;
  left: 0;
  width: 18px;
  height: 18px;
  background: var(--surface2);
  border: 1.5px solid var(--border);
  border-radius: 4px;
  transition: all var(--transition-fast);
}
.rb-custom-checkbox:hover .rb-checkmark {
  border-color: var(--rb-emerald);
}
.rb-custom-checkbox input:checked ~ .rb-checkmark {
  background: var(--rb-emerald);
  border-color: var(--rb-emerald);
}
.rb-checkmark::after {
  content: '';
  position: absolute;
  display: none;
  left: 5px;
  top: 2px;
  width: 4px;
  height: 8px;
  border: solid #042417;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
.rb-custom-checkbox input:checked ~ .rb-checkmark::after {
  display: block;
}
.rb-star-btn {
  background: transparent;
  border: none;
  font-size: 15px;
  color: var(--text-dim);
  cursor: pointer;
  padding: 0 2px;
  line-height: 1;
  transition: color var(--transition-fast);
}
.rb-star-btn:hover {
  color: #ffd54a;
}
.rb-star-btn.starred {
  color: #ffd54a;
}
.rb-prob-index {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 700;
  color: var(--text-dim);
}

/* Center Content */
.rb-col-main {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  min-width: 0;
}
.rb-prob-title-line {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.rb-ref-pill {
  font-size: 10.5px;
  font-family: var(--font-mono);
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
  white-space: nowrap;
}
.rb-prob-name {
  font-size: 13.5px;
  font-weight: 600;
  color: var(--text);
  line-height: 1.3;
}
.rb-diff-badge {
  font-size: 10.5px;
  font-weight: 700;
  padding: 1.5px 7px;
  border-radius: 4px;
  white-space: nowrap;
}
.rb-diff-badge.diff-easy {
  background: rgba(16, 185, 129, 0.12);
  color: #34d399;
  border: 1px solid rgba(16, 185, 129, 0.25);
}
.rb-diff-badge.diff-med {
  background: rgba(245, 158, 11, 0.12);
  color: #fbbf24;
  border: 1px solid rgba(245, 158, 11, 0.25);
}
.rb-diff-badge.diff-hard {
  background: rgba(239, 68, 68, 0.12);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.25);
}

.rb-prob-sub-line {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.rb-links-container {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.rb-platform-link {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 2px 7px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  text-decoration: none;
  transition: all var(--transition-fast);
}
.rb-platform-link.lc {
  background: var(--lc-bg);
  color: var(--lc);
  border: 1px solid var(--lc-border);
}
.rb-platform-link.lc:hover {
  background: rgba(255, 161, 22, 0.22);
  transform: translateY(-1px);
}
.rb-platform-link.gfg {
  background: var(--gfg-bg);
  color: #34d399;
  border: 1px solid var(--gfg-border);
}
.rb-platform-link.gfg:hover {
  background: rgba(47, 141, 70, 0.22);
  transform: translateY(-1px);
}
.rb-platform-link.yt {
  background: rgba(239, 68, 68, 0.12);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.3);
}
.rb-platform-link.yt:hover {
  background: rgba(239, 68, 68, 0.22);
  transform: translateY(-1px);
}
.rb-ext-icon {
  width: 10px;
  height: 10px;
  opacity: 0.75;
}

.rb-companies-container {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}
.rb-company-chip {
  font-size: 10.5px;
  font-weight: 500;
  padding: 1.5px 6px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.04);
  color: var(--text-dim);
  border: 1px solid var(--border-subtle);
}

.rb-crossref-container {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

/* Actions Column */
.rb-col-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.rb-status-dropdown {
  font-size: 11.5px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
  background: var(--surface2);
  color: var(--text);
  border: 1px solid var(--border-subtle);
  outline: none;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.rb-status-dropdown:focus {
  border-color: var(--rb-emerald);
}
.rb-status-dropdown.status-NOT_STARTED { color: var(--text-dim); }
.rb-status-dropdown.status-ATTEMPTED { color: #f59e0b; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.08); }
.rb-status-dropdown.status-SOLVED_INDEPENDENT { color: #10b981; border-color: rgba(16, 185, 129, 0.4); background: rgba(16, 185, 129, 0.1); }
.rb-status-dropdown.status-SOLVED_HINT { color: #f97316; border-color: rgba(249, 115, 22, 0.4); background: rgba(249, 115, 22, 0.1); }
.rb-status-dropdown.status-NEEDS_REVISION { color: #a855f7; border-color: rgba(168, 85, 247, 0.4); background: rgba(168, 85, 247, 0.1); }
.rb-status-dropdown.status-MASTERED { color: #eab308; border-color: rgba(234, 179, 8, 0.5); background: rgba(234, 179, 8, 0.12); }

.rb-rev-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 11.5px;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 6px;
  background: transparent;
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.rb-rev-btn:hover {
  background: var(--surface3);
  color: #ffffff;
  border-color: rgba(255, 255, 255, 0.2);
}
.rb-rev-badge {
  font-size: 10px;
  font-weight: 800;
  font-family: var(--font-mono);
  padding: 0 4px;
  border-radius: 3px;
  background: var(--rb-emerald);
  color: #042417;
}

/* Empty State */
.rb-empty-state {
  background: var(--surface);
  border: 1px dashed var(--border);
  border-radius: var(--rb-card-radius);
  padding: 3rem 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.65rem;
}
.rb-empty-icon {
  font-size: 2.2rem;
  margin-bottom: 0.25rem;
}
.rb-empty-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #ffffff;
}
.rb-empty-subtitle {
  font-size: 13px;
  color: var(--text-muted);
  max-width: 400px;
}
.rb-empty-reset-btn {
  margin-top: 0.5rem;
  background: var(--rb-emerald);
  color: #042417;
  border: none;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all var(--transition-fast);
}
.rb-empty-reset-btn:hover {
  background: var(--rb-emerald-hover);
  color: #ffffff;
}

/* --- Responsive Adjustments --- */
@media (max-width: 1100px) {
  .rb-hero-header {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 860px) {
  .rb-main-workspace {
    grid-template-columns: 1fr;
  }
  .rb-topic-sidebar {
    position: static;
    max-height: 220px;
  }
  .rb-prob-row {
    grid-template-columns: 1fr;
    gap: 0.65rem;
  }
  .rb-col-check {
    justify-content: flex-start;
  }
  .rb-col-actions {
    justify-content: flex-start;
  }
}
"""

def generate_view_markup():
    return """<!-- VIEW 2.7: RISINGBRAIN PATTERN-WISE SHEET (UPGRADED PREMIER DESIGN) -->
    <section class="view-section" id="view-risingbrain">
      <!-- 1. HERO BANNER & COMPACT PROGRESS DASHBOARD -->
      <div class="rb-hero-header">
        <div class="rb-hero-left">
          <div class="rb-hero-badge">
            <span class="rb-pulse-dot"></span>
            <span>Pattern-Wise Curriculum</span>
            <span class="rb-badge-tag">385 Problems · 68 Patterns · 17 Topics</span>
          </div>
          <h1 class="rb-hero-title">RisingBrain Pattern Wise</h1>
          <p class="rb-hero-subtitle">
            Master coding interviews by learning reusable algorithmic patterns instead of memorizing individual problems.
          </p>
          <div class="rb-hero-actions">
            <button class="rb-action-btn primary" onclick="jumpToNextUnsolvedRbProblem()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
              <span>Resume Next Problem</span>
            </button>
            <button class="rb-action-btn" onclick="expandAllRbPatterns(true)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="7 13 12 18 17 13"/><polyline points="7 6 12 11 17 6"/></svg>
              <span>Expand All</span>
            </button>
            <button class="rb-action-btn" onclick="expandAllRbPatterns(false)">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="17 11 12 6 7 11"/><polyline points="17 18 12 13 7 18"/></svg>
              <span>Collapse All</span>
            </button>
          </div>
        </div>

        <div class="rb-hero-dashboard">
          <div class="rb-metric-card">
            <div class="rb-radial-gauge-container">
              <svg class="rb-radial-gauge" viewBox="0 0 100 100">
                <circle class="rb-gauge-bg" cx="50" cy="50" r="42" />
                <circle class="rb-gauge-fill" id="rb-gauge-circle" cx="50" cy="50" r="42" />
              </svg>
              <div class="rb-radial-content">
                <span class="rb-gauge-pct" id="rb-radial-pct">0%</span>
                <span class="rb-gauge-label">Done</span>
              </div>
            </div>
            <div class="rb-metric-info">
              <div class="rb-metric-heading">Overall Completion</div>
              <div class="rb-metric-main-stat" id="rb-header-solved-count">0 <span class="rb-metric-denom">/ 385</span></div>
              <div class="rb-quick-chips">
                <span class="rb-quick-chip starred" id="rb-stat-chip-starred" title="Starred problems">★ 0</span>
                <span class="rb-quick-chip mastered" id="rb-stat-chip-mastered" title="Mastered problems">👑 0</span>
                <span class="rb-quick-chip needsrev" id="rb-stat-chip-needsrev" title="Needs revision">🟣 0</span>
              </div>
            </div>
          </div>

          <div class="rb-diff-bars-card">
            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-easy">Easy</span>
                <span class="rb-diff-bar-numbers" id="rb-easy-ratio">0 / 81 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill easy" id="rb-easy-fill" style="width:0%;"></div></div>
            </div>

            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-med">Medium</span>
                <span class="rb-diff-bar-numbers" id="rb-med-ratio">0 / 251 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill med" id="rb-med-fill" style="width:0%;"></div></div>
            </div>

            <div class="rb-diff-bar-item">
              <div class="rb-diff-bar-header">
                <span class="rb-diff-badge diff-hard">Hard</span>
                <span class="rb-diff-bar-numbers" id="rb-hard-ratio">0 / 53 (0%)</span>
              </div>
              <div class="rb-prog-track"><div class="rb-prog-fill hard" id="rb-hard-fill" style="width:0%;"></div></div>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. SEARCH & ADVANCED FILTER CONTROLS -->
      <div class="rb-controls-bar">
        <div class="rb-controls-top">
          <div class="rb-search-wrapper">
            <svg class="rb-search-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            <input type="text" id="rbSearch" class="rb-search-input" placeholder="Search 385 problems, references (e.g. LC 167), patterns, topics, companies..." oninput="handleRbSearchInput(this.value)">
            <button id="rbSearchClearBtn" class="rb-search-clear" onclick="clearRbSearch()" title="Clear search" style="display:none;">✕</button>
          </div>

          <div class="rb-filter-selects">
            <select class="form-select rb-select" id="rbTopicSelectDropdown" onchange="jumpToRbTopic(this.value)">
              <!-- Populated dynamically with all 17 topics -->
            </select>

            <select class="form-select rb-select" id="rbCompanyFilter" onchange="setRbCompany(this.value)">
              <option value="all">🏢 All Companies</option>
              <option value="Amazon">🛒 Amazon</option>
              <option value="Google">🔍 Google</option>
              <option value="Microsoft">🪟 Microsoft</option>
              <option value="Meta">👤 Meta</option>
              <option value="Apple">🍎 Apple</option>
              <option value="Bloomberg">📈 Bloomberg</option>
              <option value="Uber">🚗 Uber</option>
              <option value="Goldman Sachs">🏦 Goldman Sachs</option>
              <option value="Adobe">🎨 Adobe</option>
              <option value="Salesforce">☁️ Salesforce</option>
              <option value="Flipkart">🛍️ Flipkart</option>
            </select>
          </div>
        </div>

        <div class="rb-filter-pills-row">
          <div class="rb-pill-group">
            <button class="rb-pill active" id="f-rb-all" onclick="setRbFilter('all', this)">All <span class="rb-pill-count">385</span></button>
            <button class="rb-pill diff-e" id="f-rb-easy" onclick="setRbFilter('e', this)">Easy <span class="rb-pill-count" id="rb-pill-easy-cnt">81</span></button>
            <button class="rb-pill diff-m" id="f-rb-medium" onclick="setRbFilter('m', this)">Medium <span class="rb-pill-count" id="rb-pill-med-cnt">251</span></button>
            <button class="rb-pill diff-h" id="f-rb-hard" onclick="setRbFilter('h', this)">Hard <span class="rb-pill-count" id="rb-pill-hard-cnt">53</span></button>
          </div>

          <div class="rb-pill-divider"></div>

          <div class="rb-pill-group">
            <button class="rb-pill" id="f-rb-pending" onclick="setRbStatusFilter('pending', this)">Pending</button>
            <button class="rb-pill" id="f-rb-done" onclick="setRbStatusFilter('done', this)">Done</button>
            <button class="rb-pill" id="f-rb-attempted" onclick="setRbStatusFilter('attempted', this)">🟡 Attempted</button>
            <button class="rb-pill" id="f-rb-needsrev" onclick="setRbStatusFilter('needsrev', this)">🟣 Needs Rev</button>
            <button class="rb-pill" id="f-rb-mastered" onclick="setRbStatusFilter('mastered', this)">👑 Mastered</button>
            <button class="rb-pill" id="f-rb-starred" onclick="setRbStatusFilter('starred', this)">⭐ Starred</button>
          </div>
        </div>
      </div>

      <!-- 3. MAIN WORKSPACE: SIDEBAR & PATTERNS -->
      <div class="rb-main-workspace">
        <!-- Topic Navigation Sidebar -->
        <aside class="rb-topic-sidebar" id="rbTopicNavSidebar">
          <!-- Populated dynamically with all 17 topics -->
        </aside>

        <!-- Topic Sections & Pattern Cards -->
        <div class="rb-content-area" id="risingBrainContent">
          <!-- Populated dynamically with pattern cards and problem rows -->
        </div>
      </div>
    </section>"""

def generate_upgraded_js():
    return """
/* ==========================================================================
   RISINGBRAIN UPGRADED INTERACTIVE CONTROLLER
   ========================================================================== */

function toggleRisingBrainStar(n) {
  const ps = getRisingBrainProblemState(n);
  ps.starred = !ps.starred;
  saveRisingBrainState();
  updateRisingBrainStats();
  renderRisingBrainContent();
}

function handleRbSearchInput(val) {
  const clearBtn = document.getElementById('rbSearchClearBtn');
  if (clearBtn) clearBtn.style.display = val && val.trim().length > 0 ? 'flex' : 'none';
  renderRisingBrainContent();
}

function clearRbSearch() {
  const input = document.getElementById('rbSearch');
  if (input) {
    input.value = '';
    input.focus();
  }
  const clearBtn = document.getElementById('rbSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';
  renderRisingBrainContent();
}

function resetAllRbFilters() {
  const input = document.getElementById('rbSearch');
  if (input) input.value = '';
  const clearBtn = document.getElementById('rbSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';

  const co = document.getElementById('rbCompanyFilter');
  if (co) co.value = 'all';
  currentRbCompany = 'all';

  jumpToRbTopic('all');
  setRbFilter('all', document.getElementById('f-rb-all'));
  setRbStatusFilter('all', null);
}

function jumpToNextUnsolvedRbProblem() {
  let nextUnsolved = null;
  for (const topic of RISINGBRAIN_DATA) {
    if (currentActiveRbTopic !== 'all' && currentActiveRbTopic !== topic.id) continue;
    for (const pat of topic.patterns) {
      for (const p of pat.problems) {
        const ps = getRisingBrainProblemState(p.n);
        if (!ps.done) {
          nextUnsolved = { topic, pat, prob: p };
          break;
        }
      }
      if (nextUnsolved) break;
    }
    if (nextUnsolved) break;
  }

  // If no unsolved in current topic, check all topics
  if (!nextUnsolved && currentActiveRbTopic !== 'all') {
    for (const topic of RISINGBRAIN_DATA) {
      for (const pat of topic.patterns) {
        for (const p of pat.problems) {
          const ps = getRisingBrainProblemState(p.n);
          if (!ps.done) {
            nextUnsolved = { topic, pat, prob: p };
            break;
          }
        }
        if (nextUnsolved) break;
      }
      if (nextUnsolved) break;
    }
  }

  if (nextUnsolved) {
    // Expand topic and pattern if collapsed
    risingBrainState.collapsedTopics[nextUnsolved.topic.id] = false;
    risingBrainState.collapsedPatterns[nextUnsolved.pat.id] = false;
    saveRisingBrainState();
    renderRisingBrainContent();

    setTimeout(() => {
      const el = document.getElementById('rb-prob-' + nextUnsolved.prob.n);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.style.boxShadow = '0 0 0 3px #10b981, 0 0 20px rgba(16, 185, 129, 0.4)';
        setTimeout(() => el.style.boxShadow = '', 2500);
      }
    }, 150);
    showToast(`Jumped to Next Unsolved: #${nextUnsolved.prob.n} (${nextUnsolved.prob.t})`);
  } else {
    showToast('🎉 Incredible! All 385 RisingBrain problems are marked solved!');
  }
}

function updateRisingBrainStats() {
  const total = totalRisingBrainProbs();
  const allStates = Object.values(risingBrainState.problems);
  const done = allStates.filter(p => p.done).length;
  const pct = total > 0 ? Math.round((done / total) * 100) : 0;

  // Counts by difficulty
  let easyTotal = 0, easyDone = 0;
  let medTotal = 0, medDone = 0;
  let hardTotal = 0, hardDone = 0;
  let starredCount = 0, masteredCount = 0, needsRevCount = 0;

  RISINGBRAIN_DATA.forEach(t => {
    t.patterns.forEach(pat => {
      pat.problems.forEach(p => {
        const ps = getRisingBrainProblemState(p.n);
        if (p.diff === 'e') {
          easyTotal++;
          if (ps.done) easyDone++;
        } else if (p.diff === 'm') {
          medTotal++;
          if (ps.done) medDone++;
        } else if (p.diff === 'h') {
          hardTotal++;
          if (ps.done) hardDone++;
        }
        if (ps.starred) starredCount++;
        if (ps.status === 'MASTERED') masteredCount++;
        if (ps.status === 'NEEDS_REVISION') needsRevCount++;
      });
    });
  });

  const easyPct = easyTotal > 0 ? Math.round((easyDone / easyTotal) * 100) : 0;
  const medPct = medTotal > 0 ? Math.round((medDone / medTotal) * 100) : 0;
  const hardPct = hardTotal > 0 ? Math.round((hardDone / hardTotal) * 100) : 0;

  // Update Nav Badge
  const badge = document.getElementById('nav-risingbrain-badge');
  if (badge) badge.textContent = `${done}/${total}`;

  // Update Hero Radial & Stats
  const radialPct = document.getElementById('rb-radial-pct');
  if (radialPct) radialPct.textContent = `${pct}%`;

  const gaugeCircle = document.getElementById('rb-gauge-circle');
  if (gaugeCircle) {
    const circumference = 2 * Math.PI * 42; // ~263.89
    const offset = circumference - (pct / 100) * circumference;
    gaugeCircle.style.strokeDashoffset = offset;
  }

  const headerSolved = document.getElementById('rb-header-solved-count');
  if (headerSolved) headerSolved.innerHTML = `${done} <span class="rb-metric-denom">/ ${total}</span>`;

  const chipStar = document.getElementById('rb-stat-chip-starred');
  if (chipStar) chipStar.textContent = `★ ${starredCount}`;

  const chipMaster = document.getElementById('rb-stat-chip-mastered');
  if (chipMaster) chipMaster.textContent = `👑 ${masteredCount}`;

  const chipRev = document.getElementById('rb-stat-chip-needsrev');
  if (chipRev) chipRev.textContent = `🟣 ${needsRevCount}`;

  // Update Difficulty Ratios & Bars
  const eRatio = document.getElementById('rb-easy-ratio');
  if (eRatio) eRatio.textContent = `${easyDone} / ${easyTotal} (${easyPct}%)`;
  const eFill = document.getElementById('rb-easy-fill');
  if (eFill) eFill.style.width = `${easyPct}%`;

  const mRatio = document.getElementById('rb-med-ratio');
  if (mRatio) mRatio.textContent = `${medDone} / ${medTotal} (${medPct}%)`;
  const mFill = document.getElementById('rb-med-fill');
  if (mFill) mFill.style.width = `${medPct}%`;

  const hRatio = document.getElementById('rb-hard-ratio');
  if (hRatio) hRatio.textContent = `${hardDone} / ${hardTotal} (${hardPct}%)`;
  const hFill = document.getElementById('rb-hard-fill');
  if (hFill) hFill.style.width = `${hardPct}%`;

  // Update Main Dashboard Card if present
  const dbCount = document.getElementById('db-rb-count-large');
  if (dbCount) dbCount.innerHTML = `${done} <span style="font-size:13px; color:var(--text-muted); font-weight:500;">/ ${total}</span>`;
  const dbBar = document.getElementById('db-rb-bar-large');
  if (dbBar) dbBar.style.width = `${pct}%`;
  const dbPct = document.getElementById('db-rb-pct-large');
  if (dbPct) dbPct.textContent = `${pct}% Solved · 17 Topics`;
}

const RB_TOPIC_ICONS = {
  'Array': 'AR',
  'Strings': 'ST',
  'Binary Search': 'BS',
  'Stack': 'SK',
  'Queue': 'QU',
  'Recursion': 'RC',
  'Linked List': 'LL',
  'Double Linked List': 'DL',
  'HashMap': 'HM',
  'Binary Tree': 'BT',
  'Graph': 'GR',
  'Heap': 'HP',
  'Backtracking': 'BK',
  'Greedy': 'GD',
  'Dynamic Programming': 'DP',
  'Trie': 'TR',
  'Bit Manipulation': 'BM'
};

function populateRisingBrainNav() {
  const sb = document.getElementById('rbTopicNavSidebar');
  const dd = document.getElementById('rbTopicSelectDropdown');
  if (!sb || !dd) return;

  let totalDoneAll = 0;
  let totalProbsAll = 0;

  RISINGBRAIN_DATA.forEach(t => {
    totalDoneAll += doneRisingBrainProbsForTopic(t);
    totalProbsAll += t.patterns.reduce((acc, p) => acc + p.problems.length, 0);
  });

  let sbHtml = '<div class="rb-sidebar-heading">17 Topics · 68 Patterns</div>';
  let ddHtml = `<option value="all">📚 All 17 Topics (${totalDoneAll}/${totalProbsAll})</option>`;

  const isAllActive = currentActiveRbTopic === 'all';
  const allPct = totalProbsAll > 0 ? Math.round((totalDoneAll / totalProbsAll) * 100) : 0;

  sbHtml += `
    <div class="rb-topic-nav-item ${isAllActive ? 'active' : ''}" onclick="jumpToRbTopic('all')">
      <span class="rb-nav-icon-badge">ALL</span>
      <div class="rb-nav-info">
        <div class="rb-nav-title-row">
          <span class="rb-nav-topic-title">All Topics</span>
          <span class="rb-nav-fraction">${totalDoneAll}/${totalProbsAll}</span>
        </div>
        <div class="rb-nav-track"><div class="rb-nav-fill" style="width:${allPct}%;"></div></div>
      </div>
    </div>
  `;

  RISINGBRAIN_DATA.forEach(t => {
    const doneC = doneRisingBrainProbsForTopic(t);
    const totalC = t.patterns.reduce((acc, p) => acc + p.problems.length, 0);
    const pct = totalC > 0 ? Math.round((doneC / totalC) * 100) : 0;
    const isActive = currentActiveRbTopic === t.id;
    const iconCode = RB_TOPIC_ICONS[t.name] || t.name.substring(0, 2).toUpperCase();

    sbHtml += `
      <div class="rb-topic-nav-item ${isActive ? 'active' : ''}" id="rb-nav-${t.id}" onclick="jumpToRbTopic('${t.id}')">
        <span class="rb-nav-icon-badge">${iconCode}</span>
        <div class="rb-nav-info">
          <div class="rb-nav-title-row">
            <span class="rb-nav-topic-title" title="${t.name}">${t.name}</span>
            <span class="rb-nav-fraction">${doneC}/${totalC}</span>
          </div>
          <div class="rb-nav-track"><div class="rb-nav-fill" style="width:${pct}%;"></div></div>
        </div>
      </div>
    `;
    ddHtml += `<option value="${t.id}" ${isActive ? 'selected' : ''}>${t.name} (${doneC}/${totalC})</option>`;
  });

  sb.innerHTML = sbHtml;
  dd.innerHTML = ddHtml;
}

function renderRisingBrainContent() {
  const q = (document.getElementById('rbSearch')?.value || '').toLowerCase().trim();
  const content = document.getElementById('risingBrainContent');
  if (!content) return;

  let html = '';
  let totalVisible = 0;

  RISINGBRAIN_DATA.forEach(topic => {
    if (currentActiveRbTopic !== 'all' && currentActiveRbTopic !== topic.id) return;

    let topicHasVisible = false;
    let topicPatternsHtml = '';

    const doneTopicCount = doneRisingBrainProbsForTopic(topic);
    const totalTopicCount = topic.patterns.reduce((acc, p) => acc + p.problems.length, 0);
    const topicPct = totalTopicCount > 0 ? Math.round((doneTopicCount / totalTopicCount) * 100) : 0;
    const isTopicCollapsed = !!risingBrainState.collapsedTopics[topic.id];

    topic.patterns.forEach((pat, patIdx) => {
      const visibleProblems = pat.problems.filter(p => {
        const ps = getRisingBrainProblemState(p.n);

        // Search matching
        let matchesSearch = true;
        if (q) {
          const tMatch = p.t.toLowerCase().includes(q);
          const refMatch = (p.ref || '').toLowerCase().includes(q);
          const numMatch = ('#' + p.n).includes(q) || String(p.n) === q;
          const patMatch = pat.name.toLowerCase().includes(q);
          const topMatch = topic.name.toLowerCase().includes(q);
          const coMatch = Array.isArray(p.c) && p.c.some(c => c.toLowerCase().includes(q));
          matchesSearch = (tMatch || refMatch || numMatch || patMatch || topMatch || coMatch);
        }

        // Difficulty matching
        let matchesDiff = true;
        if (currentRbFilter !== 'all') {
          matchesDiff = (p.diff === currentRbFilter);
        }

        // Status matching
        let matchesStatus = true;
        if (currentRbStatusFilter === 'pending') matchesStatus = !ps.done;
        else if (currentRbStatusFilter === 'done') matchesStatus = !!ps.done;
        else if (currentRbStatusFilter === 'attempted') matchesStatus = (ps.status === 'ATTEMPTED');
        else if (currentRbStatusFilter === 'needsrev') matchesStatus = (ps.status === 'NEEDS_REVISION');
        else if (currentRbStatusFilter === 'mastered') matchesStatus = (ps.status === 'MASTERED');
        else if (currentRbStatusFilter === 'starred') matchesStatus = !!ps.starred;

        // Company matching
        let matchesCo = true;
        if (currentRbCompany !== 'all') {
          matchesCo = Array.isArray(p.c) && p.c.some(c => c.toLowerCase().includes(currentRbCompany.toLowerCase()));
        }

        return matchesSearch && matchesDiff && matchesStatus && matchesCo;
      });

      if (visibleProblems.length === 0) return;
      topicHasVisible = true;
      totalVisible += visibleProblems.length;

      const donePatCount = doneRisingBrainProbsForPattern(pat);
      const patPct = Math.round((donePatCount / pat.problems.length) * 100);
      const isPatCollapsed = !!risingBrainState.collapsedPatterns[pat.id];

      topicPatternsHtml += `
        <div class="rb-pattern-card" id="rb-pat-${pat.id}">
          <div class="rb-pattern-header" onclick="toggleRbPatternCollapse('${pat.id}')">
            <div class="rb-pattern-header-left">
              <span class="rb-pat-badge">Pattern ${patIdx + 1}</span>
              <h3 class="rb-pattern-title">${pat.name}</h3>
            </div>
            <div class="rb-pattern-header-right">
              <span class="rb-pattern-ratio">${donePatCount}/${pat.problems.length} solved</span>
              <div class="rb-pat-mini-track">
                <div class="rb-pat-mini-fill" style="width:${patPct}%;"></div>
              </div>
              <span class="rb-pat-pct-badge">${patPct}%</span>
              <svg class="rb-accordion-chevron ${isPatCollapsed ? 'collapsed' : ''}" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </div>
          </div>

          ${!isPatCollapsed ? `
            <div class="rb-pattern-body">
              ${(pat.strategy || pat.desc) ? `
                <div class="rb-pattern-strategy-box">
                  <div class="rb-callout-header">
                    <span>💡</span>
                    <span>Algorithmic Strategy</span>
                  </div>
                  <div class="rb-callout-text">${pat.strategy || pat.desc}</div>
                </div>
              ` : ''}

              ${(pat.identification || pat.clues) ? `
                <div class="rb-pattern-clues-box">
                  <div class="rb-callout-header">
                    <span>🔍</span>
                    <span>Pattern Recognition Clues & Interview Signals</span>
                  </div>
                  <div class="rb-callout-text">${pat.identification || pat.clues}</div>
                </div>
              ` : ''}

              <div class="rb-problems-table">
                ${visibleProblems.map(p => {
                  const ps = getRisingBrainProblemState(p.n);
                  const isDone = !!ps.done;
                  const isStarred = !!ps.starred;
                  const diffClass = p.diff === 'e' ? 'diff-easy' : p.diff === 'm' ? 'diff-med' : 'diff-hard';
                  const diffLabel = p.diff === 'e' ? 'Easy' : p.diff === 'm' ? 'Medium' : 'Hard';

                  const lcUrl = p.l || p.lc;
                  const gfgUrl = p.g || p.gfg;
                  const ytUrl = p.v;
                  let linksHtml = '';

                  if (lcUrl) {
                    linksHtml += `
                      <a class="rb-platform-link lc" href="${lcUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Open on LeetCode">
                        <span>LC</span>
                        <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                      </a>
                    `;
                  }
                  if (gfgUrl) {
                    linksHtml += `
                      <a class="rb-platform-link gfg" href="${gfgUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Open on GeeksforGeeks">
                        <span>GFG</span>
                        <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                      </a>
                    `;
                  }
                  if (ytUrl) {
                    linksHtml += `
                      <a class="rb-platform-link yt" href="${ytUrl}" target="_blank" rel="noopener noreferrer" onclick="event.stopPropagation()" title="Watch video solution">
                        <span>▶ Video</span>
                        <svg class="rb-ext-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                      </a>
                    `;
                  }

                  let coTagsHtml = '';
                  if (Array.isArray(p.c) && p.c.length > 0) {
                    const topCos = p.c.slice(0, 3);
                    const moreCount = p.c.length > 3 ? ` +${p.c.length - 3}` : '';
                    coTagsHtml = `<span class="rb-company-chip" title="Companies: ${p.c.join(', ')}">🏢 ${topCos.join(', ')}${moreCount}</span>`;
                  }

                  let crossRefHtml = '';
                  if (p.cross) {
                    if (p.cross.striver) {
                      crossRefHtml += `<a class="cross-ref-badge" href="javascript:void(0)" onclick="jumpToCrossSheet('striver', ${p.cross.striver.num})" title="Also in Striver Sheet: #${p.cross.striver.num} (${p.cross.striver.title}) in ${p.cross.striver.step}">🔗 Striver #${p.cross.striver.num}</a>`;
                    }
                    if (p.cross.dsa) {
                      crossRefHtml += `<a class="cross-ref-badge dsa-ref" href="javascript:void(0)" onclick="jumpToCrossSheet('dsa', ${p.cross.dsa.num})" title="Also in DSA Patterns: #${p.cross.dsa.num} (${p.cross.dsa.title}) in ${p.cross.dsa.pattern}">🔗 DSA #${p.cross.dsa.num}</a>`;
                    }
                  }

                  let dueTag = '';
                  if (isProblemOverdue(ps)) {
                    dueTag = `<span class="due-badge overdue">⚠️ Overdue</span>`;
                  } else if (isProblemDue(ps)) {
                    dueTag = `<span class="due-badge today">⏰ Due Today</span>`;
                  } else if (ps.nextDueDate) {
                    dueTag = `<span class="due-badge future">Due: ${formatDateDisplay(ps.nextDueDate)}</span>`;
                  }

                  return `
                    <div class="rb-prob-row ${isDone ? 'is-done' : ''}" id="rb-prob-${p.n}">
                      <div class="rb-col-check">
                        <label class="rb-custom-checkbox" title="Mark problem solved">
                          <input type="checkbox" ${isDone ? 'checked' : ''} onchange="toggleRisingBrainDone(${p.n}, this.checked)">
                          <span class="rb-checkmark"></span>
                        </label>
                        <button type="button" class="rb-star-btn ${isStarred ? 'starred' : ''}" onclick="toggleRisingBrainStar(${p.n})" title="${isStarred ? 'Unstar problem' : 'Star problem'}">${isStarred ? '★' : '☆'}</button>
                        <span class="rb-prob-index">#${p.n}</span>
                      </div>

                      <div class="rb-col-main">
                        <div class="rb-prob-title-line">
                          ${p.ref ? `<span class="rb-ref-pill">${p.ref}</span>` : ''}
                          <span class="rb-prob-name" title="${p.t}">${p.t}</span>
                          <span class="rb-diff-badge ${diffClass}" title="Difficulty: ${diffLabel}">${diffLabel}</span>
                          ${dueTag}
                        </div>

                        <div class="rb-prob-sub-line">
                          <div class="rb-links-container">${linksHtml}</div>
                          ${coTagsHtml ? `<div class="rb-companies-container">${coTagsHtml}</div>` : ''}
                          ${crossRefHtml ? `<div class="rb-crossref-container">${crossRefHtml}</div>` : ''}
                        </div>
                      </div>

                      <div class="rb-col-actions">
                        <select class="rb-status-dropdown status-${ps.status || 'NOT_STARTED'}" onchange="setRisingBrainStatus(${p.n}, this.value)" title="Change Practice Status">
                          <option value="NOT_STARTED" ${ps.status === 'NOT_STARTED' ? 'selected' : ''}>⚪ Not Started</option>
                          <option value="ATTEMPTED" ${ps.status === 'ATTEMPTED' ? 'selected' : ''}>🟡 Attempted</option>
                          <option value="SOLVED_INDEPENDENT" ${ps.status === 'SOLVED_INDEPENDENT' ? 'selected' : ''}>🟢 Solved Solo</option>
                          <option value="SOLVED_HINT" ${ps.status === 'SOLVED_HINT' ? 'selected' : ''}>🟠 Solved Hint</option>
                          <option value="NEEDS_REVISION" ${ps.status === 'NEEDS_REVISION' ? 'selected' : ''}>🟣 Needs Rev</option>
                          <option value="MASTERED" ${ps.status === 'MASTERED' ? 'selected' : ''}>👑 Mastered</option>
                        </select>

                        <button class="rb-rev-btn" onclick="openRevisionModal(${p.n}, 'risingbrain')" title="Log revision or inspect notes">
                          <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
                          <span>+1 Rev</span>
                          ${ps.revisionCount > 0 ? `<span class="rb-rev-badge">${ps.revisionCount}</span>` : ''}
                        </button>
                      </div>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>
          ` : ''}
        </div>
      `;
    });

    if (topicHasVisible) {
      const iconCode = RB_TOPIC_ICONS[topic.name] || topic.name.substring(0, 2).toUpperCase();
      html += `
        <div class="rb-topic-section" id="rb-topic-${topic.id}">
          <div class="rb-topic-header">
            <div class="rb-topic-title-wrap">
              <span class="rb-topic-icon">${iconCode}</span>
              <div>
                <div class="rb-topic-name">${topic.name}</div>
                <div class="rb-topic-desc">${topic.desc}</div>
              </div>
            </div>
            <div class="rb-topic-stats-wrap">
              <span class="rb-topic-ratio">${doneTopicCount} / ${totalTopicCount} solved</span>
              <div class="step-mini-bar" style="width:90px;"><div class="step-mini-fill" style="width:${topicPct}%; background:#10b981;"></div></div>
              <button class="rb-topic-toggle-btn" onclick="toggleRbTopicCollapse('${topic.id}')">
                ${isTopicCollapsed ? 'Expand Topic ▼' : 'Collapse Topic ▲'}
              </button>
            </div>
          </div>
          ${!isTopicCollapsed ? topicPatternsHtml : ''}
        </div>
      `;
    }
  });

  if (totalVisible === 0) {
    html = `
      <div class="rb-empty-state">
        <div class="rb-empty-icon">🔍</div>
        <div class="rb-empty-title">No Matching RisingBrain Problems Found</div>
        <div class="rb-empty-subtitle">We couldn't find any questions matching your current search query or filter combination.</div>
        <button class="rb-empty-reset-btn" onclick="resetAllRbFilters()">Clear All Filters & Show 385 Problems</button>
      </div>
    `;
  }

  content.innerHTML = html;
}
"""

def assemble_and_test():
    with open('/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace CSS
    css_start_tag = '/* ==========================================================================\n   RISINGBRAIN PATTERN-WISE STYLES & CLUES'
    css_end_tag = '</style>'
    
    start_pos = html.find(css_start_tag)
    if start_pos == -1:
        # try more flexible match
        css_start_regex = re.compile(r'/\*\s*=+ RISINGBRAIN PATTERN-WISE STYLES & CLUES =+\s*\*/')
        m = css_start_regex.search(html)
        if m:
            start_pos = m.start()
        else:
            print("ERROR: Could not locate RisingBrain CSS section!")
            return False

    end_pos = html.find(css_end_tag, start_pos)
    if end_pos == -1:
        print("ERROR: Could not locate </style> after RisingBrain CSS!")
        return False

    new_css = generate_redesigned_css()
    html = html[:start_pos] + new_css.strip() + "\n\n" + html[end_pos:]

    # 2. Replace HTML markup for view-risingbrain
    view_start_tag = '<section class="view-section" id="view-risingbrain">'
    view_end_tag = '</section>'
    v_start = html.find(view_start_tag)
    if v_start == -1:
        # try comment
        v_start = html.find('<!-- VIEW 2.7: RISINGBRAIN PATTERN-WISE SHEET -->')
    
    if v_start == -1:
        print("ERROR: Could not locate view-risingbrain HTML section!")
        return False

    v_end = html.find('</section>', v_start) + len('</section>')
    new_view_markup = generate_view_markup()
    html = html[:v_start] + new_view_markup + html[v_end:]

    # 3. Enhance openRevisionModal, undoLastRevision, saveProblemNotesDebounced
    # openRevisionModal update:
    target_rev_modal = """  if (trackerType === 'striver') {
    ps = getStriverProblemState(probNum);
    STRIVER_DATA.forEach(s => {
      const found = s.problems.find(p => p.n === probNum);
      if (found) { pObj = found; stepName = s.name; }
    });
  } else {
    ps = getProblemState(probNum);
    DATA.forEach(s => {
      const found = s.problems.find(p => p.n === probNum);
      if (found) { pObj = found; stepName = s.name; }
    });
  }"""
    
    replacement_rev_modal = """  if (trackerType === 'striver') {
    ps = getStriverProblemState(probNum);
    STRIVER_DATA.forEach(s => {
      const found = s.problems.find(p => p.n === probNum);
      if (found) { pObj = found; stepName = s.name; }
    });
  } else if (trackerType === 'risingbrain') {
    ps = getRisingBrainProblemState(probNum);
    RISINGBRAIN_DATA.forEach(t => {
      t.patterns.forEach(pat => {
        const found = pat.problems.find(p => p.n === probNum);
        if (found) { pObj = found; stepName = `${t.name} · ${pat.name}`; }
      });
    });
  } else {
    ps = getProblemState(probNum);
    DATA.forEach(s => {
      const found = s.problems.find(p => p.n === probNum);
      if (found) { pObj = found; stepName = s.name; }
    });
  }"""
    
    if target_rev_modal in html:
        html = html.replace(target_rev_modal, replacement_rev_modal, 1)
        print("Updated openRevisionModal with risingbrain support!")
    else:
        print("Note: target_rev_modal exact string not matched; checking if already present...")

    # undoLastRevision update:
    target_undo = """function undoLastRevision() {
  if (!activeModalProbNum) return;
  const isStriver = activeModalTracker === 'striver';
  const ps = isStriver ? getStriverProblemState(activeModalProbNum) : getProblemState(activeModalProbNum);
  if (!ps.revisions || ps.revisions.length === 0) return;

  const removed = ps.revisions.pop();
  ps.revisionCount = ps.revisions.length;

  if (ps.revisions.length > 0) {
    const last = ps.revisions[ps.revisions.length - 1];
    ps.lastRevisedDate = last.date;
    const { nextDueDate, nextLevel } = calculateNextDueDate(last.outcome, Math.max(0, ps.spacedIntervalLevel - 1));
    ps.nextDueDate = nextDueDate;
    ps.spacedIntervalLevel = nextLevel;
  } else {
    ps.lastRevisedDate = null;
    ps.nextDueDate = null;
    ps.spacedIntervalLevel = 0;
  }

  if (isStriver) {
    striverState.problems[activeModalProbNum] = ps;
    saveStriverState();
    renderStriverContent();
  } else {
    state.problems[activeModalProbNum] = ps;
    saveState();
    refreshAllUI();
  }"""

    replacement_undo = """function undoLastRevision() {
  if (!activeModalProbNum) return;
  const isRisingBrain = activeModalTracker === 'risingbrain';
  const isStriver = activeModalTracker === 'striver';
  const ps = isRisingBrain ? getRisingBrainProblemState(activeModalProbNum) : isStriver ? getStriverProblemState(activeModalProbNum) : getProblemState(activeModalProbNum);
  if (!ps.revisions || ps.revisions.length === 0) return;

  const removed = ps.revisions.pop();
  ps.revisionCount = ps.revisions.length;

  if (ps.revisions.length > 0) {
    const last = ps.revisions[ps.revisions.length - 1];
    ps.lastRevisedDate = last.date;
    const { nextDueDate, nextLevel } = calculateNextDueDate(last.outcome, Math.max(0, ps.spacedIntervalLevel - 1));
    ps.nextDueDate = nextDueDate;
    ps.spacedIntervalLevel = nextLevel;
  } else {
    ps.lastRevisedDate = null;
    ps.nextDueDate = null;
    ps.spacedIntervalLevel = 0;
  }

  if (isRisingBrain) {
    risingBrainState.problems[activeModalProbNum] = ps;
    saveRisingBrainState();
    renderRisingBrainContent();
    updateRisingBrainStats();
  } else if (isStriver) {
    striverState.problems[activeModalProbNum] = ps;
    saveStriverState();
    renderStriverContent();
  } else {
    state.problems[activeModalProbNum] = ps;
    saveState();
    refreshAllUI();
  }"""

    if target_undo in html:
        html = html.replace(target_undo, replacement_undo, 1)
        print("Updated undoLastRevision with risingbrain support!")

    # saveProblemNotesDebounced update:
    target_notes = """function saveProblemNotesDebounced() {
  clearTimeout(problemNotesAutosaveTimeout);
  problemNotesAutosaveTimeout = setTimeout(() => {
    if (!activeModalProbNum) return;
    const isStriver = activeModalTracker === 'striver';
    const ps = isStriver ? getStriverProblemState(activeModalProbNum) : getProblemState(activeModalProbNum);
    if (!ps.notes) ps.notes = { approach: '', mistakes: '', complexity: '' };
    ps.notes.approach = document.getElementById('probNoteApproach').value;
    ps.notes.mistakes = document.getElementById('probNoteMistakes').value;
    if (isStriver) {
      striverState.problems[activeModalProbNum] = ps;
      saveStriverState();
    } else {
      state.problems[activeModalProbNum] = ps;
      saveState();
    }
  }, 500);
}"""

    replacement_notes = """function saveProblemNotesDebounced() {
  clearTimeout(problemNotesAutosaveTimeout);
  problemNotesAutosaveTimeout = setTimeout(() => {
    if (!activeModalProbNum) return;
    const isRisingBrain = activeModalTracker === 'risingbrain';
    const isStriver = activeModalTracker === 'striver';
    const ps = isRisingBrain ? getRisingBrainProblemState(activeModalProbNum) : isStriver ? getStriverProblemState(activeModalProbNum) : getProblemState(activeModalProbNum);
    if (!ps.notes) ps.notes = { approach: '', mistakes: '', complexity: '' };
    ps.notes.approach = document.getElementById('probNoteApproach').value;
    ps.notes.mistakes = document.getElementById('probNoteMistakes').value;
    if (isRisingBrain) {
      risingBrainState.problems[activeModalProbNum] = ps;
      saveRisingBrainState();
    } else if (isStriver) {
      striverState.problems[activeModalProbNum] = ps;
      saveStriverState();
    } else {
      state.problems[activeModalProbNum] = ps;
      saveState();
    }
  }, 500);
}"""

    if target_notes in html:
        html = html.replace(target_notes, replacement_notes, 1)
        print("Updated saveProblemNotesDebounced with risingbrain support!")

    # 4. Replace RisingBrain JS functions
    # Find start of renderRisingBrainContent or updateRisingBrainStats
    js_func_start = html.find('function renderRisingBrainContent() {')
    js_init_start = html.find('/* ==========================================================================\n   INITIALIZATION')
    if js_init_start == -1:
        js_init_start = html.find('function init() {')

    if js_func_start != -1 and js_init_start != -1:
        new_js = generate_upgraded_js()
        html = html[:js_func_start] + new_js.strip() + "\n\n" + html[js_init_start:]
        print("Successfully replaced RisingBrain JS rendering engine!")
    else:
        print("ERROR: Could not locate RisingBrain JS engine bounds!")
        return False

    out_path = '/Users/devrajput/.gemini/antigravity-ide/scratch/test_redesign_assembled.html'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Assembled test redesign HTML file: {out_path} ({len(html)} bytes)")
    return True

if __name__ == '__main__':
    assemble_and_test()
