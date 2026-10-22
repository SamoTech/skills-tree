    ]
  },
  "drifted": [
    {
      "package": "agentic-payment-protocol-selection-reasoning",
      "reason": "content-differs-from-deterministic-projection",
      "source": "skills/02-reasoning/agentic-payment-protocol-selection-reasoning.md"
    }
  ],
  "eligible_missing": [],
  "existing_package_count": 1599,
  "extra": [
    {
      "description": "Query and consume the Skills Tree registry when an agent needs a canonical AI-skill definition, related capability, quality state, or machine-readable skill metadata.",
      "frontmatter_name": "skills-tree-registry",
      "package": "skills-tree-registry",
      "path": "agent-skills/skills-tree-registry/SKILL.md",
      "source": ""
    }
  ],
  "legacy_compatibility": [
    {
      "description": "Use GitHub REST APIs for bounded repository, issue, pull-request, and metadata operations with explicit scopes and verified mutations.",
      "expected_package": "tool-use-github-api",
      "frontmatter_name": "github-api",
      "match": "legacy-compatibility",
      "package": "github-api",
      "path": "agent-skills/github-api/SKILL.md",
      "source": "skills/07-tool-use/github-api.md"
    },
    {
      "description": "Transcribe speech audio into timestamped text while preserving uncertainty, speaker boundaries when available, and non-speech events.",
      "expected_package": "multimodal-audio-transcription",
      "frontmatter_name": "audio-transcription",
      "match": "legacy-compatibility",
      "package": "audio-transcription",
      "path": "agent-skills/audio-transcription/SKILL.md",
      "source": "skills/08-multimodal/audio-transcription.md"
    },
    {
      "description": "Ground generation with retrieved external context by separating ingestion, retrieval, context assembly, generation, and source attribution, with explicit handling for weak or conflicting retrieval.",
      "expected_package": "agentic-patterns-rag",
      "frontmatter_name": "rag",
      "match": "legacy-compatibility",
      "package": "rag",
      "path": "agent-skills/rag/SKILL.md",
      "source": "skills/09-agentic-patterns/rag.md"
    },
    {
      "description": "Interleave Thought \u2192 Action \u2192 Observation steps in a tool-calling loop until the agent declares Final Answer. The most-used reasoning-with-tools pattern.",
      "expected_package": "agentic-patterns-react",
      "frontmatter_name": "react",
      "match": "legacy-compatibility",
      "package": "react",
      "path": "agent-skills/react/SKILL.md",
      "source": "skills/09-agentic-patterns/react.md"
    },
    {
      "description": "Move a verified UI object from a source target to a destination target using controlled drag-and-drop.",
      "expected_package": "computer-use-drag-drop",
      "frontmatter_name": "drag-drop",
      "match": "legacy-compatibility",
      "package": "drag-drop",
      "path": "agent-skills/drag-drop/SKILL.md",
      "source": "skills/10-computer-use/drag-drop.md"
    },
    {
      "description": "Capture a screenshot of a verified screen or region for observation, evidence, or postcondition checking.",
      "expected_package": "computer-use-screenshot-capture",
      "frontmatter_name": "screenshot-capture",
      "match": "legacy-compatibility",
      "package": "screenshot-capture",
      "path": "agent-skills/screenshot-capture/SKILL.md",
      "source": "skills/10-computer-use/screenshot-capture.md"
    },
    {
      "description": "Scroll a verified UI container or viewport by a bounded amount and verify the resulting visible state.",
      "expected_package": "computer-use-scroll",
      "frontmatter_name": "scroll",
      "match": "legacy-compatibility",
      "package": "scroll",
      "path": "agent-skills/scroll/SKILL.md",
      "source": "skills/10-computer-use/scroll.md"
    },
    {
      "description": "Query a search API (Tavily, Serper, Bing, Brave, Exa) and return ranked URLs + snippets. The agent's bridge to fresh, open-web information when its training cutoff or private corpus isn't enough.",
      "expected_package": "web-web-search",
      "frontmatter_name": "web-search",
      "match": "legacy-compatibility",
      "package": "web-search",
      "path": "agent-skills/web-search/SKILL.md",
      "source": "skills/11-web/web-search.md"
    },
    {
      "description": "Generate testable hypotheses from observations, data, or documented literature gaps, with explicit falsifiability criteria and expected outcomes.",
      "expected_package": "domain-specific-hypothesis-generation",
      "frontmatter_name": "hypothesis-generation",
      "match": "legacy-compatibility",
      "package": "hypothesis-generation",
      "path": "agent-skills/hypothesis-generation/SKILL.md",
      "source": "skills/16-domain-specific/hypothesis-generation.md"
    },
    {
      "description": "Audit declared skill dependencies and executable examples in isolated environments, producing reproducible pass/fail evidence without silently promoting trust state.",
      "expected_package": "infrastructure-dependency-auditor",
      "frontmatter_name": "dependency-auditor",
      "match": "legacy-compatibility",
      "package": "dependency-auditor",
      "path": "agent-skills/dependency-auditor/SKILL.md",
      "source": "skills/17-infrastructure/dependency-auditor.md"
    }
  ],
  "matched_by_name_only": [],
  "matched_by_provenance": [
    {
      "expected_package": "a2a-agent-card-capability-parsing",
      "match": "provenance",
      "package": "a2a-agent-card-capability-parsing",
      "source": "skills/01-perception/a2a-agent-card-capability-parsing.md"
    },
    {
      "expected_package": "accessibility-tree-screenshot-fusion",
      "match": "provenance",
      "package": "accessibility-tree-screenshot-fusion",
      "source": "skills/01-perception/accessibility-tree-screenshot-fusion.md"
    },
    {
      "expected_package": "ag-ui-event-stream-parsing",
      "match": "provenance",
      "package": "ag-ui-event-stream-parsing",
      "source": "skills/01-perception/ag-ui-event-stream-parsing.md"
    },
    {
      "expected_package": "agent-card-parsing",
      "match": "provenance",
      "package": "agent-card-parsing",
      "source": "skills/01-perception/agent-card-parsing.md"
    },
    {
      "expected_package": "agent-eval-report-parsing",
      "match": "provenance",
      "package": "agent-eval-report-parsing",
      "source": "skills/01-perception/agent-eval-report-parsing.md"
    },
    {
      "expected_package": "agent-payment-protocol-message-parsing",
      "match": "provenance",
      "package": "agent-payment-protocol-message-parsing",
      "source": "skills/01-perception/agent-payment-protocol-message-parsing.md"
    },
    {
      "expected_package": "agent-protocol-message-envelope-parsing",
      "match": "provenance",
      "package": "agent-protocol-message-envelope-parsing",
      "source": "skills/01-perception/agent-protocol-message-envelope-parsing.md"
    },
    {
      "expected_package": "agent-runtime-action-event-parsing",
      "match": "provenance",
      "package": "agent-runtime-action-event-parsing",
      "source": "skills/01-perception/agent-runtime-action-event-parsing.md"
    },
    {
      "expected_package": "agent-screen-event-stream-parsing",
      "match": "provenance",
      "package": "agent-screen-event-stream-parsing",
      "source": "skills/01-perception/agent-screen-event-stream-parsing.md"
    },
    {
      "expected_package": "agent-trace-span-parsing",
      "match": "provenance",
      "package": "agent-trace-span-parsing",
      "source": "skills/01-perception/agent-trace-span-parsing.md"
    },
    {
      "expected_package": "agent-watcher-alert-stream-parsing",
      "match": "provenance",
      "package": "agent-watcher-alert-stream-parsing",
      "source": "skills/01-perception/agent-watcher-alert-stream-parsing.md"
    },
    {
      "expected_package": "agentic-payment-status-response-parsing",
      "match": "provenance",
      "package": "agentic-payment-status-response-parsing",
      "source": "skills/01-perception/agentic-payment-status-response-parsing.md"
    },
    {
      "expected_package": "api-response-parsing",
      "match": "provenance",
      "package": "api-response-parsing",
      "source": "skills/01-perception/api-response-parsing.md"
    },
    {
      "expected_package": "asr-hallucination-detection",
      "match": "provenance",
      "package": "asr-hallucination-detection",
      "source": "skills/01-perception/asr-hallucination-detection.md"
    },
    {
      "expected_package": "audio-stream-segmentation",
      "match": "provenance",
      "package": "audio-stream-segmentation",
      "source": "skills/01-perception/audio-stream-segmentation.md"

  "unresolved_collisions": {}
}Reconciliation check failed: drifted: 1

