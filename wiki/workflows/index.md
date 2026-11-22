---
title: Production Workflows
description: Use a short everyday workflow; invoke proofs and release checks only when needed.
---

# Production workflows

PSE supports one ordinary editing loop and two optional production handoffs. You do **not** need to perform release-engineering procedures after each manuscript edit.

| Situation | What to run | Where to read more |
| --- | --- | --- |
| Editing or correcting your book | `pse build .` → `pse check .` → human visual review | [Edit–build–check](edit-build-check.md) |
| Sending a review copy | `pse proof . --recipient "Recipient Name"` | [Recipient proofs](recipient-proofs.md) |
| Approved final publication | `pse release .` → `pse verify-release <release-directory>` | [Publication release](publication-release.md) |

**When troubleshooting**, use [clean rebuilds](clean-build.md). [Human review](human-review.md) remains necessary for scholarly accuracy and page quality. [After-release verification](after-release.md) and release-evidence machinery are for archiving, audit and maintainers, not daily editorial work.

Fix the canonical manuscript, not files inside `build/` or `release/`. Keep unpublished project directories outside the public PSE source repository.
