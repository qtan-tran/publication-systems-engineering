from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
checks: list[dict[str, object]] = []

def record(name: str, passed: bool, detail: object = "") -> None:
    checks.append({"name": name, "passed": bool(passed), "detail": detail})

asset = ROOT / "core" / "pse-attribution-banner.png"
record("canonical_asset_present", asset.is_file() and asset.stat().st_size > 0, str(asset.relative_to(ROOT)) if asset.exists() else "missing")
if asset.is_file():
    record("canonical_asset_sha256", hashlib.sha256(asset.read_bytes()).hexdigest() == "5c579be8fc09e8b28a76e48a678712e8bce7f79ee447508e2b5e577d3e9996a0", hashlib.sha256(asset.read_bytes()).hexdigest())

core = (ROOT / "core" / "pse-core.sty").read_text(encoding="utf-8")
record("banner_macro_defined", "\\newcommand{\\PSEAttributionBanner}" in core and "pse-attribution-banner.png" in core, "core/pse-core.sty")
record("default_publication_page_places_banner", "\\PSEAttributionBanner" in core.split("\\newcommand{\\PSEPublicationPage}", 1)[1], "default publication page")

basic = (ROOT / "profiles" / "basic-book" / "pse-profile-basic-book.sty").read_text(encoding="utf-8")
record("basic_profile_override_places_banner", "\\PSEAttributionBanner" in basic.split("\\renewcommand{\\PSEPublicationPage}", 1)[1], "basic-book publication page")

setup_text = (ROOT / "setup.py").read_text(encoding="utf-8")
record("wheel_packages_banner", 'core = ROOT / "core"' in setup_text and 'if p.is_file()' in setup_text, "manifest-driven setup.py core packaging")

cli = (ROOT / "tools" / "pse_cli" / "cli.py").read_text(encoding="utf-8")
record("release_gate_records_render_evidence", "mandatory PSE attribution banner did not render" in cli and '"attribution": attribution' in cli, "release gate + manifest")

brand = (ROOT / "docs" / "design" / "BRAND-AND-ATTRIBUTION.md").read_text(encoding="utf-8")
record("public_contract_documented", "Every ebook released through the PSE publication-release pipeline" in brand and "copyright/publication page" in brand and "colophon" in brand, "brand contract")

payload = {"audit_kind": "attribution_contract", "passed": all(c["passed"] for c in checks), "checks": checks}
print(json.dumps(payload, indent=2))
raise SystemExit(0 if payload["passed"] else 1)
