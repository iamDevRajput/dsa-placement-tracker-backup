import re
import os

INDEX_PATH = "/Users/devrajput/@Resources/Tracker/dsa-placement-dashboard/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

start_marker = '/* ==========================================================================\n   MIK INTERVIEW DSA STATE & ENGINE'
end_marker = 'function switchView(viewName, navEl) {'

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Error: Could not locate markers in index.html")
    exit(1)

js_content = """/* ==========================================================================
   MIK INTERVIEW DSA STATE & ENGINE (4-MODE PEDAGOGICAL WORKSPACE)
   ========================================================================== */
const STORAGE_MIK_KEY = 'mik_interview_dsa_tracker_v1';

let mikState = {
  version: 1,
  problems: {},
  collapsedTopics: {},
  collapsedSubtopics: {},
  currentMode: 'playlist',
  activePlaylistId: 'PLpIkg8OmuX-LkgtrEF7eyyYWJM3m5tVQY',
  activeStageId: 'stage_1',
  activePatternCategory: 'all'
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
          activePatternCategory: parsed.activePatternCategory || 'all'
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
    activePatternCategory: 'all'
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
// MODE MANAGEMENT (4 Complementary Views)
// --------------------------------------------------------------------------
function setMikMode(mode) {
  mikState.currentMode = mode;
  saveMikState();

  document.querySelectorAll('.mik-mode-tab').forEach(tab => {
    tab.classList.toggle('active', tab.id === `mikModeTab-${mode}`);
  });

  populateMikNav();
  renderMikContent();
}

function setMikActivePlaylist(playlistId) {
  mikState.activePlaylistId = playlistId;
  saveMikState();
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
// FILTER CONTROLS
// --------------------------------------------------------------------------
function handleMikSearchInput(val) {
  mikFilter.search = (val || '').trim().toLowerCase();
  const clearBtn = document.getElementById('mikSearchClearBtn');
  if (clearBtn) clearBtn.style.display = mikFilter.search ? 'block' : 'none';
  renderMikContent();
}

function clearMikSearch() {
  const input = document.getElementById('mikSearchInput');
  if (input) input.value = '';
  handleMikSearchInput('');
}

function setMikTopic(topic) {
  mikFilter.topic = topic;
  const select = document.getElementById('mikTopicDropdown');
  if (select && select.value !== topic) select.value = topic;
  populateMikNav();
  renderMikContent();
}

function setMikCompany(company) {
  mikFilter.company = company;
  renderMikContent();
}

function setMikSort(sortOrder) {
  mikFilter.sort = sortOrder;
  renderMikContent();
}

function setMikStatusFilter(status, btn) {
  mikFilter.status = status;
  document.querySelectorAll('.mik-pill').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderMikContent();
}

function resetAllMikFilters() {
  mikFilter = { topic: 'all', company: 'all', status: 'all', search: '', sort: 'default' };
  const searchInput = document.getElementById('mikSearchInput');
  if (searchInput) searchInput.value = '';
  const clearBtn = document.getElementById('mikSearchClearBtn');
  if (clearBtn) clearBtn.style.display = 'none';

  const topicDropdown = document.getElementById('mikTopicDropdown');
  if (topicDropdown) topicDropdown.value = 'all';

  const companyDropdown = document.getElementById('mikCompanyDropdown');
  if (companyDropdown) companyDropdown.value = 'all';

  const sortDropdown = document.getElementById('mikSortDropdown');
  if (sortDropdown) sortDropdown.value = 'default';

  document.querySelectorAll('.mik-pill').forEach(b => b.classList.remove('active'));
  const allPill = document.getElementById('f-mik-all');
  if (allPill) allPill.classList.add('active');

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
    // collapse all visible groups
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
        label.textContent = `🎬 Video ${contextVideoIndex + 1} of ${activePl.videos.length} · ${activePl.title}`;
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

  // Topic filter
  if (mikFilter.topic !== 'all' && p.topic !== mikFilter.topic) return false;

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

  // Filter videos
  const filteredVideos = activePl.videos.filter(v => {
    if (!v.problem_id) return (mikFilter.status === 'all' && !mikFilter.search);
    const p = catMap[v.problem_id];
    if (!p) return false;
    return matchesMikFilter(p);
  });

  let videosHtml = '';
  filteredVideos.forEach((v, idx) => {
    if (v.problem_id && catMap[v.problem_id]) {
      const p = catMap[v.problem_id];
      videosHtml += renderMikProblemRow(p, `#${v.seq}`, v.seq - 1);
    } else {
      // Unmatched or standalone video row
      videosHtml += `
        <div class="mik-prob-row">
          <div class="mik-prob-seq playlist-seq">#${v.seq}</div>
          <div class="mik-prob-title-group">
            <span class="mik-prob-title-link" style="color:var(--text-dim);">
              🎬 ${v.video_title}
            </span>
            <div class="mik-prob-tags">
              <span class="mik-tag" style="color:#fbbf24;">Playlist Video (Independent)</span>
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
            <div style="padding:0.5rem 0; font-size:12px; border-bottom:1px solid rgba(255,255,255,0.05); display:flex; justify-content:space-between; align-items:center;">
              <div>
                <span style="font-weight:700; color:#fbbf24; margin-right:0.5rem;">#${uv.seq}</span>
                <span style="color:var(--text);">${uv.video_title}</span>
                <div style="font-size:11px; color:var(--text-muted); margin-top:2px;">${uv.reason}</div>
              </div>
              <a href="${uv.video_url}" target="_blank" rel="noopener noreferrer" class="btn btn-secondary" style="font-size:11px; padding:0.25rem 0.6rem;">Watch on YouTube</a>
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
          <span class="mik-tag" style="background:rgba(239,68,68,0.15); color:#fca5a5; border-color:rgba(239,68,68,0.3);">
            codestorywithMIK Verified
          </span>
        </div>
        <div class="mik-playlist-banner-desc">${activePl.description || ''}</div>
        <div style="font-size:12px; color:var(--text-dim); display:flex; gap:1rem; align-items:center;">
          <span>Progress: <strong style="color:#ffffff;">${plSolved} / ${plMatched}</strong> (${plPct}%)</span>
          <span>Total Playlist Videos: <strong style="color:#ffffff;">${activePl.total_videos}</strong></span>
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
          <span>📋 Verified Sequence Order (${filteredVideos.length} Items)</span>
        </div>
      </div>
      <div class="mik-prob-list">
        ${videosHtml || '<div style="padding:1.5rem; text-align:center; color:var(--text-dim); font-size:13px;">No problems match current filters.</div>'}
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
    let stageSolved = 0;
    let stageTotal = 0;

    // Calculate stage stats
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
      // Topic filter check
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
                <span style="font-size:12px; color:var(--text-dim);">${isSubCollapsed ? '▶' : '▼'}</span>
                <span>${sub.subtopic}</span>
              </div>
              <div style="font-size:11.5px; color:var(--text-dim); display:flex; gap:0.5rem; align-items:center;">
                <span class="mik-topic-nav-badge">${subSolved}/${sub.problem_count}</span>
              </div>
            </div>
            ${!isSubCollapsed ? `
              <div class="mik-prob-list">
                ${matchedProbs.map((p, idx) => renderMikProblemRow(p, idx + 1)).join('') || '<div style="padding:1rem; font-size:12px; color:var(--text-muted); text-align:center;">No matching problems in this subtopic.</div>'}
              </div>
            ` : ''}
          </div>
        `;
      });

      if (subtopicsHtml) {
        topicsHtml += `
          <div style="margin-bottom:1rem;">
            <div style="font-size:13px; font-weight:700; color:var(--text); margin-bottom:0.4rem; display:flex; justify-content:space-between;">
              <span>📂 ${t.topic}</span>
              <span style="font-size:11px; color:var(--text-dim);">${t.problem_count} problems</span>
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
            <span style="font-size:13px; color:var(--text-dim);">${isCollapsed ? '▶' : '▼'}</span>
            <div>
              <div class="mik-stage-title">${st.stage_title}</div>
              <div class="mik-stage-desc">${st.stage_description}</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:0.85rem;">
            <div style="text-align:right;">
              <div style="font-size:12px; font-weight:700; color:#ffffff;">${stageSolved} / ${stageTotal}</div>
              <div style="font-size:10.5px; color:var(--text-dim);">${stagePct}% Done</div>
            </div>
          </div>
        </div>
        ${!isCollapsed ? `
          <div class="mik-stage-body">
            ${topicsHtml || '<div style="text-align:center; padding:1.5rem; color:var(--text-dim);">No problems match active filters in this stage.</div>'}
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
                <span style="font-size:12px; color:var(--text-dim);">${isCollapsed ? '▶' : '▼'}</span>
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
              ${matchedProbs.map((p, idx) => renderMikProblemRow(p, idx + 1)).join('') || '<div style="padding:1rem; font-size:12px; color:var(--text-muted); text-align:center;">No matching problems in this pattern.</div>'}
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
              <span style="font-size:12px; color:var(--text-dim);">${isSubCollapsed ? '▶' : '▼'}</span>
              <span>📁 ${subName}</span>
            </div>
            <div style="font-size:11.5px; color:var(--text-dim); display:flex; gap:0.5rem; align-items:center;">
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
            <span style="font-size:13px; color:var(--text-dim);">${isTopicCollapsed ? '▶' : '▼'}</span>
            <div>
              <div class="mik-stage-title">📂 ${topic}</div>
              <div class="mik-stage-desc">Original source folder from MAZHARMIK / Interview_DS_Algo</div>
            </div>
          </div>
          <div style="display:flex; align-items:center; gap:0.75rem;">
            <div style="text-align:right;">
              <div style="font-size:12px; font-weight:700; color:#ffffff;">${topicSolved} / ${topicTotal}</div>
              <div style="font-size:10.5px; color:var(--text-dim);">${topicTotal > 0 ? Math.round((topicSolved / topicTotal) * 100) : 0}% Done</div>
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
  } else {
    renderMikRepoView();
  }
}

// --------------------------------------------------------------------------
// SIDEBAR POPULATION (Context-Aware)
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
    html += `<div class="mik-sidebar-heading">Learning Roadmap (5 Stages)</div>`;
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
    // Original Repo Mode: 23 Topics
    const cat = getMikCatalog();
    const topicsMap = {};
    cat.forEach(p => {
      if (!topicsMap[p.topic]) topicsMap[p.topic] = { total: 0, solved: 0 };
      topicsMap[p.topic].total++;
      if (mikState.problems[p.id]?.done) topicsMap[p.topic].solved++;
    });

    html += `<div class="mik-sidebar-heading">Original Topics (23)</div>`;
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

  // Also populate topic filter dropdown if not already populated
  const select = document.getElementById('mikTopicDropdown');
  if (select && select.options.length <= 1) {
    const cat = getMikCatalog();
    const topics = Array.from(new Set(cat.map(p => p.topic))).sort();
    topics.forEach(t => {
      const opt = document.createElement('option');
      opt.value = t;
      opt.textContent = `📂 ${t}`;
      select.appendChild(opt);
    });
  }
}

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  loadMikState();
  updateMikStats();
});
"""

html = html[:start_idx] + js_content + "\n\n" + html[end_idx:]

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully replaced MIK JS engine with 4-mode pedagogical engine!")
