/* Blueprint Generator app.js
 * Initiative: INITIATIVE-012C
 * No backend. No AI inference. Pure graph evidence.
 * schema_version: 3.1 | Goals: 25
 */

const GOALS = [
  {id:"customer-support-agent",title:"AI Customer Support Agent",desc:"An agent that handles customer inquiries, resolves tickets, and escalates edge cases automatically.",categories:["09-agentic-patterns","07-tool-use","06-communication","03-memory"],keywords:["support","customer","ticket","chat","helpdesk","escalation","faq"]},
  {id:"rag-assistant",title:"RAG Assistant",desc:"Retrieval-augmented assistant that answers questions grounded in a private document corpus.",categories:["09-agentic-patterns","03-memory","07-tool-use","01-perception"],keywords:["rag","retrieval","documents","knowledge","qa","search","vector","embedding"]},
  {id:"research-agent",title:"Research Agent",desc:"Autonomous agent that searches, synthesizes, and summarizes information from the web and internal sources.",categories:["09-agentic-patterns","11-web","07-tool-use","02-reasoning","06-communication"],keywords:["research","search","web","synthesis","report","literature","analysis"]},
  {id:"coding-agent",title:"Coding Agent",desc:"Agent that writes, reviews, debugs, and deploys code based on natural language specifications.",categories:["05-code","09-agentic-patterns","07-tool-use","02-reasoning"],keywords:["code","coding","programming","development","software","debug","refactor","test"]},
  {id:"autonomous-browser-agent",title:"Autonomous Browser Agent",desc:"Agent that navigates websites, fills forms, extracts data, and completes web-based tasks autonomously.",categories:["10-computer-use","11-web","09-agentic-patterns","07-tool-use"],keywords:["browser","web","automation","scraping","navigation","form","click","selenium","playwright"]},
  {id:"document-intelligence",title:"Document Intelligence System",desc:"System that ingests, classifies, extracts structured data from, and routes documents of all types.",categories:["01-perception","09-agentic-patterns","02-reasoning","06-communication"],keywords:["document","ocr","extraction","pdf","parsing","classification","invoice","contract"]},
  {id:"voice-agent",title:"Voice Agent",desc:"End-to-end voice-enabled agent with speech-to-text, reasoning, and text-to-speech response pipeline.",categories:["08-multimodal","09-agentic-patterns","07-tool-use","06-communication"],keywords:["voice","speech","audio","tts","stt","transcription","spoken","conversation"]},
  {id:"multi-agent-team",title:"Multi-Agent Team",desc:"Orchestrated team of specialized agents collaborating to solve complex multi-step problems.",categories:["09-agentic-patterns","07-tool-use","02-reasoning","06-communication"],keywords:["multi-agent","orchestration","team","collaboration","swarm","delegation","coordinator"]},
  {id:"data-analyst-agent",title:"Data Analyst Agent",desc:"Agent that loads datasets, runs statistical analyses, generates visualizations, and produces insights.",categories:["05-code","02-reasoning","08-multimodal","07-tool-use"],keywords:["data","analysis","statistics","chart","visualization","pandas","sql","jupyter","analytics"]},
  {id:"evaluation-pipeline",title:"Evaluation Pipeline",desc:"Automated pipeline for evaluating LLM outputs using rubrics, benchmarks, and human-feedback loops.",categories:["09-agentic-patterns","05-code","02-reasoning","07-tool-use"],keywords:["eval","evaluation","benchmark","testing","scoring","llm","quality","metrics","grading"]},
  {id:"workflow-automation",title:"Workflow Automation Agent",desc:"Agent that maps, automates, and monitors business workflows across SaaS tools and internal systems.",categories:["07-tool-use","09-agentic-patterns","04-action-execution","02-reasoning"],keywords:["workflow","automation","zapier","n8n","integration","trigger","pipeline","process","bpm"]},
  {id:"knowledge-management",title:"Knowledge Management Agent",desc:"Agent that captures, organizes, retrieves, and surfaces institutional knowledge from diverse sources.",categories:["03-memory","09-agentic-patterns","01-perception","07-tool-use"],keywords:["knowledge","wiki","notion","documentation","memory","organization","taxonomy","ontology"]},
  {id:"code-review-agent",title:"Code Review Agent",desc:"Automated agent that performs security, style, logic, and performance reviews on pull requests.",categories:["05-code","09-agentic-patterns","02-reasoning","07-tool-use"],keywords:["code","review","pull request","security","lint","bug","quality","github","static analysis"]},
  {id:"sales-copilot",title:"Sales Copilot",desc:"AI assistant that supports sales reps with prospect research, email drafting, CRM updates, and deal coaching.",categories:["09-agentic-patterns","07-tool-use","06-communication","11-web"],keywords:["sales","crm","prospecting","email","deal","outreach","linkedin","hubspot","salesforce"]},
  {id:"executive-assistant",title:"Executive Assistant Agent",desc:"AI agent that manages calendars, emails, meeting prep, and action items for executives.",categories:["07-tool-use","04-action-execution","06-communication","09-agentic-patterns"],keywords:["calendar","email","meeting","schedule","assistant","executive","task","follow-up","slack"]},
  {id:"security-scanner",title:"Security Scanning Agent",desc:"Agent that audits codebases, APIs, and infrastructure for vulnerabilities and generates remediation plans.",categories:["05-code","09-agentic-patterns","11-web","02-reasoning"],keywords:["security","vulnerability","owasp","scanning","audit","pentest","cve","sast","dast"]},
  {id:"writing-assistant",title:"Technical Writing Assistant",desc:"Agent that drafts, edits, and formats technical documentation, API docs, and user guides.",categories:["06-communication","05-code","09-agentic-patterns","02-reasoning"],keywords:["writing","documentation","docs","api","technical","guide","tutorial","editing","content"]},
  {id:"monitoring-agent",title:"Infrastructure Monitoring Agent",desc:"Autonomous agent that monitors system health, detects anomalies, and triggers remediation workflows.",categories:["07-tool-use","04-action-execution","09-agentic-patterns","01-perception"],keywords:["monitoring","observability","alerts","metrics","logs","infrastructure","devops","prometheus","grafana"]},
  {id:"personalization-engine",title:"Personalization Engine",desc:"System that builds user profiles and delivers personalized recommendations across surfaces.",categories:["03-memory","09-agentic-patterns","02-reasoning","07-tool-use"],keywords:["personalization","recommendation","user","profile","collaborative filtering","content","ranking"]},
  {id:"contract-analyst",title:"Contract Analysis Agent",desc:"Agent that reads, summarizes, extracts clauses, and flags risks in legal contracts.",categories:["01-perception","02-reasoning","06-communication","09-agentic-patterns"],keywords:["contract","legal","clause","risk","document","nda","agreement","compliance","review"]},
  {id:"financial-analyst",title:"Financial Analysis Agent",desc:"Agent that ingests financial data, runs models, and produces investment or business analysis reports.",categories:["02-reasoning","05-code","07-tool-use","06-communication"],keywords:["finance","financial","investment","analysis","model","excel","data","forecast","accounting"]},
  {id:"content-creator",title:"Content Creation Agent",desc:"Agent that researches, outlines, drafts, and optimizes content for blogs, social media, and marketing.",categories:["06-communication","11-web","09-agentic-patterns","07-tool-use"],keywords:["content","blog","social","seo","marketing","writing","copywriting","brand","campaign"]},
  {id:"testing-agent",title:"Automated Testing Agent",desc:"Agent that generates test suites, runs them, interprets failures, and patches the code automatically.",categories:["05-code","09-agentic-patterns","07-tool-use","02-reasoning"],keywords:["testing","test","qa","unit","integration","coverage","automation","ci","regression"]},
  {id:"data-pipeline-agent",title:"Data Pipeline Agent",desc:"Agent that designs, builds, monitors, and repairs ETL/ELT data pipelines automatically.",categories:["05-code","07-tool-use","04-action-execution","09-agentic-patterns"],keywords:["etl","pipeline","data","ingestion","transformation","airflow","dbt","spark","warehouse"]},
  {id:"customer-onboarding",title:"Customer Onboarding Agent",desc:"Guided agent that walks new users through product setup, configuration, and first value moment.",categories:["06-communication","09-agentic-patterns","07-tool-use","03-memory"],keywords:["onboarding","setup","guide","tutorial","user","product","activation","welcome"]}
];

const CAT_NAMES = {
  "00-sandbox":"Sandbox","01-perception":"Perception","02-reasoning":"Reasoning",
  "03-memory":"Memory","04-action-execution":"Action","05-code":"Code",
  "06-communication":"Communication","07-tool-use":"Tools","08-multimodal":"Multimodal",
  "09-agentic-patterns":"Agentic Patterns","10-computer-use":"Computer Use","11-web":"Web"
};

const CAT_ORDER = [
  "01-perception","02-reasoning","03-memory","04-action-execution",
  "05-code","06-communication","07-tool-use","08-multimodal",
  "09-agentic-patterns","10-computer-use","11-web"
];

let graphData = null;
let nodeMap = null;
let currentBlueprint = null;
let activeGoalId = null;

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  renderGoalList(GOALS);
  setupSearch();
  setupExampleBtns();
  loadGraph();
  checkDeepLink();
});

function initTheme() {
  const toggle = document.querySelector("[data-theme-toggle]");
  const root = document.documentElement;
  const isDark = matchMedia("(prefers-color-scheme: dark)").matches;
  root.setAttribute("data-theme", isDark ? "dark" : "light");
  if (!toggle) return;
  toggle.addEventListener("click", () => {
    const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    toggle.innerHTML = next === "dark"
      ? `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`
      : `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>`;
  });
}

function loadGraph() {
  fetch("../../data/SKILLS_GRAPH.json")
    .then(r => r.json())
    .then(data => {
      graphData = data;
      nodeMap = {};
      for (const node of data.nodes) nodeMap[node.id] = node;
    })
    .catch(() => { /* graceful degradation — catalog data is sufficient */ });
}

function checkDeepLink() {
  const params = new URLSearchParams(location.search);
  const goalId = params.get("goal");
  if (goalId) {
    const goal = GOALS.find(g => g.id === goalId);
    if (goal) setTimeout(() => selectGoal(goal), 200);
  }
}

function renderGoalList(goals) {
  const list = document.getElementById("goalList");
  if (!list) return;
  list.innerHTML = "";
  if (!goals.length) {
    list.innerHTML = `<li style="padding:1rem;color:var(--color-text-faint);font-size:.875rem;text-align:center">No goals match</li>`;
    return;
  }
  for (const goal of goals) {
    const li = document.createElement("li");
    li.className = "goal-item" + (goal.id === activeGoalId ? " active" : "");
    li.setAttribute("role", "button");
    li.setAttribute("tabindex", "0");
    li.dataset.id = goal.id;
    li.innerHTML = `
      <div class="goal-title">${goal.title}</div>
      <div class="goal-cats">${goal.categories.slice(0,3).map(c => CAT_NAMES[c] || c).join(" · ")}</div>
    `;
    li.addEventListener("click", () => selectGoal(goal));
    li.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") selectGoal(goal); });
    list.appendChild(li);
  }
}

function setupSearch() {
  const input = document.getElementById("goalSearch");
  if (!input) return;
  input.addEventListener("input", () => {
    const q = input.value.toLowerCase().trim();
    if (!q) { renderGoalList(GOALS); return; }
    const filtered = GOALS.filter(g =>
      g.title.toLowerCase().includes(q) ||
      g.keywords.some(k => k.includes(q)) ||
      g.categories.some(c => (CAT_NAMES[c]||c).toLowerCase().includes(q))
    );
    renderGoalList(filtered);
  });
}

function setupExampleBtns() {
  document.querySelectorAll(".example-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const g = GOALS.find(x => x.id === btn.dataset.goal);
      if (g) selectGoal(g);
    });
  });
  const shareBtn = document.getElementById("shareBtn");
  const jsonBtn = document.getElementById("exportJsonBtn");
  const mdBtn = document.getElementById("exportMdBtn");
  if (shareBtn) shareBtn.addEventListener("click", shareBlueprint);
  if (jsonBtn) jsonBtn.addEventListener("click", exportJson);
  if (mdBtn) mdBtn.addEventListener("click", exportMarkdown);
}

function selectGoal(goal) {
  activeGoalId = goal.id;
  const url = new URL(location.href);
  url.searchParams.set("goal", goal.id);
  history.pushState({}, "", url.toString());
  document.querySelectorAll(".goal-item").forEach(el => {
    el.classList.toggle("active", el.dataset.id === goal.id);
  });
  currentBlueprint = generateBlueprint(goal);
  renderBlueprint(currentBlueprint);
  if (window.innerWidth <= 900) {
    document.getElementById("blueprintOutput").scrollIntoView({behavior:"smooth",block:"start"});
  }
}

function generateBlueprint(goal) {
  const skills = [];
  const skillIds = new Set();
  if (graphData) {
    for (const node of graphData.nodes) {
      if (node.category === "00-sandbox") continue;
      if (goal.categories.includes(node.category)) {
        if (!skillIds.has(node.id)) {
          skillIds.add(node.id);
          skills.push({id:node.id,title:node.title,category:node.category,level:node.level,stability:node.stability,reason:reasonForSkill(node,goal)});
        }
        for (const prereqId of (node.prerequisites||[])) {
          if (!skillIds.has(prereqId) && nodeMap && nodeMap[prereqId] && nodeMap[prereqId].category !== "00-sandbox") {
            skillIds.add(prereqId);
            const p = nodeMap[prereqId];
            skills.push({id:p.id,title:p.title,category:p.category,level:p.level,stability:p.stability,reason:"Prerequisite"});
          }
        }
      }
    }
  }
  const lw = {basic:0,intermediate:1,advanced:2};
  skills.sort((a,b) => {
    const ca = CAT_ORDER.indexOf(a.category), cb = CAT_ORDER.indexOf(b.category);
    return ca !== cb ? ca - cb : (lw[a.level]||0) - (lw[b.level]||0);
  });
  const learningPath = buildLearningPath(skills);
  const advCount = skills.filter(s => s.level === "advanced").length;
  const totalW = skills.reduce((a,s) => a + ({basic:0.5,intermediate:1,advanced:2}[s.level]||1), 0);
  const difficulty = advCount > skills.length*0.4 ? "advanced" : advCount > skills.length*0.15 ? "intermediate" : "beginner";
  const weeks = Math.max(2, Math.round(totalW * 0.8));
  const categories = [...new Set(skills.map(s => s.category))].sort((a,b) => CAT_ORDER.indexOf(a)-CAT_ORDER.indexOf(b));
  return {id:goal.id,goal:goal.title,summary:goal.desc,skills,learningPath,categories,difficulty,estimatedTime:`${Math.max(2,weeks-1)}–${weeks+2} weeks`,version:"1.0",generatedAt:new Date().toISOString()};
}

function reasonForSkill(node, goal) {
  if (goal.categories[0] === node.category) return "Core skill for this goal";
  if (goal.categories[1] === node.category) return "Supporting capability";
  return "Required for full implementation";
}

function buildLearningPath(skills) {
  const phases = {};
  for (const skill of skills) {
    const ph = CAT_ORDER.indexOf(skill.category);
    const key = ph >= 0 ? ph : 99;
    if (!phases[key]) phases[key] = [];
    phases[key].push(skill);
  }
  const result = [];
  for (const key of Object.keys(phases).map(Number).sort((a,b)=>a-b)) {
    const g = phases[key];
    const basic = g.filter(s=>s.level==="basic");
    const inter = g.filter(s=>s.level==="intermediate");
    const adv = g.filter(s=>s.level==="advanced");
    if (basic.length) result.push(basic);
    if (inter.length) result.push(inter);
    if (adv.length) result.push(adv);
  }
  const merged = [];
  let i = 0;
  while (i < result.length) {
    if (result[i].length < 2 && i+1 < result.length) { merged.push([...result[i],...result[i+1]]); i+=2; }
    else { merged.push(result[i]); i++; }
  }
  return merged;
}

function renderBlueprint(bp) {
  document.getElementById("emptyState").classList.add("hidden");
  document.getElementById("blueprintCard").classList.remove("hidden");
  document.getElementById("bpTitle").textContent = bp.goal;
  document.getElementById("bpSummary").textContent = bp.summary;
  const diffEl = document.getElementById("bpDifficulty");
  diffEl.textContent = bp.difficulty.charAt(0).toUpperCase()+bp.difficulty.slice(1);
  diffEl.className = `meta-chip difficulty-${bp.difficulty}`;
  document.getElementById("bpTime").textContent = "⏱ " + bp.estimatedTime;
  document.getElementById("bpSkillCount").textContent = bp.skills.length + " skills";
  document.getElementById("skillCountHint").textContent = `${bp.skills.length} skills across ${bp.categories.length} categories`;

  const lpEl = document.getElementById("learningPath");
  lpEl.innerHTML = "";
  bp.learningPath.forEach((phase, i) => {
    const div = document.createElement("div");
    div.className = "lp-phase";
    div.innerHTML = `<div class="phase-num">${i+1}</div><div class="phase-skills">${phase.map(s=>`<span class="phase-skill" title="${s.category}">${s.title}</span>`).join("")}</div>`;
    lpEl.appendChild(div);
  });

  document.getElementById("skillGrid").innerHTML = bp.skills.slice(0,30).map(s=>`
    <div class="skill-card">
      <div class="skill-card-header">
        <div class="skill-name">${s.title}</div>
        <span class="skill-level level-${s.level}">${s.level}</span>
      </div>
      <div class="skill-cat">${s.category}</div>
      ${s.reason !== "Prerequisite" ? `<div class="skill-reason">${s.reason}</div>` : ""}
    </div>
  `).join("") + (bp.skills.length > 30 ? `<div class="skill-card" style="display:flex;align-items:center;justify-content:center;color:var(--color-text-faint);font-size:.875rem">+${bp.skills.length-30} more skills</div>` : "");

  document.getElementById("categoryList").innerHTML = bp.categories.map(c=>`<span class="cat-chip">${CAT_NAMES[c]||c}</span>`).join("");
}

function exportJson() {
  if (!currentBlueprint) return;
  const blob = new Blob([JSON.stringify(currentBlueprint,null,2)],{type:"application/json"});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `blueprint-${currentBlueprint.id}.json`; a.click(); URL.revokeObjectURL(a.href);
  showToast("Blueprint JSON downloaded");
}

function exportMarkdown() {
  if (!currentBlueprint) return;
  const bp = currentBlueprint;
  let md = `# Blueprint: ${bp.goal}\n\n> Generated: ${bp.generatedAt.slice(0,10)} | Skills Tree v${bp.version}\n\n## Summary\n\n${bp.summary}\n\n**Difficulty:** ${bp.difficulty} | **Estimated Time:** ${bp.estimatedTime} | **Skills:** ${bp.skills.length}\n\n## Learning Path\n\n`;
  bp.learningPath.forEach((phase,i) => { md += `### Phase ${i+1}\n\n`; phase.forEach(s => { md += `- **${s.title}** (\`${s.id}\`) — ${s.level}\n`; }); md += "\n"; });
  md += `## Required Skills (${bp.skills.length})\n\n| Skill | Category | Level | Stability |\n|-------|----------|-------|----------|\n`;
  bp.skills.forEach(s => { md += `| ${s.title} | ${CAT_NAMES[s.category]||s.category} | ${s.level} | ${s.stability} |\n`; });
  md += `\n## Categories\n\n${bp.categories.map(c=>`- ${CAT_NAMES[c]||c}`).join("\n")}\n\n---\n\n*Generated by [Skills Tree Blueprint Generator](https://samotech.github.io/skills-tree/blueprints/)*\n`;
  const blob = new Blob([md],{type:"text/markdown"});
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `blueprint-${bp.id}.md`; a.click(); URL.revokeObjectURL(a.href);
  showToast("Blueprint Markdown downloaded");
}

function shareBlueprint() {
  const url = new URL(location.href);
  if (currentBlueprint) url.searchParams.set("goal", currentBlueprint.id);
  navigator.clipboard.writeText(url.toString()).then(()=>showToast("Share URL copied")).catch(()=>showToast("URL: "+url.toString()));
}

let toastTimer = null;
function showToast(msg) {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.remove("hidden");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.add("hidden"), 2500);
}
