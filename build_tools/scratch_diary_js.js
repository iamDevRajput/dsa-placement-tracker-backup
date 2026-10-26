/* ==========================================================================
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
    return str.trim().split(/\s+/).length;
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
    const snippet = (e.accomplishments || e.freeform || e.mistakes || 'No notes written yet.').replace(/\n+/g, ' ');

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
    let md = '# 📓 Placement Preparation Engineering Journal\n\n';
    md += `*Exported on ${formatDateDisplay(getTodayKey())} • Total entries: ${Object.keys(diaryState.entries).length}*\n\n---\n\n`;

    const keys = Object.keys(diaryState.entries).sort();
    keys.forEach(k => {
      const e = diaryState.entries[k];
      const moodEmoji = { great: '🤩', good: '😊', neutral: '😐', low: '😔', stressed: '😫' }[e.mood] || '📝';
      const focus = e.focusRating || 3;
      const energy = e.energyRating || 3;

      md += `## 📅 Entry: ${formatDateDisplay(k)} (${k})\n\n`;
      md += `**State:** ${moodEmoji} ${e.mood || 'good'} | **Focus:** ${focus}/5 | **Energy:** ${energy}/5\n\n`;

      if (e.accomplishments && e.accomplishments.trim()) {
        md += `### 🏆 Accomplishments & Topics Studied\n${e.accomplishments.trim()}\n\n`;
      }
      if (e.mistakes && e.mistakes.trim()) {
        md += `### ⚠️ Mistakes, Edge Cases & Lessons Learned\n${e.mistakes.trim()}\n\n`;
      }
      if (e.distractions && e.distractions.trim()) {
        md += `### 🛑 Distractions Faced\n${e.distractions.trim()}\n\n`;
      }
      if (e.freeform && e.freeform.trim()) {
        md += `### 📝 Free-Form Reflection & Notes\n${e.freeform.trim()}\n\n`;
      }
      if (e.priorities && e.priorities.some(Boolean)) {
        md += `### 🚀 Tomorrow\'s Priorities\n`;
        const pDone = e.priorityDone || [false, false, false];
        e.priorities.forEach((p, idx) => {
          if (p && p.trim()) {
            const checkMark = pDone[idx] ? '[x]' : '[ ]';
            md += `- ${checkMark} **P${idx + 1}:** ${p.trim()}\n`;
          }
        });
        md += '\n';
      }
      md += '---\n\n';
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