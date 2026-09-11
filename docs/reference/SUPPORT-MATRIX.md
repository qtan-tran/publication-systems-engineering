# Support Matrix — Beta Candidate Staging

## Operating systems

| Platform | Intended support | Local evidence | Public-beta claim |
|---|---|---|---|
| Windows | yes | workflow/configuration authored | requires live GitHub CI |
| macOS | yes | workflow/configuration authored | requires live GitHub CI |
| Linux | yes | exercised locally | requires candidate CI run |

## Runtime

- Python: 3.11+; CI matrix also exercises 3.13 where applicable.
- Production engine: LuaLaTeX.
- Canonical manuscript source: LaTeX for the current product line.

## Tested Python dependency family

Current engineering tests use compatible releases in these families:

- PyYAML 6.x;
- pypdf 5.x;
- Pillow 10+ / 12.x tested.

These are support guidance, not a byte-for-byte lockfile guarantee.

## Optional/feature dependencies

- `biber` for bibliography modules;
- `makeindex` for index modules;
- Gentium Plus for the scholarly multilingual baseline;
- Poppler (`pdftoppm`) for visual-regression rendering.

`pse doctor` and profile-aware preflight should be used instead of assuming an installation is complete.

## Output inspection

`pse inspect-output` uses the packaged `pypdf` dependency and therefore does not require Poppler. It provides only the documented metadata/navigation/text-extractability baseline. Tagged-PDF structure, reading order, image alternative text, PDF/UA, WCAG, archival conformance, and legal accessibility compliance are not certified by the current support contract.
