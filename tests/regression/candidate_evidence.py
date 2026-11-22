from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "release" / "candidate_evidence.py"


def run(cmd: list[str], cwd: Path, expect: int = 0) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    if proc.returncode != expect:
        raise AssertionError(
            f"command failed ({proc.returncode}, expected {expect}): {' '.join(cmd)}\n"
            f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
        )
    return proc


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    with tempfile.TemporaryDirectory(prefix="pse-candidate-evidence-") as td:
        repo = Path(td) / "repo"
        shutil.copytree(
            ROOT,
            repo,
            ignore=shutil.ignore_patterns(
                ".git", ".claude", "_output", "__pycache__", "*.pyc",
                "build", "*.egg-info", ".pytest_cache",
            ),
        )
        run(["git", "init"], repo)
        run(["git", "config", "user.email", "regression@example.invalid"], repo)
        run(["git", "config", "user.name", "PSE Regression"], repo)
        run(["git", "add", "."], repo)
        run(["git", "commit", "-m", "candidate fixture"], repo)
        head = run(["git", "rev-parse", "HEAD"], repo).stdout.strip()

        proc = run([sys.executable, str(repo / "scripts" / "release" / "candidate_evidence.py")], repo)
        report = json.loads((repo / "tests" / "_output" / "release-evidence" / "candidate-evidence.json").read_text())
        history = json.loads((repo / "tests" / "_output" / "release-evidence" / "full-history-scan.json").read_text())
        checks.append(("clean_candidate_passes", report.get("passed") is True, proc.stdout[-500:]))
        checks.append(("exact_commit_recorded", report.get("candidate", {}).get("head_commit") == head, str(report.get("candidate"))))
        checks.append(("history_bound_to_commit", history.get("head_commit") == head and history.get("shallow_repository") is False, str(history)))
        checks.append(("no_false_external_evidence", report.get("legal_approval_recorded") is False and report.get("cross_platform_ci_complete") is False, str({"legal": report.get("legal_approval_recorded"), "ci": report.get("cross_platform_ci_complete")})))

        (repo / "README.md").write_text((repo / "README.md").read_text() + "\n", encoding="utf-8")
        dirty = run([sys.executable, str(repo / "scripts" / "release" / "candidate_evidence.py")], repo, expect=1)
        dirty_report = json.loads((repo / "tests" / "_output" / "release-evidence" / "candidate-evidence.json").read_text())
        dirty_check = next(x for x in dirty_report["checks"] if x["name"] == "working_tree_clean")
        checks.append(("dirty_candidate_blocked", dirty_check["passed"] is False, dirty.stdout[-500:]))

    failed = [item for item in checks if not item[1]]
    print("Candidate evidence self-test")
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
