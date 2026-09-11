# Scholarly Edition Foundation

The `scholarly-edition` profile is a neutral visual baseline that activates the current release semantic-module set. It is not a house style.

A generated starter demonstrates:

```tex
\PSELocator{A1}
\PSEGreek{ὄνομα}
\PSEApparatusEntry{A1}{name}{...}
\autocite{synthetic2027}
\PSEIndex{name}
```

The locator identifier is canonical project data and must be unique. Apparatus entries should point to locators rather than page numbers so pagination can change without invalidating the editorial structure.

The multilingual module requires the openly licensed Gentium Plus font. Bibliography and index modules require `biber` and `makeindex` respectively. Run `pse doctor` and `pse build` rather than invoking auxiliary tools manually.

For source-oriented text-critical work, see the narrower [`critical-edition`](../profiles/critical-edition.md) profile, which reuses the same semantic modules with a more compact presentation contract.
