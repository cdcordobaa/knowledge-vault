---
type: source_summary
source_path: notion://33f50d3082278038b806f0e766fac882
source_type: paper
ingested_at: 2026-04-13T21:00:00Z
content_hash: notion_proposal_v2
confidence: high
relations:
  cites: [dora-2025, faros-ai-2025, slater-2025, gitclear-2024]
  extracted_to: [daedalus-arch, apg, fitness-functions, neuro-symbolic-compliance]
  enables: [daedalus-arch]
  derived_from: [domain-9-research, research-audit-trail]
---

> **TLDR:** Master's thesis proposal by Cristian Cordoba at UNAL for a neuro-symbolic architectural firewall that checks AI-generated TypeScript code against AaC YAML specs using an APG in Neo4j. Uses DSR + quasi-experimental methodology with 3-phase validation (golden dataset, factorial design, developer study). 13-week timeline, ~$32K budget.

## Key Claims
[FACT] Over 80% of developers use AI coding tools daily (DORA 2025); PR volume rose 98% while task completion rose only 21% (Faros AI 2025).
[FACT] Slater (2025) measured 80% boundary violation rate in agent-generated code.
[FACT] GitClear (2024-2025) found 9x more code churn and 8x more copy-paste among heavy AI users.
[FACT] Feasibility spike produced AHS scores ranging 0.33 (violated) to 0.85 (clean).
[FACT] 6 core evaluation dimensions: structural, pattern, convention, testability, complexity, evolvability.

## Methodology
[FACT] DSR + quasi-experimental. Phase 1: golden dataset with seeded violations. Phase 2: factorial design (LLM x spec quality) with ANOVA. Phase 3: controlled developer study. 90+ generated projects across conditions.
