# CI and maintainer workflow

PSE 1.48 deliberately uses **four** GitHub Actions workflows instead of ten. The daily edit loop is not a release ceremony.

| Workflow | Trigger | Purpose |
| --- | --- | --- |
| `qa-regression` | Pull requests and main | Source/security/installed-contract checks; fast PDF smoke on PRs and full profile visual tests on main |
| `documentation-pages` | Documentation changes or manual | Strict MkDocs build, site QA, Pages deployment evidence |
| `beta-candidate` | Manual dispatch | Explicit candidate preflight; does **not** imply legal authorisation |
| `release-evidence` | Manual dispatch | Exact-commit evidence on Windows, macOS and Linux |

**Editor:** `pse build .` → `pse check .` → visually review. **Maintainer:** run the full release workflows only for an actual candidate commit. This reduces repeated installs and lengthy TeX jobs while preserving release assurance when needed.

The root `LICENSE` remains absent pending independent legal review. A green workflow is never sufficient to claim publicly licensed release status, accessible-PDF certification or official publication readiness.
