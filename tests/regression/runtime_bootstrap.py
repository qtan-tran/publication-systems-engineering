from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def run(cmd: list[str], *, cwd: Path, env: dict[str, str] | None = None, expect: int = 0) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(cmd, cwd=cwd, env=env, text=True, capture_output=True)
    if proc.returncode != expect:
        raise AssertionError(f"command failed ({proc.returncode} != {expect}): {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
    return proc


def main() -> int:
    checks: list[tuple[str, bool, str]] = []

    # Source-checkout doctor must discover the runtime without PSE_ROOT.
    env = os.environ.copy()
    env.pop("PSE_ROOT", None)
    env["PYTHONPATH"] = str(REPO / "tools") + os.pathsep + env.get("PYTHONPATH", "")
    proc = run([sys.executable, "-m", "pse_cli.cli", "doctor", "--json"], cwd=REPO, env=env)
    report = json.loads(proc.stdout)
    runtime_check = next(c for c in report["checks"] if c["name"] == "runtime_discovery")
    checks.append(("source_runtime_discovery", runtime_check["status"] == "pass" and "source-checkout" in runtime_check["detail"], runtime_check["detail"]))

    # A bad explicit PSE_ROOT must fail closed rather than silently falling back.
    with tempfile.TemporaryDirectory(prefix="pse-bad-root-") as td:
        bad_env = env.copy()
        bad_env["PSE_ROOT"] = td
        proc = run([sys.executable, "-m", "pse_cli.cli", "doctor", "--json"], cwd=Path(td), env=bad_env, expect=1)
        bad_report = json.loads(proc.stdout)
        bad_runtime = next(c for c in bad_report["checks"] if c["name"] == "runtime_discovery")
        checks.append(("invalid_override_fails_closed", bad_runtime["status"] == "fail" and "PSE_ROOT" in bad_runtime["detail"], bad_runtime["detail"]))

    # Install the wheel into a clean target directory and operate outside the repository
    # with no PSE_ROOT. The running Python supplies dependencies; the target supplies PSE.
    with tempfile.TemporaryDirectory(prefix="pse-regression") as td:
        td_path = Path(td)
        wheelhouse = td_path / "wheelhouse"
        wheelhouse.mkdir()
        run([sys.executable, "-m", "pip", "wheel", "--no-build-isolation", "--no-deps", "-w", str(wheelhouse), str(REPO)], cwd=td_path)
        wheels = list(wheelhouse.glob("publication_systems_engineering-*.whl"))
        if len(wheels) != 1:
            raise AssertionError(f"expected one PSE wheel, found {wheels}")
        target = td_path / "target"
        run([sys.executable, "-m", "pip", "install", "--no-deps", "--target", str(target), str(wheels[0])], cwd=td_path)
        clean_env = os.environ.copy()
        clean_env.pop("PSE_ROOT", None)
        clean_env["PYTHONPATH"] = str(target)
        proc = run([sys.executable, "-m", "pse_cli.cli", "doctor", "--json"], cwd=td_path, env=clean_env)
        installed_report = json.loads(proc.stdout)
        installed_runtime = next(c for c in installed_report["checks"] if c["name"] == "runtime_discovery")
        checks.append(("installed_runtime_discovery", installed_runtime["status"] == "pass" and "installed-share" in installed_runtime["detail"], installed_runtime["detail"]))

        parent = td_path / "books"
        parent.mkdir()
        cli = [sys.executable, "-m", "pse_cli.cli"]
        run(cli + [
            "new", str(parent), "--non-interactive",
            "--title", "Installed Runtime Book", "--author", "Runtime Tester",
            "--language", "en", "--publication-year", "2027", "--slug", "installed-runtime-book"
        ], cwd=td_path, env=clean_env)
        project = parent / "installed-runtime-book"
        run(cli + ["build", str(project)], cwd=td_path, env=clean_env)
        run(cli + ["check", str(project)], cwd=td_path, env=clean_env)
        qa = json.loads((project / "build" / "qa-report.json").read_text(encoding="utf-8"))
        checks.append(("external_project_build", qa.get("status") == "pass" and (project / "build" / "book.pdf").exists(), f"qa={qa.get('status')}"))

    failed = [c for c in checks if not c[1]]
    print("Runtime/bootstrap regression")
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
