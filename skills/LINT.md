# SKILL: LINT
# Health-check the wiki for quality, consistency, and gaps.

## Trigger
`/lint` or `/lint --fix`

## Checks

### C1: Provenance
- Every `[FACT]` has a `[src: ...]` citation
- Every `[INFERENCE]` has `[inferred from: ...]`
- Every `[DERIVED]` has `[derived from query: ...]`
- Flag any unmarked claims as `[UNTYPED — needs classification]`

### C2: Source Staleness
```bash
python scripts/hash_tracker.py check
```
Reports which sources have changed since ingest.
For each stale source, list all wiki pages that cite it.
These pages have POTENTIALLY outdated claims.

### C3: Contradictions
Scan for `[CONTRADICTS: ...]` markers.
Ensure both sides of every contradiction are documented.
Flag contradictions that haven't been resolved (no `supersedes` relation).

### C4: Orphans and Connectivity
- Pages with no inbound wikilinks = orphans. They're invisible.
- Pages with no outbound wikilinks = dead ends. They don't contribute.
- Flag both. Suggest connections.

### C5: Broken Wikilinks
Every `[[target]]` should resolve to an existing page.
If target doesn't exist → flag as "missing page" and suggest creation.

### C6: TLDR Quality
- Every page must have a TLDR
- TLDR should be 2-3 sentences (flag if too short/long)
- TLDR should contain the most important keywords for retrieval

### C7: Frontmatter Relations
- Every page must have `relations:` in frontmatter
- Flag pages with no relations (disconnected from graph)
- Flag `cites:` that reference non-existent sources

### C8: Index Completeness
- Every wiki page should appear in `wiki/index.md`
- Flag pages missing from index
- Flag index entries pointing to deleted pages

### C9: Thin Coverage
- Topics with only 1 source = thin. Flag for enrichment.
- Entities mentioned in 3+ pages but lacking their own page = missing entity page.

### C10: One-Sided Coverage (anti-bias)
For evaluative topics (comparisons, product analysis, strategy):
- Check if only positive OR only negative claims exist
- Suggest counter-sources to seek
- Label any generated counter-arguments as `[GENERATED — not from sources]`

## Output
Generate a lint report:
```markdown
## Lint Report — YYYY-MM-DD HH:MM

### Critical
- X claims without citations
- Y stale sources affecting Z pages

### Warnings
- A orphan pages
- B broken wikilinks
- C pages missing from index

### Suggestions
- D thin topics that need more sources
- E missing entity pages
- F unresolved contradictions

### Stats
- Total pages: N
- Total sources: M
- Total citations: P
- Graph edges: Q
- Communities: R
```

## --fix Mode
When `--fix` is passed:
- Add missing pages to index
- Remove broken index entries
- Add `[UNTYPED]` markers to unmarked claims
- Create stub pages for frequently-referenced missing entities
- Do NOT auto-resolve contradictions (that needs human judgment)
