from __future__ import annotations
import json
import re
import subprocess
import sys
import tomllib
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "tests" / "_output" / "regression-output"
OUT.mkdir(parents=True, exist_ok=True)
checks = []

def record(name, ok, detail=""):
    checks.append({"name": name, "passed": bool(ok), "detail": detail})
    if not ok:
        print(f"FAIL: {name}: {detail}")

# Version synchronization. The public package version is the source of truth.
pyproject_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
package_version = tomllib.loads(pyproject_text)["project"]["version"]
public_version = re.sub(r"a(\d+)$", r"-alpha", package_version)
cli = (ROOT / "tools/pse_cli/cli.py").read_text(encoding="utf-8")
init = (ROOT / "tools/pse_cli/__init__.py").read_text(encoding="utf-8")
runtime = json.loads((ROOT / "runtime/pse-runtime.json").read_text(encoding="utf-8"))
citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
record("version_pyproject", bool(re.fullmatch(r"\d+\.\d+\.\d+a\d+", package_version)), package_version)
record("version_cli", f'VERSION = "{public_version}"' in cli and f'__version__ = "{public_version}"' in init, public_version)
record("version_runtime_citation", runtime.get("runtime_version") == public_version and citation.count(f'version: "{public_version}"') >= 2, public_version)

# Required staging docs/templates.
required = [
    "docs/beta/BETA-CANDIDATE-FREEZE.md",
    "docs/beta/PUBLIC-BETA-CHECKLIST.md",
    "docs/beta/RC-SURFACE-FREEZE.md",
    "docs/beta/RC-READINESS-REVIEW.md",
    "scripts/release/rc_readiness.py",
    "docs/architecture/COMPATIBILITY-MIGRATION-POLICY.md",
    "docs/reference/CLI-COMPATIBILITY-MATRIX.md",
    "docs/reference/API-SCHEMA-COMPATIBILITY.md",
    "docs/reference/SUPPORT-MATRIX.md",
    "docs/workflows/ONBOARDING.md",
    "docs/licensing/COMMERCIAL-LICENSING-INQUIRY.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/feature_request.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/beta-candidate.yml",
    "scripts/release/candidate_evidence.py",
    ".github/workflows/release-evidence.yml",
]
record("staging_files", all((ROOT / p).is_file() for p in required), ", ".join(p for p in required if not (ROOT / p).is_file()))

# GitHub YAML must parse as YAML. PyYAML interprets `on` as a YAML 1.1 boolean, but parsing itself must succeed.
try:
    for p in [ROOT / ".github/workflows/beta-candidate.yml", ROOT / ".github/ISSUE_TEMPLATE/bug_report.yml", ROOT / ".github/ISSUE_TEMPLATE/feature_request.yml"]:
        yaml.safe_load(p.read_text(encoding="utf-8"))
    record("github_yaml_parse", True)
except Exception as e:
    record("github_yaml_parse", False, repr(e))

# README synchronization and legal status.
readme = (ROOT / "README.md").read_text(encoding="utf-8")
readme_vi = (ROOT / "README.vi.md").read_text(encoding="utf-8")
record("readme_status", public_version in readme and public_version in readme_vi and "not yet a public licensed beta" in readme and "chưa phải public licensed beta" in readme_vi)
record("readme_not_public_beta", "not yet a public licensed beta" in readme and "chưa phải public licensed beta" in readme_vi)
record("legal_gate_visible", "legal review" in readme.lower() and "legal review" in readme_vi.lower())

# Final LICENSE must still be absent until legal review.
record("license_hard_gate_preserved", not (ROOT / "LICENSE").exists())

# Public docs must not contain the reserved design-reference terms.
# Terms are represented only by SHA-256 fingerprints so the public repository does not itself reproduce them.
import hashlib
reserved = {
    (3, "2ae51bf9b0cc6ec1cbef6ddb5b4ad9ba2f6f3e3099bd86dd347d7a9d3bf970b6"),
    (5, "869fd96f5f47143da9c1ed6171581be03ea3ccf23bf0639cf71d42f907aa4512"),
    (1, "5779b3939b57acd8c35a5b1049900eb80e3ab6dd0c98cacaaf34b66db26ab762"),
    (1, "46b5716336845d36dd27e4800a6cd57a87e3bccd4b0f484ddd84b378ea067ef0"),
    (1, "55293d3ffed4d03a37cf67c0fb1990db30bbeee55a6d6d8ffdafe32eebb88573"),
    (3, "2458b1fbd32c06421494f462195696d6a4ffed2b6bdf4b0a910f377308826cfe"),
}
public_files = [ROOT / "README.md", ROOT / "README.vi.md"] + list((ROOT / "docs").rglob("*.md"))
bad=[]
for src in public_files:
    words=re.findall(r"[a-z0-9]+", src.read_text(encoding="utf-8", errors="replace").lower())
    for n,digest in reserved:
        for i in range(max(0,len(words)-n+1)):
            phrase=" ".join(words[i:i+n])
            if hashlib.sha256(phrase.encode()).hexdigest()==digest:
                bad.append(str(src)); break
record("forbidden_inspiration_names_absent", not bad, str(sorted(set(bad))))

# Commercial inquiry must explicitly reject manuscript attachment and not invent contact data.
commercial = (ROOT / "docs/licensing/COMMERCIAL-LICENSING-INQUIRY.md").read_text(encoding="utf-8").lower()
record("commercial_inquiry_safe", "unpublished manuscripts" in commercial and "not yet open" in commercial)

# CLI surface should match the compatibility matrix.
proc = subprocess.run([sys.executable, "-m", "pse_cli.cli", "--help"], cwd=ROOT, env={**__import__('os').environ, "PYTHONPATH": str(ROOT / "tools")}, text=True, capture_output=True)
expected = ["build", "check", "clean", "smoke", "visual-check", "regression", "doctor", "proof", "release", "verify-release", "profiles", "modules", "semantic-ir", "new"]
matrix = (ROOT / "docs/reference/CLI-COMPATIBILITY-MATRIX.md").read_text(encoding="utf-8")
missing = [cmd for cmd in expected if cmd not in proc.stdout or f"`pse {cmd}`" not in matrix]
record("cli_matrix_matches_help", proc.returncode == 0 and not missing, str(missing))

report = {
    "audit_kind": "beta_candidate",
    "framework_version": public_version,
    "passed": all(x["passed"] for x in checks),
    "checks_passed": sum(x["passed"] for x in checks),
    "checks_total": len(checks),
    "checks": checks,
    "public_beta_authorized": False,
    "blocking_external_gate": "final legally reviewed license and live candidate CI",
}
(OUT / "beta-candidate-audit.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
raise SystemExit(0 if report["passed"] else 1)
