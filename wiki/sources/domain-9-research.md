---
type: source_summary
source_path: notion://2131c5978be44eb5b0e85a364b719e4b
source_type: research
ingested_at: 2026-04-13T21:00:00Z
content_hash: notion_domain9
confidence: high
relations:
  cites: [ox-security-2025, li-et-al-2022, slopcodebench-2026, veribench-iclr-2026, agentsight-2025, toolfuzz-2025, conflictlens-2025, opa, firecracker, a2a-protocol]
  extracted_to: [architecture-erosion, daedalus-arch, neuro-symbolic-compliance]
  enables: [daedalus-arch, architecture-erosion]
---

> **TLDR:** Comprehensive research summary covering 11 sections of the architecture firewall literature: architecture erosion (OX Security, Li et al., SlopCodeBench), semantic merge conflicts (SafeMerge, ConflictLens), runtime observability (AgentSight/eBPF), adversarial validation (ToolFuzz, PBT), multi-agent coordination (AgentSpawn, A2A/MCP), execution isolation (Firecracker), formal verification (vericoding, proof-carrying code), and policy-as-code (OPA, Governance-as-Code).

## Key Claims
[FACT] OX Security analyzed 300+ repositories, finding 10 critical anti-patterns at 80-90% prevalence in AI-generated code.
[FACT] VeriBench (ICLR 2026): same model goes from 12.5% to ~90% compilation when embedded in agentic loop with deterministic feedback.
[FACT] AgentSight provides eBPF-based system-level observability with under 3% performance overhead.
[FACT] ToolFuzz discovered 20x more erroneous inputs than prompt-engineering approaches across 67 LangChain/custom tools.
[FACT] Google A2A Protocol (2025): 150+ technology partners for standardized agent-to-agent communication.
[FACT] Vericoding benchmark: 82% success in Dafny, 68%→96% year-over-year improvement.

## Cross-Cutting Themes
[INFERENCE] The literature converges on a 4-tier layered defense: (1) Pre-generation context guards, (2) Architecture firewall, (3) Semantic integration layer, (4) Human exception handler. [inferred from: all sections]
