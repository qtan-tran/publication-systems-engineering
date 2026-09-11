from __future__ import annotations

from pathlib import Path
from setuptools import setup

ROOT = Path(__file__).resolve().parent
SHARE = Path("share/publication-systems-engineering")

def _files(directory: Path, names: list[str]):
    return [str(directory / name) for name in names]

def runtime_data_files():
    data = []
    core = ROOT / "core"
    data.append((str(SHARE / "core"), [str(p.relative_to(ROOT)) for p in sorted(core.iterdir()) if p.is_file()]))
    for manifest in sorted((ROOT / "profiles").glob("*/profile.json")):
        pid = manifest.parent.name
        package = manifest.parent / f"pse-profile-{pid}.sty"
        presentation = manifest.parent / "presentation.json"
        if not package.is_file():
            raise RuntimeError(f"Profile {pid} is missing {package.name}")
        if not presentation.is_file():
            raise RuntimeError(f"Profile {pid} is missing {presentation.name}")
        data.append((str(SHARE / "profiles" / pid), [str(manifest.relative_to(ROOT)), str(package.relative_to(ROOT)), str(presentation.relative_to(ROOT))]))
    for manifest in sorted((ROOT / "modules").glob("*/module.json")):
        mid = manifest.parent.name
        package = manifest.parent / f"pse-module-{mid}.sty"
        if not package.is_file():
            raise RuntimeError(f"Semantic module {mid} is missing {package.name}")
        data.append((str(SHARE / "modules" / mid), [str(manifest.relative_to(ROOT)), str(package.relative_to(ROOT))]))
    schema_files = [str(p.relative_to(ROOT)) for p in sorted((ROOT / "schema").iterdir()) if p.is_file() and p.name != ".gitkeep"]
    data.append((str(SHARE / "schema"), schema_files))
    data.append((str(SHARE / "runtime"), ["runtime/pse-runtime.json"]))
    return data

setup(data_files=runtime_data_files())
