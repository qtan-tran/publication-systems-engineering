# Critical Edition

**Profile ID:** `critical-edition`  
**Best for:** source-oriented critical editions, textual editions, and editions where canonical locators, textual decisions, apparatus streams, and scholarly matter are central.

Use another profile when ordinary monographs or reading editions where apparatus and source locators would be unnecessary editorial overhead.

## What this profile feels like

Compact and source-critical. The text, visible canonical locators, multi-stream apparatus, scholarly matter, multilingual material, and outer-margin objects form one integrated edition system.

Its integrated presentation preset is `source-critical`. The page-grid mode is `asymmetric-scholarly`, side-material mode is `outer-margin`, apparatus mode is `multi-stream`, locator mode is `primary-visible`, and parallel-text mode is `none`.

## Semantic modules

Modules enabled by the generated starter: `canonical-locators`, `apparatus`, `multilingual`, `bibliography`, `index`, `scholarly-matter`, `structural-hierarchy`, `contributor-metadata`, `margin-objects`.

Other modules with an explicit policy for this profile: `publication-unit-metadata`.

| Module | Policy | Starter default |
| --- | --- | --- |
| `canonical-locators` | required | on |
| `apparatus` | required | on |
| `multilingual` | required | on |
| `bibliography` | required | on |
| `index` | recommended | on |
| `scholarly-matter` | required | on |
| `structural-hierarchy` | recommended | on |
| `publication-unit-metadata` | optional | off |
| `contributor-metadata` | required | on |
| `margin-objects` | recommended | on |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- `content/critical-text.tex` — edited text and stable locator structure
- `content/apparatus.tex` — apparatus entries linked to semantic locators
- `content/editorial-notes.tex` — explanatory/editorial material
- `references.bib` — bibliography source
- `config/locator-scheme.json` and related locator config — locator policy

Create a private starter project with:

```text
pse new /path/to/private-projects --profile critical-edition
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- Use apparatus streams (`textual`, `editorial`, `translation`, `commentary`, `source`) according to editorial function, not visual label.
- Use margin objects for genuinely side-oriented material; fallback behavior remains visible when margin placement is unavailable.
- Override typography and grid locally, but preserve stable semantic IDs.

## Boundaries and limitations

- This profile assumes real editorial control over a source text; it is intentionally heavier than a reading edition.
- PSE does not establish the scholarly validity of readings, witnesses, or editorial judgments.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/critical-edition/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py critical-edition
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
