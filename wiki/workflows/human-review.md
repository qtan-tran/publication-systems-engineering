---
title: Human Review
description: Separate machine findings from editorial, typographic, factual, and publication decisions that require people.
---

# Human review

PSE machine QA is deliberately limited. It can detect many structural and technical problems, but it cannot decide whether a translation is accurate, an apparatus is intellectually adequate, a bibliography is factually correct, a line break is aesthetically acceptable, or a page is ready to be signed off by an editor.

## Review the findings, then review the book

After:

```text
pse check . --human
```

work through the reported severity levels:

| Level | Production meaning |
| --- | --- |
| `error` | blocking condition; fix before release |
| `warning` | technical issue that requires attention |
| `review` | explicit human judgement required |
| `info` | recorded status/evidence |

Then inspect the actual PDF. A zero-error machine report is not a visual proofread.

## Typical human review areas

Check at least the areas relevant to the publication: textual accuracy, factual references, contributor names and affiliations, hierarchy, widows/orphans, note placement, apparatus readability, parallel-text correspondence, illustration quality, captions, running heads, page numbers, blank-page behavior, contents/index correctness, publication page, and final page count.

For changed shared framework code or an intentionally preserved visual baseline, maintainers may also use `pse visual-check`; visual comparison is a review signal, not an automatic design verdict.

## Acknowledging review findings

`pse release` blocks unresolved release gates. When only reviewed and consciously accepted `review` findings remain, the release manager may use:

```text
pse release . --acknowledge-review
```

That flag means a human has reviewed those findings. It must not be used to bypass `error` findings or to convert an unreviewed book into an approved one.

Next: [Recipient proofs](recipient-proofs.md) or [Prepare a publication release](publication-release.md).
