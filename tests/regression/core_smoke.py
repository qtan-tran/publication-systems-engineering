from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "examples" / "synthetic" / "basic-book"
ENV = os.environ.copy()
ENV["PYTHONPATH"] = str(ROOT / "tools") + os.pathsep + ENV.get("PYTHONPATH", "")


def run(*args: str) -> None:
    cmd = [sys.executable, "-m", "pse_cli.cli", *args]
    subprocess.run(cmd, cwd=ROOT, env=ENV, check=True)


def main() -> int:
    run("clean", str(FIXTURE))
    run("build", str(FIXTURE))
    run("check", str(FIXTURE))
    report = json.loads((FIXTURE / "build" / "qa-report.json").read_text(encoding="utf-8"))
    assert report["status"] == "pass"
    assert report["metrics"]["pdf"]["pages"] >= 4
    assert abs(report["metrics"]["pdf"]["width_mm"] - 126) < 0.5
    assert abs(report["metrics"]["pdf"]["height_mm"] - 198) < 0.5
    print("Core smoke regression: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
