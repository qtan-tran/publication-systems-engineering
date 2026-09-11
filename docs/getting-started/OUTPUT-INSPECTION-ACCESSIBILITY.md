# Output inspection and accessibility baseline

PSE can inspect a finished PDF for a **limited machine-verifiable baseline**. This is intentionally narrower than accessibility certification.

Run:

```text
pse inspect-output build/book.pdf --expected-language en --human
```

or from a project directory:

```text
pse inspect-output . --expected-language en
```

The command checks PDF readability, core title/author metadata, document-level PDF catalog language, bookmark navigation, and text extractability.

It records the following as **human or specialist review** at this stage: tagged-PDF structure, logical reading order, alternative text for meaningful images, and formal accessibility conformance.

PSE 1.24 does **not** certify PDF/UA, WCAG conformance, archival standards, or compliance with accessibility law. A clean inspection means only that the explicitly machine-verifiable checks completed.

## Language metadata

The PSE core writes the title language from `book.yml` into the PDF catalog `/Lang` entry. Use a concise language code such as `en`, `vi`, or `de`. For multilingual books this is only the document-level primary language; it does not replace span-level language tagging.

## Fonts and Unicode

Use fonts with appropriate Unicode coverage. Successful visual rendering does not prove extracted text is semantically correct for every glyph, so text extractability is a baseline rather than a Unicode-conformance claim.

## Images and alt text

The current print-PDF pipeline does not claim automated alt-text coverage. Image-bearing titles require project-specific accessibility review.

## Reading order

Extraction order can reveal obvious problems but is not equivalent to tagged structural reading order. PSE therefore leaves reading order at review status.

## Canonical demo corpus

The nine PDFs under `examples/profiles/*/output/` are the public output-inspection corpus. They are synthetic and can be used to test metadata, navigation, and text extraction without exposing private manuscripts.

## Release evidence integration

From PSE 1.25, `pse release` runs the same inspection baseline against the final publication PDF and stores `output-inspection.json` beside the release manifest, QA report, and PDF. The release manifest records the inspection file SHA-256 and the exact release-PDF SHA-256 to which the report is bound. `pse verify-release` checks both bindings.

Release policy is intentionally narrow:

- unreadable PDF, missing title/author metadata, or missing/mismatched document-level language metadata are **blocking**;
- failure to pass the lightweight text-extractability baseline is a **human-review gate**;
- tagging, logical reading order, image alt text, PDF/UA/WCAG/archival/legal conformance remain **evidence-only review concerns** and are not automatically certified or failed by this baseline.

This distinction prevents a technically useful release gate from becoming a false accessibility claim.

For the hash-binding and legacy-manifest policy used by publication releases, see [Publication release manifest contract](../release/RELEASE-MANIFEST-CONTRACT.md).
