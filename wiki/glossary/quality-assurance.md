---
title: Quality Assurance and Release
description: A summary of the PSE Quality Assurance process, with the concepts of validation, regression testing, quality sign-off layers, and the release decision.
---

# Quality assurance and release

A publishing system must not only produce one good book; it must help guarantee that later edits do not break the parts that already work. This group of terms is the foundation of Quality Assurance in PSE.

## The PSE Quality Assurance process (summary)

The process below synthesizes the concepts on this page into one workflow; the four-layer sign-off model at the end is a proposal drawn from real production experience.

1. **Prepare the environment and freeze scope.** Check the build environment with `pse doctor`; fix the copy-text, the [locator scheme](locators-and-references.md), and the scope of change before starting (source freeze, editorial freeze, production freeze).
2. **Preflight.** Confirm that source files, assets, fonts, and configuration are complete before building.
3. **Build.** Run `pse build .`; the pipeline compiles over multiple passes until page numbers, contents, and references stabilize; prefer a clean build when stale auxiliary files are suspected.
4. **Structural validation.** Run `pse check . --human`: collate locator sets, anchors, table of contents, index, metadata, and technical links; read the results by the four levels `error`, `warning`, `review`, `info`, and clear every `error` before continuing.
5. **Visual and geometry validation.** Render pages to images, compare against the baseline (render-diff), review the contact sheet, and check that markers sit in the right margin on the right page.
6. **Output inspection.** Run `pse inspect-output .` to record the baseline of metadata, navigation, and text extraction of the finished PDF.
7. **Human content validation.** Proofread full pages at full resolution, reconcile link meaning and the semantic alignment ledger; every `review` finding needs editorial judgment and cannot be closed by a formal check.
8. **Aggregate into the four sign-off layers.** (1) source and copy-text, (2) content and philology, (3) structure and lookup, (4) typesetting and production (details at the end of this page).
9. **The release decision.** Fix the definition of done, separate release blockers from known issues, and only then use `pse release .` and `pse verify-release` for the release boundary.
10. **Regression-test after every change.** For each edit, rerun the relevant checks; when a shared component changes, run cross-title regression testing for every edition using that component.

Deeper pages for each stage: [Quality Model](../quality-release/quality-model.md), [Build and check your PDF](../getting-started/build-and-check.md), and [Human Review](../workflows/human-review.md).

## Validation principles

| Term | Explanation |
| --- | --- |
| **Quality assurance (QA)** | The system of principles and processes built to prevent, detect, and address quality problems across the whole production process. |
| **Quality control (QC)** | The activity of testing specific products to determine whether they meet the stated standard. |
| **Testing** | Performing a check with defined conditions and a predefined expected result. |
| **Validator** | A tool or rule set used to confirm whether a component satisfies established requirements. |
| **Acceptance criteria** | The concrete criteria for concluding that a product or piece of work meets the requirement. |
| **Quality gate** | A checkpoint at which certain conditions must be met before the project moves to the next state. |
| **Independent validation** | Checking based on sources, methods, or a reviewer sufficiently independent from the work that produced the product. |
| **Validation evidence** | Measurements, collation records, images, logs, or reviews that can be used to support a quality conclusion. |
| **Validation coverage** | The portion of content, functionality, or real cases that has actually been checked. |
| **Spot check** | Checking a selected subset instead of the whole; the result is valid only within the corresponding scope. |

## Regression testing

A **regression** is a defect introduced by a change, making a function or property that previously worked fail or no longer meet requirements. **Regression testing** is rechecking previously confirmed functions after a change, in order to detect unintended impacts. For example, restyling an index can accidentally break the table of contents, shift page numbers, or affect the presentation of another book that shares the template.

Regression testing does not demand that nothing changes. It demands that intended changes are implemented correctly and that components outside the scope of change still behave as expected.

| Term | Explanation |
| --- | --- |
| **Cross-title regression testing** | Testing multiple different books after changing the shared core, to detect impacts outside the project being edited. |
| **Test fixture** | A document or data set prepared to test one defined case, for example two speakers sharing one verse line. |
| **Change isolation** | Limiting an edit to the part that actually needs fixing, reducing the risk of new defects elsewhere. |
| **Blast radius** | The number and degree of components or projects that can be affected by one change. |

For PSE, fixing a rule that is local to one title has a different blast radius from fixing a rule shared across the whole shelf; the two kinds of change need different levels of validation.

## Structural, positional, and semantic validation

| Term | Explanation |
| --- | --- |
| **Structural QA** | Checking the completeness and validity of components such as page numbers, anchors, contents, index, links, and metadata. |
| **Semantic QA** | Checking whether the content and the relations inside the document are right in meaning. |
| **Geometry validation** | Checking the position, size, spacing, and overlap of components on the page. |
| **Marker geometry regression** | Rechecking marker positions after edits, to make sure they remain in the right margin, on the right page, aligned with their anchors, and not overlapping content. |
| **Locator-set validation** | Comparing the actual locator set with the set expected from the source edition to find missing, duplicated, or out-of-order locators. |
| **Claim-to-output validation** | Checking whether what the book claims matches the actual content and form. |

The canonical position of a marker depends on the typesetting rules, the baseline grid, the trim size, and the presentation profile; no fixed offset fits every publication type, and every tolerance must be stated rather than assumed.

## Image checks and page proofing

| Term | Explanation |
| --- | --- |
| **Rendering** | Converting a document page into an image that can be inspected or analyzed directly. |
| **Render-diff** | Rendering the same page or content from two versions and comparing them to detect visual changes. |
| **Pixel comparison** | An image-comparison method based on per-pixel differences under identical rendering conditions. |
| **Pixel-identical page** | A page whose rendered image is identical to the reference under the defined comparison conditions. It does not necessarily mean all data inside the PDFs is identical. |
| **Contact sheet** | Many pages shown as thumbnails for an overview of the book's rhythm, layout, and consistency. |
| **Page-by-page proofing** | Checking the pages of an edition one by one for content, layout, and reading-experience problems. |
| **Full-resolution proof queue** | The list of pages that need detailed inspection at a size and quality sufficient to read text, marks, and small components. |
| **Unexpected diff** | A change between two versions outside the intended change scope, or not yet explained. |

### Distinguishing image comparison from content comparison

Image comparison identifies **where** something changed; the reviewer must still read and judge whether that change is a correct fix, a new defect, or an insignificant difference.

In the final editorial proof of a real production project, the record counted 80 of 94 pages pixel-identical to the production proof at 72 dpi, with 14 pages changed. A 72 dpi comparison does not replace proofing the whole book at full resolution. What matters is not the highest possible identical-page ratio, but the ability to **explain** the changes that occurred and to verify their impact.

## Quality sign-off and release

| Term | Explanation |
| --- | --- |
| **Editorial draft** | The version being refined in content, structure, notes, and editorial decisions. |
| **Production proof** | The version built in book form to check layout, type, pagination, and technical properties. |
| **Final editorial proof** | The version prepared for the final editorial review. The name does not automatically mean all validation is complete. |
| **Editorial freeze** | Establishing a stable state of content and editorial decisions so that further checks can proceed. |
| **Production freeze** | Establishing a stable state of layout and production, limiting changes outside the defined scope. |
| **Sign-off** | The grounded decision that a scope of work has met its conditions and can be considered complete. |
| **Definition of done** | The predefined set of requirements that a piece of work, a phase, or an edition must meet to count as complete. |
| **Release blocker** | A problem serious enough that an edition cannot yet be released: omitted content, a broken book file, unconfirmed source licensing. |
| **Known issue** | A problem identified and recorded but not yet fully resolved. Depending on severity it may or may not block release. |
| **Release** | The version confirmed to meet the publication conditions and delivered to readers within the defined scope. |
| **Technical postmortem** | The document analyzing the problems that occurred during production, their causes, how they were handled, the limits of verification, and the lessons for future projects. |

### The four sign-off layers of an edition

From real production experience, the model proposed for PSE distinguishes **four sign-off layers** instead of one blanket conclusion that the book is finished:

1. **Source and copy-text sign-off.** The right source, the right edition, the right locator conventions; licensing and provenance are clear.
2. **Content and philology sign-off.** The translation, speaker assignment, interpretation, and editorial decisions have appropriate grounding.
3. **Structure and lookup sign-off.** The parts, the notes, the index, and the links correspond to each other correctly.
4. **Typesetting and production sign-off.** The layout, the book files, the fonts, the build process, and the archival bundle meet requirements.

The release decision draws on the evidence of all four layers. Splitting source and philology into two layers follows the principle of not using one kind of evidence to certify a different kind of quality: structural validation cannot replace [philological sign-off](textual-scholarship.md).

Related pages: [Build and versioning](build-and-versioning.md), the overview in [The PSE Glossary](index.md).
