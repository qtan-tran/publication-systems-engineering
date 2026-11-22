# Audit evidence verification and deterministic export

PSE audit evidence is intentionally separate from publication release artifacts. Version 1.30 adds two verification commands and one deterministic export command without rewriting historical releases.

## Verify an audit record

Detached contract verification:

```text
pse verify-audit-record audit-record.json
```

Optional re-binding to an observed release directory:

```text
pse verify-audit-record audit-record.json --release-dir /path/to/release
```

Detached verification checks the audit-record contract and portable fingerprint consistency. With `--release-dir`, PSE additionally recomputes the current manifest, PDF, checksum-file hashes, and release fingerprint. A moved but unchanged release still matches because absolute paths are excluded from the portable identity.

## Verify an audit index

Detached:

```text
pse verify-audit-index audit-index.json
```

With a release collection:

```text
pse verify-audit-index audit-index.json --collection-dir /path/to/releases
```

The second form verifies every indexed immediate-child release against the fingerprints and hashes recorded in the index. The index file itself remains external evidence and is never inserted into a publication release.

## Deterministic audit-evidence export

```text
pse export-audit-evidence audit-evidence.zip audit-record.json audit-index.json
```

The ZIP contains only audit evidence and `audit-evidence-bundle-manifest.json`. For identical evidence bytes and filenames, export ordering, ZIP timestamps, file permissions, compression method, manifest serialization, and resulting ZIP bytes are deterministic. Input argument order does not affect the result.

The bundle manifest records each evidence file's SHA-256 and a bundle fingerprint. It explicitly states that publication release artifacts are not included.

The export is **not** a digital signature, PKI assertion, trusted timestamp, notarization service, or proof that an external repository preserved the files. Cryptographic signing and trusted timestamping require a separate trust layer.
