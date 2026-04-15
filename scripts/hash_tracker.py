#!/usr/bin/env python3
"""
Hash Tracker — Source change detection for Wiki Memory Engine.
Zero dependencies. Zero infrastructure. Detects source drift in 2 seconds.

Usage:
  python hash_tracker.py hash <file_path>       # Record hash of a source
  python hash_tracker.py check                   # Check all sources for changes
  python hash_tracker.py check <file_path>       # Check specific source
  python hash_tracker.py status                  # Show all tracked sources
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

HASH_STORE = "graph/hashes.json"


def load_hashes():
    if os.path.exists(HASH_STORE):
        with open(HASH_STORE, "r") as f:
            return json.load(f)
    return {}


def save_hashes(data):
    os.makedirs(os.path.dirname(HASH_STORE), exist_ok=True)
    with open(HASH_STORE, "w") as f:
        json.dump(data, f, indent=2)


def compute_hash(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_hash(filepath):
    """Record hash of a source file."""
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    hashes = load_hashes()
    file_hash = compute_hash(filepath)
    now = datetime.now(timezone.utc).isoformat()

    hashes[filepath] = {
        "hash": file_hash,
        "recorded_at": now,
        "last_checked": now,
        "status": "current"
    }
    save_hashes(hashes)
    print(f"RECORDED: {filepath} → {file_hash[:12]}... at {now}")


def cmd_check(filepath=None):
    """Check sources for changes since recording."""
    hashes = load_hashes()
    if not hashes:
        print("NO SOURCES TRACKED. Use 'hash <file>' to start tracking.")
        return

    targets = {filepath: hashes[filepath]} if filepath else hashes
    changed = []
    missing = []
    current = []

    for path, record in targets.items():
        if not os.path.exists(path):
            missing.append(path)
            record["status"] = "missing"
            continue

        new_hash = compute_hash(path)
        record["last_checked"] = datetime.now(timezone.utc).isoformat()

        if new_hash != record["hash"]:
            changed.append({
                "path": path,
                "old_hash": record["hash"][:12],
                "new_hash": new_hash[:12],
                "recorded_at": record["recorded_at"]
            })
            record["status"] = "changed"
        else:
            current.append(path)
            record["status"] = "current"

    save_hashes(hashes)

    # Output
    if changed:
        print(f"⚠ {len(changed)} SOURCE(S) CHANGED:")
        for c in changed:
            print(f"  CHANGED: {c['path']} (was {c['old_hash']}... now {c['new_hash']}... recorded {c['recorded_at']})")
    if missing:
        print(f"✗ {len(missing)} SOURCE(S) MISSING:")
        for m in missing:
            print(f"  MISSING: {m}")
    if current:
        print(f"✓ {len(current)} source(s) unchanged")

    if not changed and not missing:
        print("ALL SOURCES CURRENT. No drift detected.")

    return {"changed": changed, "missing": missing, "current_count": len(current)}


def cmd_status():
    """Show all tracked sources."""
    hashes = load_hashes()
    if not hashes:
        print("NO SOURCES TRACKED.")
        return

    print(f"TRACKING {len(hashes)} SOURCES:")
    for path, record in sorted(hashes.items()):
        status = record.get("status", "unknown")
        icon = {"current": "✓", "changed": "⚠", "missing": "✗"}.get(status, "?")
        print(f"  {icon} {path} [{status}] recorded {record['recorded_at']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    if command == "hash" and len(sys.argv) >= 3:
        cmd_hash(sys.argv[2])
    elif command == "check":
        cmd_check(sys.argv[2] if len(sys.argv) >= 3 else None)
    elif command == "status":
        cmd_status()
    else:
        print(__doc__)
        sys.exit(1)
