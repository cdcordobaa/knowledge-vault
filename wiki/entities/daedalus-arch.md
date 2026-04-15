---
type: entity
subtype: product
created_at: 2026-04-13T21:00:00Z
updated_at: 2026-04-13T21:00:00Z
confidence: high
aliases: [architectural-firewall, governance-engine, neuro-symbolic-firewall]
relations:
  depends_on: [apg, fitness-functions, neo4j, neuro-symbolic-compliance]
  generates: [avr-score, ahs-score, violation-reports]
  enables: [automated-architecture-compliance]
  measured_by: [precision, recall, cohens-kappa]
  derived_from: [domain-9-research, thesis-proposal-v2, system-requirements-spec]
  supersedes: [sonarqube-aac, codeql-for-architecture]
  contradicts: [codegen-benchmarks-are-sufficient]
---

> **TLDR:** DaedalusArch is a neuro-symbolic architectural firewall that combines deterministic graph queries (Cypher on an APG in Neo4j) with an LLM Critic agent to evaluate whether AI-generated code complies with architectural specifications expressed as AaC YAML.

## Overview
[FACT] DaedalusArch is the working implementation of the thesis "Architectural Compliance Instrument for Evaluating LLM-Generated Code" by Cristian Daniel Cordoba Aguirre at Universidad Nacional de Colombia. [src: thesis-proposal-v2]

[FACT] The system has two verification paths: a symbolic path (17 Cypher fitness functions on the APG) and a neuronal path (LLM Critic agent for semantic/intent violations). [src: system-requirements-spec]

[FACT] Routing between paths is deterministic: structural/coupling/pattern/convention violations go symbolic-only; semantic/intent violations go neuronal; SOLID violations use a hybrid cascade (symbolic first, then neuronal if symbolic passes). [src: system-requirements-spec]

## Key Architecture
- **Symbolic Path**: AaC YAML → deterministic compiler → parameterized Cypher queries → APG (Neo4j)
- **Neuronal Path**: Code snippet + APG subgraph + semantic_criteria → LLM Critic → structured verdict
- **Hybrid Path**: Symbolic check first → if passes, LLM Critic evaluates semantic compliance

## Scoring
[FACT] Two-tier scoring: AVR (Architectural Violation Ratio per dimension, 0.0-1.0) and AHS (Architectural Health Score, weighted complement across dimensions). [src: system-requirements-spec]

[FACT] Reports distinguish deterministic score (symbolic only, reproducible) from combined score (symbolic + neuronal, may vary). [src: system-requirements-spec]

## Validation
[FACT] Empirical validation uses seeded violations in clean architecture TypeScript projects, with 2-3 independent human evaluators. Targets: Precision >= 0.90, Recall >= 0.85, Cohen's kappa >= 0.60. [src: system-requirements-spec]

[FACT] Ablation study compares symbolic-only vs neuronal-only vs combined to prove marginal value of LLM Critic. [src: system-requirements-spec]

## Open Questions
[GAP] LLM Critic reproducibility — ICC target is >= 0.70 across runs but not yet validated.
[GAP] Confidence calibration thresholds (0.60/0.85) are proposed but not empirically grounded yet.
