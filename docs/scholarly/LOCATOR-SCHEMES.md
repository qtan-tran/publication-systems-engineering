# Canonical locator scheme contract

Scholarly projects may declare `config/locator-scheme.json`. The file is project-owned source and defines the canonical order explicitly; PSE does not infer scholarly sequences from typography or identifier spelling.

Required fields: `schema_version`, `id`, `order`, `require_complete`, `strict_order`.

`pse check` inventories `\\PSELocator{...}` in `main.tex` and `content/**/*.tex` and reports duplicate, unknown, missing, out-of-order, unresolved-reference, and invalid-range conditions. A complete strict scheme makes these conditions release-blocking errors.

Use `\\PSELocatorRangeRef{start}{end}` for a displayed range reference and `\\PSEApparatusRangeEntry{start}{end}{lemma}{note}` for apparatus keyed to a range.

The explicit-order model is intentionally generic: projects may represent page/section locators, line locators, canonical paragraph identifiers, manuscript foliation, or other scholarly systems without PSE hard-coding any one tradition.
