# Wiki Memory Engine

A compiled, graph-augmented, epistemically-aware memory system for AI agents.

## What This Is

The **Wiki Memory Engine** is a high-performance knowledge synthesis platform designed to provide AI agents with a "compounding memory." Unlike traditional vector databases that merely store raw data, this engine **compiles and synthesizes** information into a structured, relational, and auditable knowledge base.

Knowledge is **COMPILED** (not just stored), **RELATIONAL** (typed graph edges), **TEMPORAL** (validity windows), and **EPISTEMICALLY HONEST** (fact/inference/gap with provenance).

## Core Value Propositions

*   **Knowledge Compilation vs. Storage:** Synthesizes information across multiple sources into coherent Wiki pages.
*   **Dual-Output Compounding Loop:** Every interaction produces a response to the user AND updates the permanent knowledge base.
*   **Epistemic Honesty & Provenance:** Every claim is typed as `[FACT]`, `[INFERENCE]`, or `[GAP]` with direct citations (`[src: filename.md]`).
*   **Relational Intelligence:** Uses 10 distinct, typed relationship edges (e.g., `depends_on`, `contradicts`, `supersedes`) for complex reasoning.
*   **Token Efficiency:** Tiered retrieval strategy (L0 to L3) reduces operational costs by loading only relevant content.
*   **Temporal Awareness:** Automated hash tracking detects when source documents change, flagging stale knowledge.

## Architecture

- **raw/**: Immutable source documents (never edited by LLM).
- **wiki/**: LLM-compiled markdown pages (the source of truth).
- **graph/**: Neo4j graph layer derived from wiki frontmatter.
- **scripts/**: Python utilities for graph building, querying, and maintenance.
- **skills/**: Specialized operational guidance for Ingest, Query, Lint, and more.

## Getting Started

### Prerequisites
- **Docker**: For Neo4j (`docker compose up -d`)
- **Python 3.10+**: `pip install -r requirements.txt`

### Setup
1.  Initialize the directory structure:
    ```bash
    bash scripts/init.sh
    ```
2.  Initialize the Neo4j schema:
    ```bash
    python scripts/neo4j_config.py --init
    ```

### Basic Usage
- **Ingest**: `/ingest raw/document.md` — Compiles a source into the wiki.
- **Query**: `/query "Your question"` — Graph-first retrieval + dual output.
- **Lint**: `/lint` — Health check for contradictions and stale sources.
- **Graph**: `/graph communities` — Visualize knowledge clusters.

## Why This Is Different
1. **COMPILED**: Knowledge is synthesized across sources, not stored raw.
2. **EPISTEMIC**: Every claim is typed with provenance.
3. **RELATIONAL**: 10 typed edge types, not just "related to."
4. **TEMPORAL**: Hash tracking detects when sources change.
5. **COMPOUNDING**: Dual output means every interaction enriches the wiki.
6. **AUDITABLE**: Human-readable markdown, git-diffable, and browsable.

---
*Refer to `CLAUDE.md` for the full technical schema and core rules.*
