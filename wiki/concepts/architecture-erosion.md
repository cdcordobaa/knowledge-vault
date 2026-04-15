---
type: concept
created_at: 2026-04-13T21:00:00Z
updated_at: 2026-04-13T21:00:00Z
confidence: high
aliases: [architectural-degradation, code-erosion, ai-code-quality]
relations:
  cites: [domain-9-research]
  blocks: [code-quality-at-scale]
  enables: [daedalus-arch]
  measured_by: [avr-score, slopcodebench]
  related_to: [fitness-functions]
---

> **TLDR:** Architecture erosion is the empirically validated phenomenon where AI-generated code systematically degrades software architecture through anti-patterns like refactoring avoidance, over-specification, and pattern fixation — acting as an "army of enthusiastic junior developers" who write working code without understanding the system.

## Definition
[FACT] Architecture erosion (AEr) manifests through architectural violations, structural issues, degraded quality, and impeded evolution. Non-technical reasons cause erosion as frequently as technical ones. [src: domain-9-research §Li et al. 2022]

## Key Evidence
[FACT] OX Security (2025) analyzed 300+ repositories and identified 10 critical anti-patterns in AI-generated code, with "Avoidance of Refactors" at 80-90% prevalence. [src: domain-9-research §OX Security]

[FACT] SlopCodeBench (Snorkel AI, 2026) measures iterative degradation — each agent iteration may pass tests but progressively introduces "slop" that compounds silently. [src: domain-9-research §SlopCodeBench]

[FACT] GIST Study (2026) found developers document AI-introduced debt in code comments, revealing three AI roles in technical debt: Source, Catalyst, and Mitigator. [src: domain-9-research §GIST]

[INFERENCE] AI doesn't create new types of erosion — it accelerates existing patterns at unprecedented scale. The volume effect is the key differentiator from human-caused erosion. [inferred from: domain-9-research §Li et al., §OX Security]

## Implications for DaedalusArch
[FACT] The OX Security anti-patterns serve as a concrete "threat model" for conformance checking — they define what the [[daedalus-arch]] must defend against. [src: domain-9-research]

## Open Questions
[GAP] How does erosion compound across multiple agent iterations in real-world multi-agent development?
