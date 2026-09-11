---
title: Historical Releases
description: Verify and assess legacy release evidence without inventing modern evidence or upgrading artifacts in place.
---

# Historical releases

Current PSE releases use release-manifest schema `0.2`. PSE retains verification-only compatibility for structurally valid legacy schema `0.1` releases.

The key rule is: **do not rewrite historical evidence to make it look current.** An old release cannot legitimately acquire an output-inspection report that did not exist at its original release time.

## Verify first

```text
pse verify-release /path/to/historical-release
```

A valid `0.1` release may verify with a legacy-schema warning. Unknown schema versions are rejected.

## Assess migration without mutation

Use:

```text
pse release-migration /path/to/historical-release --human
```

or write a separate assessment outside the historical release directory:

```text
pse release-migration /path/to/historical-release \
  --output /path/to/audits/release-migration-assessment.json
```

The assessment does not upgrade the release and does not infer missing historical inspection evidence.

If full current `0.2` evidence is required and the original source project still exists, preserve the historical artifact and create a **new release from source** using the current runtime. That creates new publication evidence rather than replacing history.
