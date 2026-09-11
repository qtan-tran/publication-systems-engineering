from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "release" / "rc_readiness.py"
OUT = ROOT / "tests" / "_output" / "release-evidence" / "rc-readiness.json"
checks=[]
def ck(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

proc=subprocess.run([sys.executable, str(SCRIPT)], cwd=ROOT, text=True, capture_output=True)
ck("report_command_passes_internal_checks", proc.returncode==0, proc.stderr[-500:])
report=json.loads(OUT.read_text(encoding="utf-8"))
ck("surface_is_9_profiles_14_modules", report.get("surface_freeze",{}).get("profiles")==9 and report.get("surface_freeze",{}).get("semantic_modules")==14, report.get("surface_freeze"))
ck("feature_growth_frozen", report.get("surface_freeze",{}).get("new_features_before_gate_clearance") is False)
ck("not_false_public_beta", report.get("public_beta_ready") is False and report.get("decision")=="stabilization_only_not_public_rc", report.get("decision"))
codes={g.get("code") for g in report.get("external_hard_gates",[])}
for code in ["legal_review","operative_license","contributor_rights","commercial_contact","live_exact_candidate_ci","live_documentation_render"]:
    ck(f"external_gate_{code}_visible", code in codes)
ck("license_still_absent", not (ROOT/"LICENSE").exists())
freeze=(ROOT/"docs/beta/BETA-CANDIDATE-FREEZE.md").read_text(encoding="utf-8")
ck("freeze_schema_current", "profile manifest schema 1.1" in freeze and "semantic module activation schema 1.1" in freeze)
ck("review_docs_present", (ROOT/"docs/beta/RC-SURFACE-FREEZE.md").is_file() and (ROOT/"docs/beta/RC-READINESS-REVIEW.md").is_file())
blocked=subprocess.run([sys.executable,str(SCRIPT),"--require-public-beta"],cwd=ROOT,text=True,capture_output=True)
ck("require_public_beta_blocks", blocked.returncode==2, blocked.returncode)
failed=[x for x in checks if not x[1]]
for n,ok,d in checks: print(f"{'PASS' if ok else 'FAIL'} {n}: {d}")
print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
raise SystemExit(1 if failed else 0)
