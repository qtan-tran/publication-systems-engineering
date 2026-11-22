#!/usr/bin/env python3
"""Generate exact-commit release-candidate evidence for the public repository.

This command is intentionally evidence-oriented: it refuses a dirty or shallow checkout,
records the exact Git commit, runs the public-tree integrity gate and full-history secret
scan, and writes a machine-readable report. It does not claim legal approval or CI
coverage beyond the environment in which it actually runs.
"""
from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "tests" / "_output" / "release-evidence"


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=check
    )


def run_python(path: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [sys.executable, str(path)], cwd=ROOT, env=env, text=True, capture_output=True
    )


def main() -> int:
    checks: list[dict[str, object]] = []

    def record(name: str, passed: bool, detail: object = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    inside = git("rev-parse", "--is-inside-work-tree", check=False)
    is_git = inside.returncode == 0 and inside.stdout.strip() == "true"
    record("git_repository", is_git, (inside.stderr or inside.stdout).strip())
    if not is_git:
        OUT.mkdir(parents=True, exist_ok=True)
        payload = {
            "audit_kind": "candidate_evidence",
            "passed": False,
            "checks": checks,
            "note": "Exact-commit evidence requires a Git checkout.",
        }
        (OUT / "candidate-evidence.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(payload, indent=2))
        return 2

    head = git("rev-parse", "HEAD").stdout.strip()
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    shallow_raw = git("rev-parse", "--is-shallow-repository").stdout.strip().lower()
    shallow = shallow_raw == "true"
    record("full_history_available", not shallow, {"shallow": shallow})

    status = git("status", "--porcelain=v1", "--untracked-files=all").stdout.splitlines()
    # Generated regression output is intentionally ignored and therefore absent here.
    record("working_tree_clean", not status, status[:50])

    registry = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "release" / "sync_registry.py"), "--check"],
        cwd=ROOT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, text=True, capture_output=True
    )
    record("registry_synchronization", registry.returncode == 0, (registry.stdout + registry.stderr)[-2000:])

    integrity = run_python(ROOT / "tests" / "regression" / "public_tree_integrity.py")
    record(
        "public_tree_integrity",
        integrity.returncode == 0,
        (integrity.stdout + integrity.stderr)[-2000:],
    )

    output_inspection = run_python(ROOT / "tests" / "regression" / "output_inspection.py")
    record(
        "output_inspection_regression",
        output_inspection.returncode == 0,
        (output_inspection.stdout + output_inspection.stderr)[-2000:],
    )

    OUT.mkdir(parents=True, exist_ok=True)
    history = run_python(ROOT / "scripts" / "release" / "full_history_scan.py")
    history_path = OUT / "full-history-scan.json"
    history_payload: dict[str, object] = {}
    if history_path.is_file():
        try:
            history_payload = json.loads(history_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            history_payload = {}
    history_ok = (
        history.returncode == 0
        and history_payload.get("passed") is True
        and history_payload.get("head_commit") == head
        and history_payload.get("shallow_repository") is False
    )
    record("history_scan", history_ok, history_payload or (history.stdout + history.stderr)[-2000:])

    github_actions = os.environ.get("GITHUB_ACTIONS", "").lower() == "true"
    github_sha = os.environ.get("GITHUB_SHA")
    github_sha_matches = bool(github_actions and github_sha and github_sha == head)

    payload = {
        "audit_kind": "candidate_evidence",
        "passed": all(item["passed"] for item in checks),
        "candidate": {
            "head_commit": head,
            "branch": branch,
            "working_tree_clean": not status,
            "full_history_available": not shallow,
        },
        "environment": {
            "platform": platform.platform(),
            "system": platform.system(),
            "python": platform.python_version(),
            "github_actions": github_actions,
            "github_sha": github_sha,
            "github_sha_matches_head": github_sha_matches,
            "runner_os": os.environ.get("RUNNER_OS"),
        },
        "checks": checks,
        "legal_approval_recorded": False,
        "cross_platform_ci_complete": False,
        "note": (
            "This report proves only the checks performed in this checkout/environment. "
            "It does not by itself establish independent legal approval or aggregate "
            "Windows/macOS/Linux CI completion."
        ),
    }
    (OUT / "candidate-evidence.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (OUT / "candidate-commit.txt").write_text(head + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
