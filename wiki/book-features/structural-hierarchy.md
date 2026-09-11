---
title: Structural hierarchy
description: Use bounded prose hierarchy without letting presentation profiles redefine semantic section depth.
---

# Structural hierarchy

Structural hierarchy represents the reusable prose structure of a publication: parts and chapters around a bounded section hierarchy. PSE keeps this semantic structure separate from the visual treatment of headings.

The current contract supports section depth through four levels. `Part` and `Chapter` sit outside that count. A fifth section level is rejected rather than silently flattened, because silent flattening can change the meaning and navigability of a manuscript.

## When to use it

Use structural hierarchy for books whose argument or exposition is organized through chapters and nested sections: monographs, edited collections, general prose books, and many scholarly editions. It is intentionally discouraged for poetry, drama, and literary fiction when their primary semantic structure is verse, dramatic structure, or narrative flow instead.

## Profile policy

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | required | on |
| [Basic Book](../profiles/basic-book.md) | required | on |
| [Bilingual Edition](../profiles/bilingual-edition.md) | recommended | on |
| [Critical Edition](../profiles/critical-edition.md) | recommended | on |
| [Drama](../profiles/drama.md) | discouraged | off |
| [Edited Collection](../profiles/edited-collection.md) | required | on |
| [Literary Fiction](../profiles/literary-fiction.md) | discouraged | off |
| [Poetry](../profiles/poetry.md) | discouraged | off |
| [Scholarly Edition](../profiles/scholarly-edition.md) | recommended | on |

## What it owns — and what it does not

The `structural-hierarchy` module owns **section-depth semantics and validation**. It does not own fonts, heading sizes, white space, page breaks, or running heads. Those belong to the profile/core presentation system.

A safe customization changes heading presentation while preserving the semantic level. Do not use a smaller font to simulate an extra unsupported section level.

## Practical rule

If the distinction must survive a redesign or a move to another presentation profile, model it semantically. If it is only a visual distinction, keep it in presentation configuration.

See also [Typography and page grid](typography-and-page-grid.md) and [Choose a Book Profile](../getting-started/choose-a-profile.md).
