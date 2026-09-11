from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from pse_cli.release_contract import validate_release_audit_record  # noqa: E402

ENV = os.environ.copy()
ENV["PYTHONPATH"] = str(TOOLS) + os.pathsep + str(ROOT)
ENV["PYTHONDONTWRITEBYTECODE"] = "1"
FIXTURES = ROOT / "tests" / "fixtures" / "releases"

checks = []

def add(name, passed, detail=""):
    checks.append({"name": name, "pass": bool(passed), "detail": str(detail)})

def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in root.rglob("*") if x.is_file()):
        h.update(p.relative_to(root).as_posix().encode())
        h.update(p.read_bytes())
    return h.hexdigest()

def run(*args):
    return subprocess.run([sys.executable, "-m", "pse_cli.cli", *map(str, args)], cwd=ROOT, env=ENV, text=True, capture_output=True)

for schema, expected_compat in (("schema-0.1", "legacy"), ("schema-0.2", "current")):
    release = FIXTURES / schema
    before = tree_hash(release)
    verify = run("verify-release", release)
    try:
        verify_payload = json.loads(verify.stdout)
    except json.JSONDecodeError:
        verify_payload = {}
    add(f"{schema}_verify", verify.returncode == 0 and verify_payload.get("status") == "pass", verify.stdout + verify.stderr)
    add(f"{schema}_compatibility", verify_payload.get("compatibility", {}).get("status") == expected_compat, verify_payload.get("compatibility"))

    migration = run("release-migration", release)
    try:
        migration_payload = json.loads(migration.stdout)
    except json.JSONDecodeError:
        migration_payload = {}
    expected_migration = "legacy-verifiable-not-upgraded" if schema == "schema-0.1" else "already-current"
    add(f"{schema}_migration", migration.returncode == 0 and migration_payload.get("migration_status") == expected_migration, migration.stdout + migration.stderr)

    with tempfile.TemporaryDirectory(prefix="pse-audit-") as td:
        out = Path(td) / f"{schema}-audit.json"
        audit = run("audit-release", release, "--output", out)
        try:
            audit_payload = json.loads(audit.stdout)
        except json.JSONDecodeError:
            audit_payload = {}
        add(f"{schema}_audit_pass", audit.returncode == 0 and audit_payload.get("audit_status") == "pass", audit.stdout + audit.stderr)
        add(f"{schema}_audit_contract", not validate_release_audit_record(audit_payload), validate_release_audit_record(audit_payload))
        add(f"{schema}_audit_external_written", out.is_file())
        add(f"{schema}_audit_not_release_artifact", audit_payload.get("historical_artifact_mutated") is False and audit_payload.get("audit_record_is_release_artifact") is False)
        add(f"{schema}_audit_hash_binding", audit_payload.get("source_manifest_sha256") and audit_payload.get("source_pdf_sha256"))

    after = tree_hash(release)
    add(f"{schema}_fixture_immutable", before == after, f"before={before} after={after}")

# Output may not be written into the audited release.
inside = FIXTURES / "schema-0.1" / "audit-record.json"
blocked = run("audit-release", FIXTURES / "schema-0.1", "--output", inside)
add("audit_output_inside_release_blocked", blocked.returncode != 0 and not inside.exists(), blocked.stdout + blocked.stderr)

# A tampered copy remains auditable, but the audit must fail rather than normalize it.
with tempfile.TemporaryDirectory(prefix="pse-audit-tamper-") as td:
    copied = Path(td) / "release"
    shutil.copytree(FIXTURES / "schema-0.2", copied)
    pdf = copied / "current-release.pdf"
    pdf.write_bytes(pdf.read_bytes() + b"\n% tamper\n")
    audit = run("audit-release", copied)
    try:
        payload = json.loads(audit.stdout)
    except json.JSONDecodeError:
        payload = {}
    add("tampered_release_audit_fails", audit.returncode != 0 and payload.get("audit_status") == "fail", audit.stdout + audit.stderr)
    add("tampered_release_not_rewritten", pdf.read_bytes().endswith(b"% tamper\n"))

add("audit_schema_installed", (ROOT / "schema" / "release-audit-record-0.1.schema.json").is_file())

payload = {"suite": "release_audit_compatibility", "passed": all(c["pass"] for c in checks), "checks": checks}
print(json.dumps(payload, indent=2))
raise SystemExit(0 if payload["passed"] else 1)
