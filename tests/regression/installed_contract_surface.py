from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from pypdf import PdfWriter

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from pse_cli.release_contract import (  # noqa: E402
    installed_contract_surface,
    release_schema_compatibility,
    sha256_file,
    write_checksum_file,
)

checks = []

def add(name, passed, detail=""):
    checks.append({"name": name, "pass": bool(passed), "detail": str(detail)})

surface = installed_contract_surface(ROOT, runtime_source="source-checkout", framework_version="1.47.0-alpha")
contracts = {c["id"]: c for c in surface["contracts"]}
add("release_schema_installed", contracts["publication-release-manifest"]["installed"], contracts["publication-release-manifest"])
add("inspection_schema_installed", contracts["output-inspection"]["installed"], contracts["output-inspection"])
add("audit_schema_installed", contracts["release-audit-record"]["installed"], contracts["release-audit-record"])
add("audit_schema_current_02", contracts["release-audit-record"]["current_schema_version"] == "0.2", contracts["release-audit-record"])
add("audit_index_schema_installed", contracts["release-audit-index"]["installed"], contracts["release-audit-index"])
add("audit_bundle_schema_installed", contracts["audit-evidence-bundle-manifest"]["installed"], contracts["audit-evidence-bundle-manifest"])
add("release_current_02", contracts["publication-release-manifest"]["current_schema_version"] == "0.2")
add("legacy_01_verify_only", release_schema_compatibility("0.1")["verification"] == "verification-only-with-warning")
add("unknown_schema_rejected", release_schema_compatibility("9.9")["status"] == "unsupported")

env = os.environ.copy()
env["PYTHONPATH"] = str(TOOLS) + os.pathsep + str(ROOT)
env["PYTHONDONTWRITEBYTECODE"] = "1"
proc = subprocess.run([sys.executable, "-m", "pse_cli.cli", "contracts", "--json"], cwd=ROOT, env=env, text=True, capture_output=True)
try:
    cli_surface = json.loads(proc.stdout)
except json.JSONDecodeError:
    cli_surface = {}
add("contracts_cli_json", proc.returncode == 0 and cli_surface.get("kind") == "pse-installed-contract-surface", proc.stdout + proc.stderr)
add("contracts_cli_schema_paths_exist", all(Path(c["schema_path"]).is_file() for c in cli_surface.get("contracts", [])), cli_surface.get("contracts"))

with tempfile.TemporaryDirectory(prefix="pse-legacy-release-") as td:
    release = Path(td) / "release"
    release.mkdir()
    pdf = release / "legacy.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=360, height=540)
    with pdf.open("wb") as fh:
        writer.write(fh)
    manifest = {
        "schema_version": "0.1",
        "artifact_type": "publication_release",
        "release_id": "PSE-LEGACY-TEST",
        "pse_version": "1.24.0-alpha",
        "pdf": {
            "file": pdf.name,
            "sha256": sha256_file(pdf),
            "pages": 1,
            "width_mm": 127.0,
            "height_mm": 190.5,
        },
    }
    manifest_path = release / "release-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_checksum_file(release / "SHA256SUMS.txt", [pdf, manifest_path])

    verify = subprocess.run([sys.executable, "-m", "pse_cli.cli", "verify-release", str(release)], cwd=ROOT, env=env, text=True, capture_output=True)
    verify_payload = json.loads(verify.stdout)
    add("legacy_verify_passes_with_warning", verify.returncode == 0 and verify_payload.get("compatibility", {}).get("status") == "legacy", verify.stdout + verify.stderr)

    external = Path(td) / "assessment.json"
    migration = subprocess.run([sys.executable, "-m", "pse_cli.cli", "release-migration", str(release), "--output", str(external)], cwd=ROOT, env=env, text=True, capture_output=True)
    assessment = json.loads(migration.stdout)
    add("legacy_migration_assessment", migration.returncode == 0 and assessment.get("migration_status") == "legacy-verifiable-not-upgraded", migration.stdout + migration.stderr)
    add("legacy_not_mutated", assessment.get("historical_artifact_mutated") is False and assessment.get("in_place_upgrade_supported") is False)
    add("legacy_no_retroactive_inspection", assessment.get("retroactive_output_inspection_inferred") is False)
    add("external_assessment_written", external.is_file())

    inside = release / "assessment.json"
    blocked = subprocess.run([sys.executable, "-m", "pse_cli.cli", "release-migration", str(release), "--output", str(inside)], cwd=ROOT, env=env, text=True, capture_output=True)
    add("in_place_assessment_blocked", blocked.returncode != 0 and not inside.exists(), blocked.stdout + blocked.stderr)

payload = {"suite": "installed_contract_surface", "passed": all(c["pass"] for c in checks), "checks": checks}
print(json.dumps(payload, indent=2))
raise SystemExit(0 if payload["passed"] else 1)
