# Poetry profile

The `poetry` profile is a neutral presentation layer for poetry books. It controls stanza spacing, verse indentation, hanging continuation for long lines, running heads, and optional display numbers. It does not own semantic line identity.

## Semantic boundary

Stable stanza and verse-line identifiers belong to the reusable `verse-structure` module. A semantic verse line remains one line even when the chosen page measure forces its text to wrap. Display numbering is presentation metadata and may be omitted.

The starter syntax is:

```tex
\begin{PSEStanza}{s1}
\PSEVerseLine{l1}[1]{Synthetic verse text.}
\PSEVerseLine{l2}{Another semantic verse line.}
\end{PSEStanza}
```

The first argument of `PSEVerseLine` is a stable semantic identifier. The optional bracketed argument is a display label; the final argument is line content. IDs must be unique within a build.

## Generator

```text
pse new /path/to/books --profile poetry
```

Public fixtures and generated starters contain synthetic content only.
