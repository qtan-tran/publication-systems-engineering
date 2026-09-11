from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path
from typing import Any

RELEASE_MANIFEST_SCHEMA_VERSION = "0.2"
OUTPUT_INSPECTION_SCHEMA_VERSION = "0.2"
RELEASE_AUDIT_SCHEMA_VERSION = "0.2"
SUPPORTED_RELEASE_AUDIT_SCHEMAS = {"0.1", "0.2"}
RELEASE_AUDIT_INDEX_SCHEMA_VERSION = "0.1"
AUDIT_EVIDENCE_BUNDLE_SCHEMA_VERSION = "0.1"
SUPPORTED_RELEASE_MANIFEST_SCHEMAS = {"0.1", "0.2"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
ARTIFACT_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")

RELEASE_INSPECTION_POLICY = {
    "metadata_and_language": "blocking",
    "text_extractability": "human-review-on-nonpass",
    "tagging_reading_order_alt_text_conformance": "evidence-only-not-certified",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _require_str(payload: dict[str, Any], key: str, errors: list[str], *, nonempty: bool = True) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or (nonempty and not value.strip()):
        errors.append(f"{key} must be a non-empty string")
        return ""
    return value


def _require_artifact_name(payload: dict[str, Any], key: str, errors: list[str]) -> str:
    value = _require_str(payload, key, errors)
    if value and not ARTIFACT_NAME_RE.fullmatch(value):
        errors.append(f"{key} must be a single safe artifact filename")
    return value

def _require_sha256(payload: dict[str, Any], key: str, errors: list[str]) -> str:
    value = _require_str(payload, key, errors)
    if value and not SHA256_RE.fullmatch(value):
        errors.append(f"{key} must be a lowercase SHA-256 hex digest")
    return value


def validate_output_inspection(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["output inspection must be a JSON object"]
    if payload.get("schema_version") != OUTPUT_INSPECTION_SCHEMA_VERSION:
        errors.append(f"schema_version must be {OUTPUT_INSPECTION_SCHEMA_VERSION}")
    if payload.get("kind") != "pse-output-inspection":
        errors.append("kind must be pse-output-inspection")
    _require_str(payload, "pdf", errors)
    _require_sha256(payload, "pdf_sha256", errors)
    if payload.get("certification") != "none":
        errors.append("certification must be none")
    if not isinstance(payload.get("summary"), dict):
        errors.append("summary must be an object")
    checks = payload.get("checks")
    if not isinstance(checks, list):
        errors.append("checks must be an array")
    else:
        for index, check in enumerate(checks):
            if not isinstance(check, dict):
                errors.append(f"checks[{index}] must be an object")
                continue
            if not isinstance(check.get("name"), str) or not check.get("name"):
                errors.append(f"checks[{index}].name must be a non-empty string")
            if check.get("status") not in {"error", "warning", "review", "pass", "info"}:
                errors.append(f"checks[{index}].status is invalid")
            if not isinstance(check.get("machine_verifiable"), bool):
                errors.append(f"checks[{index}].machine_verifiable must be boolean")
    return errors


def validate_release_manifest(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["release manifest must be a JSON object"]
    schema_version = payload.get("schema_version")
    if schema_version not in SUPPORTED_RELEASE_MANIFEST_SCHEMAS:
        errors.append(f"unsupported schema_version: {schema_version!r}")
        return errors
    if payload.get("artifact_type") != "publication_release":
        errors.append("artifact_type must be publication_release")
    _require_str(payload, "release_id", errors)
    _require_str(payload, "pse_version", errors)
    pdf = payload.get("pdf")
    if not isinstance(pdf, dict):
        errors.append("pdf must be an object")
    else:
        _require_artifact_name(pdf, "file", errors)
        _require_sha256(pdf, "sha256", errors)
        if not isinstance(pdf.get("pages"), int) or pdf.get("pages", 0) < 1:
            errors.append("pdf.pages must be a positive integer")
        for key in ("width_mm", "height_mm"):
            if not isinstance(pdf.get(key), (int, float)) or pdf.get(key, 0) <= 0:
                errors.append(f"pdf.{key} must be a positive number")
    if schema_version == "0.2":
        inspection = payload.get("output_inspection")
        if not isinstance(inspection, dict):
            errors.append("output_inspection must be an object for schema 0.2")
        else:
            _require_artifact_name(inspection, "file", errors)
            if inspection.get("schema_version") != OUTPUT_INSPECTION_SCHEMA_VERSION:
                errors.append(f"output_inspection.schema_version must be {OUTPUT_INSPECTION_SCHEMA_VERSION}")
            _require_sha256(inspection, "sha256", errors)
            _require_sha256(inspection, "bound_pdf_sha256", errors)
            if inspection.get("policy") != RELEASE_INSPECTION_POLICY:
                errors.append("output_inspection.policy does not match the release contract")
    return errors


def validate_release_binding(manifest: dict[str, Any], inspection: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if manifest.get("schema_version") != "0.2":
        return errors
    pdf_hash = str((manifest.get("pdf") or {}).get("sha256") or "")
    inspection_meta = manifest.get("output_inspection") or {}
    bound = str(inspection_meta.get("bound_pdf_sha256") or "")
    payload_bound = str(inspection.get("pdf_sha256") or "")
    if not pdf_hash or bound != pdf_hash or payload_bound != pdf_hash:
        errors.append("output-inspection evidence is not bound to the release PDF SHA-256")
    return errors


def write_checksum_file(path: Path, files: list[Path]) -> None:
    base = Path(path).parent
    lines = [f"{sha256_file(file)}  {file.relative_to(base).as_posix()}" for file in files]
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_checksum_file(path: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    path = Path(path)
    if not path.is_file():
        return [{"code": "release_checksum_file_missing", "message": "SHA256SUMS.txt is missing from the release directory."}]
    root = path.parent
    for lineno, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or not SHA256_RE.fullmatch(parts[0]):
            findings.append({"code": "release_checksum_file_invalid", "message": f"Invalid checksum line {lineno}."})
            continue
        expected, filename = parts[0], parts[1].strip().lstrip("*")
        target = root / filename
        if not target.is_file():
            findings.append({"code": "release_checksum_target_missing", "message": f"Checksum target is missing: {filename}"})
        elif sha256_file(target) != expected:
            findings.append({"code": "release_checksum_mismatch", "message": f"Checksum mismatch for {filename}."})
    return findings


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("JSON root must be an object")
    return payload


RELEASE_CONTRACT_ID = "publication-release-manifest"
OUTPUT_INSPECTION_CONTRACT_ID = "output-inspection"
RELEASE_AUDIT_CONTRACT_ID = "release-audit-record"
RELEASE_AUDIT_INDEX_CONTRACT_ID = "release-audit-index"
AUDIT_EVIDENCE_BUNDLE_CONTRACT_ID = "audit-evidence-bundle-manifest"


def release_schema_compatibility(schema_version: Any) -> dict[str, Any]:
    if schema_version == RELEASE_MANIFEST_SCHEMA_VERSION:
        return {
            "status": "current",
            "schema_version": str(schema_version),
            "verification": "strict-current-contract",
            "creation": "supported",
            "migration": "none-required",
        }
    if schema_version == "0.1":
        return {
            "status": "legacy",
            "schema_version": "0.1",
            "verification": "verification-only-with-warning",
            "creation": "not-supported",
            "migration": "re-release-from-source-required-for-current-evidence",
        }
    return {
        "status": "unsupported",
        "schema_version": None if schema_version is None else str(schema_version),
        "verification": "rejected",
        "creation": "not-supported",
        "migration": "no-automatic-migration",
    }


def installed_contract_surface(runtime_root: Path, *, runtime_source: str = "unknown", framework_version: str = "unknown") -> dict[str, Any]:
    runtime_root = Path(runtime_root).resolve()
    schema_root = runtime_root / "schema"
    contracts = [
        {
            "id": RELEASE_CONTRACT_ID,
            "current_schema_version": RELEASE_MANIFEST_SCHEMA_VERSION,
            "created_schema_versions": [RELEASE_MANIFEST_SCHEMA_VERSION],
            "verification_schema_versions": sorted(SUPPORTED_RELEASE_MANIFEST_SCHEMAS),
            "legacy_verification_schema_versions": ["0.1"],
            "schema_file": "release-manifest-0.2.schema.json",
            "schema_path": str((schema_root / "release-manifest-0.2.schema.json").resolve()),
            "installed": (schema_root / "release-manifest-0.2.schema.json").is_file(),
        },
        {
            "id": OUTPUT_INSPECTION_CONTRACT_ID,
            "current_schema_version": OUTPUT_INSPECTION_SCHEMA_VERSION,
            "created_schema_versions": [OUTPUT_INSPECTION_SCHEMA_VERSION],
            "verification_schema_versions": [OUTPUT_INSPECTION_SCHEMA_VERSION],
            "legacy_verification_schema_versions": [],
            "schema_file": "output-inspection-0.2.schema.json",
            "schema_path": str((schema_root / "output-inspection-0.2.schema.json").resolve()),
            "installed": (schema_root / "output-inspection-0.2.schema.json").is_file(),
        },
        {
            "id": RELEASE_AUDIT_CONTRACT_ID,
            "current_schema_version": RELEASE_AUDIT_SCHEMA_VERSION,
            "created_schema_versions": [RELEASE_AUDIT_SCHEMA_VERSION],
            "verification_schema_versions": sorted(SUPPORTED_RELEASE_AUDIT_SCHEMAS),
            "legacy_verification_schema_versions": ["0.1"],
            "schema_file": "release-audit-record-0.2.schema.json",
            "schema_path": str((schema_root / "release-audit-record-0.2.schema.json").resolve()),
            "installed": (schema_root / "release-audit-record-0.2.schema.json").is_file(),
        },
        {
            "id": RELEASE_AUDIT_INDEX_CONTRACT_ID,
            "current_schema_version": RELEASE_AUDIT_INDEX_SCHEMA_VERSION,
            "created_schema_versions": [RELEASE_AUDIT_INDEX_SCHEMA_VERSION],
            "verification_schema_versions": [RELEASE_AUDIT_INDEX_SCHEMA_VERSION],
            "legacy_verification_schema_versions": [],
            "schema_file": "release-audit-index-0.1.schema.json",
            "schema_path": str((schema_root / "release-audit-index-0.1.schema.json").resolve()),
            "installed": (schema_root / "release-audit-index-0.1.schema.json").is_file(),
        },
        {
            "id": AUDIT_EVIDENCE_BUNDLE_CONTRACT_ID,
            "current_schema_version": AUDIT_EVIDENCE_BUNDLE_SCHEMA_VERSION,
            "created_schema_versions": [AUDIT_EVIDENCE_BUNDLE_SCHEMA_VERSION],
            "verification_schema_versions": [AUDIT_EVIDENCE_BUNDLE_SCHEMA_VERSION],
            "legacy_verification_schema_versions": [],
            "schema_file": "audit-evidence-bundle-manifest-0.1.schema.json",
            "schema_path": str((schema_root / "audit-evidence-bundle-manifest-0.1.schema.json").resolve()),
            "installed": (schema_root / "audit-evidence-bundle-manifest-0.1.schema.json").is_file(),
        },
    ]
    schema_files = sorted(p.name for p in schema_root.glob("*.json") if p.is_file()) if schema_root.is_dir() else []
    return {
        "schema_version": "0.1",
        "kind": "pse-installed-contract-surface",
        "framework_version": framework_version,
        "runtime_source": runtime_source,
        "runtime_root": str(runtime_root),
        "contracts": contracts,
        "installed_schema_files": schema_files,
    }


def release_migration_assessment(release_root: Path, manifest: dict[str, Any], *, verification_status: str) -> dict[str, Any]:
    release_root = Path(release_root).resolve()
    schema_version = manifest.get("schema_version") if isinstance(manifest, dict) else None
    compatibility = release_schema_compatibility(schema_version)
    manifest_path = release_root / "release-manifest.json"
    pdf_meta = manifest.get("pdf") if isinstance(manifest, dict) else None
    pdf_name = str((pdf_meta or {}).get("file") or "") if isinstance(pdf_meta, dict) else ""
    pdf_path = release_root / pdf_name if pdf_name else None
    source_pdf_sha256 = sha256_file(pdf_path) if pdf_path and pdf_path.is_file() else None

    if compatibility["status"] == "current":
        migration_status = "already-current"
        recommended_action = "Keep the existing schema 0.2 release immutable; no migration is required."
    elif compatibility["status"] == "legacy":
        migration_status = "legacy-verifiable-not-upgraded"
        recommended_action = (
            "Preserve the historical schema 0.1 release unchanged. To obtain schema 0.2 output-inspection "
            "and PDF-binding evidence, re-release from the original source project with a current PSE runtime."
        )
    else:
        migration_status = "unsupported-no-automatic-migration"
        recommended_action = "Do not rewrite the artifact. Use a runtime that explicitly supports this schema or recover the original source project."

    return {
        "schema_version": "0.1",
        "kind": "pse-release-migration-assessment",
        "source_release_dir": str(release_root),
        "source_release_id": manifest.get("release_id") if isinstance(manifest, dict) else None,
        "source_manifest_schema_version": schema_version,
        "source_manifest_sha256": sha256_file(manifest_path) if manifest_path.is_file() else None,
        "source_pdf_sha256": source_pdf_sha256,
        "verification_status": verification_status,
        "compatibility": compatibility,
        "target_manifest_schema_version": RELEASE_MANIFEST_SCHEMA_VERSION,
        "migration_status": migration_status,
        "historical_artifact_mutated": False,
        "in_place_upgrade_supported": False,
        "retroactive_output_inspection_inferred": False,
        "recommended_action": recommended_action,
    }


def _fingerprint_inputs(release_root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    release_root = Path(release_root).resolve()
    manifest_path = release_root / "release-manifest.json"
    checksum_path = release_root / "SHA256SUMS.txt"
    pdf_meta = manifest.get("pdf") if isinstance(manifest, dict) else None
    pdf_name = str((pdf_meta or {}).get("file") or "") if isinstance(pdf_meta, dict) else ""
    pdf_path = release_root / pdf_name if pdf_name else None
    return {
        "release_id": manifest.get("release_id") if isinstance(manifest, dict) else None,
        "manifest_schema_version": manifest.get("schema_version") if isinstance(manifest, dict) else None,
        "manifest_sha256": sha256_file(manifest_path) if manifest_path.is_file() else None,
        "pdf_sha256": sha256_file(pdf_path) if pdf_path and pdf_path.is_file() else None,
        "checksum_file_sha256": sha256_file(checksum_path) if checksum_path.is_file() else None,
    }


def release_fingerprint(release_root: Path, manifest: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    """Return path-independent identity for the observed immutable release state."""
    inputs = _fingerprint_inputs(release_root, manifest)
    canonical = json.dumps(inputs, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest(), inputs


def _fingerprint_from_inputs(inputs: dict[str, Any]) -> str:
    canonical = json.dumps(inputs, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def release_audit_record(release_root: Path, manifest: dict[str, Any], verification_report: dict[str, Any], *, framework_version: str, generated_utc: str) -> dict[str, Any]:
    """Create a non-mutating audit record bound to the release state observed at audit time."""
    release_root = Path(release_root).resolve()
    pdf_meta = manifest.get("pdf") if isinstance(manifest, dict) else None
    pdf_name = str((pdf_meta or {}).get("file") or "") if isinstance(pdf_meta, dict) else ""
    fingerprint, fingerprint_inputs = release_fingerprint(release_root, manifest)
    return {
        "schema_version": RELEASE_AUDIT_SCHEMA_VERSION,
        "kind": "pse-release-audit-record",
        "generated_utc": generated_utc,
        "pse_version": framework_version,
        "source_release_dir": str(release_root),
        "source_release_id": manifest.get("release_id") if isinstance(manifest, dict) else None,
        "source_manifest_schema_version": manifest.get("schema_version") if isinstance(manifest, dict) else None,
        "source_manifest_sha256": fingerprint_inputs["manifest_sha256"],
        "source_pdf_file": pdf_name or None,
        "source_pdf_sha256": fingerprint_inputs["pdf_sha256"],
        "source_checksum_file_sha256": fingerprint_inputs["checksum_file_sha256"],
        "release_fingerprint": fingerprint,
        "release_fingerprint_inputs": fingerprint_inputs,
        "compatibility": release_schema_compatibility(manifest.get("schema_version") if isinstance(manifest, dict) else None),
        "verification": verification_report,
        "audit_status": "fail" if verification_report.get("status") == "fail" else "pass",
        "historical_artifact_mutated": False,
        "audit_record_is_release_artifact": False,
        "scope_note": "Audit evidence records observed release state; absolute paths are informational only and are excluded from the portable release fingerprint.",
    }


def validate_release_audit_record(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["release audit record must be a JSON object"]
    schema_version = payload.get("schema_version")
    if schema_version not in SUPPORTED_RELEASE_AUDIT_SCHEMAS:
        errors.append(f"unsupported audit schema_version: {schema_version!r}")
        return errors
    if payload.get("kind") != "pse-release-audit-record":
        errors.append("kind must be pse-release-audit-record")
    for key in ("generated_utc", "pse_version", "source_release_dir", "source_release_id", "source_manifest_schema_version"):
        _require_str(payload, key, errors)
    for key in ("source_manifest_sha256", "source_pdf_sha256"):
        _require_sha256(payload, key, errors)
    checksum_hash = payload.get("source_checksum_file_sha256")
    if checksum_hash is not None and (not isinstance(checksum_hash, str) or not SHA256_RE.fullmatch(checksum_hash)):
        errors.append("source_checksum_file_sha256 must be null or a lowercase SHA-256 hex digest")
    if schema_version == "0.2":
        fingerprint = _require_sha256(payload, "release_fingerprint", errors)
        inputs = payload.get("release_fingerprint_inputs")
        if not isinstance(inputs, dict):
            errors.append("release_fingerprint_inputs must be an object")
        else:
            for key in ("release_id", "manifest_schema_version"):
                _require_str(inputs, key, errors)
            for key in ("manifest_sha256", "pdf_sha256"):
                _require_sha256(inputs, key, errors)
            checksum = inputs.get("checksum_file_sha256")
            if checksum is not None and (not isinstance(checksum, str) or not SHA256_RE.fullmatch(checksum)):
                errors.append("release_fingerprint_inputs.checksum_file_sha256 must be null or SHA-256")
            if fingerprint and _fingerprint_from_inputs(inputs) != fingerprint:
                errors.append("release_fingerprint does not match release_fingerprint_inputs")
    if not isinstance(payload.get("verification"), dict):
        errors.append("verification must be an object")
    if payload.get("audit_status") not in {"pass", "fail"}:
        errors.append("audit_status must be pass or fail")
    if payload.get("historical_artifact_mutated") is not False:
        errors.append("historical_artifact_mutated must be false")
    if payload.get("audit_record_is_release_artifact") is not False:
        errors.append("audit_record_is_release_artifact must be false")
    return errors


def release_audit_index(collection_root: Path, records: list[dict[str, Any]], *, framework_version: str, generated_utc: str) -> dict[str, Any]:
    """Build an external batch index from audit records without altering any release."""
    collection_root = Path(collection_root).resolve()
    entries = []
    fingerprints = []
    for record in records:
        fp = str(record.get("release_fingerprint") or "")
        fingerprints.append(fp)
        source = Path(str(record.get("source_release_dir") or ""))
        try:
            relative_source = source.relative_to(collection_root).as_posix()
        except ValueError:
            relative_source = source.name
        entries.append({
            "relative_source_release": relative_source,
            "source_release_id": record.get("source_release_id"),
            "source_manifest_schema_version": record.get("source_manifest_schema_version"),
            "release_fingerprint": fp,
            "audit_status": record.get("audit_status"),
            "compatibility_status": (record.get("compatibility") or {}).get("status"),
            "source_manifest_sha256": record.get("source_manifest_sha256"),
            "source_pdf_sha256": record.get("source_pdf_sha256"),
            "source_checksum_file_sha256": record.get("source_checksum_file_sha256"),
        })
    entries.sort(key=lambda x: (str(x.get("source_release_id") or ""), str(x.get("release_fingerprint") or "")))
    batch_material = json.dumps(sorted(fingerprints), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "schema_version": RELEASE_AUDIT_INDEX_SCHEMA_VERSION,
        "kind": "pse-release-audit-index",
        "generated_utc": generated_utc,
        "pse_version": framework_version,
        "collection_dir": str(collection_root),
        "release_count": len(entries),
        "batch_fingerprint": hashlib.sha256(batch_material).hexdigest(),
        "entries": entries,
        "batch_status": "fail" if any(e.get("audit_status") == "fail" for e in entries) else "pass",
        "historical_artifacts_mutated": False,
        "index_is_release_artifact": False,
        "scope_note": "Batch audit evidence is external. Collection and release paths are informational only and are excluded from release fingerprints and batch fingerprint identity.",
    }


def validate_release_audit_index(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["release audit index must be a JSON object"]
    if payload.get("schema_version") != RELEASE_AUDIT_INDEX_SCHEMA_VERSION:
        errors.append(f"schema_version must be {RELEASE_AUDIT_INDEX_SCHEMA_VERSION}")
    if payload.get("kind") != "pse-release-audit-index":
        errors.append("kind must be pse-release-audit-index")
    _require_str(payload, "generated_utc", errors)
    _require_str(payload, "pse_version", errors)
    _require_str(payload, "collection_dir", errors)
    _require_sha256(payload, "batch_fingerprint", errors)
    entries = payload.get("entries")
    if not isinstance(entries, list):
        errors.append("entries must be an array")
        entries = []
    if payload.get("release_count") != len(entries):
        errors.append("release_count must equal entries length")
    fingerprints = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{i}] must be an object")
            continue
        _require_str(entry, "relative_source_release", errors)
        _require_str(entry, "source_release_id", errors)
        fp = _require_sha256(entry, "release_fingerprint", errors)
        if fp:
            fingerprints.append(fp)
        if entry.get("audit_status") not in {"pass", "fail"}:
            errors.append(f"entries[{i}].audit_status must be pass or fail")
    expected_batch = hashlib.sha256(json.dumps(sorted(fingerprints), sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()
    if isinstance(payload.get("batch_fingerprint"), str) and payload.get("batch_fingerprint") != expected_batch:
        errors.append("batch_fingerprint does not match indexed release fingerprints")
    expected_status = "fail" if any(isinstance(e, dict) and e.get("audit_status") == "fail" for e in entries) else "pass"
    if payload.get("batch_status") != expected_status:
        errors.append("batch_status does not match entry audit statuses")
    if payload.get("historical_artifacts_mutated") is not False:
        errors.append("historical_artifacts_mutated must be false")
    if payload.get("index_is_release_artifact") is not False:
        errors.append("index_is_release_artifact must be false")
    return errors


def verify_release_audit_record_payload(payload: Any, *, release_root: Path | None = None) -> dict[str, Any]:
    """Verify an audit record detached, and optionally bind it again to a release directory."""
    findings: list[dict[str, str]] = []
    errors = validate_release_audit_record(payload)
    for error in errors:
        findings.append({"code": "audit_record_contract_invalid", "message": error})
    source_binding = "not-requested"
    if not errors and release_root is not None:
        release_root = Path(release_root).resolve()
        manifest_path = release_root / "release-manifest.json"
        if not manifest_path.is_file():
            findings.append({"code": "audit_source_manifest_missing", "message": "release-manifest.json is missing from the supplied release directory."})
        else:
            try:
                manifest = load_json_object(manifest_path)
            except Exception as exc:
                findings.append({"code": "audit_source_manifest_invalid", "message": str(exc)})
            else:
                current_fp, current_inputs = release_fingerprint(release_root, manifest)
                if payload.get("schema_version") == "0.2" and payload.get("release_fingerprint") != current_fp:
                    findings.append({"code": "audit_release_fingerprint_mismatch", "message": "Current release state does not match the recorded portable release fingerprint."})
                if payload.get("source_manifest_sha256") != current_inputs.get("manifest_sha256"):
                    findings.append({"code": "audit_manifest_hash_mismatch", "message": "Current release manifest SHA-256 differs from the audit record."})
                if payload.get("source_pdf_sha256") != current_inputs.get("pdf_sha256"):
                    findings.append({"code": "audit_pdf_hash_mismatch", "message": "Current release PDF SHA-256 differs from the audit record."})
                if payload.get("source_checksum_file_sha256") != current_inputs.get("checksum_file_sha256"):
                    findings.append({"code": "audit_checksum_hash_mismatch", "message": "Current release checksum-file SHA-256 differs from the audit record."})
                source_binding = "match" if not findings else "mismatch"
    return {
        "schema_version": "0.1",
        "kind": "pse-audit-record-verification",
        "status": "fail" if findings else "pass",
        "detached_contract_verified": not errors,
        "source_binding": source_binding,
        "findings": findings,
    }


def verify_release_audit_index_payload(payload: Any, *, collection_root: Path | None = None) -> dict[str, Any]:
    """Verify an audit index detached, and optionally compare its entries with a release collection."""
    findings: list[dict[str, str]] = []
    errors = validate_release_audit_index(payload)
    for error in errors:
        findings.append({"code": "audit_index_contract_invalid", "message": error})
    source_binding = "not-requested"
    if not errors and collection_root is not None:
        collection_root = Path(collection_root).resolve()
        for entry in payload.get("entries", []):
            rel = str(entry.get("relative_source_release") or "")
            candidate = (collection_root / rel).resolve()
            try:
                candidate.relative_to(collection_root)
            except ValueError:
                findings.append({"code": "audit_index_source_escape", "message": f"Indexed release escapes collection root: {rel}"})
                continue
            manifest_path = candidate / "release-manifest.json"
            if not manifest_path.is_file():
                findings.append({"code": "audit_index_source_missing", "message": f"Indexed release is missing: {rel}"})
                continue
            try:
                manifest = load_json_object(manifest_path)
                current_fp, current_inputs = release_fingerprint(candidate, manifest)
            except Exception as exc:
                findings.append({"code": "audit_index_source_invalid", "message": f"{rel}: {exc}"})
                continue
            if current_fp != entry.get("release_fingerprint"):
                findings.append({"code": "audit_index_fingerprint_mismatch", "message": f"Release fingerprint differs for {rel}."})
            if current_inputs.get("manifest_sha256") != entry.get("source_manifest_sha256"):
                findings.append({"code": "audit_index_manifest_hash_mismatch", "message": f"Manifest hash differs for {rel}."})
            if current_inputs.get("pdf_sha256") != entry.get("source_pdf_sha256"):
                findings.append({"code": "audit_index_pdf_hash_mismatch", "message": f"PDF hash differs for {rel}."})
            if current_inputs.get("checksum_file_sha256") != entry.get("source_checksum_file_sha256"):
                findings.append({"code": "audit_index_checksum_hash_mismatch", "message": f"Checksum-file hash differs for {rel}."})
        source_binding = "match" if not findings else "mismatch"
    return {
        "schema_version": "0.1",
        "kind": "pse-audit-index-verification",
        "status": "fail" if findings else "pass",
        "detached_contract_verified": not errors,
        "source_binding": source_binding,
        "findings": findings,
    }


def audit_evidence_bundle_manifest(evidence_files: list[Path]) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for path in evidence_files:
        path = Path(path)
        name = path.name
        if not ARTIFACT_NAME_RE.fullmatch(name):
            raise ValueError(f"unsafe evidence filename: {name}")
        if name in seen:
            raise ValueError(f"duplicate evidence filename: {name}")
        seen.add(name)
        payload = load_json_object(path)
        kind = str(payload.get("kind") or "")
        schema_version = str(payload.get("schema_version") or "")
        if kind == "pse-release-audit-record":
            contract_errors = validate_release_audit_record(payload)
        elif kind == "pse-release-audit-index":
            contract_errors = validate_release_audit_index(payload)
        else:
            raise ValueError(f"unsupported evidence kind in {name}: {kind!r}")
        if contract_errors:
            raise ValueError(f"invalid evidence {name}: " + "; ".join(contract_errors))
        entries.append({"file": name, "kind": kind, "schema_version": schema_version, "sha256": sha256_file(path)})
    entries.sort(key=lambda x: x["file"])
    material = json.dumps(entries, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "schema_version": AUDIT_EVIDENCE_BUNDLE_SCHEMA_VERSION,
        "kind": "pse-audit-evidence-bundle-manifest",
        "entry_count": len(entries),
        "entries": entries,
        "bundle_fingerprint": hashlib.sha256(material).hexdigest(),
        "contains_publication_release_artifacts": False,
        "scope_note": "This deterministic export contains audit evidence only; it is not a publication release, signature, PKI assertion, or trusted timestamp.",
    }


def validate_audit_evidence_bundle_manifest(payload: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["audit evidence bundle manifest must be a JSON object"]
    if payload.get("schema_version") != AUDIT_EVIDENCE_BUNDLE_SCHEMA_VERSION:
        errors.append(f"schema_version must be {AUDIT_EVIDENCE_BUNDLE_SCHEMA_VERSION}")
    if payload.get("kind") != "pse-audit-evidence-bundle-manifest":
        errors.append("kind must be pse-audit-evidence-bundle-manifest")
    entries = payload.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries must be a non-empty array")
        entries = []
    if payload.get("entry_count") != len(entries):
        errors.append("entry_count must equal entries length")
    names: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{i}] must be an object")
            continue
        name = _require_artifact_name(entry, "file", errors)
        if name in names:
            errors.append(f"duplicate evidence filename: {name}")
        names.add(name)
        kind = _require_str(entry, "kind", errors)
        schema = _require_str(entry, "schema_version", errors)
        digest = _require_sha256(entry, "sha256", errors)
        normalized.append({"file": name, "kind": kind, "schema_version": schema, "sha256": digest})
    material = json.dumps(sorted(normalized, key=lambda x: x["file"]), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    expected = hashlib.sha256(material).hexdigest()
    if payload.get("bundle_fingerprint") != expected:
        errors.append("bundle_fingerprint does not match bundle entries")
    if payload.get("contains_publication_release_artifacts") is not False:
        errors.append("contains_publication_release_artifacts must be false")
    return errors


def write_deterministic_audit_bundle(output: Path, evidence_files: list[Path]) -> dict[str, Any]:
    """Write byte-reproducible ZIP for identical evidence bytes and filenames."""
    output = Path(output)
    evidence_files = [Path(p) for p in evidence_files]
    manifest = audit_evidence_bundle_manifest(evidence_files)
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as zf:
        items = [("audit-evidence-bundle-manifest.json", manifest_bytes)]
        items += [(p.name, p.read_bytes()) for p in evidence_files]
        for name, data in sorted(items, key=lambda x: x[0]):
            info = zipfile.ZipInfo(filename=name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            zf.writestr(info, data)
    return manifest
