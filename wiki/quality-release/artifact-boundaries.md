---
title: Working PDF, Proof, and Release
description: Distinguish iteration output, recipient-specific review artifacts, and the evidence-bearing publication release.
---

# Working PDF, proof, and release

These PDFs may look similar on screen, but they have different lifecycle meanings.

| Artifact | Created by | Typical location | Purpose |
| --- | --- | --- | --- |
| Working PDF | `pse build .` | `build/book.pdf` | local iteration and review |
| Recipient proof | `pse proof . --recipient ...` | `build/proofs/` | controlled external/internal review with recipient identity |
| Publication release | `pse release .` | `release/<release-id>/` | final evidence-bearing publication artifact boundary |

## Working PDF

A working PDF is disposable build output. Rebuild it as the project changes. Do not deposit or archive it as though it were the release contract.

## Recipient proof

A proof is tied to a named recipient/proof identity and is watermarked for deterrence and traceability. It is not a clean release and it may still contain content awaiting correction.

## Publication release

A release is created independently through release gates. Its PDF is bound to machine-readable evidence and checksums. A release is **not** “the proof without a watermark,” and a proof is **not** “a release with an extra mark.”

This distinction prevents accidental distribution of the wrong lifecycle artifact and makes later verification meaningful.
