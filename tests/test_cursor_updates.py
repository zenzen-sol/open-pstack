import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("notice", ROOT / "scripts/cursor-update-notice.py")
notice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(notice)


class CursorAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.repo / "scripts").mkdir()
        for name in ("upstream-audit.py", "check-cursor-update.py", "upstream-merge.py", "upstream-merge-probe.py"):
            shutil.copy(ROOT / "scripts" / name, self.repo / "scripts" / name)
        self.write("pstack/.cursor-plugin/plugin.json", '{"version":"0.15.1"}')
        self.write("pstack/README.md", "original\n")
        self.write("pstack/skills/example/SKILL.md", "original skill\n")
        self.write("pstack/skills/retired/SKILL.md", "retired\n")
        self.write("pstack/skills/changed/SKILL.md", "original changed\n")
        self.write("pstack/docs/guide.md", "Cursor instructions\n")
        self.base = self.commit("Cursor base")
        self.git("branch", "cursor-base")
        self.git("switch", "-q", "-c", "port")
        self.write("UPSTREAM.md", f"| Commit | `{self.base}` |\n")
        self.write("plugins/pstack/.claude-plugin/plugin.json", '{"version":"1.0.0"}')
        self.write("README-UPSTREAM.md", "original\n")
        self.write("plugins/pstack/skills/example/SKILL.md", "adapted skill\n")
        self.write("plugins/pstack/skills/retired/SKILL.md", "retired\n")
        self.write("plugins/pstack/skills/changed/SKILL.md", "original changed\n")
        self.write("plugins/pstack/skills/local/SKILL.md", "local helper\n")
        self.port = self.commit("Port adaptations")
        self.git("switch", "-q", "cursor-base")
        self.write("pstack/.cursor-plugin/plugin.json", '{"version":"0.15.15"}')
        self.write("pstack/skills/example/SKILL.md", "new upstream skill\n")
        self.write("pstack/skills/changed/SKILL.md", "changed upstream\n")
        self.write("pstack/skills/new/SKILL.md", "new skill\n")
        (self.repo / "pstack/skills/retired/SKILL.md").unlink()
        self.target = self.commit("Cursor update")
        self.git("switch", "-q", "port")

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True).strip()

    def write(self, path, text):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text)

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def audit(self, target=None):
        return json.loads(subprocess.check_output([
            sys.executable, "scripts/upstream-audit.py", "--port", self.port,
            "--upstream", target or self.target,
        ], cwd=self.repo, text=True))

    def test_accounts_for_source_delta_without_mutation(self):
        before = self.git("status", "--porcelain")
        report = self.audit()
        rows = {row["upstream_path"]: row for row in report["changes"]}
        self.assertEqual(report["summary"]["by_change"], {"add": 1, "delete": 1, "modify": 3})
        self.assertEqual(rows["pstack/skills/example/SKILL.md"]["comparison"], "port-diverged-review")
        self.assertEqual(rows["pstack/skills/changed/SKILL.md"]["comparison"], "unchanged-since-base")
        self.assertEqual(rows["pstack/.cursor-plugin/plugin.json"]["comparison"], "distribution-review")
        self.assertIn("plugins/pstack/skills/local/SKILL.md", report["port_only_files"])
        self.assertEqual(self.git("status", "--porcelain"), before)
        self.assertEqual(self.git("rev-parse", "HEAD"), self.port)

    def test_unrelated_cursor_commit_does_not_raise_update(self):
        self.git("switch", "-q", "-c", "unrelated", self.base)
        self.write("other-plugin/README.md", "unrelated\n")
        target = self.commit("Unrelated plugin")
        self.git("switch", "-q", "port")
        result = subprocess.run([
            sys.executable, "scripts/check-cursor-update.py", "--port", self.port,
            "--upstream", target, "--output", "audit.json", "--github-output", "outputs",
        ], cwd=self.repo, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.repo / "audit.json").read_text())["changes"], [])
        self.assertIn("changed=false\n", (self.repo / "outputs").read_text())

    def test_duplicate_pin_is_rejected(self):
        self.write("UPSTREAM.md", f"| Commit | `{self.base}` |\n| Commit | `{self.base}` |\n")
        port = self.commit("Invalid duplicate pin")
        result = subprocess.run([
            sys.executable, "scripts/upstream-audit.py", "--port", port, "--upstream", self.target,
        ], cwd=self.repo, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("exactly the recorded full commit row", result.stderr)

    def test_merge_probe_uses_actual_range_without_fixed_counts(self):
        self.write("audit.json", json.dumps(self.audit()))
        result = subprocess.run([
            sys.executable, "scripts/upstream-merge-probe.py", "audit.json",
        ], cwd=self.repo, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("stale HEAD refused", result.stdout)
        self.assertIn("binary merge-file failure reported", result.stdout)
        self.assertEqual(self.git("worktree", "list").count("\n"), 0)


class CursorNoticeTests(unittest.TestCase):
    def setUp(self):
        self.report = {"changes": [{"change": "modify"}], "upstream_target": "b" * 40,
                       "upstream_base": "a" * 40, "upstream_version": "0.15.15",
                       "summary": {"changed_files": 65}}

    def issue(self, target, state="open", author="github-actions[bot]"):
        return {"number": 7, "state": state, "user": {"login": author},
                "body": f"{notice.MARKER}\n<!-- cursor-target:{target} -->"}

    def test_no_delta_has_no_notice(self):
        self.report["changes"] = []
        self.assertEqual(notice.plan_notice(self.report, [])["action"], "none")

    def test_same_target_is_not_repeated_even_after_issue_closed(self):
        for state in ("open", "closed"):
            with self.subTest(state=state):
                result = notice.plan_notice(self.report, [self.issue("b" * 40, state)])
                self.assertEqual(result["action"], "none")

    def test_new_target_updates_single_pending_notice(self):
        result = notice.plan_notice(self.report, [self.issue("c" * 40)])
        self.assertEqual(result["action"], "update")
        self.assertEqual(result["number"], 7)
        self.assertIn("cursor-target:" + "b" * 40, result["body"])

    def test_human_marker_cannot_suppress_bot_notice(self):
        result = notice.plan_notice(self.report, [self.issue("b" * 40, author="someone")])
        self.assertEqual(result["action"], "create")

    def run_cli(self, write=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            audit = root / "audit.json"
            audit.write_text(json.dumps(self.report))
            fake = root / "gh"
            fake.write_text(
                "#!/usr/bin/env python3\n"
                "import json, pathlib, sys\n"
                "p = pathlib.Path(__file__).parent / 'calls.jsonl'\n"
                "with p.open('a') as f: f.write(json.dumps(sys.argv[1:]) + '\\n')\n"
                "if '--method' in sys.argv:\n"
                "    data = json.load(sys.stdin)\n"
                "    (pathlib.Path(__file__).parent / 'sent.json').write_text(json.dumps(data))\n"
                "    print('{}')\n"
                "else: print('[[]]')\n"
            )
            fake.chmod(0o755)
            command = [sys.executable, str(ROOT / "scripts/cursor-update-notice.py"),
                       str(audit), "--repo", "fixture/port"]
            if write:
                command.append("--write")
            result = subprocess.run(command, capture_output=True, text=True,
                                    env={**os.environ, "PATH": str(root) + os.pathsep + os.environ["PATH"]})
            self.assertEqual(result.returncode, 0, result.stderr)
            calls = [json.loads(line) for line in (root / "calls.jsonl").read_text().splitlines()]
            sent = json.loads((root / "sent.json").read_text()) if (root / "sent.json").exists() else None
            return calls, sent

    def test_cli_is_read_only_without_write_flag(self):
        calls, sent = self.run_cli()
        self.assertEqual(len(calls), 1)
        self.assertNotIn("--method", calls[0])
        self.assertIsNone(sent)

    def test_cli_writes_one_structured_notice_only_with_write_flag(self):
        calls, sent = self.run_cli(write=True)
        self.assertEqual(len(calls), 2)
        self.assertIn("POST", calls[1])
        self.assertEqual(sent["title"], "Update direct Cursor pstack to 0.15.15")
        self.assertIn("cursor-target:" + "b" * 40, sent["body"])


if __name__ == "__main__":
    unittest.main()
