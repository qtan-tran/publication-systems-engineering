# Security & Trust Architecture

## Trust zones

PSE distinguishes five zones.

### Zone 0 — Public framework
Public PSE source, synthetic fixtures, documentation, CI configuration, and openly licensed fonts. No private manuscript data belongs here.

### Zone 1 — Private project source
A publisher-controlled private repository or filesystem containing manuscripts, title configuration, private assets, and project metadata.

### Zone 2 — Build workspace
Generated metadata, logs, intermediary TeX files, indexes, and temporary artifacts. This zone should be disposable and excluded from source control.

### Zone 3 — Controlled proofs
Recipient-specific watermarked PDFs and local provenance manifests. Proofs are distribution artifacts, not source artifacts. Recipient manifests may contain personal information and should remain private.

### Zone 4 — Release artifacts
Approved print-ready PDFs, release manifests, checksums, and later digital signatures. Release artifacts should be produced by an explicit release command, never inferred from the existence of `book.pdf`.

## Dependency direction

Security follows the same architectural rule as production: public core must not depend on private title data. Private projects may depend on the public core. CI must not expose private secrets to untrusted pull-request code.

## Secure build contract

The default PSE build contract is:

- LuaLaTeX only;
- shell escape disabled;
- safe YAML parsing;
- strict validation of fields that affect command structure or geometry;
- generated metadata bridge rather than parsing YAML in TeX;
- no network access required for ordinary builds;
- build artifacts written beneath the project build boundary;
- no claim that TeX itself is a sandbox.

`--no-shell-escape` materially reduces command-execution risk but does **not** make untrusted TeX safe to run on a sensitive workstation. Highly untrusted source should eventually be built in an operating-system/container sandbox with only the project directory mounted.

## Distribution contract

PSE distinguishes `build`, `proof`, and later `release`. A proof is bound to a recipient identifier and a provenance manifest. A release is not a proof with the watermark removed; it is a separately authorized lifecycle state.

## Future enterprise extension points

The architecture must permit downstream adapters for SSO, private artifact stores, signing services, hardware-backed keys, secure print portals, enterprise DRM, DLP, and audit-log systems without moving those concerns into the generic typesetting core.
