import os, re, json

with open("/Users/devrajput/@Resources/Tracker/dsa_patterns_trackerfinal copy.html") as f:
    html = f.read()

# ---------------------------------------------------------------------------
# 1. NEW CSS FOR VIEW 5: PRIVATE DIARY
# ---------------------------------------------------------------------------
new_diary_css = """/* ==========================================================================
   VIEW 5: PRIVATE PLACEMENT JOURNAL (PREMIUM REDESIGN)
   ========================================================================== */
.diary-container {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 350px;
  gap: 1.5rem;
  align-items: start;
}

@media (max-width: 1120px) {
  .diary-container {
    grid-template-columns: 1fr;
  }
}

/* Main Workspace */
.diary-workspace {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.diary-card {
  background: var(--surface, #0e131b);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.28);
  position: relative;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.diary-card:hover {
  border-color: rgba(255, 255, 255, 0.12);
}

/* Header Banner */
.diary-header-card {
  padding: 1.5rem 1.75rem;
}

.diary-header-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.diary-header-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.diary-pretitle-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  width: fit-content;
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent, #10b981);
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.22);
  padding: 3px 10px;
  border-radius: 9999px;
}

.diary-header-title {
  font-family: var(--font-heading, 'Syne', sans-serif);
  font-size: 1.4rem;
  font-weight: 700;
  color: #f1f5f9;
  letter-spacing: -0.02em;
  margin: 0;
}

.diary-header-subtitle {
  font-size: 0.82rem;
  color: #94a3b8;
  margin: 0;
  line-height: 1.45;
  max-width: 600px;
}

.diary-header-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.diary-save-badge {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  border-radius: 9999px;
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.25);
  color: #10b981;
  transition: all 0.2s ease;
}

.diary-save-badge.saving {
  background: rgba(245, 158, 11, 0.1);
  border-color: rgba(245, 158, 11, 0.3);
  color: #f59e0b;
}

.diary-save-badge.error {
  background: rgba(239, 68, 68, 0.1);
  border-color: rgba(239, 68, 68, 0.3);
  color: #ef4444;
}

.diary-streak-badge {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 11px;
  border-radius: 9999px;
  background: rgba(245, 158, 11, 0.08);
  border: 1px solid rgba(245, 158, 11, 0.22);
  color: #f59e0b;
}

.diary-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 11.5px;
  font-weight: 600;
  padding: 5px 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  cursor: pointer;
  transition: all 0.18s ease;
}

.diary-action-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.2);
  color: #f8fafc;
}

.diary-action-btn.delete-btn {
  background: rgba(239, 68, 68, 0.06);
  border-color: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.diary-action-btn.delete-btn:hover {
  background: rgba(239, 68, 68, 0.14);
  border-color: rgba(239, 68, 68, 0.35);
  color: #fca5a5;
}

/* Date Navigator Bar */
.diary-date-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
  margin-top: 1.25rem;
  padding: 0.65rem 1rem;
  background: rgba(20, 27, 36, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  flex-wrap: wrap;
}

.diary-date-nav-left {
  display: flex;
  align-items: center;
  gap: 0.65rem;
}

.diary-nav-arrow-btn {
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #cbd5e1;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.15s ease;
}

.diary-nav-arrow-btn:hover {
  background: rgba(16, 185, 129, 0.12);
  border-color: var(--accent);
  color: var(--accent);
}

.diary-date-display {
  font-family: var(--font-heading, sans-serif);
  font-size: 0.95rem;
  font-weight: 700;
  color: #f8fafc;
}

.diary-date-tag {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 9999px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.28);
  color: var(--accent);
}

.diary-date-tag.past {
  background: rgba(148, 163, 184, 0.08);
  border-color: rgba(148, 163, 184, 0.2);
  color: #94a3b8;
}

.diary-date-tag.future {
  background: rgba(56, 189, 248, 0.1);
  border-color: rgba(56, 189, 248, 0.25);
  color: #38bdf8;
}

.diary-date-nav-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.diary-date-picker-input {
  background: #090e14;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  padding: 4px 8px;
  font-family: var(--font-mono);
  font-size: 11.5px;
  color: #cbd5e1;
  color-scheme: dark;
  cursor: pointer;
}

.diary-today-btn {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 6px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.25);
  color: var(--accent);
  cursor: pointer;
  transition: all 0.15s ease;
}

.diary-today-btn:hover {
  background: var(--accent);
  color: #0d131a;
}

/* Mental State & Energy Section */
.diary-metrics-grid {
  display: grid;
  grid-template-columns: 1.15fr 1fr 1fr;
  gap: 1.25rem;
  background: var(--surface2, #141b24);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 14px;
  padding: 1.25rem;
}

@media (max-width: 900px) {
  .diary-metrics-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
}

.diary-metric-col {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.diary-metric-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2px;
}

.diary-metric-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 4px;
}

.diary-metric-val-tag {
  font-family: var(--font-mono);
  font-size: 11px;
  font-weight: 600;
  color: var(--accent, #10b981);
}

.diary-mood-bar {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 5px;
}

.diary-mood-pill {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  padding: 7px 4px;
  border-radius: 9px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}

.diary-mood-pill:hover {
  background: rgba(255, 255, 255, 0.06);
  border-color: rgba(255, 255, 255, 0.15);
  transform: translateY(-1px);
}

.diary-mood-pill.active {
  background: rgba(16, 185, 129, 0.14);
  border-color: var(--accent);
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.22);
}

.diary-mood-emoji {
  font-size: 1.15rem;
  line-height: 1;
}

.diary-mood-text {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  color: #94a3b8;
}

.diary-mood-pill.active .diary-mood-text {
  color: var(--accent);
}

/* Rating Beads Track */
.diary-rating-track {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 5px;
}

.diary-rating-cell {
  height: 38px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  font-family: var(--font-mono);
  font-size: 11.5px;
  font-weight: 700;
  color: #64748b;
  transition: all 0.15s ease;
}

.diary-rating-cell:hover {
  background: rgba(255, 255, 255, 0.07);
  color: #cbd5e1;
}

.diary-rating-cell.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #0b1117;
  font-weight: 800;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.3);
}

.diary-rating-cell.energy-active {
  background: #f59e0b;
  border-color: #f59e0b;
  color: #0b1117;
  font-weight: 800;
  box-shadow: 0 0 12px rgba(245, 158, 11, 0.3);
}

/* Writing Sections */
.diary-section-block {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.diary-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.diary-section-title-wrap {
  display: flex;
  align-items: center;
  gap: 7px;
}

.diary-section-icon {
  font-size: 1rem;
}

.diary-section-title {
  font-family: var(--font-heading, sans-serif);
  font-size: 0.95rem;
  font-weight: 700;
  color: #f1f5f9;
}

.diary-word-counter {
  font-family: var(--font-mono);
  font-size: 10.5px;
  color: #64748b;
  background: rgba(255, 255, 255, 0.03);
  padding: 2px 7px;
  border-radius: 9999px;
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.diary-section-prompt {
  font-size: 0.78rem;
  color: #94a3b8;
  line-height: 1.4;
  margin: 0;
}

.diary-textarea-field {
  width: 100%;
  background: #090e15;
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 11px;
  padding: 0.85rem 1rem;
  font-family: var(--font-sans, Inter, sans-serif);
  font-size: 0.88rem;
  line-height: 1.6;
  color: #f1f5f9;
  resize: vertical;
  min-height: 95px;
  transition: all 0.2s ease;
  outline: none;
}

.diary-textarea-field:focus {
  border-color: var(--accent);
  background: #0c121b;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

.diary-textarea-field::placeholder {
  color: #475569;
}

.diary-textarea-field.freeform {
  min-height: 120px;
}

.diary-input-field {
  width: 100%;
  background: #090e15;
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 9px;
  padding: 0.7rem 0.9rem;
  font-family: var(--font-sans, Inter, sans-serif);
  font-size: 0.88rem;
  color: #f1f5f9;
  outline: none;
  transition: all 0.2s ease;
}

.diary-input-field:focus {
  border-color: var(--accent);
  background: #0c121b;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.15);
}

.diary-input-field::placeholder {
  color: #475569;
}

/* Tomorrow's Priorities */
.diary-priorities-wrap {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  margin-top: 0.25rem;
}

.diary-priority-row {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  background: #090e15;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 0.4rem 0.75rem;
  transition: all 0.18s ease;
}

.diary-priority-row:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.12);
}

.diary-prio-badge {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 5px;
  white-space: nowrap;
}

.diary-prio-badge.p1 {
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.25);
  color: #f87171;
}

.diary-prio-badge.p2 {
  background: rgba(245, 158, 11, 0.12);
  border: 1px solid rgba(245, 158, 11, 0.25);
  color: #fbbf24;
}

.diary-prio-badge.p3 {
  background: rgba(56, 189, 248, 0.12);
  border: 1px solid rgba(56, 189, 248, 0.25);
  color: #38bdf8;
}

.diary-prio-checkbox {
  width: 17px;
  height: 17px;
  accent-color: var(--accent);
  cursor: pointer;
}

.diary-priority-input {
  flex: 1;
  background: transparent;
  border: none;
  color: #f1f5f9;
  font-size: 0.88rem;
  outline: none;
  font-family: var(--font-sans, Inter, sans-serif);
}

.diary-priority-input::placeholder {
  color: #475569;
}

.diary-priority-row.completed .diary-priority-input {
  text-decoration: line-through;
  color: #64748b;
}

/* Sidebar History & Insights */
.diary-sidebar-panel {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.diary-history-card {
  background: var(--surface, #0e131b);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.28);
}

.diary-history-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.75rem;
}

.diary-history-title {
  font-family: var(--font-heading, sans-serif);
  font-size: 1rem;
  font-weight: 700;
  color: #f8fafc;
  display: flex;
  align-items: center;
  gap: 6px;
}

.diary-count-pill {
  font-family: var(--font-mono);
  font-size: 10.5px;
  font-weight: 600;
  padding: 2px 7px;
  border-radius: 9999px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #94a3b8;
}

.diary-search-box {
  position: relative;
  margin-bottom: 0.75rem;
}

.diary-search-input {
  width: 100%;
  background: #090e15;
  border: 1px solid rgba(255, 255, 255, 0.09);
  border-radius: 9px;
  padding: 0.55rem 0.85rem 0.55rem 2rem;
  font-size: 0.82rem;
  color: #f1f5f9;
  outline: none;
  transition: all 0.2s ease;
}

.diary-search-input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.15);
}

.diary-search-icon {
  position: absolute;
  left: 0.65rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
  pointer-events: none;
  font-size: 12px;
}

.diary-history-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-height: 480px;
  overflow-y: auto;
  padding-right: 2px;
}

.diary-history-item {
  padding: 0.75rem 0.9rem;
  background: rgba(20, 27, 36, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.diary-history-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.14);
  transform: translateX(2px);
}

.diary-history-item.active {
  background: rgba(16, 185, 129, 0.09);
  border-color: var(--accent);
  box-shadow: 0 0 14px rgba(16, 185, 129, 0.15);
}

.diary-history-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.diary-history-item-date {
  font-family: var(--font-heading, sans-serif);
  font-size: 0.82rem;
  font-weight: 700;
  color: #f1f5f9;
  display: flex;
  align-items: center;
  gap: 5px;
}

.diary-history-item.active .diary-history-item-date {
  color: var(--accent);
}

.diary-history-badges {
  display: flex;
  align-items: center;
  gap: 4px;
}

.diary-history-mini-pill {
  font-family: var(--font-mono);
  font-size: 9.5px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.04);
  color: #94a3b8;
}

.diary-history-item-preview {
  font-size: 0.76rem;
  color: #64748b;
  line-height: 1.35;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Insights Card */
.diary-insights-card {
  background: var(--surface, #0e131b);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 1.25rem;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.28);
}

.diary-insights-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.85rem;
}

.diary-insights-title {
  font-family: var(--font-heading, sans-serif);
  font-size: 0.95rem;
  font-weight: 700;
  color: #f8fafc;
  display: flex;
  align-items: center;
  gap: 6px;
}

.diary-insights-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.65rem;
}

.diary-stat-tile {
  background: rgba(20, 27, 36, 0.65);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 0.75rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.diary-stat-val {
  font-family: var(--font-mono);
  font-size: 1.15rem;
  font-weight: 700;
  color: #f1f5f9;
}

.diary-stat-val.accent {
  color: var(--accent);
}

.diary-stat-label {
  font-size: 10px;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.03em;
}

.diary-insight-tip-box {
  margin-top: 0.85rem;
  background: rgba(16, 185, 129, 0.06);
  border: 1px solid rgba(16, 185, 129, 0.18);
  border-radius: 10px;
  padding: 0.7rem 0.85rem;
  display: flex;
  align-items: flex-start;
  gap: 7px;
}

.diary-insight-tip-text {
  font-size: 0.78rem;
  color: #94a3b8;
  line-height: 1.4;
  margin: 0;
}
"""

# ---------------------------------------------------------------------------
# 2. NEW HTML FOR <section class="view-section" id="view-diary">
# ---------------------------------------------------------------------------
new_diary_html = """<section class="view-section" id="view-diary">
      <div class="diary-container">
        <!-- Main Writing Workspace -->
        <div class="diary-workspace">
          
          <!-- Header Banner & Date Navigation -->
          <div class="diary-card diary-header-card">
            <div class="diary-header-top">
              <div class="diary-header-title-group">
                <span class="diary-pretitle-pill">📓 Private Placement Journal</span>
                <h2 class="diary-header-title">Daily Debrief & Reflection</h2>
                <p class="diary-header-subtitle">Reflect on problem patterns cracked, document edge-case lessons, and lock in tomorrow's priorities.</p>
              </div>

              <div class="diary-header-actions">
                <span class="diary-streak-badge" id="diaryStreakBadge">🔥 1 d streak</span>
                <span class="diary-save-badge" id="diarySavedIndicator">Saved ✓</span>
                <button type="button" class="diary-action-btn" onclick="exportDiary('md')" title="Export journal entries to clean Markdown">
                  <span>📥</span> Export MD
                </button>
                <button type="button" class="diary-action-btn delete-btn" onclick="confirmDeleteDiaryEntry()" title="Delete entry for the currently selected date">
                  <span>🗑</span> Delete
                </button>
              </div>
            </div>

            <!-- Date Navigator Bar -->
            <div class="diary-date-nav">
              <div class="diary-date-nav-left">
                <button type="button" class="diary-nav-arrow-btn" onclick="changeDiaryDate(-1)" title="Go to previous day">◀</button>
                <span class="diary-date-display" id="diaryCurrentDateLabel">Loading date...</span>
                <span class="diary-date-tag" id="diaryDateBadge">Today</span>
                <button type="button" class="diary-nav-arrow-btn" onclick="changeDiaryDate(1)" title="Go to next day">▶</button>
              </div>

              <div class="diary-date-nav-right">
                <button type="button" class="diary-today-btn" onclick="jumpToDiaryToday()">Today</button>
                <input type="date" id="diaryDateInput" class="diary-date-picker-input" onchange="onDiaryDatePickerChange(this.value)" title="Jump directly to a specific date">
              </div>
            </div>
          </div>

          <!-- Mental State, Focus & Energy Selector -->
          <div class="diary-metrics-grid">
            <!-- Mood Selector -->
            <div class="diary-metric-col">
              <div class="diary-metric-label-row">
                <span class="diary-metric-label">🧠 Mental State</span>
                <span class="diary-metric-val-tag" id="diaryMoodValLabel">Productive</span>
              </div>
              <div class="diary-mood-bar" id="diaryMoodSelector">
                <button type="button" class="diary-mood-pill" data-mood="great" onclick="setDiaryMood('great')" title="Flow State / Peak Energy">
                  <span class="diary-mood-emoji">🤩</span>
                  <span class="diary-mood-text">Flow</span>
                </button>
                <button type="button" class="diary-mood-pill" data-mood="good" onclick="setDiaryMood('good')" title="Productive / Solid Output">
                  <span class="diary-mood-emoji">😊</span>
                  <span class="diary-mood-text">Good</span>
                </button>
                <button type="button" class="diary-mood-pill" data-mood="neutral" onclick="setDiaryMood('neutral')" title="Steady / Moderate">
                  <span class="diary-mood-emoji">😐</span>
                  <span class="diary-mood-text">Steady</span>
                </button>
                <button type="button" class="diary-mood-pill" data-mood="low" onclick="setDiaryMood('low')" title="Fatigued / Low Energy">
                  <span class="diary-mood-emoji">😔</span>
                  <span class="diary-mood-text">Low</span>
                </button>
                <button type="button" class="diary-mood-pill" data-mood="stressed" onclick="setDiaryMood('stressed')" title="Challenged / High Resistance">
                  <span class="diary-mood-emoji">😫</span>
                  <span class="diary-mood-text">Tired</span>
                </button>
              </div>
            </div>

            <!-- Focus Rating -->
            <div class="diary-metric-col">
              <div class="diary-metric-label-row">
                <span class="diary-metric-label">🎯 Deep Focus</span>
                <span class="diary-metric-val-tag" id="diaryFocusValLabel">3 / 5</span>
              </div>
              <div class="diary-rating-track" id="diaryFocusRating">
                <div class="diary-rating-cell" data-val="1" onclick="setDiaryRating('focus', 1)" title="1 - Scattered / Low Concentration">1</div>
                <div class="diary-rating-cell" data-val="2" onclick="setDiaryRating('focus', 2)" title="2 - Distracted / Slow progress">2</div>
                <div class="diary-rating-cell" data-val="3" onclick="setDiaryRating('focus', 3)" title="3 - Good steady focus">3</div>
                <div class="diary-rating-cell" data-val="4" onclick="setDiaryRating('focus', 4)" title="4 - Deep uninterrupted work">4</div>
                <div class="diary-rating-cell" data-val="5" onclick="setDiaryRating('focus', 5)" title="5 - Flawless flow state">5</div>
              </div>
            </div>

            <!-- Energy Level -->
            <div class="diary-metric-col">
              <div class="diary-metric-label-row">
                <span class="diary-metric-label">⚡ Physical Energy</span>
                <span class="diary-metric-val-tag" id="diaryEnergyValLabel" style="color:#f59e0b;">3 / 5</span>
              </div>
              <div class="diary-rating-track" id="diaryEnergyRating">
                <div class="diary-rating-cell" data-val="1" onclick="setDiaryRating('energy', 1)" title="1 - Exhausted">1</div>
                <div class="diary-rating-cell" data-val="2" onclick="setDiaryRating('energy', 2)" title="2 - Sluggish">2</div>
                <div class="diary-rating-cell" data-val="3" onclick="setDiaryRating('energy', 3)" title="3 - Moderate">3</div>
                <div class="diary-rating-cell" data-val="4" onclick="setDiaryRating('energy', 4)" title="4 - High Alertness">4</div>
                <div class="diary-rating-cell" data-val="5" onclick="setDiaryRating('energy', 5)" title="5 - Peak Energy">5</div>
              </div>
            </div>
          </div>

          <!-- Section 1: Accomplishments & Topics Studied -->
          <div class="diary-card diary-section-block">
            <div class="diary-section-header">
              <div class="diary-section-title-wrap">
                <span class="diary-section-icon">🏆</span>
                <span class="diary-section-title">Accomplishments & Topics Studied Today</span>
              </div>
              <span class="diary-word-counter" id="diaryCounterAcc">0 words</span>
            </div>
            <p class="diary-section-prompt">What algorithms, problem patterns, or system concepts did you master or conquer today?</p>
            <textarea class="diary-textarea-field" id="diaryAccomplishments" placeholder="e.g. Solved 3 Sliding Window questions (Maximum Subarray, Minimum Window Substring). Clear intuition on contracting left pointer when condition breaks..." oninput="onDiaryInputChanged()"></textarea>
          </div>

          <!-- Section 2: Mistakes, Doubts & Lessons Learned -->
          <div class="diary-card diary-section-block">
            <div class="diary-section-header">
              <div class="diary-section-title-wrap">
                <span class="diary-section-icon">⚠️</span>
                <span class="diary-section-title">Mistakes, Edge Cases & Lessons Learned</span>
              </div>
              <span class="diary-word-counter" id="diaryCounterMist">0 words</span>
            </div>
            <p class="diary-section-prompt">Where did you get stuck? What edge case, off-by-one index, or TLE tripped you up? Turn it into a permanent rule.</p>
            <textarea class="diary-textarea-field" id="diaryMistakes" placeholder="e.g. In binary search on rotated array, forgot to check if nums[mid] == nums[left] when duplicates exist. Rule: strictly narrow window when bounds match..." oninput="onDiaryInputChanged()"></textarea>
          </div>

          <!-- Section 3: Distractions & Time Wasters -->
          <div class="diary-card diary-section-block">
            <div class="diary-section-header">
              <div class="diary-section-title-wrap">
                <span class="diary-section-icon">🛑</span>
                <span class="diary-section-title">Distractions & Time Wasters Faced</span>
              </div>
              <span class="diary-word-counter" id="diaryCounterDist">0 words</span>
            </div>
            <p class="diary-section-prompt">Phone notifications, context switching, fatigue, endless tabs... what hindered deep work and how will you block it tomorrow?</p>
            <textarea class="diary-textarea-field" style="min-height:75px;" id="diaryDistractions" placeholder="e.g. Spent 30 mins browsing social media after lunch. Action: leave phone in another room during 2-hour morning deep work slot..." oninput="onDiaryInputChanged()"></textarea>
          </div>

          <!-- Section 4: Free-Form Reflection & Strategic Notes -->
          <div class="diary-card diary-section-block">
            <div class="diary-section-header">
              <div class="diary-section-title-wrap">
                <span class="diary-section-icon">📝</span>
                <span class="diary-section-title">Free-Form Mindset & Strategic Notes</span>
              </div>
              <span class="diary-word-counter" id="diaryCounterFree">0 words</span>
            </div>
            <p class="diary-section-prompt">Mindset reflection, interview preparation observations, target company shortlists, or mental resets.</p>
            <textarea class="diary-textarea-field freeform" id="diaryFreeform" placeholder="e.g. Feeling much more confident about Trees & BSTs after 4 days of recursion practice. Need to schedule dynamic programming revision next..." oninput="onDiaryInputChanged()"></textarea>
          </div>

          <!-- Section 5: Tomorrow's Top 3 Priorities -->
          <div class="diary-card diary-section-block">
            <div class="diary-section-header">
              <div class="diary-section-title-wrap">
                <span class="diary-section-icon">🚀</span>
                <span class="diary-section-title">Tomorrow's Top 3 Priorities</span>
              </div>
              <span class="diary-word-counter" id="diaryCounterPrio">0 / 3 done</span>
            </div>
            <p class="diary-section-prompt">Prime tomorrow's momentum before going to sleep. Prioritize high-impact problem patterns and revisions.</p>
            
            <div class="diary-priorities-wrap">
              <!-- Priority 1 -->
              <div class="diary-priority-row" id="diaryPrioRow0">
                <span class="diary-prio-badge p1">P1 • Critical</span>
                <input type="checkbox" id="diaryPrioDone1" class="diary-prio-checkbox" onchange="toggleDiaryPriorityDone(0, this.checked)" title="Mark priority complete">
                <input type="text" class="diary-priority-input" id="diaryPrio1" placeholder="1. Most critical pattern or problem to solve first thing in the morning..." oninput="onDiaryInputChanged()">
              </div>

              <!-- Priority 2 -->
              <div class="diary-priority-row" id="diaryPrioRow1">
                <span class="diary-prio-badge p2">P2 • High</span>
                <input type="checkbox" id="diaryPrioDone2" class="diary-prio-checkbox" onchange="toggleDiaryPriorityDone(1, this.checked)" title="Mark priority complete">
                <input type="text" class="diary-priority-input" id="diaryPrio2" placeholder="2. Revision batch or secondary problem set..." oninput="onDiaryInputChanged()">
              </div>

              <!-- Priority 3 -->
              <div class="diary-priority-row" id="diaryPrioRow2">
                <span class="diary-prio-badge p3">P3 • Moderate</span>
                <input type="checkbox" id="diaryPrioDone3" class="diary-prio-checkbox" onchange="toggleDiaryPriorityDone(2, this.checked)" title="Mark priority complete">
                <input type="text" class="diary-priority-input" id="diaryPrio3" placeholder="3. Core CS theory (OS/DBMS), mock interview problem, or company review..." oninput="onDiaryInputChanged()">
              </div>
            </div>
          </div>

        </div>

        <!-- Right Side Panel: History, Search & Insights -->
        <div class="diary-sidebar-panel">
          
          <!-- History & Search Card -->
          <div class="diary-history-card">
            <div class="diary-history-header">
              <div class="diary-history-title">
                <span>📅</span>
                <span>Journal History</span>
              </div>
              <span class="diary-count-pill" id="diaryHistoryCountBadge">0 entries</span>
            </div>

            <!-- Search Filter -->
            <div class="diary-search-box">
              <span class="diary-search-icon">🔍</span>
              <input type="text" class="diary-search-input" id="diarySearchInput" placeholder="Search entries, topics, notes..." oninput="renderDiaryHistoryList()">
            </div>

            <!-- History Entries Scroll List -->
            <div class="diary-history-list" id="diaryHistoryList">
              <!-- Dynamically populated -->
            </div>
          </div>

          <!-- Weekly/Monthly Reflection Insights Card -->
          <div class="diary-insights-card" id="diaryInsightsCard">
            <div class="diary-insights-header">
              <div class="diary-insights-title">
                <span>📊</span>
                <span>Reflective Insights</span>
              </div>
            </div>

            <div class="diary-insights-grid">
              <div class="diary-stat-tile">
                <span class="diary-stat-val accent" id="diaryStatTotalEntries">0</span>
                <span class="diary-stat-label">Debriefs Logged</span>
              </div>
              <div class="diary-stat-tile">
                <span class="diary-stat-val" id="diaryStatAvgFocus">0.0</span>
                <span class="diary-stat-label">Avg Focus (1-5)</span>
              </div>
              <div class="diary-stat-tile">
                <span class="diary-stat-val" id="diaryStatAvgEnergy" style="color:#f59e0b;">0.0</span>
                <span class="diary-stat-label">Avg Energy (1-5)</span>
              </div>
              <div class="diary-stat-tile">
                <span class="diary-stat-val" id="diaryStatCommonMood">😊 Good</span>
                <span class="diary-stat-label">Dominant Mood</span>
              </div>
            </div>

            <div class="diary-insight-tip-box">
              <span style="font-size:1rem; line-height:1;">💡</span>
              <p class="diary-insight-tip-text" id="diaryInsightTipText">Consistent reflection turns random mistakes into algorithmic mastery. Every daily entry compounds into placement readiness.</p>
            </div>
          </div>

        </div>
      </div>
    </section>"""

# ---------------------------------------------------------------------------
# 3. NEW JAVASCRIPT FOR PRIVATE DIARY ENGINE
# ---------------------------------------------------------------------------
new_diary_js = """/* ==========================================================================
   PRIVATE PLACEMENT JOURNAL ENGINE (PREMIUM REDESIGN)
   Offline-first, Autosaving, Date-Navigable, Insights-Driven
   ========================================================================== */

function getDiaryEntry(dateKey) {
  if (!diaryState.entries[dateKey]) {
    diaryState.entries[dateKey] = {
      date: dateKey,
      updatedAt: Date.now(),
      mood: 'good',
      focusRating: 3,
      energyRating: 3,
      accomplishments: '',
      mistakes: '',
      distractions: '',
      freeform: '',
      priorities: ['', '', ''],
      priorityDone: [false, false, false]
    };
  } else {
    // Ensure priorityDone exists non-destructively
    const e = diaryState.entries[dateKey];
    if (!Array.isArray(e.priorityDone)) {
      e.priorityDone = [false, false, false];
    }
  }
  return diaryState.entries[dateKey];
}

function renderDiaryView() {
  const dateKey = currentDiaryDate;
  const entry = getDiaryEntry(dateKey);
  const todayKey = getTodayKey();

  // 1. Date Header & Badges
  const label = document.getElementById('diaryCurrentDateLabel');
  if (label) {
    label.textContent = formatDateDisplay(dateKey);
  }

  const badge = document.getElementById('diaryDateBadge');
  if (badge) {
    if (dateKey === todayKey) {
      badge.textContent = 'Today';
      badge.className = 'diary-date-tag';
    } else if (dateKey < todayKey) {
      badge.textContent = 'Past Entry';
      badge.className = 'diary-date-tag past';
    } else {
      badge.textContent = 'Future Target';
      badge.className = 'diary-date-tag future';
    }
  }

  // Sync date picker value
  const datePicker = document.getElementById('diaryDateInput');
  if (datePicker && datePicker.value !== dateKey) {
    datePicker.value = dateKey;
  }

  // 2. Streak Badge
  const streakBadge = document.getElementById('diaryStreakBadge');
  if (streakBadge) {
    const curStreak = (typeof state !== 'undefined' && state.maxStreak) ? Math.max(1, state.maxStreak) : 1;
    streakBadge.textContent = `🔥 ${curStreak} d streak`;
  }

  // 3. Mood Selector
  const moodLabels = {
    great: 'Flow State 🤩',
    good: 'Productive 😊',
    neutral: 'Steady 😐',
    low: 'Fatigued 😔',
    stressed: 'Tired / Challenged 😫'
  };
  const curMood = entry.mood || 'good';
  const moodValLabel = document.getElementById('diaryMoodValLabel');
  if (moodValLabel) {
    moodValLabel.textContent = moodLabels[curMood] || curMood;
  }

  document.querySelectorAll('#diaryMoodSelector .diary-mood-pill').forEach(btn => {
    if (btn.dataset.mood === curMood) btn.classList.add('active');
    else btn.classList.remove('active');
  });

  // 4. Focus Rating
  const focusVal = entry.focusRating || 3;
  const focusValLabel = document.getElementById('diaryFocusValLabel');
  const focusDescriptions = ['1 / 5 (Scattered)', '2 / 5 (Distracted)', '3 / 5 (Steady)', '4 / 5 (Deep Focus)', '5 / 5 (Flow State)'];
  if (focusValLabel) {
    focusValLabel.textContent = focusDescriptions[focusVal - 1] || `${focusVal} / 5`;
  }
  document.querySelectorAll('#diaryFocusRating .diary-rating-cell').forEach(cell => {
    const val = Number(cell.dataset.val);
    if (val <= focusVal) cell.classList.add('active');
    else cell.classList.remove('active');
  });

  // 5. Energy Rating
  const energyVal = entry.energyRating || 3;
  const energyValLabel = document.getElementById('diaryEnergyValLabel');
  const energyDescriptions = ['1 / 5 (Exhausted)', '2 / 5 (Sluggish)', '3 / 5 (Moderate)', '4 / 5 (High Alert)', '5 / 5 (Peak Energy)'];
  if (energyValLabel) {
    energyValLabel.textContent = energyDescriptions[energyVal - 1] || `${energyVal} / 5`;
  }
  document.querySelectorAll('#diaryEnergyRating .diary-rating-cell').forEach(cell => {
    const val = Number(cell.dataset.val);
    if (val <= energyVal) cell.classList.add('energy-active');
    else cell.classList.remove('energy-active');
  });

  // 6. Text Inputs
  const elAcc = document.getElementById('diaryAccomplishments');
  const elMist = document.getElementById('diaryMistakes');
  const elDist = document.getElementById('diaryDistractions');
  const elFree = document.getElementById('diaryFreeform');
  const elP1 = document.getElementById('diaryPrio1');
  const elP2 = document.getElementById('diaryPrio2');
  const elP3 = document.getElementById('diaryPrio3');

  if (elAcc) elAcc.value = entry.accomplishments || '';
  if (elMist) elMist.value = entry.mistakes || '';
  if (elDist) elDist.value = entry.distractions || '';
  if (elFree) elFree.value = entry.freeform || '';
  if (elP1) elP1.value = (entry.priorities && entry.priorities[0]) || '';
  if (elP2) elP2.value = (entry.priorities && entry.priorities[1]) || '';
  if (elP3) elP3.value = (entry.priorities && entry.priorities[2]) || '';

  // 7. Priorities Checkboxes & Strikethrough
  const pDone = entry.priorityDone || [false, false, false];
  for (let i = 0; i < 3; i++) {
    const chk = document.getElementById(`diaryPrioDone${i + 1}`);
    const row = document.getElementById(`diaryPrioRow${i}`);
    if (chk) chk.checked = !!pDone[i];
    if (row) {
      if (pDone[i]) row.classList.add('completed');
      else row.classList.remove('completed');
    }
  }

  // 8. Update Word / Character Counters
  updateDiaryWordCounters();

  // 9. Render History & Insights
  renderDiaryHistoryList();
  renderDiaryInsights();
}

function updateDiaryWordCounters() {
  const countWords = (str) => {
    if (!str || !str.trim()) return 0;
    return str.trim().split(/\\s+/).length;
  };

  const accText = document.getElementById('diaryAccomplishments')?.value || '';
  const mistText = document.getElementById('diaryMistakes')?.value || '';
  const distText = document.getElementById('diaryDistractions')?.value || '';
  const freeText = document.getElementById('diaryFreeform')?.value || '';

  const elCAcc = document.getElementById('diaryCounterAcc');
  const elCMist = document.getElementById('diaryCounterMist');
  const elCDist = document.getElementById('diaryCounterDist');
  const elCFree = document.getElementById('diaryCounterFree');
  const elCPrio = document.getElementById('diaryCounterPrio');

  if (elCAcc) elCAcc.textContent = `${countWords(accText)} words • ${accText.length} chars`;
  if (elCMist) elCMist.textContent = `${countWords(mistText)} words • ${mistText.length} chars`;
  if (elCDist) elCDist.textContent = `${countWords(distText)} words`;
  if (elCFree) elCFree.textContent = `${countWords(freeText)} words • ${freeText.length} chars`;

  // Priority count
  const entry = getDiaryEntry(currentDiaryDate);
  const pDone = entry.priorityDone || [false, false, false];
  const doneCount = pDone.filter(Boolean).length;
  if (elCPrio) elCPrio.textContent = `${doneCount} / 3 done`;
}

function onDiaryInputChanged() {
  updateDiaryWordCounters();
  queueDiaryAutosave();
}

function setDiaryMood(mood) {
  const entry = getDiaryEntry(currentDiaryDate);
  entry.mood = mood;
  entry.updatedAt = Date.now();
  saveDiaryFromInputs();
  renderDiaryView();
  showDiarySaved();
}

function setDiaryRating(type, val) {
  const entry = getDiaryEntry(currentDiaryDate);
  if (type === 'focus') entry.focusRating = val;
  if (type === 'energy') entry.energyRating = val;
  entry.updatedAt = Date.now();
  saveDiaryFromInputs();
  renderDiaryView();
  showDiarySaved();
}

function toggleDiaryPriorityDone(idx, checked) {
  const entry = getDiaryEntry(currentDiaryDate);
  if (!Array.isArray(entry.priorityDone)) {
    entry.priorityDone = [false, false, false];
  }
  entry.priorityDone[idx] = checked;
  entry.updatedAt = Date.now();
  saveDiaryState();

  const row = document.getElementById(`diaryPrioRow${idx}`);
  if (row) {
    if (checked) row.classList.add('completed');
    else row.classList.remove('completed');
  }

  updateDiaryWordCounters();
  showDiarySaved();
}

function changeDiaryDate(deltaDays) {
  // Flush current inputs before moving dates
  saveDiaryFromInputs();

  const [y, m, d] = currentDiaryDate.split('-').map(Number);
  const dt = new Date(y, m - 1, d);
  dt.setDate(dt.getDate() + deltaDays);

  const newYear = dt.getFullYear();
  const newMonth = String(dt.getMonth() + 1).padStart(2, '0');
  const newDay = String(dt.getDate()).padStart(2, '0');

  currentDiaryDate = `${newYear}-${newMonth}-${newDay}`;
  renderDiaryView();
}

function jumpToDiaryToday() {
  saveDiaryFromInputs();
  currentDiaryDate = getTodayKey();
  renderDiaryView();
}

function onDiaryDatePickerChange(val) {
  if (!val) return;
  saveDiaryFromInputs();
  currentDiaryDate = val;
  renderDiaryView();
}

function queueDiaryAutosave() {
  const indicator = document.getElementById('diarySavedIndicator');
  if (indicator) {
    indicator.textContent = 'Saving...';
    indicator.className = 'diary-save-badge saving';
  }

  clearTimeout(diaryAutosaveTimeout);
  diaryAutosaveTimeout = setTimeout(() => {
    saveDiaryFromInputs();
  }, 450);
}

function saveDiaryFromInputs() {
  const entry = getDiaryEntry(currentDiaryDate);
  const elAcc = document.getElementById('diaryAccomplishments');
  const elMist = document.getElementById('diaryMistakes');
  const elDist = document.getElementById('diaryDistractions');
  const elFree = document.getElementById('diaryFreeform');
  const elP1 = document.getElementById('diaryPrio1');
  const elP2 = document.getElementById('diaryPrio2');
  const elP3 = document.getElementById('diaryPrio3');

  if (elAcc) entry.accomplishments = elAcc.value;
  if (elMist) entry.mistakes = elMist.value;
  if (elDist) entry.distractions = elDist.value;
  if (elFree) entry.freeform = elFree.value;
  entry.priorities = [
    elP1 ? elP1.value : '',
    elP2 ? elP2.value : '',
    elP3 ? elP3.value : ''
  ];
  entry.updatedAt = Date.now();

  saveDiaryState();
  showDiarySaved();
  renderDiaryHistoryList();
  renderDiaryInsights();
}

function showDiarySaved() {
  const indicator = document.getElementById('diarySavedIndicator');
  if (indicator) {
    const now = new Date();
    const timeStr = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    indicator.textContent = `Saved at ${timeStr} ✓`;
    indicator.className = 'diary-save-badge';
  }
}

function confirmDeleteDiaryEntry() {
  const dateStr = formatDateDisplay(currentDiaryDate);
  if (confirm(`Are you sure you want to permanently delete the debrief entry for ${dateStr} (${currentDiaryDate})? This cannot be undone.`)) {
    delete diaryState.entries[currentDiaryDate];
    saveDiaryState();
    if (typeof showToast === 'function') {
      showToast(`Deleted journal entry for ${dateStr}`);
    }
    currentDiaryDate = getTodayKey();
    renderDiaryView();
  }
}

function renderDiaryHistoryList() {
  const list = document.getElementById('diaryHistoryList');
  if (!list) return;

  const q = (document.getElementById('diarySearchInput')?.value || '').toLowerCase().trim();
  const keys = Object.keys(diaryState.entries).sort().reverse();

  const countBadge = document.getElementById('diaryHistoryCountBadge');
  if (countBadge) {
    countBadge.textContent = `${keys.length} entries`;
  }

  let html = '';
  let matchCount = 0;

  keys.forEach(k => {
    const e = diaryState.entries[k];
    const fullText = (
      (e.accomplishments || '') + ' ' +
      (e.mistakes || '') + ' ' +
      (e.distractions || '') + ' ' +
      (e.freeform || '') + ' ' +
      (e.priorities ? e.priorities.join(' ') : '') + ' ' +
      k
    ).toLowerCase();

    if (q && !fullText.includes(q)) return;
    matchCount++;

    const moodEmoji = { great: '🤩', good: '😊', neutral: '😐', low: '😔', stressed: '😫' }[e.mood] || '📝';
    const focusVal = e.focusRating || 3;
    const isActive = (k === currentDiaryDate);
    const snippet = (e.accomplishments || e.freeform || e.mistakes || 'No notes written yet.').replace(/\\n+/g, ' ');

    html += `
      <div class="diary-history-item ${isActive ? 'active' : ''}" onclick="selectDiaryDate('${k}')">
        <div class="diary-history-item-top">
          <span class="diary-history-item-date">
            <span>${moodEmoji}</span>
            <span>${formatDateDisplay(k)}</span>
          </span>
          <div class="diary-history-badges">
            <span class="diary-history-mini-pill">Focus ${focusVal}/5</span>
            ${k === getTodayKey() ? '<span class="diary-date-tag" style="font-size:8.5px; padding:1px 5px;">Today</span>' : ''}
          </div>
        </div>
        <div class="diary-history-item-preview">${snippet}</div>
      </div>
    `;
  });

  if (keys.length === 0) {
    html = `
      <div style="font-size:12px; color:#64748b; text-align:center; padding:2rem 1rem;">
        <span style="font-size:1.6rem; display:block; margin-bottom:0.4rem;">📓</span>
        No journal entries recorded yet.<br>Start by writing today's debrief above!
      </div>
    `;
  } else if (matchCount === 0 && q) {
    html = `
      <div style="font-size:12px; color:#64748b; text-align:center; padding:1.5rem 1rem;">
        No entries match "<strong style="color:#cbd5e1;">${q}</strong>".<br>
        <button type="button" class="diary-today-btn" style="margin-top:0.6rem;" onclick="document.getElementById('diarySearchInput').value=''; renderDiaryHistoryList();">Clear Search</button>
      </div>
    `;
  }

  list.innerHTML = html;
}

function selectDiaryDate(k) {
  saveDiaryFromInputs();
  currentDiaryDate = k;
  renderDiaryView();
}

function renderDiaryInsights() {
  const keys = Object.keys(diaryState.entries);
  const totalEntries = keys.length;

  const elTotal = document.getElementById('diaryStatTotalEntries');
  const elAvgFocus = document.getElementById('diaryStatAvgFocus');
  const elAvgEnergy = document.getElementById('diaryStatAvgEnergy');
  const elMood = document.getElementById('diaryStatCommonMood');
  const elTip = document.getElementById('diaryInsightTipText');

  if (!elTotal) return;

  elTotal.textContent = totalEntries;

  if (totalEntries === 0) {
    if (elAvgFocus) elAvgFocus.textContent = '0.0';
    if (elAvgEnergy) elAvgEnergy.textContent = '0.0';
    if (elMood) elMood.textContent = '—';
    return;
  }

  let sumFocus = 0;
  let sumEnergy = 0;
  const moodCounts = {};

  keys.forEach(k => {
    const e = diaryState.entries[k];
    sumFocus += (Number(e.focusRating) || 3);
    sumEnergy += (Number(e.energyRating) || 3);
    const m = e.mood || 'good';
    moodCounts[m] = (moodCounts[m] || 0) + 1;
  });

  const avgFocus = (sumFocus / totalEntries).toFixed(1);
  const avgEnergy = (sumEnergy / totalEntries).toFixed(1);

  if (elAvgFocus) elAvgFocus.textContent = avgFocus;
  if (elAvgEnergy) elAvgEnergy.textContent = avgEnergy;

  // Most frequent mood
  let topMood = 'good';
  let topCount = 0;
  for (const [m, count] of Object.entries(moodCounts)) {
    if (count > topCount) {
      topCount = count;
      topMood = m;
    }
  }

  const moodDisplayMap = {
    great: '🤩 Flow',
    good: '😊 Good',
    neutral: '😐 Steady',
    low: '😔 Low',
    stressed: '😫 Tired'
  };

  if (elMood) elMood.textContent = moodDisplayMap[topMood] || topMood;

  // Contextual tip based on data
  if (elTip) {
    if (Number(avgFocus) >= 4.0) {
      elTip.textContent = 'Exceptional focus! Your consistency in deep problem-solving is driving compounding placement momentum.';
    } else if (Number(avgEnergy) <= 2.5) {
      elTip.textContent = 'Energy levels have dipped recently. Prioritize 7+ hours of quality sleep and structured study breaks to maintain cognitive sharpness.';
    } else if (totalEntries >= 7) {
      elTip.textContent = `Great streak with ${totalEntries} debriefs logged! Reviewing past mistakes weekly cements tricky edge cases into permanent intuition.`;
    } else {
      elTip.textContent = 'Consistent reflection turns random mistakes into algorithmic mastery. Every daily entry compounds into placement readiness.';
    }
  }
}

function exportDiary(format) {
  if (format === 'md') {
    let md = '# 📓 Placement Preparation Engineering Journal\\n\\n';
    md += `*Exported on ${formatDateDisplay(getTodayKey())} • Total entries: ${Object.keys(diaryState.entries).length}*\\n\\n---\\n\\n`;

    const keys = Object.keys(diaryState.entries).sort();
    keys.forEach(k => {
      const e = diaryState.entries[k];
      const moodEmoji = { great: '🤩', good: '😊', neutral: '😐', low: '😔', stressed: '😫' }[e.mood] || '📝';
      const focus = e.focusRating || 3;
      const energy = e.energyRating || 3;

      md += `## 📅 Entry: ${formatDateDisplay(k)} (${k})\\n\\n`;
      md += `**State:** ${moodEmoji} ${e.mood || 'good'} | **Focus:** ${focus}/5 | **Energy:** ${energy}/5\\n\\n`;

      if (e.accomplishments && e.accomplishments.trim()) {
        md += `### 🏆 Accomplishments & Topics Studied\\n${e.accomplishments.trim()}\\n\\n`;
      }
      if (e.mistakes && e.mistakes.trim()) {
        md += `### ⚠️ Mistakes, Edge Cases & Lessons Learned\\n${e.mistakes.trim()}\\n\\n`;
      }
      if (e.distractions && e.distractions.trim()) {
        md += `### 🛑 Distractions Faced\\n${e.distractions.trim()}\\n\\n`;
      }
      if (e.freeform && e.freeform.trim()) {
        md += `### 📝 Free-Form Reflection & Notes\\n${e.freeform.trim()}\\n\\n`;
      }
      if (e.priorities && e.priorities.some(Boolean)) {
        md += `### 🚀 Tomorrow\\'s Priorities\\n`;
        const pDone = e.priorityDone || [false, false, false];
        e.priorities.forEach((p, idx) => {
          if (p && p.trim()) {
            const checkMark = pDone[idx] ? '[x]' : '[ ]';
            md += `- ${checkMark} **P${idx + 1}:** ${p.trim()}\\n`;
          }
        });
        md += '\\n';
      }
      md += '---\\n\\n';
    });

    if (typeof downloadFile === 'function') {
      downloadFile(md, `placement_journal_${getTodayKey()}.md`, 'text/markdown');
    }
  }
}

// Keyboard shortcuts for diary (Cmd+S / Ctrl+S to save)
document.addEventListener('keydown', function(e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 's') {
    const isDiaryActive = document.getElementById('view-diary')?.classList.contains('active');
    if (isDiaryActive) {
      e.preventDefault();
      saveDiaryFromInputs();
      if (typeof showToast === 'function') {
        showToast('Journal entry saved ✓');
      }
    }
  }
});
"""

# ---------------------------------------------------------------------------
# 4. PERFORM CLEAN REPLACEMENTS
# ---------------------------------------------------------------------------
# Replace Section HTML
sec_start = html.find('<section class="view-section" id="view-diary">')
sec_end = html.find("</section>", sec_start) + len("</section>")
if sec_start == -1 or sec_end == -1:
    print("ERROR: could not locate section view-diary")
    exit(1)

html = html[:sec_start] + new_diary_html + html[sec_end:]
print("1. Replaced section view-diary HTML.")

# Replace CSS
pos1 = html.find("VIEW 5: PRIVATE DIARY")
pos2 = html.find("VIEW 6: DAILY MOTIVATION")
if pos1 == -1 or pos2 == -1:
    print("ERROR: could not locate diary CSS")
    exit(1)

css_start = html.rfind("/*", 0, pos1)
css_end = html.rfind("/*", 0, pos2)

html = html[:css_start] + new_diary_css + "\n\n" + html[css_end:]
print("2. Replaced diary CSS.")

# Replace JS
pos3 = html.find("PRIVATE DIARY ENGINE")
pos4 = html.find("DSA PATTERNS RENDERING")
if pos3 == -1 or pos4 == -1:
    print("ERROR: could not locate diary JS")
    exit(1)

js_start = html.rfind("/*", 0, pos3)
js_end = html.rfind("/*", 0, pos4)

html = html[:js_start] + new_diary_js + "\n\n" + html[js_end:]
print("3. Replaced diary JS.")

# Save to test_diary_assembled.html
with open("test_diary_assembled.html", "w") as f:
    f.write(html)

print("SUCCESS: Assembled test_diary_assembled.html cleanly!")
