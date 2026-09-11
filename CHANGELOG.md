# Changelog

## 1.47.0-alpha — Release-Candidate Readiness Review

- Entered a stabilization-only surface freeze at 9 profiles and 14 semantic modules after completion of the 1.33–1.46 architecture/documentation roadmap.
- Added a machine-readable RC-readiness assessment that separates internally checkable technical state from legal, live-CI, and live-documentation deployment evidence.
- Recorded the explicit decision not to advertise the current snapshot as a public release candidate or public licensed beta while external hard gates remain open.
- Corrected stale beta-freeze schema references to profile manifest schema 1.1 and semantic module activation schema 1.1.
- Removed generated `*.egg-info` packaging metadata from the public source tree, fixing exact-commit candidate-evidence portability when source snapshots are reconstructed without build artifacts.
- Kept root `LICENSE` absent pending independent legal review and prohibited feature-surface growth during stabilization except for correctness, security, compatibility, or release-blocking fixes.

## 1.46.0-alpha — Documentation Release Engineering

- Added generated-site QA for page titles, canonical links, sitemap/base-URL consistency, and deployment-safe metadata checks after strict MkDocs rendering.
- Added documentation release evidence schema 0.1 and a SHA-256 inventory generator binding generated-site files to the PSE version, deployment base URL, and source revision without making signature, timestamp, live-deployment, or preservation claims.
- Froze a stable public documentation URL baseline and added regression tooling that prevents previously published paths from silently disappearing.
- Strengthened the Pages workflow to validate source and stable URLs before rendering, validate the generated site after rendering, retain documentation evidence as a workflow artifact, and then deploy the site.
- Recorded the 1.46 decision not to create a GitHub Wiki mirror; `/wiki` remains the only editable canonical documentation source and MkDocs Pages remains the primary rendered documentation product.
- Kept the legal/public-license gate separate from documentation readiness; root `LICENSE` remains absent.

## 1.45.0-alpha — Workflow / QA / Release Handbook

- Replaced the public Workflows and Quality/Release stubs with task-oriented handbook coverage from canonical source through build, machine QA, human review, recipient proofs, publication release, verification, and detached audit evidence.
- Formalized the end-user distinction between working PDF, recipient proof, and publication release so generated iteration artifacts cannot be mistaken for the evidence-bearing release boundary.
- Documented the four QA severities, finished-PDF output-inspection baseline and explicit accessibility/conformance limits, release manifest schema 0.2 verification, legacy schema 0.1 handling, and non-mutating historical migration assessment.
- Added public audit guidance for detached audit records/indexes, verification, and deterministic evidence-only export while explicitly excluding digital-signature, PKI, timestamp, notarization, and preservation claims.
- Added regression coverage binding handbook commands/flags to the current CLI surface, release/audit contract terminology, artifact locations, navigation, and stale-stub removal.
- Kept release schemas and runtime semantics unchanged; documentation release engineering and the GitHub Wiki mirror decision remain scheduled for 1.46.

## 1.44.0-alpha — Feature Handbook

- Replaced Book Features stubs with a reusable-capability handbook covering all fourteen semantic modules plus the typography/page-grid presentation boundary.
- Added cross-profile policy tables for structural hierarchy, publication/contributor metadata, margin objects, parallel text, apparatus, locator modules, verse/drama semantics, bibliography, index, scholarly matter, and multilingual text.
- Bound handbook policy rows to public `profile.json` manifests and page-grid/side-material guidance to `presentation.json`, including an explicit `not declared` state that is not treated as incompatibility.
- Added practical semantic-versus-presentation guidance so layout changes do not rewrite stable IDs, apparatus streams, alignment relations, or other reusable publication semantics.
- Added regression coverage for all feature pages, all fourteen module IDs, all declared/undeclared profile policy rows, presentation descriptors, feature-specific invariants, navigation, and stale-stub removal.
- Deferred the full workflow/QA/release handbook to 1.45.

## 1.43.0-alpha — Profile Handbook

- Replaced the single profile overview stub with a nine-profile end-user handbook covering editorial fit, presentation character, module policy/defaults, starter project areas, customization points, limitations, and synthetic demos.
- Kept profile guidance synchronized with machine-readable `profile.json` module policy and `presentation.json` descriptors rather than duplicating a separate feature model.
- Added explicit decision guidance for commonly confused profile pairs: Academic Monograph vs Scholarly Edition, Critical Edition vs Scholarly Edition, and Basic Book vs Literary Fiction.
- Added regression coverage binding handbook pages to all nine profile manifests, presentation presets, demo locations, navigation entries, and supported CLI commands.
- Kept developer profile API contracts in `/docs` and deferred feature-by-feature handbook expansion to 1.44.

## 1.42.0-alpha — Beginner Handbook

- Replaced the Getting Started stub with a task-oriented beginner handbook covering installation, profile selection, project generation, source ownership, first edits, build/check, troubleshooting, and the transition to proof/release workflows.
- Kept the beginner path on supported public CLI commands and generated project structure rather than exposing framework internals as prerequisites.
- Added cross-platform command guidance and explicit boundaries between canonical project source, generated build output, working PDFs, proofs, and releases.
- Added regression coverage for handbook navigation, command accuracy, source-of-truth guidance, privacy guidance, and the nine-profile selection surface.
- Deferred full per-profile documentation to 1.43.

## 1.41.0-alpha — Documentation Platform

- Promoted the MkDocs website to the primary rendered public documentation product while retaining `/wiki` as the canonical Markdown source.
- Adopted MkDocs Material with a restrained PSE documentation baseline, search, dark/light mode, and stable IA-driven navigation.
- Added deployment-time `site_url` binding so GitHub Pages or a future custom domain can generate host-correct canonical/sitemap output without rewriting documentation source.
- Added documentation-source QA for navigation, local links/assets, orphan pages, and the public/private trust boundary.
- Added a custom 404 page, metadata conventions, and a documentation-platform technical contract.
- Kept analytics provider-neutral and deferred broader product-site branding and full handbook content to later documentation phases.


## 1.40.0-alpha - Integrated Scholarly Presentation System

- Added a core integrated-presentation contract coordinating hierarchy, publication-unit metadata, typography/page-grid composition, side material, apparatus, locators, and parallel text without creating a new semantic engine.
- Formalized machine-readable `presentation.json` descriptors for all nine profiles under public schema `presentation-profile-1.0` and bound each descriptor to the TeX runtime contract.
- Added `pse profiles --presentation` and presentation-system QA metrics/fail-closed dependency checks.
- Added architecture documentation and froze the primary public Wiki IA into eight user/task-oriented sections with clean, non-versioned URL families.
- Branding remains explicitly deferred; 1.40 uses neutral presentation preset identifiers only.


## 1.39.0-alpha - Locator Orchestration

- added a core-owned locator orchestration policy without creating a new locator engine;
- coordinated canonical, dramatic-line, verse-line, and parallel-alignment namespaces while preserving module ownership;
- added `config/locator-orchestration.json` schema 1.0 plus generated TeX policy bridge;
- extended the semantic parser to inventory `\PSEVerseLine` stable IDs and optional display labels;
- added unified locator-orchestration QA metrics and inactive-namespace/stable-ID validation;
- generated profile-appropriate locator policies for critical, scholarly, drama, poetry, and bilingual starters;
- added technical and Wiki documentation stubs.


## 1.38.0-alpha - Multi-Stream Apparatus

- Extended the existing `apparatus` module with five semantic streams: `textual`, `editorial`, `translation`, `commentary`, and `source`.
- Kept stream identity separate from presentation labels so profiles/projects may render full names, abbreviations, or labels such as A/B/C without rewriting semantic source.
- Preserved the legacy generic apparatus commands for backward compatibility and added stream-aware locator/range validation to semantic source QA.
- Defined cross-profile apparatus policy and added multi-stream technical documentation plus a public Wiki stub; branding remains deferred.

## 1.37.0-alpha - Parallel Text Consolidation

- Extended the existing `parallel-text` module with alignment locators and typed alignment notes while preserving `\PSEParallelTranslationNote` compatibility.
- Expanded the bilingual presentation contract to five modes: parallel columns, facing pages, sequential blocks, source-dominant, and target-dominant.
- Kept alignment semantics independent of page/column position and added QA for unresolved or duplicate locator/note relations.
- Added parallel-text technical documentation and a public Wiki stub; branding remains deferred.

## 1.36.0-alpha — Margin Objects & Side Material

- added the reusable `margin-objects` semantic module with stable IDs for marginal notes, side captions, apparatus anchors, locator markers, and running-side objects;
- separated semantic object ownership from profile/core placement and introduced a deterministic visible fallback when outer-margin placement is unavailable;
- added a core margin-object presentation contract and fixed pre-composition outer-margin width/separation configuration for scholarly side-zone profiles;
- defined cross-profile module policy without making side material mandatory manuscript content;
- added architecture documentation, a public Wiki stub, and regression coverage while deferring collision management and formal tagged-PDF reading-order claims.

## 1.35.0-alpha — Asymmetric Scholarly Grid

- Added core page-grid presentation contract version 1 with named inner, outer, header, footer, primary-text, and apparatus-allocation regions.
- Migrated all nine profiles from direct geometry ownership to the shared grid contract while preserving their established dimensions.
- Defined per-profile asymmetric-grid policy without turning layout into a semantic module.
- Established a pre-composition boundary: semantic modules may consume grid regions but may not resize the grid dynamically.
- Added technical architecture documentation, a non-technical Wiki stub, and grid regression coverage.
- Branding remains deferred until the information architecture and integrated presentation system stabilize.

## 1.34.0-alpha

- added a core-owned typography role contract for body, display, chapter, section, metadata, running-head, caption, and apparatus presentation;
- migrated all nine profiles to explicit typography-role overrides while preserving semantic ownership boundaries and existing visual baselines;
- made the apparatus module consume the shared apparatus role instead of owning an independent type-size decision;
- added architecture documentation, a public Wiki typography stub, and documentation-maturity tracking;
- deliberately deferred branding, palette, logo, and documentation-site visual identity until the integrated presentation architecture stabilizes.

## 1.33.0-alpha

- added reusable `publication-unit-metadata` semantics for unit title/subtitle, abstract, keywords, DOI, and contributor relations;
- extended contributor semantics with query access and silent relation registration while preserving the legacy presentation command;
- added cross-profile contributor and publication-unit metadata policy;
- updated edited-collection starter/demo to use metadata-rich publication-unit openers;
- established `/wiki` as the canonical public explanatory documentation source with MkDocs configuration and GitHub Pages workflow;
- added documentation maturity tracking and Wiki regression checks.

## 1.32.0-alpha

- added the reusable `structural-hierarchy` semantic module;
- defined a four-level prose section contract inside chapters: section, subsection, subsubsection, and paragraph;
- treated Part and Chapter as higher-order publication structures outside the section-depth count;
- rejected fifth-level `subparagraph` structure when the module is active and explicitly avoided silent manuscript flattening;
- added profile-specific hierarchy policy and regression coverage.

## 1.31.0-alpha

- added profile manifest schema 1.1 with per-profile semantic module policy and default activation;
- added `required`, `recommended`, `optional`, `discouraged`, and `incompatible` module-policy states;
- added project-level `deactivate` support for default-enabled recommended modules while protecting required modules;
- established index policy across all nine profiles: recommended/default for seven profiles, optional for poetry, discouraged for literary fiction;
- expanded edited-collection generator/demo with reusable subject indexing;
- exposed policy through `pse profiles --modules` and added dedicated regression coverage.

## 1.30.0-alpha

- added detached `verify-audit-record` and `verify-audit-index` commands with optional source re-binding;
- added deterministic `export-audit-evidence` ZIP generation for audit records/indexes only;
- added the `audit-evidence-bundle-manifest` 0.1 public contract and installed schema;
- verified relocation-safe source binding through portable release fingerprints;
- kept audit evidence outside publication release artifacts and made no signature, PKI, or trusted-timestamp claim;
- added no profile or semantic module.

## 1.29.0-alpha

- added path-independent release fingerprints to current audit records;
- added `pse audit-index` for external batch audit indexes over multiple release directories;
- added release-audit-record schema 0.2 and release-audit-index schema 0.1 while retaining audit-record 0.1 as legacy-verifiable material;
- added regression coverage proving fingerprint stability after release relocation and batch fingerprint stability after collection relocation;
- kept absolute filesystem paths informational only and outside portable identity;
- added no profile or semantic module.

## 1.28.0-alpha

- added `pse contracts` to expose the active runtime's installed release/output-inspection schema surface and compatibility policy;
- added compatibility metadata to `pse verify-release` reports so current, legacy, and unsupported manifest schemas are explicit to audit tooling;
- added `pse release-migration` as a non-mutating historical-release assessment command;
- migration assessment records source manifest/PDF hashes and explicitly forbids in-place upgrade or retroactive output-inspection inference;
- preserved schema `0.1` as verification-only history and schema `0.2` as the only current creation contract;
- added installed-contract and migration regressions; no profile or semantic module added.

## 1.25.0-alpha

- Added a human-facing demo gallery for all 9 generator-supported profiles, with canonical synthetic PDF outputs committed under `examples/profiles/*/output/`.
- Added beginner-facing profile-selection and demo-build documentation.
- Added `scripts/examples/build_profile_demos.py` to reproduce one or all canonical profile demos using the normal PSE build path.
- Added regression coverage for demo/source/output parity and root README gallery links.
- Hardened public-tree integrity so committed PDFs are limited to canonical profile-demo outputs.
- Added no new profile or semantic module; framework capability remains 9 profiles / 11 semantic modules.

## 1.21.0-alpha

- Added the generator-supported `edited-collection` profile.
- Added the minimal reusable `contributor-metadata` semantic module for stable contributor identity and contributor/unit/role relations.
- Kept affiliation and ORCID optional and deliberately excluded external identity lookup, CRediT, ROR, Crossref export, and authority reconciliation.
- Extended registry/profile regression coverage to 9 profiles and 11 semantic modules.


## 1.20.0-alpha

- Consolidated profile and semantic-module registration around manifest discovery instead of hand-maintained packaging/runtime lists.
- Added a reproducible registry synchronization command and exact registry-drift gates for release evidence and beta-candidate CI.
- Replaced static wheel data-file enumeration with manifest-driven packaging for all registered profiles and modules.
- Added registry-wide contract coverage for runtime parity, dependency references, installed wheel contents, and the presentation/semantic boundary.
- Kept the framework at 8 profiles and 10 semantic modules; this increment adds no publishing feature.

## 1.19.0-alpha

- Added the neutral `poetry` profile for stanza spacing, verse indentation, long-line continuation, and optional display numbering.
- Added the reusable `verse-structure` semantic module so stanza and verse-line identity remain stable independently of page presentation.
- Added synthetic poetry generation, fixture, documentation, visual-baseline coverage, and semantic duplicate-ID regression.
- Preserved the profile/module trust boundary: poetry presentation owns layout; verse semantics own identifiers and structure.

## 1.18.0-alpha

- Added the neutral `critical-edition` profile for source-oriented scholarly editions using the existing locator, apparatus, multilingual, bibliography, index, and scholarly-matter modules.
- Added a synthetic critical-edition generator starter, fixture, documentation, proof/build checks, and visual-regression baseline contract.
- Replaced stale hard-coded profile tuples in profile regression and visual orchestration with manifest-driven discovery of generator-supported profiles.
- Kept semantic ownership in reusable modules; the new profile contains presentation rules only and does not duplicate locator or apparatus semantics.

## 1.17.0-alpha

- Added exact-commit candidate evidence generation for clean, non-shallow Git checkouts.
- Bound full-history high-confidence credential/key scanning to the candidate `HEAD` and made shallow history a hard failure.
- Corrected release-evidence CI artifact collection so generated evidence is uploaded from the directory where the scanners actually write it.
- Preserved the external legal-review and live cross-platform CI gates; no public licensed-beta authorization is asserted.

## 1.16.0-alpha

- Added the canonical PSE colophon/copyright-page attribution banner as a bundled framework asset.
- Made banner rendering a publication-release contract: standard publication pages render it automatically, and `pse release` blocks when final-build attribution evidence is absent.
- Added attribution evidence (placement policy and asset SHA-256) to release manifests and regression coverage.
- Kept the public licensed beta blocked pending independent legal review and live release evidence.

## 1.15.0-alpha

- Sanitised the public repository so internal development reports, counsel discussions, release deliberations, and historical milestone notes are excluded from the GitHub-facing tree.
- Renamed regression tests and CI workflows by function rather than internal development stage.
- Added public brand/attribution guidance and preserved the future option of a separately designated commercial licensing entity without exposing internal commercial planning.
- Added public-tree integrity regression and synchronized release-state metadata.
- Kept the public licensed beta blocked pending independent legal review and live release evidence.

## 1.14.0-alpha

- Added commercial-entity readiness and brand/colophon planning in the private development record.

## 1.13.0-alpha

- Hardened release evidence, candidate-history scanning, and licence-candidate review.

## 1.12.0-alpha

- Defined organised publishing use, contractor boundaries, and electronic-assent requirements.

## 1.11.0-alpha

- Adopted `Produced with Publication Systems Engineering.` as the canonical English attribution line.
- Clarified output ownership and third-party component licensing.

## 1.10.0-alpha

- Added public-launch staging, security-disclosure preparation, archival/citation readiness, and legal-review gating.

## 1.9.0-alpha

- Froze the public CLI, schema, QA-severity, and generated-project contracts for beta-candidate preparation.

## 1.8.0-alpha

- Added bounded parser limits, source diagnostics, deterministic parser fuzz tests, and compatibility documentation.

## 1.7.0-alpha

- Added a safe semantic intermediate representation and non-executing semantic source parser.

## 1.6.0-alpha

- Added the bilingual-edition profile and parallel-column/facing-page presentation modes.

## 1.5.0-alpha

- Added generic parallel-text semantics and alignment QA.

## 1.4.0-alpha

- Added a neutral drama visual profile and generator integration.

## 1.3.0-alpha

- Added drama semantics, speaker registry, speech/stage-direction structures, and dramatic locators.

## 1.2.0-alpha

- Added semantic namespaces and multi-family composition contracts.

## 1.1.0-alpha

- Added scholarly locator QA, explicit locator schemes, apparatus, bibliography, index, and multilingual scholarly support.

## 1.0.0-alpha

- Added the scholarly-edition foundation and semantic module registry.

## 0.9.0-alpha

- Hardened profile visual baselines and generator contracts.

## 0.8.0-alpha

- Added controlled profile expansion for literary fiction and academic monographs.

## 0.7.0-alpha

- Added deterministic release engineering, provenance manifests, checksums, and tamper verification.

## 0.6.0-alpha

- Added QA severity, regression orchestration, and visual regression.

## 0.5.0-alpha

- Added typography and page-architecture contracts.

## 0.4.0-alpha

- Added installation, runtime discovery, and bootstrap diagnostics.

## 0.3.0-alpha

- Added project generation with YAML metadata and safe generated-project contracts.

## 0.2.5-alpha

- Added secure-by-default build/proof architecture and recipient-specific proof provenance.

## 0.2.0-alpha

- Added the minimal executable core, CLI, build, clean, and QA foundation.

## 0.1.0-alpha

- Established the initial architecture specification.
