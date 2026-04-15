---
type: source_summary
source_path: notion://33550d30822781738788cb0e43a6892e
source_type: research
ingested_at: 2026-04-13T21:00:00Z
content_hash: notion_aac_validation
confidence: high
relations:
  cites: [ford-richards-2017, ford-richards-adl-2025, medvidovic-taylor-2000, sonarqube-aac, archunit]
  extracted_to: [fitness-functions, daedalus-arch]
  contradicts: [formal-adls]
  supersedes: [sonarqube-aac]
---

> **TLDR:** Research validation for the AaC YAML + fitness functions approach. Confirms it is well-grounded (Ford/Richards 2017-2025), novel (no prior work does declarative YAML → deterministic Cypher compilation), and appropriately scoped. Ford/Richards' ADL is the closest parallel but uses non-deterministic LLM-mediated compilation.

## Key Claims
[FACT] Ford & Richards' "Architecture as Code" (O'Reilly 2025) validates the thesis premise of fitness function-driven AaC governance.
[FACT] Two existing forms of fitness functions: imperative code (ArchUnit) and shallow declarative (SonarQube). The thesis adds a third: deep declarative YAML → Cypher.
[FACT] Formal ADLs consistently failed industry adoption due to poor usability, limited tooling, and domain specificity.
[FACT] All existing fitness function literature frames them as CI/CD guardrails. The thesis is the first to apply them as benchmark scoring instruments for generated code.
