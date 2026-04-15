---
type: source_summary
source_path: notion://domain-3-context-engineering
source_type: research
ingested_at: 2026-04-13T21:00:00Z
content_hash: notion_domain_3
confidence: high
relations:
  cites: [mei-et-al-2025, mcp-anthropic-2024, graphrag-microsoft-2024, liu-lost-in-middle-2024]
  enables: [apg, daedalus-arch]
  contradicts: [bigger-models-solve-everything]
  related_to: [fitness-functions]
---

> **TLDR:** Context Engineering Theory — the paradigm shift from prompt engineering to designing entire information pipelines. Context quality (not model size) is the primary driver of AI code quality, with graph-based retrieval (GraphRAG) outperforming flat-text RAG.

## Key Claims

[FACT] Mei et al. survey 1,400 papers and establish that context pipeline design — what information reaches the model and how — is a stronger predictor of AI output quality than model scale, contradicting the "bigger is better" assumption. [src: mei-et-al-2025]

[FACT] Liu "Lost in the Middle" demonstrates U-shaped attention in LLMs: information placed in the middle of long contexts is systematically ignored relative to information at the beginning or end, with performance degrading by up to 20%. [src: liu-lost-in-middle-2024]

[FACT] Anthropic's Model Context Protocol (MCP) provides a standardized interface for agent-data communication — described as "USB-C for AI" — and has been adopted by OpenAI, Google, JetBrains, and other major platforms within months of release. [src: mcp-anthropic-2024]

[FACT] Microsoft's GraphRAG combines knowledge graph construction with community summarization to answer global queries (e.g., "what are the main themes across this corpus?") that flat-text RAG fundamentally cannot address. [src: graphrag-microsoft-2024]

[FACT] Kalliamvakou reports that context quality is the single strongest driver of GitHub Copilot suggestion acceptance rates, outweighing model version, prompt length, and user experience level. [src: kalliamvakou-github-2024]

[FACT] The paradigm shift from "prompt engineering" to "context engineering" reframes the problem: prompts are a single input, but context engineering designs the full information pipeline including retrieval, ranking, compression, and placement. [src: mei-et-al-2025]

[FACT] GraphRAG's community detection step clusters related entities and generates hierarchical summaries, enabling multi-hop reasoning that vector-similarity RAG misses because semantic similarity does not capture structural relationships. [src: graphrag-microsoft-2024]

## Cross-Cutting Themes

[INFERENCE] The convergence of MCP adoption across competing platforms suggests context engineering infrastructure is becoming a shared layer, similar to how HTTP standardized web communication — the competitive advantage shifts from "how to connect" to "what context to provide." [inferred from: mcp-anthropic-2024, mei-et-al-2025]

[INFERENCE] Liu's U-shaped attention finding has direct architectural implications: any system feeding context to LLMs must place critical information at context boundaries, making context placement strategy as important as context selection. [inferred from: liu-lost-in-middle-2024, mei-et-al-2025]
