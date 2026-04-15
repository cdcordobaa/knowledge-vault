---
type: concept
created_at: 2026-04-13T21:00:00Z
updated_at: 2026-04-13T21:00:00Z
confidence: high
aliases: [architectural-property-graph, code-graph, neo4j-apg]
relations:
  enables: [daedalus-arch, fitness-functions]
  depends_on: [neo4j, ts-morph]
  supersedes: [full-cpg, codeql-for-architecture, joern]
  generates: [cypher-queries]
  derived_from: [system-requirements-spec, research-audit-trail]
---

> **TLDR:** The Architectural Property Graph (APG) is a Neo4j-stored graph representation of TypeScript code structure, with nodes for files/classes/interfaces/methods and typed edges for imports/implements/extends/injects. It enables deterministic Cypher queries for architectural compliance checking.

## Definition
[FACT] The APG represents AI-generated code as a queryable graph with node types: File, Class, Interface, Method, Function. Properties include name, filePath, layer, role, isExported, isAbstract, visibility, decorators. [src: system-requirements-spec §FR-APG-01]

[FACT] Relationship types: IMPORTS, IMPLEMENTS, EXTENDS, CONSTRUCTOR_INJECTS, CALLS, DECLARES, CONTAINS. [src: system-requirements-spec §FR-APG-01]

## Construction Pipeline
[FACT] Built from TypeScript projects using ts-morph. Validated capabilities: barrel import resolution, path alias resolution, interface vs concrete type resolution for DI, decorator extraction, lenient parsing for partially broken code. [src: system-requirements-spec §FR-APG-01]

## Layer Annotation
[FACT] Nodes are annotated with layer and role using deterministic mapping from AaC YAML: (1) directory mapping, (2) naming conventions, (3) decorator mapping. Files matching no rule get layer: null. [src: system-requirements-spec §FR-APG-02]

## Persistence and Drift Detection
[FACT] The APG supports delta updates (only changed files reprocessed) and historical snapshots per commit for drift detection: structural drift, coupling drift, convention drift, violation trends. [src: system-requirements-spec §NF-APG-01]

## Performance
[FACT] Full APG construction in under 5 seconds per project. Delta updates under 2 seconds for typical PR changes. Spike-validated. [src: system-requirements-spec §NF-APG-02]

## Open Questions
[GAP] APG currently covers Layer 1 (structural) + small parts of Layer 2. Deeper analysis (control flow, data flow) mapped but not implemented.
