# ONE-HOUR SPRINT PLAN
# Building Wiki Memory Engine with Claude Code

## What You Have (this repo)
- `CLAUDE.md` — master schema (Claude Code reads this automatically)
- `skills/` — 6 skill files (INGEST, COMPILE, QUERY, LINT, REFLECT, GRAPH)
- `scripts/` — 3 Python utilities (hash_tracker, graph_builder, graph_query)
- `templates/` — 4 page templates (entity, concept, source_summary, output)
- `scripts/init.sh` — directory structure setup

## The Sprint (60 minutes)

### Minute 0-5: Setup
```bash
# 1. Copy this entire repo to your project
cp -r wiki-memory-product/ ~/hardcore-ai-wiki/
cd ~/hardcore-ai-wiki/

# 2. Initialize the structure
bash scripts/init.sh hardcore-ai

# 3. Copy your existing 76 source files into raw/
cp /path/to/your/sources/* raw/

# Claude Code will now read CLAUDE.md automatically on every session.
```

### Minute 5-15: First Ingest (prove the pipeline works)
Open Claude Code in the project directory. Say:

```
Read skills/INGEST.md. Then ingest this single source: raw/<your_most_important_file>.md
Follow the full pipeline: classify, hash, extract, compile, reflect, build graph.
```

Watch it:
- Create wiki/sources/<slug>.md with hash + citations
- Create/update entity and concept pages with typed relations
- Append to wiki/log.md with reflect entry
- Run graph_builder.py

**Checkpoint:** You should have 3-5 wiki pages, all with TLDRs, all with
`[FACT]`/`[INFERENCE]` markers, all with `relations:` in frontmatter.

### Minute 15-30: Batch Ingest (build mass)
```
Ingest these 10 most important sources one at a time:
raw/spec-motoko.md, raw/sales-report.md, raw/playbook-b2b.md,
raw/contract-template.md, raw/marketing-plan.md, ...
(list your top 10)

After each, do the reflect step. After all 10, rebuild the graph.
```

**Checkpoint:** ~20-30 wiki pages. Graph should show connections.

### Minute 30-40: Test Graph Retrieval
```
Run: python scripts/graph_builder.py --communities

Then answer this question using graph-first retrieval (read skills/QUERY.md):
"How does the WhatsApp pipeline affect B2B conversion?"

Use dual output — save the analysis as a wiki output page.
```

**Checkpoint:** The graph query should find the path between entities.
The output page should exist in wiki/outputs/.

### Minute 40-50: Test the Compounding Loop
```
Now ask a cross-domain question that requires the previous output:
"Based on the WhatsApp conversion analysis, what should we change in 
Motoko's auto-approval flow?"

This should reference the output page we just created. That's the
compounding loop — knowledge building on knowledge.
```

Then:
```
Run /lint. Fix any issues found.
```

### Minute 50-60: Verify the Differentiators
Test each unique feature:

**Provenance:** Pick any wiki page. Every claim should have `[src: ...]`.
Trace one claim back to its original source in raw/.

**Epistemic honesty:** The wiki should have `[FACT]`, `[INFERENCE]`, and `[GAP]`
markers. Check that inferences cite multiple sources.

**Temporal/staleness:** Edit one source file in raw/ (add a line). Run:
```bash
python scripts/hash_tracker.py check
```
It should detect the change and tell you which wiki pages might be stale.

**Graph structure:** Run:
```bash
python scripts/graph_query.py neighbors motoko
python scripts/graph_query.py path motoko conversion
python scripts/graph_query.py gaps
```
You should see typed edges (depends_on, generates, measured_by, etc.)

**Dual output:** Check wiki/log.md. Every query should have produced
wiki updates. Nothing should have evaporated into chat.

---

## What You Tell Claude Code at Session Start

Just open the project. Claude Code reads CLAUDE.md automatically.
Then use the commands:

```
/ingest raw/<file>          # Compile a source into the wiki
/query "<question>"          # Graph-first retrieval + dual output
/query --fast "<question>"   # Quick lookup from TLDRs only
/query --exhaustive "<q>"    # Deep analysis with gap detection
/lint                        # Health check
/lint --fix                  # Auto-fix what's safe
/graph                       # Rebuild graph
/graph communities           # Show knowledge clusters
/graph path <a> <b>          # Find connection between entities
/status                      # Overview stats
/reflect                     # Synthesize recent changes
```

## What Makes This Different From Mem0/Zep/Everyone

1. COMPILED: Knowledge is synthesized across sources, not stored raw
2. EPISTEMIC: Every claim is typed (fact/inference/gap) with provenance
3. RELATIONAL: 10 typed edge types, not just "related to"
4. TEMPORAL: Hash tracking detects when sources change
5. COMPOUNDING: Dual output means every interaction enriches the wiki
6. AUDITABLE: Human-readable markdown, git-diffable, browsable in Obsidian
7. ZERO INFRA: No Neo4j, no vector DB, no Docker. Python + markdown + JSON.

## Next Steps After the Sprint
- Open the wiki/ folder in Obsidian → instant graph view + navigation
- Git init → version history of knowledge evolution
- Add more sources → the compounding loop starts working
- When it hurts (500+ pages) → swap graph.json for Graphiti/Neo4j
