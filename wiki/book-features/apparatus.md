---
title: Critical apparatus and note streams
description: Model apparatus meaning independently from the visual label or placement used by a publication profile.
---

# Critical apparatus and note streams

An apparatus connects scholarly note material to a stable place in the text. PSE distinguishes **what kind of note it is** from **how that note is presented**.

The apparatus module recognizes five semantic streams:

- `textual` — readings and textual-critical decisions;
- `editorial` — editorial interventions or explanations;
- `translation` — translation-oriented notes;
- `commentary` — interpretive or explanatory commentary;
- `source` — source/witness or source-oriented information.

A presentation may render those streams with full labels, abbreviations, or labels such as A/B/C without changing their semantic identities.

## Profile policy

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | optional | off |
| [Basic Book](../profiles/basic-book.md) | discouraged | off |
| [Bilingual Edition](../profiles/bilingual-edition.md) | recommended | off |
| [Critical Edition](../profiles/critical-edition.md) | required | on |
| [Drama](../profiles/drama.md) | recommended | off |
| [Edited Collection](../profiles/edited-collection.md) | optional | off |
| [Literary Fiction](../profiles/literary-fiction.md) | discouraged | off |
| [Poetry](../profiles/poetry.md) | optional | off |
| [Scholarly Edition](../profiles/scholarly-edition.md) | required | on |

Critical Edition and Scholarly Edition require and enable apparatus support. Bilingual Edition and Drama recommend it but leave it off until needed. Academic Monograph, Edited Collection, and Poetry permit it as an optional capability. Basic Book and Literary Fiction discourage it as a starter convention.

## Stable locators first

An apparatus is only as reliable as the address to which it points. Prefer semantic locators over PDF page numbers so the note remains attached when pagination changes.

The legacy generic apparatus commands remain supported, so an older PSE project does not have to classify every existing note into a stream before it can build.

## Boundary

The apparatus module owns note-stream semantics and locator/range validation. Typography, labels, foot/margin placement, and page allocation belong to presentation contracts.

Continue with [Locators and stable addresses](locators.md) or [Margins and side material](margins-and-side-material.md).
