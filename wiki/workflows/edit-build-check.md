---
title: Everyday Edit–Build–Check Cycle
description: Use the shortest safe production loop while manuscript and presentation are still changing.
---

# Everyday edit–build–check cycle

During ordinary editorial work, use this loop:

```text
edit canonical source
      ↓
pse build .
      ↓
pse check . --human
      ↓
inspect build/book.pdf
      ↓
fix source and repeat
```

`pse build .` creates the working PDF at `build/book.pdf`. `pse check . --human` runs machine QA against the project without rewriting manuscript source.

## What belongs in source

Treat these as the project’s editable source of truth:

- `book.yml` — publication metadata;
- `content/` — manuscript and structured publication content;
- `config/` — project configuration;
- `config/pse-local.tex` — sanctioned title-local presentation overrides;
- project-owned images, bibliographic data, and other declared assets.

Treat `build/`, `build/proofs/`, and `release/` as generated boundaries. Do not correct a typo by editing a generated PDF, `.tex` bridge, release manifest, or checksum file.

## When a build succeeds

A successful build means the compilation pipeline produced a PDF. It does **not** mean that the book is editorially correct, visually approved, accessible, archival, legally cleared, or ready for publication.

After every material edit, inspect the resulting pages that could have changed: headings near page breaks, notes, tables, illustrations, indexes, parallel text, apparatus, running heads, and the final pages of chapters are common places for layout consequences to surface.

## When a check reports findings

Fix `error` findings before proceeding. Investigate `warning` findings. Read `review` findings as an explicit request for human judgement rather than as an automatic failure or automatic approval.

Next: [Human review](human-review.md). If generated state may be stale, use a [clean build](clean-build.md).
