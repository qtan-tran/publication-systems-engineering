# Structural hierarchy contract

PSE distinguishes publication-level divisions from section depth.

- `Part` is a publication division.
- `Chapter` is a publication unit.
- Inside a chapter, the supported prose section depth is:
  1. `section`
  2. `subsection`
  3. `subsubsection`
  4. `paragraph`

A fifth section level (`subparagraph`) is rejected when the `structural-hierarchy` module is active. PSE does not silently flatten or rewrite manuscript structure. Authors and editors must make the structural decision explicitly, normally by converting deeper material to a run-in `paragraph`, a list, or another appropriate semantic form.

## Profile policy

The module is required and enabled by default for `academic-monograph`, `edited-collection`, and `basic-book`; recommended and enabled by default for `scholarly-edition`, `critical-edition`, and `bilingual-edition`; and discouraged/off by default for `drama`, `poetry`, and `literary-fiction`.

The discouraged profiles may still opt in if a particular project genuinely uses prose-section hierarchy.
