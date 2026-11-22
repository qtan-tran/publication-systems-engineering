from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples" / "profiles"


def registered_profiles() -> list[str]:
    result = []
    for manifest in sorted((ROOT / "profiles").glob("*/profile.json")):
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("generator_supported") is True:
            result.append(data["id"])
    return result


def build_one(profile: str) -> None:
    project = EXAMPLES / profile / "source"
    output_dir = EXAMPLES / profile / "output"
    if not (project / "book.yml").is_file():
        raise SystemExit(f"missing demo source for {profile}: {project}")
    subprocess.run(
        [sys.executable, "-m", "tools.pse_cli.cli", "build", str(project)],
        cwd=ROOT,
        check=True,
    )
    built = project / "build" / "book.pdf"
    if not built.is_file():
        raise SystemExit(f"build did not produce PDF for {profile}")
    output_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(built, output_dir / f"{profile}-demo.pdf")
    shutil.rmtree(project / "build", ignore_errors=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build canonical synthetic profile demo PDFs.")
    parser.add_argument("profiles", nargs="*", help="Profile ids; omit to build every generator-supported profile.")
    parser.add_argument("--check", action="store_true", help="Validate demo source/output parity without rebuilding PDFs.")
    args = parser.parse_args()
    known = registered_profiles()
    selected = args.profiles or known
    unknown = sorted(set(selected) - set(known))
    if unknown:
        raise SystemExit("unknown profile(s): " + ", ".join(unknown))
    if args.check:
        failures = []
        for profile in selected:
            demo = EXAMPLES / profile
            required = [
                demo / "README.md",
                demo / "source" / "book.yml",
                demo / "source" / "main.tex",
                demo / "output" / f"{profile}-demo.pdf",
            ]
            missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file()]
            if missing:
                failures.extend(missing)
            elif (demo / "output" / f"{profile}-demo.pdf").read_bytes()[:5] != b"%PDF-":
                failures.append(f"{profile}: canonical output is not a PDF")
        if failures:
            raise SystemExit("demo parity check failed:\n" + "\n".join(failures))
        print(f"validated {len(selected)} canonical demo project(s)")
        return 0
    for profile in selected:
        print(f"==> demo: {profile}")
        build_one(profile)
    print(f"built {len(selected)} canonical demo PDF(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
