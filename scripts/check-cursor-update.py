#!/usr/bin/env python3
"""Report a direct Cursor pstack delta. Fetching and notices belong to the caller."""

import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--port", default="HEAD")
parser.add_argument("--upstream", default="cursor/main")
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--github-output", type=Path)
args = parser.parse_args()
result = subprocess.run(
    [sys.executable, str(ROOT / "scripts/upstream-audit.py"), "--port", args.port,
     "--upstream", args.upstream], cwd=ROOT, capture_output=True, text=True,
)
if result.returncode:
    sys.stderr.write(result.stderr)
    sys.exit(result.returncode)
report = json.loads(result.stdout)
changed = bool(report["changes"])
args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
if args.github_output:
    with args.github_output.open("a") as output:
        output.write(f"changed={str(changed).lower()}\n")
        output.write(f"target={report['upstream_target']}\n")
print(f"Cursor {report['upstream_version']}: {report['summary']['changed_files']} changed pstack paths")
