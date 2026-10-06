#!/usr/bin/env python3
"""Plan one deduplicated fork issue for a Cursor delta. Writes require --write."""

import argparse
import json
from pathlib import Path
import subprocess

MARKER = "<!-- pstack-cursor-update -->"


def plan_notice(report, issues):
    if not report["changes"]:
        return {"action": "none", "reason": "pstack tree is unchanged"}
    target = report["upstream_target"]
    target_marker = f"<!-- cursor-target:{target} -->"
    tracked = [issue for issue in issues if MARKER in (issue.get("body") or "")
               and issue.get("user", {}).get("login") == "github-actions[bot]"]
    if any(target_marker in (issue.get("body") or "") for issue in tracked):
        return {"action": "none", "reason": "target already reported"}
    body = "\n".join([
        MARKER, target_marker,
        f"Cursor pstack {report['upstream_version']} differs from the recorded source pin.",
        "",
        f"Base: `{report['upstream_base']}`",
        f"Target: `{target}`",
        f"Changed paths: {report['summary']['changed_files']}",
        f"[Source comparison](https://github.com/cursor/plugins/compare/{report['upstream_base']}...{target})",
        "",
        "Review the workflow audit artifact and follow UPSTREAM.md. Preserve the harness adaptations and configured GPT routes.",
        "This notice does not authorize installation, merging, tagging, or release.",
    ])
    notice = {"title": f"Update direct Cursor pstack to {report['upstream_version']}", "body": body}
    opened = sorted((issue for issue in tracked if issue["state"] == "open"), key=lambda issue: issue["number"])
    if opened:
        return {"action": "update", "number": opened[0]["number"], **notice}
    return {"action": "create", **notice}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("audit", type=Path)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    report = json.loads(args.audit.read_text())
    if not report["changes"]:
        print(json.dumps(plan_notice(report, [])))
        return
    pages = subprocess.check_output([
        "gh", "api", "--paginate", "--slurp",
        f"repos/{args.repo}/issues?state=all&creator=github-actions%5Bbot%5D&per_page=100",
    ], text=True)
    issues = [issue for page in json.loads(pages) for issue in page if "pull_request" not in issue]
    plan = plan_notice(report, issues)
    print(json.dumps(plan, indent=2))
    if not args.write or plan["action"] == "none":
        return
    endpoint = f"repos/{args.repo}/issues"
    method = "POST"
    if plan["action"] == "update":
        endpoint += f"/{plan['number']}"
        method = "PATCH"
    subprocess.run([
        "gh", "api", "--method", method, endpoint, "--input", "-",
    ], input=json.dumps({"title": plan["title"], "body": plan["body"]}), text=True, check=True)


if __name__ == "__main__":
    main()
