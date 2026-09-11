# CLI Compatibility Matrix

current release freezes the following command surface for beta-candidate staging.

| Command | Audience | Contract | Typical output |
|---|---|---|---|
| `pse doctor` | all users | environment/runtime preflight | human or JSON diagnostics |
| `pse profiles` | all users | installed profile registry | text/JSON |
| `pse modules` | advanced users | installed semantic-module registry | text/JSON |
| `pse new` | editors/layout staff | secure project generation | project directory |
| `pse build` | editors/layout staff | safe LuaLaTeX build | `build/book.pdf` + generated bridge files |
| `pse check` | editors/QA | machine QA | structured QA report |
| `pse clean` | all users | remove generated build boundary | cleaned project |
| `pse proof` | production staff | recipient-specific proof | watermarked PDF + provenance JSON |
| `pse release` | release managers | clean promotion through QA gates | release directory + manifest/checksums |
| `pse verify-release` | production/audit | release-integrity verification | verification report |
| `pse contracts` | production/audit/tooling | installed public schema/contract discovery | text/JSON contract surface |
| `pse release-migration` | production/audit | non-mutating historical release migration assessment | text/JSON assessment; never an upgraded release |
| `pse inspect-output` | editors/QA | limited finished-PDF metadata/navigation/text baseline; no accessibility certification | human or JSON inspection report |
| `pse visual-check` | maintainers/production | baseline visual comparison | report + renders/diffs |
| `pse semantic-ir` | advanced QA/tooling | non-executing semantic source inventory | semantic IR JSON |
| `pse regression` | framework maintainers | layered framework regression | aggregate JSON |
| `pse smoke` | framework maintainers | minimal executable smoke test | pass/fail report |

## Exit-code classes

Where applicable:

- `0`: command completed without blocking `error` findings;
- `1`: publication/framework error or failed regression gate;
- `2`: invocation/configuration misuse.

Commands may document narrower meanings but must not reverse these classes without a compatibility change.
