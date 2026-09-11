from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ENV = os.environ.copy()
ENV["PYTHONPATH"] = str(REPO / "tools") + os.pathsep + ENV.get("PYTHONPATH", "")
FIXTURE = REPO / "tests" / "fixtures" / "profile-books" / "basic-book"


def run(*args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, "-m", "pse_cli.cli", *args]
    proc = subprocess.run(cmd, cwd=REPO, env=ENV, text=True, capture_output=True)
    if proc.returncode != expect:
        raise AssertionError(f"command failed: {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
    return proc


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    run("clean", str(FIXTURE))
    run("build", str(FIXTURE))
    run("check", str(FIXTURE), "--baseline", str(REPO / "tests" / "qa" / "baselines" / "basic-book.json"))
    qa = json.loads((FIXTURE / "build" / "qa-report.json").read_text(encoding="utf-8"))
    checks.append(("severity_schema", qa.get("schema_version") == "0.2" and set(qa.get("summary", {})) == {"error", "warning", "review", "info"}, str(qa.get("summary"))))
    checks.append(("fixture_no_errors", qa.get("summary", {}).get("error") == 0, f"status={qa.get('status')}"))
    checks.append(("page_count_baseline", qa.get("metrics", {}).get("baseline", {}).get("page_count", {}).get("delta") == 0, str(qa.get("metrics", {}).get("baseline"))))

    baseline_dir = REPO / "tests" / "visual" / "baselines" / "basic-book"
    run("visual-check", str(FIXTURE), "--baseline-dir", str(baseline_dir))
    visual = json.loads((FIXTURE / "build" / "visual-regression" / "visual-report.json").read_text(encoding="utf-8"))
    checks.append(("visual_no_errors", visual.get("summary", {}).get("error") == 0, str(visual.get("summary"))))
    checks.append(("visual_profile_pages", len(visual.get("results", [])) == 3, f"results={len(visual.get('results', []))}"))
    checks.append(("visual_baseline_match", all(float(x.get("pixel_diff_ratio", 1.0)) <= 0.005 for x in visual.get("results", [])), str([x.get('pixel_diff_ratio') for x in visual.get('results', [])])))

    # Deliberate page-count drift is review-only and must not return a failing exit code.
    tmp = FIXTURE / "build" / "regression-output.json"
    tmp.write_text(json.dumps({"pages": 7}), encoding="utf-8")
    run("check", str(FIXTURE), "--baseline", str(tmp), expect=0)
    drift = json.loads((FIXTURE / "build" / "qa-report.json").read_text(encoding="utf-8"))
    drift_codes = {(f.get("code"), f.get("severity")) for f in drift.get("findings", [])}
    checks.append(("page_drift_review_only", ("page_count_drift", "review") in drift_codes and drift.get("summary", {}).get("error") == 0, str(drift_codes)))

    failed = [c for c in checks if not c[1]]
    print("QA/regression foundation self-test")
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
