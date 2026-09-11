# A Synthetic Play

This is a Publication Systems Engineering project generated with the `drama` profile.

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

`drama` is a generator-supported profile. Use `config/pse-local.tex` for restrained title-local exceptions rather than editing the shared core or profile package.

## Drama semantic modules

This project uses stable speaker IDs, speech and stage-direction semantics, act/scene structure, and an optional dramatic-line locator namespace. Presentation belongs to the `drama` profile; semantic IDs belong in title-owned source.
