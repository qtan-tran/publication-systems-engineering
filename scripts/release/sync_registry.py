from __future__ import annotations

import argparse
import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime" / "pse-runtime.json"
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def public_version() -> str:
    value = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    return re.sub(r"a(\d+)$", r"-alpha", value)


def discover(kind: str, manifest_name: str, package_prefix: str) -> dict[str, str]:
    base = ROOT / kind
    registry: dict[str, str] = {}
    for manifest in sorted(base.glob(f"*/{manifest_name}")):
        item_id = manifest.parent.name
        if not ID_RE.fullmatch(item_id):
            raise SystemExit(f"Invalid {kind[:-1]} directory id: {item_id}")
        data = json.loads(manifest.read_text(encoding="utf-8"))
        if data.get("id") != item_id:
            raise SystemExit(f"{manifest.relative_to(ROOT)} id does not match directory name")
        package = manifest.parent / f"{package_prefix}{item_id}.sty"
        if not package.is_file():
            raise SystemExit(f"Missing package for {item_id}: {package.relative_to(ROOT)}")
        registry[item_id] = package.relative_to(ROOT).as_posix()
    return registry


def expected() -> dict[str, object]:
    return {
        "schema_version": "0.1",
        "framework": "publication-systems-engineering",
        "runtime_version": public_version(),
        "engine": "LuaLaTeX",
        "core_path": "core/pse-core.sty",
        "profiles": discover("profiles", "profile.json", "pse-profile-"),
        "modules": discover("modules", "module.json", "pse-module-"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronise the checked-in runtime registry from profile and module manifests.")
    parser.add_argument("--check", action="store_true", help="Fail if runtime/pse-runtime.json differs from manifest discovery.")
    args = parser.parse_args()
    wanted = expected()
    current = json.loads(RUNTIME.read_text(encoding="utf-8")) if RUNTIME.is_file() else None
    if args.check:
        if current != wanted:
            print("runtime registry is stale; run: python scripts/release/sync_registry.py")
            return 1
        print(f"registry synchronized: {len(wanted['profiles'])} profiles / {len(wanted['modules'])} modules")
        return 0
    RUNTIME.parent.mkdir(parents=True, exist_ok=True)
    RUNTIME.write_text(json.dumps(wanted, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {RUNTIME.relative_to(ROOT)}: {len(wanted['profiles'])} profiles / {len(wanted['modules'])} modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
