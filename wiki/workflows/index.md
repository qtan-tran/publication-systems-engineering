---
title: Production Workflows
description: Follow PSE from canonical source through build, QA, human review, proofing, and release without confusing generated artifacts with source.
---

# Production workflows

PSE treats book production as a sequence of controlled states rather than a single “make PDF” action. The ordinary production path is:

```text
canonical source
      ↓
build working PDF
      ↓
machine QA
      ↓
human editorial + visual review
      ↓
recipient proof when needed
      ↓
publication release
      ↓
release verification
```

The most important rule is simple: **fix the source that produced a problem; do not patch generated artifacts by hand.** Files in `build/` and `release/` are outputs of the production system, not canonical manuscript source.

## Choose the workflow you need

- [Everyday edit–build–check cycle](edit-build-check.md) — the normal loop while a book is still changing.
- [Clean build and reproducibility](clean-build.md) — when you need to eliminate stale generated state and verify that the project rebuilds from source.
- [Human review](human-review.md) — what machine QA cannot decide for you.
- [Recipient proofs](recipient-proofs.md) — controlled review PDFs for authors, proofreaders, reviewers, printers, or other named recipients.
- [Prepare a publication release](publication-release.md) — move from an approved project state to a release artifact through the release gates.
- [After release](after-release.md) — verify, preserve, and audit an existing release without rewriting it.

For the meaning of `error`, `warning`, `review`, output inspection, release evidence, and audit records, continue to [Quality and Release](../quality-release/index.md).
