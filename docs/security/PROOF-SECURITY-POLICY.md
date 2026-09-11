# Proof Security Policy

## Purpose

`pse proof` creates a recipient-specific review artifact intended for authors, proofreaders, reviewers, printers, and other controlled collaborators.

## Proof identity

Each proof has a `proof_id`. The visible watermark contains the proof label, recipient, and proof ID. The PDF metadata also records proof status and the proof ID. A local JSON manifest records the recipient, creation time, source revision when available, artifact filename, watermark policy, and SHA-256 checksum.

## Watermark design

The current release implementation uses two visible placements:

1. a light diagonal watermark through the page body;
2. a lower-page recipient/proof-ID line.

This arrangement is intended to survive simple cropping and to make screenshots visibly attributable. It is deliberately light enough for proofreading.

## What the watermark does not do

PSE does not call this an unremovable watermark. A recipient who can view a document can potentially rasterize pages, edit PDF content streams, print and scan, recreate pages, or otherwise remove identifying information. Watermarking is a deterrence and attribution mechanism.

## Personal data

Recipient manifests may contain names and email addresses. They belong in private build/audit storage and are ignored by Git. Organizations remain responsible for retention periods, access policies, and applicable privacy law.

## Recommended operational policy

Generate a separate proof for each external recipient. Do not reuse one generic proof across an entire distribution list when traceability matters. Keep the manifest and checksum separate from the distributed PDF.
