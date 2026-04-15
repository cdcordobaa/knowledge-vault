#!/usr/bin/env python3
"""
Graph Query — Find relevant wiki pages using hybrid text+vector+graph retrieval.
Uses Neo4j full-text index, vector similarity, and Cypher graph traversal.

Usage:
  python scripts/graph_query.py "<keywords>"                    # Find relevant nodes
  python scripts/graph_query.py path "<entity_a>" "<entity_b>"  # Shortest path
  python scripts/graph_query.py neighbors "<entity>"             # Direct connections
  python scripts/graph_query.py gaps                             # Find structural holes
"""

import sys

from neo4j_config import get_driver, check_connection, close
from embeddings import embed_text

# Weights for combining text and vector search scores
TEXT_WEIGHT = 0.6
VECTOR_WEIGHT = 0.4


def cmd_query(keywords_str):
    """Find relevant nodes by hybrid text+vector search + graph expansion."""
    if not check_connection():
        sys.exit(1)

    driver = get_driver()

    # Phase 1: Full-text search
    text_results = {}
    with driver.session() as session:
        result = session.run(
            "CALL db.index.fulltext.queryNodes('node_search', $search_text) "
            "YIELD node, score "
            "RETURN node.id AS id, node.tldr AS tldr, node.type AS type, "
            "       node.path AS path, node.aliases AS aliases, score "
            "ORDER BY score DESC LIMIT 10",
            search_text=keywords_str,
        )
        for r in result:
            text_results[r["id"]] = {
                "id": r["id"], "tldr": r["tldr"] or "", "type": r["type"] or "?",
                "path": r["path"] or "?", "aliases": r["aliases"] or [],
                "text_score": r["score"],
            }

    # Phase 2: Vector similarity search
    query_embedding = embed_text(keywords_str)
    vector_results = {}
    with driver.session() as session:
        result = session.run(
            "CALL db.index.vector.queryNodes('node_embedding', 10, $embedding) "
            "YIELD node, score "
            "RETURN node.id AS id, node.tldr AS tldr, node.type AS type, "
            "       node.path AS path, score",
            embedding=query_embedding,
        )
        for r in result:
            vector_results[r["id"]] = {
                "id": r["id"], "tldr": r["tldr"] or "", "type": r["type"] or "?",
                "path": r["path"] or "?",
                "vector_score": r["score"],
            }

    # Phase 3: Combine scores
    all_ids = set(text_results.keys()) | set(vector_results.keys())
    combined = {}
    for nid in all_ids:
        text_score = text_results.get(nid, {}).get("text_score", 0)
        vector_score = vector_results.get(nid, {}).get("vector_score", 0)
        score = text_score * TEXT_WEIGHT + vector_score * VECTOR_WEIGHT
        info = text_results.get(nid) or vector_results.get(nid)
        combined[nid] = {
            "score": score,
            "tldr": info["tldr"],
            "type": info["type"],
            "path": info["path"],
        }

    # Take top 5 seeds for graph expansion
    seeds = sorted(combined.items(), key=lambda x: -x[1]["score"])[:5]
    seed_ids = [s[0] for s in seeds]

    if not seed_ids:
        print("NO MATCHES FOUND. Try different keywords.")
        return

    # Phase 4: 2-hop graph expansion via Cypher
    expanded = {}
    for sid, info in seeds:
        expanded[sid] = {"score": info["score"], "hops": 0, "edges": [], **info}

    with driver.session() as session:
        result = session.run(
            "MATCH (seed:WikiNode) WHERE seed.id IN $seed_ids "
            "OPTIONAL MATCH (seed)-[r1]-(hop1:WikiNode) "
            "OPTIONAL MATCH (hop1)-[r2]-(hop2:WikiNode) "
            "WHERE hop2.id <> seed.id AND NOT hop2.id IN $seed_ids "
            "RETURN seed.id AS seed, "
            "       hop1.id AS hop1_id, hop1.tldr AS hop1_tldr, hop1.type AS hop1_type, "
            "       hop1.path AS hop1_path, type(r1) AS r1_type, r1.weight AS r1_weight, "
            "       hop2.id AS hop2_id, hop2.tldr AS hop2_tldr, hop2.type AS hop2_type, "
            "       hop2.path AS hop2_path, type(r2) AS r2_type, r2.weight AS r2_weight",
            seed_ids=seed_ids,
        )
        for r in result:
            seed_score = expanded.get(r["seed"], {}).get("score", 0)

            # 1-hop neighbor
            if r["hop1_id"] and r["hop1_id"] not in seed_ids:
                hop1_score = seed_score * (r["r1_weight"] or 0.5) * 0.7
                edge_str = f"{r['seed']} --{r['r1_type']}--> {r['hop1_id']}"
                if r["hop1_id"] not in expanded or expanded[r["hop1_id"]]["score"] < hop1_score:
                    expanded[r["hop1_id"]] = {
                        "score": hop1_score, "hops": 1, "edges": [edge_str],
                        "tldr": r["hop1_tldr"] or "", "type": r["hop1_type"] or "?",
                        "path": r["hop1_path"] or "?",
                    }

            # 2-hop neighbor
            if r["hop2_id"] and r["hop1_id"]:
                hop1_score_base = seed_score * (r["r1_weight"] or 0.5) * 0.7
                hop2_score = hop1_score_base * (r["r2_weight"] or 0.5) * 0.5
                edge1 = f"{r['seed']} --{r['r1_type']}--> {r['hop1_id']}"
                edge2 = f"{r['hop1_id']} --{r['r2_type']}--> {r['hop2_id']}"
                if r["hop2_id"] not in expanded or expanded[r["hop2_id"]]["score"] < hop2_score:
                    expanded[r["hop2_id"]] = {
                        "score": hop2_score, "hops": 2, "edges": [edge1, edge2],
                        "tldr": r["hop2_tldr"] or "", "type": r["hop2_type"] or "?",
                        "path": r["hop2_path"] or "?",
                    }

    # Rank and output
    ranked = sorted(expanded.items(), key=lambda x: -x[1]["score"])[:15]

    print(f'QUERY: "{keywords_str}"')
    print(f"FOUND: {len(ranked)} relevant nodes\n")

    for node_id, info in ranked:
        tldr = info.get("tldr", "(no TLDR)")
        hops = info["hops"]
        score = info["score"]
        node_type = info.get("type", "?")
        path_info = info.get("path", "?")

        hop_label = {0: "DIRECT", 1: "1-hop", 2: "2-hop"}[hops]
        print(f"  [{hop_label}] {node_id} ({node_type}) — score: {score:.2f}")
        print(f"    TLDR: {str(tldr)[:120]}")
        print(f"    Path: {path_info}")
        if info["edges"]:
            print(f"    Via: {' -> '.join(info['edges'])}")
        print()


def cmd_path(entity_a, entity_b):
    """Find shortest path between two entities using Cypher."""
    if not check_connection():
        sys.exit(1)

    driver = get_driver()

    with driver.session() as session:
        # Find matching start and end nodes
        start = session.run(
            "MATCH (n:WikiNode) WHERE toLower(n.id) CONTAINS $q "
            "RETURN n.id AS id LIMIT 1",
            q=entity_a.lower().replace(" ", "_"),
        ).single()

        end = session.run(
            "MATCH (n:WikiNode) WHERE toLower(n.id) CONTAINS $q "
            "RETURN n.id AS id LIMIT 1",
            q=entity_b.lower().replace(" ", "_"),
        ).single()

        if not start:
            print(f"NOT FOUND: {entity_a}")
            return
        if not end:
            print(f"NOT FOUND: {entity_b}")
            return

        start_id = start["id"]
        end_id = end["id"]

        result = session.run(
            "MATCH p = shortestPath((a:WikiNode {id: $start})-[*..10]-(b:WikiNode {id: $end})) "
            "RETURN [n IN nodes(p) | n.id] AS node_ids, "
            "       [n IN nodes(p) | n.tldr] AS tldrs, "
            "       [r IN relationships(p) | type(r)] AS rel_types, "
            "       length(p) AS hops",
            start=start_id, end=end_id,
        ).single()

        if not result:
            print(f"NO PATH between {start_id} and {end_id}")
            return

        node_ids = result["node_ids"]
        tldrs = result["tldrs"]
        rel_types = result["rel_types"]
        hops = result["hops"]

        print(f"PATH: {start_id} -> {end_id} ({hops} hops)\n")
        for i, node_id in enumerate(node_ids):
            prefix = "  " * i
            if i > 0:
                print(f"{prefix}--{rel_types[i-1]}-->")
            tldr = (tldrs[i] or "")[:80]
            print(f"{prefix}[{node_id}] {tldr}")


def cmd_neighbors(entity):
    """Show all direct connections of an entity."""
    if not check_connection():
        sys.exit(1)

    driver = get_driver()

    with driver.session() as session:
        node = session.run(
            "MATCH (n:WikiNode) WHERE toLower(n.id) CONTAINS $q "
            "RETURN n.id AS id, n.tldr AS tldr LIMIT 1",
            q=entity.lower().replace(" ", "_"),
        ).single()

        if not node:
            print(f"NOT FOUND: {entity}")
            return

        node_id = node["id"]
        print(f"NEIGHBORS OF: {node_id}")
        print(f"TLDR: {node['tldr'] or '(none)'}\n")

        outbound = session.run(
            "MATCH (n:WikiNode {id: $id})-[r]->(t:WikiNode) "
            "RETURN type(r) AS rel_type, t.id AS target, t.tldr AS tldr",
            id=node_id,
        )
        out_list = list(outbound)

        inbound = session.run(
            "MATCH (s:WikiNode)-[r]->(n:WikiNode {id: $id}) "
            "RETURN type(r) AS rel_type, s.id AS source, s.tldr AS tldr",
            id=node_id,
        )
        in_list = list(inbound)

        if out_list:
            print("OUTBOUND:")
            for r in out_list:
                tldr = (r["tldr"] or "")[:80]
                print(f"  --{r['rel_type']}--> {r['target']}: {tldr}")

        if in_list:
            print("\nINBOUND:")
            for r in in_list:
                tldr = (r["tldr"] or "")[:80]
                print(f"  <--{r['rel_type']}-- {r['source']}: {tldr}")

        if not out_list and not in_list:
            print("  (isolated — no connections)")


def cmd_gaps():
    """Find structural holes in the graph."""
    if not check_connection():
        sys.exit(1)

    driver = get_driver()

    with driver.session() as session:
        # Check if community_id exists on nodes
        has_communities = session.run(
            "MATCH (n:WikiNode) WHERE n.community_id IS NOT NULL "
            "RETURN count(n) AS c"
        ).single()["c"]

        if has_communities == 0:
            print("No communities detected. Run: python scripts/graph_builder.py --communities")
            return

        # Get community count
        comm_count = session.run(
            "MATCH (n:WikiNode) WHERE n.community_id IS NOT NULL "
            "RETURN count(DISTINCT n.community_id) AS c"
        ).single()["c"]

        # Find community pairs with no cross-edges
        result = session.run(
            "MATCH (a:WikiNode), (b:WikiNode) "
            "WHERE a.community_id IS NOT NULL AND b.community_id IS NOT NULL "
            "  AND a.community_id < b.community_id "
            "WITH DISTINCT a.community_id AS ca, b.community_id AS cb "
            "OPTIONAL MATCH (x:WikiNode {community_id: ca})-[r]-(y:WikiNode {community_id: cb}) "
            "WITH ca, cb, count(r) AS cross "
            "WHERE cross = 0 "
            "RETURN ca, cb"
        )
        gaps = list(result)

        print(f"STRUCTURAL GAPS IN {comm_count} COMMUNITIES:\n")

        if gaps:
            for g in gaps:
                # Get member previews for each community
                members_a = session.run(
                    "MATCH (n:WikiNode {community_id: $c}) RETURN n.id AS id LIMIT 3",
                    c=g["ca"],
                )
                members_b = session.run(
                    "MATCH (n:WikiNode {community_id: $c}) RETURN n.id AS id LIMIT 3",
                    c=g["cb"],
                )
                ma = ', '.join(r["id"] for r in members_a)
                mb = ', '.join(r["id"] for r in members_b)
                print(f"  GAP: Community {g['ca']} ({ma}) <-?-> Community {g['cb']} ({mb})")
                print(f"    -> What connects these domains?\n")
        else:
            print("  No structural gaps found — all communities are connected.")

        # Isolated nodes
        isolated = session.run(
            "MATCH (n:WikiNode) WHERE NOT (n)--() RETURN n.id AS id"
        )
        isolated_list = [r["id"] for r in isolated]

        if isolated_list:
            print(f"\nISOLATED NODES (not connected):")
            for nid in isolated_list:
                print(f"  * {nid}")


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print(__doc__)
            sys.exit(1)

        cmd = sys.argv[1]
        if cmd == "path" and len(sys.argv) >= 4:
            cmd_path(sys.argv[2], sys.argv[3])
        elif cmd == "neighbors" and len(sys.argv) >= 3:
            cmd_neighbors(sys.argv[2])
        elif cmd == "gaps":
            cmd_gaps()
        else:
            cmd_query(" ".join(sys.argv[1:]))
    finally:
        close()
