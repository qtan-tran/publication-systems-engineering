---
title: Release Verification
description: Verify that an existing release still matches its manifest, PDF contract, output-inspection evidence, and checksums.
---

# Release verification

Run:

```text
pse verify-release /path/to/release
```

For a current manifest schema `0.2` release, verification checks the public release-manifest contract, final PDF checksum, page count and geometry, output-inspection contract and PDF-hash binding, and `SHA256SUMS.txt` evidence.

A pass means the checked artifacts satisfy those recorded contracts under the installed verifier. It does not independently validate editorial correctness, rights clearance, accessibility certification, or archival repository status.

## Contract discovery

Auditors and tooling can inspect the installed public schema surface with:

```text
pse contracts
pse contracts --json
```

This resolves the active runtime rather than assuming a source checkout.

## If verification fails

Do not make the manifest “match” by manually refreshing hashes or editing evidence files. Investigate whether the release is incomplete, corrupted, altered, or unsupported. If a publication must be corrected, return to canonical source and create a new release through the normal release pipeline.

For verification-only support of legacy schema `0.1`, see [Historical releases](historical-releases.md).
