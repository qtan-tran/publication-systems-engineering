from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
checks: list[dict[str, object]] = []


def record(name: str, passed: bool, detail: object = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})


# Source checkouts should not carry build/test artefacts that belong outside release source.
forbidden_dirs = {"__pycache__", ".pytest_cache", "build", "dist", "_output"}
forbidden_suffixes = {".aux", ".bcf", ".blg", ".fdb_latexmk", ".fls", ".ilg", ".ind", ".log", ".run.xml", ".synctex.gz", ".xdv"}
artifact_hits: list[str] = []
for path in ROOT.rglob("*"):
    rel = path.relative_to(ROOT)
    if any(part in forbidden_dirs for part in rel.parts):
        artifact_hits.append(str(rel))
        continue
    if path.is_file() and any(path.name.endswith(suffix) for suffix in forbidden_suffixes):
        artifact_hits.append(str(rel))
record("generated_artifacts_absent", not artifact_hits, sorted(set(artifact_hits))[:50])

# Canonical profile demos and frozen synthetic release fixtures are intentional public PDF artefacts.
unexpected_pdfs: list[str] = []
approved_pdf_patterns = (
    r"examples/profiles/[^/]+/output/[^/]+-demo\.pdf",
    r"tests/fixtures/releases/schema-0\.[12]/(?:legacy|current)-release\.pdf",
)
for path in ROOT.rglob("*.pdf"):
    rel = path.relative_to(ROOT).as_posix()
    if not any(re.fullmatch(pattern, rel) for pattern in approved_pdf_patterns):
        unexpected_pdfs.append(rel)
record("only_approved_public_pdfs_committed", not unexpected_pdfs, unexpected_pdfs[:50])

# Symlinks in a distributable source tree must not escape the repository root.
escaping_links: list[str] = []
root_resolved = ROOT.resolve()
for path in ROOT.rglob("*"):
    if path.is_symlink():
        try:
            path.resolve().relative_to(root_resolved)
        except (ValueError, OSError):
            escaping_links.append(str(path.relative_to(ROOT)))
record("symlinks_contained", not escaping_links, escaping_links)

# Local Markdown links must resolve inside the checkout.
missing_links: list[str] = []
link_rx = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
for source in ROOT.rglob("*.md"):
    text = source.read_text(encoding="utf-8", errors="replace")
    for match in link_rx.finditer(text):
        target = match.group(1).strip()
        if not target or target.startswith("#") or "://" in target or target.startswith("mailto:"):
            continue
        target = target.split("#", 1)[0]
        if not (source.parent / target).resolve().exists():
            line = text.count("\n", 0, match.start()) + 1
            missing_links.append(f"{source.relative_to(ROOT)}:{line}:{target}")
record("local_markdown_links_resolve", not missing_links, missing_links[:50])

# Internal development-step labels are not part of the public naming/documentation contract.
# Build the detector without embedding any concrete historical label in the public source.
step_word = "".join(chr(n) for n in (112, 104, 97, 115, 101))
step_rx = re.compile(rf"(?i)(?:\b{step_word}\s+[a-z](?:\b|_)|{step_word}_[a-z])")
step_hits: list[str] = []
text_suffixes = {".py", ".md", ".yml", ".yaml", ".json", ".toml", ".cff", ".sty", ".tex", ".txt"}
for path in ROOT.rglob("*"):
    rel = path.relative_to(ROOT)
    if step_rx.search(str(rel)):
        step_hits.append(str(rel))
    if path.is_file() and path.suffix.lower() in text_suffixes:
        text = path.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            if step_rx.search(line):
                step_hits.append(f"{rel}:{i}")
record("internal_step_labels_absent", not step_hits, step_hits[:50])

# SHA256SUMS is a release-evidence manifest for every public source file except itself.
manifest = ROOT / "SHA256SUMS.txt"
manifest_bad: list[str] = []
listed: set[str] = set()
if manifest.is_file():
    for i, line in enumerate(manifest.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) != 2:
            manifest_bad.append(f"line {i}: malformed")
            continue
        expected, rel_text = parts
        rel_text = rel_text.lstrip("* ")
        listed.add(rel_text)
        path = ROOT / rel_text
        if not path.is_file():
            manifest_bad.append(f"line {i}: missing {rel_text}")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            manifest_bad.append(f"line {i}: checksum mismatch {rel_text}")
    public_files = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path != manifest and not any(part in {".git"} for part in path.relative_to(ROOT).parts)
    }
    for rel in sorted(public_files - listed):
        manifest_bad.append(f"unlisted: {rel}")
    for rel in sorted(listed - public_files):
        manifest_bad.append(f"non-public/missing listing: {rel}")
else:
    manifest_bad.append("SHA256SUMS.txt missing")
record("source_manifest_complete", not manifest_bad, manifest_bad[:50])

payload = {
    "audit_kind": "public_tree_integrity",
    "passed": all(item["passed"] for item in checks),
    "checks": checks,
}
print(json.dumps(payload, ensure_ascii=False, indent=2))
raise SystemExit(0 if payload["passed"] else 1)
