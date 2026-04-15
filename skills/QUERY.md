# SKILL: QUERY
# Answer questions using graph-first retrieval. Every query enriches the wiki.

## Trigger
User asks a question, or says `/query <question>`.

## Pipeline

### Step 1: Graph Retrieval (requires Neo4j: `docker compose up -d`)
```bash
python scripts/graph_query.py "<question_keywords>"
```
This performs hybrid retrieval: full-text search + vector similarity + 2-hop graph expansion.
Returns: relevant nodes, connecting edges, hop-distance, and combined scores.
If Neo4j is not running, fall back to index scan (L1).

### Step 2: Progressive Disclosure
- Read TLDRs of the top-ranked nodes (L2 budget: ~2-5K tokens)
- Decide which pages need full loading
- Load full pages only for directly relevant content (L3 budget: 5-20K tokens)

### Step 3: Synthesize Answer
- Answer the question using compiled wiki content
- Cite wiki pages: `[wiki: entities/motoko.md]`
- Cite original sources through wiki pages: `[src: original.md via wiki: entities/motoko.md]`
- Mark confidence: which parts are FACT, INFERENCE, or uncertain

### Step 4: DUAL OUTPUT (MANDATORY)
Output 1: The answer to the user (in chat or as a file).

Output 2: Wiki updates. ALWAYS do at least one of:
a) **Create an output page** if the query produced novel synthesis:
   Save to `wiki/outputs/YYYY-MM-DD-<slug>.md` with:
   ```yaml
   ---
   type: output
   query: "<the question>"
   derived_at: YYYY-MM-DDTHH:MM:SSZ
   pages_consulted: [list]
   relations:
     derived_from: [pages that informed this]
     cites: [original sources]
   ---
   > **TLDR:** ...
   
   [DERIVED] The synthesis content... [derived from: page1.md, page2.md]
   ```

b) **Update existing pages** if the query revealed new connections:
   - Add cross-references between pages that weren't linked
   - Add new relations to frontmatter
   - Add notes to relevant entity/concept pages

c) **Log the query** in `wiki/log.md`:
   ```markdown
   ## [YYYY-MM-DD HH:MM] query | <short question summary>
   **Consulted:** <pages read>
   **Output:** <output page created, if any>
   **Wiki updates:** <pages modified>
   **New connections:** <relations discovered>
   ```

### Step 5: Graph Update
If new relations were added to any frontmatter:
```bash
python scripts/graph_builder.py
```

## Query Depth Modes
- **fast**: Graph → TLDRs → answer. No full page loading. For quick lookups.
- **deep**: Graph → TLDRs → full pages → cross-reference → answer. For analysis.
- **exhaustive**: Everything above + lint check on relevant pages + gap identification.

Default is `deep`. User can specify: `/query --fast "question"` or `/query --exhaustive "question"`

## Cross-Domain Queries
When a query spans multiple domains (e.g., "how does agent X affect metric Y"):
1. Graph traversal finds the SHORTEST PATH between domains
2. Load all nodes on that path
3. The path itself is the answer structure
4. Create an output page that maps the cross-domain connection

## Resume Mode
`/query --resume` → Read log.md (last 5 entries) + check for stale sources + report:
- What was done recently
- What sources changed
- What gaps were identified
- Suggested next actions
