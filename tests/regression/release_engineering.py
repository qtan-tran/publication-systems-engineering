from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ENV = os.environ.copy()
ENV["PYTHONPATH"] = str(REPO / "tools") + os.pathsep + ENV.get("PYTHONPATH", "")


def run(*args: str, expect: int = 0, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [sys.executable, "-m", "pse_cli.cli", *args]
    proc = subprocess.run(cmd, cwd=cwd or REPO, env=ENV, text=True, capture_output=True)
    if proc.returncode != expect:
        raise AssertionError(f"command failed ({proc.returncode}, expected {expect}): {' '.join(cmd)}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}")
    return proc


def git(project: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=project, text=True, capture_output=True, check=True)


def main() -> int:
    checks: list[tuple[str, bool, str]] = []
    with tempfile.TemporaryDirectory(prefix="pse-regression") as td:
        parent = Path(td)
        run("new", str(parent), "--non-interactive", "--title", "Release Fixture", "--author", "Synthetic Editor", "--language", "en", "--publication-year", "2027", "--slug", "release-fixture")
        project = parent / "release-fixture"

        # Establish Git provenance, then deliberately dirty the manuscript.
        git(project, "init")
        git(project, "config", "user.email", "regression@example.invalid")
        git(project, "config", "user.name", "PSE Regression")
        git(project, "add", ".")
        git(project, "commit", "-m", "fixture baseline")
        chapter = project / "content" / "chapter-01.tex"
        chapter.write_text(chapter.read_text(encoding="utf-8") + "\nDirty-state regression sentence.\n", encoding="utf-8")

        blocked = run("release", str(project), "--release-id", "PSE-R-G-BLOCKED", expect=1)
        checks.append(("review_gate_blocks_dirty_release", "acknowledgement" in (blocked.stderr + blocked.stdout).lower(), (blocked.stderr + blocked.stdout)[-500:]))

        run("release", str(project), "--release-id", "PSE-R-G-001", "--acknowledge-review")
        release = project / "release" / "PSE-R-G-001"
        manifest = json.loads((release / "release-manifest.json").read_text(encoding="utf-8"))
        checks.append(("release_artifact_contract", (release / manifest["pdf"]["file"]).is_file() and (release / "qa-report.json").is_file() and (release / "SHA256SUMS.txt").is_file(), str(list(p.name for p in release.iterdir()))))
        checks.append(("dirty_state_recorded", manifest.get("project_dirty") is True and manifest.get("qa", {}).get("review_acknowledged") is True, str({"dirty": manifest.get("project_dirty"), "ack": manifest.get("qa", {}).get("review_acknowledged")})))
        checks.append(("byte_reproducible", manifest.get("reproducibility", {}).get("byte_identical") is True, str(manifest.get("reproducibility"))))
        attribution = manifest.get("attribution", {})
        checks.append(("mandatory_attribution_rendered", attribution.get("required") is True and attribution.get("rendered") is True and bool(attribution.get("asset_sha256")), str(attribution)))

        inspection_meta = manifest.get("output_inspection", {})
        inspection_path = release / str(inspection_meta.get("file", ""))
        inspection = json.loads(inspection_path.read_text(encoding="utf-8")) if inspection_path.is_file() else {}
        checks.append((
            "output_inspection_artifact_contract",
            inspection_path.is_file()
            and inspection_meta.get("bound_pdf_sha256") == manifest.get("pdf", {}).get("sha256")
            and inspection.get("pdf_sha256") == manifest.get("pdf", {}).get("sha256")
            and inspection.get("certification") == "none",
            str({"manifest": inspection_meta, "report_status": inspection.get("status"), "certification": inspection.get("certification")}),
        ))
        checks.append((
            "output_inspection_release_policy",
            inspection_meta.get("policy", {}).get("metadata_and_language") == "blocking"
            and inspection_meta.get("policy", {}).get("text_extractability") == "human-review-on-nonpass"
            and inspection_meta.get("policy", {}).get("tagging_reading_order_alt_text_conformance") == "evidence-only-not-certified",
            str(inspection_meta.get("policy")),
        ))

        verify = run("verify-release", str(release))
        checks.append(("verify_release_pass", '"status": "pass"' in verify.stdout, verify.stdout[-400:]))
        checks.append(("manifest_schema_0_2", manifest.get("schema_version") == "0.2", str(manifest.get("schema_version"))))

        # Contract validation must detect semantic tampering even when checksums are refreshed.
        original_manifest = (release / "release-manifest.json").read_bytes()
        bad_manifest = json.loads(original_manifest.decode("utf-8"))
        bad_manifest["output_inspection"]["policy"]["metadata_and_language"] = "advisory"
        (release / "release-manifest.json").write_text(json.dumps(bad_manifest, indent=2) + "\n", encoding="utf-8")
        sums = release / "SHA256SUMS.txt"
        lines = []
        import hashlib
        for target in [release / manifest["pdf"]["file"], release / "release-manifest.json", release / "qa-report.json", release / "output-inspection.json"]:
            lines.append(f"{hashlib.sha256(target.read_bytes()).hexdigest()}  {target.name}")
        sums.write_text("\n".join(lines) + "\n", encoding="utf-8")
        contract_tampered = run("verify-release", str(release), expect=1)
        checks.append(("manifest_contract_tamper_detection", "release_manifest_contract_invalid" in contract_tampered.stdout, contract_tampered.stdout[-600:]))
        (release / "release-manifest.json").write_bytes(original_manifest)
        lines = []
        for target in [release / manifest["pdf"]["file"], release / "release-manifest.json", release / "qa-report.json", release / "output-inspection.json"]:
            lines.append(f"{hashlib.sha256(target.read_bytes()).hexdigest()}  {target.name}")
        sums.write_text("\n".join(lines) + "\n", encoding="utf-8")

        # Schema 0.1 remains readable as a legacy verification contract; no inspection evidence is inferred.
        legacy = parent / "legacy-release"
        shutil.copytree(release, legacy)
        legacy_manifest_path = legacy / "release-manifest.json"
        legacy_manifest = json.loads(legacy_manifest_path.read_text(encoding="utf-8"))
        legacy_manifest["schema_version"] = "0.1"
        legacy_manifest.pop("output_inspection", None)
        legacy_manifest_path.write_text(json.dumps(legacy_manifest, indent=2) + "\n", encoding="utf-8")
        legacy_lines = []
        for target in [legacy / legacy_manifest["pdf"]["file"], legacy_manifest_path, legacy / "qa-report.json", legacy / "output-inspection.json"]:
            legacy_lines.append(f"{hashlib.sha256(target.read_bytes()).hexdigest()}  {target.name}")
        (legacy / "SHA256SUMS.txt").write_text("\n".join(legacy_lines) + "\n", encoding="utf-8")
        legacy_verify = run("verify-release", str(legacy))
        checks.append(("legacy_manifest_0_1_compatibility", "legacy_release_manifest_schema" in legacy_verify.stdout and '"status": "pass"' in legacy_verify.stdout, legacy_verify.stdout[-600:]))

        original_inspection = inspection_path.read_bytes()
        inspection_path.write_bytes(original_inspection + b"\n ")
        inspection_tampered = run("verify-release", str(release), expect=1)
        checks.append(("inspection_evidence_tamper_detection", "output_inspection_checksum_mismatch" in inspection_tampered.stdout or "checksum_mismatch" in inspection_tampered.stdout, inspection_tampered.stdout[-500:]))
        inspection_path.write_bytes(original_inspection)

        pdf = release / manifest["pdf"]["file"]
        with pdf.open("ab") as fh:
            fh.write(b"PSE_TAMPER_SENTINEL")
        tampered = run("verify-release", str(release), expect=1)
        checks.append(("tamper_detection", "checksum_mismatch" in tampered.stdout, tampered.stdout[-500:]))

        # release/ must remain outside the source-of-truth tracked set.
        ignored = git(project, "check-ignore", "release/PSE-R-G-001/release-manifest.json")
        checks.append(("release_gitignored", ignored.returncode == 0, ignored.stdout.strip()))

    failed = [c for c in checks if not c[1]]
    print("Release engineering self-test")
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
