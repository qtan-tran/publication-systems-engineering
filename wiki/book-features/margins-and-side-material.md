---
title: Margins and side material
description: Represent side material semantically and preserve it through deterministic fallback when margin placement is unavailable.
---

# Margins and side material

PSE can represent material that may appear beside the main text without making “in the margin” part of the object's semantic identity.

The `margin-objects` module provides stable IDs for five object types: marginal notes, side captions, apparatus anchors, locator markers, and running-side objects. A profile or project decides whether those objects appear in the outer margin or use the visible fallback presentation in the main reading stream.

That fallback is important: PSE does not silently discard semantic content because a page design lacks sufficient side space.

## Profile policy

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | recommended | off |
| [Basic Book](../profiles/basic-book.md) | optional | off |
| [Bilingual Edition](../profiles/bilingual-edition.md) | recommended | off |
| [Critical Edition](../profiles/critical-edition.md) | recommended | on |
| [Drama](../profiles/drama.md) | recommended | off |
| [Edited Collection](../profiles/edited-collection.md) | optional | off |
| [Literary Fiction](../profiles/literary-fiction.md) | optional | off |
| [Poetry](../profiles/poetry.md) | optional | off |
| [Scholarly Edition](../profiles/scholarly-edition.md) | recommended | on |

Critical and Scholarly Editions enable margin objects by default. Several other profiles recommend or permit them but leave them off in the starter so the manuscript does not acquire side material it does not actually need.

## When to use a margin object

Use one when the content has a stable editorial identity that should survive presentation changes. Do not use it merely to push ordinary prose sideways for visual effect.

Typical cases include a concise marginal gloss, a side caption attached to a figure-like object, a locator marker, or a semantic apparatus anchor.

## Presentation and accessibility boundary

Outer-margin placement is a visual choice. It does not by itself establish tagged-PDF reading order or accessibility conformance. When margin placement is unavailable, the default contract keeps the object visible in the primary reading stream rather than pretending the content is optional.

For page geometry, see [Typography and page grid](typography-and-page-grid.md).
