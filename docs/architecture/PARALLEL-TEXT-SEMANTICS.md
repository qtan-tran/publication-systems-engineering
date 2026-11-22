# Parallel-Text Semantic Contract

PSE separates parallel-text meaning from its visual arrangement. Source and target segments receive stable role-scoped IDs. Stable alignment IDs connect one or more source segments to one or more target segments. Source order and page position do not determine pairing.

## Semantic objects

- `\PSEParallelSegment{source|target}{id}{text}` declares a stable segment.
- `\PSEParallelAlign{alignment-id}{source-ids}{target-ids}` declares the alignment relation.
- `\PSEParallelAlignmentLocator{alignment-id}{locator}` optionally attaches a human-facing locator to the relation.
- `\PSEParallelNote{alignment-id}{kind}{text}` attaches one typed note of a given kind.
- `\PSEParallelTranslationNote` remains a compatibility shorthand for a `translation` note.

Locators and notes refer to alignment IDs, never to pages or column positions. PSE validates unresolved relations and duplicate locator/note-kind assignments. No DOI, language-service, translation-memory, or external alignment service is implied.

## Presentation modes

The bilingual profile can render the same semantic source as `parallel-columns`, `facing-pages`, `sequential-blocks`, `source-dominant`, or `target-dominant`. Changing mode must not rewrite semantic source. `facing-pages` remains a review-sensitive mode when aligned material exceeds a page.

`config/parallel-text.json` owns language roles and alignment cardinality policy. `config/bilingual-layout.json` owns presentation. This boundary allows future profiles to reuse parallel semantics without inheriting bilingual page design.
