#!/usr/bin/env python3
"""PostToolUse hook (Edit/Write): validate an edited schema file right away.

Checks it is valid JSON and a valid JSON Schema (draft 2020-12) using check-jsonschema, the same
check CI runs. Problems go back to Claude (exit 2) to fix.
"""
import json
import shutil
import subprocess
import sys

data = json.load(sys.stdin)
path = data.get("tool_input", {}).get("file_path", "")
if not path.endswith(".schema.json"):
    sys.exit(0)
try:
    json.load(open(path))
except Exception as e:  # noqa: BLE001
    print(f"{path} is not valid JSON: {e}", file=sys.stderr)
    sys.exit(2)
tool = shutil.which("check-jsonschema")
if tool:
    r = subprocess.run([tool, "--check-metaschema", path], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        print(f"{path} is not a valid JSON Schema:\n{(r.stdout + r.stderr).strip()}", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
