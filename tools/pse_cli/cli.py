from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import sysconfig
import platform
import tempfile
import hashlib
import secrets
from datetime import datetime, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from importlib import metadata as importlib_metadata

import yaml
from pypdf import PdfReader

from .qa import Finding, summarize as _qa_summarize, visual_check as _visual_check
from .semantic_parser import parse_files, loc_dict
from .output_inspection import inspect_pdf, render_human
from .release_contract import (
    RELEASE_MANIFEST_SCHEMA_VERSION,
    RELEASE_INSPECTION_POLICY,
    SUPPORTED_RELEASE_MANIFEST_SCHEMAS,
    sha256_file,
    validate_release_manifest,
    validate_output_inspection,
    validate_release_binding,
    write_checksum_file,
    verify_checksum_file,
    installed_contract_surface,
    release_schema_compatibility,
    release_migration_assessment,
    release_audit_record,
    validate_release_audit_record,
    release_audit_index,
    validate_release_audit_index,
    verify_release_audit_record_payload,
    verify_release_audit_index_payload,
    write_deterministic_audit_bundle,
    validate_audit_evidence_bundle_manifest,
)

VERSION = "1.47.0-alpha"
REQUIRED_METADATA = ("title", "author", "language", "publication_year")



PROFILE_SCHEMA_VERSION = "1.1"
SUPPORTED_PROFILE_SCHEMA_VERSIONS = {"1.0", "1.1"}
MODULE_POLICY_STATUSES = {"required", "recommended", "optional", "discouraged", "incompatible"}

PRESENTATION_SCHEMA_VERSION = "1.0"
PRESENTATION_PRESETS = {"book-reading", "scholarly-monograph", "parallel-edition", "source-critical", "dramatic-reading", "scholarly-collection", "fiction-reading", "verse-reading", "scholarly-edition"}
PRESENTATION_ENUMS = {
    "hierarchy": {"structured", "compact", "dramatic", "verse", "narrative"},
    "publication_unit_metadata": {"chapter-opener", "available", "deferred"},
    "grid": {"book", "asymmetric-scholarly"},
    "side_material": {"outer-margin", "fallback"},
    "apparatus": {"multi-stream", "available", "deferred"},
    "locator": {"primary-visible", "source-defined", "none"},
    "parallel_text": {"profile-controlled", "none"},
}


def _profile_manifest_path(runtime_root: Path, profile: str) -> Path:
    return runtime_root / "profiles" / profile / "profile.json"


def _validate_profile_manifest(data: dict[str, Any], *, expected_id: str | None = None) -> dict[str, Any]:
    required = {"schema_version", "id", "version", "extends", "generator_supported", "capabilities", "required_metadata", "open_font_policy", "description"}
    missing = sorted(required - set(data))
    if missing:
        raise SystemExit("Invalid profile manifest; missing fields: " + ", ".join(missing))
    if data.get("schema_version") not in SUPPORTED_PROFILE_SCHEMA_VERSIONS:
        raise SystemExit(f"Unsupported profile manifest schema: {data.get('schema_version')!r}")
    pid = data.get("id")
    if not isinstance(pid, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", pid):
        raise SystemExit("Invalid profile id in profile.json.")
    if expected_id and pid != expected_id:
        raise SystemExit(f"Profile manifest id mismatch: expected {expected_id}, found {pid}")
    if data.get("extends") != "pse-core":
        raise SystemExit(f"Profile {pid} must extend pse-core.")
    if not isinstance(data.get("generator_supported"), bool) or data.get("open_font_policy") is not True:
        raise SystemExit(f"Profile {pid} has invalid generator/open-font policy fields.")
    for field in ("capabilities", "required_metadata"):
        vals=data.get(field)
        if not isinstance(vals, list) or not vals or not all(isinstance(x,str) and x for x in vals) or len(vals)!=len(set(vals)):
            raise SystemExit(f"Profile {pid} field {field} must be a non-empty unique string array.")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        raise SystemExit(f"Profile {pid} requires a non-empty description.")
    if data.get("schema_version") == "1.1":
        policy = data.get("module_policy")
        if not isinstance(policy, dict):
            raise SystemExit(f"Profile {pid} schema 1.1 requires module_policy.")
        for mid, rule in policy.items():
            if not isinstance(mid, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", mid):
                raise SystemExit(f"Profile {pid} has invalid module_policy id: {mid!r}")
            if not isinstance(rule, dict) or set(rule) != {"status", "default_enabled"}:
                raise SystemExit(f"Profile {pid} module policy for {mid} must contain status and default_enabled only.")
            status = rule.get("status")
            default_enabled = rule.get("default_enabled")
            if status not in MODULE_POLICY_STATUSES or not isinstance(default_enabled, bool):
                raise SystemExit(f"Profile {pid} has invalid module policy for {mid}.")
            if status in {"incompatible", "discouraged"} and default_enabled:
                raise SystemExit(f"Profile {pid} cannot default-enable a {status} module: {mid}.")
            if status == "required" and not default_enabled:
                raise SystemExit(f"Profile {pid} required module must be default-enabled: {mid}.")
    return data


def _load_profile_manifest(runtime_root: Path, profile: str) -> dict[str, Any]:
    path = _profile_manifest_path(runtime_root, profile)
    if not path.is_file():
        raise SystemExit(f"Installed runtime is missing profile manifest: {profile}")
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in profile manifest {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Profile manifest must be a JSON object: {path}")
    return _validate_profile_manifest(data, expected_id=profile)


def _presentation_manifest_path(runtime_root: Path, profile: str) -> Path:
    return runtime_root / "profiles" / profile / "presentation.json"


def _load_presentation_manifest(runtime_root: Path, profile: str) -> dict[str, Any]:
    path = _presentation_manifest_path(runtime_root, profile)
    if not path.is_file():
        raise SystemExit(f"Profile {profile} is missing integrated presentation descriptor: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in presentation descriptor {path}: {exc}") from exc
    required = {"schema_version", "profile", "preset", "hierarchy", "publication_unit_metadata", "grid", "side_material", "apparatus", "locator", "parallel_text", "description"}
    if not isinstance(data, dict) or set(data) != required:
        raise SystemExit(f"Presentation descriptor for {profile} must contain exactly: " + ", ".join(sorted(required)))
    if data.get("schema_version") != PRESENTATION_SCHEMA_VERSION or data.get("profile") != profile:
        raise SystemExit(f"Presentation descriptor identity/schema mismatch for {profile}.")
    if data.get("preset") not in PRESENTATION_PRESETS:
        raise SystemExit(f"Unknown presentation preset for {profile}: {data.get('preset')!r}")
    for field, allowed in PRESENTATION_ENUMS.items():
        if data.get(field) not in allowed:
            raise SystemExit(f"Invalid presentation {field} for {profile}: {data.get(field)!r}")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        raise SystemExit(f"Presentation descriptor for {profile} requires a description.")
    return data


def _presentation_system_qa(project: Project) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    metadata = _load_metadata(project.metadata_path)
    profile = str(metadata.get("profile", "basic-book"))
    manifest = _load_profile_manifest(project.repo_root, profile)
    presentation = _load_presentation_manifest(project.repo_root, profile)
    active = {m["id"] for m in _project_modules(project, manifest)}
    findings: list[dict[str, Any]] = []
    if presentation["apparatus"] == "multi-stream" and "apparatus" not in active:
        findings.append(Finding("presentation_missing_apparatus", "error", "Integrated presentation requires the apparatus module, but it is not active.").as_dict())
    if presentation["parallel_text"] == "profile-controlled" and "parallel-text" not in active:
        findings.append(Finding("presentation_missing_parallel_text", "error", "Integrated presentation requires the parallel-text module, but it is not active.").as_dict())
    if presentation["publication_unit_metadata"] == "chapter-opener" and "publication-unit-metadata" not in active:
        findings.append(Finding("presentation_missing_publication_unit_metadata", "error", "Integrated chapter-opener presentation requires publication-unit-metadata, but it is not active.").as_dict())
    if presentation["locator"] != "none":
        loc = _load_locator_orchestration(project)
        if not loc or loc.get("primary_namespace") in {None, "", "none"}:
            findings.append(Finding("presentation_missing_locator_policy", "error", "Integrated presentation expects a primary locator policy, but locator orchestration is not configured.").as_dict())
    metrics = {k: presentation[k] for k in ("schema_version", "profile", "preset", "hierarchy", "publication_unit_metadata", "grid", "side_material", "apparatus", "locator", "parallel_text")}
    metrics["active_semantic_modules"] = sorted(active)
    return findings, metrics


def _available_profiles(runtime_root: Path, *, generator_only: bool = False) -> list[dict[str, Any]]:
    root=runtime_root / "profiles"
    out=[]
    if not root.is_dir():
        return out
    for child in sorted(root.iterdir()):
        if not child.is_dir() or not (child / "profile.json").is_file():
            continue
        data=_load_profile_manifest(runtime_root, child.name)
        if generator_only and not data.get("generator_supported"):
            continue
        sty=child / f"pse-profile-{child.name}.sty"
        if not sty.is_file():
            raise SystemExit(f"Profile {child.name} is missing its package: {sty}")
        out.append(data)
    return out


def _validate_profile_metadata(data: dict[str, Any], manifest: dict[str, Any]) -> None:
    missing=[k for k in manifest.get("required_metadata", []) if not data.get(k)]
    if missing:
        raise SystemExit(f"Profile {manifest['id']} requires metadata: " + ", ".join(missing))

def _module_manifest_path(runtime_root: Path, module: str) -> Path:
    return runtime_root / "modules" / module / "module.json"


def _validate_module_manifest(data: dict[str, Any], *, expected_id: str | None = None) -> dict[str, Any]:
    required={"schema_version","api_version","id","namespace","version","extends","capabilities","requires_capabilities","build_tools","required_fonts","depends_on","conflicts_with","compatible_profiles","qa_hooks","description"}
    missing=sorted(required-set(data))
    if missing:
        raise SystemExit("Invalid semantic module manifest; missing fields: " + ", ".join(missing))
    if data.get("schema_version") != "1.1" or data.get("api_version") != "1":
        raise SystemExit(f"Unsupported semantic module manifest/API schema: {data.get('schema_version')!r}/{data.get('api_version')!r}")
    mid=data.get("id")
    if expected_id and mid != expected_id:
        raise SystemExit(f"Semantic module id mismatch: expected {expected_id!r}, got {mid!r}")
    if data.get("extends") != "pse-core":
        raise SystemExit(f"Semantic module {mid} must extend pse-core.")
    if not isinstance(data.get("namespace"),str) or not re.fullmatch(r"[a-z][a-z0-9.-]*",data["namespace"]):
        raise SystemExit(f"Semantic module {mid} has invalid namespace.")
    for field in ("capabilities","requires_capabilities","depends_on","conflicts_with","compatible_profiles","qa_hooks"):
        vals=data.get(field)
        if not isinstance(vals,list) or len(vals)!=len(set(vals)) or not all(isinstance(x,str) and x for x in vals):
            raise SystemExit(f"Semantic module {mid} has invalid {field}.")
    if not data["capabilities"] or not data["compatible_profiles"]:
        raise SystemExit(f"Semantic module {mid} must declare capabilities and profile compatibility.")
    if mid in data["depends_on"] or mid in data["conflicts_with"]:
        raise SystemExit(f"Semantic module {mid} cannot depend on or conflict with itself.")
    for tool in data.get("build_tools", []):
        if tool not in {"biber","makeindex"}:
            raise SystemExit(f"Unsupported semantic-module build tool: {tool}")
    for hook in data.get("qa_hooks",[]):
        if hook not in {"locator-contract","drama-contract","parallel-text-contract"}:
            raise SystemExit(f"Unsupported semantic-module QA hook: {hook}")
    return data


def _load_module_manifest(runtime_root: Path, module: str) -> dict[str, Any]:
    path=_module_manifest_path(runtime_root,module)
    if not path.is_file():
        raise SystemExit(f"Installed runtime is missing semantic module manifest: {module}")
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in semantic module manifest {path}: {exc}") from exc
    if not isinstance(data,dict):
        raise SystemExit(f"Semantic module manifest must be a JSON object: {path}")
    sty=runtime_root / "modules" / module / f"pse-module-{module}.sty"
    if not sty.is_file():
        raise SystemExit(f"Semantic module {module} is missing its package: {sty}")
    return _validate_module_manifest(data, expected_id=module)


def _all_module_manifests(runtime_root: Path) -> list[dict[str, Any]]:
    root=runtime_root/"modules"
    return [_load_module_manifest(runtime_root,d.name) for d in sorted(root.iterdir()) if d.is_dir() and (d/"module.json").is_file()] if root.is_dir() else []


def _resolve_module_ids(runtime_root: Path, profile_manifest: dict[str, Any], declared: list[str]) -> list[dict[str, Any]]:
    ids=[]
    for mid in declared:
        if mid not in ids: ids.append(mid)
    allmods={m["id"]:m for m in _all_module_manifests(runtime_root)}
    profile=profile_manifest["id"]
    changed=True
    while changed:
        changed=False
        for mid in list(ids):
            if mid not in allmods: raise SystemExit(f"Unknown semantic module: {mid}")
            m=allmods[mid]
            compat=m["compatible_profiles"]
            if "*" not in compat and profile not in compat:
                raise SystemExit(f"Semantic module {mid} is not compatible with profile {profile}.")
            for dep in m["depends_on"]:
                if dep not in ids: ids.append(dep); changed=True
            active_caps={cap for aid in ids if aid in allmods for cap in allmods[aid]["capabilities"]}
            for cap in m["requires_capabilities"]:
                if cap in active_caps: continue
                providers=[x["id"] for x in allmods.values() if cap in x["capabilities"] and ("*" in x["compatible_profiles"] or profile in x["compatible_profiles"])]
                if len(providers)!=1:
                    raise SystemExit(f"Capability {cap!r} required by {mid} has {len(providers)} compatible providers; activation must be unambiguous.")
                if providers[0] not in ids: ids.append(providers[0]); changed=True
    active=[allmods[mid] for mid in ids]
    active_set=set(ids)
    for m in active:
        conflicts=sorted(active_set & set(m["conflicts_with"]))
        if conflicts: raise SystemExit(f"Semantic module {m['id']} conflicts with active module(s): " + ", ".join(conflicts))
    # capability ownership must be unambiguous for active modules
    owners={}
    for m in active:
        for cap in m["capabilities"]: owners.setdefault(cap,[]).append(m["id"])
    ambiguous={c:v for c,v in owners.items() if len(v)>1}
    if ambiguous: raise SystemExit("Ambiguous active semantic capability providers: " + "; ".join(f"{c}={','.join(v)}" for c,v in sorted(ambiguous.items())))
    return active


def _module_policy(profile_manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if profile_manifest.get("schema_version") == "1.1":
        return dict(profile_manifest.get("module_policy", {}))
    return {
        mid: {"status": "required", "default_enabled": True}
        for mid in profile_manifest.get("semantic_modules", [])
    }


def _profile_default_module_ids(profile_manifest: dict[str, Any]) -> list[str]:
    return [mid for mid, rule in _module_policy(profile_manifest).items() if rule.get("default_enabled") is True]


def _profile_required_module_ids(profile_manifest: dict[str, Any]) -> list[str]:
    return [mid for mid, rule in _module_policy(profile_manifest).items() if rule.get("status") == "required"]


def _load_semantic_config(project: "Project") -> dict[str, Any]:
    path=project.root/"config"/"semantic-modules.json"
    if not path.is_file(): return {"schema_version":"1.1","activate":[],"deactivate":[],"config":{}}
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc: raise SystemExit(f"Invalid semantic module config {path}: {exc}") from exc
    if not isinstance(data,dict) or data.get("schema_version") not in {"1.0","1.1"} or not isinstance(data.get("activate"),list) or not isinstance(data.get("config"),dict):
        raise SystemExit("Invalid config/semantic-modules.json contract.")
    deactivate = data.get("deactivate", []) if data.get("schema_version") == "1.1" else []
    if not isinstance(deactivate, list):
        raise SystemExit("semantic-modules deactivate must be an array.")
    for field, vals in (("activate", data["activate"]), ("deactivate", deactivate)):
        if len(vals)!=len(set(vals)) or not all(isinstance(x,str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",x) for x in vals):
            raise SystemExit(f"semantic-modules {field} must be a unique module-id array.")
    overlap=set(data["activate"]) & set(deactivate)
    if overlap:
        raise SystemExit("semantic module cannot be both activated and deactivated: " + ", ".join(sorted(overlap)))
    unknown_cfg=set(data["config"])-set(data["activate"])
    if unknown_cfg: raise SystemExit("semantic module config exists for inactive title module(s): " + ", ".join(sorted(unknown_cfg)))
    return {"schema_version":data.get("schema_version"),"activate":list(data["activate"]),"deactivate":list(deactivate),"config":dict(data["config"])}


def _profile_modules(runtime_root: Path, profile_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return _resolve_module_ids(runtime_root, profile_manifest, _profile_default_module_ids(profile_manifest))


def _project_modules(project: "Project", profile_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    cfg=_load_semantic_config(project)
    required=set(_profile_required_module_ids(profile_manifest))
    forbidden=required & set(cfg["deactivate"])
    if forbidden:
        raise SystemExit("Required profile module(s) cannot be deactivated: " + ", ".join(sorted(forbidden)))
    policy=_module_policy(profile_manifest)
    incompatible={mid for mid, rule in policy.items() if rule.get("status") == "incompatible"}
    bad_activation=incompatible & set(cfg["activate"])
    if bad_activation:
        raise SystemExit("Profile-incompatible semantic module(s) cannot be activated: " + ", ".join(sorted(bad_activation)))
    declared=[mid for mid in _profile_default_module_ids(profile_manifest) if mid not in set(cfg["deactivate"])] + list(cfg["activate"])
    return _resolve_module_ids(project.repo_root, profile_manifest, declared)


def _profile_build_tools(runtime_root: Path, profile_manifest: dict[str, Any]) -> list[str]:
    tools=[]
    for module in _profile_modules(runtime_root,profile_manifest):
        for tool in module.get("build_tools",[]):
            if tool not in tools: tools.append(tool)
    return tools


def _project_build_tools(project: "Project", profile_manifest: dict[str, Any]) -> list[str]:
    tools=[]
    for module in _project_modules(project,profile_manifest):
        for tool in module.get("build_tools",[]):
            if tool not in tools: tools.append(tool)
    return tools


@dataclass(frozen=True)
class RuntimeInfo:
    root: Path
    source: str


@dataclass
class Project:
    root: Path
    repo_root: Path
    runtime_source: str
    metadata_path: Path
    main_tex: Path
    build_dir: Path
    output_pdf: Path


def _is_runtime_root(candidate: Path, *, require_marker: bool = True) -> bool:
    core_ok = (candidate / "core" / "pse-core.sty").is_file()
    if not core_ok:
        return False
    if not require_marker:
        return True
    return (candidate / "runtime" / "pse-runtime.json").is_file() or (candidate / "pyproject.toml").is_file()


def _installed_runtime_candidates() -> list[Path]:
    candidates = [Path(sysconfig.get_path("data")).resolve() / "share" / "publication-systems-engineering"]
    # `pip --target` and some application bundlers colocate `share/` with site packages.
    package_target = Path(__file__).resolve().parents[1] / "share" / "publication-systems-engineering"
    if package_target not in candidates:
        candidates.append(package_target)
    return candidates


def _find_runtime(start: Path) -> RuntimeInfo:
    env = os.environ.get("PSE_ROOT")
    if env:
        candidate = Path(env).expanduser().resolve()
        if _is_runtime_root(candidate, require_marker=False):
            return RuntimeInfo(candidate, "environment")
        raise SystemExit(f"PSE_ROOT is set but does not contain a valid PSE runtime: {candidate}")

    here = start.resolve()
    for candidate in (here, *here.parents):
        if _is_runtime_root(candidate):
            return RuntimeInfo(candidate, "source-checkout")

    source_candidate = Path(__file__).resolve().parents[2]
    if _is_runtime_root(source_candidate):
        return RuntimeInfo(source_candidate, "source-checkout")

    for installed in _installed_runtime_candidates():
        if _is_runtime_root(installed):
            return RuntimeInfo(installed, "installed-share")

    raise SystemExit(
        "PSE runtime not found. Run `pse doctor` for diagnostics, reinstall PSE, "
        "or set PSE_ROOT only as an explicit development/operations override."
    )


def _find_repo_root(start: Path) -> Path:
    """Compatibility helper retained for legacy compatibility tests and internal callers."""
    return _find_runtime(start).root


def _load_project(project_dir: str | Path) -> Project:
    root = Path(project_dir).resolve()
    if not root.is_dir():
        raise SystemExit(f"Project directory does not exist: {root}")
    runtime = _find_runtime(root)
    repo_root = runtime.root
    metadata = root / "book.yml"
    main_tex = root / "main.tex"
    if not metadata.exists():
        raise SystemExit(f"Missing required metadata file: {metadata}")
    if not main_tex.exists():
        raise SystemExit(f"Missing required source file: {main_tex}")
    build_dir = root / "build"
    output_pdf = build_dir / "book.pdf"
    return Project(root, repo_root, runtime.source, metadata, main_tex, build_dir, output_pdf)


def _load_metadata(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SystemExit(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("book.yml must contain a YAML mapping at the top level.")
    missing = [key for key in REQUIRED_METADATA if not data.get(key)]
    if missing:
        raise SystemExit("Missing required metadata: " + ", ".join(missing))
    year = data.get("publication_year")
    if not isinstance(year, int) or not (1000 <= year <= 9999):
        raise SystemExit("publication_year must be a four-digit integer.")
    page = data.get("page", {})
    if page and not isinstance(page, dict):
        raise SystemExit("page must be a mapping when present.")
    for key, default in (("width_mm", 126), ("height_mm", 198)):
        value = page.get(key, default) if isinstance(page, dict) else default
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise SystemExit(f"page.{key} must be numeric.")
        if not (50 <= float(value) <= 500):
            raise SystemExit(f"page.{key} is outside the supported safety range (50–500 mm).")
    for key, value in data.items():
        if isinstance(value, str) and any(ord(ch) < 32 and ch not in "\n\t" for ch in value):
            raise SystemExit(f"Metadata field {key!r} contains unsupported control characters.")
    return data



LOCATOR_SCHEME_SCHEMA_VERSION = "1.0"


def _load_locator_scheme(project: Project) -> dict[str, Any] | None:
    path = project.root / "config" / "locator-scheme.json"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid locator scheme JSON {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("locator-scheme.json must contain a JSON object.")
    required = {"schema_version", "id", "order", "require_complete", "strict_order"}
    missing = sorted(required - set(data))
    if missing:
        raise SystemExit("Invalid locator scheme; missing fields: " + ", ".join(missing))
    if data.get("schema_version") != LOCATOR_SCHEME_SCHEMA_VERSION:
        raise SystemExit(f"Unsupported locator-scheme schema: {data.get('schema_version')!r}")
    order = data.get("order")
    if not isinstance(order, list) or not order or not all(isinstance(x, str) and x.strip() for x in order):
        raise SystemExit("locator-scheme order must be a non-empty array of strings.")
    if len(order) != len(set(order)):
        raise SystemExit("locator-scheme order contains duplicate canonical identifiers.")
    for key in ("require_complete", "strict_order"):
        if not isinstance(data.get(key), bool):
            raise SystemExit(f"locator-scheme {key} must be boolean.")
    return data


def _project_tex_sources(project: Project) -> list[Path]:
    roots = [project.main_tex, *(project.root / "content").rglob("*.tex")]
    out=[]
    seen=set()
    for path in roots:
        path=Path(path)
        if path.is_file() and path.resolve() not in seen:
            seen.add(path.resolve()); out.append(path)
    return sorted(out, key=lambda x: str(x))


def _load_locator_schemes(project: Project) -> dict[str, Any]:
    modern=project.root/"config"/"locator-schemes.json"
    if modern.is_file():
        try: data=json.loads(modern.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc: raise SystemExit(f"Invalid locator-schemes JSON {modern}: {exc}") from exc
        if not isinstance(data,dict) or data.get("schema_version")!="1.0" or not isinstance(data.get("schemes"),dict) or not data["schemes"]:
            raise SystemExit("Invalid config/locator-schemes.json contract.")
        for ns,scheme in data["schemes"].items():
            if not re.fullmatch(r"[a-z][a-z0-9.-]*",ns): raise SystemExit(f"Invalid locator namespace: {ns}")
            if not isinstance(scheme,dict) or not isinstance(scheme.get("order"),list) or not scheme["order"]:
                raise SystemExit(f"Invalid locator scheme for namespace {ns}.")
            if len(scheme["order"])!=len(set(scheme["order"])): raise SystemExit(f"Locator scheme {ns} contains duplicates.")
            for key in ("require_complete","strict_order"):
                if not isinstance(scheme.get(key),bool): raise SystemExit(f"Locator scheme {ns}.{key} must be boolean.")
        return data
    legacy=_load_locator_scheme(project)
    return {"schema_version":"1.0","schemes":{"canonical":legacy}} if legacy else {"schema_version":"1.0","schemes":{}}



LOCATOR_ORCHESTRATION_SCHEMA_VERSION = "1.0"
LOCATOR_ORCHESTRATION_NAMESPACES = {
    "canonical": "canonical-locators",
    "dramatic-line": "dramatic-locators",
    "verse-line": "verse-structure",
    "parallel-alignment": "parallel-text",
}


def _load_locator_orchestration(project: Project) -> dict[str, Any] | None:
    path=project.root/"config"/"locator-orchestration.json"
    if not path.is_file():
        return None
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid locator orchestration JSON {path}: {exc}") from exc
    required={"schema_version","primary_namespace","secondary_namespaces","visible_numbering","stable_id_policy"}
    if not isinstance(data,dict) or required-set(data):
        raise SystemExit("Invalid config/locator-orchestration.json contract.")
    if data.get("schema_version")!=LOCATOR_ORCHESTRATION_SCHEMA_VERSION:
        raise SystemExit(f"Unsupported locator-orchestration schema: {data.get('schema_version')!r}")
    primary=data.get("primary_namespace")
    if primary not in LOCATOR_ORCHESTRATION_NAMESPACES:
        raise SystemExit("locator-orchestration primary_namespace is unsupported.")
    secondary=data.get("secondary_namespaces")
    if not isinstance(secondary,list) or not all(isinstance(x,str) and x in LOCATOR_ORCHESTRATION_NAMESPACES for x in secondary):
        raise SystemExit("locator-orchestration secondary_namespaces must contain supported namespaces.")
    if len(secondary)!=len(set(secondary)) or primary in secondary:
        raise SystemExit("locator-orchestration namespaces must be unique and primary may not also be secondary.")
    if data.get("visible_numbering") not in {"show","hide","source-defined","profile-default"}:
        raise SystemExit("locator-orchestration visible_numbering is unsupported.")
    if data.get("stable_id_policy")!="required":
        raise SystemExit("locator-orchestration stable_id_policy currently must be required.")
    return data


def _write_generated_locator_orchestration(project: Project) -> Path | None:
    cfg=_load_locator_orchestration(project)
    generated=project.build_dir/"pse-locator-orchestration.tex"
    if cfg is None:
        if generated.exists(): generated.unlink()
        return None
    generated.parent.mkdir(parents=True,exist_ok=True)
    secondary=",".join(cfg["secondary_namespaces"])
    generated.write_text(
        "% Generated by PSE locator orchestration. Do not edit by hand.\n"
        + rf"\PSEConfigureLocatorOrchestration{{{_tex_escape(cfg['primary_namespace'])}}}{{{_tex_escape(secondary)}}}{{{_tex_escape(cfg['visible_numbering'])}}}{{required}}" + "\n",
        encoding="utf-8",
    )
    return generated


def _locator_orchestration_qa(project: Project) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg=_load_locator_orchestration(project)
    if cfg is None:
        return [],{}
    metadata=_load_metadata(project.metadata_path)
    profile=_load_profile_manifest(project.repo_root,str(metadata.get("profile","basic-book")))
    active=_project_modules(project,profile)
    active_ids={m["id"] for m in active}
    findings=[]
    configured=[cfg["primary_namespace"],*cfg["secondary_namespaces"]]
    inactive=[ns for ns in configured if LOCATOR_ORCHESTRATION_NAMESPACES[ns] not in active_ids]
    if inactive:
        findings.append(Finding("locator_orchestration_inactive_namespace","error","Locator orchestration references namespaces whose owning semantic modules are not active.",data={"namespaces":inactive}).as_dict())
    nodes,parse_findings=_semantic_ir(project)
    findings.extend(parse_findings)
    inv={ns:[] for ns in LOCATOR_ORCHESTRATION_NAMESPACES}
    parallel_locators={}
    for n in nodes:
        a=n.args
        if n.name=="PSELocator": inv["canonical"].append(_node_record(n,id=a[0].strip(),display=a[0].strip()))
        elif n.name=="PSELocatorNS" and a[0].strip()=="canonical": inv["canonical"].append(_node_record(n,id=a[1].strip(),display=a[1].strip()))
        elif n.name=="PSEDramaLine": inv["dramatic-line"].append(_node_record(n,id=a[0].strip(),display=a[0].strip()))
        elif n.name=="PSEVerseLine": inv["verse-line"].append(_node_record(n,id=a[0].strip(),display=(a[1].strip() or None)))
        elif n.name=="PSEParallelAlign": inv["parallel-alignment"].append(_node_record(n,id=a[0].strip(),display=None))
        elif n.name=="PSEParallelAlignmentLocator": parallel_locators[a[0].strip()]=a[1].strip()
    for row in inv["parallel-alignment"]:
        row["display"]=parallel_locators.get(row["id"])
    idpat=re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    bad=[]
    for ns in configured:
        for row in inv[ns]:
            if not idpat.fullmatch(row["id"]): bad.append({"namespace":ns,**row})
    if bad:
        findings.append(Finding("locator_orchestration_unstable_id","error","Configured locator namespaces contain IDs that are not stable machine-safe identifiers.",data={"entries":bad},location=_first_location(bad)).as_dict())
    metrics={
        "schema_version":cfg["schema_version"],
        "primary_namespace":cfg["primary_namespace"],
        "secondary_namespaces":cfg["secondary_namespaces"],
        "visible_numbering":cfg["visible_numbering"],
        "stable_id_policy":cfg["stable_id_policy"],
        "namespaces":{ns:{"count":len(inv[ns]),"inventory":inv[ns]} for ns in configured},
        "ownership":{ns:LOCATOR_ORCHESTRATION_NAMESPACES[ns] for ns in configured},
    }
    return findings,metrics

def _semantic_ir(project: Project) -> tuple[list[Any], list[dict[str, Any]]]:
    cached=getattr(project,"_semantic_ir_cache",None)
    if cached is not None:
        return cached
    nodes, errors = parse_files(_project_tex_sources(project), project.root)
    findings=[]
    for e in errors:
        findings.append(Finding("semantic_source_parse_error","error",e.message,location=loc_dict(e.loc),data={"parser_code":getattr(e,"code","parse_error")}).as_dict())
    payload=(nodes,findings)
    setattr(project,"_semantic_ir_cache",payload)
    return payload


def _node_record(node, **extra):
    d={"file":node.loc.file,"line":node.loc.line,"column":node.loc.column,"offset":node.loc.offset}
    d.update(extra); return d


def _record_location(record: dict[str, Any] | None) -> dict[str, Any] | None:
    if not record or not record.get("file"):
        return None
    return {
        "file": record["file"],
        "line": int(record.get("line", 1)),
        "column": int(record.get("column", 1)),
        "offset": int(record.get("offset", 0)),
    }


def _first_location(records: list[dict[str, Any]]) -> dict[str, Any] | None:
    return _record_location(records[0]) if records else None


def _format_finding_line(finding: dict[str, Any]) -> str:
    loc=finding.get("location") or {}
    prefix=""
    if loc.get("file"):
        prefix=f"{loc['file']}:{loc.get('line',1)}:{loc.get('column',1)}: "
    return f"{prefix}{finding.get('severity','info')}: {finding.get('code','finding')}: {finding.get('message','')}"


def _scholarly_source_qa(project: Project) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    metadata=_load_metadata(project.metadata_path)
    profile=_load_profile_manifest(project.repo_root,str(metadata.get("profile","basic-book")))
    active=_project_modules(project,profile)
    if not any("locator-contract" in m.get("qa_hooks",[]) for m in active): return [],{}
    nodes,findings=_semantic_ir(project); inventory=[]; refs=[]; ranges=[]; apparatus_stream_entries=[]
    for n in nodes:
        a=n.args
        if n.name=='PSELocatorNS': inventory.append(_node_record(n,namespace=a[0].strip(),id=a[1].strip()))
        elif n.name=='PSELocator': inventory.append(_node_record(n,namespace='canonical',id=a[0].strip()))
        elif n.name=='PSELocatorRefNS': refs.append(_node_record(n,namespace=a[0].strip(),id=a[1].strip()))
        elif n.name in {'PSELocatorRef','PSEApparatusEntry','PSEExplanatoryNote'}: refs.append(_node_record(n,namespace='canonical',id=a[0].strip()))
        elif n.name=='PSEApparatusStreamEntry':
            apparatus_stream_entries.append(_node_record(n,stream=a[0].strip(),kind='entry'))
            refs.append(_node_record(n,namespace='canonical',id=a[1].strip()))
        elif n.name=='PSELocatorRangeRefNS': ranges.append(_node_record(n,namespace=a[0].strip(),start=a[1].strip(),end=a[2].strip()))
        elif n.name in {'PSELocatorRangeRef','PSEApparatusRangeEntry'}: ranges.append(_node_record(n,namespace='canonical',start=a[0].strip(),end=a[1].strip()))
        elif n.name=='PSEApparatusStreamRangeEntry':
            apparatus_stream_entries.append(_node_record(n,stream=a[0].strip(),kind='range'))
            ranges.append(_node_record(n,namespace='canonical',start=a[1].strip(),end=a[2].strip()))
        elif n.name=='PSEDramaLine': inventory.append(_node_record(n,namespace='dramatic-line',id=a[0].strip()))
        elif n.name=='PSEDramaLineRef': refs.append(_node_record(n,namespace='dramatic-line',id=a[0].strip()))
        elif n.name=='PSEDramaLineRangeRef': ranges.append(_node_record(n,namespace='dramatic-line',start=a[0].strip(),end=a[1].strip()))
    allowed_apparatus_streams=("textual","editorial","translation","commentary","source")
    bad_streams=[x for x in apparatus_stream_entries if x["stream"] not in allowed_apparatus_streams]
    if bad_streams:
        findings.append(Finding("unknown_apparatus_stream","error","Source uses an undeclared apparatus stream.",data={"allowed":list(allowed_apparatus_streams),"entries":bad_streams},location=_first_location(bad_streams)).as_dict())
    schemes=_load_locator_schemes(project); metrics_schemes={}
    for ns,scheme in schemes["schemes"].items():
        inv=[x for x in inventory if x["namespace"]==ns]; ids=[x["id"] for x in inv]
        dup=sorted({x for x in ids if ids.count(x)>1})
        if dup: findings.append(Finding("duplicate_canonical_locator","error",f"Locator identifiers are duplicated in namespace {ns}.",data={"namespace":ns,"duplicates":dup},location=_first_location([x for x in inv if x["id"] in dup])).as_dict())
        order=scheme["order"]; pos={x:i for i,x in enumerate(order)}; present=set(ids)
        unknown=sorted(present-set(order))
        if unknown: findings.append(Finding("unknown_canonical_locator","error",f"Namespace {ns} contains undeclared locators.",data={"namespace":ns,"unknown":unknown},location=_first_location([x for x in inv if x["id"] in unknown])).as_dict())
        known=[x for x in ids if x in pos]
        if scheme["strict_order"] and any(pos[b]<=pos[a] for a,b in zip(known,known[1:])):
            findings.append(Finding("canonical_locator_out_of_order","error",f"Locator sequence is out of order in namespace {ns}.",data={"namespace":ns},location=_first_location(inv)).as_dict())
        missing=[x for x in order if x not in present]
        if scheme["require_complete"] and missing: findings.append(Finding("missing_canonical_locators","error",f"Namespace {ns} is missing required locators.",data={"namespace":ns,"missing":missing}).as_dict())
        badrefs=[x for x in refs if x["namespace"]==ns and (x["id"] not in pos or x["id"] not in present)]
        if badrefs: findings.append(Finding("unresolved_locator_source_reference","error",f"Namespace {ns} has unresolved locator references.",data={"namespace":ns,"references":badrefs},location=_first_location(badrefs)).as_dict())
        badranges=[]
        for rr in [x for x in ranges if x["namespace"]==ns]:
            a,b=rr["start"],rr["end"]
            if a not in pos or b not in pos or a not in present or b not in present or pos[a]>pos[b]: badranges.append(rr)
        if badranges: findings.append(Finding("invalid_locator_range","error",f"Namespace {ns} has invalid locator ranges.",data={"namespace":ns,"ranges":badranges},location=_first_location(badranges)).as_dict())
        metrics_schemes[ns]={"id":scheme.get("id",ns),"declared":len(order),"present":len(present),"missing":missing,"strict_order":scheme["strict_order"],"require_complete":scheme["require_complete"]}
    declared_ns=set(schemes["schemes"]); source_ns={x["namespace"] for x in inventory+refs+ranges}
    unknown_ns=sorted(source_ns-declared_ns)
    if unknown_ns:
        unknown_records=[x for x in inventory+refs+ranges if x["namespace"] in unknown_ns]
        findings.append(Finding("undeclared_locator_namespace","error","Source uses locator namespaces without declared schemes.",data={"namespaces":unknown_ns},location=_first_location(unknown_records)).as_dict())
    if not schemes["schemes"] and inventory: findings.append(Finding("locator_scheme_missing","review","Locator-capable project has locators but no locator scheme; sequence/completeness cannot be machine-audited.",location=_first_location(inventory)).as_dict())
    legacy_ranges=[{"start":x["start"],"end":x["end"],"file":x["file"],"line":x["line"]} for x in ranges if x["namespace"]=="canonical"]
    stream_counts={name:sum(1 for x in apparatus_stream_entries if x["stream"]==name) for name in allowed_apparatus_streams}
    metrics={"parser":"semantic-ir-1","locator_inventory":inventory,"locator_references":refs,"locator_ranges":legacy_ranges,"locator_ranges_namespaced":ranges,"locator_schemes":metrics_schemes,"apparatus_streams":{"allowed":list(allowed_apparatus_streams),"used":[name for name in allowed_apparatus_streams if stream_counts[name]],"counts":stream_counts,"entries":apparatus_stream_entries}}
    if "canonical" in metrics_schemes: metrics["locator_scheme"]=metrics_schemes["canonical"]
    return findings,metrics

def _drama_source_qa(project: Project) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    metadata=_load_metadata(project.metadata_path)
    profile=_load_profile_manifest(project.repo_root,str(metadata.get("profile","basic-book")))
    active=_project_modules(project,profile)
    if not any("drama-contract" in m.get("qa_hooks",[]) for m in active): return [],{}
    nodes,findings=_semantic_ir(project)
    speakers=[]; speech_uses=[]; acts=[]; scenes=[]; directions=[]
    idpat=re.compile(r"^[a-z][a-z0-9.-]*$")
    for n in nodes:
        a=n.args
        if n.name=='PSEDeclareSpeaker': speakers.append(_node_record(n,id=a[0].strip(),display=a[1].strip()))
        elif n.kind=='environment_begin' and n.name=='PSESpeech': speech_uses.append(_node_record(n,speaker_id=a[0].strip()))
        elif n.name=='PSEAct': acts.append(_node_record(n,id=a[0].strip(),display=a[1].strip()))
        elif n.name=='PSEScene': scenes.append(_node_record(n,id=a[0].strip(),display=a[1].strip()))
        elif n.name=='PSEStageDirection': directions.append(_node_record(n))
    def dup_ids(items):
        ids=[x['id'] for x in items]; return sorted({x for x in ids if ids.count(x)>1})
    bad_speaker_ids=sorted({x['id'] for x in speakers if not idpat.fullmatch(x['id'])})
    bad_act_ids=sorted({x['id'] for x in acts if not idpat.fullmatch(x['id'])})
    bad_scene_ids=sorted({x['id'] for x in scenes if not idpat.fullmatch(x['id'])})
    if bad_speaker_ids: findings.append(Finding('invalid_drama_speaker_id','error','Speaker identifiers must use stable lowercase semantic IDs.',data={'ids':bad_speaker_ids},location=_first_location([x for x in speakers if x['id'] in bad_speaker_ids])).as_dict())
    if bad_act_ids: findings.append(Finding('invalid_drama_act_id','error','Act identifiers must use stable lowercase semantic IDs.',data={'ids':bad_act_ids},location=_first_location([x for x in acts if x['id'] in bad_act_ids])).as_dict())
    if bad_scene_ids: findings.append(Finding('invalid_drama_scene_id','error','Scene identifiers must use stable lowercase semantic IDs.',data={'ids':bad_scene_ids},location=_first_location([x for x in scenes if x['id'] in bad_scene_ids])).as_dict())
    ds,da,dc=dup_ids(speakers),dup_ids(acts),dup_ids(scenes)
    if ds: findings.append(Finding('duplicate_drama_speaker','error','Speaker IDs are declared more than once.',data={'ids':ds},location=_first_location([x for x in speakers if x['id'] in ds])).as_dict())
    if da: findings.append(Finding('duplicate_drama_act','error','Act IDs are declared more than once.',data={'ids':da},location=_first_location([x for x in acts if x['id'] in da])).as_dict())
    if dc: findings.append(Finding('duplicate_drama_scene','error','Scene IDs are declared more than once.',data={'ids':dc},location=_first_location([x for x in scenes if x['id'] in dc])).as_dict())
    declared={x['id'] for x in speakers}; used=[x['speaker_id'] for x in speech_uses]
    undefined=sorted(set(used)-declared); unused=sorted(declared-set(used))
    if undefined: findings.append(Finding('undefined_drama_speaker','error','Speech blocks reference undeclared speaker IDs.',data={'ids':undefined},location=_first_location([x for x in speech_uses if x['speaker_id'] in undefined])).as_dict())
    if unused: findings.append(Finding('unused_drama_speaker','review','Declared speakers are not used by any speech block.',data={'ids':unused},location=_first_location([x for x in speakers if x['id'] in unused])).as_dict())
    metrics={'parser':'semantic-ir-1','speaker_registry':{'declared':speakers,'used':speech_uses,'unused':unused},'acts':acts,'scenes':scenes,'stage_directions':len(directions)}
    return findings,metrics

def _tex_escape(value: Any) -> str:
    s = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in s)


def _load_parallel_text_config(project: Project) -> dict[str, Any] | None:
    path=project.root/"config"/"parallel-text.json"
    if not path.is_file():
        return None
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid parallel-text config {path}: {exc}") from exc
    required={"schema_version","source_language","target_language","require_all_paired","alignment_policy"}
    if not isinstance(data,dict) or required-set(data):
        raise SystemExit("Invalid config/parallel-text.json contract.")
    if data.get("schema_version")!="1.0":
        raise SystemExit(f"Unsupported parallel-text config schema: {data.get('schema_version')!r}")
    for key in ("source_language","target_language"):
        if not isinstance(data.get(key),str) or not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*",data[key]):
            raise SystemExit(f"parallel-text {key} must be a BCP-47-like language tag.")
    if data["source_language"].lower()==data["target_language"].lower():
        raise SystemExit("parallel-text source_language and target_language must differ.")
    if not isinstance(data.get("require_all_paired"),bool):
        raise SystemExit("parallel-text require_all_paired must be boolean.")
    if data.get("alignment_policy") not in {"one-to-one","one-to-many","many-to-one","many-to-many"}:
        raise SystemExit("parallel-text alignment_policy is invalid.")
    return data


def _parallel_text_source_qa(project: Project) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    metadata=_load_metadata(project.metadata_path)
    profile=_load_profile_manifest(project.repo_root,str(metadata.get("profile","basic-book")))
    active=_project_modules(project,profile)
    if not any("parallel-text-contract" in m.get("qa_hooks",[]) for m in active): return [],{}
    nodes,findings=_semantic_ir(project); segments=[]; alignments=[]; notes=[]; locators=[]
    idpat=re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]*$")
    for n in nodes:
        a=n.args
        if n.name=='PSEParallelSegment':
            segments.append(_node_record(n,role=a[0].strip(),id=a[1].strip()))
        elif n.name=='PSEParallelAlign':
            alignments.append(_node_record(n,id=a[0].strip(),source_ids=[x.strip() for x in a[1].split(',') if x.strip()],target_ids=[x.strip() for x in a[2].split(',') if x.strip()]))
        elif n.name=='PSEParallelTranslationNote': notes.append(_node_record(n,alignment_id=a[0].strip(),kind='translation'))
        elif n.name=='PSEParallelNote': notes.append(_node_record(n,alignment_id=a[0].strip(),kind=a[1].strip()))
        elif n.name=='PSEParallelAlignmentLocator': locators.append(_node_record(n,alignment_id=a[0].strip(),locator=a[1].strip()))
    bad_roles=[x for x in segments if x['role'] not in {'source','target'}]
    if bad_roles: findings.append(Finding('parallel_invalid_role','error','Parallel-text segment role must be source or target.',data={'segments':bad_roles},location=_first_location(bad_roles)).as_dict())
    bad_ids=[x for x in segments if not idpat.fullmatch(x['id'])]
    if bad_ids: findings.append(Finding('parallel_invalid_segment_id','error','Parallel-text segment IDs must use stable machine-safe identifiers.',data={'segments':bad_ids},location=_first_location(bad_ids)).as_dict())
    keys=[(x['role'],x['id']) for x in segments]; dup=sorted({f'{r}:{i}' for r,i in keys if keys.count((r,i))>1})
    if dup: findings.append(Finding('parallel_duplicate_segment','error','Parallel-text segment IDs are duplicated within a role.',data={'duplicates':dup},location=_first_location([x for x in segments if f"{x['role']}:{x['id']}" in dup])).as_dict())
    aids=[x['id'] for x in alignments]; dup_a=sorted({x for x in aids if aids.count(x)>1})
    if dup_a: findings.append(Finding('parallel_duplicate_alignment','error','Parallel-text alignment IDs are duplicated.',data={'duplicates':dup_a},location=_first_location([x for x in alignments if x['id'] in dup_a])).as_dict())
    src_ids={x['id'] for x in segments if x['role']=='source'}; tgt_ids={x['id'] for x in segments if x['role']=='target'}
    unresolved=[]; invalid_shape=[]; config=_load_parallel_text_config(project)
    if config is None:
        findings.append(Finding('parallel_config_missing','error','Active parallel-text module requires config/parallel-text.json.').as_dict()); policy='many-to-many'
    else: policy=config['alignment_policy']
    for a in alignments:
        miss_s=[x for x in a['source_ids'] if x not in src_ids]; miss_t=[x for x in a['target_ids'] if x not in tgt_ids]
        if miss_s or miss_t: unresolved.append({'alignment':a['id'],'missing_source':miss_s,'missing_target':miss_t,'file':a['file'],'line':a['line']})
        ns,nt=len(a['source_ids']),len(a['target_ids']); ok=ns>=1 and nt>=1
        if policy=='one-to-one': ok=ok and ns==1 and nt==1
        elif policy=='one-to-many': ok=ok and ns==1
        elif policy=='many-to-one': ok=ok and nt==1
        if not ok: invalid_shape.append({'alignment':a['id'],'source_count':ns,'target_count':nt,'policy':policy,'file':a['file'],'line':a['line']})
    if unresolved: findings.append(Finding('parallel_unresolved_alignment','error','Parallel-text alignments reference undeclared segments.',data={'alignments':unresolved},location=_first_location(unresolved)).as_dict())
    if invalid_shape: findings.append(Finding('parallel_alignment_policy_violation','error','Parallel-text alignment shape violates the declared policy.',data={'alignments':invalid_shape},location=_first_location(invalid_shape)).as_dict())
    known_a=set(aids); bad_notes=[n for n in notes if n['alignment_id'] not in known_a]
    bad_locators=[n for n in locators if n['alignment_id'] not in known_a]
    if bad_notes: findings.append(Finding('parallel_unresolved_translation_note','error','Parallel-text notes reference undeclared alignment IDs.',data={'notes':bad_notes},location=_first_location(bad_notes)).as_dict())
    if bad_locators: findings.append(Finding('parallel_unresolved_locator','error','Parallel-text locators reference undeclared alignment IDs.',data={'locators':bad_locators},location=_first_location(bad_locators)).as_dict())
    loc_ids=[x['alignment_id'] for x in locators]; dup_l=sorted({x for x in loc_ids if loc_ids.count(x)>1})
    if dup_l: findings.append(Finding('parallel_duplicate_locator','error','Each parallel-text alignment may declare at most one locator.',data={'alignments':dup_l},location=_first_location([x for x in locators if x['alignment_id'] in dup_l])).as_dict())
    note_keys=[(x['alignment_id'],x.get('kind','translation')) for x in notes]; dup_n=sorted({f'{a}:{k}' for a,k in note_keys if note_keys.count((a,k))>1})
    if dup_n: findings.append(Finding('parallel_duplicate_note','error','Parallel-text note kinds must be unique within an alignment.',data={'notes':dup_n}).as_dict())
    paired_s={x for a in alignments for x in a['source_ids'] if x in src_ids}; paired_t={x for a in alignments for x in a['target_ids'] if x in tgt_ids}
    unpaired_s=sorted(src_ids-paired_s); unpaired_t=sorted(tgt_ids-paired_t)
    if config and config['require_all_paired'] and (unpaired_s or unpaired_t): findings.append(Finding('parallel_unpaired_segments','error','Parallel-text project requires all source and target segments to participate in an alignment.',data={'source':unpaired_s,'target':unpaired_t}).as_dict())
    elif unpaired_s or unpaired_t: findings.append(Finding('parallel_unpaired_segments','review','Parallel-text project contains unpaired segments.',data={'source':unpaired_s,'target':unpaired_t}).as_dict())
    metrics={'parser':'semantic-ir-1','source_language':config.get('source_language') if config else None,'target_language':config.get('target_language') if config else None,'alignment_policy':policy,'segments':{'source':len(src_ids),'target':len(tgt_ids)},'alignments':len(alignments),'translation_notes':sum(1 for n in notes if n.get('kind')=='translation'),'notes':len(notes),'locators':len(locators),'unpaired':{'source':unpaired_s,'target':unpaired_t},'inventory':segments,'alignment_inventory':alignments,'translation_note_inventory':notes,'locator_inventory':locators}
    return findings,metrics

def _load_bilingual_layout_config(project: Project) -> dict[str, Any] | None:
    path=project.root/"config"/"bilingual-layout.json"
    if not path.is_file():
        return None
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid bilingual layout config {path}: {exc}") from exc
    required={"schema_version","mode","synchronization_policy","long_segment_policy","show_language_labels"}
    if not isinstance(data,dict) or required-set(data):
        raise SystemExit("Invalid config/bilingual-layout.json contract.")
    if data.get("schema_version") not in {"1.0","1.1"}:
        raise SystemExit(f"Unsupported bilingual-layout config schema: {data.get('schema_version')!r}")
    if data.get("mode") not in {"parallel-columns","facing-pages","sequential-blocks","source-dominant","target-dominant"}:
        raise SystemExit("bilingual-layout mode must be parallel-columns, facing-pages, sequential-blocks, source-dominant, or target-dominant.")
    if data.get("synchronization_policy") != "alignment-block":
        raise SystemExit("bilingual-layout synchronization_policy is unsupported.")
    if data.get("long_segment_policy") not in {"flow","review"}:
        raise SystemExit("bilingual-layout long_segment_policy must be flow or review.")
    if not isinstance(data.get("show_language_labels"),bool):
        raise SystemExit("bilingual-layout show_language_labels must be boolean.")
    return data


def _write_generated_bilingual_layout(project: Project) -> Path | None:
    cfg=_load_bilingual_layout_config(project)
    if cfg is None:
        return None
    parallel=_load_parallel_text_config(project)
    if parallel is None:
        raise SystemExit("A bilingual visual profile requires config/parallel-text.json.")
    generated=project.build_dir/"pse-bilingual-layout.tex"
    generated.parent.mkdir(parents=True,exist_ok=True)
    show="true" if cfg["show_language_labels"] else "false"
    lines=[
        "% Generated by PSE bilingual layout bridge. Do not edit by hand.",
        rf"\renewcommand{{\PSEBilingualLayoutMode}}{{{_tex_escape(cfg['mode'])}}}",
        rf"\renewcommand{{\PSEBilingualSourceLanguage}}{{{_tex_escape(parallel['source_language'])}}}",
        rf"\renewcommand{{\PSEBilingualTargetLanguage}}{{{_tex_escape(parallel['target_language'])}}}",
        rf"\renewcommand{{\PSEBilingualShowLanguageLabels}}{{{show}}}",
        rf"\renewcommand{{\PSEBilingualLongSegmentPolicy}}{{{_tex_escape(cfg['long_segment_policy'])}}}",
    ]
    generated.write_text("\n".join(lines)+"\n",encoding="utf-8")
    return generated

def _bilingual_layout_qa(project: Project) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg=_load_bilingual_layout_config(project)
    if cfg is None:
        return [],{}
    findings=[]
    metrics={"mode":cfg["mode"],"synchronization_policy":cfg["synchronization_policy"],"long_segment_policy":cfg["long_segment_policy"],"show_language_labels":cfg["show_language_labels"]}
    if cfg["mode"]=="facing-pages" and cfg["long_segment_policy"]=="review":
        findings.append(Finding("bilingual_facing_pages_overflow_review","review","Facing-page mode cannot guarantee exact page pairing when a segment exceeds one page; review long alignments visually.").as_dict())
    return findings,metrics


def _write_generated_metadata(project: Project, data: dict[str, Any]) -> Path:
    project.build_dir.mkdir(parents=True, exist_ok=True)
    generated = project.build_dir / "pse-metadata.tex"
    page = data.get("page", {}) or {}
    width = page.get("width_mm", 126)
    height = page.get("height_mm", 198)
    lines = [
        "% Generated by PSE. Do not edit by hand.",
        rf"\PSESetTitle{{{_tex_escape(data['title'])}}}",
        rf"\PSESetAuthor{{{_tex_escape(data['author'])}}}",
        rf"\PSESetLanguage{{{_tex_escape(data['language'])}}}",
        rf"\PSESetPublicationYear{{{_tex_escape(data['publication_year'])}}}",
        rf"\PSESetSubtitle{{{_tex_escape(data.get('subtitle', ''))}}}",
        rf"\PSESetSeries{{{_tex_escape(data.get('series', ''))}}}",
        rf"\PSESetPageWidth{{{width}mm}}",
        rf"\PSESetPageHeight{{{height}mm}}",
    ]
    generated.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return generated



def _strip_tex_comments(text: str) -> str:
    lines=[]
    for line in text.splitlines():
        escaped=False
        cut=None
        for i,ch in enumerate(line):
            if ch == "\\":
                escaped = not escaped
                continue
            if ch == "%" and not escaped:
                cut=i
                break
            escaped=False
        lines.append(line if cut is None else line[:cut])
    return "\n".join(lines)


def _validate_structural_hierarchy_source(project: Project, modules: list[dict[str, Any]]) -> None:
    if not any(m.get("id") == "structural-hierarchy" for m in modules):
        return
    violations=[]
    for tex in sorted(project.root.rglob("*.tex")):
        try:
            rel=tex.relative_to(project.root)
        except ValueError:
            continue
        if rel.parts and rel.parts[0] == "build":
            continue
        text=_strip_tex_comments(tex.read_text(encoding="utf-8",errors="replace"))
        for match in re.finditer(r"\\subparagraph\s*(?:\[[^\]]*\]\s*)?\{", text):
            line=text.count("\n",0,match.start())+1
            violations.append(f"{rel.as_posix()}:{line}")
    if violations:
        raise SystemExit(
            "Structural hierarchy depth exceeds the four-level section contract at "
            + ", ".join(violations)
            + ". Part and Chapter are publication divisions/units and are not counted. "
              "Inside a chapter use section -> subsection -> subsubsection -> paragraph. "
              "PSE does not flatten deeper manuscript structure automatically."
        )


def _write_generated_modules(project: Project, metadata: dict[str, Any]) -> Path:
    profile=str(metadata.get("profile","basic-book"))
    manifest=_load_profile_manifest(project.repo_root,profile)
    modules=_project_modules(project,manifest)
    _validate_structural_hierarchy_source(project, modules)
    generated=project.build_dir/"pse-modules.tex"
    generated.parent.mkdir(parents=True,exist_ok=True)
    lines=["% Generated by PSE semantic resolver. Do not edit by hand."]
    lines += [rf"\usepackage{{pse-module-{m['id']}}}" for m in modules]
    generated.write_text("\n".join(lines)+"\n",encoding="utf-8")
    _write_generated_bilingual_layout(project)
    _write_generated_locator_orchestration(project)
    return generated


def _run_lualatex(project: Project, passes: int = 2, *, output_dir: Path | None = None, jobname: str = "book", source_date_epoch: int | None = None) -> None:
    exe = shutil.which("lualatex")
    if not exe:
        raise SystemExit("LuaLaTeX is not available on PATH.")
    env = os.environ.copy()
    if source_date_epoch is not None:
        env["SOURCE_DATE_EPOCH"] = str(int(source_date_epoch))
        env["FORCE_SOURCE_DATE"] = "1"
    metadata = _load_metadata(project.metadata_path)
    profile = str(metadata.get("profile", "basic-book"))
    manifest = _load_profile_manifest(project.repo_root, profile)
    _validate_profile_metadata(metadata, manifest)
    profile_dir = project.repo_root / "profiles" / profile
    module_manifests = _project_modules(project, manifest)
    tex_roots = [
        str((project.repo_root / "core").resolve()),
        str(profile_dir.resolve()),
        *[str((project.repo_root / "modules" / m["id"]).resolve()) for m in module_manifests],
    ]
    old = env.get("TEXINPUTS", "")
    sep = os.pathsep
    env["TEXINPUTS"] = sep.join(tex_roots) + sep + old
    actual_output = output_dir or project.build_dir
    actual_output.mkdir(parents=True, exist_ok=True)
    cmd = [
        exe,
        "--no-shell-escape",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-output-directory={actual_output}",
        f"-jobname={jobname}",
        project.main_tex.name,
    ]
    # First LaTeX pass establishes auxiliary files. Semantic modules may then
    # request explicit, non-shell auxiliary tools. No command is constructed
    # from manuscript text.
    def run_tex(pass_no: int) -> None:
        proc = subprocess.run(cmd, cwd=project.root, env=env, text=True, capture_output=True)
        (actual_output / f"lualatex-pass-{pass_no}.stdout.log").write_text(proc.stdout + "\n" + proc.stderr, encoding="utf-8")
        if proc.returncode != 0:
            tail = "\n".join((proc.stdout + "\n" + proc.stderr).splitlines()[-30:])
            raise SystemExit(f"LuaLaTeX failed on pass {pass_no}.\n{tail}")
    run_tex(1)
    build_tools=_project_build_tools(project, manifest)
    if "biber" in build_tools and (actual_output / f"{jobname}.bcf").is_file():
        exe_biber=shutil.which("biber")
        if not exe_biber:
            raise SystemExit("This profile requires biber, but biber is not available on PATH.")
        proc=subprocess.run([exe_biber, f"--output-directory={actual_output}", jobname],cwd=project.root,env=env,text=True,capture_output=True)
        (actual_output / "biber.stdout.log").write_text(proc.stdout+"\n"+proc.stderr,encoding="utf-8")
        if proc.returncode != 0:
            raise SystemExit("biber failed. See build/biber.stdout.log.")
    if "makeindex" in build_tools and (actual_output / f"{jobname}.idx").is_file():
        exe_idx=shutil.which("makeindex")
        if not exe_idx:
            raise SystemExit("This profile requires makeindex, but makeindex is not available on PATH.")
        proc=subprocess.run([exe_idx,"-o",f"{jobname}.ind",f"{jobname}.idx"],cwd=actual_output,env=env,text=True,capture_output=True)
        (actual_output / "makeindex.stdout.log").write_text(proc.stdout+"\n"+proc.stderr,encoding="utf-8")
        if proc.returncode != 0:
            raise SystemExit("makeindex failed. See build/makeindex.stdout.log.")
    final_passes = max(3 if build_tools else 2, passes)
    for idx in range(2, final_passes + 1):
        run_tex(idx)


def _slugify(value: str) -> str:
    """Return a conservative cross-platform project slug."""
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    if not value:
        raise SystemExit("Project slug cannot be empty after normalization.")
    if len(value) > 64:
        raise SystemExit("Project slug must be 64 characters or fewer.")
    reserved = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}
    if value in reserved:
        raise SystemExit(f"Project slug {value!r} is reserved on Windows.")
    return value


def _prompt(label: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    answer = input(f"{label}{suffix}: ").strip()
    return answer or (default or "")


def _safe_project_destination(parent: Path, slug: str) -> Path:
    parent = parent.expanduser().resolve()
    dest = (parent / slug).resolve()
    try:
        dest.relative_to(parent)
    except ValueError as exc:
        raise SystemExit("Unsafe project path resolution.") from exc
    if dest.exists():
        if not dest.is_dir():
            raise SystemExit(f"Destination exists and is not a directory: {dest}")
        if any(dest.iterdir()):
            raise SystemExit(f"Destination directory is not empty: {dest}")
    return dest


def _write_new_project(dest: Path, *, title: str, author: str, language: str, publication_year: int,
                       subtitle: str = "", series: str = "", width_mm: float = 126, height_mm: float = 198,
                       profile: str = "basic-book") -> None:
    for rel in ("content", "assets", "config", "tests"):
        (dest / rel).mkdir(parents=True, exist_ok=True)
    for rel in ("assets/.gitkeep", "tests/.gitkeep"):
        (dest / rel).write_text("", encoding="utf-8")
    (dest / "config" / "pse-local.tex").write_text(
        "% Title-local overrides only. Keep shared/profile rules out of this file unless the exception is truly title-specific.\n",
        encoding="utf-8",
    )
    (dest / "config" / "semantic-modules.json").write_text(
        json.dumps({"schema_version":"1.1","activate":[],"deactivate":[],"config":{}}, indent=2) + "\n",
        encoding="utf-8",
    )

    metadata = {
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "language": language,
        "publication_year": publication_year,
        "series": series,
        "profile": profile,
        "page": {"width_mm": width_mm, "height_mm": height_mm},
    }
    (dest / "book.yml").write_text(yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False), encoding="utf-8")

    locator_defaults = {
        "scholarly-edition": ("canonical", "show"),
        "critical-edition": ("canonical", "show"),
        "drama": ("dramatic-line", "show"),
        "poetry": ("verse-line", "source-defined"),
        "bilingual-edition": ("parallel-alignment", "source-defined"),
    }
    if profile in locator_defaults:
        primary, visibility = locator_defaults[profile]
        locator_orchestration={
            "schema_version":"1.0",
            "primary_namespace":primary,
            "secondary_namespaces":[],
            "visible_numbering":visibility,
            "stable_id_policy":"required",
        }
        (dest / "config" / "locator-orchestration.json").write_text(json.dumps(locator_orchestration,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    if profile == "scholarly-edition":
        locator_scheme = {"schema_version":"1.0","id":"synthetic-sequence","order":["A1","A2","B1"],"require_complete":True,"strict_order":True}
        (dest / "config" / "locator-scheme.json").write_text(json.dumps(locator_scheme, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        locator_schemes={"schema_version":"1.0","schemes":{"canonical":locator_scheme}}
        (dest / "config" / "locator-schemes.json").write_text(json.dumps(locator_schemes, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
        semantic_cfg={"schema_version":"1.1","activate":[],"deactivate":[],"config":{}}
        (dest / "config" / "semantic-modules.json").write_text(json.dumps(semantic_cfg,indent=2)+"\n",encoding="utf-8")
        scholarly_main = r'''% Generated by Publication Systems Engineering.
% Generic scholarly-edition starter with synthetic content only.
\documentclass[10pt,twoside,openany]{book}
\usepackage{pse-core}
\usepackage{pse-profile-scholarly-edition}
\InputIfFileExists{build/pse-modules.tex}{}{}
\PSEAddBibliographyResource{references.bib}
\InputIfFileExists{config/pse-local.tex}{}{}

\begin{document}
\PSEBeginFrontMatter
\PSETitlePage
\PSEPublicationPage
\PSEScholarlyFrontChapter{Editorial Note}
This synthetic starter demonstrates semantic scholarly modules. Replace it with project-owned editorial matter.
\tableofcontents
\clearpage
\PSEBeginBody
\input{content/text.tex}
\PSEBeginBackMatter
\PSEScholarlyBackChapter{Apparatus}
\input{content/apparatus.tex}
\PSEPrintBibliography
\PSEPrintIndex
\end{document}
'''
        (dest / "main.tex").write_text(scholarly_main, encoding="utf-8")
        (dest / "content" / "text.tex").write_text(r'''\chapter{Synthetic text}
\PSELocator{A1}This is synthetic scholarly text. The term \PSEGreek{ὄνομα} (\PSETransliteration{onoma}) is indexed here.\PSEIndex{name}\PSEIndexTerm{onoma}{\PSEGreek{ὄνομα}}

\PSELocator{A2}A second passage demonstrates canonical location and citation.\autocite{synthetic2027}

\section{A semantic boundary}
\PSELocator{B1}The visual profile controls presentation; semantic modules control locator, apparatus, bibliography, index, and multilingual behavior.
''', encoding="utf-8")
        (dest / "content" / "apparatus.tex").write_text(r'''\begin{PSEApparatus}
\PSEApparatusStreamEntry{commentary}{A1}{name}{Synthetic explanatory note attached to a canonical locator.}
\PSEApparatusStreamRangeEntry{editorial}{A1}{A2}{range note}{Synthetic note demonstrating an apparatus range keyed to canonical locators.}
\PSEApparatusStreamEntry{source}{B1}{semantic boundary}{The note demonstrates separation between presentation profiles and scholarly semantics.}
\end{PSEApparatus}
''', encoding="utf-8")
        (dest / "references.bib").write_text(r'''@book{synthetic2027,
  author = {Example, Ada},
  title = {Synthetic Reference for Regression Testing},
  year = {2027},
  publisher = {Example Imprint}
}
''', encoding="utf-8")
    elif profile == "critical-edition":
        locator_scheme = {"schema_version":"1.0","id":"synthetic-critical-sequence","order":["1.1","1.2","1.3","2.1"],"require_complete":True,"strict_order":True}
        (dest / "config" / "locator-scheme.json").write_text(json.dumps(locator_scheme, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        locator_schemes={"schema_version":"1.0","schemes":{"canonical":locator_scheme}}
        (dest / "config" / "locator-schemes.json").write_text(json.dumps(locator_schemes, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
        semantic_cfg={"schema_version":"1.1","activate":[],"deactivate":[],"config":{}}
        (dest / "config" / "semantic-modules.json").write_text(json.dumps(semantic_cfg,indent=2)+"\n",encoding="utf-8")
        critical_main = r'''% Generated by Publication Systems Engineering.
% Generic critical-edition starter with synthetic content only.
\documentclass[10pt,twoside,openany]{book}
\usepackage{pse-core}
\usepackage{pse-profile-critical-edition}
\InputIfFileExists{build/pse-modules.tex}{}{}
\PSEAddBibliographyResource{references.bib}
\InputIfFileExists{config/pse-local.tex}{}{}

\begin{document}
\PSEBeginFrontMatter
\PSETitlePage
\PSEPublicationPage
\PSEScholarlyFrontChapter{Editorial Principles}
This synthetic starter demonstrates a source-oriented critical edition. Canonical locators and apparatus semantics remain module-owned and independent of page position.
\tableofcontents
\clearpage
\PSEBeginBody
\input{content/critical-text.tex}
\PSEBeginBackMatter
\PSEScholarlyBackChapter{Critical Apparatus}
\input{content/apparatus.tex}
\PSEScholarlyBackChapter{Editorial Notes}
\input{content/editorial-notes.tex}
\PSEPrintBibliography
\PSEPrintIndex
\end{document}
'''
        (dest / "main.tex").write_text(critical_main, encoding="utf-8")
        (dest / "content" / "critical-text.tex").write_text(r'''\chapter{Synthetic Critical Text}
\PSELocator{1.1}A short synthetic lemma establishes the first canonical location. The Greek term \PSEGreek{λόγος} (\PSETransliteration{logos}) is indexed as an example.\PSEIndex{logos}\PSEIndexTerm{logos}{\PSEGreek{λόγος}}

\PSELocator{1.2}A second synthetic sentence demonstrates continuous text whose semantic address remains stable when pagination changes.\autocite{syntheticcritical2027}

\PSELocator{1.3}A third sentence supplies a variant-bearing location for the apparatus without encoding the apparatus into presentation markup.

\section{Second synthetic section}
\PSELocator{2.1}A final location demonstrates that critical-text presentation belongs to the profile while locator, apparatus, bibliography, index, and multilingual behavior remain reusable modules.
''' ,encoding="utf-8")
        (dest / "content" / "apparatus.tex").write_text(r'''\begin{PSEApparatus}
\PSEApparatusStreamEntry{textual}{1.1}{lemma}{Synthetic witness A reads \emph{logos}; witness B omits the term.}
\PSEApparatusStreamRangeEntry{editorial}{1.2}{1.3}{punctuation}{Synthetic witnesses differ only in punctuation across this range.}
\PSEApparatusStreamEntry{source}{2.1}{structure}{The entry demonstrates an apparatus keyed to canonical source locations rather than page numbers.}
\end{PSEApparatus}
''' ,encoding="utf-8")
        (dest / "content" / "editorial-notes.tex").write_text(r'''\noindent These notes are synthetic. They demonstrate scholarly back matter without importing manuscript-specific editorial policy into the framework.

A critical edition may add project-owned witness descriptions, sigla, or editorial rationale through title source and documented semantic modules.
''' ,encoding="utf-8")
        (dest / "references.bib").write_text(r'''@book{syntheticcritical2027,
  author = {Example, Ada},
  title = {Synthetic Witnesses and Critical Editing},
  year = {2027},
  publisher = {Example Imprint}
}
''' ,encoding="utf-8")
    elif profile == "edited-collection":
        semantic_cfg={"schema_version":"1.1","activate":[],"deactivate":[],"config":{}}
        (dest / "config" / "semantic-modules.json").write_text(json.dumps(semantic_cfg,indent=2)+"\n",encoding="utf-8")
        edited_main = r'''% Generated by Publication Systems Engineering.
% Generic edited-collection starter with synthetic content only.
\documentclass[10pt,twoside,openany]{book}
\usepackage{pse-core}
\usepackage{pse-profile-edited-collection}
\InputIfFileExists{build/pse-modules.tex}{}{}
\InputIfFileExists{config/pse-local.tex}{}{}

\begin{document}
\PSEDeclareContributor{ada-example}{Ada Example}[Institute for Synthetic Studies][0000-0000-0000-0000]
\PSEDeclareContributor{ben-example}{Ben Example}[Department of Demonstration]
\PSEDeclareContributor{cy-example}{Cy Example}
\PSEBeginFrontMatter
\PSETitlePage
\PSEPublicationPage
\tableofcontents
\clearpage
\PSEBeginBody
\input{content/chapter-01.tex}
\input{content/chapter-02.tex}
\input{content/chapter-03.tex}
\PSEBeginBackMatter
\chapter*{Contributor Note}
\addcontentsline{toc}{chapter}{Contributor Note}
Contributor identity is semantic data; chapter-credit typography belongs to the edited-collection profile.
\PSEPrintIndex
\end{document}
'''
        (dest / "main.tex").write_text(edited_main, encoding="utf-8")
        chapters = [
            ('chapter-01.tex', r'''\PSEDeclarePublicationUnit{chapter-01}{Infrastructure as a publication problem}
\PSEPublicationUnitAbstract{chapter-01}{This synthetic abstract demonstrates publication-unit metadata that remains independent of chapter-title typography.}
\PSEPublicationUnitKeywords{chapter-01}{infrastructure; publishing systems; metadata}
\PSEPublicationUnitDOI{chapter-01}{10.0000/pse.synthetic.001}
\PSEPublicationUnitContributor{chapter-01}{ada-example}{author}
\PSEOpenPublicationUnit{chapter-01}
This synthetic chapter demonstrates a single chapter author. Contributor identity and affiliation are reused from the contributor registry.\PSEIndex{publication infrastructure}

\section{A reusable relation}
A contributor can be related to a publication unit without encoding that relation in the chapter title itself.\PSEIndex{contributors}
'''),
            ('chapter-02.tex', r'''\PSEDeclarePublicationUnit{chapter-02}{Shared editorial work}
\PSEPublicationUnitContributor{chapter-02}{ben-example}{author}
\PSEPublicationUnitContributor{chapter-02}{cy-example}{author}
\PSEOpenPublicationUnit{chapter-02}
This synthetic chapter demonstrates two contributors attached independently to the same publication unit.\PSEIndex{collaboration}
'''),
            ('chapter-03.tex', r'''\PSEDeclarePublicationUnit{chapter-03}{Roles can differ by unit}
\PSEPublicationUnitContributor{chapter-03}{ada-example}{editor}
\PSEOpenPublicationUnit{chapter-03}
This synthetic chapter demonstrates that role belongs to a contribution relation, not permanently to a person identity.\PSEIndex{roles}
'''),
        ]
        for fn, body in chapters:
            (dest / "content" / fn).write_text(body, encoding="utf-8")
    elif profile == "poetry":
        semantic_cfg={"schema_version":"1.1","activate":[],"deactivate":[],"config":{}}
        (dest / "config" / "semantic-modules.json").write_text(json.dumps(semantic_cfg,indent=2)+"\n",encoding="utf-8")
        poetry_main = r'''% Generated by Publication Systems Engineering.
% Generic poetry starter with synthetic content only.
\documentclass[10pt,twoside,openany]{book}
\usepackage{pse-core}
\usepackage{pse-profile-poetry}
\InputIfFileExists{build/pse-modules.tex}{}{}
\InputIfFileExists{config/pse-local.tex}{}{}

\begin{document}
\PSEBeginFrontMatter
\PSETitlePage
\PSEPublicationPage
\tableofcontents
\clearpage
\PSEBeginBody
\input{content/poems.tex}
\end{document}
'''
        (dest / "main.tex").write_text(poetry_main, encoding="utf-8")
        (dest / "content" / "poems.tex").write_text(r'''\chapter*{Synthetic Poems}
\addcontentsline{toc}{chapter}{Synthetic Poems}

\section*{A Small Structure}
\begin{PSEStanza}{s1}
\PSEVerseLine{l1}[1]{A synthetic line begins where meaning stays,}
\PSEVerseLine{l2}[2]{while page design may alter where it lays.}
\PSEVerseLine{l3}[3]{The identifier persists through every flow,}
\PSEVerseLine{l4}[4]{and presentation changes what readers know.}
\end{PSEStanza}

\begin{PSEStanza}{s2}
\PSEVerseLine{l5}{This deliberately longer synthetic verse line demonstrates hanging continuation when a line exceeds the available measure without creating a second semantic verse line.}
\PSEVerseLine{l6}[6]{A final line closes the synthetic test.}
\end{PSEStanza}
''', encoding="utf-8")
    elif profile == "drama":
        locator_scheme={"schema_version":"1.0","id":"synthetic-dramatic-lines","order":["L1","L2","L3","L4"],"require_complete":True,"strict_order":True}
        locator_schemes={"schema_version":"1.0","schemes":{"dramatic-line":locator_scheme}}
        (dest / "config" / "locator-schemes.json").write_text(json.dumps(locator_schemes,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        semantic_cfg={"schema_version":"1.1","activate":[],"deactivate":[],"config":{}}
        (dest / "config" / "semantic-modules.json").write_text(json.dumps(semantic_cfg,indent=2)+"\n",encoding="utf-8")
        drama_main=r'''% Generated by Publication Systems Engineering.
% Generic drama starter with synthetic content only.
\documentclass[10pt,twoside,openany]{book}
\usepackage{pse-core}
\usepackage{pse-profile-drama}
\InputIfFileExists{build/pse-modules.tex}{}{}
\InputIfFileExists{config/pse-local.tex}{}{}
\begin{document}
\PSEBeginFrontMatter
\PSETitlePage
\PSEPublicationPage
\input{content/cast.tex}
\PSEPrintCastList
\tableofcontents
\clearpage
\PSEBeginBody
\chapter{The Play}
\input{content/play.tex}
\PSEBeginBackMatter
\chapter*{Production Note}
\addcontentsline{toc}{chapter}{Production Note}
This generated starter contains synthetic dramatic text only. Replace it with project-owned content.
\PSEPrintIndex
\end{document}
'''
        (dest / "main.tex").write_text(drama_main,encoding="utf-8")
        (dest / "content" / "cast.tex").write_text(r'''\PSEDeclareSpeaker{alpha}{Alpha}
\PSEDeclareSpeaker{beta}{Beta}
\PSEDeclareSpeaker{chorus}{Chorus}
''',encoding="utf-8")
        (dest / "content" / "play.tex").write_text(r'''\PSEAct{act-one}{Act One}
\PSEScene{scene-one}{A bare room}
\PSEStageDirection{Alpha enters. Beta waits by the window.}
\PSEDramaLine{L1}\begin{PSESpeech}{alpha}We begin with a synthetic line.\end{PSESpeech}
\PSEDramaLine{L2}\begin{PSESpeech}{beta}And answer it with another.\end{PSESpeech}
\PSEStageDirection{The chorus enters.}
\PSEDramaLine{L3}\begin{PSESpeech}{chorus}A semantic system should survive changes in presentation.\PSEIndex{chorus}\end{PSESpeech}
\PSEDramaLine{L4}\begin{PSESpeech}{alpha}Then let the profile change the page, not the meaning.\end{PSESpeech}
''',encoding="utf-8")
    elif profile == "bilingual-edition":
        semantic_cfg={"schema_version":"1.1","activate":[],"deactivate":[],"config":{}}
        (dest / "config" / "semantic-modules.json").write_text(json.dumps(semantic_cfg,indent=2)+"\n",encoding="utf-8")
        parallel_cfg={"schema_version":"1.0","source_language":"fr","target_language":language,"require_all_paired":True,"alignment_policy":"one-to-one"}
        (dest / "config" / "parallel-text.json").write_text(json.dumps(parallel_cfg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        layout_cfg={"schema_version":"1.1","mode":"parallel-columns","synchronization_policy":"alignment-block","long_segment_policy":"flow","show_language_labels":True}
        (dest / "config" / "bilingual-layout.json").write_text(json.dumps(layout_cfg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        bilingual_main=r'''% Generated by Publication Systems Engineering.
% Generic bilingual-edition starter with synthetic content only.
\documentclass[10pt,twoside,openany]{book}
\usepackage{pse-core}
\usepackage{pse-profile-bilingual-edition}
\InputIfFileExists{build/pse-bilingual-layout.tex}{}{}
\InputIfFileExists{build/pse-modules.tex}{}{}
\InputIfFileExists{config/pse-local.tex}{}{}
\begin{document}
\PSEBeginFrontMatter
\PSETitlePage
\PSEPublicationPage
\tableofcontents
\clearpage
\PSEBeginBody
\chapter{Parallel Text}
\input{content/parallel.tex}
\PSEBeginBackMatter
\chapter*{Translation Note}
\addcontentsline{toc}{chapter}{Translation Note}
This generated starter contains synthetic source and target segments only. Replace them with project-owned text.
\PSEPrintIndex
\end{document}
'''
        (dest / "main.tex").write_text(bilingual_main,encoding="utf-8")
        (dest / "content" / "parallel.tex").write_text(r'''\PSEParallelSegment{source}{s1}{Une première phrase synthétique sert de texte source.}
\PSEParallelSegment{target}{t1}{A first synthetic sentence serves as the target text.}
\PSEParallelAlign{a1}{s1}{t1}
\PSEParallelAlignmentLocator{a1}{§ 1}
\PSEParallelTranslationNote{a1}{This note is linked to alignment a1, not to a visual page position.}\PSEIndex{alignment}

\PSEParallelSegment{source}{s2}{Une seconde unité est volontairement un peu plus longue afin de montrer que la présentation peut laisser le texte couler sans modifier les identifiants sémantiques.}
\PSEParallelSegment{target}{t2}{A second unit is deliberately a little longer to show that presentation may let text flow without changing the semantic identifiers.}
\PSEParallelAlign{a2}{s2}{t2}
\PSEParallelNote{a2}{editorial}{Alignment is semantic and survives a presentation-mode change.}
''',encoding="utf-8")
    else:
        main_tex = r'''% Generated by Publication Systems Engineering.
% Source of truth: book.yml + main.tex + content/ + project-owned assets/config.
\documentclass[10pt,twoside,openany]{book}
\usepackage{pse-core}
\usepackage{pse-profile-PROFILE_ID}
\InputIfFileExists{build/pse-modules.tex}{}{}
\InputIfFileExists{config/pse-local.tex}{}{}

\begin{document}
\PSEBeginFrontMatter
\PSETitlePage
\PSEPublicationPage
\tableofcontents
\clearpage
\PSEBeginBody
\input{content/chapter-01.tex}
\PSEBeginBackMatter
\chapter*{Production Note}
\addcontentsline{toc}{chapter}{Production Note}
This generated starter contains synthetic text only. Replace it with project-owned content.
\end{document}
'''.replace("PROFILE_ID", profile)
        if profile in {"basic-book", "academic-monograph"}:
            main_tex = main_tex.replace("\\end{document}", "\\PSEPrintIndex\n\\end{document}")
        (dest / "main.tex").write_text(main_tex, encoding="utf-8")
        chapter = r'''\chapter{First chapter}

Replace this synthetic starter text with your manuscript. Keep semantic structure in the source: use chapter, section, quotation, footnote and other document commands rather than manual visual formatting.

\section{A first section}

This project was generated with the selected PSE profile. Project-specific design changes belong in \texttt{config/pse-local.tex}; reusable profile rules belong in the profile, never in the shared core.
'''
        if profile in {"basic-book", "academic-monograph"}:
            chapter += "\n\\PSEIndex{publication systems}\n"
        (dest / "content" / "chapter-01.tex").write_text(chapter, encoding="utf-8")

    gitignore = '''# Generated build, proof, and publication-release artifacts
/build/
/release/

# Local editor/OS files
.DS_Store
Thumbs.db
*.swp
*.tmp

# Python cache
__pycache__/
*.py[cod]

# Secrets and local environment files
.env
.env.*
!.env.example
*.key
*.pem
'''
    (dest / ".gitignore").write_text(gitignore, encoding="utf-8")

    readme = f'''# {title}

This is a Publication Systems Engineering project generated with the `{profile}` profile.

## Source of truth

The canonical project sources are `book.yml`, `main.tex`, `content/`, `assets/`, and project-owned configuration. The `build/` directory is generated and must not be edited as source.

## Environment preflight

After installing or updating PSE, run `pse doctor`. Use `pse doctor --deep` when diagnosing a workstation or secure-build environment. Normal installed use does not require `PSE_ROOT` or manual `PYTHONPATH`.

## Standard workflow

```text
pse build .
pse check .
pse proof . --recipient "Recipient Name"
pse release .
pse verify-release release/<release-id>
pse clean .
```

Do not run LuaLaTeX with shell escape. PSE invokes LuaLaTeX with `--no-shell-escape` by default.

## Security boundary

Keep unpublished manuscripts and project assets in a private repository or private storage controlled by your organization. Do not commit generated recipient proofs. Watermarked proof PDFs support deterrence and traceability; they are not unremovable DRM.

## Profile status

`{profile}` is a generator-supported profile. Use `config/pse-local.tex` for restrained title-local exceptions rather than editing the shared core or profile package.
'''
    if profile == "scholarly-edition":
        readme += '''
## Scholarly semantic modules

This project activates generic canonical locators, apparatus, multilingual/Greek text, bibliography, index, and scholarly-matter modules. Keep semantic markup in title-owned source; do not copy framework module code into the title.
'''
    if profile == "critical-edition":
        readme += '''
## Critical-edition semantics

This project uses canonical locators, apparatus, multilingual text, bibliography, index, and scholarly-matter modules. Critical-text page architecture belongs to the `critical-edition` profile; canonical locations and editorial source data belong in title-owned source.
'''
    if profile == "edited-collection":
        readme += '''
## Edited-collection contributor semantics

This project uses stable contributor identities and explicit contributor/unit/role relations from the `contributor-metadata` semantic module. Chapter-credit typography belongs to the `edited-collection` profile; contributor identity and contribution roles remain semantic data. The reusable `index` module is recommended and enabled by default for edited collections; remove it through the project semantic-module configuration only when the title does not need an index.
'''
    if profile == "poetry":
        readme += '''
## Poetry semantics

This project uses stable stanza and verse-line identifiers from the `verse-structure` semantic module. Indentation, hanging continuation, stanza spacing, and display numbering belong to the `poetry` profile; semantic line identity belongs in title-owned source. Indexing is optional for poetry: activate the reusable `index` module for large collections, selected/collected poems, or editions that need thematic/name navigation.
'''
    if profile == "drama":
        readme += '''
## Drama semantic modules

This project uses stable speaker IDs, speech and stage-direction semantics, act/scene structure, and an optional dramatic-line locator namespace. Presentation belongs to the `drama` profile; semantic IDs belong in title-owned source.
'''
    if profile == "bilingual-edition":
        readme += '''
## Bilingual / parallel-text semantics

This project uses stable source/target segment IDs and explicit alignment IDs from the `parallel-text` semantic module. Choose presentation in `config/bilingual-layout.json`; supported modes include parallel columns, facing pages, sequential blocks, source-dominant, and target-dominant layouts. Do not encode alignment by page position or manual column formatting.
'''
    (dest / "README.md").write_text(readme, encoding="utf-8")

    security = '''# Project Security Notes

- Treat unpublished source and proofs as confidential publishing assets.
- Keep this project in private storage unless the manuscript is intended to be public.
- Generated proofs belong under `build/proofs/`; publication releases belong under `release/`. Both are generated artifacts and are ignored by Git.
- Do not put passwords, API tokens, private keys, or credentials in `book.yml` or source files.
- PSE builds with LuaLaTeX `--no-shell-escape` by default.
- If a proof is shared externally, prefer `pse proof --recipient ...` so the artifact receives a recipient-specific proof ID and provenance manifest.
'''
    (dest / "SECURITY.md").write_text(security, encoding="utf-8")

def cmd_new(args: argparse.Namespace) -> int:
    runtime = _find_runtime(Path.cwd())
    available = {p["id"]: p for p in _available_profiles(runtime.root, generator_only=True)}
    if args.profile not in available:
        raise SystemExit("Unsupported profile. Supported profiles: " + ", ".join(sorted(available)))
    profile_manifest = available[args.profile]

    interactive = not args.non_interactive
    title = args.title or (_prompt("Book title") if interactive else "")
    author = args.author or (_prompt("Author/editor") if interactive else "")
    language = args.language or (_prompt("Language", "en") if interactive else "")
    year_raw = str(args.publication_year or (_prompt("Publication year", str(datetime.now().year)) if interactive else ""))
    subtitle = args.subtitle or (_prompt("Subtitle", "") if interactive else "")
    series = args.series or (_prompt("Series", "") if interactive else "")

    if not title or not author or not language or not year_raw:
        raise SystemExit("title, author, language, and publication year are required.")
    try:
        year = int(year_raw)
    except ValueError as exc:
        raise SystemExit("publication year must be a four-digit integer.") from exc
    if not 1000 <= year <= 9999:
        raise SystemExit("publication year must be a four-digit integer.")

    slug = _slugify(args.slug or title)
    dest = _safe_project_destination(Path(args.parent or "."), slug)
    dest.mkdir(parents=True, exist_ok=True)
    _write_new_project(dest, title=title, author=author, language=language, publication_year=year,
                       subtitle=subtitle, series=series, width_mm=args.width_mm, height_mm=args.height_mm, profile=args.profile)
    generated_meta = _load_metadata(dest / "book.yml")
    _validate_profile_metadata(generated_meta, profile_manifest)
    print(f"created: {dest}")
    print(f"profile: {args.profile}")
    print("next: pse build <project> && pse check <project>")
    return 0



def cmd_semantic_ir(args: argparse.Namespace) -> int:
    project=_load_project(args.project)
    nodes,errors=parse_files(_project_tex_sources(project),project.root)
    payload={
        "schema_version":"1.0",
        "project":str(project.root),
        "nodes":[{"kind":n.kind,"name":n.name,"args":list(n.args),"location":loc_dict(n.loc)} for n in nodes],
        "errors":[{"code":getattr(e,"code","parse_error"),"message":e.message,"location":loc_dict(e.loc)} for e in errors],
    }
    text=json.dumps(payload,ensure_ascii=False,indent=2)
    if args.output:
        out=Path(args.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(text+"\n",encoding="utf-8"); print(f"semantic-ir: {out}")
    else:
        print(text)
    return 1 if errors else 0

def cmd_build(args: argparse.Namespace) -> int:
    project = _load_project(args.project)
    metadata = _load_metadata(project.metadata_path)
    generated = _write_generated_metadata(project, metadata)
    modules_file = _write_generated_modules(project, metadata)
    print(f"metadata: {generated.relative_to(project.root)}")
    print(f"modules: {modules_file.relative_to(project.root)}")
    _run_lualatex(project, passes=2)
    if not project.output_pdf.exists():
        raise SystemExit("Build completed without expected output PDF.")
    print(f"built: {project.output_pdf}")
    return 0


def _scan_log(log_text: str) -> dict[str, Any]:
    def count(pattern: str, flags: int = 0) -> int:
        return len(re.findall(pattern, log_text, flags))
    return {
        "missing_glyphs": count(r"Missing character:", re.I),
        "undefined_references": count(r"undefined references?", re.I),
        "undefined_citations": count(r"undefined citations?", re.I),
        "overfull_hbox": count(r"Overfull \\hbox"),
        "overfull_vbox": count(r"Overfull \\vbox"),
        "underfull_hbox": count(r"Underfull \\hbox"),
        "underfull_vbox": count(r"Underfull \\vbox"),
        "font_substitution": count(r"font.*substitut", re.I),
        "hyperref_warnings": count(r"Package hyperref Warning", re.I),
    }


def _pdf_geometry_mm(pdf: Path) -> tuple[float, float, int]:
    reader = PdfReader(str(pdf))
    first = reader.pages[0]
    box = first.mediabox
    pt_to_mm = 25.4 / 72.0
    width = float(box.width) * pt_to_mm
    height = float(box.height) * pt_to_mm
    return width, height, len(reader.pages)


def _qa_findings_from_build(project: Project, metadata: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    metrics: dict[str, Any] = {}
    if not project.output_pdf.exists():
        findings.append(Finding("output_pdf_missing", "error", "Expected output PDF is missing.").as_dict())
    log = project.build_dir / "book.log"
    if not log.exists():
        findings.append(Finding("build_log_missing", "error", "Expected LuaLaTeX build log is missing.").as_dict())
    else:
        log_metrics = _scan_log(log.read_text(encoding="utf-8", errors="replace"))
        metrics["latex"] = log_metrics
        if log_metrics.get("missing_glyphs", 0):
            findings.append(Finding("missing_glyphs", "error", "LuaLaTeX reported missing glyphs.", count=log_metrics["missing_glyphs"]).as_dict())
        if log_metrics.get("undefined_references", 0) or log_metrics.get("undefined_citations", 0):
            findings.append(Finding("undefined_references_or_citations", "error", "Undefined references or citations remain after the build.", count=log_metrics.get("undefined_references", 0) + log_metrics.get("undefined_citations", 0)).as_dict())
        severity = {
            "overfull_hbox": "review",
            "overfull_vbox": "review",
            "underfull_hbox": "warning",
            "underfull_vbox": "warning",
            "font_substitution": "review",
            "hyperref_warnings": "warning",
        }
        for key, sev in severity.items():
            count = int(log_metrics.get(key, 0))
            if count:
                findings.append(Finding(key, sev, f"LuaLaTeX reported {key.replace('_', ' ')}.", count=count).as_dict())
    if project.output_pdf.exists():
        width, height, pages = _pdf_geometry_mm(project.output_pdf)
        metrics["pdf"] = {"width_mm": round(width, 3), "height_mm": round(height, 3), "pages": pages}
        page = metadata.get("page", {}) or {}
        expected_w = float(page.get("width_mm", 126))
        expected_h = float(page.get("height_mm", 198))
        dw, dh = abs(width - expected_w), abs(height - expected_h)
        metrics["pdf"]["geometry_drift_mm"] = {"width": round(dw, 3), "height": round(dh, 3)}
        if dw > 0.5 or dh > 0.5:
            findings.append(Finding("incorrect_page_geometry", "error", "PDF page geometry differs materially from book.yml.", data={"expected_width_mm": expected_w, "expected_height_mm": expected_h, "actual_width_mm": round(width, 3), "actual_height_mm": round(height, 3)}).as_dict())
    return findings, metrics


def cmd_check(args: argparse.Namespace) -> int:
    project = _load_project(args.project)
    metadata = _load_metadata(project.metadata_path)
    findings, metrics = _qa_findings_from_build(project, metadata)
    scholarly_findings, scholarly_metrics = _scholarly_source_qa(project)
    findings.extend(scholarly_findings)
    if scholarly_metrics:
        metrics["scholarly"] = scholarly_metrics
    drama_findings, drama_metrics = _drama_source_qa(project)
    findings.extend(drama_findings)
    if drama_metrics:
        metrics["drama"] = drama_metrics

    parallel_findings, parallel_metrics = _parallel_text_source_qa(project)
    findings.extend(parallel_findings)
    if parallel_metrics:
        metrics["parallel_text"] = parallel_metrics

    locator_findings, locator_metrics = _locator_orchestration_qa(project)
    findings.extend(locator_findings)
    if locator_metrics:
        metrics["locator_orchestration"] = locator_metrics

    presentation_findings, presentation_metrics = _presentation_system_qa(project)
    findings.extend(presentation_findings)
    if presentation_metrics:
        metrics["presentation_system"] = presentation_metrics

    bilingual_findings, bilingual_metrics = _bilingual_layout_qa(project)
    findings.extend(bilingual_findings)
    if bilingual_metrics:
        metrics["bilingual_layout"] = bilingual_metrics

    if getattr(args, "baseline", None) and project.output_pdf.exists():
        baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        expected_pages = baseline.get("pages")
        actual_pages = metrics.get("pdf", {}).get("pages")
        if isinstance(expected_pages, int) and isinstance(actual_pages, int):
            delta = actual_pages - expected_pages
            metrics.setdefault("baseline", {})["page_count"] = {"expected": expected_pages, "actual": actual_pages, "delta": delta}
            if delta:
                findings.append(Finding("page_count_drift", "review", "Page count differs from the approved QA baseline.", data={"expected": expected_pages, "actual": actual_pages, "delta": delta}).as_dict())

    summary = _qa_summarize(findings)
    report: dict[str, Any] = {
        "schema_version": "0.2",
        "pse_version": VERSION,
        "project": str(project.root),
        "status": "fail" if summary["error"] else ("review" if summary["review"] else ("warn" if summary["warning"] else "pass")),
        "review_required": bool(summary["review"]),
        "findings": findings,
        "summary": summary,
        "metrics": metrics,
        # Compatibility fields retained during the alpha transition.
        "hard_failures": [f["code"] for f in findings if f["severity"] == "error"],
        "warnings": [{"code": f["code"], **({"count": f["count"]} if "count" in f else {})} for f in findings if f["severity"] in {"warning", "review"}],
    }
    out = project.build_dir / "qa-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if getattr(args, "human", False):
        for finding in findings:
            print(_format_finding_line(finding))
        print(f"summary: errors={summary['error']} warnings={summary['warning']} reviews={summary['review']} info={summary['info']}")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if summary["error"] else 0


def cmd_visual_check(args: argparse.Namespace) -> int:
    project = _load_project(args.project)
    if not project.output_pdf.exists():
        raise SystemExit("Build the project before visual comparison.")
    baseline_dir = Path(args.baseline_dir).resolve()
    manifest = Path(args.manifest).resolve() if args.manifest else baseline_dir / "baseline-manifest.json"
    output_dir = project.build_dir / "visual-regression"
    report = _visual_check(project.output_pdf, baseline_dir, manifest, output_dir, review_threshold=args.review_threshold)
    out = output_dir / "visual-report.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["summary"]["error"] else 0



def _sha256(path: Path) -> str:
    return sha256_file(path)


def _git_revision(repo_root: Path) -> str | None:
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo_root, text=True, capture_output=True, timeout=5)
        if proc.returncode == 0:
            return proc.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return None


def _safe_filename_part(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    value = value.strip("-._")
    return value[:80] or "proof"


def cmd_proof(args: argparse.Namespace) -> int:
    project = _load_project(args.project)
    metadata = _load_metadata(project.metadata_path)
    _write_generated_metadata(project, metadata)
    _write_generated_modules(project, metadata)
    recipient = args.recipient.strip()
    if not recipient:
        raise SystemExit("--recipient must not be empty.")
    proof_id = args.proof_id or ("PSE-" + secrets.token_hex(4).upper())
    if not re.fullmatch(r"[A-Za-z0-9._-]{4,64}", proof_id):
        raise SystemExit("--proof-id must use 4–64 ASCII letters, numbers, dot, underscore, or hyphen.")
    proof_control = project.build_dir / "pse-proof.tex"
    proof_control.write_text("\n".join([
        "% Generated by PSE proof pipeline. Do not edit by hand.",
        r"\PSEEnableProofMode",
        rf"\PSESetProofRecipient{{{_tex_escape(recipient)}}}",
        rf"\PSESetProofID{{{_tex_escape(proof_id)}}}",
        rf"\PSESetProofLabel{{{_tex_escape(args.label)}}}",
    ]) + "\n", encoding="utf-8")
    proofs_dir = project.build_dir / "proofs"
    jobname = f"book-proof-{_safe_filename_part(proof_id)}"
    try:
        _run_lualatex(project, passes=2, output_dir=proofs_dir, jobname=jobname)
    finally:
        proof_control.unlink(missing_ok=True)
    pdf = proofs_dir / f"{jobname}.pdf"
    if not pdf.exists():
        raise SystemExit("Proof build completed without expected PDF.")
    manifest = {
        "schema_version": "0.1",
        "artifact_type": "recipient_proof",
        "pse_version": VERSION,
        "proof_id": proof_id,
        "recipient": recipient,
        "recipient_email": args.email or None,
        "watermark_policy": "visible-recipient-watermark-v0.1",
        "project_revision": _git_revision(project.root),
        "framework_revision": _git_revision(project.repo_root),
        "runtime_source": project.runtime_source,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "pdf": pdf.name,
        "sha256": _sha256(pdf),
        "security_note": "Watermarking provides deterrence and traceability, not unremovable DRM.",
    }
    manifest_path = proofs_dir / f"{jobname}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"proof: {pdf}")
    print(f"manifest: {manifest_path}")
    print(f"proof_id: {proof_id}")
    return 0



def _git_state(project_root: Path) -> dict[str, Any]:
    try:
        rev = subprocess.run(["git", "rev-parse", "HEAD"], cwd=project_root, text=True, capture_output=True, timeout=5)
        if rev.returncode != 0:
            return {"available": False, "revision": None, "dirty": None}
        status = subprocess.run(["git", "status", "--porcelain"], cwd=project_root, text=True, capture_output=True, timeout=5)
        dirty = bool(status.stdout.strip()) if status.returncode == 0 else None
        epoch = subprocess.run(["git", "log", "-1", "--format=%ct"], cwd=project_root, text=True, capture_output=True, timeout=5)
        source_epoch = int(epoch.stdout.strip()) if epoch.returncode == 0 and epoch.stdout.strip().isdigit() else None
        return {"available": True, "revision": rev.stdout.strip(), "dirty": dirty, "source_date_epoch": source_epoch}
    except (OSError, subprocess.SubprocessError, ValueError):
        return {"available": False, "revision": None, "dirty": None}


def _default_source_date_epoch(project: Project, metadata: dict[str, Any]) -> int:
    state = _git_state(project.root)
    if state.get("source_date_epoch"):
        return int(state["source_date_epoch"])
    # Stable fallback for projects without Git: UTC midnight on 1 January of publication year.
    return int(datetime(int(metadata["publication_year"]), 1, 1, tzinfo=timezone.utc).timestamp())


def _release_attribution_evidence(project: Project) -> dict[str, Any]:
    marker = "PSE-ATTRIBUTION-BANNER: rendered"
    logs = sorted(project.build_dir.glob("lualatex-pass-*.stdout.log"))
    rendered = any(marker in path.read_text(encoding="utf-8", errors="replace") for path in logs)
    asset = project.repo_root / "core" / "pse-attribution-banner.png"
    return {
        "required": True,
        "rendered": rendered,
        "placement": "publication-or-colophon-page",
        "asset": "core/pse-attribution-banner.png",
        "asset_sha256": _sha256(asset) if asset.is_file() else None,
        "verification": "final-build-log-marker",
    }


def _release_qa(project: Project, metadata: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    findings, metrics = _qa_findings_from_build(project, metadata)
    scholarly_findings, scholarly_metrics = _scholarly_source_qa(project)
    findings.extend(scholarly_findings)
    if scholarly_metrics:
        metrics["scholarly"] = scholarly_metrics
    drama_findings, drama_metrics = _drama_source_qa(project)
    findings.extend(drama_findings)
    if drama_metrics:
        metrics["drama"] = drama_metrics
    parallel_findings, parallel_metrics = _parallel_text_source_qa(project)
    findings.extend(parallel_findings)
    if parallel_metrics:
        metrics["parallel_text"] = parallel_metrics
    bilingual_findings, bilingual_metrics = _bilingual_layout_qa(project)
    findings.extend(bilingual_findings)
    if bilingual_metrics:
        metrics["bilingual_layout"] = bilingual_metrics
    state = _git_state(project.root)
    metrics["project_git"] = state
    if state.get("available") and state.get("dirty") is True:
        findings.append(Finding("dirty_working_tree", "review", "Project working tree contains uncommitted changes; release provenance will record this state.").as_dict())
    elif not state.get("available"):
        findings.append(Finding("git_state_unavailable", "info", "Project is not a Git working tree or Git is unavailable; revision provenance is limited.").as_dict())
    return findings, metrics


def _release_output_inspection_findings(report: dict[str, Any]) -> list[dict[str, Any]]:
    """Translate the narrow machine-verifiable inspection baseline into release policy.

    Accessibility-review items remain evidence only and never become automatic
    certification or release blockers merely because the PDF is untagged.
    """
    findings: list[dict[str, Any]] = []
    by_name = {item.get("name"): item for item in report.get("checks", [])}

    for name, code, message in [
        ("pdf_readable", "release_pdf_inspection_unreadable", "Release PDF must be machine-readable by the output inspector."),
        ("title_metadata", "release_pdf_title_metadata_missing", "Release PDF must contain title metadata."),
        ("author_metadata", "release_pdf_author_metadata_missing", "Release PDF must contain author/editor metadata."),
        ("document_language", "release_pdf_language_metadata_invalid", "Release PDF must contain the expected document-level language metadata."),
    ]:
        item = by_name.get(name)
        if not item or item.get("status") != "pass":
            findings.append(Finding(code, "error", message, data={"inspection": item}).as_dict())

    text_item = by_name.get("text_extractability")
    if not text_item or text_item.get("status") != "pass":
        findings.append(Finding(
            "release_pdf_text_extractability_review",
            "review",
            "Release PDF did not pass the lightweight text-extractability baseline; inspect Unicode mapping and reading output before release.",
            data={"inspection": text_item},
        ).as_dict())
    return findings


def cmd_release(args: argparse.Namespace) -> int:
    project = _load_project(args.project)
    metadata = _load_metadata(project.metadata_path)

    # Release is always rebuilt from a clean generated boundary. Recipient proofs and old
    # build artefacts must not influence the publication artefact.
    if project.build_dir.exists():
        shutil.rmtree(project.build_dir)
    _write_generated_metadata(project, metadata)
    _write_generated_modules(project, metadata)
    epoch = int(args.source_date_epoch) if args.source_date_epoch is not None else _default_source_date_epoch(project, metadata)

    _run_lualatex(project, passes=2, source_date_epoch=epoch)
    if not project.output_pdf.exists():
        raise SystemExit("Release build completed without expected output PDF.")
    first_hash = _sha256(project.output_pdf)
    first_copy = project.build_dir / "book.release-first.pdf"
    shutil.copy2(project.output_pdf, first_copy)

    # A second clean compile with the same SOURCE_DATE_EPOCH tests byte-level reproducibility.
    for child in project.build_dir.iterdir():
        if child.name in {"pse-metadata.tex", "pse-modules.tex", "pse-bilingual-layout.tex", "pse-locator-orchestration.tex", "book.release-first.pdf"}:
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    _run_lualatex(project, passes=2, source_date_epoch=epoch)
    second_hash = _sha256(project.output_pdf)
    reproducible = first_hash == second_hash
    first_copy.unlink(missing_ok=True)

    attribution = _release_attribution_evidence(project)
    if not attribution["rendered"] or not attribution["asset_sha256"]:
        raise SystemExit("Release blocked: mandatory PSE attribution banner did not render on the publication/copyright page or colophon.")

    output_inspection = inspect_pdf(project.output_pdf, expected_language=str(metadata.get("language") or ""))
    inspection_findings = _release_output_inspection_findings(output_inspection)

    findings, metrics = _release_qa(project, metadata)
    findings.extend(inspection_findings)
    metrics["attribution"] = attribution
    metrics["output_inspection"] = output_inspection
    metrics["reproducibility"] = {
        "source_date_epoch": epoch,
        "first_sha256": first_hash,
        "second_sha256": second_hash,
        "byte_identical": reproducible,
    }
    if not reproducible:
        findings.append(Finding("pdf_not_byte_reproducible", "review", "Two clean release builds with the same SOURCE_DATE_EPOCH produced different PDF bytes.").as_dict())

    summary = _qa_summarize(findings)
    if summary["error"]:
        raise SystemExit("Release blocked: machine QA contains error-severity findings. Run `pse check` and resolve them first.")
    if summary["review"] and not args.acknowledge_review:
        codes = ", ".join(f["code"] for f in findings if f["severity"] == "review")
        raise SystemExit("Release requires human acknowledgement for review findings: " + codes + ". Re-run with --acknowledge-review after review.")

    created = datetime.now(timezone.utc)
    release_id = args.release_id or ("PSE-R" + created.strftime("%Y%m%dT%H%M%SZ") + "-" + second_hash[:8].upper())
    if not re.fullmatch(r"[A-Za-z0-9._-]{6,96}", release_id):
        raise SystemExit("--release-id must use 6–96 ASCII letters, numbers, dot, underscore, or hyphen.")
    release_root = project.root / "release" / _safe_filename_part(release_id)
    if release_root.exists() and any(release_root.iterdir()):
        raise SystemExit(f"Release destination already exists and is not empty: {release_root}")
    release_root.mkdir(parents=True, exist_ok=True)

    slug = _slugify(str(metadata["title"]))
    pdf_name = f"{slug}-{_safe_filename_part(release_id)}.pdf"
    release_pdf = release_root / pdf_name
    shutil.copy2(project.output_pdf, release_pdf)
    release_pdf_hash = _sha256(release_pdf)
    release_inspection = inspect_pdf(release_pdf, expected_language=str(metadata.get("language") or ""))
    if release_inspection.get("pdf_sha256") != release_pdf_hash:
        raise SystemExit("Release blocked: output-inspection evidence does not bind to the final release PDF hash.")
    width, height, pages = _pdf_geometry_mm(release_pdf)
    git_state = _git_state(project.root)
    manifest = {
        "schema_version": RELEASE_MANIFEST_SCHEMA_VERSION,
        "artifact_type": "publication_release",
        "release_id": release_id,
        "created_utc": created.isoformat(),
        "pse_version": VERSION,
        "runtime_source": project.runtime_source,
        "project_revision": git_state.get("revision"),
        "project_dirty": git_state.get("dirty"),
        "framework_revision": _git_revision(project.repo_root),
        "source_date_epoch": epoch,
        "qa": {"summary": summary, "review_acknowledged": bool(args.acknowledge_review), "findings": findings},
        "reproducibility": metrics["reproducibility"],
        "attribution": attribution,
        "output_inspection": {
            "file": "output-inspection.json",
            "schema_version": release_inspection.get("schema_version"),
            "sha256": None,
            "bound_pdf_sha256": release_pdf_hash,
            "policy": dict(RELEASE_INSPECTION_POLICY),
        },
        "pdf": {
            "file": pdf_name,
            "sha256": release_pdf_hash,
            "pages": pages,
            "width_mm": round(width, 3),
            "height_mm": round(height, 3),
        },
        "signing": {"status": "unsigned", "note": "Digital-signature/enterprise PKI integration is an extension point; not required by the core release contract."},
    }
    inspection_path = release_root / "output-inspection.json"
    inspection_path.write_text(json.dumps(release_inspection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest["output_inspection"]["sha256"] = _sha256(inspection_path)
    inspection_contract_errors = validate_output_inspection(release_inspection)
    manifest_contract_errors = validate_release_manifest(manifest)
    binding_contract_errors = validate_release_binding(manifest, release_inspection)
    contract_errors = inspection_contract_errors + manifest_contract_errors + binding_contract_errors
    if contract_errors:
        raise SystemExit("Release blocked: generated release evidence violates the public contract: " + "; ".join(contract_errors))
    manifest_path = release_root / "release-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    qa_path = release_root / "qa-report.json"
    qa_path.write_text(json.dumps({"schema_version": "0.2", "status": "review" if summary["review"] else ("warn" if summary["warning"] else "pass"), "summary": summary, "findings": findings, "metrics": metrics}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    sums = release_root / "SHA256SUMS.txt"
    write_checksum_file(sums, [release_pdf, manifest_path, qa_path, inspection_path])
    print(f"release: {release_root}")
    print(f"pdf: {release_pdf}")
    print(f"manifest: {manifest_path}")
    print(f"release_id: {release_id}")
    print(f"byte_reproducible: {str(reproducible).lower()}")
    return 0


def cmd_verify_release(args: argparse.Namespace) -> int:
    release_root = Path(args.release_dir).resolve()
    manifest_path = release_root / "release-manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Missing release manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid release manifest JSON: {exc}") from exc

    findings: list[dict[str, Any]] = []
    schema_version = manifest.get("schema_version") if isinstance(manifest, dict) else None
    contract_errors = validate_release_manifest(manifest)
    for message in contract_errors:
        findings.append(Finding("release_manifest_contract_invalid", "error", message).as_dict())

    if schema_version == "0.1":
        findings.append(Finding(
            "legacy_release_manifest_schema",
            "warning",
            "Release manifest schema 0.1 is supported for legacy verification only. Output-inspection evidence is not required and cannot be inferred retroactively.",
        ).as_dict())
    elif schema_version not in SUPPORTED_RELEASE_MANIFEST_SCHEMAS:
        # Do not trust artifact paths from an unsupported manifest contract.
        summary = _qa_summarize(findings)
        report = {"schema_version": "0.2", "release_id": manifest.get("release_id") if isinstance(manifest, dict) else None, "manifest_schema_version": schema_version, "compatibility": release_schema_compatibility(schema_version), "status": "fail", "summary": summary, "findings": findings}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 1

    pdf_meta = manifest.get("pdf", {}) if isinstance(manifest, dict) else {}
    pdf_name = str(pdf_meta.get("file", "")) if isinstance(pdf_meta, dict) else ""
    pdf = release_root / pdf_name if pdf_name else None
    if pdf is None or not pdf.is_file():
        findings.append(Finding("release_pdf_missing", "error", "Release PDF named by the manifest is missing.").as_dict())
    else:
        actual = _sha256(pdf)
        expected = str(pdf_meta.get("sha256", ""))
        if actual != expected:
            findings.append(Finding("release_pdf_checksum_mismatch", "error", "Release PDF SHA-256 does not match the manifest.", data={"expected": expected, "actual": actual}).as_dict())
        try:
            width, height, pages = _pdf_geometry_mm(pdf)
            if pages != pdf_meta.get("pages") or abs(width - float(pdf_meta.get("width_mm", width))) > 0.5 or abs(height - float(pdf_meta.get("height_mm", height))) > 0.5:
                findings.append(Finding("release_pdf_structure_mismatch", "error", "Release PDF page count or geometry differs from the manifest.").as_dict())
        except Exception as exc:
            findings.append(Finding("release_pdf_unreadable", "error", f"Cannot inspect release PDF: {exc}").as_dict())

    if schema_version == "0.2":
        inspection_meta = manifest.get("output_inspection", {})
        inspection_name = str(inspection_meta.get("file", "")) if isinstance(inspection_meta, dict) else ""
        inspection_path = release_root / inspection_name if inspection_name else None
        if not inspection_name or inspection_path is None or not inspection_path.is_file():
            findings.append(Finding("release_output_inspection_missing", "error", "Release output-inspection evidence is missing.").as_dict())
        else:
            expected_inspection_hash = str(inspection_meta.get("sha256", ""))
            actual_inspection_hash = _sha256(inspection_path)
            if not expected_inspection_hash or actual_inspection_hash != expected_inspection_hash:
                findings.append(Finding("release_output_inspection_checksum_mismatch", "error", "Output-inspection evidence SHA-256 does not match the manifest.").as_dict())
            try:
                inspection_payload = json.loads(inspection_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                findings.append(Finding("release_output_inspection_invalid", "error", f"Cannot read output-inspection evidence: {exc}").as_dict())
            else:
                for message in validate_output_inspection(inspection_payload):
                    findings.append(Finding("release_output_inspection_contract_invalid", "error", message).as_dict())
                for message in validate_release_binding(manifest, inspection_payload):
                    findings.append(Finding("release_output_inspection_pdf_binding_mismatch", "error", message).as_dict())

    for checksum_finding in verify_checksum_file(release_root / "SHA256SUMS.txt"):
        findings.append(Finding(checksum_finding["code"], "error", checksum_finding["message"]).as_dict())

    summary = _qa_summarize(findings)
    report = {
        "schema_version": "0.2",
        "release_id": manifest.get("release_id") if isinstance(manifest, dict) else None,
        "manifest_schema_version": schema_version,
        "compatibility": release_schema_compatibility(schema_version),
        "status": "fail" if summary["error"] else "pass",
        "summary": summary,
        "findings": findings,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if summary["error"] else 0


def cmd_contracts(args: argparse.Namespace) -> int:
    runtime = _find_runtime(Path.cwd())
    payload = installed_contract_surface(runtime.root, runtime_source=runtime.source, framework_version=VERSION)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print(f"PSE installed contract surface ({VERSION})")
    print(f"runtime: {runtime.source} - {runtime.root}")
    for contract in payload["contracts"]:
        current = contract["current_schema_version"]
        verified = ", ".join(contract["verification_schema_versions"])
        legacy = ", ".join(contract["legacy_verification_schema_versions"]) or "none"
        installed = "yes" if contract["installed"] else "NO"
        print(f"- {contract['id']}: current={current}; verify={verified}; legacy={legacy}; schema-installed={installed}")
        print(f"  schema: {contract['schema_path']}")
    return 0 if all(c["installed"] for c in payload["contracts"]) else 1


def _verify_release_capture(release_root: Path) -> tuple[str, int]:
    """Run the existing verifier logic without mutating the release directory."""
    import contextlib
    import io
    buf = io.StringIO()
    namespace = argparse.Namespace(release_dir=str(release_root))
    with contextlib.redirect_stdout(buf):
        rc = cmd_verify_release(namespace)
    return buf.getvalue(), int(rc)


def cmd_release_migration(args: argparse.Namespace) -> int:
    release_root = Path(args.release_dir).resolve()
    manifest_path = release_root / "release-manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Missing release manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid release manifest JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise SystemExit("Release manifest must be a JSON object.")

    verify_text, verify_rc = _verify_release_capture(release_root)
    try:
        verify_report = json.loads(verify_text)
        verification_status = str(verify_report.get("status") or ("pass" if verify_rc == 0 else "fail"))
    except json.JSONDecodeError:
        verification_status = "pass" if verify_rc == 0 else "fail"

    assessment = release_migration_assessment(release_root, manifest, verification_status=verification_status)
    if args.output:
        output = Path(args.output).expanduser().resolve()
        try:
            output.relative_to(release_root)
        except ValueError:
            pass
        else:
            raise SystemExit("Migration assessment output must be outside the historical release directory; PSE does not mutate release artifacts in place.")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(assessment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.human:
        print(f"PSE release migration assessment: {release_root}")
        print(f"source schema: {assessment['source_manifest_schema_version']}")
        print(f"verification: {assessment['verification_status']}")
        print(f"migration status: {assessment['migration_status']}")
        print("historical artifact mutated: false")
        print(f"recommended action: {assessment['recommended_action']}")
        if args.output:
            print(f"assessment: {Path(args.output).expanduser().resolve()}")
    else:
        print(json.dumps(assessment, ensure_ascii=False, indent=2))
    return 1 if assessment["compatibility"]["status"] == "unsupported" or verification_status == "fail" else 0



def cmd_audit_release(args: argparse.Namespace) -> int:
    release_root = Path(args.release_dir).resolve()
    manifest_path = release_root / "release-manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Missing release manifest: {manifest_path}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid release manifest JSON: {exc}") from exc
    if not isinstance(manifest, dict):
        raise SystemExit("Release manifest must be a JSON object.")

    verify_text, verify_rc = _verify_release_capture(release_root)
    try:
        verify_report = json.loads(verify_text)
    except json.JSONDecodeError:
        verify_report = {"status": "fail" if verify_rc else "pass", "raw_output": verify_text.strip()}
    record = release_audit_record(
        release_root,
        manifest,
        verify_report,
        framework_version=VERSION,
        generated_utc=datetime.now(timezone.utc).isoformat(),
    )
    contract_errors = validate_release_audit_record(record)
    if contract_errors:
        raise SystemExit("Audit record generation violated its public contract: " + "; ".join(contract_errors))

    if args.output:
        output = Path(args.output).expanduser().resolve()
        try:
            output.relative_to(release_root)
        except ValueError:
            pass
        else:
            raise SystemExit("Audit record output must be outside the release directory; historical release artifacts remain immutable.")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.human:
        print(f"PSE release audit: {release_root}")
        print(f"release id: {record['source_release_id']}")
        print(f"manifest schema: {record['source_manifest_schema_version']}")
        print(f"compatibility: {record['compatibility']['status']}")
        print(f"verification: {record['verification'].get('status')}")
        print(f"audit status: {record['audit_status']}")
        print(f"release fingerprint: {record.get('release_fingerprint')}")
        print("historical artifact mutated: false")
        if args.output:
            print(f"audit record: {Path(args.output).expanduser().resolve()}")
    else:
        print(json.dumps(record, ensure_ascii=False, indent=2))
    return 1 if record["audit_status"] == "fail" else 0

def _command_version(executable: str, *args: str) -> tuple[int, str]:
    try:
        proc = subprocess.run([executable, *args], text=True, capture_output=True, timeout=15)
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, str(exc)
    text = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, text.strip()


def _doctor_deep_compile(runtime: RuntimeInfo) -> tuple[bool, str]:
    lualatex = shutil.which("lualatex")
    if not lualatex:
        return False, "LuaLaTeX unavailable"
    with tempfile.TemporaryDirectory(prefix="pse-doctor-") as td:
        root = Path(td)
        (root / "build").mkdir()
        (root / "build" / "pse-metadata.tex").write_text("\n".join([
            r"\PSESetTitle{PSE Doctor}",
            r"\PSESetAuthor{Runtime Test}",
            r"\PSESetLanguage{en}",
            r"\PSESetPublicationYear{2027}",
            r"\PSESetSubtitle{}",
            r"\PSESetSeries{}",
            r"\PSESetPageWidth{126mm}",
            r"\PSESetPageHeight{198mm}",
        ]) + "\n", encoding="utf-8")
        tex = r'''\documentclass{book}
\usepackage{pse-core}
\usepackage{pse-profile-basic-book}
\begin{document}
PSE doctor secure-build test.
\immediate\write18{echo PSE_SECURITY_SENTINEL > pse-doctor-sentinel.txt}
\end{document}
'''
        (root / "main.tex").write_text(tex, encoding="utf-8")
        env = os.environ.copy()
        env["TEXINPUTS"] = os.pathsep.join([
            str((runtime.root / "core").resolve()),
            str((runtime.root / "profiles" / "basic-book").resolve()),
        ]) + os.pathsep + env.get("TEXINPUTS", "")
        proc = subprocess.run([
            lualatex, "--no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
            "-output-directory=build", "main.tex"
        ], cwd=root, env=env, text=True, capture_output=True)
        if proc.returncode != 0 or not (root / "build" / "main.pdf").exists():
            tail = "\n".join((proc.stdout + "\n" + proc.stderr).splitlines()[-12:])
            return False, "secure test compile failed: " + tail
        if (root / "pse-doctor-sentinel.txt").exists():
            return False, "shell command executed despite --no-shell-escape"
        return True, "secure LuaLaTeX test build passed; shell escape remained disabled"


def _doctor_report(deep: bool = False) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []

    def add(name: str, status: str, detail: str, *, required: bool = True) -> None:
        checks.append({"name": name, "status": status, "required": required, "detail": detail})

    py_ok = sys.version_info >= (3, 11)
    add("python", "pass" if py_ok else "fail", f"{platform.python_implementation()} {platform.python_version()} ({sys.executable})")

    add("pse_cli", "pass", f"PSE CLI {VERSION}")
    try:
        dist_version = importlib_metadata.version("publication-systems-engineering")
        normalized_cli = VERSION.replace("-alpha", "a0")
        dist_status = "pass" if dist_version in {normalized_cli, "0.6.0a0"} else "warn"
        add("python_distribution", dist_status, f"installed distribution {dist_version}", required=False)
    except importlib_metadata.PackageNotFoundError:
        add("python_distribution", "warn", "not installed as a Python distribution; source-checkout execution", required=False)

    try:
        runtime = _find_runtime(Path.cwd())
        add("runtime_discovery", "pass", f"{runtime.source}: {runtime.root}")
        add("core", "pass" if (runtime.root / "core" / "pse-core.sty").is_file() else "fail", str(runtime.root / "core" / "pse-core.sty"))
        try:
            manifests = _available_profiles(runtime.root)
            for manifest in manifests:
                profile = manifest["id"]
                profile_path = runtime.root / "profiles" / profile / f"pse-profile-{profile}.sty"
                presentation = _load_presentation_manifest(runtime.root, profile)
                add(f"profile_{profile.replace('-', '_')}", "pass", f"{profile_path}; schema={manifest['schema_version']}; preset={presentation['preset']}; capabilities={','.join(manifest['capabilities'])}")
            add("profile_registry", "pass" if manifests else "fail", f"{len(manifests)} validated profile manifest(s)")
        except SystemExit as exc:
            add("profile_registry", "fail", str(exc))
        marker = runtime.root / "runtime" / "pse-runtime.json"
        if marker.is_file():
            try:
                runtime_meta = json.loads(marker.read_text(encoding="utf-8"))
                declared = str(runtime_meta.get("runtime_version", ""))
                add("runtime_manifest", "pass" if declared == VERSION else "warn", f"declared runtime {declared or 'unknown'}", required=False)
            except (OSError, json.JSONDecodeError) as exc:
                add("runtime_manifest", "warn", f"cannot read runtime manifest: {exc}", required=False)
    except SystemExit as exc:
        runtime = None
        add("runtime_discovery", "fail", str(exc))
        add("core", "fail", "core unavailable")

    lua = shutil.which("lualatex")
    if lua:
        rc, version_text = _command_version(lua, "--version")
        first = version_text.splitlines()[0] if version_text else lua
        add("lualatex", "pass" if rc == 0 else "fail", first)
    else:
        add("lualatex", "fail", "LuaLaTeX not found on PATH")

    kpse = shutil.which("kpsewhich")
    if kpse:
        add("kpsewhich", "pass", kpse, required=False)
        packages = ["fontspec.sty", "geometry.sty", "microtype.sty", "hyperref.sty", "xcolor.sty", "etoolbox.sty", "eso-pic.sty", "graphicx.sty", "titlesec.sty", "fancyhdr.sty", "needspace.sty"]
        missing = []
        for package in packages:
            proc = subprocess.run([kpse, package], text=True, capture_output=True)
            if proc.returncode != 0 or not proc.stdout.strip():
                missing.append(package)
        add("tex_packages", "pass" if not missing else "fail", "all required packages found" if not missing else "missing: " + ", ".join(missing))
        font_proc = subprocess.run([kpse, "lmroman10-regular.otf"], text=True, capture_output=True)
        font_ok = font_proc.returncode == 0 and bool(font_proc.stdout.strip())
        add("open_fonts", "pass" if font_ok else "warn", font_proc.stdout.strip() if font_ok else "Latin Modern OTF not located by kpsewhich; verify with a build", required=False)
    else:
        add("kpsewhich", "warn", "kpsewhich not found; TeX package/font preflight is limited", required=False)
        add("tex_packages", "warn", "not checked because kpsewhich is unavailable", required=False)
        add("open_fonts", "warn", "not checked because kpsewhich is unavailable", required=False)

    try:
        with tempfile.NamedTemporaryFile(prefix="pse-doctor-", delete=True) as fh:
            fh.write(b"PSE")
            fh.flush()
        add("temporary_storage", "pass", tempfile.gettempdir())
    except OSError as exc:
        add("temporary_storage", "fail", str(exc))

    add("safe_build_policy", "pass", "PSE invokes LuaLaTeX with --no-shell-escape")
    renderer = shutil.which("pdftoppm")
    add("visual_regression_renderer", "pass" if renderer else "warn", renderer or "pdftoppm not found; ordinary builds work, but visual regression is unavailable", required=False)

    if deep:
        if runtime is None:
            add("deep_secure_build", "fail", "runtime unavailable")
        else:
            ok, detail = _doctor_deep_compile(runtime)
            add("deep_secure_build", "pass" if ok else "fail", detail)

    failures = [c for c in checks if c["status"] == "fail" and c["required"]]
    warnings = [c for c in checks if c["status"] == "warn"]
    return {
        "schema_version": "0.1",
        "pse_version": VERSION,
        "platform": {"system": platform.system(), "release": platform.release(), "machine": platform.machine()},
        "status": "fail" if failures else ("warn" if warnings else "pass"),
        "checks": checks,
        "summary": {"required_failures": len(failures), "warnings": len(warnings)},
    }


def cmd_doctor(args: argparse.Namespace) -> int:
    report = _doctor_report(deep=args.deep)
    requested_profile = getattr(args, "profile", None)
    if requested_profile:
        checks = report["checks"]
        def add(name: str, status: str, detail: str, required: bool = True) -> None:
            checks.append({"name":name,"status":status,"required":required,"detail":detail})
        try:
            runtime=_find_runtime(Path.cwd())
            manifest=_load_profile_manifest(runtime.root, requested_profile)
            add("requested_profile", "pass", f"{requested_profile} {manifest['version']}")
            for module in _profile_modules(runtime.root,manifest):
                add(f"module_{module['id'].replace('-','_')}","pass",module['description'])
                for tool in module.get("build_tools",[]):
                    exe=shutil.which(tool)
                    add(f"tool_{tool}","pass" if exe else "fail",exe or f"{tool} not found on PATH")
                for font in module.get("required_fonts",[]):
                    fc=shutil.which("fc-match")
                    if fc:
                        proc=subprocess.run([fc,font],text=True,capture_output=True)
                        ok=proc.returncode==0 and bool(proc.stdout.strip())
                        add("font_"+re.sub(r"[^a-z0-9]+","_",font.lower()),"pass" if ok else "fail",proc.stdout.strip() if ok else f"{font} not found")
                    else:
                        add("font_"+re.sub(r"[^a-z0-9]+","_",font.lower()),"warn","fc-match unavailable; verify by build",required=False)
        except SystemExit as exc:
            add("requested_profile","fail",str(exc))
        failures=[c for c in checks if c["status"]=="fail" and c["required"]]
        warnings=[c for c in checks if c["status"]=="warn"]
        report["summary"]={"required_failures":len(failures),"warnings":len(warnings)}
        report["status"]="fail" if failures else ("warn" if warnings else "pass")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Publication Systems Engineering doctor — {report['status'].upper()}")
        print(f"Platform: {report['platform']['system']} {report['platform']['release']} ({report['platform']['machine']})")
        for check in report["checks"]:
            mark = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[check["status"]]
            req = "" if check["required"] else " [advisory]"
            print(f"{mark:4} {check['name']}{req}: {check['detail']}")
        if report["status"] == "fail":
            print("Result: installation/runtime is not ready for reliable PSE builds.")
        elif report["status"] == "warn":
            print("Result: core requirements pass; review advisory warnings.")
        else:
            print("Result: runtime is ready.")
    return 1 if report["summary"]["required_failures"] else 0


def cmd_clean(args: argparse.Namespace) -> int:
    project = _load_project(args.project)
    if project.build_dir.exists():
        shutil.rmtree(project.build_dir)
        print(f"removed: {project.build_dir}")
    else:
        print("already clean")
    return 0


def cmd_smoke(args: argparse.Namespace) -> int:
    repo = _find_repo_root(Path(args.project).resolve())
    fixture = repo / "examples" / "synthetic" / "basic-book"
    ns = argparse.Namespace(project=str(fixture))
    cmd_clean(ns)
    cmd_build(ns)
    rc = cmd_check(ns)
    if rc == 0:
        print("smoke regression: PASS")
    return rc



def _run_regression_script(repo: Path, rel: str) -> dict[str, Any]:
    path = repo / rel
    if not path.is_file():
        return {"name": rel, "status": "fail", "returncode": 1, "detail": "script missing"}
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo / "tools") + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run([sys.executable, str(path)], cwd=repo, env=env, text=True, capture_output=True)
    return {"name": rel, "status": "pass" if proc.returncode == 0 else "fail", "returncode": proc.returncode, "stdout": proc.stdout[-12000:], "stderr": proc.stderr[-4000:]}


def cmd_regression(args: argparse.Namespace) -> int:
    runtime = _find_runtime(Path.cwd())
    repo = runtime.root
    if not (repo / "tests" / "regression").is_dir():
        raise SystemExit("Framework regression suite is available from a source checkout, not the minimal installed runtime.")
    scripts = [
        "tests/regression/core_smoke.py",
        "tests/security/security_regression.py",
        "tests/regression/project_generator.py",
        "tests/regression/runtime_bootstrap.py",
        "tests/regression/typography_page_architecture.py",
        "tests/regression/qa_foundation.py",
        "tests/regression/release_engineering.py",
        "tests/regression/profile_expansion.py",
        "tests/regression/profile_contracts.py",
        "tests/regression/scholarly_foundation.py",
        "tests/regression/scholarly_locator_contracts.py",
        "tests/regression/semantic_namespaces.py",
        "tests/regression/drama_semantics.py",
        "tests/regression/drama_profile.py",
        "tests/regression/parallel_text.py",
        "tests/regression/bilingual_profile.py",
        "tests/regression/semantic_parser.py",
    ]
    if args.quick:
        scripts = [scripts[0], scripts[4], scripts[5]]
    results = [_run_regression_script(repo, rel) for rel in scripts]

    visual: dict[str, Any] | None = None
    if not args.no_visual:
        profile_results: dict[str, Any] = {}
        for profile_manifest in _available_profiles(repo, generator_only=True):
            profile = profile_manifest["id"]
            fixture = repo / "tests" / "fixtures" / "profile-books" / profile
            baseline_dir = repo / "tests" / "visual" / "baselines" / profile
            if not fixture.is_dir() or not baseline_dir.is_dir():
                continue
            ns = argparse.Namespace(project=str(fixture))
            cmd_clean(ns)
            cmd_build(ns)
            profile_results[profile] = _visual_check(
                fixture / "build" / "book.pdf", baseline_dir, baseline_dir / "baseline-manifest.json",
                repo / "tests" / "_output" / f"visual-{profile}", review_threshold=args.visual_review_threshold
            )
        summaries=[v.get("summary", {}) for v in profile_results.values()]
        visual={
            "schema_version": "0.2",
            "profiles": profile_results,
            "summary": {
                "error": sum(int(x.get("error",0)) for x in summaries),
                "warning": sum(int(x.get("warning",0)) for x in summaries),
                "review": sum(int(x.get("review",0)) for x in summaries),
                "info": sum(int(x.get("info",0)) for x in summaries),
            },
        }

    failed = [r for r in results if r["status"] == "fail"]
    visual_errors = int((visual or {}).get("summary", {}).get("error", 0))
    visual_reviews = int((visual or {}).get("summary", {}).get("review", 0))
    aggregate = {
        "schema_version": "0.1",
        "pse_version": VERSION,
        "suite": "quick" if args.quick else "full",
        "status": "fail" if failed or visual_errors else ("review" if visual_reviews else "pass"),
        "exit_policy": {"0": "no error-severity regression failures; review findings may remain", "1": "error-severity regression failure", "2": "invocation/configuration error"},
        "results": results,
        "visual": visual,
        "summary": {"scripts": len(results), "script_failures": len(failed), "visual_errors": visual_errors, "visual_reviews": visual_reviews},
    }
    output = Path(args.output).resolve() if args.output else repo / "tests" / "_output" / "regression-report.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(aggregate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(aggregate, ensure_ascii=False, indent=2))
    return 1 if failed or visual_errors else 0

def cmd_profiles(args: argparse.Namespace) -> int:
    runtime=_find_runtime(Path.cwd())
    manifests=_available_profiles(runtime.root, generator_only=bool(args.generator_only))
    if args.json:
        payload={"schema_version": PROFILE_SCHEMA_VERSION, "profiles": manifests}
        if args.presentation:
            payload["presentation_schema_version"] = PRESENTATION_SCHEMA_VERSION
            payload["presentations"] = [_load_presentation_manifest(runtime.root,m["id"]) for m in manifests]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    print("Available PSE profiles")
    for m in manifests:
        caps=", ".join(m["capabilities"])
        print(f"- {m['id']}: {m['description']}")
        print(f"  capabilities: {caps}")
        print(f"  generator_supported: {str(m['generator_supported']).lower()}")
        if args.modules:
            policy=_module_policy(m)
            if not policy:
                print("  module policy: none")
            for status in ("required", "recommended", "optional", "discouraged", "incompatible"):
                mids=[mid + (" [default]" if rule.get("default_enabled") else "") for mid, rule in policy.items() if rule.get("status") == status]
                if mids:
                    print(f"  {status}: {', '.join(mids)}")
        if args.presentation:
            pdesc=_load_presentation_manifest(runtime.root,m["id"])
            print(f"  presentation preset: {pdesc['preset']}")
            print(f"  composition: hierarchy={pdesc['hierarchy']}; metadata={pdesc['publication_unit_metadata']}; grid={pdesc['grid']}; side={pdesc['side_material']}; apparatus={pdesc['apparatus']}; locator={pdesc['locator']}; parallel={pdesc['parallel_text']}")
    return 0



def cmd_modules(args: argparse.Namespace) -> int:
    runtime=_find_runtime(Path.cwd())
    root=runtime.root / "modules"
    manifests=[]
    if root.is_dir():
        for child in sorted(root.iterdir()):
            if child.is_dir() and (child / "module.json").is_file():
                manifests.append(_load_module_manifest(runtime.root, child.name))
    if args.json:
        print(json.dumps({"schema_version": "1.1", "modules": manifests}, ensure_ascii=False, indent=2))
        return 0
    print("Available PSE semantic modules")
    for m in manifests:
        print(f"- {m['id']}: {m['description']}")
        print(f"  capabilities: {', '.join(m['capabilities'])}")
        print(f"  build_tools: {', '.join(m['build_tools']) or 'none'}")
        print(f"  required_fonts: {', '.join(m['required_fonts']) or 'none'}")
    return 0

def cmd_inspect_output(args: argparse.Namespace) -> int:
    target = Path(args.target).resolve()
    if target.is_dir():
        target = target / "build" / "book.pdf"
    report = inspect_pdf(target, expected_language=args.expected_language)
    if args.output:
        Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(render_human(report) if args.human else json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["summary"]["error"] else 0



def cmd_audit_index(args: argparse.Namespace) -> int:
    collection_root = Path(args.collection_dir).resolve()
    if not collection_root.is_dir():
        raise SystemExit(f"Audit collection directory not found: {collection_root}")
    release_roots = sorted(
        child.resolve() for child in collection_root.iterdir()
        if child.is_dir() and (child / "release-manifest.json").is_file()
    )
    if not release_roots:
        raise SystemExit("No immediate child release directories with release-manifest.json were found.")

    records = []
    for release_root in release_roots:
        manifest_path = release_root / "release-manifest.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid release manifest JSON in {release_root.name}: {exc}") from exc
        if not isinstance(manifest, dict):
            raise SystemExit(f"Release manifest must be a JSON object: {manifest_path}")
        verify_text, verify_rc = _verify_release_capture(release_root)
        try:
            verify_report = json.loads(verify_text)
        except json.JSONDecodeError:
            verify_report = {"status": "fail" if verify_rc else "pass", "raw_output": verify_text.strip()}
        record = release_audit_record(
            release_root,
            manifest,
            verify_report,
            framework_version=VERSION,
            generated_utc=datetime.now(timezone.utc).isoformat(),
        )
        contract_errors = validate_release_audit_record(record)
        if contract_errors:
            raise SystemExit(f"Audit record contract failure for {release_root.name}: " + "; ".join(contract_errors))
        records.append(record)

    index = release_audit_index(
        collection_root,
        records,
        framework_version=VERSION,
        generated_utc=datetime.now(timezone.utc).isoformat(),
    )
    contract_errors = validate_release_audit_index(index)
    if contract_errors:
        raise SystemExit("Audit index generation violated its public contract: " + "; ".join(contract_errors))

    if args.output:
        output = Path(args.output).expanduser().resolve()
        for release_root in release_roots:
            try:
                output.relative_to(release_root)
            except ValueError:
                continue
            raise SystemExit("Audit index output must be outside every audited release directory; release artifacts remain immutable.")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.human:
        print(f"PSE release audit index: {collection_root}")
        print(f"releases: {index['release_count']}")
        print(f"batch status: {index['batch_status']}")
        print(f"batch fingerprint: {index['batch_fingerprint']}")
        for entry in index["entries"]:
            print(f"- {entry['source_release_id']}: {entry['audit_status']} {entry['release_fingerprint']}")
        print("historical artifacts mutated: false")
        if args.output:
            print(f"audit index: {Path(args.output).expanduser().resolve()}")
    else:
        print(json.dumps(index, ensure_ascii=False, indent=2))
    return 1 if index["batch_status"] == "fail" else 0




def cmd_verify_audit_record(args: argparse.Namespace) -> int:
    path = Path(args.audit_record).expanduser().resolve()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read audit record: {exc}") from exc
    report = verify_release_audit_record_payload(payload, release_root=Path(args.release_dir).expanduser().resolve() if args.release_dir else None)
    if args.human:
        print(f"PSE audit-record verification: {path}")
        print(f"status: {report['status']}")
        print(f"detached contract verified: {str(report['detached_contract_verified']).lower()}")
        print(f"source binding: {report['source_binding']}")
        for f in report['findings']:
            print(f"- {f['code']}: {f['message']}")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report['status'] == 'fail' else 0


def cmd_verify_audit_index(args: argparse.Namespace) -> int:
    path = Path(args.audit_index).expanduser().resolve()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read audit index: {exc}") from exc
    report = verify_release_audit_index_payload(payload, collection_root=Path(args.collection_dir).expanduser().resolve() if args.collection_dir else None)
    if args.human:
        print(f"PSE audit-index verification: {path}")
        print(f"status: {report['status']}")
        print(f"detached contract verified: {str(report['detached_contract_verified']).lower()}")
        print(f"source binding: {report['source_binding']}")
        for f in report['findings']:
            print(f"- {f['code']}: {f['message']}")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report['status'] == 'fail' else 0


def cmd_export_audit_evidence(args: argparse.Namespace) -> int:
    output = Path(args.output).expanduser().resolve()
    evidence = [Path(p).expanduser().resolve() for p in args.evidence]
    for p in evidence:
        if not p.is_file():
            raise SystemExit(f"Audit evidence file not found: {p}")
        if output == p:
            raise SystemExit("Output bundle may not overwrite an input evidence file.")
    try:
        manifest = write_deterministic_audit_bundle(output, evidence)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot export audit evidence: {exc}") from exc
    errors = validate_audit_evidence_bundle_manifest(manifest)
    if errors:
        output.unlink(missing_ok=True)
        raise SystemExit("Audit evidence bundle contract failure: " + "; ".join(errors))
    if args.human:
        print(f"PSE deterministic audit-evidence bundle: {output}")
        print(f"entries: {manifest['entry_count']}")
        print(f"bundle fingerprint: {manifest['bundle_fingerprint']}")
        print("publication release artifacts included: false")
    else:
        print(json.dumps({"output": str(output), "sha256": sha256_file(output), "manifest": manifest}, ensure_ascii=False, indent=2))
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pse", description="Publication Systems Engineering CLI prototype")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, help_text, func in [
        ("build", "Build a book project with LuaLaTeX.", cmd_build),
        ("check", "Run machine QA against a built project.", cmd_check),
        ("clean", "Remove generated build artifacts.", cmd_clean),
        ("smoke", "Run the core smoke regression fixture.", cmd_smoke),
    ]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("project", nargs="?", default=".", help="Project directory (default: current directory).")
        p.set_defaults(func=func)
    # QA options.
    check_parser = next(p for p in sub.choices.values() if p.prog.endswith(" check"))
    check_parser.add_argument("--baseline", help="Optional JSON QA baseline for page-count drift review.")
    check_parser.add_argument("--human", action="store_true", help="Print concise file:line:column diagnostics instead of full JSON.")

    inspect_cmd = sub.add_parser("inspect-output", help="Inspect a built PDF for metadata, navigation, and text-extraction baselines without claiming accessibility certification.")
    inspect_cmd.add_argument("target", nargs="?", default=".", help="PDF file or project directory (default: current project build/book.pdf).")
    inspect_cmd.add_argument("--expected-language", help="Optional expected PDF catalog language code, e.g. en or vi.")
    inspect_cmd.add_argument("--human", action="store_true", help="Print a concise human-readable report instead of JSON.")
    inspect_cmd.add_argument("--output", help="Optional JSON report output path.")
    inspect_cmd.set_defaults(func=cmd_inspect_output)

    visual = sub.add_parser("visual-check", help="Render selected PDF pages and compare them with approved visual baselines.")
    visual.add_argument("project", nargs="?", default=".", help="Project directory (default: current directory).")
    visual.add_argument("--baseline-dir", required=True, help="Directory containing baseline images and manifest.")
    visual.add_argument("--manifest", help="Optional baseline manifest path; defaults to baseline-manifest.json in baseline directory.")
    visual.add_argument("--review-threshold", type=float, default=0.005, help="Material pixel-difference ratio that triggers human review (default: 0.005).")
    visual.set_defaults(func=cmd_visual_check)

    regress = sub.add_parser("regression", help="Run the layered framework regression suite and emit an aggregate JSON report.")
    regress.add_argument("--quick", action="store_true", help="Run smoke + typography + QA self-test only.")
    regress.add_argument("--no-visual", action="store_true", help="Skip visual comparison.")
    regress.add_argument("--visual-review-threshold", type=float, default=0.005, help="Visual review threshold (default: 0.005).")
    regress.add_argument("--output", help="Optional aggregate JSON report path.")
    regress.set_defaults(func=cmd_regression)

    doctor = sub.add_parser("doctor", help="Diagnose the installed PSE runtime, LuaLaTeX environment, fonts, and safe-build capability.")
    doctor.add_argument("--json", action="store_true", help="Emit a machine-readable diagnostic report.")
    doctor.add_argument("--deep", action="store_true", help="Run a temporary secure LuaLaTeX build in addition to lightweight checks.")
    doctor.add_argument("--profile", help="Validate dependencies for one installed profile, e.g. scholarly-edition.")
    doctor.set_defaults(func=cmd_doctor)

    proof = sub.add_parser("proof", help="Build a recipient-specific watermarked proof with provenance manifest.")
    proof.add_argument("project", nargs="?", default=".", help="Project directory (default: current directory).")
    proof.add_argument("--recipient", required=True, help="Recipient name or organization displayed on the proof.")
    proof.add_argument("--email", help="Optional recipient email recorded in the local proof manifest.")
    proof.add_argument("--proof-id", help="Optional stable proof identifier; otherwise generated automatically.")
    proof.add_argument("--label", default="CONFIDENTIAL PROOF", help="Visible proof label.")
    proof.set_defaults(func=cmd_proof)

    release = sub.add_parser("release", help="Create a publication release artifact after QA and provenance gates.")
    release.add_argument("project", nargs="?", default=".", help="Project directory (default: current directory).")
    release.add_argument("--release-id", help="Optional stable release identifier; generated when omitted.")
    release.add_argument("--source-date-epoch", type=int, help="Optional deterministic-build epoch; defaults to project Git commit time or publication-year fallback.")
    release.add_argument("--acknowledge-review", action="store_true", help="Explicitly acknowledge review-severity findings after human review.")
    release.set_defaults(func=cmd_release)

    verify = sub.add_parser("verify-release", help="Verify a release PDF against its provenance manifest.")
    verify.add_argument("release_dir", help="Directory containing release-manifest.json and the release PDF.")
    verify.set_defaults(func=cmd_verify_release)


    contracts_cmd = sub.add_parser("contracts", help="Show installed public schema/contract files and release-schema compatibility from the active runtime.")
    contracts_cmd.add_argument("--json", action="store_true", help="Emit the installed contract surface as JSON.")
    contracts_cmd.set_defaults(func=cmd_contracts)

    migration_cmd = sub.add_parser("release-migration", help="Assess a historical release against the current release contract without rewriting or upgrading the artifact in place.")
    migration_cmd.add_argument("release_dir", help="Historical release directory containing release-manifest.json.")
    migration_cmd.add_argument("--output", help="Optional external path for a non-mutating migration-assessment JSON file; it may not be inside the release directory.")
    migration_cmd.add_argument("--human", action="store_true", help="Print a concise human-readable migration assessment.")
    migration_cmd.set_defaults(func=cmd_release_migration)

    audit_cmd = sub.add_parser("audit-release", help="Create a separate non-mutating audit record for a historical or current release.")
    audit_cmd.add_argument("release_dir", help="Release directory containing release-manifest.json.")
    audit_cmd.add_argument("--output", help="Optional external JSON path; it may not be inside the release directory.")
    audit_cmd.add_argument("--human", action="store_true", help="Print a concise human-readable audit summary.")
    audit_cmd.set_defaults(func=cmd_audit_release)

    audit_index_cmd = sub.add_parser("audit-index", help="Audit immediate child release directories and create a separate path-independent batch index.")
    audit_index_cmd.add_argument("collection_dir", nargs="?", default=".", help="Directory whose immediate child directories are releases.")
    audit_index_cmd.add_argument("--output", help="Optional external JSON audit-index output path; it may not be inside any audited release.")
    audit_index_cmd.add_argument("--human", action="store_true", help="Print a concise human-readable batch summary instead of JSON.")
    audit_index_cmd.set_defaults(func=cmd_audit_index)

    verify_audit_record_cmd = sub.add_parser("verify-audit-record", help="Verify a release audit record detached, with optional binding to a release directory.")
    verify_audit_record_cmd.add_argument("audit_record", help="Audit-record JSON file.")
    verify_audit_record_cmd.add_argument("--release-dir", help="Optional release directory to re-check source hashes and portable fingerprint.")
    verify_audit_record_cmd.add_argument("--human", action="store_true", help="Print a concise human-readable verification report.")
    verify_audit_record_cmd.set_defaults(func=cmd_verify_audit_record)

    verify_audit_index_cmd = sub.add_parser("verify-audit-index", help="Verify a release audit index detached, with optional binding to a release collection.")
    verify_audit_index_cmd.add_argument("audit_index", help="Audit-index JSON file.")
    verify_audit_index_cmd.add_argument("--collection-dir", help="Optional release collection directory used to re-check indexed fingerprints and hashes.")
    verify_audit_index_cmd.add_argument("--human", action="store_true", help="Print a concise human-readable verification report.")
    verify_audit_index_cmd.set_defaults(func=cmd_verify_audit_index)

    export_audit_cmd = sub.add_parser("export-audit-evidence", help="Create a deterministic ZIP containing audit evidence only, never publication release artifacts.")
    export_audit_cmd.add_argument("output", help="Output .zip path.")
    export_audit_cmd.add_argument("evidence", nargs="+", help="Audit-record and/or audit-index JSON files to include.")
    export_audit_cmd.add_argument("--human", action="store_true", help="Print a concise human-readable export summary.")
    export_audit_cmd.set_defaults(func=cmd_export_audit_evidence)

    profiles_cmd = sub.add_parser("profiles", help="List installed profiles, capabilities, and generator support.")
    profiles_cmd.add_argument("--json", action="store_true", help="Emit machine-readable profile registry JSON.")
    profiles_cmd.add_argument("--generator-only", action="store_true", help="Show only profiles supported by the project generator.")
    profiles_cmd.add_argument("--modules", action="store_true", help="Show per-profile semantic module policy and default activation.")
    profiles_cmd.add_argument("--presentation", action="store_true", help="Show the integrated presentation preset and composition contract for each profile.")
    profiles_cmd.set_defaults(func=cmd_profiles)

    modules_cmd = sub.add_parser("modules", help="List installed scholarly semantic modules and their dependencies.")
    modules_cmd.add_argument("--json", action="store_true", help="Emit machine-readable semantic module registry JSON.")
    modules_cmd.set_defaults(func=cmd_modules)

    sem = sub.add_parser("semantic-ir", help="Parse PSE semantic source commands without executing TeX and emit a source-located intermediate representation.")
    sem.add_argument("project", nargs="?", default=".", help="Project directory (default: current directory).")
    sem.add_argument("--output", help="Optional JSON output path.")
    sem.set_defaults(func=cmd_semantic_ir)

    newp = sub.add_parser("new", help="Create a secure-by-default book project from a supported profile.")
    newp.add_argument("parent", nargs="?", default=".", help="Parent directory in which the project directory will be created.")
    newp.add_argument("--profile", default="basic-book", help="Installed generator-supported profile id. Use `pse profiles --generator-only` to inspect choices.")
    newp.add_argument("--title", help="Book title.")
    newp.add_argument("--subtitle", default="", help="Optional subtitle.")
    newp.add_argument("--author", help="Author/editor display name.")
    newp.add_argument("--language", help="Primary language code or label.")
    newp.add_argument("--publication-year", type=int, help="Four-digit publication year.")
    newp.add_argument("--series", default="", help="Optional series name.")
    newp.add_argument("--slug", help="Optional filesystem-safe project directory name.")
    newp.add_argument("--width-mm", type=float, default=126, help="Page width in millimetres (default: 126).")
    newp.add_argument("--height-mm", type=float, default=198, help="Page height in millimetres (default: 198).")
    newp.add_argument("--non-interactive", action="store_true", help="Require all mandatory values from command-line options; never prompt.")
    newp.set_defaults(func=cmd_new)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main()
