from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from pse_cli.release_contract import (  # noqa: E402
    RELEASE_INSPECTION_POLICY,
    RELEASE_MANIFEST_SCHEMA_VERSION,
    OUTPUT_INSPECTION_SCHEMA_VERSION,
    validate_output_inspection,
    validate_release_binding,
    validate_release_manifest,
)

checks: list[tuple[str, bool, str]] = []

def add(name: str, ok: bool, detail: object = "") -> None:
    checks.append((name, bool(ok), str(detail)))

pdf_hash = "a" * 64
inspection_hash = "b" * 64
inspection = {
    "schema_version": OUTPUT_INSPECTION_SCHEMA_VERSION,
    "kind": "pse-output-inspection",
    "pdf": "/synthetic/release.pdf",
    "pdf_sha256": pdf_hash,
    "status": "review",
    "summary": {"error": 0, "warning": 0, "review": 3, "pass": 7, "info": 1},
    "checks": [
        {"name": "pdf_readable", "status": "pass", "detail": "1 page", "machine_verifiable": True},
        {"name": "reading_order", "status": "review", "detail": "human review", "machine_verifiable": False},
    ],
    "certification": "none",
    "scope_note": "Synthetic contract fixture; no certification.",
}
manifest = {
    "schema_version": RELEASE_MANIFEST_SCHEMA_VERSION,
    "artifact_type": "publication_release",
    "release_id": "PSE-R-CONTRACT-001",
    "pse_version": "1.36.0-alpha",
    "pdf": {"file": "synthetic.pdf", "sha256": pdf_hash, "pages": 1, "width_mm": 126.0, "height_mm": 198.0},
    "output_inspection": {
        "file": "output-inspection.json",
        "schema_version": OUTPUT_INSPECTION_SCHEMA_VERSION,
        "sha256": inspection_hash,
        "bound_pdf_sha256": pdf_hash,
        "policy": dict(RELEASE_INSPECTION_POLICY),
    },
}

add("schema_files_present", (ROOT / "schema/release-manifest-0.2.schema.json").is_file() and (ROOT / "schema/output-inspection-0.2.schema.json").is_file())
add("current_manifest_valid", not validate_release_manifest(manifest), validate_release_manifest(manifest))
add("current_inspection_valid", not validate_output_inspection(inspection), validate_output_inspection(inspection))
add("binding_valid", not validate_release_binding(manifest, inspection), validate_release_binding(manifest, inspection))

legacy = dict(manifest)
legacy["schema_version"] = "0.1"
legacy.pop("output_inspection", None)
add("legacy_0_1_supported", not validate_release_manifest(legacy), validate_release_manifest(legacy))

future = dict(manifest)
future["schema_version"] = "9.9"
add("unknown_schema_rejected", bool(validate_release_manifest(future)), validate_release_manifest(future))

unsafe = json.loads(json.dumps(manifest))
unsafe["pdf"]["file"] = "../outside.pdf"
add("unsafe_artifact_path_rejected", any("safe artifact filename" in e for e in validate_release_manifest(unsafe)), validate_release_manifest(unsafe))

wrong_binding = json.loads(json.dumps(inspection))
wrong_binding["pdf_sha256"] = "c" * 64
add("wrong_pdf_binding_rejected", bool(validate_release_binding(manifest, wrong_binding)), validate_release_binding(manifest, wrong_binding))

bad_cert = json.loads(json.dumps(inspection))
bad_cert["certification"] = "PDF/UA"
add("false_certification_rejected", bool(validate_output_inspection(bad_cert)), validate_output_inspection(bad_cert))

failed = [c for c in checks if not c[1]]
print("Release manifest contract self-test")
for name, ok, detail in checks:
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
raise SystemExit(1 if failed else 0)
