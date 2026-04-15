# Wiki Memory Engine — CLAUDE.md
# A compiled, graph-augmented, epistemically-aware memory system for AI agents.
# This is NOT a note-taking app. This is a memory PRODUCT that beats Mem0/Zep/Letta.

## What This Is

A memory engine where knowledge is COMPILED (not just stored), RELATIONAL (typed graph edges),
TEMPORAL (validity windows), and EPISTEMICALLY HONEST (fact/inference/gap with provenance).

Every interaction makes the memory better (dual output). Every claim traces to sources (provenance).
The system knows what it knows, how it knows it, and how confident it is.

## Architecture

```
raw/                    # Immutable source documents (never edited by LLM)
wiki/                   # LLM-compiled markdown pages (LLM owns this layer)
  index.md              # Catalog of all pages with one-line summaries
  log.md                # Append-only chronological record of changes
  entities/             # Person, org, product, agent pages
  concepts/             # Topic and concept pages
  sources/              # Source summary pages
  outputs/              # Query-derived pages (analysis, comparisons)
  troubleshooting/      # Operational knowledge
graph/                  # Graph layer (Neo4j — derived from wiki, rebuildable)
  hashes.json           # Source content hashes
scripts/                # Python utilities
  neo4j_config.py       # Neo4j connection management + schema init
  embeddings.py         # Local vector embeddings (sentence-transformers)
  wiki_parser.py        # Shared markdown/frontmatter parsing
  hash_tracker.py       # Source change detection
  graph_builder.py      # Push graph to Neo4j from wiki frontmatter
  graph_query.py        # Hybrid text+vector+graph retrieval via Cypher
  community_detect.py   # GDS Louvain clustering (BFS fallback)
templates/              # Page templates by type
  entity.md
  concept.md
  source_summary.md
  output.md
skills/                 # Skill files for each operation
  INGEST.md
  COMPILE.md
  QUERY.md
  LINT.md
  REFLECT.md
  GRAPH.md
docker-compose.yml      # Neo4j container setup
requirements.txt        # Python dependencies
CLAUDE.md               # This file — the schema
```

## Prerequisites
- Docker (for Neo4j): `docker compose up -d`
- Python deps: `pip install -r requirements.txt`
- Schema init: `python scripts/neo4j_config.py --init`

## Core Rules (NON-NEGOTIABLE)

### Rule 1: Dual Output
Every interaction produces TWO outputs:
1. The response to the user
2. Updates to the wiki (new pages, updated pages, new graph edges)
If a query generates insight, that insight becomes a wiki page. No knowledge evaporates into chat.

### Rule 2: Provenance
Every claim in the wiki cites its source: `[src: filename.md]` or `[src: filename.md §section]`
Every source has a content hash recorded at ingest time.
Every claim is classified: `[FACT]`, `[INFERENCE]`, or `[GAP]`

### Rule 3: Progressive Disclosure (Token Budget)
- L0 (~200 tokens): This CLAUDE.md context section. Always loaded.
- L1 (~1-2K): wiki/index.md — scan to find relevant pages.
- L2 (~2-5K): TLDRs from relevant pages. Every page starts with `> **TLDR:** ...`
- L3 (5-20K): Full articles. Load ONLY when TLDR confirms relevance.
NEVER read full articles without checking index + TLDRs first.

### Rule 4: Relations in Frontmatter
Every wiki page includes a `relations:` block in YAML frontmatter with TYPED edges:
```yaml
relations:
  depends_on: [list of entities this requires]
  generates: [list of outputs this produces]
  contradicts: [claims that conflict]
  supersedes: [older claims this replaces]
  measured_by: [metrics/KPIs that evaluate this]
  derived_from: [queries/analysis this came from]
  cites: [source files]
  enables: [what this makes possible]
  blocks: [what this prevents]
```
These are the graph edges. The graph is DERIVED from frontmatter — wiki is source of truth.

### Rule 5: Reflect After Every Ingest
After compiling, append to log.md:
- What claims were added/changed
- What contradictions were found
- What remains uncertain
- What graph edges were created

### Rule 6: Graph-First Retrieval (when graph exists)
When answering queries (requires Neo4j: `docker compose up -d`):
1. Run `python scripts/graph_query.py "<query>"` — hybrid text+vector+graph retrieval
2. Load TLDRs of connected nodes
3. Load full pages only if needed
4. Synthesize answer
5. DUAL OUTPUT: update wiki + graph with new knowledge

## Operations

### /ingest <source_path>
Read skill: skills/INGEST.md
1. Classify source type (article, paper, transcript, report, code, conversation)
2. Hash the source content → record in source_summary frontmatter
3. Extract claims with citations
4. Compile into wiki pages (create or update)
5. Add relations to frontmatter
6. Reflect (append to log.md)
7. Rebuild graph: `python scripts/graph_builder.py`

### /query <question>
Read skill: skills/QUERY.md
1. Graph retrieval: `python scripts/graph_query.py "<question>"`
2. Load TLDRs of relevant pages
3. Load full pages if needed
4. Synthesize answer
5. DUAL OUTPUT: create output page + update related pages

### /lint
Read skill: skills/LINT.md
Check: contradictions, stale sources (hash mismatch), orphan pages,
missing citations, one-sided coverage, thin topics, broken wikilinks.

### /graph
Read skill: skills/GRAPH.md
Rebuild graph from wiki frontmatter. Run community detection.
Show clusters, bridges, gaps.

### /status
Show: page count, source count, stale sources, last ingest, graph stats,
communities, open gaps.

## L0 Context (always loaded)
This is a compiled wiki memory engine. Knowledge is synthesized, not just stored.
Every claim has provenance. Every relation is typed. Every interaction compounds.
The wiki is the source of truth. The graph is a derived index.
Read skills/ before any operation.
