#!/usr/bin/env python3
"""
Wiki Parser — Shared functions for parsing wiki markdown frontmatter.
Used by graph_builder.py, graph_query.py, and community_detect.py.
"""

import os
import re

WIKI_DIR = "wiki"

# Edge types and their weights for retrieval scoring
EDGE_WEIGHTS = {
    "depends_on": 1.0,
    "generates": 1.0,
    "enables": 1.0,
    "blocks": 1.0,
    "cites": 0.9,
    "derived_from": 0.9,
    "contradicts": 0.8,
    "supersedes": 0.8,
    "measured_by": 0.7,
    "related_to": 0.4,
    "mentions": 0.2,
}

# Map wiki page types to Neo4j labels
TYPE_LABELS = {
    "entity": "Entity",
    "concept": "Concept",
    "source_summary": "Source",
    "output": "Output",
    "troubleshooting": "Troubleshooting",
}


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content.
    Returns (frontmatter_dict, body_text)."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 3:].strip()

    fm = {}
    current_key = None
    current_list = None
    in_nested = None
    nested_dict = None

    for line in fm_text.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        indent = len(line) - len(line.lstrip())

        if in_nested and indent == 0 and ":" in stripped:
            fm[in_nested] = nested_dict
            in_nested = None
            nested_dict = None

        if in_nested and indent > 0:
            if ":" in stripped and not stripped.startswith("-"):
                key, _, value = stripped.partition(":")
                key = key.strip()
                value = value.strip()
                if value.startswith("[") and value.endswith("]"):
                    items = [i.strip().strip("'\"") for i in value[1:-1].split(",") if i.strip()]
                    nested_dict[key] = items
                elif value == "" or value == "[]":
                    nested_dict[key] = []
                    current_key = key
                else:
                    nested_dict[key] = value.strip("'\"")
            elif stripped.startswith("- ") and current_key and current_key in nested_dict:
                item = stripped[2:].strip().strip("'\"")
                if isinstance(nested_dict.get(current_key), list):
                    nested_dict[current_key].append(item)
            continue

        if ":" in stripped and not stripped.startswith("-"):
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()

            if value == "" or value == "[]":
                if key in ("relations",):
                    in_nested = key
                    nested_dict = {}
                    current_key = None
                else:
                    current_key = key
                    current_list = []
                    fm[key] = current_list
            elif value.startswith("[") and value.endswith("]"):
                items = [i.strip().strip("'\"") for i in value[1:-1].split(",") if i.strip()]
                fm[key] = items
                current_key = key
                current_list = None
            else:
                fm[key] = value.strip("'\"")
                current_key = key
                current_list = None
        elif stripped.startswith("- ") and current_key:
            item = stripped[2:].strip().strip("'\"")
            if isinstance(fm.get(current_key), list):
                fm[current_key].append(item)

    if in_nested and nested_dict is not None:
        fm[in_nested] = nested_dict

    return fm, body


def extract_wikilinks(body):
    """Extract [[wikilinks]] from markdown body text."""
    pattern = r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]'
    return list(set(re.findall(pattern, body)))


def normalize_id(page_path):
    """Convert file path to node ID."""
    return page_path.replace(WIKI_DIR + "/", "").replace(".md", "")


def extract_tldr(body):
    """Extract TLDR from page body."""
    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("> **TLDR:**") or line.startswith("> **TLDR**:"):
            return line.replace("> **TLDR:**", "").replace("> **TLDR**:", "").strip()
    return ""


def scan_wiki_pages():
    """Scan all wiki markdown pages. Returns list of (filepath, frontmatter, body) tuples."""
    pages = []
    for root, dirs, files in os.walk(WIKI_DIR):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            if fname in ("index.md", "log.md"):
                continue
            filepath = os.path.join(root, fname)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            fm, body = parse_frontmatter(content)
            pages.append((filepath, fm, body))
    return pages


def build_node_data(filepath, fm, body):
    """Build a node dict from a parsed wiki page."""
    node_id = normalize_id(filepath)

    relations_block = fm.get("relations", {})
    if not isinstance(relations_block, dict):
        relations_block = {}
    cites_list = relations_block.get("cites", fm.get("cites", []))
    if isinstance(cites_list, str):
        cites_list = [cites_list]
    if not isinstance(cites_list, list):
        cites_list = []

    page_type = fm.get("type", "unknown")

    return {
        "id": node_id,
        "path": filepath,
        "type": page_type,
        "subtype": fm.get("subtype", ""),
        "tldr": extract_tldr(body),
        "confidence": fm.get("confidence", "medium"),
        "source_count": len(cites_list),
        "aliases": fm.get("aliases", []),
        "neo4j_label": TYPE_LABELS.get(page_type, "WikiNode"),
    }


def build_edges(node_id, fm, body):
    """Build edge list from a parsed wiki page's frontmatter and body."""
    edges = []

    relations = fm.get("relations", {})
    if not isinstance(relations, dict):
        relations = {}

    for edge_type in EDGE_WEIGHTS:
        if edge_type == "mentions":
            continue
        targets = relations.get(edge_type, [])
        if isinstance(targets, str):
            targets = [targets]
        if not isinstance(targets, list):
            targets = []
        for target in targets:
            if target:
                target_clean = target.strip().replace(" ", "_").lower()
                edges.append({
                    "source": node_id,
                    "target": target_clean,
                    "type": edge_type,
                    "weight": EDGE_WEIGHTS[edge_type],
                })

    # Wikilinks as MENTIONS edges (weaker)
    wikilinks = extract_wikilinks(body)
    existing_targets = {e["target"] for e in edges}
    for link in wikilinks:
        link_normalized = link.strip().replace(" ", "_").lower()
        if link_normalized not in existing_targets:
            edges.append({
                "source": node_id,
                "target": link_normalized,
                "type": "mentions",
                "weight": EDGE_WEIGHTS["mentions"],
            })

    return edges
