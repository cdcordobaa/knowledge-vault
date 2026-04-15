---
type: source_summary
source_path: notion://domain-8-spec-driven
source_type: research
ingested_at: 2026-04-13T21:00:00Z
content_hash: notion_domain_8
confidence: high
relations:
  cites: [baxbench-2025, karpathy-vibe-coding, swebench-2024, cursor-background-agents-2025]
  enables: [daedalus-arch, fitness-functions]
  derived_from: [domain-6-verification, domain-2-speed-stability]
  contradicts: [vibe-coding-is-sufficient]
  supersedes: [manual-spec-writing]
---

> **TLDR:** Spec-Driven & Agentic Engineering — the paradigm where specifications (not code) are the primary artifact. Covers vibe coding risks, agentic TDD, architecture-aware agents, and the BaxBench benchmark showing vulnerability rates worsen from 40% (functions) to 80% (repo-level agentic tasks).

## Key Claims

[FACT] Andrej Karpathy coined "vibe coding" to describe the practice of generating code through natural language without understanding the output — embracing vibes over comprehension — which has rapidly become the default mode for many AI-assisted developers. [src: karpathy-vibe-coding]

[FACT] BaxBench demonstrates that AI vulnerability rates scale with task scope: 40% of function-level AI-generated code contains security vulnerabilities, rising to 80% for repo-level agentic tasks where the agent manages full project structure. [src: baxbench-2025]

[FACT] Cursor's Background Agents represent the shift from AI-as-assistant (human drives, AI suggests) to AI-as-autonomous-agent (AI drives, human reviews), fundamentally changing the developer's role from writer to verifier. [src: cursor-background-agents-2025]

[FACT] Agentic TDD inverts the traditional workflow: AI generates tests from specifications first, then implements code to pass those tests, using the spec-test-code pipeline to constrain generation and catch deviations early. [src: baxbench-2025, swebench-2024]

[FACT] Architecture-aware agents that enforce dependency rules, layer constraints, and module boundaries before generating code produce significantly fewer architectural violations than agents that generate first and check later. [src: swebench-2024]

[FACT] SWE-Bench reveals that even top-performing AI agents solve only 12-20% of real-world GitHub issues end-to-end, with failure modes concentrated in tasks requiring cross-file reasoning and architectural understanding. [src: swebench-2024]

[FACT] The spec-driven paradigm redefines engineering roles: specifications become the primary artifact requiring human expertise, code becomes a generated and disposable output, and verification (not writing) becomes the core craft. [src: baxbench-2025, cursor-background-agents-2025]

[FACT] BaxBench's 40%-to-80% vulnerability escalation demonstrates that agentic autonomy and security are inversely correlated without architectural guardrails — more agent freedom produces more vulnerabilities. [src: baxbench-2025]

## Cross-Cutting Themes

[INFERENCE] Vibe coding is the natural endpoint of the speed-stability paradox (Domain 2): when AI maximizes velocity, developers rationally reduce comprehension effort, but this creates a fragility debt that compounds until architectural failure. [inferred from: karpathy-vibe-coding, domain-2-speed-stability]

[INFERENCE] The convergence of spec-driven development (Domain 6) with agentic engineering suggests a future where human engineers primarily write and maintain specifications while AI agents handle implementation — but only if verification frameworks can close the 40-80% vulnerability gap. [inferred from: domain-6-verification, baxbench-2025, cursor-background-agents-2025]
