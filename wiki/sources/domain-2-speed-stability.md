---
type: source_summary
source_path: notion://domain-2-speed-stability
source_type: research
ingested_at: 2026-04-13T21:00:00Z
content_hash: notion_domain_2
confidence: high
relations:
  cites: [dora-2025, gitclear-2024, faros-ai-2025, metr-2025, perry-et-al-2023]
  enables: [architecture-erosion, daedalus-arch]
  contradicts: [ai-always-boosts-productivity]
  measured_by: [deployment-frequency, lead-time, change-failure-rate, code-churn]
  derived_from: []
---

> **TLDR:** The Speed-Stability Paradox — empirical evidence that AI makes developers 21% more productive individually while creating 91% slower reviews, 9x more code churn, and developers who are 19% slower while believing they're 24% faster (METR RCT).

## Key Claims

[FACT] DORA 2025 finds AI is an amplifier, not a panacea — 90% of teams report AI adoption, but outcomes diverge across 7 distinct team archetypes depending on engineering practices. [src: dora-2025]

[FACT] GitClear 2024-2025 reports copy-paste code exceeded refactoring for the first time in 2024, with heavy AI users exhibiting 9x more code churn than non-AI users, indicating generated code is frequently revised or reverted. [src: gitclear-2024]

[FACT] Faros AI observes a 21/98 split: developers complete 21% more tasks but generate 98% more pull requests, leading to review rot where review throughput collapses under PR volume — reviews are 91% slower. [src: faros-ai-2025]

[FACT] METR randomized controlled trial (n=16 experienced OSS devs) shows developers are 19% slower with AI assistance on their own repos, while self-reporting they believed they were 24% faster — a 43 percentage point perception-reality gap. [src: metr-2025]

[FACT] Perry et al. find developers write significantly less secure code when using AI assistants while expressing greater confidence that their code is secure — the Trust Paradox. [src: perry-et-al-2023]

[FACT] Bird et al. document the Writer-to-Verifier shift: AI accelerates code writing by ~55% but debugging time increases proportionally, yielding diminishing net gains as complexity rises. [src: bird-et-al-2023]

[FACT] DORA identifies that teams with strong DevOps foundations (CI/CD, trunk-based development, monitoring) amplify AI benefits, while teams without foundations see AI amplify dysfunction. [src: dora-2025]

[FACT] GitClear's churn metric — percentage of code changed within 2 weeks of being written — is the strongest leading indicator that AI-generated code creates downstream maintenance burden. [src: gitclear-2024]

## Cross-Cutting Themes

[INFERENCE] The speed-stability paradox is fundamentally a measurement failure: organizations track individual velocity (which improves) but not system-level quality metrics (which degrade), creating a false narrative of productivity gains. [inferred from: faros-ai-2025, dora-2025, metr-2025]

[INFERENCE] The 43-point perception-reality gap from METR, combined with Perry's trust paradox, suggests AI tools create a systematic overconfidence bias that may distort organizational decision-making about AI adoption and staffing. [inferred from: metr-2025, perry-et-al-2023]
