# Source diagnostics contract

PSE QA findings use one common optional source-location object when a finding can be tied to manuscript source:

```json
{"file":"content/play.tex","line":42,"column":1,"offset":1068}
```

`file` is project-relative. `line` and `column` are one-based; `offset` is zero-based in the decoded UTF-8 source string. Findings that concern generated PDFs, runtime installation, release artifacts, or global configuration may legitimately have no source location.

For editor-facing work, `pse check --human` prints concise diagnostics in `file:line:column` form. JSON remains the canonical machine-report format.

Source locations identify the PSE semantic command or environment that triggered a finding. They do not attempt to identify dynamically generated TeX produced by arbitrary macro expansion; semantic identifiers intended for machine QA must occur directly in the public PSE semantic API.
