# Semantic IR compatibility contract

The semantic intermediate representation is a diagnostic API between PSE source parsing and QA. It is not a manuscript storage format and does not replace TeX source.

## Versioning

`schema_version: 1.0` is retained during current release. Backward-compatible additions may add optional fields. Removing fields, changing the meaning of existing fields, or changing location semantics requires a new schema version and migration note.

Stable 1.0 fields are `project`, `nodes`, `errors`, node `kind/name/args/location`, and location `file/line/column/offset`. Parser errors may additionally include a machine-readable `code`.

## Security boundary

The parser never executes TeX, expands macros, follows arbitrary executable hooks, or changes catcodes. Only allow-listed PSE semantic commands are inventoried. This deliberately constrained contract is part of PSE's security model.
