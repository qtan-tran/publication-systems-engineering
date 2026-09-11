---
title: Quality and Release
description: Understand PSE finding levels, output inspection, artifact boundaries, release verification, and detached audit evidence.
---

# Quality and release

PSE separates several kinds of evidence because they answer different questions:

```text
machine QA          → did declared project checks find blocking problems?
human review        → did people examine editorial and visual questions?
output inspection   → does the finished PDF meet the limited technical baseline?
release contract    → which exact PDF and evidence constitute this release?
release verification→ does that release still match its recorded contract?
audit evidence      → what can be recorded and checked later without mutating it?
```

None of these layers, alone or together, is a claim that a book is error-free, legally cleared, accessible under a particular law, PDF/UA-conformant, archival to a particular standard, or intellectually correct.

## Start here

- [Quality model](quality-model.md) — `error`, `warning`, `review`, and `info`.
- [Working PDF, proof, and release](artifact-boundaries.md) — three artifacts with three different purposes.
- [Output inspection](output-inspection.md) — the finished-PDF baseline and its limits.
- [Release verification](release-verification.md) — verify the manifest, PDF binding, geometry, inspection evidence, and checksums.
- [Audit evidence](audit-evidence.md) — detached release audit records, indexes, verification, and deterministic evidence export.
- [Historical releases](historical-releases.md) — preserve legacy evidence rather than rewriting history.
- [Release checklist](release-checklist.md) — a compact human sign-off sequence.
