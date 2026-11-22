---
title: Audit Evidence
description: Create and verify detached release-audit records and deterministic evidence-only export bundles without modifying publication releases.
---

# Audit evidence

Audit evidence is deliberately **detached** from the publication release it describes. This lets an auditor record later verification results without rewriting the release directory.

## Audit one release

```text
pse audit-release /path/to/release \
  --output /path/to/audits/release-audit.json
```

The output path must be outside the audited release.

Verify the audit record by itself:

```text
pse verify-audit-record /path/to/audits/release-audit.json --human
```

or re-bind it to the release during verification:

```text
pse verify-audit-record /path/to/audits/release-audit.json \
  --release-dir /path/to/release --human
```

## Audit a collection

For a directory whose immediate child directories are releases:

```text
pse audit-index /path/to/releases \
  --output /path/to/audits/audit-index.json --human
```

The index is path-independent evidence over the audited release set. Verify it detached or bind it back to a collection with `pse verify-audit-index` and `--collection-dir`.

## Export evidence

Create a deterministic ZIP containing audit evidence only:

```text
pse export-audit-evidence /path/to/audits/evidence.zip \
  /path/to/audits/release-audit.json \
  /path/to/audits/audit-index.json --human
```

The export does not contain publication PDFs. It is not a digital signature, PKI assertion, trusted timestamp, notarization service, or proof that an external repository preserved the files. Those require a separate trust layer.
