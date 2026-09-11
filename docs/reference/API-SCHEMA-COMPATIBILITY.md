# API and Schema Compatibility Matrix

| Surface | Current contract | current release status |
|---|---:|---|
| Framework runtime | `1.47.0-alpha` | beta-candidate staging |
| Profile manifest | schema `1.1` (runtime reads legacy `1.0`) | current |
| Semantic module manifest | schema `1.1`, API `1` | frozen |
| Locator scheme | schema `1.0` | frozen |
| Namespaced locator schemes | schema `1.0` | frozen |
| Locator orchestration | schema `1.0` | current |
| Semantic module activation | schema `1.1` | current |
| Parallel-text config | schema `1.0` | frozen |
| Bilingual layout config | schema `1.1` (runtime reads `1.0`) | current |
| Semantic IR | schema `1.0` | frozen with additive optional fields allowed |
| Publication release manifest | schema `0.2` | current strict contract; `0.1` verification-only legacy compatibility |
| Output inspection report | schema `0.2` | hash-bound baseline; no conformance certification |
| QA severity model | `error/warning/review/info` | frozen |

Unknown future schema versions must be rejected unless an explicit compatibility rule says otherwise.


Installed contract discovery is available through `pse contracts --json`. The reported schema paths belong to the active runtime and are suitable for local validators and audit tooling. `pse release-migration` is an assessment surface only; it does not transform schema `0.1` artifacts into schema `0.2` artifacts.


## Release audit record

`pse audit-release` emits schema `0.2` audit records validated against `schema/release-audit-record-0.2.schema.json`; schema `0.1` remains legacy-verifiable. Audit records are external evidence and are never written into or treated as part of the audited release. Frozen synthetic compatibility fixtures live under `tests/fixtures/releases/`.

## Audit evidence contracts

- `release-audit-record-0.2.schema.json` is the current audit-record contract and adds a portable path-independent release fingerprint.
- `release-audit-record-0.1.schema.json` remains a legacy audit-record schema.
- `release-audit-index-0.1.schema.json` defines external multi-release audit indexes and their path-independent batch fingerprint.
