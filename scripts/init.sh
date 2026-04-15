#!/usr/bin/env bash
# Wiki Memory Engine — Init Script
# Run this once to set up the directory structure and Neo4j.
# Usage: bash scripts/init.sh [wiki_name]

WIKI_NAME="${1:-my-wiki}"
echo "Initializing Wiki Memory Engine: $WIKI_NAME"

# Create directory structure
mkdir -p raw
mkdir -p wiki/{entities,concepts,sources,outputs,troubleshooting}
mkdir -p graph
mkdir -p scripts
mkdir -p templates
mkdir -p skills

# Create index.md
cat > wiki/index.md << 'EOF'
# Wiki Index
Last updated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Entities
<!-- Entity pages listed here -->

## Concepts
<!-- Concept pages listed here -->

## Sources
<!-- Source summary pages listed here -->

## Outputs
<!-- Query-derived pages listed here -->

---
Pages: 0 | Sources: 0 | Citations: 0 | Graph edges: 0
EOF

# Create log.md
cat > wiki/log.md << 'EOF'
# Wiki Memory Log
Append-only record of all operations.

---
EOF

echo ""
echo "Directory structure created"
echo "wiki/index.md initialized"
echo "wiki/log.md initialized"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "WARNING: pip not found. Install manually: pip install -r requirements.txt"
fi

# Start Neo4j
echo ""
if command -v docker &> /dev/null; then
    echo "Starting Neo4j..."
    docker compose up -d
    echo "Waiting for Neo4j to be ready..."
    sleep 10
    python3 scripts/neo4j_config.py --init
else
    echo "WARNING: Docker not found. Install Docker and run:"
    echo "  docker compose up -d"
    echo "  python scripts/neo4j_config.py --init"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Drop source files into raw/"
echo "  2. Tell Claude Code: /ingest raw/<filename>"
echo "  3. Ask questions: /query 'your question'"
echo "  4. Health check: /lint"
echo "  5. See the graph: /graph communities"
echo ""
echo "The CLAUDE.md file is your schema. Claude Code reads it automatically."
