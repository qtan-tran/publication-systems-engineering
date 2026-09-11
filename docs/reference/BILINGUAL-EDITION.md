# Bilingual / Parallel-Text Profile

The `bilingual-edition` profile is a neutral presentation layer over the `parallel-text` semantic module. Stable segment and alignment IDs remain the source of truth. Presentation is configured in `config/bilingual-layout.json`.

Supported modes:

- `parallel-columns`: source and target flow in paired columns at alignment-block boundaries.
- `facing-pages`: source begins on verso and target on the facing recto; long alignments require visual review.
- `sequential-blocks`: source is followed by target in the primary reading stream.
- `source-dominant`: source is primary and target is visually subordinate.
- `target-dominant`: target is primary and source is visually subordinate.

Changing presentation mode must not rewrite segment IDs, alignment IDs, locators, or notes. Use alignment locators for edition-facing references and typed notes for semantic annotation; do not encode those relations through page position.
