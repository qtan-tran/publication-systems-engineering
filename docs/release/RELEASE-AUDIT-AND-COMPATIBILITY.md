# Release audit records and compatibility fixtures

PSE treats a publication release as an immutable historical artifact. Auditing a release must therefore produce **new evidence outside the release directory**, not rewrite or silently upgrade the release itself.

## Audit a release

```text
pse audit-release /path/to/release
```

The JSON emitted to stdout records the observed release ID and schema, manifest SHA-256, PDF SHA-256, checksum-file SHA-256 when present, schema compatibility, and the full `verify-release` result.

To retain that audit evidence:

```text
pse audit-release /path/to/release --output /path/to/audits/release-audit.json
```

PSE rejects an `--output` path inside the release directory. The audit record states both:

```text
historical_artifact_mutated: false
audit_record_is_release_artifact: false
```

An audit record describes what the current runtime observed. It is **not** a migration, signature, accessibility certificate, or replacement release manifest.

## Release schema compatibility

Current PSE creates release-manifest schema `0.2`. Schema `0.1` remains verification-only legacy material. An audit of `0.1` preserves that distinction and does not infer output-inspection evidence retroactively.

Use `pse release-migration` when the question is whether a historical release can be brought to the current evidence model. Use `pse audit-release` when the question is whether a release, as it exists now, verifies under the installed compatibility policy.

## Frozen synthetic fixture corpus

`tests/fixtures/releases/` contains two public synthetic fixtures:

- `schema-0.1/` - a legacy release with manifest, PDF and checksum file, but no output-inspection evidence;
- `schema-0.2/` - a current-contract release whose output-inspection record is bound to the PDF SHA-256.

These fixtures are deliberately small and contain no private publication content. Regression tests use them as frozen historical-style inputs so compatibility behavior is tested against stable artifacts rather than only temporary in-memory cases.

The corpus is a testing contract, not an example of how to hand-author release artifacts. Normal users should create releases with `pse release`.

## Portable release fingerprint

Audit-record schema `0.2` adds `release_fingerprint`. It is calculated from canonical release-state inputs: release ID, manifest schema version, manifest SHA-256, PDF SHA-256, and checksum-file SHA-256 when present. Absolute filesystem paths and audit timestamps are excluded. Copying an unchanged release to another directory therefore preserves its fingerprint.

`source_release_dir` remains useful audit context, but it is informational only and is never part of release identity. A changed manifest, PDF, or checksum file changes the fingerprint. This is a content fingerprint, not a digital signature or trusted timestamp.

## Batch audit index

For a directory whose immediate child directories are releases, run:

```text
pse audit-index /path/to/release-collection --output /path/to/audits/index.json
```

The index contains one portable release fingerprint per audited release and a `batch_fingerprint` calculated from the sorted release fingerprints. The batch fingerprint remains stable if the unchanged collection is moved to another filesystem location. The index must remain outside every audited release directory.

A failing release still appears in the index with `audit_status: fail`, and the batch status becomes `fail`; PSE does not normalize or repair it. The index is audit evidence, not part of any publication release.
