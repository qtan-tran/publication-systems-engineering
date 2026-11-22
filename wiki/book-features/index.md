---
title: Book features
description: Use reusable PSE capabilities without confusing semantic structure with profile presentation.
---

# Book features

PSE separates **book features** from **book profiles**. A profile answers “what kind of publication am I producing?” A feature answers “what reusable semantic or presentation capability does this publication need?”

This distinction matters because the same capability can appear in more than one publication type. An index can belong to a monograph, a critical edition, or a drama. Contributor metadata can describe an edited collection, a bilingual edition, or a scholarly edition. A margin object can be rendered beside the text in one profile and fall back into the reading stream in another.

## Feature handbook

- [Structural hierarchy](structural-hierarchy.md) — parts, chapters, sections, and the supported depth boundary.
- [Publication-unit and contributor metadata](publication-metadata.md) — chapter-like units, abstracts, keywords, DOI, contributors, affiliations, and roles.
- [Typography and page grid](typography-and-page-grid.md) — presentation roles, page geometry, and the boundary between semantic modules and layout.
- [Margins and side material](margins-and-side-material.md) — marginal notes, side captions, anchors, markers, and deterministic fallback.
- [Parallel text](parallel-text.md) — stable source/target segments, alignments, notes, locators, and layout modes.
- [Critical apparatus](apparatus.md) — textual, editorial, translation, commentary, and source streams.
- [Locators and stable addresses](locators.md) — canonical, dramatic-line, verse-line, and parallel-alignment address systems.
- [Verse and drama semantics](verse-and-drama.md) — stanzas, verse lines, speakers, speeches, stage directions, acts, and scenes.
- [Bibliography, index, and scholarly matter](bibliography-index-scholarly-matter.md) — reusable scholarly front/back matter and retrieval structures.
- [Multilingual text](multilingual-text.md) — language-aware text, Polytonic Greek, and transliteration support.

## How to read the policy tables

Feature pages reproduce profile policy only where a profile manifest explicitly declares it. The statuses mean:

- `required` — the profile depends on the capability;
- `recommended` — normally a good editorial fit, but not structurally mandatory;
- `optional` — supported when the project needs it;
- `discouraged` — technically possible but usually a poor default for that publication type;
- `incompatible` — reserved for a real semantic or technical coexistence conflict.

`not declared` does **not** mean incompatible. It means the current starter profile has no explicit policy entry for that module. These handbook tables are regression-checked against the public `profile.json` manifests so the prose cannot quietly become a second source of truth.

Presentation capabilities such as typography roles and the page grid are core/profile contracts rather than semantic modules, so they use presentation descriptors instead of module-policy status.
