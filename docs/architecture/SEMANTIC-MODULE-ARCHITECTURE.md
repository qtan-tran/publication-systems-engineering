# Semantic Module Architecture

Publication Systems Engineering separates **visual profiles** from **semantic modules**.

A profile controls page architecture and presentation. A semantic module provides structured publishing behavior such as canonical locators, apparatus entries, bibliography, index generation, or multilingual text. Neither layer owns security, proof generation, QA, release provenance, runtime discovery, or metadata transport; those remain backbone responsibilities.

## Dependency rule

```text
title -> profile -> core
title -> semantic modules -> core
```

Profiles and modules are siblings. A semantic module must not depend on a specific profile, and a profile must not copy a semantic module's implementation. Titles may activate the modules declared by their selected profile.

## Current release modules

- `canonical-locators`: unique canonical anchors and references.
- `apparatus`: locator-keyed apparatus entries with semantic `textual`, `editorial`, `translation`, `commentary`, and `source` streams; presentation labels remain separate.
- `multilingual`: open-font multilingual primitives with polytonic Greek support.
- `bibliography`: `biblatex`/`biber` integration.
- `index`: `imakeidx`/`makeindex` integration.
- `scholarly-matter`: generic scholarly front- and back-matter primitives.
- `drama-structure`: speaker, speech, stage-direction, and act/scene semantics.
- `dramatic-locators`: dramatic locators composed through canonical locator semantics.
- `parallel-text`: stable source/target segment identity and alignment.
- `verse-structure`: stable stanza and verse-line identity independent of layout.

The checked-in runtime registry is generated from these module manifests and the profile manifests. `scripts/release/sync_registry.py --check` fails when runtime metadata drifts from the manifest-discovered registry. Packaging uses the same filesystem contracts rather than a hand-maintained profile/module list.

All public fixtures are synthetic. This architecture does not reproduce private downstream publishing systems.

## Build tools

Semantic modules declare auxiliary tools in `module.json`. The CLI invokes only allow-listed tools (`biber`, `makeindex`) as argument arrays; manuscript text cannot construct shell commands. LuaLaTeX remains `--no-shell-escape`.

## Extension rule

New modules require a manifest, package, synthetic fixture, regression test, security review, and documentation. A module should remain narrow: if it controls page design, it belongs in a profile; if it controls release or security, it belongs in the backbone.

## Current release composition contract

current release generalizes modules into namespaced semantic families. Profiles may provide defaults, while a title may activate additional modules through `config/semantic-modules.json`. Runtime resolution is authoritative: direct dependencies and required capabilities are resolved before TeX is invoked, conflicts and incompatible profiles fail closed, and the resulting package list is generated as `build/pse-modules.tex`.

Module manifests are declarative data, never executable plugin entry points. QA hooks are allow-listed runtime identifiers. This preserves the security boundary while leaving room for later third-party semantic families.

## Verse structure

`verse-structure` owns stable stanza and verse-line identity. Poetry profiles may redefine presentation hooks for spacing, indentation, line wrapping, and visible numbering, but must not infer semantic line identity from physical lines on a page.


## Structural hierarchy

`structural-hierarchy` owns the reusable four-level prose section-depth contract. Part and Chapter remain higher-order publication structures and are not counted as section levels. The module validates depth; profiles own heading typography.
