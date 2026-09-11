from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ENV = os.environ.copy()
ENV["PYTHONPATH"] = str(REPO / "tools") + os.pathsep + ENV.get("PYTHONPATH", "")


def run(*args: str, cwd: Path | None = None, expect: int = 0) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, "-m", "pse_cli.cli", *args]
    proc = subprocess.run(cmd, cwd=cwd or REPO, env=ENV, text=True, capture_output=True)
    if proc.returncode != expect:
        raise AssertionError(f"command failed: {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
    return proc


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    with tempfile.TemporaryDirectory(prefix="pse-regression") as td:
        parent = Path(td)
        run(
            "new", str(parent), "--non-interactive",
            "--title", "Synthetic Generated Book",
            "--author", "Synthetic Editor",
            "--language", "en",
            "--publication-year", "2027",
            "--slug", "synthetic-generated-book",
        )
        project = parent / "synthetic-generated-book"
        required = [
            "book.yml", "main.tex", "README.md", "SECURITY.md", ".gitignore",
            "content/chapter-01.tex", "assets/.gitkeep", "config/pse-local.tex", "tests/.gitkeep",
        ]
        checks.append(("project_contract", all((project / p).exists() for p in required), "required generated files"))
        checks.append(("build_ignored", "/build/" in (project / ".gitignore").read_text(), "generated artifacts ignored"))
        checks.append(("security_note", "--no-shell-escape" in (project / "SECURITY.md").read_text(), "safe build documented"))
        run("build", str(project))
        check = run("check", str(project))
        report = json.loads((project / "build" / "qa-report.json").read_text())
        checks.append(("generated_build", (project / "build" / "book.pdf").exists(), "PDF generated"))
        checks.append(("generated_qa", report.get("status") == "pass", f"qa={report.get('status')}"))
        run("proof", str(project), "--recipient", "Synthetic Proofreader", "--proof-id", "PSE-GEN-C-001")
        proof_pdf = project / "build" / "proofs" / "book-proof-PSE-GEN-C-001.pdf"
        proof_json = project / "build" / "proofs" / "book-proof-PSE-GEN-C-001.json"
        checks.append(("proof_pipeline", proof_pdf.exists() and proof_json.exists(), "recipient proof + manifest"))
        run("clean", str(project))
        checks.append(("clean_boundary", not (project / "build").exists(), "build directory removed"))

        # Safety: non-empty destination must not be overwritten.
        occupied = parent / "occupied"
        occupied.mkdir()
        (occupied / "keep.txt").write_text("keep")
        proc = run(
            "new", str(parent), "--non-interactive", "--title", "Occupied", "--author", "X",
            "--language", "en", "--publication-year", "2027", "--slug", "occupied", expect=1,
        )
        checks.append(("no_overwrite", "not empty" in (proc.stdout + proc.stderr), "occupied directory rejected"))

        # Safety: unsupported profile fails closed.
        proc = run(
            "new", str(parent), "--non-interactive", "--profile", "unknown-profile", "--title", "Nope",
            "--author", "X", "--language", "en", "--publication-year", "2027", expect=1,
        )
        detail = proc.stdout + proc.stderr
        checks.append(("profile_fail_closed", "Unsupported profile" in detail and "scholarly-edition" in detail, "unknown profile rejected; supported registry reported"))

    failed = [c for c in checks if not c[1]]
    print("Generated-project regression")
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
