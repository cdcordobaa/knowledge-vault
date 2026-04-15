# SKILL: REFLECT
# The wiki's self-awareness. Synthesizes what changed and why.

## Trigger
Called automatically after every /ingest. Can also be run manually: `/reflect`

## What Reflect Does
After any wiki modification, append a structured entry to `wiki/log.md`.
This is NOT a simple changelog. It's the wiki's REASONING about its own evolution.

## Log Entry Format
```markdown
## [YYYY-MM-DD HH:MM] <operation> | <title>

### What Changed
- Created: <new pages>
- Updated: <modified pages>
- New citations: <count>
- New graph edges: <typed list>

### Why It Changed
<1-2 sentences explaining the causal chain: what source said what, 
which triggered what updates>

### Contradictions Found
- <claim A> [src: X] vs <claim B> [src: Y] — <which is more authoritative and why>
- Resolution: superseded | unresolved | needs human judgment

### Confidence Assessment
- High confidence: <claims well-supported by multiple sources>
- Medium confidence: <claims from single source or inference>
- Low confidence: <claims that are weak or contradicted>

### Gaps Identified
- [GAP] <what the wiki still doesn't know>
- [GAP] <what would be valuable to ingest next>

### Graph Impact
- New communities formed: <if any>
- Bridge nodes identified: <entities connecting otherwise separate clusters>
- Isolated nodes: <entities not yet connected to the main graph>
```

## Why This Matters for a Product
Existing memory products (Mem0, Zep) can tell you WHAT they remember.
They cannot tell you WHY they believe it, WHEN it changed, or HOW CONFIDENT they are.

The reflect log turns your memory into an AUDITABLE system:
- Trace any current belief back through the log to its origin
- See how understanding evolved over time
- Identify moments where the knowledge base pivoted

## Manual Reflect
`/reflect` without a prior operation → generate a SYNTHESIS of recent changes:
- Summarize last 5-10 log entries
- Identify patterns (are we adding knowledge in one domain but not another?)
- Suggest rebalancing (domains that are thin vs. domains that are deep)
- Check for stale sources
