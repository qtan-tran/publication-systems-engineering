---
title: Output Inspection
description: Inspect finished-PDF metadata, navigation, and text extractability without making unsupported accessibility claims.
---

# Output inspection

Inspect a built PDF directly:

```text
pse inspect-output build/book.pdf --expected-language en --human
```

or point the command at a project directory:

```text
pse inspect-output . --expected-language en
```

The current baseline checks PDF readability, relevant title/author metadata, document language, bookmarks/navigation, and text extractability. A JSON report can be written with `--output`.

## What output inspection does not certify

PSE does not currently certify tagged-PDF structure, reading order, image alternative text, PDF/UA, WCAG, archival conformance, or legal accessibility compliance. Those remain explicit review/conformance layers outside the current automated baseline.

## Release binding

For current schema `0.2` releases, `pse release` runs the output-inspection baseline against the final publication PDF and stores `output-inspection.json` in the release directory. The release manifest records the inspection file hash and the exact final-PDF SHA-256 to which the inspection applies.

`pse verify-release` re-checks that binding, so replacing the PDF while keeping an old inspection report is detectable.
