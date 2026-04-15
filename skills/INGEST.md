# SKILL: INGEST
# Compiles a raw source into the wiki. This is where memory gets BUILT, not stored.

## Trigger
User says `/ingest <path>` or drops a file and asks to process it.

## Pipeline

### Step 1: Classify
Determine source type. This affects extraction strategy.
- `article` → key claims, data points, conclusions
- `paper` → methodology, findings, limitations, statistical significance
- `transcript` → speaker attribution, decisions, action items (skip filler)
- `report` → KPIs, projections, methodology
- `code` → architecture, dependencies, known issues, API surface
- `conversation` → decisions made, preferences expressed, context shared

### Step 2: Hash
```bash
python scripts/hash_tracker.py hash "<source_path>"
```
This records `sha256` of the source content. Used later to detect staleness.

### Step 3: Create Source Summary Page
Create `wiki/sources/<slug>.md` using template:

```markdown
---
type: source_summary
source_path: raw/<filename>
source_type: article|paper|transcript|report|code|conversation
ingested_at: YYYY-MM-DDTHH:MM:SSZ
content_hash: <sha256>
confidence: high|medium|low
relations:
  cites: []
  extracted_to: [list of wiki pages this source informed]
---

> **TLDR:** 2-3 sentence summary of what this source contains and why it matters.

## Key Claims
- [FACT] Claim text [src: <this_source>]
- [FACT] Another claim [src: <this_source>]

## Methodology / Context
How the claims were produced. Relevant for evaluating reliability.

## Limitations
What this source does NOT cover or where it might be wrong.

## Open Questions
- [GAP] What remains unclear from this source alone.
```

### Step 4: Compile Into Wiki
For each extracted claim/entity/concept:

**If a wiki page already exists for this topic:**
- Read the existing page
- Integrate new claims WITH citations
- Flag contradictions explicitly: `[CONTRADICTS: existing claim from src: other.md]`
- Update the TLDR
- Update frontmatter relations
- Do NOT silently overwrite — contradictions are features, not bugs

**If no page exists:**
- Create using appropriate template (entity, concept, etc.)
- Add all claims with citations
- Add relations in frontmatter
- Add TLDR

### Step 5: Update Index
Add/update entries in `wiki/index.md`:
```markdown
- [[entities/motoko]] — Sales agent handling WhatsApp pipeline [5 sources, high confidence]
```

### Step 6: Reflect
Append to `wiki/log.md`:
```markdown
## [YYYY-MM-DD HH:MM] ingest | <source_name>
**Added:** <list of new claims/pages>
**Updated:** <list of changed pages>
**Contradictions:** <any conflicts found>
**New relations:** <typed edges created>
**Gaps identified:** <what's still missing>
**Epistemic notes:** <confidence assessment>
```

### Step 7: Rebuild Graph
```bash
python scripts/graph_builder.py
```
This extracts all frontmatter `relations:` blocks and builds `graph/graph.json`.

## Idempotency Rule
Re-ingesting an unchanged source (same hash) MUST NOT alter the wiki.
Check hash first. If unchanged, skip and report "source unchanged, skipping."

## Multi-Source Ingest
When ingesting multiple sources:
- Process one at a time
- After each, run Step 6 (reflect)
- After all, run Step 7 (rebuild graph) once
- Report summary: X sources ingested, Y pages created, Z pages updated, W contradictions found
