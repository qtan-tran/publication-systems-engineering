---
title: Parallel text
description: Keep source/target alignment stable while switching among bilingual presentation modes.
---

# Parallel text

Parallel text represents source and target segments as stable semantic objects and connects them through explicit alignment relations. PSE does not infer alignment merely because two paragraphs happen to appear opposite one another on a page.

A bilingual project can therefore change presentation without rewriting its segment IDs or alignments.

## Semantic model

The module keeps source/target segments, stable alignment IDs, optional alignment locators, and typed notes. Translation-note compatibility is retained for older projects.

## Presentation modes

The Bilingual Edition profile supports five presentation modes over the same semantic source:

- `parallel-columns`;
- `facing-pages`;
- `sequential-blocks`;
- `source-dominant`;
- `target-dominant`.

Changing mode must not rewrite `content/parallel.tex` or turn page/column position into semantic identity.

## Profile policy

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | not declared | — |
| [Basic Book](../profiles/basic-book.md) | not declared | — |
| [Bilingual Edition](../profiles/bilingual-edition.md) | required | on |
| [Critical Edition](../profiles/critical-edition.md) | not declared | — |
| [Drama](../profiles/drama.md) | not declared | — |
| [Edited Collection](../profiles/edited-collection.md) | not declared | — |
| [Literary Fiction](../profiles/literary-fiction.md) | not declared | — |
| [Poetry](../profiles/poetry.md) | not declared | — |
| [Scholarly Edition](../profiles/scholarly-edition.md) | not declared | — |

Only Bilingual Edition currently declares `parallel-text` as required in its starter policy. Absence from another profile's policy is not an incompatibility declaration; it means PSE does not currently advertise that module as part of that profile's supported starter policy surface.

## Use it when

Use parallel text when correspondence between source and target units matters editorially. If you merely quote another language occasionally, use multilingual text instead of constructing an alignment model.

For stable address systems used by aligned units, see [Locators and stable addresses](locators.md).
