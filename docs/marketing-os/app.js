/**
 * MARKETING AI OS — app.js
 * Initiative: INITIATIVE-020 | Skills Tree
 * Blueprint Generator Engine
 */

// ============================================================
// DATA — 50 Marketing Goals (from MARKETING_GOAL_CATALOG.md)
// ============================================================

const GOALS = [
  // Category 1 — Paid Social Media Buying
  { id: 1,  cat: 'Paid Social',      tag: 'meta-cold-traffic',          name: 'Launch a Meta Ads cold-traffic prospecting campaign', skills: ['audience-segmentation','creative-testing','bid-optimization'] },
  { id: 2,  cat: 'Paid Social',      tag: 'tiktok-ugc-testing',         name: 'Build a TikTok UGC creative testing system', skills: ['creative-testing','data-analysis','intent-classification'] },
  { id: 3,  cat: 'Paid Social',      tag: 'paid-social-scaling',        name: 'Scale a winning ad set from $100/day to $1,000/day', skills: ['bid-optimization','data-analysis','audience-segmentation'] },
  { id: 4,  cat: 'Paid Social',      tag: 'cross-platform-retargeting', name: 'Create a retargeting architecture across Meta and Google', skills: ['audience-segmentation','multi-agent-orchestration','rag'] },
  { id: 5,  cat: 'Paid Social',      tag: 'lookalike-expansion',        name: 'Build a lookalike audience expansion strategy', skills: ['audience-segmentation','embedding-generation','data-analysis'] },
  { id: 6,  cat: 'Paid Social',      tag: 'youtube-brand-awareness',    name: 'Launch a YouTube pre-roll campaign for brand awareness', skills: ['intent-classification','creative-testing','data-analysis'] },
  { id: 7,  cat: 'Paid Social',      tag: 'linkedin-b2b-leads',         name: 'Build a LinkedIn B2B lead generation campaign', skills: ['audience-segmentation','intent-classification','bid-optimization'] },
  { id: 8,  cat: 'Paid Social',      tag: 'paid-social-full-funnel',    name: 'Create a full-funnel paid social strategy (TOFU-MOFU-BOFU)', skills: ['audience-segmentation','bid-optimization','data-analysis'] },
  // Category 2 — Creative
  { id: 9,  cat: 'Creative',         tag: 'dtc-ab-creative',            name: 'Build an A/B creative testing framework for DTC ads', skills: ['creative-testing','data-analysis','reasoning'] },
  { id: 10, cat: 'Creative',         tag: 'video-hook-testing',         name: 'Create a hook-testing system for video ads', skills: ['creative-testing','intent-classification','summarization'] },
  { id: 11, cat: 'Creative',         tag: 'creative-brief-agent',       name: 'Design a creative brief generation agent', skills: ['code-generation','summarization','rag'] },
  { id: 12, cat: 'Creative',         tag: 'ugc-script-generator',       name: 'Build a UGC script generator for influencer ads', skills: ['summarization','rag','reasoning'] },
  { id: 13, cat: 'Creative',         tag: 'ad-copy-variants',           name: 'Create an ad copy variant generator', skills: ['code-generation','summarization','intent-classification'] },
  { id: 14, cat: 'Creative',         tag: 'creative-fatigue-rotation',  name: 'Build a creative fatigue detection and rotation system', skills: ['data-analysis','intent-classification','audit-logging'] },
  { id: 15, cat: 'Creative',         tag: 'creative-adaptation-pipeline', name: 'Create a multi-format creative adaptation pipeline', skills: ['summarization','code-generation','data-analysis'] },
  // Category 3 — Landing Page
  { id: 16, cat: 'Landing Page',     tag: 'landing-page-audit',         name: 'Audit and score a landing page for conversion', skills: ['reasoning','rag','data-analysis'] },
  { id: 17, cat: 'Landing Page',     tag: 'landing-page-copy-variants', name: 'Generate landing page copy variants for A/B testing', skills: ['summarization','creative-testing','code-generation'] },
  { id: 18, cat: 'Landing Page',     tag: 'cro-agent',                  name: 'Build a conversion rate optimization (CRO) agent', skills: ['reasoning','data-analysis','rag'] },
  { id: 19, cat: 'Landing Page',     tag: 'headline-testing',           name: 'Create a headline testing framework', skills: ['creative-testing','data-analysis','reasoning'] },
  { id: 20, cat: 'Landing Page',     tag: 'post-click-audit',           name: 'Build a post-click experience audit system', skills: ['reasoning','rag','audit-logging'] },
  { id: 21, cat: 'Landing Page',     tag: 'landing-page-personalization', name: 'Create a landing page personalization engine', skills: ['audience-segmentation','rag','memory-injection'] },
  // Category 4 — Agent Teams
  { id: 22, cat: 'Agent Teams',      tag: 'media-buying-team',          name: 'Build a media buying AI agent team', skills: ['multi-agent-orchestration','bid-optimization','data-analysis'] },
  { id: 23, cat: 'Agent Teams',      tag: 'campaign-strategy-team',     name: 'Create a campaign strategy AI agent team', skills: ['multi-agent-orchestration','reasoning','rag'] },
  { id: 24, cat: 'Agent Teams',      tag: 'creative-production-team',   name: 'Build a creative production AI agent team', skills: ['multi-agent-orchestration','summarization','creative-testing'] },
  { id: 25, cat: 'Agent Teams',      tag: 'performance-analysis-team',  name: 'Create a performance analysis AI agent team', skills: ['multi-agent-orchestration','data-analysis','reporting'] },
  { id: 26, cat: 'Agent Teams',      tag: 'content-marketing-team',     name: 'Build a content marketing AI agent team', skills: ['multi-agent-orchestration','rag','summarization'] },
  { id: 27, cat: 'Agent Teams',      tag: 'growth-hacking-team',        name: 'Create a growth hacking AI agent team', skills: ['multi-agent-orchestration','reasoning','data-analysis'] },
  // Category 5 — Analytics
  { id: 28, cat: 'Analytics',        tag: 'marketing-attribution',      name: 'Build a marketing attribution model', skills: ['data-analysis','reasoning','audit-logging'] },
  { id: 29, cat: 'Analytics',        tag: 'ltv-prediction',             name: 'Create a customer lifetime value (LTV) prediction system', skills: ['data-analysis','embedding-generation','reasoning'] },
  { id: 30, cat: 'Analytics',        tag: 'campaign-reporting-agent',   name: 'Build a campaign performance reporting agent', skills: ['data-analysis','summarization','rag'] },
  { id: 31, cat: 'Analytics',        tag: 'cohort-analysis',            name: 'Create a cohort analysis and segmentation pipeline', skills: ['data-analysis','audience-segmentation','reasoning'] },
  { id: 32, cat: 'Analytics',        tag: 'realtime-spend-optimization', name: 'Build a real-time ad spend optimization system', skills: ['data-analysis','bid-optimization','audit-logging'] },
  { id: 33, cat: 'Analytics',        tag: 'funnel-dropoff-agent',       name: 'Create a funnel drop-off analysis agent', skills: ['data-analysis','reasoning','rag'] },
  // Category 6 — Content & SEO
  { id: 34, cat: 'Content & SEO',    tag: 'content-calendar-agent',     name: 'Build a content calendar generation agent', skills: ['rag','summarization','reasoning'] },
  { id: 35, cat: 'Content & SEO',    tag: 'seo-brief-generator',        name: 'Create an SEO content brief generator', skills: ['rag','web-search','summarization'] },
  { id: 36, cat: 'Content & SEO',    tag: 'content-gap-agent',          name: 'Build a competitor content gap analysis agent', skills: ['web-search','rag','reasoning'] },
  { id: 37, cat: 'Content & SEO',    tag: 'blog-optimization-agent',    name: 'Create a blog post optimization agent', skills: ['rag','summarization','code-generation'] },
  { id: 38, cat: 'Content & SEO',    tag: 'email-sequence-generator',   name: 'Build an email sequence generator', skills: ['summarization','rag','intent-classification'] },
  { id: 39, cat: 'Content & SEO',    tag: 'content-repurposing-agent',  name: 'Create a social media content repurposing agent', skills: ['summarization','intent-classification','code-generation'] },
  // Category 7 — Acquisition & Retention
  { id: 40, cat: 'Acquisition',      tag: 'lead-scoring-agent',         name: 'Build a lead scoring and qualification agent', skills: ['intent-classification','data-analysis','reasoning'] },
  { id: 41, cat: 'Acquisition',      tag: 'churn-prevention-system',    name: 'Create a churn prediction and prevention system', skills: ['data-analysis','reasoning','rag'] },
  { id: 42, cat: 'Acquisition',      tag: 'plg-activation-agent',       name: 'Build a product-led growth (PLG) activation agent', skills: ['intent-classification','reasoning','multi-agent-orchestration'] },
  { id: 43, cat: 'Acquisition',      tag: 'referral-optimization',      name: 'Create a referral program optimization agent', skills: ['data-analysis','reasoning','audit-logging'] },
  { id: 44, cat: 'Acquisition',      tag: 'onboarding-optimization',    name: 'Build an onboarding sequence optimization agent', skills: ['intent-classification','rag','memory-injection'] },
  { id: 45, cat: 'Acquisition',      tag: 'win-back-campaign-agent',    name: 'Create a win-back campaign automation agent', skills: ['intent-classification','summarization','data-analysis'] },
  // Category 8 — Strategy
  { id: 46, cat: 'Strategy',         tag: 'competitor-ad-intel',        name: 'Build a competitor ad intelligence agent', skills: ['web-search','rag','summarization'] },
  { id: 47, cat: 'Strategy',         tag: 'market-positioning-agent',   name: 'Create a market positioning analysis agent', skills: ['rag','reasoning','web-search'] },
  { id: 48, cat: 'Strategy',         tag: 'gtm-strategy-generator',     name: 'Build a GTM (go-to-market) strategy generator', skills: ['rag','reasoning','summarization'] },
  { id: 49, cat: 'Strategy',         tag: 'media-mix-modeling',         name: 'Create a media mix modeling agent', skills: ['data-analysis','reasoning','rag'] },
  { id: 50, cat: 'Strategy',         tag: 'marketing-benchmarking',     name: 'Build a marketing performance benchmarking agent', skills: ['data-analysis','web-search','rag'] },
];

// ============================================================
// BLUEPRINT ENGINE
// ============================================================

const AGENT_TEAMS = {
  'Paid Social':    [ { name: 'Campaign Orchestrator', role: 'Supervisor / Planner',       skills: ['multi-agent-orchestration','task-decomposition','planning'] },
                      { name: 'Audience Analyst',      role: 'Audience Specialist',         skills: ['audience-segmentation','embedding-generation','data-analysis'] },
                      { name: 'Bidding Strategist',    role: 'Bid & Budget Specialist',     skills: ['bid-optimization','data-analysis','reasoning'] } ],
  'Creative':       [ { name: 'Creative Director',     role: 'Creative Lead',               skills: ['creative-testing','summarization','reasoning'] },
                      { name: 'Copy Generator',        role: 'Content Specialist',          skills: ['code-generation','summarization','intent-classification'] },
                      { name: 'Performance Analyst',   role: 'Measurement Specialist',      skills: ['data-analysis','audit-logging','rag'] } ],
  'Landing Page':   [ { name: 'CRO Auditor',           role: 'Conversion Specialist',       skills: ['reasoning','rag','data-analysis'] },
                      { name: 'Copy Optimizer',        role: 'Content Specialist',          skills: ['summarization','creative-testing','code-generation'] },
                      { name: 'UX Analyst',            role: 'Experience Analyst',          skills: ['reasoning','audit-logging','data-analysis'] } ],
  'Agent Teams':    [ { name: 'Orchestrator',          role: 'Supervisor',                  skills: ['multi-agent-orchestration','task-decomposition','handoff'] },
                      { name: 'Specialist Agent A',    role: 'Domain Expert',               skills: ['reasoning','rag','summarization'] },
                      { name: 'Evaluator Agent',       role: 'Quality Controller',          skills: ['reflection','audit-logging','consensus'] } ],
  'Analytics':      [ { name: 'Data Analyst',          role: 'Analytics Lead',              skills: ['data-analysis','reasoning','audit-logging'] },
                      { name: 'Attribution Modeler',   role: 'Attribution Specialist',      skills: ['data-analysis','rag','reasoning'] },
                      { name: 'Report Generator',      role: 'Reporting Specialist',        skills: ['summarization','rag','data-analysis'] } ],
  'Content & SEO':  [ { name: 'Content Strategist',    role: 'Strategy Lead',               skills: ['rag','reasoning','web-search'] },
                      { name: 'SEO Writer',            role: 'Content Specialist',          skills: ['summarization','rag','code-generation'] },
                      { name: 'Gap Analyst',           role: 'Competitive Analyst',         skills: ['web-search','rag','reasoning'] } ],
  'Acquisition':    [ { name: 'Growth Lead',           role: 'Acquisition Strategist',      skills: ['reasoning','data-analysis','multi-agent-orchestration'] },
                      { name: 'Intent Classifier',     role: 'Lead Scoring Specialist',     skills: ['intent-classification','data-analysis','rag'] },
                      { name: 'Retention Agent',       role: 'Retention Specialist',        skills: ['memory-injection','rag','summarization'] } ],
  'Strategy':       [ { name: 'Strategy Analyst',      role: 'Strategic Lead',              skills: ['reasoning','rag','web-search'] },
                      { name: 'Intel Agent',           role: 'Competitive Intelligence',    skills: ['web-search','rag','summarization'] },
                      { name: 'GTM Planner',           role: 'Go-To-Market Specialist',     skills: ['reasoning','summarization','task-decomposition'] } ],
};

const KPI_MAP = {
  'Paid Social':   [ { label: 'Primary KPI',   value: 'ROAS ≥ 3.0×' },    { label: 'Target CPA',     value: '< $45' },
                     { label: 'CTR Benchmark', value: '≥ 1.5%' },          { label: 'CPM Target',     value: '< $12' } ],
  'Creative':      [ { label: 'Primary KPI',   value: 'CTR lift ≥ 20%' },  { label: 'Hook Rate',      value: '≥ 40% 3-sec view' },
                     { label: 'Test Duration', value: '7–14 days' },        { label: 'Sig. Threshold', value: '95% confidence' } ],
  'Landing Page':  [ { label: 'Primary KPI',   value: 'CVR ≥ 3.5%' },      { label: 'Bounce Rate',    value: '< 55%' },
                     { label: 'Time on Page',  value: '≥ 90 sec' },         { label: 'CTA Click Rate', value: '≥ 8%' } ],
  'Agent Teams':   [ { label: 'Agents Deployed', value: '3–5 specialists' },{ label: 'Orchestration', value: 'Supervisor pattern' },
                     { label: 'Handoff Protocol', value: 'Typed envelope' },  { label: 'Eval Loop',     value: 'Built-in reflector' } ],
  'Analytics':     [ { label: 'Attribution',   value: 'Last-touch + MTA' }, { label: 'LTV Target',     value: '> 3× CAC' },
                     { label: 'Report Cadence', value: 'Weekly + monthly' }, { label: 'Accuracy',       value: '≥ 90% model' } ],
  'Content & SEO': [ { label: 'Organic Traffic', value: '+30% in 90 days' },{ label: 'Keyword Rank',   value: 'Top 10 for 5+ terms' },
                     { label: 'Content Velocity', value: '4 posts/week' },   { label: 'Engagement',    value: '≥ 3% avg. rate' } ],
  'Acquisition':   [ { label: 'Primary KPI',   value: 'CAC < $80' },        { label: 'Activation Rate', value: '≥ 40%' },
                     { label: 'Churn Rate',     value: '< 5%/month' },       { label: 'LTV:CAC',        value: '≥ 3:1' } ],
  'Strategy':      [ { label: 'Primary KPI',   value: 'Market share +5%' }, { label: 'Intel Coverage', value: '5+ competitors' },
                     { label: 'GTM Timeline',   value: '30–90 days' },       { label: 'Win Rate',       value: '≥ 35%' } ],
};

const TIMELINE_MAP = {
  'Paid Social':   [ { label: 'Setup', days: 'Days 1–3' }, { label: 'Launch', days: 'Days 4–7' }, { label: 'Optimize', days: 'Days 8–21' }, { label: 'Scale', days: 'Days 22–30' } ],
  'Creative':      [ { label: 'Brief', days: 'Days 1–2' }, { label: 'Produce', days: 'Days 3–7' }, { label: 'Test', days: 'Days 8–21' }, { label: 'Promote', days: 'Days 22–30' } ],
  'Landing Page':  [ { label: 'Audit', days: 'Days 1–2' }, { label: 'Fix', days: 'Days 3–5' }, { label: 'Test', days: 'Days 6–21' }, { label: 'Report', days: 'Days 22–30' } ],
  'Agent Teams':   [ { label: 'Design', days: 'Days 1–3' }, { label: 'Build', days: 'Days 4–10' }, { label: 'Test', days: 'Days 11–20' }, { label: 'Deploy', days: 'Days 21–30' } ],
  'Analytics':     [ { label: 'Instrument', days: 'Days 1–5' }, { label: 'Collect', days: 'Days 6–14' }, { label: 'Model', days: 'Days 15–22' }, { label: 'Report', days: 'Days 23–30' } ],
  'Content & SEO': [ { label: 'Audit', days: 'Days 1–3' }, { label: 'Brief', days: 'Days 4–7' }, { label: 'Produce', days: 'Days 8–20' }, { label: 'Publish', days: 'Days 21–30' } ],
  'Acquisition':   [ { label: 'Baseline', days: 'Days 1–3' }, { label: 'Launch', days: 'Days 4–7' }, { label: 'Nurture', days: 'Days 8–21' }, { label: 'Retain', days: 'Days 22–30' } ],
  'Strategy':      [ { label: 'Intel', days: 'Days 1–5' }, { label: 'Position', days: 'Days 6–12' }, { label: 'GTM Plan', days: 'Days 13–21' }, { label: 'Execute', days: 'Days 22–30' } ],
};

// ============================================================
// RENDER FUNCTIONS
// ============================================================

function renderGoals(list) {
  const grid = document.getElementById('goals-grid');
  grid.innerHTML = '';
  if (!list.length) {
    grid.innerHTML = '<p style="padding:var(--space-6);color:var(--text-muted);font-size:var(--text-sm);text-align:center">No goals match your search.</p>';
    return;
  }
  list.forEach(goal => {
    const el = document.createElement('div');
    el.className = 'goal-item';
    el.setAttribute('role', 'listitem');
    el.setAttribute('tabindex', '0');
    el.dataset.id = goal.id;
    el.innerHTML = `
      <span class="goal-num">${String(goal.id).padStart(2,'0')}</span>
      <div class="goal-body">
        <div class="goal-name">${goal.name}</div>
        <div class="goal-cat">${goal.cat}</div>
      </div>`;
    el.addEventListener('click', () => selectGoal(goal));
    el.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectGoal(goal); } });
    grid.appendChild(el);
  });
}

function renderCategoryFilters() {
  const cats = ['All', ...new Set(GOALS.map(g => g.cat))];
  const container = document.getElementById('category-filters');
  cats.forEach(cat => {
    const btn = document.createElement('button');
    btn.className = 'cat-btn' + (cat === 'All' ? ' active' : '');
    btn.textContent = cat;
    btn.type = 'button';
    btn.addEventListener('click', () => {
      document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filterGoals();
    });
    container.appendChild(btn);
  });
}

function filterGoals() {
  const query = document.getElementById('goal-search').value.toLowerCase();
  const activeCat = document.querySelector('.cat-btn.active')?.textContent;
  const filtered = GOALS.filter(g => {
    const matchCat = activeCat === 'All' || g.cat === activeCat;
    const matchSearch = !query || g.name.toLowerCase().includes(query) || g.cat.toLowerCase().includes(query);
    return matchCat && matchSearch;
  });
  renderGoals(filtered);
}

function generateBlueprint(goal) {
  const agents = AGENT_TEAMS[goal.cat] || AGENT_TEAMS['Strategy'];
  const kpis   = KPI_MAP[goal.cat]    || KPI_MAP['Strategy'];
  const timeline = TIMELINE_MAP[goal.cat] || TIMELINE_MAP['Strategy'];

  const agentsHTML = agents.map(a => `
    <div class="agent-card">
      <div class="agent-name">${a.name}</div>
      <div class="agent-role">${a.role}</div>
      <div class="agent-skills">${a.skills.map(s => `<span class="skill-chip">${s}</span>`).join('')}</div>
    </div>`).join('');

  const kpisHTML = `<div class="kpi-grid">${kpis.map(k => `
    <div class="kpi-item">
      <div class="kpi-label">${k.label}</div>
      <div class="kpi-value">${k.value}</div>
    </div>`).join('')}</div>`;

  const timelineHTML = `<div class="timeline-bar">${timeline.map(p => `
    <div class="timeline-phase">
      <span class="phase-label">${p.label}</span>
      <span class="phase-days">${p.days}</span>
    </div>`).join('')}</div>`;

  const requiredSkillsHTML = `<div class="agent-skills" style="flex-wrap:wrap">${
    goal.skills.map(s => `<span class="skill-chip">${s}</span>`).join('')
  }</div>`;

  return `
    <div class="bp-header">
      <div class="bp-goal-title">${goal.name}</div>
      <span class="bp-category">${goal.cat}</span>
    </div>
    <div class="bp-section">
      <div class="bp-section-title">AI Agent Team</div>
      ${agentsHTML}
    </div>
    <div class="bp-section">
      <div class="bp-section-title">Required AI Skills</div>
      ${requiredSkillsHTML}
    </div>
    <div class="bp-section">
      <div class="bp-section-title">KPI Targets</div>
      ${kpisHTML}
    </div>
    <div class="bp-section">
      <div class="bp-section-title">30-Day Execution Timeline</div>
      ${timelineHTML}
    </div>`;
}

function selectGoal(goal) {
  document.querySelectorAll('.goal-item').forEach(el => el.classList.remove('selected'));
  const el = document.querySelector(`.goal-item[data-id="${goal.id}"]`);
  if (el) el.classList.add('selected');

  const empty  = document.getElementById('blueprint-empty');
  const output = document.getElementById('blueprint-output');
  const actions = document.getElementById('blueprint-actions');

  empty.style.display  = 'none';
  output.style.display = 'block';
  actions.style.display = 'flex';

  output.innerHTML = generateBlueprint(goal);
  output.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

  console.info('MARKETING OS: Blueprint generated for goal', goal.id, '—', goal.name);
}

// ============================================================
// INIT
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  console.info('MARKETING AI OS — Initiative INITIATIVE-020');
  console.info('GOALS:', GOALS.length);

  renderCategoryFilters();
  renderGoals(GOALS);

  document.getElementById('goal-search').addEventListener('input', filterGoals);

  document.getElementById('btn-copy')?.addEventListener('click', () => {
    const output = document.getElementById('blueprint-output');
    const text = output ? output.innerText : '';
    navigator.clipboard.writeText(text).then(() => {
      const btn = document.getElementById('btn-copy');
      btn.textContent = 'Copied!';
      setTimeout(() => { btn.textContent = 'Copy'; }, 1800);
    }).catch(() => {});
  });

  document.getElementById('btn-reset')?.addEventListener('click', () => {
    document.querySelectorAll('.goal-item').forEach(el => el.classList.remove('selected'));
    document.getElementById('blueprint-empty').style.display  = 'flex';
    document.getElementById('blueprint-output').style.display = 'none';
    document.getElementById('blueprint-actions').style.display = 'none';
  });
});
