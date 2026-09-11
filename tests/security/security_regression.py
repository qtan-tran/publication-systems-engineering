from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))
from pse_cli import cli


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def test_metadata_escaping() -> None:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "book.yml"
        p.write_text("title: '\\\\input{secret}'\nauthor: Tester\nlanguage: en\npublication_year: 2026\npage:\n  width_mm: 126\n  height_mm: 198\n", encoding="utf-8")
        data = cli._load_metadata(p)
        escaped = cli._tex_escape(data["title"])
        require(r"\input" not in escaped, "TeX command survived metadata escaping")
        require("textbackslash" in escaped, "Backslash was not neutralized")


def test_dimension_injection_rejected() -> None:
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "book.yml"
        p.write_text("title: Test\nauthor: Tester\nlanguage: en\npublication_year: 2026\npage:\n  width_mm: '126mm\\\\input{secret}'\n  height_mm: 198\n", encoding="utf-8")
        try:
            cli._load_metadata(p)
        except SystemExit:
            return
        raise AssertionError("Non-numeric page dimension was accepted")


def test_cli_contains_safe_build_flag() -> None:
    source = (ROOT / "tools/pse_cli/cli.py").read_text(encoding="utf-8")
    require('"--no-shell-escape"' in source, "LuaLaTeX safe-build flag is missing")


def test_shell_escape_runtime() -> None:
    if not shutil.which("lualatex"):
        print("SKIP runtime shell-escape test: lualatex not found")
        return
    fixture = ROOT / "tests/fixtures/security-book"
    sentinel = fixture / "PSE_SECURITY_SENTINEL"
    sentinel.unlink(missing_ok=True)
    env = dict(**__import__('os').environ)
    env["PYTHONPATH"] = str(TOOLS)
    subprocess.run([sys.executable, "-m", "pse_cli.cli", "clean", str(fixture)], cwd=ROOT, env=env, check=True)
    subprocess.run([sys.executable, "-m", "pse_cli.cli", "build", str(fixture)], cwd=ROOT, env=env, check=True)
    require(not sentinel.exists(), "Shell command executed despite --no-shell-escape")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-tex", action="store_true")
    args = ap.parse_args()
    tests = [test_metadata_escaping, test_dimension_injection_rejected, test_cli_contains_safe_build_flag]
    if not args.no_tex:
        tests.append(test_shell_escape_runtime)
    for t in tests:
        t()
        print(f"PASS {t.__name__}")
    print(f"security regression: PASS ({len(tests)} tests)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
