# Changelog

## 1.48.0-alpha — Lean core and maintained six-profile surface (2026-11-21)

- **Breaking profile change:** retire `basic-book`, `poetry` and `scholarly-edition` presentation profiles; retain six profiles, all 14 semantic modules and the shared LuaLaTeX engine. The `verse-structure` module remains available.
- Default generated project uses `academic-monograph`. Removed profile IDs fail explicitly; no silent visual or semantic aliasing.
- Consolidate ten overlapping GitHub Actions workflows into four. Full release-evidence and beta-candidate checks require explicit maintainer invocation; routine PR CI uses lighter security, registry and TeX gates.
- Bring CLI, runtime registry, profile handbooks, Wiki tables, QA, demo inventory and tests into agreement; preserve historical document URLs with retirement notices.
- Preserve root `LICENSE` absence, release verification, security gates and external release blockers. No live CI or deployment pass is asserted.
- See `docs/architecture/CORE-SIMPLIFICATION-AUDIT-1.48.md` for the architecture decision and scope.

## Historical development (unpublished)

PSE 1.48.0-alpha is the first publicly released version. Records of the earlier internal alpha milestones are not part of the published release history; the public history begins with 1.48.
