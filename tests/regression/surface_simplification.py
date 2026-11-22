"""Guard the supported six-profile surface and fail-closed migration boundary."""
from __future__ import annotations
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED = {"academic-monograph", "bilingual-edition", "critical-edition", "drama", "edited-collection", "literary-fiction"}
RETIRED = {"basic-book", "poetry", "scholarly-edition"}
checks = []

def ck(name, ok):
    checks.append((name, bool(ok)))

runtime = json.loads((ROOT / "runtime/pse-runtime.json").read_text(encoding="utf-8"))
ck("six_runtime_profiles", set(runtime["profiles"]) == EXPECTED)
ck("fourteen_semantic_modules", len(runtime["modules"]) == 14 and "verse-structure" in runtime["modules"])
ck("retired_profiles_absent", all(not (ROOT / "profiles" / x).exists() for x in RETIRED))
ck("canonical_migration_guide", (ROOT / "wiki/getting-started/profile-migration.md").is_file())
ck("release_workflows_preserved", all((ROOT / ".github/workflows" / f).is_file() for f in ("qa-regression.yml", "docs-pages.yml", "release-evidence.yml", "beta-candidate.yml")))
ck("four_workflows", len(list((ROOT / ".github/workflows").glob("*.yml"))) == 4)
ck("license_not_invented", not (ROOT / "LICENSE").exists())

cli = [sys.executable, "-m", "pse_cli.cli"]
env = {**os.environ, "PYTHONPATH": str(ROOT / "tools") + os.pathsep + os.environ.get("PYTHONPATH", "")}
result = subprocess.run(cli + ["profiles", "--json"], cwd=ROOT, env=env, capture_output=True, text=True)
ck("cli_registry_exact", result.returncode == 0 and {x["id"] for x in json.loads(result.stdout)["profiles"]} == EXPECTED)
with tempfile.TemporaryDirectory(prefix="pse-retired-profiles-") as temp:
    for pid in sorted(RETIRED):
        result = subprocess.run(cli + ["new", temp, "--non-interactive", "--profile", pid,
             "--title", "Rejected Legacy Profile", "--author", "PSE", "--language", "en",
             "--publication-year", "2027", "--slug", "should-not-exist"],
             cwd=ROOT, env=env, capture_output=True, text=True)
        ck(f"retired_{pid}_rejected", result.returncode != 0 and "Unsupported profile" in (result.stdout + result.stderr)
            and not (Path(temp) / "should-not-exist").exists())
    result = subprocess.run(cli + ["new", temp, "--non-interactive", "--title", "Default Book",
        "--author", "PSE", "--language", "en", "--publication-year", "2027", "--slug", "default"],
        cwd=ROOT, env=env, capture_output=True, text=True)
    book = Path(temp) / "default" / "book.yml"
    ck("default_profile_academic_monograph", result.returncode == 0 and book.is_file()
       and "profile: academic-monograph" in book.read_text(encoding="utf-8"))

for name, ok in checks:
    print(("PASS" if ok else "FAIL"), name)
print(f"summary: {sum(ok for _, ok in checks)}/{len(checks)} pass")
raise SystemExit(0 if all(ok for _, ok in checks) else 1)
