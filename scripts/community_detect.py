#!/usr/bin/env python3
"""
Community Detection — Detect knowledge clusters using Neo4j GDS Louvain.
Falls back to BFS connected components if GDS is not available.

Usage:
  python scripts/community_detect.py              # Detect communities
  python scripts/community_detect.py --stats      # Detect + print summary
"""

import sys
from collections import defaultdict, deque

from neo4j_config import get_driver, check_connection, close


def detect_communities_gds(driver):
    """Use Neo4j GDS Louvain algorithm for community detection."""
    with driver.session() as session:
        # Drop existing projection if any
        try:
            session.run("CALL gds.graph.drop('wiki-graph', false)")
        except Exception:
            pass

        # Project the graph into GDS
        session.run(
            "CALL gds.graph.project("
            "  'wiki-graph', 'WikiNode', '*', "
            "  {relationshipProperties: 'weight'}"
            ")"
        )

        # Run Louvain community detection, write back to nodes
        result = session.run(
            "CALL gds.louvain.write('wiki-graph', {"
            "  writeProperty: 'community_id',"
            "  relationshipWeightProperty: 'weight'"
            "}) "
            "YIELD communityCount, modularity"
        ).single()

        community_count = result["communityCount"]
        modularity = result["modularity"]

        # Drop projection
        session.run("CALL gds.graph.drop('wiki-graph', false)")

    return community_count, modularity


def detect_communities_bfs(driver):
    """Fallback: BFS connected components when GDS is not available."""
    with driver.session() as session:
        # Get all nodes and edges
        nodes_result = session.run("MATCH (n:WikiNode) RETURN n.id AS id")
        all_nodes = [r["id"] for r in nodes_result]

        edges_result = session.run(
            "MATCH (a:WikiNode)-[r]->(b:WikiNode) "
            "RETURN a.id AS source, b.id AS target"
        )
        adjacency = defaultdict(set)
        for r in edges_result:
            adjacency[r["source"]].add(r["target"])
            adjacency[r["target"]].add(r["source"])

    # BFS connected components
    visited = set()
    communities = []

    def bfs(start):
        queue = deque([start])
        component = set()
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            component.add(node)
            for neighbor in adjacency.get(node, set()):
                if neighbor not in visited:
                    queue.append(neighbor)
        return component

    for node_id in all_nodes:
        if node_id not in visited:
            component = bfs(node_id)
            if component:
                communities.append(sorted(list(component)))

    # Write community_id back to Neo4j
    with driver.session() as session:
        for i, members in enumerate(communities):
            session.run(
                "UNWIND $ids AS nid "
                "MATCH (n:WikiNode {id: nid}) SET n.community_id = $comm",
                ids=members, comm=i,
            )

    return len(communities), None


def get_community_details(driver):
    """Query community memberships, bridge nodes, and isolated nodes."""
    with driver.session() as session:
        # Community memberships
        result = session.run(
            "MATCH (n:WikiNode) WHERE n.community_id IS NOT NULL "
            "RETURN n.community_id AS comm, collect(n.id) AS members "
            "ORDER BY size(collect(n.id)) DESC"
        )
        communities = []
        for r in result:
            communities.append({
                "id": r["comm"],
                "members": r["members"],
                "size": len(r["members"]),
            })

        # Bridge nodes (connected to multiple communities)
        bridge_result = session.run(
            "MATCH (n:WikiNode)-[r]-(m:WikiNode) "
            "WHERE n.community_id IS NOT NULL AND m.community_id IS NOT NULL "
            "  AND n.community_id <> m.community_id "
            "RETURN DISTINCT n.id AS id"
        )
        bridges = sorted([r["id"] for r in bridge_result])

        # Isolated nodes
        isolated_result = session.run(
            "MATCH (n:WikiNode) WHERE NOT (n)--() RETURN n.id AS id"
        )
        isolated = sorted([r["id"] for r in isolated_result])

    return {
        "communities": communities,
        "bridge_nodes": bridges,
        "isolated_nodes": isolated,
        "community_count": len(communities),
    }


def detect_communities():
    """Run community detection and return results."""
    if not check_connection():
        sys.exit(1)

    driver = get_driver()

    # Try GDS first, fall back to BFS
    try:
        count, modularity = detect_communities_gds(driver)
        method = "GDS Louvain"
        if modularity is not None:
            print(f"Community detection ({method}): {count} communities, modularity={modularity:.3f}")
        else:
            print(f"Community detection ({method}): {count} communities")
    except Exception as e:
        if "gds" in str(e).lower() or "procedure" in str(e).lower():
            print("GDS not available, falling back to BFS connected components...")
            count, _ = detect_communities_bfs(driver)
            method = "BFS"
            print(f"Community detection ({method}): {count} communities")
        else:
            raise

    return get_community_details(driver)


def print_community_stats(details):
    """Print community detection results."""
    print(f"\nCommunities: {details['community_count']}")
    for c in details["communities"]:
        members_preview = ', '.join(c['members'][:5])
        suffix = '...' if len(c['members']) > 5 else ''
        print(f"  Cluster {c['id']}: {c['size']} nodes — {members_preview}{suffix}")
    if details["bridge_nodes"]:
        print(f"\nBridge nodes: {', '.join(details['bridge_nodes'])}")
    if details["isolated_nodes"]:
        print(f"Isolated nodes: {', '.join(details['isolated_nodes'])}")


if __name__ == "__main__":
    try:
        details = detect_communities()
        if "--stats" in sys.argv or len(sys.argv) == 1:
            print_community_stats(details)
    finally:
        close()
