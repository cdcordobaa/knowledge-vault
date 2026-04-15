---
type: source_summary
source_path: notion://5120aceda28947ffa2799ff861695f21
source_type: report
ingested_at: 2026-04-13T21:00:00Z
content_hash: notion_srs
confidence: high
relations:
  cites: [thesis-proposal-v2, research-audit-trail]
  extracted_to: [daedalus-arch, apg, fitness-functions, neuro-symbolic-compliance]
  derived_from: [thesis-proposal-v2]
  enables: [daedalus-arch]
---

> **TLDR:** Formal system requirements specification for the neuro-symbolic architectural firewall, mapping 4 specific objectives (SO1-SO4) to concrete functional and non-functional requirements. Covers spec ingestion pipeline, APG construction, neuro-symbolic review gate, and empirical validation methodology.

## Key Requirements
[FACT] SO1: AoC YAML parser with 3 layers (Model, Fitness Functions, Scoring), ADR parsing, violation taxonomy.
[FACT] SO2: APG construction via ts-morph with 5 node types, 7 relationship types, delta updates, drift detection.
[FACT] SO3: 17 symbolic fitness functions across 5 dimensions, LLM Critic for semantic evaluation, hybrid routing logic.
[FACT] SO4: Seeded violation ground truth, ablation study (symbolic vs neuronal vs combined), factorial benchmark (3 LLMs x 3 spec levels x 5 tasks x 3 reps = 135 projects).
