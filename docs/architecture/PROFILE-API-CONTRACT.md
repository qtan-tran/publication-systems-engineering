# Profile API and Inheritance Contract

Profiles are presentation and document-structure layers that depend on `pse-core`. They must not duplicate or replace the security, build, QA, proof, or release backbone.

## Dependency direction

`title -> profile -> core`. Dependencies must never point upward. Profiles may load ordinary LaTeX packages, but they may not import title-owned files.

## Allowed profile responsibilities

- page margins and optical page architecture;
- body type scale, leading, paragraph treatment;
- chapter/section hierarchy and opening-page behaviour;
- running heads and folios;
- title/publication-page presentation through the documented presentation hooks;
- profile-specific semantic presentation commands that do not alter core security or provenance behaviour.

## Forbidden profile responsibilities

Profiles must not redefine metadata setters, generated-metadata loading, proof-mode controls/watermarks, shell/build policy, QA/release semantics, provenance manifests, or runtime discovery. They must not write outside normal TeX output paths or require shell escape.

## Capability and module-policy declaration

Every profile contains `profile.json` declaring `id`, `version`, `extends`, `generator_supported`, `capabilities`, `required_metadata`, and `open_font_policy`. Manifest schema `1.1` also declares `module_policy`, which distinguishes required, recommended, optional, discouraged, and incompatible reusable semantic modules plus their default activation. The CLI validates the selected profile against installed runtime data. See [Profile module policy](PROFILE-MODULE-POLICY.md).


## Typography roles

Reusable typographic decisions use the core-owned [Typography Role System](TYPOGRAPHY-ROLE-SYSTEM.md). Profiles may override role values but must not create semantic meaning through font choices. Semantic modules may consume role commands but may not redefine the role contract.

## Locator orchestration

Profiles may declare a primary locator presentation policy through the core-owned [Locator Orchestration](LOCATOR-ORCHESTRATION.md) contract. Semantic locator identity remains owned by the corresponding semantic module; profiles must not re-register or renumber source IDs.

## Override boundary

Title-local exceptions belong in `config/pse-local.tex`. A profile change is appropriate only when the rule is reusable across multiple titles of that profile.

## Regression obligation

Every generator-supported profile must have: synthetic-only fixture, build/check regression, page-geometry assertion, secure proof smoke test, and visual baselines before it can be treated as stable.

## Current release hardening

`profile.json` is normative machine-readable API metadata. Schema `1.1` adds per-profile semantic-module policy while the runtime retains read compatibility for schema `1.0`. The runtime validates manifests before build/generation and fails closed on incompatible schema versions, invalid identifiers, missing required metadata, missing profile packages, or non-open framework font policy. `pse profiles` exposes the installed registry. Synthetic fixtures and visual baselines are profile-owned regression assets.


## Registry ownership

Profile directories and their `profile.json` manifests are the public source of truth for profile discovery. The runtime registry is generated from those manifests and checked for drift in CI. Wheel packaging discovers every registered profile dynamically, so adding a profile cannot silently leave the installed runtime behind. Semantic modules follow the equivalent `modules/*/module.json` contract.
