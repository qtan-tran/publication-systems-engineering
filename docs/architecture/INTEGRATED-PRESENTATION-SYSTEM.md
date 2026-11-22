# Integrated Presentation System

PSE 1.40 makes the presentation layer explicit as a composition contract across all nine publication profiles. Earlier releases established structural hierarchy, publication-unit metadata, typography roles, the page grid, margin objects, parallel text, multi-stream apparatus, and locator orchestration independently. The integrated presentation system records how a profile combines those capabilities without creating a new semantic engine.

## Two synchronized surfaces

Each profile contains `presentation.json` using public schema `presentation-profile-1.0`. The descriptor records eight presentation dimensions: preset, hierarchy, publication-unit metadata, grid, side material, apparatus, locator presentation, and parallel-text presentation.

The matching profile package calls `\PSEConfigureIntegratedPresentation` with the same eight values. Core exposes read-only accessors such as `\PSEPresentationPreset`, `\PSEPresentationGridMode`, `\PSEPresentationApparatusMode`, and `\PSEPresentationLocatorMode`.

This makes the JSON descriptor useful to CLI/tooling while the TeX runtime sees the same contract.

## Presentation descriptors are not semantic configuration

A descriptor does not activate a semantic module. It states how the profile expects active capabilities to be presented. `pse check` therefore fails closed when a descriptor requires a semantic capability that has been deactivated, for example a multi-stream apparatus without the `apparatus` module or a profile-controlled parallel presentation without `parallel-text`.

Semantic ownership remains unchanged:

- hierarchy semantics remain module-owned where active;
- publication-unit data remains owned by `publication-unit-metadata`;
- apparatus stream identity remains owned by `apparatus`;
- parallel segments and alignments remain owned by `parallel-text`;
- locator identities remain owned by their existing locator modules;
- profiles and core own presentation composition.

## CLI inspection

`pse profiles --presentation` shows the presentation contract for each registered profile. The JSON form provides the same descriptors for tooling.

## Stability rule

Changing profile presentation may change pagination, typography, margins, or the visual treatment of scholarly furniture. It must not silently rewrite manuscript semantics, stable IDs, contributor relations, apparatus stream names, or parallel-text alignments.

## Branding boundary

The 1.40 system uses neutral PSE presentation identifiers. It is not the documentation-site brand layer, a publisher house style, or a web theme. Documentation branding remains deferred until the documentation platform phase.
