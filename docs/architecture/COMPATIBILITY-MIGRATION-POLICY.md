# Compatibility, Deprecation, and Migration Policy

## 1. Compatibility promise during beta-candidate staging

PSE follows Semantic Versioning for the executable framework, with an additional rule: while the project remains alpha, public contracts marked "frozen for beta-candidate staging" should not change incompatibly without a migration note and regression coverage.

## 2. Public contract categories

### CLI
Command names, documented required arguments, and exit-code classes are public contracts.

### Project contract
Generated source directories, `book.yml`, `content/`, `config/`, `assets/`, `build/`, and `release/` roles are public contracts. Generated artifacts are never canonical source.

### Profile and module manifests
Schema versions are explicit. A runtime must reject a manifest version it cannot safely understand rather than silently guessing.

### Semantic TeX API
Documented `\PSE...` commands are public semantic APIs. Presentation hooks are public only where the profile/module authoring documentation marks them as such.

### Machine reports
QA and semantic-IR schemas are versioned. New optional fields may be added compatibly; removal or meaning changes require a schema-version change.

## 3. Deprecation lifecycle

A non-security API removal should normally follow:

1. **announce** — document the replacement and first affected version;
2. **warn** — tooling may emit a non-blocking deprecation finding;
3. **migrate** — provide an actionable migration note or automated migration where practical;
4. **remove** — only in a version that permits the compatibility break.

Security-sensitive behavior may be removed immediately if keeping it would create an unreasonable risk.

## 4. Migration notes

Every incompatible change must document:

- old contract;
- new contract;
- affected profiles/modules/projects;
- exact source/config changes required;
- regression evidence;
- release notes entry.

## 5. No silent compatibility repair

The runtime must not silently reinterpret malformed project metadata, unknown schema versions, ambiguous module capabilities, or invalid semantic identifiers. Fail-closed behavior is preferred where guessing could corrupt a publication artifact.
