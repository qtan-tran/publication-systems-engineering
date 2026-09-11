---
title: After Release
description: Verify, preserve, and audit publication releases without mutating historical artifacts.
---

# After release

Treat a publication release as evidence-bearing output. Do not edit its PDF, manifest, QA report, inspection report, or checksum file in place to “fix” history.

## Verify before distribution or deposit

Run:

```text
pse verify-release release/<release-id>
```

If verification fails, investigate the source project and release process. Releasing again from canonical source is different from modifying the failed release directory.

## Preserve the release boundary

Keep the release directory intact according to your publication and records policy. If you later need a new corrected edition or corrected release, create a new release from source with its own release identity and evidence.

## Create detached audit evidence when needed

For a current or historical release:

```text
pse audit-release /path/to/release --output /path/to/audits/release-audit.json
```

The audit record must live outside the audited release. It records verification-derived evidence without mutating the release itself.

For collections, PSE also supports `pse audit-index`; detached audit records/indexes can be verified and packaged into an evidence-only deterministic ZIP. See [Audit evidence](../quality-release/audit-evidence.md).

For older release-manifest schema `0.1`, do not manufacture missing modern evidence. See [Historical releases](../quality-release/historical-releases.md).
