# SKILL: COMPILE
# Transform raw extracted claims into synthesized wiki pages.
# This is what makes compiled memory different from stored memory.

## Trigger
Called as part of /ingest pipeline (Step 4), or manually with `/compile`.

## Compilation Rules

### 1. Synthesis, Not Copy
NEVER copy-paste from sources. Wiki pages are SYNTHESIZED:
- Combine claims from multiple sources into coherent narrative
- Note where sources agree (strengthens confidence)
- Note where sources disagree (flag as contradiction)
- Add context that connects this knowledge to other wiki pages

### 2. Every Claim Gets a Type
```
[FACT] Direct statement from a source [src: file.md]
[INFERENCE] Synthesized by LLM from multiple sources [inferred from: src1.md, src2.md]
[GAP] Something the wiki acknowledges it doesn't know [no source addresses this]
[DERIVED] Produced during a query/analysis session [derived from query: YYYY-MM-DD]
```

### 3. Contradiction Handling
When a new source contradicts an existing claim:
- Do NOT silently replace
- Add BOTH claims with their sources
- Mark: `[CONTRADICTS: <page>#<claim> from src: <other_source>]`
- Add a `contradicts` relation in frontmatter of BOTH pages
- Add a `supersedes` relation if the new source is clearly newer/more authoritative
- Log the contradiction in reflect step

### 4. TLDR First
Every page MUST start with:
```
> **TLDR:** 2-3 sentences. This is what the progressive disclosure system reads
> before deciding whether to load the full page. Make it count.
```

### 5. Frontmatter Relations (MANDATORY)
Every page MUST have typed relations in frontmatter:
```yaml
relations:
  depends_on: []      # What this requires to function/exist
  generates: []       # What this produces
  cites: []           # Source files
  contradicts: []     # Conflicting pages/claims
  supersedes: []      # Older claims this replaces
  measured_by: []     # How this is evaluated
  derived_from: []    # Analysis that produced this
  enables: []         # What this makes possible
  blocks: []          # What this prevents
  related_to: []      # Semantic connections (weaker than above)
```
Only include non-empty relations. Don't add empty arrays.

### 6. Wikilinks
Use `[[page_name]]` for every cross-reference. These become navigable in Obsidian
and parseable by the graph builder.

### 7. Page Types and Templates
Use the templates in `templates/` directory:
- `entity.md` → people, orgs, agents, products
- `concept.md` → topics, methodologies, patterns
- `source_summary.md` → per-source extraction
- `output.md` → query-derived synthesis

### 8. Deduplication
Before creating a new page, check if a page for this entity/concept exists.
Check by: exact name match, alias match (check `aliases:` in frontmatter),
semantic similarity (same topic, different name).
If exists → UPDATE, don't create duplicate.

### 9. Update Cascade
When updating a page, check: do any other pages cite or depend on the changed claims?
If yes → update their TLDRs and relations too.
This is what "compiled memory" means — changes propagate.
