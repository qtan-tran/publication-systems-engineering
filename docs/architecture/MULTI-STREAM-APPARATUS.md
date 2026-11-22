# Multi-Stream Apparatus

PSE separates **apparatus semantics** from **apparatus presentation**. The reusable `apparatus` module owns locator-keyed notes and five stable semantic stream identifiers; profiles and title-local presentation may decide how those streams are labelled or arranged.

## Canonical streams

The current contract defines exactly five semantic streams:

- `textual` - readings, variants, omissions, additions, and other text-critical evidence;
- `editorial` - punctuation, normalization, emendation, segmentation, or other editorial intervention;
- `translation` - translation decisions or translation-specific alternatives;
- `commentary` - explanatory or interpretive commentary tied to a locator;
- `source` - source, witness, provenance, or source-relational notes.

These names are semantic identifiers. They are **not** required to appear literally in the PDF. A profile or project may present them as words, abbreviations, letters such as A/B/C, separate blocks, foot apparatus, or another supported layout.

## API

```tex
\begin{PSEApparatus}
\PSEApparatusStreamEntry{textual}{1.1}{lemma}{...}
\PSEApparatusStreamRangeEntry{editorial}{1.2}{1.3}{punctuation}{...}
\PSEApparatusStreamEntry{translation}{2.1}{rendering}{...}
\end{PSEApparatus}
```

Presentation labels are independently configurable. The framework baseline uses compact labels (`T`, `E`, `Tr`, `C`, `S`) so the semantic stream names do not become a visual requirement:

```tex
\PSESetApparatusStreamPresentationLabel{textual}{A}
\PSESetApparatusStreamPresentationLabel{editorial}{B}
```

Changing a presentation label must not change the semantic stream identifier in source.

## Backward compatibility

The existing `\PSEApparatusEntry`, `\PSEExplanatoryNote`, and `\PSEApparatusRangeEntry` commands remain valid. They are intentionally generic and do not infer a stream retroactively. Existing titles therefore do not need to be rewritten merely to compile under the multi-stream contract. New scholarly work should prefer the explicit stream API where the distinction is meaningful.

## Validation

PSE source QA inventories stream-aware entries and rejects unknown stream identifiers. Locator validation remains owned by `canonical-locators`; stream-aware entries participate in the same locator-reference and locator-range checks as legacy apparatus entries.

This phase does not introduce automatic witness collation, stemmatics, TEI critical apparatus import/export, or dynamic stream placement. Those remain outside this contract.
