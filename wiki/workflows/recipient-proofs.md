---
title: Recipient Proofs
description: Create recipient-specific review artifacts without confusing proofs with working PDFs or publication releases.
---

# Recipient proofs

Use a proof when a specific person or organization needs a controlled review copy:

```text
pse proof . --recipient "Recipient Name"
```

An email address may be recorded in the local proof manifest:

```text
pse proof . --recipient "Recipient Name" --email recipient@example.org
```

PSE creates a recipient-specific watermarked PDF under `build/proofs/` together with provenance/checksum information. Each proof receives a `proof_id`; you may supply a stable one with `--proof-id`, otherwise PSE generates it.

## A proof is not a release

A recipient proof is a distribution artifact for review. It may contain visible recipient and proof identifiers and may still represent a publication that is changing.

A publication release is a separately authorized lifecycle state created by `pse release`. Do not “make a release” by removing a proof watermark or renaming a working PDF.

## Watermarking boundary

The proof watermark supports deterrence and traceability. PSE does not claim it is unremovable DRM. A person who can view a PDF can potentially rasterize, print/scan, recreate, or edit it.

Generate separate proofs for separate external recipients when traceability matters. Recipient manifests can contain personal data and belong in controlled private storage, not in a public repository.

When corrections return, apply them to canonical source, rebuild, check, and issue a new proof if another review round is required.

Next: [Prepare a publication release](publication-release.md).
