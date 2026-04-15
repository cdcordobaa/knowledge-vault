---
type: concept
created_at: 2026-04-13T21:00:00Z
updated_at: 2026-04-13T21:00:00Z
confidence: high
aliases: [neuro-symbolic-review, hybrid-verification, symbolic-neuronal]
relations:
  enables: [daedalus-arch]
  depends_on: [apg, fitness-functions]
  derived_from: [veribench-iclr-2026, conflictlens-2025, system-requirements-spec]
  supersedes: [symbolic-only-verification, llm-review-only]
  contradicts: [coderabbit-sufficiency]
  measured_by: [ablation-study, cohens-kappa]
---

> **TLDR:** Neuro-symbolic compliance combines deterministic symbolic verification (Cypher graph queries on the APG) with an LLM Critic agent for semantic evaluation, routing each architectural check to the appropriate path based on the nature of the violation. This hybrid approach catches what neither path alone can detect.

## The Two Paths
[FACT] Symbolic path: parameterized Cypher queries against the APG for all graph-observable violations. Deterministic, auditable, under 5 seconds. [src: system-requirements-spec §FR-GATE-01]

[FACT] Neuronal path: LLM Critic evaluates violations requiring judgment about intent or semantic meaning. Input: code snippet + APG subgraph + semantic_criteria + rubric + optional ADR prose. Output: pass/fail/warning with confidence score and evidence. [src: system-requirements-spec §FR-GATE-02]

## Routing Logic
[FACT] Routing is static and deterministic by fitness function type: structural/coupling/pattern/convention → symbolic only; semantic/intent → neuronal always; SOLID → hybrid cascade (symbolic first, neuronal if symbolic passes). [src: system-requirements-spec §FR-GATE-03]

## Why Hybrid?
[INFERENCE] The symbolic path catches structural violations precisely but cannot evaluate architectural intent. The neuronal path catches semantic violations but is non-deterministic. Combined approach maximizes recall while maintaining precision. [inferred from: system-requirements-spec §FR-GATE-03, §FR-VAL-03]

[FACT] The ablation study is designed to prove this: Expected outcome is Combined > Symbolic-only > Neuronal-only for Recall, and Combined ≈ Symbolic-only for Precision. [src: system-requirements-spec §FR-VAL-03]

## Research Context
[FACT] The neuro-symbolic approach is validated by VeriBench (ICLR 2026): same model that fails 87.5% in single-shot generation succeeds 90% when embedded in an agentic loop with deterministic feedback — directly validating the architectural firewall thesis. [src: domain-9-research §11]

## Open Questions
[GAP] Can the LLM Critic compensate for low-quality specs? (Interaction effect: neuronal path may recover violations that weak specs cause symbolic path to miss.)
