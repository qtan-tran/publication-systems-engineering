# Publication Systems Engineering

**Publication Systems Engineering (PSE)** is a source-available framework for building reliable, extensible, sustainable book-production systems.

PSE treats publication production as an engineered lifecycle rather than a collection of one-off templates:

`content → metadata → title configuration → profile + semantic modules → core → build → QA → proof/release`

The current production target is deliberately narrow: **print-ready PDF with LuaLaTeX** on Windows, macOS, and Linux.

> **Status — 1.47.0-alpha:** technical beta candidate in a stabilization-only surface freeze (9 profiles / 14 semantic modules). The public repository surface is sanitised and the command/schema contracts are frozen, but this is **not yet a public licensed beta**. Independent legal review and live CI on the exact release candidate remain hard gates.

## See what PSE produces

You can inspect finished PDFs before installing anything. Every demo is built from synthetic content with the same public PSE build path used by generated projects.

| Profile | Best for | Finished PDF |
| --- | --- | --- |
| `basic-book` | General prose books | [View demo](examples/profiles/basic-book/output/basic-book-demo.pdf) |
| `literary-fiction` | Novels and reading-oriented prose | [View demo](examples/profiles/literary-fiction/output/literary-fiction-demo.pdf) |
| `academic-monograph` | Research monographs | [View demo](examples/profiles/academic-monograph/output/academic-monograph-demo.pdf) |
| `scholarly-edition` | Annotated scholarly editions | [View demo](examples/profiles/scholarly-edition/output/scholarly-edition-demo.pdf) |
| `critical-edition` | Source-oriented critical editions | [View demo](examples/profiles/critical-edition/output/critical-edition-demo.pdf) |
| `drama` | Plays and dramatic texts | [View demo](examples/profiles/drama/output/drama-demo.pdf) |
| `bilingual-edition` | Parallel bilingual publications | [View demo](examples/profiles/bilingual-edition/output/bilingual-edition-demo.pdf) |
| `poetry` | Poetry collections | [View demo](examples/profiles/poetry/output/poetry-demo.pdf) |
| `edited-collection` | Multi-author edited volumes | [View demo](examples/profiles/edited-collection/output/edited-collection-demo.pdf) |

Not sure where to start? See the [profile demo gallery](docs/getting-started/PROFILE-DEMO-GALLERY.md), then [Choose a profile](docs/getting-started/CHOOSE-A-PROFILE.md). If you are new to PSE, use the public [Beginner Handbook](wiki/getting-started/index.md). To reproduce the showcase PDFs, see [Build the demos](docs/getting-started/BUILD-THE-DEMOS.md).

## Why PSE exists

PSE is designed for editors, layout professionals, independent/small publishing teams, and scholarly editors who need:

- consistent series production;
- reusable core architecture rather than copied templates;
- secure-by-default manuscript and proof workflows;
- clean builds and reproducible release artifacts;
- regression testing and human-review gates;
- profiles that control presentation without owning security or semantic QA;
- semantic modules that can be composed without rewriting the backbone.

## Current capabilities

The alpha backbone includes:

- `pse new` secure project generation;
- installed-runtime discovery and `pse doctor`;
- neutral profiles for basic books, literary fiction, academic monographs, scholarly editions, critical editions, poetry, edited collections, drama, and bilingual editions;
- semantic modules for locators, apparatus, multilingual text, bibliography, index, scholarly matter, verse, drama, and parallel text;
- non-executing semantic source parsing with source locations;
- `pse build`, `pse check`, visual/regression QA;
- `pse inspect-output` for a limited PDF metadata/navigation/text-extractability baseline without accessibility certification; release artifacts bind the resulting inspection evidence to the exact final PDF SHA-256;
- recipient-specific watermarked `pse proof` artifacts;
- deterministic local `pse release` promotion with manifests and SHA-256 integrity checks;
- `pse verify-release` tamper/integrity verification.
- `pse contracts` for installed release-schema discovery, `pse release-migration` for non-mutating legacy-release assessment, and `pse audit-release` for separate hash-bound audit evidence.
- `pse audit-index` creates an external portable batch audit index for a collection of releases.

All public fixtures are synthetic. PSE does not include private downstream publishing architecture or unpublished manuscript material.

## Quick start

Install from a checked-out candidate:

```text
python -m pip install .
pse doctor --deep
```

Create a project in private storage:

```text
pse new /path/to/private-projects
```

Then:

```text
pse build .
pse check . --human
pse proof . --recipient "Recipient Name"
pse release .
pse verify-release release/<release-id>
```

See [Onboarding](docs/workflows/ONBOARDING.md) for the complete workflow. For finished-PDF inspection, see [Output inspection and accessibility baseline](docs/getting-started/OUTPUT-INSPECTION-ACCESSIBILITY.md). Audit evidence can be checked with `pse verify-audit-record` / `pse verify-audit-index` and exported reproducibly with `pse export-audit-evidence`; see [Audit evidence verification and deterministic export](docs/release/AUDIT-EVIDENCE-VERIFICATION-AND-EXPORT.md).

## Architecture boundaries

- **Core** provides shared production infrastructure.
- **Profiles** provide presentation/page architecture.
- **Semantic modules** provide meaning-aware structures and QA contracts.
- **Titles** provide canonical content, metadata, and title-local configuration.
- **Security, QA, runtime, proof, and release provenance** remain backbone responsibilities and must not be duplicated by profiles/modules.

See [Architecture Specification](docs/architecture/ARCHITECTURE-SPECIFICATION.md), [Profile API](docs/architecture/PROFILE-API-CONTRACT.md), and [Semantic Module Architecture](docs/architecture/SEMANTIC-MODULE-ARCHITECTURE.md).

## Security model

PSE is designed to run inside publisher-controlled infrastructure. LuaLaTeX shell escape is disabled by default; YAML parsing and metadata bridges are validated; unpublished manuscripts do not need to leave the publisher's environment. Recipient-specific proof watermarking is a deterrence and traceability mechanism, **not unremovable DRM**.

Never attach unpublished manuscripts, recipient proofs, secrets, or proprietary production data to public issues. See [Security](SECURITY.md) and `docs/security/`.

## QA and release philosophy

Machine findings use four severities:

- `error` — blocking;
- `warning` — technical warning;
- `review` — human production/editorial judgement required;
- `info` — recorded evidence/status.

A successful working build is not automatically a publication release. Use `pse release` and `pse verify-release` for the release artifact boundary.

## Licensing, citation, and commercial use

PSE is currently **source-available in development**. The final public licence has not yet been published. Source visibility does not itself grant institutional, commercial, enterprise, embedding, OEM, white-label, hosted, or managed-service rights.

Every ebook produced by the PSE publication-release pipeline must include the canonical PSE attribution banner on a copyright/publication page or colophon. The standard publication page inserts it automatically, and `pse release` blocks if final-build attribution evidence is absent. The banner includes the canonical line:

> **Produced with Publication Systems Engineering.**

This is currently a framework release contract; any separate licence-level attribution obligation remains subject to independent legal review. See [Brand and Attribution](docs/design/BRAND-AND-ATTRIBUTION.md), [Licensing Overview](docs/licensing/OVERVIEW.md), [Commercial Licensing Inquiry](docs/licensing/COMMERCIAL-LICENSING-INQUIRY.md), and [`LICENSE-STATUS.md`](LICENSE-STATUS.md). Citation metadata is in [`CITATION.cff`](CITATION.cff).

## Beta-candidate contracts

The public command/schema surface is frozen while legal review and release evidence are completed. See:

- [Beta Candidate Freeze](docs/beta/BETA-CANDIDATE-FREEZE.md)
- [Public Beta Checklist](docs/beta/PUBLIC-BETA-CHECKLIST.md)
- [CLI Compatibility Matrix](docs/reference/CLI-COMPATIBILITY-MATRIX.md)
- [API & Schema Compatibility](docs/reference/API-SCHEMA-COMPATIBILITY.md)
- [Compatibility & Migration Policy](docs/architecture/COMPATIBILITY-MIGRATION-POLICY.md)
- [Support Matrix](docs/reference/SUPPORT-MATRIX.md)

## Contributing

PSE is maintainer-led and contribution-friendly, but external code contribution acceptance remains gated by the final contributor-rights/dual-licensing policy. Small reproducible bug reports and architecture-aligned proposals are welcome once the public repository is staged. Use synthetic reproductions only.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Project origin

Publication Systems Engineering is a public contribution developed as part of the broader publishing work surrounding **Marginalia – Trật tự ẩn**. No private architecture, title-specific source, production code, or internal materials from that project are included here.

## Maintainer

This repository was created and is maintained by **Quoc-Tan Tran**, Open Science Researcher at the Faculty of Sociology, Bielefeld University


## Documentation

Public explanatory documentation is maintained from [`wiki/`](wiki/index.md). Technical contracts remain under [`docs/`](docs/).
