#!/usr/bin/env python3
"""
Graph Builder — Extracts knowledge graph from wiki markdown frontmatter.
Wiki is source of truth. Graph is derived in Neo4j. Always rebuildable.

Usage:
  python scripts/graph_builder.py                    # Build graph from wiki/
  python scripts/graph_builder.py --stats            # Build + show statistics
  python scripts/graph_builder.py --communities      # Build + detect communities
  python scripts/graph_builder.py --full-rebuild     # Clear graph + rebuild from scratch
  python scripts/graph_builder.py --dry-run          # Parse wiki, show what would change
"""

import sys
from datetime import datetime, timezone
from collections import defaultdict

from wiki_parser import (
    scan_wiki_pages, build_node_data, build_edges, normalize_id,
    TYPE_LABELS, EDGE_WEIGHTS,
)
from neo4j_config import get_driver, check_connection, close
from embeddings import embed_batch


def clear_graph(driver):
    """Delete all WikiNode nodes and their relationships."""
    with driver.session() as session:
        session.run("MATCH (n:WikiNode) DETACH DELETE n")
    print("Graph cleared.")


def upsert_nodes(driver, nodes, embeddings_map):
    """Batch upsert nodes into Neo4j, grouped by type label."""
    # Group nodes by their Neo4j label
    by_label = defaultdict(list)
    for node in nodes:
        label = node.pop("neo4j_label", "WikiNode")
        props = {
            "id": node["id"],
            "path": node["path"],
            "type": node["type"],
            "subtype": node.get("subtype", ""),
            "tldr": node["tldr"],
            "confidence": node["confidence"],
            "source_count": node["source_count"],
            "aliases": node.get("aliases", []),
        }
        if node["id"] in embeddings_map:
            props["tldr_embedding"] = embeddings_map[node["id"]]
        by_label[label].append(props)

    with driver.session() as session:
        for label, node_list in by_label.items():
            # MERGE on WikiNode, then add the type-specific label
            query = f"""
            UNWIND $nodes AS node
            MERGE (n:WikiNode {{id: node.id}})
            SET n += node, n:{label}
            """
            session.run(query, nodes=node_list)

    return sum(len(v) for v in by_label.values())


def upsert_edges(driver, edges):
    """Delete existing outbound edges per source node, then create new ones."""
    # Group edges by source
    by_source = defaultdict(list)
    for edge in edges:
        by_source[edge["source"]].append(edge)

    with driver.session() as session:
        # Delete all outbound edges for nodes we're updating
        source_ids = list(by_source.keys())
        session.run(
            "UNWIND $ids AS sid "
            "MATCH (n:WikiNode {id: sid})-[r]->() DELETE r",
            ids=source_ids,
        )

        # Create edges grouped by type (Cypher needs static relationship types)
        by_type = defaultdict(list)
        for edge in edges:
            by_type[edge["type"]].append(edge)

        for edge_type, edge_list in by_type.items():
            rel_type = edge_type.upper()
            params = [
                {"source": e["source"], "target": e["target"], "weight": e["weight"]}
                for e in edge_list
            ]
            query = f"""
            UNWIND $edges AS edge
            MATCH (a:WikiNode {{id: edge.source}})
            MATCH (b:WikiNode {{id: edge.target}})
            MERGE (a)-[r:{rel_type}]->(b)
            SET r.weight = edge.weight
            """
            session.run(query, edges=params)

    return len(edges)


def remove_orphaned_nodes(driver, current_ids):
    """Remove nodes in Neo4j that no longer exist in wiki/."""
    with driver.session() as session:
        result = session.run(
            "MATCH (n:WikiNode) WHERE NOT n.id IN $ids "
            "WITH n, n.id AS removed_id DETACH DELETE n "
            "RETURN removed_id",
            ids=current_ids,
        )
        removed = [r["removed_id"] for r in result]
    if removed:
        print(f"Removed {len(removed)} orphaned nodes: {', '.join(removed)}")
    return removed


def get_stats(driver):
    """Query graph statistics from Neo4j."""
    with driver.session() as session:
        node_count = session.run(
            "MATCH (n:WikiNode) RETURN count(n) AS c"
        ).single()["c"]

        edge_result = session.run(
            "MATCH ()-[r]->() RETURN type(r) AS t, count(r) AS c ORDER BY c DESC"
        )
        edge_types = {r["t"]: r["c"] for r in edge_result}
        edge_count = sum(edge_types.values())

    return {
        "node_count": node_count,
        "edge_count": edge_count,
        "edge_types": edge_types,
        "built_at": datetime.now(timezone.utc).isoformat(),
    }


def print_stats(stats, communities=None):
    """Print graph statistics."""
    print(f"\n{'='*50}")
    print(f"WIKI MEMORY GRAPH — {stats['built_at']}")
    print(f"{'='*50}")
    print(f"Nodes: {stats['node_count']}")
    print(f"Edges: {stats['edge_count']}")
    print(f"\nEdge types:")
    for etype, count in sorted(stats["edge_types"].items(), key=lambda x: -x[1]):
        print(f"  {etype}: {count}")

    if communities:
        print(f"\nCommunities: {communities['community_count']}")
        for c in communities["communities"]:
            members_preview = ', '.join(c['members'][:5])
            suffix = '...' if len(c['members']) > 5 else ''
            print(f"  Cluster {c['id']}: {c['size']} nodes — {members_preview}{suffix}")
        if communities.get("bridge_nodes"):
            print(f"\nBridge nodes: {', '.join(communities['bridge_nodes'])}")
        if communities.get("isolated_nodes"):
            print(f"Isolated nodes: {', '.join(communities['isolated_nodes'])}")


def build_graph(dry_run=False, full_rebuild=False):
    """Scan wiki/ and push the knowledge graph to Neo4j."""
    if not check_connection():
        sys.exit(1)

    driver = get_driver()

    if full_rebuild:
        clear_graph(driver)

    # Parse all wiki pages
    pages = scan_wiki_pages()
    if not pages:
        print("No wiki pages found in wiki/. Run /ingest first.")
        return None

    nodes = []
    all_edges = []
    tldrs = []

    for filepath, fm, body in pages:
        node = build_node_data(filepath, fm, body)
        nodes.append(node)
        tldrs.append(node["tldr"])

        node_id = normalize_id(filepath)
        edges = build_edges(node_id, fm, body)
        all_edges.extend(edges)

    # Resolve short-name edge targets to full node IDs
    # e.g., "motoko" → "entities/motoko" if that node exists
    node_ids = {n["id"] for n in nodes}
    short_to_full = {}
    for nid in node_ids:
        short_name = nid.rsplit("/", 1)[-1]  # "entities/motoko" → "motoko"
        short_to_full[short_name] = nid

    for edge in all_edges:
        if edge["target"] not in node_ids and edge["target"] in short_to_full:
            edge["target"] = short_to_full[edge["target"]]

    if dry_run:
        print(f"DRY RUN: Would upsert {len(nodes)} nodes and {len(all_edges)} edges")
        for n in nodes:
            print(f"  Node: {n['id']} ({n['type']}) — {n['tldr'][:60]}")
        for e in all_edges:
            print(f"  Edge: {e['source']} --{e['type']}--> {e['target']}")
        return None

    # Generate embeddings for all tldrs
    print(f"Generating embeddings for {len(tldrs)} nodes...")
    vectors = embed_batch(tldrs)
    embeddings_map = {nodes[i]["id"]: vectors[i] for i in range(len(nodes))}

    # Push to Neo4j
    node_count = upsert_nodes(driver, nodes, embeddings_map)
    edge_count = upsert_edges(driver, all_edges)

    current_ids = [n["id"] for n in nodes]
    remove_orphaned_nodes(driver, current_ids)

    stats = get_stats(driver)
    print(f"Graph built: {stats['node_count']} nodes, {stats['edge_count']} edges -> Neo4j")
    return stats


if __name__ == "__main__":
    try:
        do_communities = "--communities" in sys.argv
        do_stats = "--stats" in sys.argv
        do_dry_run = "--dry-run" in sys.argv
        do_full_rebuild = "--full-rebuild" in sys.argv

        stats = build_graph(dry_run=do_dry_run, full_rebuild=do_full_rebuild)

        if stats and (do_communities or do_stats):
            communities = None
            if do_communities:
                from community_detect import detect_communities
                communities = detect_communities()
            print_stats(stats, communities)
    finally:
        close()
