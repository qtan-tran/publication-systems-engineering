---
title: Release Checklist
description: Use a compact human checklist before and immediately after creating a publication release.
---

# Release checklist

Use this as an operational reminder, not as a substitute for your organization’s editorial, legal, or accessibility procedures.

## Before release

- Canonical manuscript source contains all approved corrections.
- Publication metadata, contributor data, identifiers, bibliography/index material, and assets have been reviewed as applicable.
- `pse build .` succeeds.
- `pse check . --human` has no unresolved `error` findings.
- `warning` and `review` findings have been investigated by the responsible person.
- The working PDF has received visual and editorial review.
- Output language and other expected PDF properties have been inspected where relevant.
- Rights, privacy, permissions, and organization-specific publication approvals have been handled outside PSE where required.

## Create and verify

```text
pse release .
pse verify-release release/<release-id>
```

If accepted human-review findings remain, use `--acknowledge-review` only after that review has actually occurred.

## After release

- Preserve the complete release directory, not only the PDF.
- Distribute/deposit the release artifact intended for publication, not `build/book.pdf` or a recipient proof.
- If independent audit evidence is needed, create it outside the release directory.
- Do not edit evidence files in place after publication; create a new release from canonical source for corrections.
