---
type: concept
created_at: 2026-04-13T21:00:00Z
updated_at: 2026-04-13T21:00:00Z
confidence: high
aliases: [architectural-fitness-functions, aac-yaml, architecture-as-code]
relations:
  cites: [aac-yaml-validation]
  enables: [daedalus-arch]
  depends_on: [apg, neo4j]
  derived_from: [ford-richards-2017, ford-richards-adl-2025]
  supersedes: [sonarqube-aac, archunit-imperative]
  generates: [cypher-queries, avr-score]
  contradicts: [formal-adls]
---

> **TLDR:** Fitness functions are executable architectural constraints that verify code compliance. The thesis contributes a novel approach: declarative AaC YAML compiled deterministically to Cypher graph queries, which is deeper than existing tools (SonarQube) and more deterministic than the closest alternative (Ford/Richards' ADL → LLM → imperative code).

## Definition
[FACT] Concept introduced by Ford, Parsons, Kua in "Building Evolutionary Architectures" (O'Reilly 2017). Fitness functions are objective metrics that evaluate how well an architecture meets defined criteria. [src: aac-yaml-validation §2.1]

## Two Existing Forms (and the thesis gap)
[FACT] Two forms exist: (1) Imperative code (ArchUnit, NetArchTest) — must be written manually, language-specific; (2) Declarative constraints (SonarQube AaC YAML) — shallow, import-level only. [src: aac-yaml-validation §2.2]

[FACT] The thesis adds a third form: declarative YAML compiled deterministically to Cypher queries — deeper than import-level, without requiring imperative code. No prior work does this. [src: aac-yaml-validation §2.2]

## Ford/Richards ADL vs Thesis YAML
[FACT] Ford & Richards (2025) created an Architecture Definition Language that is "prompt-friendly" — fed to an LLM to generate executable fitness functions. Key difference: they use an LLM to generate imperative code; the thesis compiles YAML deterministically to Cypher. [src: aac-yaml-validation §1.2]

## 3-Layer AaC YAML Specification
[FACT] Layer A: Architectural Model (style, layers, allowed dependencies, mapping rules). Layer B: Fitness Functions (dimension tags, severity, thresholds, route: symbolic/neuronal/hybrid). Layer C: Scoring Configuration (AHS weights, pass/fail thresholds). [src: system-requirements-spec §FR-SPEC-02]

## 17 Validated Symbolic Fitness Functions
[FACT] 5 dimensions: Structural (3), Coupling (3), Pattern (3), SOLID (4), Convention (4). All deterministic, auditable, under 5 seconds for all 17 functions. Spike-validated. [src: system-requirements-spec §FR-GATE-01]

## Limitations
[FACT] YAML struggles with behavioral constraints, contextual rules, and semantic qualities. The thesis scopes to static structural fitness functions and uses LLM-as-judge for semantic qualities. [src: aac-yaml-validation §4.1]

[GAP] Threshold calibration for coupling metrics not empirically validated in TypeScript backend code.
[GAP] Novel application of fitness functions as benchmark scoring instruments (all prior work uses pass/fail for CI/CD).
