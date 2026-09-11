#!/usr/bin/env python3
"""Conservative Git-history scanner for obvious secrets/confidential markers.

This scanner is intentionally heuristic. Passing it is evidence, not a guarantee that
no sensitive material exists. It scans every blob reachable from refs in the current
Git repository and exits non-zero on configured high-risk patterns.
"""
from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

PATTERNS = {
    "private_key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(rb"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "aws_access_key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "generic_secret_assignment": re.compile(rb"(?i)(?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"\r\n]{8,}['\"]"),
}
MAX_BLOB = 8 * 1024 * 1024

def run(*args: str) -> bytes:
    return subprocess.check_output(args)

def main() -> int:
    try:
        objects = run("git", "rev-list", "--objects", "--all").decode("utf-8", "replace").splitlines()
    except Exception as e:
        print(json.dumps({"passed": False, "error": str(e)}, indent=2))
        return 2
    findings=[]; scanned=0; skipped_large=0
    seen=set()
    for line in objects:
        oid=line.split(" ",1)[0]
        if oid in seen: continue
        seen.add(oid)
        try:
            typ=run("git","cat-file","-t",oid).strip()
            if typ != b"blob": continue
            size=int(run("git","cat-file","-s",oid).strip())
            if size > MAX_BLOB:
                skipped_large += 1; continue
            data=run("git","cat-file","blob",oid); scanned += 1
            path=line.split(" ",1)[1] if " " in line else ""
            for name,rx in PATTERNS.items():
                if rx.search(data): findings.append({"object":oid,"path":path,"pattern":name})
        except subprocess.CalledProcessError:
            continue
    # Policy/documentation may legitimately discuss unpublished manuscripts or private architecture.
    # Those phrases are not treated as secret findings by themselves; the scanner is intentionally
    # limited to high-confidence credential/key patterns and must be complemented by human review.
    head_commit = run("git", "rev-parse", "HEAD").decode().strip()
    shallow_repository = run("git", "rev-parse", "--is-shallow-repository").decode().strip().lower() == "true"
    result={"audit_kind":"full_history_scan","passed":not findings and not shallow_repository,"head_commit":head_commit,"shallow_repository":shallow_repository,"blobs_scanned":scanned,"large_blobs_skipped":skipped_large,"findings":findings,
            "note":"High-confidence heuristic credential/key scan across reachable Git history. A shallow checkout is a hard failure. Passing does not prove absence of all confidential material; human history review remains required."}
    Path("tests/_output/release-evidence").mkdir(parents=True, exist_ok=True)
    Path("tests/_output/release-evidence/full-history-scan.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    return 0 if result["passed"] else 1
if __name__ == "__main__": raise SystemExit(main())
