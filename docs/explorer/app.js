/* ============================================================
   INITIATIVE-014A3 — Explorer V2 + Shareable URLs
   AI Engineering Operating System — Skills Explorer
   ============================================================ */

'use strict';

/* ------ Category normalization map ------ */
const CAT_LABELS = {
  '01-perception':            'Perception',
  '02-reasoning':             'Reasoning',
  '03-memory':                'Memory',
  '04-action':                'Action',
  '05-code':                  'Code',
  '06-communication':         'Communication',
  '07-tool-use':              'Tool Use',
  '08-multimodal':            'Multimodal',
  '09-agentic-patterns':      'Agentic Patterns',
  '10-content-understanding': 'Content Understanding',
  '11-web':                   'Web',
  '12-data':                  'Data',
  '13-creative':              'Creative',
  '14-security':              'Security',
  '15-orchestration':         'Orchestration',
  '16-domain-specific':       'Domain Specific',
  '17-infrastructure':        'Infrastructure',
};

function catLabel(raw) {
  if (!raw) return 'Uncategorised';
  const key = raw.toLowerCase();
  if (CAT_LABELS[key]) return CAT_LABELS[key];
  for (const [k, v] of Object.entries(CAT_LABELS)) {
    if (key.startsWith(k)) return v;
  }
  return raw;
}

/* ------ Path normalization (INITIATIVE-012B1) ------ */
function getGraphUrl() {
  const h = window.location.hostname;
  if (h === 'localhost' || h === '127.0.0.1') {
    return '../../data/SKILLS_GRAPH.json';
  }
  return '/skills-tree/data/SKILLS_GRAPH.json';
}

const GRAPH_URL = getGraphUrl();
console.info('GRAPH URL:', GRAPH_URL);

/* ------ DOM refs ------ */
const $grid          = document.getElementById('skill-grid');
const $search        = document.getElementById('skill-search');
const $count         = document.getElementById('results-count');
const $catFilter     = document.getElementById('filter-category');
const $detailEmpty   = document.getElementById('detail-empty');
const $detailContent = document.getElementById('detail-content');
const $toast         = document.getElementById('toast');

/* ------ State ------ */
let allNodes       = [];
let nodeMap        = {};
let prereqMap      = {};
let requiredByMap  = {};
let requiresOutMap = {};
let relatedMap     = {};
let activeFilters  = { level: 'all', stability: 'all', category: 'all' };
let selectedId     = null;
let _toastTimer    = null;

/* ============================================================
   PHASE 3 — Featured Skills & Popular Paths (V2)
   ============================================================ */
const FEATURED_SKILLS = [
  { id: '09-agentic-patterns/react',           label: 'ReAct',             emoji: '🔄' },
  { id: '03-memory/rag',                       label: 'RAG',               emoji: '🗄️' },
  { id: '09-agentic-patterns/reflection',      label: 'Reflection',        emoji: '🪞' },
  { id: '09-agentic-patterns/lats',            label: 'LATS',              emoji: '🌳' },
  { id: '07-tool-use/function-calling',        label: 'Function Calling',  emoji: '🔧' },
  { id: '09-agentic-patterns/tool-use-loop',   label: 'Tool Use Loop',     emoji: '⚙️' },
  { id: '02-reasoning/task-decomposition',     label: 'Goal Decomposition',emoji: '🎯' },
  { id: '02-reasoning/planning',               label: 'Plan & Execute',    emoji: '📋' },
];

const POPULAR_PATHS = [
  {
    name: 'RAG Engineer',
    skills: ['03-memory/rag', '12-data/embedding-generation', '03-memory/vector-store-retrieval', '03-memory/memory-injection'],
  },
  {
    name: 'Coding Agent',
    skills: ['09-agentic-patterns/react', '05-code/code-generation', '07-tool-use/function-calling', '09-agentic-patterns/reflection'],
  },
  {
    name: 'Research Agent',
    skills: ['11-web/web-search', '03-memory/rag', '02-reasoning/task-decomposition', '06-communication/summarization'],
  },
  {
    name: 'Multi-Agent Systems',
    skills: ['15-orchestration/multi-agent', '09-agentic-patterns/react', '07-tool-use/function-calling', '02-reasoning/planning'],
  },
  {
    name: 'Evaluation Specialist',
    skills: ['09-agentic-patterns/reflection', '02-reasoning/self-consistency', '09-agentic-patterns/lats', '02-reasoning/task-decomposition'],
  },
];

function renderDiscoveryPanel() {
  const $panel = document.getElementById('discovery-panel');
  if (!$panel) return;

  /* Featured Skills strip */
  const featuredItems = FEATURED_SKILLS.map(f => {
    const node = Object.values(nodeMap).find(n =>
      n.id === f.id ||
      n.id.endsWith('/' + f.id.split('/').pop()) ||
      (n.id || '').toLowerCase().includes(f.id.split('/').pop())
    );
    const resolvedId = node ? node.id : null;
    return `<button class="featured-chip${resolvedId ? '' : ' featured-chip-disabled'}" 
      data-nav="${escHtml(resolvedId || '')}" 
      title="${escHtml(f.label)}"
      ${resolvedId ? '' : 'disabled'}>
      <span class="featured-emoji">${f.emoji}</span>
      <span class="featured-label">${escHtml(f.label)}</span>
    </button>`;
  }).join('');

  /* Popular Paths */
  const pathItems = POPULAR_PATHS.map((path, pi) => {
    const steps = path.skills.map((sid, i) => {
      const node = Object.values(nodeMap).find(n =>
        n.id === sid || n.id.endsWith('/' + sid.split('/').pop())
      );
      const label = node ? (node.name || node.label || node.id) : sid.split('/').pop();
      const nid   = node ? node.id : null;
      return `<button class="path-step${nid ? '' : ' path-step-disabled'}" 
        data-nav="${escHtml(nid || '')}" 
        ${nid ? '' : 'disabled'}
        aria-label="Navigate to ${escHtml(label)}">${i + 1}. ${escHtml(label)}</button>`;
    }).join('<span class="path-arrow">→</span>');
    return `<div class="path-row"><span class="path-name">${escHtml(path.name)}</span><div class="path-steps">${steps}</div></div>`;
  }).join('');

  $panel.innerHTML = `
    <section class="discovery-section">
      <div class="discovery-header">
        <h3 class="discovery-title">⭐ Featured Skills</h3>
        <button class="surprise-btn" id="btn-surprise" aria-label="Navigate to a random skill">
          🎲 Surprise Me
        </button>
      </div>
      <div class="featured-strip">${featuredItems}</div>
    </section>
    <section class="discovery-section">
      <h3 class="discovery-title">🛤️ Popular Learning Paths</h3>
      <div class="paths-list">${pathItems}</div>
    </section>`;

  /* Surprise Me */
  document.getElementById('btn-surprise')?.addEventListener('click', () => {
    const visible = allNodes.filter(n => !isSandbox(n));
    if (!visible.length) return;
    const node = visible[Math.floor(Math.random() * visible.length)];
    selectCard(node.id);
    scrollToCard(node.id);
    showToast(`🎲 ${node.name || node.id}`);
  });

  /* Featured chip nav */
  $panel.querySelectorAll('.featured-chip[data-nav]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (!btn.dataset.nav) return;
      selectCard(btn.dataset.nav);
      scrollToCard(btn.dataset.nav);
    });
  });

  /* Path step nav */
  $panel.querySelectorAll('.path-step[data-nav]').forEach(btn => {
    btn.addEventListener('click', () => {
      if (!btn.dataset.nav) return;
      selectCard(btn.dataset.nav);
      scrollToCard(btn.dataset.nav);
    });
  });
}

/* ============================================================
   PHASE 3 — Shareable #skill= URL scheme (INITIATIVE-014A3)
   Back-compat: bare #<id> still works.
   ============================================================ */
function getHashSkillId() {
  const raw = window.location.hash.slice(1);
  if (!raw) return null;
  if (raw.startsWith('skill=')) return decodeURIComponent(raw.slice(6));
  return decodeURIComponent(raw); // legacy bare hash
}

function setHashSkillId(id) {
  const encoded = encodeURIComponent(id);
  const newHash = `#skill=${encoded}`;
  if (window.location.hash !== newHash) {
    history.pushState(null, '', newHash);
  }
}

window.addEventListener('popstate', () => {
  const id = getHashSkillId();
  if (id && nodeMap[id]) {
    showDetail(nodeMap[id]);
    scrollToCard(id);
  }
});

/* ============================================================
   Dependency Index Builder
   ============================================================ */
function buildDependencyIndex(graph) {
  prereqMap = {}; requiredByMap = {}; requiresOutMap = {}; relatedMap = {};
  for (const node of graph.nodes) {
    prereqMap[node.id] = []; requiredByMap[node.id] = [];
    requiresOutMap[node.id] = []; relatedMap[node.id] = [];
  }
  if (!Array.isArray(graph.edges)) return;
  for (const edge of graph.edges) {
    const src  = nodeMap[edge.source];
    const tgt  = nodeMap[edge.target];
    if (!src || !tgt) continue;
    const type = (edge.type || edge.relation || '').toLowerCase();
    if (type === 'prerequisite' || type === 'prereq') {
      prereqMap[tgt.id].push(src);
      requiredByMap[src.id].push(tgt);
    } else if (type === 'requires') {
      requiresOutMap[src.id].push(tgt);
      requiredByMap[tgt.id].push(src);
    } else if (type === 'related' || type === 'relates' || type === 'related_to') {
      relatedMap[src.id].push(tgt);
      relatedMap[tgt.id].push(src);
    } else {
      prereqMap[tgt.id].push(src);
      requiredByMap[src.id].push(tgt);
    }
  }
  for (const id of Object.keys(nodeMap)) {
    prereqMap[id]      = dedup(prereqMap[id]);
    requiredByMap[id]  = dedup(requiredByMap[id]);
    requiresOutMap[id] = dedup(requiresOutMap[id]);
    relatedMap[id]     = dedup(relatedMap[id]);
  }
}

function dedup(arr) {
  const seen = new Set();
  return arr.filter(n => { if (seen.has(n.id)) return false; seen.add(n.id); return true; });
}

/* ============================================================
   Resilient loader (INITIATIVE-012B1)
   ============================================================ */
async function loadGraph() {
  try {
    const res = await fetch(GRAPH_URL);
    if (!res.ok) throw new Error(`HTTP ${res.status}: ${GRAPH_URL}`);
    const data = await res.json();
    if (!data || !Array.isArray(data.nodes)) throw new Error('Invalid graph schema: nodes array missing');
    return data;
  } catch (err) {
    console.error('Graph load failed:', err);
    showGraphError(err);
    throw err;
  }
}

function showGraphError(err) {
  $grid.innerHTML = `
    <div class="empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
      </svg>
      <p class="empty-state-title">Failed to load graph</p>
      <p>Attempted URL:<br><code>${GRAPH_URL}</code></p>
      <p>Reason: ${err.message}</p>
      <p style="text-align:left;color:var(--color-text-faint);font-size:var(--text-xs);margin-top:.5rem">
        ✓ Start a local server from repo root<br>
        ✓ Verify <code>data/SKILLS_GRAPH.json</code> exists<br>
        ✓ Verify the fetch path is correct<br>
        ✓ Open the correct URL
      </p>
    </div>`;
}

/* ============================================================
   Filtering + Rendering
   ============================================================ */
function isSandbox(node) {
  const cat = (node.category || node.domain || '').toLowerCase();
  return cat.startsWith('00-sandbox') || cat === 'sandbox';
}

function matchesFilters(node) {
  if (isSandbox(node)) return false;
  const q = ($search.value || '').trim().toLowerCase();
  if (q) {
    const hay = [node.id, node.name, node.label, node.category, node.domain, node.layer]
      .filter(Boolean).join(' ').toLowerCase();
    if (!hay.includes(q)) return false;
  }
  if (activeFilters.level !== 'all') {
    if (!(node.level || node.complexity || '').toLowerCase().includes(activeFilters.level)) return false;
  }
  if (activeFilters.stability !== 'all') {
    if (!(node.stability || node.status || '').toLowerCase().includes(activeFilters.stability)) return false;
  }
  if (activeFilters.category !== 'all') {
    if (!(node.category || node.domain || '').toLowerCase().includes(activeFilters.category)) return false;
  }
  return true;
}

function highlight(text, q) {
  if (!q || !text) return escHtml(text || '');
  const esc = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return escHtml(text).replace(new RegExp(esc, 'gi'), m => `<mark>${m}</mark>`);
}

function escHtml(s) {
  return (s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

function renderList() {
  const q   = ($search.value || '').trim().toLowerCase();
  const vis = allNodes.filter(matchesFilters);
  if (!vis.length) {
    $grid.innerHTML = `<div class="empty-state">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
      <p class="empty-state-title">No skills found</p><p>Try adjusting your search or filters</p></div>`;
    $count.textContent = '0 results';
    return;
  }
  $count.textContent = `${vis.length} skill${vis.length !== 1 ? 's' : ''}`;
  $grid.innerHTML = vis.map(node => {
    const name  = node.name || node.label || node.id;
    const cat   = catLabel(node.category || node.domain || '');
    const level = (node.level || node.complexity || '').toLowerCase();
    const reqBy = (requiredByMap[node.id] || []).length;
    const reqByBadge = reqBy > 0 ? `<span class="skill-card-reqby" title="${reqBy} skill(s) require this">${reqBy} required by</span>` : '';
    const lvlBadge   = level ? `<span class="badge badge-level-${level}">${level}</span>` : '';
    return `<article class="skill-card${selectedId === node.id ? ' selected' : ''}"
               role="listitem" tabindex="0"
               data-id="${escHtml(node.id)}"
               aria-label="${escHtml(name)}, ${cat}, ${level || 'no level'}">
      <div class="skill-card-title">${highlight(name, q)}</div>
      <div class="skill-card-row">
        <code class="skill-card-id">${escHtml(node.id)}</code>
        <span class="skill-card-cat">${escHtml(cat)}</span>
        ${lvlBadge}
        ${reqByBadge}
      </div>
    </article>`;
  }).join('');
}

/* ============================================================
   Category chips
   ============================================================ */
function buildCategoryChips(nodes) {
  const catCounts = {};
  for (const n of nodes) {
    if (isSandbox(n)) continue;
    const key   = (n.category || n.domain || '').toLowerCase();
    const label = CAT_LABELS[key];
    if (!label) continue;
    catCounts[key] = (catCounts[key] || 0) + 1;
  }
  const sorted = Object.entries(catCounts).sort((a, b) => (parseInt(a[0]) || 99) - (parseInt(b[0]) || 99));
  const allBtn = `<button class="chip chip-active" data-filter="category" data-value="all" aria-pressed="true">All</button>`;
  const chips  = sorted.map(([key, cnt]) =>
    `<button class="chip" data-filter="category" data-value="${escHtml(key)}" aria-pressed="false" title="${cnt} skills">${escHtml(CAT_LABELS[key])}</button>`
  ).join('');
  $catFilter.innerHTML = allBtn + chips;
}

/* ============================================================
   Graph Health Panel
   ============================================================ */
function updateHealthPanel(graph) {
  const visible = allNodes;
  const withEdges = visible.filter(n =>
    (prereqMap[n.id]||[]).length || (requiredByMap[n.id]||[]).length ||
    (requiresOutMap[n.id]||[]).length || (relatedMap[n.id]||[]).length
  );
  const isolated = visible.length - withEdges.length;
  const density  = visible.length ? ((graph.edges||[]).length / visible.length).toFixed(1) : '—';
  let topNode = null, topCount = 0;
  for (const n of visible) {
    const cnt = (prereqMap[n.id]||[]).length + (requiredByMap[n.id]||[]).length +
                (requiresOutMap[n.id]||[]).length + (relatedMap[n.id]||[]).length;
    if (cnt > topCount) { topCount = cnt; topNode = n; }
  }
  const pct = visible.length ? Math.round(withEdges.length / visible.length * 100) : 0;
  document.getElementById('h-coverage').textContent = `${pct}%`;
  document.getElementById('h-isolated').textContent = isolated;
  document.getElementById('h-density').textContent  = density;
  document.getElementById('h-top').textContent      = topNode ? `${topNode.name || topNode.id} (${topCount})` : '—';
}

/* ============================================================
   Hero stats
   ============================================================ */
function updateHeroStats(graph) {
  const cats = new Set(allNodes.map(n => n.category || n.domain || '').filter(Boolean));
  const reqEdges = (graph.edges||[]).filter(e => {
    const t = (e.type||e.relation||'').toLowerCase();
    return t === 'requires' || t === 'prerequisite' || t === 'prereq' || !t;
  }).length;
  document.getElementById('hero-nodes').textContent    = allNodes.length;
  document.getElementById('hero-edges').textContent    = (graph.edges||[]).length;
  document.getElementById('hero-cats').textContent     = cats.size;
  document.getElementById('hero-requires').textContent = reqEdges;
}

/* ============================================================
   Detail Panel
   ============================================================ */
function showDetail(node) {
  selectedId = node.id;
  setHashSkillId(node.id); // Phase 3 — update shareable URL
  renderList();
  attachCardListeners();
  $detailEmpty.hidden   = true;
  $detailContent.hidden = false;

  const name  = node.name || node.label || node.id;
  const level = (node.level || node.complexity || '').toLowerCase();
  const stab  = (node.stability || node.status  || '').toLowerCase();
  const ver   = node.version || node.schema_version || '';
  const layer = node.layer || '';
  const cat   = catLabel(node.category || node.domain || '');

  document.getElementById('d-cat').textContent   = cat;
  document.getElementById('d-title').textContent = name;
  document.getElementById('d-id').textContent    = node.id;

  document.getElementById('btn-github').onclick = () =>
    window.open('https://github.com/SamoTech/skills-tree', '_blank');

  // Phase 3 — canonical #skill= share URL
  document.getElementById('btn-share').onclick = () => {
    const url = `${location.origin}${location.pathname}#skill=${encodeURIComponent(node.id)}`;
    navigator.clipboard?.writeText(url)
      .then(() => showToast('🔗 Link copied!'))
      .catch(() => showToast('Copy failed — use the address bar'));
  };

  const $lvl = document.getElementById('d-level');
  const $stab = document.getElementById('d-stability');
  const $ver  = document.getElementById('d-version');
  const $lay  = document.getElementById('d-layer');
  $lvl.textContent  = level ? `\u25cf ${level}` : '';
  $stab.textContent = stab  ? stab              : '';
  $ver.textContent  = ver   ? `v${ver}`          : '';
  $lay.textContent  = layer ? layer              : '';
  $lvl.className    = `tag badge badge-level-${level}`;
  $stab.className   = `tag badge badge-${stab}`;
  $ver.className    = 'tag'; $lay.className = 'tag';

  const $tw = document.getElementById('d-tags-wrap');
  const tags = node.tags || node.keywords || [];
  if (Array.isArray(tags) && tags.length) {
    $tw.innerHTML = tags.map(t => `<span class="tag">${escHtml(t)}</span>`).join('');
    $tw.hidden = false;
  } else { $tw.innerHTML = ''; $tw.hidden = true; }

  document.getElementById('d-domain').textContent = catLabel(node.domain || node.category || '');
  document.getElementById('d-added').textContent  = node.added || node.created_at || '—';
  document.getElementById('d-source').textContent = node.source_file || node.file || node.id;

  renderDepSection('section-prereqs',     'd-prereqs',     prereqMap[node.id]     || [], 'No prerequisites — this is a foundational skill.');
  renderDepSection('section-required-by', 'd-required-by', requiredByMap[node.id] || [], 'No skills currently require this as a dependency.');
  renderDepSection('section-requires-out','d-requires-out',requiresOutMap[node.id]|| [], 'No outgoing requires edges.');
  renderDepSection('section-related',     'd-related',     relatedMap[node.id]    || [], 'No related skills mapped yet.');
}

function renderDepSection(sectionId, listId, nodes, emptyMsg) {
  const $list = document.getElementById(listId);
  if (!nodes.length) {
    $list.innerHTML = `<span class="dep-empty">${escHtml(emptyMsg)}</span>`;
    return;
  }
  $list.innerHTML = nodes.map(n => {
    const label = n.name || n.label || n.id;
    const cat   = catLabel(n.category || n.domain || '');
    return `<button class="dep-item" data-nav="${escHtml(n.id)}" tabindex="0" aria-label="Navigate to ${escHtml(label)}">
      <svg class="dep-arrow" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg>
      <span class="dep-label">${escHtml(label)}</span>
      <span class="dep-cat">${escHtml(cat)}</span>
    </button>`;
  }).join('');
  $list.querySelectorAll('.dep-item').forEach(btn => {
    btn.addEventListener('click', () => {
      const t = nodeMap[btn.dataset.nav];
      if (t) { showDetail(t); scrollToCard(t.id); }
    });
    btn.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); btn.click(); }
    });
  });
}

function scrollToCard(id) {
  const el = $grid.querySelector(`[data-id="${CSS.escape(id)}"]`);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/* ============================================================
   Filter + search listeners
   ============================================================ */
function attachFilterListeners() {
  document.querySelectorAll('[data-filter]').forEach(btn => {
    btn.addEventListener('click', () => {
      const { filter, value } = btn.dataset;
      activeFilters[filter] = value;
      const group = filter === 'category'  ? $catFilter
                  : filter === 'level'     ? document.getElementById('filter-level')
                  :                          document.getElementById('filter-stability');
      group.querySelectorAll('.chip').forEach(c => {
        const a = c.dataset.value === value;
        c.classList.toggle('chip-active', a);
        c.setAttribute('aria-pressed', a);
      });
      renderList();
      attachCardListeners();
    });
  });
}

function attachCardListeners() {
  $grid.querySelectorAll('.skill-card').forEach(card => {
    card.addEventListener('click', () => selectCard(card.dataset.id));
    card.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectCard(card.dataset.id); }
    });
  });
}

function selectCard(id) {
  const node = nodeMap[id];
  if (!node) return;
  showDetail(node);
  if (window.innerWidth <= 900) showMobileOverlay();
}

function showMobileOverlay() {
  const overlay = document.getElementById('mobile-overlay');
  const body    = document.getElementById('mobile-overlay-body');
  body.innerHTML = '';
  body.appendChild($detailContent.cloneNode(true));
  overlay.hidden = false;
  document.body.style.overflow = 'hidden';
}

document.getElementById('close-overlay')?.addEventListener('click', () => {
  document.getElementById('mobile-overlay').hidden = true;
  document.body.style.overflow = '';
});

document.addEventListener('keydown', e => {
  if (e.key === '/' && document.activeElement !== $search) { e.preventDefault(); $search.focus(); }
  if (e.key === 'Escape') {
    $search.blur();
    document.getElementById('mobile-overlay').hidden = true;
    document.body.style.overflow = '';
  }
});

$search.addEventListener('input', () => { renderList(); attachCardListeners(); });

/* ============================================================
   Toast
   ============================================================ */
function showToast(msg) {
  $toast.textContent = msg;
  $toast.classList.add('show');
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => $toast.classList.remove('show'), 2500);
}

/* ============================================================
   Dark mode toggle
   ============================================================ */
(function () {
  const root   = document.documentElement;
  const toggle = document.querySelector('[data-theme-toggle]');
  let mode = root.getAttribute('data-theme') || 'dark';
  function applyTheme(m) {
    mode = m;
    root.setAttribute('data-theme', m);
    if (toggle) {
      toggle.setAttribute('aria-label', `Switch to ${m === 'dark' ? 'light' : 'dark'} mode`);
      toggle.innerHTML = m === 'dark'
        ? '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }
  }
  applyTheme(mode);
  toggle?.addEventListener('click', () => applyTheme(mode === 'dark' ? 'light' : 'dark'));
})();

/* ============================================================
   Bootstrap
   ============================================================ */
async function init() {
  let graph;
  try { graph = await loadGraph(); } catch { return; }

  console.info('NODES:', graph.nodes.length);
  console.info('EDGES:', (graph.edges || []).length);

  nodeMap  = {};
  for (const n of graph.nodes) nodeMap[n.id] = n;

  allNodes = graph.nodes.filter(n => !isSandbox(n));

  buildDependencyIndex(graph);
  updateHeroStats(graph);
  updateHealthPanel(graph);
  buildCategoryChips(allNodes);
  renderDiscoveryPanel(); // Phase 3 — Featured Skills + Popular Paths + Surprise Me
  renderList();
  attachCardListeners();
  attachFilterListeners();

  // Phase 3 — deep-link on load (supports #skill=<id> and legacy #<id>)
  const skillId = getHashSkillId();
  if (skillId && nodeMap[skillId]) {
    showDetail(nodeMap[skillId]);
    scrollToCard(skillId);
  }
}

init();
