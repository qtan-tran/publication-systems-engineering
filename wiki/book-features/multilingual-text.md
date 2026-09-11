---
title: Multilingual text
description: Handle language-aware text and scholarly language features without turning every multilingual passage into a parallel edition.
---

# Multilingual text

The `multilingual` module provides language-aware text support, including Polytonic Greek and transliteration capability. It is intended for books that need reliable multilingual composition inside a single publication structure.

## Profile policy

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

Critical Edition and Scholarly Edition currently require multilingual support because their starter architecture is designed for source-oriented scholarly material that may include original-language text.

`not declared` does not mean that another profile can never contain another language. It means the current profile manifest does not expose the multilingual module as an explicit starter-policy commitment.

## Multilingual text vs parallel text

Use multilingual text when languages occur within the same semantic flow: quotations, lemmas, original-language terms, transliterations, or passages in another language.

Use [Parallel text](parallel-text.md) when source and target segments must remain explicitly aligned as corresponding publication units across layout changes.

## Boundary

The multilingual module provides production semantics and language capabilities. It does not certify a translation, validate transliteration scholarship, or determine editorial language policy.
