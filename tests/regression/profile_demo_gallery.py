from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMOS = ROOT / "examples" / "profiles"
checks = []

def add(name, passed, detail=""):
    checks.append({"name": name, "pass": bool(passed), "detail": str(detail)})

profiles = []
for manifest in sorted((ROOT / "profiles").glob("*/profile.json")):
    data = json.loads(manifest.read_text(encoding="utf-8"))
    if data.get("generator_supported") is True:
        profiles.append(data["id"])

demo_dirs = sorted(p.name for p in DEMOS.iterdir() if p.is_dir())
add("demo_registry_parity", demo_dirs == sorted(profiles), {"registered": profiles, "demo_dirs": demo_dirs})
for profile in profiles:
    root = DEMOS / profile
    source = root / "source"
    pdf = root / "output" / f"{profile}-demo.pdf"
    readme = root / "README.md"
    add(f"{profile}_structure", source.is_dir() and readme.is_file() and pdf.is_file(), root)
    main = source / "main.tex"
    text = main.read_text(encoding="utf-8", errors="replace") if main.is_file() else ""
    add(f"{profile}_attribution_path", "\\PSEPublicationPage" in text, "standard publication page")
    add(f"{profile}_pdf_header", pdf.is_file() and pdf.read_bytes()[:5] == b"%PDF-", pdf)

builder = ROOT / "scripts" / "examples" / "build_profile_demos.py"
result = subprocess.run(
    [__import__("sys").executable, str(builder), "--check"],
    cwd=ROOT, capture_output=True, text=True
)
add("demo_builder_check_mode", result.returncode == 0, (result.stdout + result.stderr).strip())

beginner = ROOT / "docs" / "getting-started" / "BEGINNER-QUICK-START.md"
gallery = ROOT / "docs" / "getting-started" / "PROFILE-DEMO-GALLERY.md"
add("beginner_quick_start", beginner.is_file(), beginner)
add("gallery_overview", gallery.is_file(), gallery)

root_readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
for profile in profiles:
    add(f"gallery_link_{profile}", f"examples/profiles/{profile}/output/{profile}-demo.pdf" in root_readme, profile)

payload = {"suite": "profile_demo_gallery", "passed": all(x["pass"] for x in checks), "checks": checks}
print(json.dumps(payload, indent=2))
raise SystemExit(0 if payload["passed"] else 1)
