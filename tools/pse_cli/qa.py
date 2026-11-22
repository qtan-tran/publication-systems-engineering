from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageChops

SEVERITIES = ("error", "warning", "review", "info")


@dataclass(frozen=True)
class Finding:
    code: str
    severity: str
    message: str
    count: int | None = None
    data: dict[str, Any] | None = None
    location: dict[str, Any] | None = None
    related_locations: list[dict[str, Any]] | None = None

    def as_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
        }
        if self.count is not None:
            out["count"] = self.count
        if self.data:
            out["data"] = self.data
        if self.location:
            out["location"] = self.location
        if self.related_locations:
            out["related_locations"] = self.related_locations
        return out


def summarize(findings: list[dict[str, Any]]) -> dict[str, int]:
    totals = {key: 0 for key in SEVERITIES}
    for item in findings:
        sev = item.get("severity")
        if sev in totals:
            totals[sev] += 1
    return totals


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def render_pdf_page(pdf: Path, page_number: int, output: Path, dpi: int = 144) -> tuple[bool, str]:
    """Render one one-indexed PDF page with pdftoppm.

    Rendering is a regression/review dependency, not a core build dependency.
    """
    exe = shutil.which("pdftoppm")
    if not exe:
        return False, "pdftoppm not found on PATH"
    output.parent.mkdir(parents=True, exist_ok=True)
    stem = output.with_suffix("")
    cmd = [
        exe, "-png", "-singlefile", "-r", str(dpi),
        "-f", str(page_number), "-l", str(page_number),
        str(pdf), str(stem),
    ]
    proc = subprocess.run(cmd, text=True, capture_output=True)
    generated = stem.with_suffix(".png")
    if proc.returncode != 0 or not generated.exists():
        detail = (proc.stdout + "\n" + proc.stderr).strip()
        return False, detail or "pdftoppm failed"
    if generated != output:
        generated.replace(output)
    return True, str(output)


def compare_images(baseline: Path, current: Path, diff_output: Path | None = None, *, channel_threshold: int = 8) -> dict[str, Any]:
    a = Image.open(baseline).convert("RGB")
    b = Image.open(current).convert("RGB")
    if a.size != b.size:
        return {
            "comparable": False,
            "baseline_size": list(a.size),
            "current_size": list(b.size),
            "pixel_diff_ratio": 1.0,
            "mean_absolute_error": 255.0,
            "hash_match": False,
        }
    hash_match = sha256(baseline) == sha256(current)
    diff = ImageChops.difference(a, b)
    pixels = a.size[0] * a.size[1]
    channels = diff.split()
    # Pillow-native histogram operations keep this comparison lightweight and fast;
    # numpy is intentionally not a runtime dependency.
    masks = [ch.point(lambda value: 255 if value > channel_threshold else 0) for ch in channels]
    material = ImageChops.lighter(ImageChops.lighter(masks[0], masks[1]), masks[2])
    hist = material.histogram()
    changed = pixels - hist[0] if hist else 0
    absolute_sum = 0
    for ch in channels:
        ch_hist = ch.histogram()
        absolute_sum += sum(value * count for value, count in enumerate(ch_hist))
    ratio = changed / pixels if pixels else 0.0
    mae = absolute_sum / (pixels * 3) if pixels else 0.0
    if diff_output is not None:
        diff_output.parent.mkdir(parents=True, exist_ok=True)
        diff.save(diff_output)
    return {
        "comparable": True,
        "baseline_size": list(a.size),
        "current_size": list(b.size),
        "pixel_diff_ratio": round(ratio, 8),
        "mean_absolute_error": round(mae, 6),
        "hash_match": hash_match,
    }


def visual_check(pdf: Path, baseline_dir: Path, manifest_path: Path, output_dir: Path, *, review_threshold: float = 0.005) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    dpi = int(manifest.get("render_dpi", 144))
    pages = manifest.get("pages") or []
    findings: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    if not pages:
        findings.append(Finding("visual_manifest_missing_pages", "error", "Visual baseline manifest does not define page mappings.").as_dict())
        return {"status": "fail", "findings": findings, "results": results}

    for item in pages:
        name = str(item["name"])
        page_number = int(item["page"])
        baseline = baseline_dir / str(item["file"])
        current = output_dir / "current" / f"{name}.png"
        diff = output_dir / "diff" / f"{name}.png"
        if not baseline.exists():
            findings.append(Finding("visual_baseline_missing", "error", f"Missing baseline for {name}: {baseline}").as_dict())
            continue
        ok, detail = render_pdf_page(pdf, page_number, current, dpi=dpi)
        if not ok:
            findings.append(Finding("visual_render_failed", "error", f"Could not render page {page_number} ({name}): {detail}").as_dict())
            continue
        metrics = compare_images(baseline, current, diff)
        entry = {"name": name, "page": page_number, "baseline": str(baseline), "current": str(current), "diff": str(diff), **metrics}
        results.append(entry)
        if not metrics["comparable"]:
            findings.append(Finding("visual_geometry_drift", "review", f"Rendered image geometry changed for {name}.", data=metrics).as_dict())
        elif float(metrics["pixel_diff_ratio"]) > review_threshold:
            findings.append(Finding("visual_drift", "review", f"Visual baseline drift exceeds review threshold for {name}.", data={"pixel_diff_ratio": metrics["pixel_diff_ratio"], "threshold": review_threshold}).as_dict())
        else:
            findings.append(Finding("visual_baseline_ok", "info", f"Visual baseline within tolerance for {name}.", data={"pixel_diff_ratio": metrics["pixel_diff_ratio"], "hash_match": metrics["hash_match"]}).as_dict())

    totals = summarize(findings)
    return {
        "schema_version": "0.1",
        "status": "fail" if totals["error"] else ("review" if totals["review"] else "pass"),
        "render_dpi": dpi,
        "review_threshold": review_threshold,
        "findings": findings,
        "summary": totals,
        "results": results,
    }
