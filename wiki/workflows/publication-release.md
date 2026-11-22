---
title: Prepare a Publication Release
description: Promote an approved project through PSE release gates rather than treating a working PDF as the publication artifact.
---

# Prepare a publication release

Create a publication release only after editorial and visual review are complete enough for your release policy.

From the project root:

```text
pse release .
```

If the machine report contains only human-reviewed `review` findings that you intentionally accept:

```text
pse release . --acknowledge-review
```

The release operation is a gated promotion, not an alias for `pse build`.

## What the release boundary does

PSE rebuilds from a clean generated boundary, runs the required QA and output-inspection gates, verifies mandatory attribution evidence, writes the final publication PDF and evidence files into a release directory, and binds those artifacts through the release manifest and checksums.

The release directory—not `build/book.pdf`—is the publication artifact boundary.

Current releases use publication release manifest schema `0.2`. The manifest binds the final PDF to its SHA-256, page count/geometry, QA evidence, mandatory attribution evidence, `output-inspection.json`, and `SHA256SUMS.txt`.

## Optional deterministic-build epoch

Release managers who need to control the deterministic build epoch can use:

```text
pse release . --source-date-epoch 1700000000
```

When omitted, PSE uses the supported project/runtime fallback described by the release implementation. Do not invent or backdate an epoch merely to make a release appear older than it is.

## Immediately verify the release

After creation, run:

```text
pse verify-release release/<release-id>
```

Verification checks the release contract, artifact hashes, PDF structure, checksum evidence, and current-schema output-inspection binding.

Continue with [Verify a release](../quality-release/release-verification.md).
