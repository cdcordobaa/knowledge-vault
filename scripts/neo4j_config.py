#!/usr/bin/env python3
"""
Neo4j Configuration — Connection management and schema initialization.

Usage:
  python scripts/neo4j_config.py --check    # Test connection
  python scripts/neo4j_config.py --init     # Create constraints and indexes
"""

import os
import sys

from neo4j import GraphDatabase

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")

_driver = None


def get_driver():
    global _driver
    if _driver is None:
        if not NEO4J_PASSWORD:
            print("ERROR: NEO4J_PASSWORD environment variable not set.")
            sys.exit(1)
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver


def check_connection():
    try:
        driver = get_driver()
        driver.verify_connectivity()
        print(f"Connected to Neo4j at {NEO4J_URI}")
        return True
    except Exception as e:
        print(f"ERROR: Cannot connect to Neo4j at {NEO4J_URI}")
        print(f"  {e}")
        print(f"  Start with: docker compose up -d")
        return False


def init_schema():
    driver = get_driver()

    constraints = [
        "CREATE CONSTRAINT node_id_unique IF NOT EXISTS FOR (n:WikiNode) REQUIRE n.id IS UNIQUE",
    ]

    indexes = [
        # Full-text index for keyword search
        "CREATE FULLTEXT INDEX node_search IF NOT EXISTS FOR (n:WikiNode) ON EACH [n.id, n.tldr, n.type, n.subtype]",
        # Vector index for semantic search (384d from all-MiniLM-L6-v2)
        """CREATE VECTOR INDEX node_embedding IF NOT EXISTS
           FOR (n:WikiNode) ON (n.tldr_embedding)
           OPTIONS {indexConfig: {
             `vector.dimensions`: 384,
             `vector.similarity_function`: 'cosine'
           }}""",
    ]

    with driver.session() as session:
        for stmt in constraints:
            session.run(stmt)
        for stmt in indexes:
            session.run(stmt)

    print(f"Schema initialized: {len(constraints)} constraints, {len(indexes)} indexes")


def close():
    global _driver
    if _driver:
        _driver.close()
        _driver = None


if __name__ == "__main__":
    if "--check" in sys.argv:
        ok = check_connection()
        sys.exit(0 if ok else 1)
    elif "--init" in sys.argv:
        if not check_connection():
            sys.exit(1)
        init_schema()
    else:
        print(__doc__)
