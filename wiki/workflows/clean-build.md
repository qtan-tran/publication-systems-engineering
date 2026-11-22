---
title: Clean Build and Reproducibility
description: Remove generated state and confirm that a project can be rebuilt from canonical source.
---

# Clean build and reproducibility

A clean build is useful before an important proof, after configuration changes, after switching machines, or whenever you suspect stale intermediates are affecting output.

Run:

```text
pse clean .
pse build .
pse check . --human
```

`pse clean` removes generated build artifacts while preserving canonical source and user assets. The purpose is not cosmetic housekeeping; it tests whether the project can reconstruct its working output from declared source and configuration.

## What a clean build can tell you

A successful clean rebuild gives evidence that the current project does not depend on a leftover generated file from an earlier run. It does not prove that two different operating systems or TeX installations will produce byte-identical PDFs unless the relevant environment and deterministic-build conditions are also controlled.

Before a publication release, PSE’s release pipeline performs its own clean generated-boundary rebuild and applies release gates. You do not need to turn a working `build/book.pdf` into a release manually.

## Do not clean away provenance you intend to preserve

Recipient proofs and publication releases have a different lifecycle from disposable working intermediates. Preserve release directories and any audit evidence according to your organization’s records policy rather than treating them as temporary build cache.

Next: [Prepare a publication release](publication-release.md).
