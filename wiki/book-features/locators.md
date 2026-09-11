---
title: Locators and stable addresses
description: Coordinate distinct locator systems without converting their semantic identities into page numbers or each other.
---

# Locators and stable addresses

A locator is a stable way to address a meaningful place in a publication without depending on the current PDF page number. Different publication types need different locator semantics, so PSE keeps their engines separate and coordinates them through a common policy layer.

Current locator namespaces are:

- `canonical` — canonical source locations owned by `canonical-locators`;
- `dramatic-line` — line addresses owned by `dramatic-locators`;
- `verse-line` — stable verse-line identities owned by `verse-structure`;
- `parallel-alignment` — aligned-unit addresses owned by `parallel-text`.

Locator orchestration chooses a primary namespace, optional secondary namespaces, visible-numbering behavior, and the stable-ID policy. It **does not convert** one locator type into another.

## Canonical locator policy

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | not declared | — |
| [Basic Book](../profiles/basic-book.md) | not declared | — |
| [Bilingual Edition](../profiles/bilingual-edition.md) | not declared | — |
| [Critical Edition](../profiles/critical-edition.md) | required | on |
| [Drama](../profiles/drama.md) | not declared | — |
| [Edited Collection](../profiles/edited-collection.md) | not declared | — |
| [Literary Fiction](../profiles/literary-fiction.md) | not declared | — |
| [Poetry](../profiles/poetry.md) | not declared | — |
| [Scholarly Edition](../profiles/scholarly-edition.md) | required | on |

## Dramatic locator policy

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

`verse-line` and `parallel-alignment` addresses are capabilities of their owning modules rather than separate module-policy entries. See [Verse and drama semantics](verse-and-drama.md) and [Parallel text](parallel-text.md).

## Stable ID vs visible label

A stable semantic ID and the label printed for a reader are not the same thing. A verse line can keep a machine ID such as `l17` while displaying `17`, another source-defined label, or no visible label at all. A redesign therefore does not require rewriting the address space.

## Use locators for references, not pagination hacks

If a note, cross-reference, or scholarly argument must survive reflow and repagination, address the semantic unit rather than hard-coding the final page number into manuscript logic.
