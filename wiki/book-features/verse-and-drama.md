---
title: Verse and drama semantics
description: Use publication-specific semantic structures for verse and dramatic texts instead of forcing them into generic prose hierarchy.
---

# Verse and drama semantics

Poetry and drama often need semantic structures that are more specific than chapters and nested prose headings. PSE therefore keeps verse and dramatic structure in dedicated reusable modules.

## Verse structure

`verse-structure` owns stanzas, semantic verse lines, and stable verse-line IDs. A physical wrapped line is **not** a new semantic verse line. Optional display labels remain separate from stable machine identity.

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | not declared | — |
| [Basic Book](../profiles/basic-book.md) | not declared | — |
| [Bilingual Edition](../profiles/bilingual-edition.md) | not declared | — |
| [Critical Edition](../profiles/critical-edition.md) | not declared | — |
| [Drama](../profiles/drama.md) | not declared | — |
| [Edited Collection](../profiles/edited-collection.md) | not declared | — |
| [Literary Fiction](../profiles/literary-fiction.md) | not declared | — |
| [Poetry](../profiles/poetry.md) | required | on |
| [Scholarly Edition](../profiles/scholarly-edition.md) | not declared | — |

The Poetry profile requires and enables verse structure by default.

## Drama structure

`drama-structure` owns speakers, speeches, stage directions, acts/scenes, and related dramatic structure.

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | not declared | — |
| [Basic Book](../profiles/basic-book.md) | not declared | — |
| [Bilingual Edition](../profiles/bilingual-edition.md) | not declared | — |
| [Critical Edition](../profiles/critical-edition.md) | not declared | — |
| [Drama](../profiles/drama.md) | required | on |
| [Edited Collection](../profiles/edited-collection.md) | not declared | — |
| [Literary Fiction](../profiles/literary-fiction.md) | not declared | — |
| [Poetry](../profiles/poetry.md) | not declared | — |
| [Scholarly Edition](../profiles/scholarly-edition.md) | not declared | — |

The Drama profile requires and enables dramatic structure. It also requires `dramatic-locators` for stable dramatic line addressing:

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | not declared | — |
| [Basic Book](../profiles/basic-book.md) | not declared | — |
| [Bilingual Edition](../profiles/bilingual-edition.md) | not declared | — |
| [Critical Edition](../profiles/critical-edition.md) | not declared | — |
| [Drama](../profiles/drama.md) | required | on |
| [Edited Collection](../profiles/edited-collection.md) | not declared | — |
| [Literary Fiction](../profiles/literary-fiction.md) | not declared | — |
| [Poetry](../profiles/poetry.md) | not declared | — |
| [Scholarly Edition](../profiles/scholarly-edition.md) | not declared | — |

## Why not model these as headings?

A speaker cue is not a section heading; a stage direction is not a paragraph style; a stanza is not merely a visually separated prose block. Encoding these structures semantically gives QA and presentation systems something reliable to work with.

Use the [Poetry profile](../profiles/poetry.md) or [Drama profile](../profiles/drama.md) as the default starting point when these structures define the work.
