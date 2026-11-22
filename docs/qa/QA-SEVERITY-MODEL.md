# QA Severity Model

PSE separates machine-detectable conditions from editorial judgement. A clean process must not turn every TeX warning into a build failure.

## `error`

A condition that makes the artifact unreliable or invalid for the current gate. Examples: missing output PDF, missing glyphs, unresolved references/citations after the configured build, materially incorrect page geometry, failed visual rendering required by a regression job.

`error` causes exit code 1 in QA/regression commands.

## `warning`

A non-fatal technical condition that should be reviewed when it appears or increases. Examples: underfull boxes and ordinary hyperlink warnings. Warnings do not fail the build by themselves.

## `review`

A condition requiring human production/editorial judgement. Examples: overfull boxes, font substitution, page-count drift, visual baseline drift. During alpha, review findings do not make CI fail automatically.

## `info`

Evidence recorded for traceability, including visual pages that remain within approved tolerance.

## Exit policy

- `0`: no error-severity failures; warnings/review findings may remain.
- `1`: one or more error-severity failures.
- `2`: command-line/configuration error (standard CLI behavior).

A release workflow may later promote selected `review` or `warning` codes to blocking gates without changing their underlying detection semantics.
