# Bilingual Edition

**Profile ID:** `bilingual-edition`  
**Best for:** source/translation editions, parallel bilingual publications, language-learning editions, and other projects where source and target segments must stay explicitly aligned.

Use another profile when ordinary translated books that do not need source/target alignment in the published object.

## What this profile feels like

Scholarly parallel-text presentation. Semantic alignment is stable even when the visible layout changes between columns, facing pages, sequential blocks, or source/target-dominant modes.

Its integrated presentation preset is `parallel-edition`. The page-grid mode is `asymmetric-scholarly`, side-material mode is `outer-margin`, apparatus mode is `available`, locator mode is `source-defined`, and parallel-text mode is `profile-controlled`.

## Semantic modules

Modules enabled by the generated starter: `parallel-text`, `index`, `structural-hierarchy`, `contributor-metadata`.

Other modules with an explicit policy for this profile: `publication-unit-metadata`, `margin-objects`, `apparatus`.

| Module | Policy | Starter default |
| --- | --- | --- |
| `parallel-text` | required | on |
| `index` | recommended | on |
| `structural-hierarchy` | recommended | on |
| `publication-unit-metadata` | optional | off |
| `contributor-metadata` | required | on |
| `margin-objects` | recommended | off |
| `apparatus` | recommended | off |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- `content/parallel.tex` — source/target segments and alignment relations
- `config/bilingual-layout.json` — choose the presentation mode without rewriting alignment semantics
- `book.yml` and contributor metadata — publication and translation responsibility

Create a private starter project with:

```text
pse new /path/to/private-projects --profile bilingual-edition
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- Choose among `parallel-columns`, `facing-pages`, `sequential-blocks`, `source-dominant`, and `target-dominant`.
- Use typed alignment notes and alignment locators where the edition needs them.
- Apparatus and margin objects can be activated without changing segment IDs.

## Boundaries and limitations

- Page or column position is never the semantic identity of a segment.
- Do not use the profile merely to place two unrelated text columns side by side.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/bilingual-edition/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py bilingual-edition
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
