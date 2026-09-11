---
title: Typography and page grid
description: Understand the core presentation contracts for typographic roles and stable page geometry.
---

# Typography and page grid

Typography and page geometry are **presentation contracts**, not semantic modules. PSE keeps them at the core/profile layer so a semantic feature can survive a visual redesign.

## Typography roles

PSE defines named roles for body text, display text, chapter titles, section and subsection headings, metadata labels and values, running heads, captions, and apparatus. Profiles override the values of those roles rather than redefining the semantic feature that consumes them.

For example, an apparatus note consumes the apparatus typography role. The apparatus module does not choose the book's typeface.

For project-local changes, use the supported local configuration boundary rather than editing the shared core. See [Typography customization](../customization/typography.md).

## Page grid

The page-grid contract resolves inner gutter, outer margin zone, top and bottom zones, header dimensions, footer separation, apparatus allocation, and the primary text measure **before composition starts**. Semantic modules may consume those regions but must not dynamically resize the page grid after composition begins.

Current profile grid modes come from `presentation.json`:

| Profile | Grid mode | Side-material mode |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | `asymmetric-scholarly` | `outer-margin` |
| [Basic Book](../profiles/basic-book.md) | `book` | `fallback` |
| [Bilingual Edition](../profiles/bilingual-edition.md) | `asymmetric-scholarly` | `outer-margin` |
| [Critical Edition](../profiles/critical-edition.md) | `asymmetric-scholarly` | `outer-margin` |
| [Drama](../profiles/drama.md) | `asymmetric-scholarly` | `outer-margin` |
| [Edited Collection](../profiles/edited-collection.md) | `book` | `fallback` |
| [Literary Fiction](../profiles/literary-fiction.md) | `book` | `fallback` |
| [Poetry](../profiles/poetry.md) | `book` | `fallback` |
| [Scholarly Edition](../profiles/scholarly-edition.md) | `asymmetric-scholarly` | `outer-margin` |

A profile's grid mode describes its presentation baseline; it does not imply that every title must retain identical measurements. See [Page Layout customization](../customization/page-layout.md).

## Design boundary

Use semantic modules to describe meaning. Use typography roles and the grid to decide how that meaning is presented. Keeping this boundary clean is what allows PSE to change the look of a book without rewriting its scholarly structure.
