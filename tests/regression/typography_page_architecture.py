from __future__ import annotations

import json
import os
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
    profile = REPO / "profiles" / "basic-book" / "pse-profile-basic-book.sty"
    text = profile.read_text(encoding="utf-8")
    checks.append(("profile_exists", profile.is_file(), str(profile)))
    checks.append(("restrained_chapter_style", "\\PSETypographyChapterTitleRole" in text and "\\titlespacing*{\\chapter}" in text, "chapter hierarchy consumes the typography role contract"))
    checks.append(("running_heads", "\\pagestyle{fancy}" in text and "\\fancypagestyle{plain}" in text, "body and opening page styles present"))
    checks.append(("widow_orphan_policy", "\\widowpenalty=7000" in text and "\\clubpenalty=7000" in text, "non-absolute penalties present"))

    fixture = REPO / "examples" / "synthetic" / "basic-book"
    run("clean", str(fixture))
    run("build", str(fixture))
    run("check", str(fixture))
    qa = json.loads((fixture / "build" / "qa-report.json").read_text(encoding="utf-8"))
    latex = qa["metrics"].get("latex", {})
    checks.append(("fixture_qa", qa.get("status") == "pass", f"qa={qa.get('status')}"))
    checks.append(("fixture_clean_log", not qa.get("warnings") and all(latex.get(k, 0) == 0 for k in ("missing_glyphs", "undefined_references", "overfull_hbox", "overfull_vbox", "font_substitution", "hyperref_warnings")), f"warnings={qa.get('warnings')}"))
    checks.append(("page_geometry", qa["metrics"]["pdf"]["width_mm"] == 126.0 and qa["metrics"]["pdf"]["height_mm"] == 198.0, str(qa["metrics"]["pdf"])))

    with tempfile.TemporaryDirectory(prefix="pse-regression") as td:
        parent = Path(td)
        run("new", str(parent), "--non-interactive", "--title", "Typography Contract", "--author", "Synthetic Editor", "--language", "en", "--publication-year", "2027", "--slug", "typography-contract")
        project = parent / "typography-contract"
        main = (project / "main.tex").read_text(encoding="utf-8")
        checks.append(("generated_profile_load", "\\usepackage{pse-profile-basic-book}" in main, "generated main loads basic-book profile"))
        checks.append(("local_override_boundary", (project / "config" / "pse-local.tex").is_file() and "pse-local.tex" in main, "title-local config exists and is loaded"))
        run("build", str(project))
        run("check", str(project))
        project_qa = json.loads((project / "build" / "qa-report.json").read_text(encoding="utf-8"))
        checks.append(("generated_project_qa", project_qa.get("status") == "pass", f"qa={project_qa.get('status')}"))

    failed = [c for c in checks if not c[1]]
    print("Typography/page-architecture regression")
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
