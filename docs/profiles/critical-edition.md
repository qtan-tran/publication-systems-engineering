# Critical Edition Profile

The `critical-edition` profile is a source-oriented presentation layer for text-critical and documentary editions. It is intentionally neutral: it does not imitate an external publisher or encode project-specific editorial policy.

The profile activates the existing `canonical-locators`, `apparatus`, `multilingual`, `bibliography`, `index`, and `scholarly-matter` modules. Those modules own semantic identifiers and QA contracts. The profile owns only reusable page architecture: compact text hierarchy, running heads and folios, body rhythm, footnote spacing, and title-page presentation.

A generated starter demonstrates canonical locations and explicit apparatus streams:

```tex
\PSELocator{1.1}
A synthetic lemma ...

\begin{PSEApparatus}
\PSEApparatusStreamEntry{textual}{1.1}{lemma}{...}
\end{PSEApparatus}
```

Canonical locators must remain stable source data and must not be replaced by page numbers. Apparatus data should refer to those locators. Witness descriptions, sigla, editorial principles, and textual decisions belong to the downstream title project, not the framework profile.

## Boundary with `scholarly-edition`

`scholarly-edition` remains the broad neutral scholarly baseline. `critical-edition` is narrower: it uses the same reusable semantic modules but provides a more compact, source-oriented presentation contract for editions where the edited text and its canonical locations are visually primary. No locator or apparatus implementation is duplicated in the profile.

## Generator and QA

Create a starter with:

```text
pse new /path/to/books --profile critical-edition
```

Run `pse doctor --profile critical-edition` to check the required open font and auxiliary tools. The framework regression suite discovers generator-supported profiles from their validated manifests rather than from a hard-coded profile list.
