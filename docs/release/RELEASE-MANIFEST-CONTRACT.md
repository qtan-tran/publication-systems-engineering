# Publication release manifest contract

PSE 1.26 consolidates the publication-release evidence contract around **release manifest schema 0.2**. New releases are always written as schema `0.2`.

The normative public documentation schemas are:

- `schema/release-manifest-0.2.schema.json`;
- `schema/output-inspection-0.2.schema.json`.

Runtime validation is implemented in `pse_cli.release_contract`; the JSON Schema files document the same public surface and are shipped with the installed runtime.

## Current 0.2 contract

A release manifest binds the final PDF to:

- its SHA-256, page count, and geometry;
- QA and reproducibility evidence;
- mandatory attribution evidence;
- `output-inspection.json`, including that file's SHA-256;
- the exact final-PDF SHA-256 recorded inside the output-inspection evidence;
- the release inspection policy;
- `SHA256SUMS.txt` covering the PDF, manifest, QA report, and inspection report.

`pse release` validates the generated manifest, inspection report, and their PDF-hash binding before it writes the final release contract. `pse verify-release` revalidates those contracts in addition to checking artifact hashes and PDF geometry. Refreshing checksums therefore cannot make a structurally invalid 0.2 manifest valid.

Artifact filenames recorded in the manifest must be single safe filenames; path traversal is rejected by the contract validator.

## Legacy schema 0.1

`pse verify-release` retains **verification-only compatibility** for publication release manifest schema `0.1`. This is intentionally asymmetric:

- PSE never creates new `0.1` publication releases;
- a structurally valid `0.1` manifest may still be checked for its PDF contract and checksum evidence;
- verification emits `legacy_release_manifest_schema` as a warning;
- output-inspection evidence is not required for `0.1` and is not inferred retroactively;
- an unknown schema version is rejected.

This preserves the ability to inspect earlier PSE release artifacts without weakening the current `0.2` release contract.

## Accessibility boundary

Output-inspection binding is evidence, not accessibility certification. The release contract does not claim PDF/UA, WCAG, archival, or legal accessibility conformance. See [Output inspection and accessibility baseline](../getting-started/OUTPUT-INSPECTION-ACCESSIBILITY.md).


## Installed contract discovery

Use:

```text
pse contracts
pse contracts --json
```

The command resolves the **active runtime**, not an assumed source checkout, and reports the installed schema paths for the current publication-release manifest and output-inspection contracts. This gives auditors and external tooling a stable way to locate the normative machine-readable schema files after normal package installation.

For the publication-release manifest, the installed surface explicitly distinguishes:

- schema `0.2`: current creation + strict verification contract;
- schema `0.1`: legacy verification-only compatibility;
- unknown versions: rejected.

## Legacy migration assessment

A historical `0.1` artifact must not be rewritten merely to resemble a `0.2` artifact. In particular, PSE cannot legitimately manufacture historical output-inspection evidence or claim that an old PDF was inspected at its original release time.

Use:

```text
pse release-migration /path/to/historical-release --human
```

or write an assessment **outside** the historical release directory:

```text
pse release-migration /path/to/historical-release \
  --output /path/to/audit-records/release-migration-assessment.json
```

The assessment records the source manifest/PDF hashes, the result of current verification, the current target schema, and whether the artifact is legacy/current/unsupported. It always records that in-place upgrade is unsupported and that no retroactive output inspection was inferred.

For a valid `0.1` release, the correct route to full `0.2` evidence is to preserve the historical artifact and **re-release from the original source project** with a current PSE runtime. This creates a new release artifact; it does not replace history.
