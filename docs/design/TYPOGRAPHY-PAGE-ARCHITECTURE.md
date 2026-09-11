# Typography & Page Architecture — current release

## Status

current release defines the first neutral professional typography contract for the `basic-book` profile. It is a framework baseline, not a house style and not a model of any external publisher.

## Architectural boundary

The dependency direction is:

`title-local config -> profile -> core`

The core owns engine/bootstrap, metadata, generic document primitives, proof mode, and shared technical services. The `basic-book` profile owns book-specific typography and page behavior. A title may apply restrained overrides in `config/pse-local.tex`; a title must not edit the shared core to solve a local design problem.

## Baseline typography contract

- Open font baseline: Latin Modern family.
- Body: approximately 10.15 pt on 13.05 pt leading.
- Paragraph indent: approximately 1.22 em; no paragraph skip.
- First paragraph after structural headings follows standard LaTeX no-indent behavior.
- Footnotes: approximately 8.35 pt on 10.35 pt leading.
- Widow/orphan penalties are elevated but not absolute.
- Pages use `raggedbottom` in the neutral baseline to avoid destructive vertical stretching; future profiles may choose a stricter bottom alignment policy.

## Heading hierarchy

The technical fixture's oversized default `book` chapter display is explicitly retired.

- Chapter number/label: small, quiet, secondary.
- Chapter title: 17.2 pt / 20.2 pt, bold, ragged-right.
- Section: 11.8 pt / 14.2 pt, bold.
- Subsection: 10.35 pt / 12.8 pt, bold.
- Sections receive minimum remaining-space protection to reduce stranded headings.

The hierarchy is intentionally restrained so future profiles can move in either a literary or scholarly direction without undoing an aggressively branded core.

## Page architecture

For the current Crown Octavo fixture (126 x 198 mm), the profile uses:

- inner margin: 18 mm;
- outer margin: 22 mm;
- top margin: 19 mm;
- bottom margin: 23 mm;
- restrained running heads;
- outer folios on normal body pages;
- centered foot folio on chapter-opening pages.

These are profile defaults, not global requirements. The page dimensions remain metadata-driven.

## Running heads

- Even pages: book title.
- Odd pages: current chapter title.
- Folios sit on the outer side of the running head.
- Chapter-opening pages suppress running heads and retain only a quiet centered folio.

## Override contract

`config/pse-local.tex` is the designated title-local override boundary. It loads after `pse-core` and the active profile. It is intentionally empty in generated projects.

Permitted title-local uses include narrowly scoped spacing or typography adjustments required by the title. Repeated overrides across multiple projects are evidence that the profile, rather than each title, may need revision.

## Visual baseline policy

current release establishes baseline pages but does not yet make pixel differences fatal. current release will add comparison/orchestration. current release visual review focuses on:

1. title page;
2. chapter opening;
3. ordinary body page with running head;
4. long section heading;
5. footnote page.

## Non-goals

current release does not implement fiction, academic-monograph, scholarly-edition, drama, or bilingual house styles. It also does not freeze typography APIs for v1.0; it freezes only the architectural ownership boundary and the neutral `basic-book` behavior required for the next regression phase.
