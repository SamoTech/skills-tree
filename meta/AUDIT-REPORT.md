# PR #652 distribution-audit capture (temporary)

## generate_agent_skills.py --audit
~~~
    "skills/02-reasoning/tree-of-thought.md": [
      "missing Evidence section"
    ],
    "skills/02-reasoning/uncertainty-quantification.md": [
      "missing Evidence section"
    ],
    "skills/03-memory/cross-session-persistence.md": [
      "missing Evidence section"
    ],
    "skills/03-memory/episodic-memory.md": [
      "missing Evidence section"
    ],
    "skills/03-memory/forgetting.md": [
      "missing Evidence section"
    ],
    "skills/03-memory/long-term-memory.md": [
      "missing Evidence section"
    ],
    "skills/03-memory/memory-summarization.md": [
      "missing Evidence section"
    ],
    "skills/03-memory/procedural-memory.md": [
      "missing Evidence section"
    ],
    "skills/03-memory/semantic-memory.md": [
      "missing Evidence section"
    ],
    "skills/03-memory/user-profile-memory.md": [
      "missing Evidence section"
    ],
    "skills/07-tool-use/function-calling.md": [
      "missing Evidence section"
    ]
  },
  "eligible": 1561,
  "name_collisions": {
    "audio-transcription": [
      "skills/01-perception/audio-transcription.md",
      "skills/08-multimodal/audio-transcription.md"
    ],
    "dependency-auditor": [
      "skills/05-code/dependency-auditor.md",
      "skills/17-infrastructure/dependency-auditor.md"
    ],
    "drag-drop": [
      "skills/04-action-execution/drag-drop.md",
      "skills/10-computer-use/drag-drop.md"
    ],
    "github-api": [
      "skills/05-code/github-api.md",
      "skills/07-tool-use/github-api.md"
    ],
    "hypothesis-generation": [
      "skills/02-reasoning/hypothesis-generation.md",
      "skills/16-domain-specific/hypothesis-generation.md"
    ],
    "rag": [
      "skills/03-memory/rag.md",
      "skills/09-agentic-patterns/rag.md"
    ],
    "react": [
      "skills/02-reasoning/react.md",
      "skills/09-agentic-patterns/react.md"
    ],
    "screenshot-capture": [
      "skills/04-action-execution/screenshot-capture.md",
      "skills/10-computer-use/screenshot-capture.md"
    ],
    "scroll": [
      "skills/04-action-execution/scroll.md",
      "skills/10-computer-use/scroll.md"
    ],
    "web-search": [
      "skills/07-tool-use/web-search.md",
      "skills/11-web/web-search.md"
    ]
  },
  "source": "skills/",
  "total": 1589
}
exit=0
~~~

## validate_agent_skills.py
~~~
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/type-error-triage/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/ucp-universal-capability-protocol-usage/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/ui-element-waiting/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/ui-screencast-analysis/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/ui-video-tutorial-generation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/ultrafast-voice-response-latency-budgeting/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/unattended-session-lock-screen-policy-automation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/uncertainty-quantification/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/unicode-homoglyph-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/unit-consistency-reasoning/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/unit-test-generation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/universal-agent-brand-narrative-copywriting/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/url-dom-inspection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/url-fetching/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/url-normalization/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/url-rate-limiting/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/url-redirect-tracing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/url-screenshot/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/usage-based-metered-billing-actions/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/user-facing-error-copy/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/user-intent-restatement-confirmation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/user-preference-inference/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/user-profile/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/user-profile-memory/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/user-trust-calibration-communication/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/value-of-information-analysis/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vdi-session-automation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vector-db-tool/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vector-index-tuning/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vector-store-retrieval/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vector-store-schema-migration/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vendor-agent-platform-risk-assessment/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vendor-model-benchmark-normalization/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vendor-security-bulletin-parsing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vendor-soc2-evidence-collection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/verifiability-driven-planning/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/verifiable-intent-token-presentation-execution/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/verification-link-handling/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/video-continuity-error-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/video-description/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/video-frame-extraction/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/video-frame-sampling-review/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/video-highlight-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/video-object-tracking/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/video-script/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/video-understanding/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/visa-tap-protocol-usage/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vision-output-verification/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/visual-element-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vm-interaction/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-activity-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-agent-barge-in-handling/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-agent-emergency-escalation-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-agent-multi-provider-orchestration/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-agent-session-quality-analytics/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-and-tone-guide-authoring/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-clone-consent-verification/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-clone-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-driven-desktop-commanding/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/voice-to-visual-agent-response-pairing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vpn-connection-automation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vqa/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vulnerability-disclosure-handling/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vulnerability-triage/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/vulnerable-user-protection-patterns/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/wait-sleep/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/wake-word-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/warehouse-cost-attribution/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/wasm-edge-agent-runtime-deployment/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/watermark-detection/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/weather-api/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-accessibility-auditing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-agent-authenticated-session-automation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-api-mocking/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-archive-lookup/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-bot-auth-implementation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-content-freshness-checking/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-crawling/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-login/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-oauth-flow-handling/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-performance-budget-auditing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-push-subscription-automation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-scraping/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-search/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-search-tool-agents/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-session-replay/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-table-pagination-traversal/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/web-web-search/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/webauthn-passkey-automation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/webhook-handling/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/webhook-payload-parsing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/webmcp-page-tool-exposure/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/website-agent-identity-handshake-implementation/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/website-localization-verification/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/website-terms-of-service-agent-permission-audit/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/websocket-communication/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/websocket-stream-frame-parsing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/weighted-scoring-model-design/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/wikipedia-api/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/window-management/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/wolfram-api/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/workflow-cost-ceiling/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/workflow-dataflow-dependency-analysis/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/workflow-heartbeat-monitoring/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/workflow-versioning/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/working-memory/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/workplace-agent-invitation-announcement-writing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/worldbuilding/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/worldbuilding-consistency-auditing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/x402-crypto-payment-tool-usage/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/x402-http-payment-header-parsing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/x402-key-management-rotation-operations/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/x402-merchant-onboarding-copywriting/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/x402-multi-scheme-acceptance-tooling/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/x402-payment-header-negotiation-execution/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/x402-payment-provider-failover-execution/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/x402-payment-retry-idempotency-pattern/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/xml-parsing/SKILL.md
OK   /home/runner/work/skills-tree/skills-tree/agent-skills/xquik-api/SKILL.md
Validated 1599 skill package(s); 0 failed.
exit=0
~~~

## reconcile_agent_skills.py --check
~~~
    },
    {
      "expected_package": "sandbox-egress-proxy-configuration",
      "match": "provenance",
      "package": "sandbox-egress-proxy-configuration",
      "source": "skills/17-infrastructure/sandbox-egress-proxy-configuration.md"
    },
    {
      "expected_package": "secrets-management",
      "match": "provenance",
      "package": "secrets-management",
      "source": "skills/17-infrastructure/secrets-management.md"
    },
    {
      "expected_package": "serverless-cold-start-optimization",
      "match": "provenance",
      "package": "serverless-cold-start-optimization",
      "source": "skills/17-infrastructure/serverless-cold-start-optimization.md"
    },
    {
      "expected_package": "service-mesh-configuration",
      "match": "provenance",
      "package": "service-mesh-configuration",
      "source": "skills/17-infrastructure/service-mesh-configuration.md"
    },
    {
      "expected_package": "splunk-agent-otel-collector-provisioning",
      "match": "provenance",
      "package": "splunk-agent-otel-collector-provisioning",
      "source": "skills/17-infrastructure/splunk-agent-otel-collector-provisioning.md"
    },
    {
      "expected_package": "storage-lifecycle-tiering-automation",
      "match": "provenance",
      "package": "storage-lifecycle-tiering-automation",
      "source": "skills/17-infrastructure/storage-lifecycle-tiering-automation.md"
    },
    {
      "expected_package": "trace-sampling-budget-provisioning",
      "match": "provenance",
      "package": "trace-sampling-budget-provisioning",
      "source": "skills/17-infrastructure/trace-sampling-budget-provisioning.md"
    },
    {
      "expected_package": "wasm-edge-agent-runtime-deployment",
      "match": "provenance",
      "package": "wasm-edge-agent-runtime-deployment",
      "source": "skills/17-infrastructure/wasm-edge-agent-runtime-deployment.md"
    }
  ],
  "missing": [
    {
      "blockers": [
        "missing description",
        "missing Evidence section"
      ],
      "eligible": false,
      "package": "pipeline-test",
      "source": "skills/00-sandbox/pipeline-test.md"
    }
  ],
  "rename_needed": [
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
  "resolved_name_collisions": {
    "audio-transcription": [
      "skills/01-perception/audio-transcription.md",
      "skills/08-multimodal/audio-transcription.md"
    ],
    "dependency-auditor": [
      "skills/05-code/dependency-auditor.md",
      "skills/17-infrastructure/dependency-auditor.md"
    ],
    "drag-drop": [
      "skills/04-action-execution/drag-drop.md",
      "skills/10-computer-use/drag-drop.md"
    ],
    "github-api": [
      "skills/05-code/github-api.md",
      "skills/07-tool-use/github-api.md"
    ],
    "hypothesis-generation": [
      "skills/02-reasoning/hypothesis-generation.md",
      "skills/16-domain-specific/hypothesis-generation.md"
    ],
    "rag": [
      "skills/03-memory/rag.md",
      "skills/09-agentic-patterns/rag.md"
    ],
    "react": [
      "skills/02-reasoning/react.md",
      "skills/09-agentic-patterns/react.md"
    ],
    "screenshot-capture": [
      "skills/04-action-execution/screenshot-capture.md",
      "skills/10-computer-use/screenshot-capture.md"
    ],
    "scroll": [
      "skills/04-action-execution/scroll.md",
      "skills/10-computer-use/scroll.md"
    ],
    "web-search": [
      "skills/07-tool-use/web-search.md",
      "skills/11-web/web-search.md"
    ]
  },
  "stale": [],
  "unexpected": [],
  "unresolved_collisions": {}
}Reconciliation check failed: drifted: 1

exit=0
~~~
