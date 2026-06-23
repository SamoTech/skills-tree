'use strict';

// ─── PATH NORMALIZER ────────────────────────────────────────────────
function getGraphUrl() {
  const host = window.location.hostname;
  if (host === 'localhost' || host === '127.0.0.1') {
    return '../../data/SKILLS_GRAPH.json';
  }
  return '/skills-tree/data/SKILLS_GRAPH.json';
}
const GRAPH_URL = getGraphUrl();
console.info('GRAPH URL:', GRAPH_URL);

// ─── CATEGORY LABEL MAP ───────────────────────────────────────────
// INITIATIVE-012C Phase 2: human-readable labels, sandbox hidden
const CAT_LABELS = {
  '01-perception':          'Perception',
  '02-reasoning':           'Reasoning',
  '03-memory':              'Memory',
  '04-action-execution':    'Action',
  '04-action':              'Action',
  '05-code':                'Code',
  '06-communication':       'Communication',
  '07-tool-use':            'Tool Use',
  '08-multimodal':          'Multimodal',
  '09-agentic-patterns':    'Agentic Patterns',
  '10-computer-use':        'Content Understanding',
  '10-content-understanding':'Content Understanding',
  '11-web':                 'Web',
  '12-data':                'Data',
  '13-safety':              'Creative',
  '13-creative':            'Creative',
  '14-security':            'Security',
  '15-orchestration':       'Orchestration',
  '16-domain-specific':     'Domain Specific',
  '17-infrastructure':      'Infrastructure',
};

function catLabel(slug) {
  return CAT_LABELS[slug] || slug.replace(/^\d+-/, '').replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

const GITHUB_BASE = 'https://github.com/SamoTech/skills-tree/blob/main/';

let graph = null;
let nodes = [], edges = [], filteredNodes = [], selectedId = null;
let activeFilters = { level: 'all', stability: 'all', category: 'all' }, searchQuery = '';
let edgesBySource = {}, edgesByTarget = {}, nodeById = {};
// INITIATIVE-012C Phase 3: full dependency index
let prereqBy = {};    // id → [ ids that list this as prerequisite ]
let requiredByIdx = {}; // id → [ ids that REQUIRE this via edge ]
let relatedIdx = {};  // id → [ ids that list this in related_skills ]

// ─── THEME ────────────────────────────────────────────────────────
(function initTheme() {
  const btn  = document.querySelector('[data-theme-toggle]');
  const html = document.documentElement;
  let theme  = html.getAttribute('data-theme') || 'dark';
  updateThemeIcon(btn, theme);
  if (btn) {
    btn.addEventListener('click', () => {
      theme = theme === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', theme);
      updateThemeIcon(btn, theme);
    });
  }
})();

function updateThemeIcon(btn, theme) {
  if (!btn) return;
  btn.setAttribute('aria-label', 'Switch to ' + (theme === 'dark' ? 'light' : 'dark') + ' mode');
  btn.innerHTML = theme === 'dark'
    ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
    : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
}

document.addEventListener('DOMContentLoaded', () => {
  loadGraph();
  setupSearch();
  setupFilters();
  setupURLRouting();
  setupKeyboardShortcut();
  setupMobileOverlayClose();
});

// ─── RESILIENT GRAPH LOADER ────────────────────────────────────────────
async function loadGraph() {
  const url = GRAPH_URL;
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}: ${url}`);
    const data = await response.json();
    if (!data || !Array.isArray(data.nodes)) throw new Error('Invalid graph schema — missing nodes array');

    graph = data;
    nodes = graph.nodes || [];
    edges = graph.edges || [];

    nodeById = {};
    edgesBySource = {};
    edgesByTarget = {};
    prereqBy = {};
    requiredByIdx = {};
    relatedIdx = {};

    // primary indexes
    for (const n of nodes) { nodeById[n.id] = n; }
    for (const e of edges) {
      if (!edgesBySource[e.source]) edgesBySource[e.source] = [];
      edgesBySource[e.source].push(e);
      if (!edgesByTarget[e.target]) edgesByTarget[e.target] = [];
      edgesByTarget[e.target].push(e);
    }

    // INITIATIVE-012C Phase 3: build reverse dependency index
    for (const n of nodes) {
      // prereqBy: reverse of prerequisites array
      for (const pid of (n.prerequisites || [])) {
        if (!prereqBy[pid]) prereqBy[pid] = [];
        prereqBy[pid].push(n.id);
      }
      // relatedIdx: bidirectional related_skills
      for (const rid of (n.related_skills || [])) {
        if (!relatedIdx[rid]) relatedIdx[rid] = [];
        if (!relatedIdx[rid].includes(n.id)) relatedIdx[rid].push(n.id);
        if (!relatedIdx[n.id]) relatedIdx[n.id] = [];
        if (!relatedIdx[n.id].includes(rid)) relatedIdx[n.id].push(rid);
      }
      // requiredByIdx: reverse of REQUIRES edges
      for (const e of (edgesByTarget[n.id] || [])) {
        if (e.type === 'REQUIRES') {
          if (!requiredByIdx[n.id]) requiredByIdx[n.id] = [];
          requiredByIdx[n.id].push(e.source);
        }
      }
    }

    console.info('NODES:', nodes.length);
    console.info('EDGES:', edges.length);

    updateHero();
    updateHealthPanel();
    buildCategoryFilters();
    applyFilters();
    handleURLParam();

  } catch (error) {
    console.error('Graph load failed:', error);
    showGraphError(error);
    throw error;
  }
}

// ─── HERO METRICS ───────────────────────────────────────────────
function updateHero() {
  const meta   = graph.meta || {};
  const visible = nodes.filter(n => n.category !== '00-sandbox');
  const cats   = new Set(visible.map(n => n.category));
  const reqEdges = edges.filter(e => e.type === 'REQUIRES');
  animateNumber('hero-nodes',    visible.length);
  animateNumber('hero-edges',    meta.edge_count || edges.length);
  animateNumber('hero-cats',     cats.size);
  animateNumber('hero-requires', meta.requires_count || reqEdges.length);
}

// ─── GRAPH HEALTH PANEL (Phase 6) ──────────────────────────────
function updateHealthPanel() {
  const visible = nodes.filter(n => n.category !== '00-sandbox');
  let withDeps = 0, isolated = 0;
  const connCount = {};
  for (const n of visible) {
    const deps = [
      ...(n.prerequisites || []),
      ...(n.related_skills || []),
      ...(edgesBySource[n.id] || []).map(e => e.target),
      ...(edgesByTarget[n.id] || []).map(e => e.source),
    ];
    const uniq = new Set(deps);
    connCount[n.id] = uniq.size;
    if (uniq.size > 0) withDeps++;
    else isolated++;
  }
  const covPct = visible.length ? Math.round(withDeps / visible.length * 100) : 0;
  const avgConn = visible.length
    ? (Object.values(connCount).reduce((a, b) => a + b, 0) / visible.length).toFixed(1)
    : '0';

  // top connected skill
  const topId = Object.entries(connCount).sort((a, b) => b[1] - a[1])[0];
  const topNode = topId ? nodeById[topId[0]] : null;

  document.getElementById('h-coverage').textContent  = covPct + '%';
  document.getElementById('h-isolated').textContent  = isolated;
  document.getElementById('h-density').textContent   = avgConn;
  document.getElementById('h-top').textContent       = topNode ? topNode.title : '—';
  if (topNode) {
    const el = document.getElementById('h-top');
    el.style.cursor = 'pointer';
    el.title = 'Click to view: ' + topNode.id;
    el.addEventListener('click', () => selectSkill(topNode.id), { once: true });
  }
}

// ─── DIAGNOSTIC ERROR PANEL ───────────────────────────────────────
function showGraphError(err) {
  const url    = GRAPH_URL;
  const match  = err && err.message ? err.message.match(/HTTP (\d+)/) : null;
  const status = match ? match[1] : (err ? escHtml(err.message) : 'Unknown error');
  const isHttp = !!match;
  document.getElementById('skill-grid').innerHTML = `
<div class="empty-state" role="alert" aria-live="assertive">
  <p class="empty-state-title">Failed to load graph</p>
  <p><strong>Attempted URL:</strong><br><code>${escHtml(url)}</code></p>
  <p><strong>Reason:</strong> ${isHttp ? 'HTTP ' + status : escHtml(status)}</p>
  <hr style="margin:0.75rem 0;border-color:var(--color-divider)">
  <p style="text-align:left;max-width:100%">
    <strong>Checklist:</strong><br>
    ✓ Start local server: <code>python3 -m http.server 8000</code> from repo root<br>
    ✓ Open: <code>http://localhost:8000/docs/explorer/</code><br>
    ✓ Verify <code>data/SKILLS_GRAPH.json</code> exists<br>
    ✓ Verify fetch path matches environment
  </p>
</div>`;
  document.getElementById('results-count').textContent = 'Error';
}

function animateNumber(id, target) {
  const el = document.getElementById(id);
  if (!el) return;
  let current = 0;
  const step  = Math.ceil(target / 40);
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    el.textContent = current.toLocaleString();
    if (current >= target) clearInterval(timer);
  }, 16);
}

// ─── CATEGORY FILTER CHIPS ────────────────────────────────────────
// INITIATIVE-012C Phase 2: human labels, sandbox hidden
function buildCategoryFilters() {
  const container = document.getElementById('filter-category');
  // only categories that are NOT sandbox
  const cats = [...new Set(
    nodes.filter(n => n.category !== '00-sandbox').map(n => n.category)
  )].sort();

  const allChip = document.createElement('button');
  allChip.className = 'chip chip-active';
  allChip.dataset.filter = 'category';
  allChip.dataset.value  = 'all';
  allChip.setAttribute('aria-pressed', 'true');
  allChip.textContent = 'All';
  container.appendChild(allChip);

  for (const cat of cats) {
    const btn = document.createElement('button');
    btn.className = 'chip';
    btn.dataset.filter = 'category';
    btn.dataset.value  = cat;
    btn.setAttribute('aria-pressed', 'false');
    btn.textContent = catLabel(cat); // human label
    container.appendChild(btn);
  }
}

function setupSearch() {
  const input = document.getElementById('skill-search');
  input.addEventListener('input', (e) => {
    searchQuery = e.target.value.trim().toLowerCase();
    applyFilters();
  });
}

function setupKeyboardShortcut() {
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
      e.preventDefault();
      document.getElementById('skill-search').focus();
    }
    if (e.key === 'Escape') closeMobileOverlay();
  });
}

function setupFilters() {
  document.querySelectorAll('.chip[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      const value  = btn.dataset.value;
      activeFilters[filter] = value;
      const group = btn.closest('.filter-chips');
      if (group) {
        group.querySelectorAll('.chip').forEach(c => {
          const active = c.dataset.value === value;
          c.classList.toggle('chip-active', active);
          c.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
      }
      applyFilters();
    });
  });
  document.getElementById('filter-category').addEventListener('click', (e) => {
    const btn = e.target.closest('.chip[data-filter="category"]');
    if (!btn) return;
    const value = btn.dataset.value;
    activeFilters.category = value;
    document.querySelectorAll('#filter-category .chip').forEach(c => {
      const active = c.dataset.value === value;
      c.classList.toggle('chip-active', active);
      c.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    applyFilters();
  });
}

function applyFilters() {
  filteredNodes = nodes.filter(n => {
    // INITIATIVE-012C: always hide sandbox
    if (n.category === '00-sandbox') return false;
    if (activeFilters.level     !== 'all' && n.level     !== activeFilters.level)    return false;
    if (activeFilters.stability !== 'all' && n.stability !== activeFilters.stability) return false;
    if (activeFilters.category  !== 'all' && n.category  !== activeFilters.category)  return false;
    if (searchQuery) {
      const h = (n.title + ' ' + n.id + ' ' + catLabel(n.category) + ' ' + (n.tags || []).join(' ')).toLowerCase();
      if (!h.includes(searchQuery)) return false;
    }
    return true;
  });
  filteredNodes.sort((a, b) => {
    if (a.id === selectedId) return -1;
    if (b.id === selectedId) return  1;
    return a.title.localeCompare(b.title);
  });
  renderGrid();
  document.getElementById('results-count').textContent =
    filteredNodes.length.toLocaleString() + ' skill' + (filteredNodes.length !== 1 ? 's' : '');
}

function renderGrid() {
  const grid = document.getElementById('skill-grid');
  grid.innerHTML = '';
  if (filteredNodes.length === 0) {
    grid.innerHTML = '<div class="empty-state" role="status"><p class="empty-state-title">No skills found</p><p>Try a different search or clear your filters.</p></div>';
    return;
  }
  const fragment = document.createDocumentFragment();
  for (const node of filteredNodes) fragment.appendChild(createSkillCard(node));
  grid.appendChild(fragment);
}

function createSkillCard(node) {
  const card = document.createElement('div');
  card.className = 'skill-card' + (node.id === selectedId ? ' selected' : '');
  card.setAttribute('role', 'listitem');
  card.setAttribute('tabindex', '0');
  card.dataset.id = node.id;
  const title = searchQuery ? highlightText(node.title, searchQuery) : escHtml(node.title);
  // INITIATIVE-012C: show human category label on card
  card.innerHTML =
    '<div class="skill-card-title">' + title + '</div>' +
    '<div class="skill-card-row">' +
      '<span class="badge badge-level-' + node.level + '">' + node.level + '</span>' +
      '<span class="badge badge-' + node.stability + '">' + node.stability + '</span>' +
      '<span class="skill-card-cat">' + escHtml(catLabel(node.category)) + '</span>' +
      '<span class="skill-card-id">' + escHtml(node.id) + '</span>' +
    '</div>';
  card.addEventListener('click',   () => selectSkill(node.id));
  card.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectSkill(node.id); }
  });
  return card;
}

function highlightText(text, query) {
  return escHtml(text).replace(
    new RegExp('(' + escHtml(query).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi'),
    '<mark>$1</mark>'
  );
}

function escHtml(s) {
  return String(s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function selectSkill(id) {
  selectedId = id;
  const node = nodeById[id];
  if (!node) return;
  const url = new URL(window.location.href);
  url.searchParams.set('skill', id);
  window.history.pushState({ skill: id }, '', url.toString());
  document.querySelectorAll('.skill-card').forEach(c => {
    c.classList.toggle('selected', c.dataset.id === id);
  });
  renderDetail(node);
}

function renderDetail(node) {
  const empty   = document.getElementById('detail-empty');
  const content = document.getElementById('detail-content');
  empty.hidden   = true;
  content.hidden = false;

  // category badge: human label
  document.getElementById('d-cat').textContent       = catLabel(node.category);
  document.getElementById('d-title').textContent     = node.title;
  document.getElementById('d-id').textContent        = node.id;
  document.getElementById('d-level').textContent     = node.level     || '—';
  document.getElementById('d-stability').textContent = node.stability || '—';
  document.getElementById('d-version').textContent   = node.version   || '—';
  document.getElementById('d-layer').textContent     = node.layer     || '—';
  document.getElementById('d-domain').textContent    = catLabel(node.category);
  document.getElementById('d-added').textContent     = node.added     || '—';
  document.getElementById('d-source').textContent    = node.source_file || '—';

  const ghBtn = document.getElementById('btn-github');
  if (node.source_file) {
    ghBtn.onclick = () => window.open(GITHUB_BASE + node.source_file, '_blank', 'noopener');
    ghBtn.style.display = '';
  } else {
    ghBtn.style.display = 'none';
  }
  document.getElementById('btn-share').onclick = () => {
    const u = new URL(window.location.href);
    u.searchParams.set('skill', node.id);
    navigator.clipboard.writeText(u.toString()).then(() => showToast('🔗 Link copied!'));
  };

  // INITIATIVE-012C Phase 4: all dependency entries clickable with titles
  renderDepSection('d-prereqs',     'section-prereqs',     node.prerequisites || [],
    'No prerequisites — this skill is a foundation.');

  // Required By: aggregate from both prereqBy index AND requiredByIdx
  const requiredByIds = [
    ...(requiredByIdx[node.id] || []),
    ...(prereqBy[node.id]     || []),
  ];
  const requiredByUniq = [...new Set(requiredByIds)];
  renderDepSection('d-required-by', 'section-required-by', requiredByUniq,
    'No skills currently require this one.');

  // Requires (outgoing REQUIRES edges)
  const reqOut = (edgesBySource[node.id] || []).filter(e => e.type === 'REQUIRES').map(e => e.target);
  renderDepSection('d-requires-out', 'section-requires-out', reqOut,
    'This skill has no outgoing REQUIRES edges.');

  // Related: node.related_skills + bidirectional from relatedIdx
  const relatedIds = [
    ...(node.related_skills || []),
    ...(relatedIdx[node.id] || []),
  ];
  const relatedUniq = [...new Set(relatedIds)].filter(id => id !== node.id);
  renderDepSection('d-related', 'section-related', relatedUniq,
    'No related skills defined.');

  const isMobile = window.innerWidth <= 900;
  if (isMobile) {
    const overlay = document.getElementById('mobile-overlay');
    const body    = document.getElementById('mobile-overlay-body');
    body.innerHTML = document.getElementById('detail-content').outerHTML;
    body.querySelectorAll('.dep-item[data-id]').forEach(item => {
      item.addEventListener('click', () => selectSkill(item.dataset.id));
    });
    overlay.removeAttribute('hidden');
  }
}

// INITIATIVE-012C Phase 4 & 7: clickable deps with empty-state messaging
function renderDepSection(listId, sectionId, ids, emptyMsg) {
  const list    = document.getElementById(listId);
  const section = document.getElementById(sectionId);
  list.innerHTML = '';

  if (!ids.length) {
    section.style.display = '';
    const empty = document.createElement('p');
    empty.className = 'dep-empty';
    empty.textContent = emptyMsg;
    list.appendChild(empty);
    return;
  }

  section.style.display = '';
  for (const id of ids) {
    const n     = nodeById[id];
    const label = n ? n.title : id;
    const cat   = n ? catLabel(n.category) : '';
    const item  = document.createElement('div');
    item.className = 'dep-item';
    item.dataset.id = id;
    item.setAttribute('role', 'button');
    item.setAttribute('tabindex', '0');
    item.setAttribute('aria-label', label + (cat ? ' (' + cat + ')' : ''));
    item.innerHTML =
      '<svg class="dep-arrow" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="13 6 19 12 13 18"/></svg>' +
      '<span class="dep-label">' + escHtml(label) + '</span>' +
      (cat ? '<span class="dep-cat">' + escHtml(cat) + '</span>' : '');
    item.addEventListener('click',   () => { selectSkill(id); scrollToCard(id); });
    item.addEventListener('keydown', e  => { if (e.key === 'Enter') { selectSkill(id); scrollToCard(id); } });
    list.appendChild(item);
  }
}

function scrollToCard(id) {
  const card = document.querySelector('.skill-card[data-id="' + CSS.escape(id) + '"]');
  if (card) card.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function setupURLRouting()  { window.addEventListener('popstate', handleURLParam); }
function handleURLParam()   {
  const params  = new URLSearchParams(window.location.search);
  const skillId = params.get('skill');
  if (skillId && nodeById[skillId]) selectSkill(skillId);
}
function setupMobileOverlayClose() {
  document.getElementById('close-overlay').addEventListener('click', closeMobileOverlay);
}
function closeMobileOverlay() {
  document.getElementById('mobile-overlay').setAttribute('hidden', '');
}
function showToast(msg) {
  const toast = document.getElementById('toast');
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 2200);
}
