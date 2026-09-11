# Security Policy

Publication Systems Engineering (PSE) is designed to operate as a publishing-production backbone. Security therefore covers not only repository hygiene but also unpublished manuscripts, proof artifacts, build environments, release files, and downstream infrastructure.

## Security posture

PSE follows **secure defaults, local-first operation, explicit trust boundaries, and traceable proof distribution**. PSE is not a DRM system and does not claim to make viewable PDFs impossible to copy or reconstruct.

Default executable policy:

- LuaLaTeX is invoked with `--no-shell-escape`.
- YAML is parsed with `yaml.safe_load`.
- metadata is validated before TeX generation; page dimensions must be numeric and within a bounded range.
- metadata strings are TeX-escaped before entering generated TeX.
- generated proofs and manifests live under ignored `build/` paths.
- PSE does not require manuscripts to be uploaded to a PSE-operated service.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities in a public issue when they could expose private publication data, credentials, or a working exploit. Contact the maintainer privately using the security contact channel published with the repository release.

Do not include real unpublished manuscripts, credentials, API keys, commercial fonts, personal recipient manifests, or confidential downstream project data in reports unless an encrypted/private exchange has been agreed.

## Scope

Security reports may include: unsafe TeX execution, shell-escape bypass, metadata injection, path traversal, proof-generation failures that leak recipient data, insecure CI behavior, dependency/supply-chain issues, or accidental publication of ignored/private artifacts.

See `docs/security/` for the full threat model and trust architecture.
