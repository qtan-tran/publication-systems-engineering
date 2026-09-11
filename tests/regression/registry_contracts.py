from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV = os.environ.copy()
ENV["PYTHONPATH"] = str(ROOT / "tools") + os.pathsep + ENV.get("PYTHONPATH", "")


def run(args, *, cwd=ROOT, env=ENV, expect=0, timeout=240):
    proc = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, timeout=timeout)
    if proc.returncode != expect:
        raise AssertionError(f"{args}\nstdout:\n{proc.stdout[-5000:]}\nstderr:\n{proc.stderr[-5000:]}")
    return proc


def manifests(kind: str, manifest_name: str):
    out = {}
    for path in sorted((ROOT / kind).glob(f"*/{manifest_name}")):
        data = json.loads(path.read_text(encoding="utf-8"))
        out[path.parent.name] = data
    return out


def main():
    checks = []
    profiles = manifests("profiles", "profile.json")
    modules = manifests("modules", "module.json")
    runtime = json.loads((ROOT / "runtime/pse-runtime.json").read_text(encoding="utf-8"))

    checks.append(("registry_counts", len(profiles) == 9 and len(modules) == 14, f"{len(profiles)} profiles / {len(modules)} modules"))
    checks.append(("runtime_profiles_exact", set(runtime["profiles"]) == set(profiles), str(sorted(runtime["profiles"]))))
    checks.append(("runtime_modules_exact", set(runtime["modules"]) == set(modules), str(sorted(runtime["modules"]))))
    checks.append(("runtime_sync_check", run([sys.executable, "scripts/release/sync_registry.py", "--check"]).returncode == 0, "manifest-derived runtime registry"))

    # Profile manifests may reference only registered modules; modules may depend/conflict only with registered modules.
    unknown_profile_modules = {}
    for pid, profile in profiles.items():
        refs = set(profile.get("semantic_modules", [])) | set(profile.get("module_policy", {}))
        missing = sorted(refs - set(modules))
        if missing:
            unknown_profile_modules[pid] = missing
    checks.append(("profile_module_references", not unknown_profile_modules, str(unknown_profile_modules)))

    bad_edges = {}
    for mid, m in modules.items():
        refs = (set(m.get("depends_on", [])) | set(m.get("conflicts_with", []))) - set(modules)
        if refs:
            bad_edges[mid] = sorted(refs)
    checks.append(("module_graph_references", not bad_edges, str(bad_edges)))

    # Presentation packages must not directly import semantic module packages or declare module packages.
    boundary_hits = []
    for pid in profiles:
        text = (ROOT / "profiles" / pid / f"pse-profile-{pid}.sty").read_text(encoding="utf-8", errors="replace")
        if "pse-module-" in text or "\\ProvidesPackage{pse-module-" in text:
            boundary_hits.append(pid)
    checks.append(("presentation_semantic_boundary", not boundary_hits, str(boundary_hits)))

    # Dynamic packaging must ship the exact manifest-discovered profile/module sets, not a hand-maintained subset.
    with tempfile.TemporaryDirectory(prefix="pse-registry-wheel-") as td:
        td = Path(td)
        run([sys.executable, "-m", "pip", "wheel", "--no-build-isolation", "--no-deps", "-w", str(td), str(ROOT)], cwd=td)
        wheel = next(td.glob("publication_systems_engineering-*.whl"))
        with zipfile.ZipFile(wheel) as zf:
            names = set(zf.namelist())
        wheel_profiles = {pid for pid in profiles if any(n.endswith(f"/profiles/{pid}/profile.json") for n in names) and any(n.endswith(f"/profiles/{pid}/pse-profile-{pid}.sty") for n in names)}
        wheel_modules = {mid for mid in modules if any(n.endswith(f"/modules/{mid}/module.json") for n in names) and any(n.endswith(f"/modules/{mid}/pse-module-{mid}.sty") for n in names)}
        checks.append(("wheel_profiles_exact", wheel_profiles == set(profiles), str(sorted(wheel_profiles))))
        checks.append(("wheel_modules_exact", wheel_modules == set(modules), str(sorted(wheel_modules))))
        checks.append(("wheel_runtime_registry", any(n.endswith("/runtime/pse-runtime.json") for n in names), "runtime registry packaged"))

    failed = [x for x in checks if not x[1]]
    print("Registry consolidation regression")
    for name, ok, detail in checks:
        print(("PASS" if ok else "FAIL"), name + ":", detail)
    print(f"summary: {len(checks)-len(failed)}/{len(checks)} pass")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
