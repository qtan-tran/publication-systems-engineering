from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Assess PSE release-candidate readiness without inventing external evidence.")
    parser.add_argument("--output", type=Path, default=ROOT / "tests" / "_output" / "release-evidence" / "rc-readiness.json")
    parser.add_argument("--require-public-beta", action="store_true", help="Return non-zero while any public-beta hard gate remains open.")
    args = parser.parse_args()

    package_version = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    public_version = re.sub(r"a(\d+)$", r"-alpha", package_version)
    runtime = json.loads((ROOT / "runtime" / "pse-runtime.json").read_text(encoding="utf-8"))
    profiles = runtime.get("profiles", [])
    modules = runtime.get("modules", [])

    checks = []
    def check(name: str, passed: bool, detail: object = "") -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    check("version_synchronized", runtime.get("runtime_version") == public_version, public_version)
    check("profile_surface_frozen", len(profiles) == 9, {"profiles": len(profiles)})
    check("module_surface_frozen", len(modules) == 14, {"modules": len(modules)})
    check("root_license_absent_until_review", not (ROOT / "LICENSE").exists())
    check("candidate_workflow_present", (ROOT / ".github" / "workflows" / "beta-candidate.yml").is_file())
    check("release_evidence_workflow_present", (ROOT / ".github" / "workflows" / "release-evidence.yml").is_file())
    check("documentation_pages_workflow_present", (ROOT / ".github" / "workflows" / "docs-pages.yml").is_file())
    check("public_beta_checklist_present", (ROOT / "docs" / "beta" / "PUBLIC-BETA-CHECKLIST.md").is_file())
    check("surface_freeze_recorded", (ROOT / "docs" / "beta" / "RC-SURFACE-FREEZE.md").is_file())

    # Readiness reports must be sequence-independent: regression output directories may exist while a test run is in progress.
    # The integrity gate itself is therefore required here and executed separately by candidate/live-CI workflows.
    check("public_tree_integrity_gate_present", (ROOT / "tests" / "regression" / "public_tree_integrity.py").is_file())

    external_gates = [
        {"code": "legal_review", "status": "blocked", "detail": "Final public/community and commercial licensing instruments require independent legal review."},
        {"code": "operative_license", "status": "blocked", "detail": "Root LICENSE must remain absent until the legally reviewed instrument is approved."},
        {"code": "contributor_rights", "status": "blocked", "detail": "Contributor-rights and dual-licensing permissions require final legal/maintainer approval."},
        {"code": "commercial_contact", "status": "blocked", "detail": "A real commercial-licensing inquiry channel has not yet been published."},
        {"code": "live_exact_candidate_ci", "status": "blocked", "detail": "Windows, macOS, Linux and release-evidence workflows must pass live on the exact candidate commit."},
        {"code": "live_documentation_render", "status": "blocked", "detail": "The strict MkDocs Material build and generated-site QA must pass in the live Pages workflow."},
    ]

    internal_pass = all(item["passed"] for item in checks)
    public_beta_ready = internal_pass and all(gate["status"] == "pass" for gate in external_gates)
    payload = {
        "audit_kind": "rc_readiness",
        "framework_version": public_version,
        "internal_technical_checks_passed": internal_pass,
        "public_beta_ready": public_beta_ready,
        "surface_freeze": {"profiles": len(profiles), "semantic_modules": len(modules), "new_features_before_gate_clearance": False},
        "checks": checks,
        "external_hard_gates": external_gates,
        "decision": "stabilization_only_not_public_rc" if not public_beta_ready else "eligible_for_maintainer_release_decision",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    if args.require_public_beta and not public_beta_ready:
        return 2
    return 0 if internal_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
