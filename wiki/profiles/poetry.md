# Poetry

**Profile ID:** `poetry`  
**Best for:** poetry collections, verse sequences, and editions where stanza structure and stable verse-line identity need to survive wrapping or presentation changes.

Use another profile when ordinary prose or dramatic dialogue where verse semantics would misrepresent the text.

## What this profile feels like

Verse-centered. Stanzas and semantic verse lines are primary; a physically wrapped line remains one semantic verse line, and visible numbering can differ from stable line identity.

Its integrated presentation preset is `verse-reading`. The page-grid mode is `book`, side-material mode is `fallback`, apparatus mode is `available`, locator mode is `source-defined`, and parallel-text mode is `none`.

## Semantic modules

Modules enabled by the generated starter: `verse-structure`.

Other modules with an explicit policy for this profile: `index`, `structural-hierarchy`, `publication-unit-metadata`, `contributor-metadata`, `margin-objects`, `apparatus`.

| Module | Policy | Starter default |
| --- | --- | --- |
| `verse-structure` | required | on |
| `index` | optional | off |
| `structural-hierarchy` | discouraged | off |
| `publication-unit-metadata` | discouraged | off |
| `contributor-metadata` | recommended | off |
| `margin-objects` | optional | off |
| `apparatus` | optional | off |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- verse content — `PSEStanza` and stable `PSEVerseLine` identities
- `config/locator-orchestration.json` — verse-line locator policy where used
- `book.yml` — publication metadata

Create a private starter project with:

```text
pse new /path/to/private-projects --profile poetry
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- Display a line label only when the edition needs one; stable IDs remain independent.
- Adjust verse indentation and stanza spacing through profile/local presentation, not by changing IDs.
- Activate index or apparatus for annotated or larger collections when justified.

## Boundaries and limitations

- Visible line numbers are not required and are not semantic IDs.
- The profile does not infer metrical structure or validate scansion.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/poetry/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py poetry
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
