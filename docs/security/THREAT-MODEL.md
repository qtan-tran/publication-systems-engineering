# Threat Model

## Protected assets

PSE assumes that downstream publishers may process assets with commercial or contractual sensitivity:

1. unpublished manuscript sources;
2. copy-edited and typeset proofs;
3. print-ready PDFs;
4. covers, illustrations, and licensed fonts;
5. publication metadata and release schedules;
6. recipient identities and proof-distribution records;
7. repository credentials, CI tokens, signing keys, and commercial-license material.

## Primary threat classes

### T1 — Accidental disclosure
A staff member commits a proof, manuscript, secret, or recipient manifest to a public repository or sends the wrong artifact.

### T2 — Compromised workstation or account
An attacker obtains access to a publisher workstation, Git account, CI account, shared drive, or build host and copies publication assets.

### T3 — Malicious or untrusted source input
A TeX source, package, metadata file, or contributed change attempts to execute commands, read local files, write outside permitted output areas, or manipulate the build pipeline.

### T4 — Supply-chain compromise
A dependency, TeX package, Python package, CI action, or downloaded tool is replaced or compromised.

### T5 — Authorized-recipient leakage
A legitimate author, proofreader, reviewer, printer, or collaborator shares a proof outside the intended channel. Watermarking can deter and attribute some leaks but cannot prevent screenshots, re-typesetting, rasterization, printing/scanning, or determined removal.

### T6 — Build/release confusion
An internal draft or proof is mistaken for a release artifact, or a release cannot be traced back to the exact source state used to generate it.

## Out of scope for the PSE core

The core does not provide enterprise identity management, endpoint security, network segmentation, encrypted document storage, remote-access control, or full DRM. These belong to downstream infrastructure. PSE must expose clean integration boundaries so organizations can add them without modifying the production core.

## Security principle

PSE should reduce the blast radius of mistakes and make sensitive artifacts traceable. It must not imply that a PDF which can be viewed can also be made technically impossible to reproduce.
