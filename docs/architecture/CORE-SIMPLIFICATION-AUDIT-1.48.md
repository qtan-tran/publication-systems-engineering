# PSE 1.48 — Core simplification audit

**Date:** 2026-11-21  
**Basis:** the pre-publication working source tree.  
**Status:** engineering candidate for a first exact-commit GitHub CI run; **not** a publicly authorised, licensed beta.

## Decision

The supported product surface is **six book presentation profiles**. All **14 semantic modules remain** because they represent composable content capabilities, not interchangeable templates. The shared `core/pse-core.sty`, every module `.sty`, and the surviving profile `.sty` implementations have not been changed by this simplification. The original PDFs of the six retained profile demos remain unchanged.

| Retired presentation | Recommended path | Loss or limitation to review |
| --- | --- | --- |
| `basic-book` | `academic-monograph` | Review defaults, active scholarly modules, running heads and visual rhythm. It is not a bit-for-bit visual alias. |
| `scholarly-edition` | `critical-edition` | A scholarly annotated edition need not establish a critically reconstructed text. The profile is a presentation family, not an editorial-method claim; review required locators and apparatus. |
| `poetry` | `literary-fiction` **only** for narrative-oriented content, or a title-specific presentation | The `verse-structure` module remains, but poetry-specific page/stanza composition has **not** been silently moved into `literary-fiction`. Verse-heavy titles require an explicit presentation test. |

There are **no silent aliases** from retired profile IDs. Unsupported input fails closed, and choosing a replacement is an explicit title-owner decision. Inspect the installed registry with `pse profiles`.

## Maintenance reduction

The exact input archive contained **646 files / 3,286,942 uncompressed bytes**. After retiring the three profile directories and their dedicated demo projects, fixtures and visual baselines, and consolidating GitHub Actions, the working source is around **540–550 files / 2.5–2.6 MB** (the final ZIP integrity manifest gives the authoritative final inventory). The principal gain is fewer supported contracts, not disk-space optimisation.

GitHub Actions workflows have been consolidated into **four**:

- `qa-regression.yml`: common source/security/contract checks, light cross-platform installed surface, and Linux TeX QA; PRs run a quicker hard gate, while pushes to `main` run full visual regression.
- `docs-pages.yml`: docs changes, strict build and Pages evidence.
- `beta-candidate.yml`: manual candidate-specific checks.
- `release-evidence.yml`: manual exact-commit cross-platform release evidence.

Full release machinery has **not** been removed; it is only decoupled from everyday editing. A book editor ordinarily runs `pse build .` and `pse check .`, optionally `pse proof`, and runs `pse release` plus `pse verify-release` only after approval.

## Compatibility and quality controls

1. Runtime registry is manifest-derived, not manually invented. It has exactly six profiles and fourteen semantic modules.
2. Project generation defaults to `academic-monograph`, with retired IDs explicitly rejected. The CLI retains fail-closed module dependencies, security and release verification.
3. Public wiki lists only current supported profiles, with clear retirement notices at the three unsupported profile URLs.
4. Documentation’s profile-policy matrices follow current `profile.json` and `presentation.json`; historical review records are labelled historical.
5. Public source integrity checks enforce local Markdown links, generated-artifact exclusion, complete SHA256 inventory and private-boundary hygiene.
6. The source remains **source-available**, with root `LICENSE` absent pending independent legal review. This archive is not advertised as open-source licensed or a final public beta.

## Deliberately retained complexity

- Semantic module boundaries, stable IDs, bibliography/index, apparatus, parallel text and structural hierarchy are retained for existing scholarly titles and future production-domain reuse.
- Evidence-backed releases, basic output inspection and security checks remain because removing them would trade fewer files for higher publishing risk.
- `docs/` contains some historical engineering/reference material. The canonical user guidance is `/wiki`; replacing every historical record with links would provide little runtime benefit and would weaken traceability.

## Known external gates

The local audit cannot verify real Windows/macOS/Linux GitHub runners, Pages deployment, or exact-commit candidate evidence. Those checks must run in the actual GitHub repository. Licensing and contributor-rights reviews remain independent external blockers. PDF/UA, WCAG, certified accessibility, legal authorisation and real deployment must **not** be claimed from this local source audit.

## Suggested next sequence

1. Upload **only** the GitHub-clean tree so the repository root contains `.github/`, `core/`, `profiles/`, `tools/`, `wiki/`, and the other project directories directly.
2. Commit the candidate unchanged and run `qa-regression`; confirm all three jobs pass. For docs changes, verify strict `documentation-pages` build.
3. Fix actual live failures at the exact commit; keep a clear commit history and preserve the release contracts.
4. When preparing a genuine release candidate, explicitly dispatch `beta-candidate` and `release-evidence`, record the exact commit SHA, and complete external licensing gates.
