# Edited Collection

**Profile ID:** `edited-collection`  
**Best for:** multi-author books, edited volumes, proceedings-like collections, and books where chapters are publication units with their own contributor and metadata relations.

Use another profile when single-author books where chapter-level contributor metadata would add needless complexity.

## What this profile feels like

Chapter-oriented scholarly presentation. Publication units can carry title/subtitle, abstract, keywords, DOI-like identifier, and contributor relations while contributor identity remains reusable across the book.

Its integrated presentation preset is `scholarly-collection`. The page-grid mode is `book`, side-material mode is `fallback`, apparatus mode is `available`, locator mode is `none`, and parallel-text mode is `none`.

## Semantic modules

Modules enabled by the generated starter: `contributor-metadata`, `index`, `structural-hierarchy`, `publication-unit-metadata`.

Other modules with an explicit policy for this profile: `margin-objects`, `apparatus`.

| Module | Policy | Starter default |
| --- | --- | --- |
| `contributor-metadata` | required | on |
| `index` | recommended | on |
| `structural-hierarchy` | required | on |
| `publication-unit-metadata` | required | on |
| `margin-objects` | optional | off |
| `apparatus` | optional | off |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- publication-unit declarations — one semantic unit per chapter or contribution
- contributor declarations and contribution relations — identity separated from role
- chapter content files — manuscript source for each unit
- `book.yml` — volume-level metadata

Create a private starter project with:

```text
pse new /path/to/private-projects --profile edited-collection
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- A contributor can hold different roles in different publication units without duplicating identity.
- Use publication-unit abstracts, keywords, identifiers, and contributor credits at chapter openers.
- Optional apparatus and margin objects remain available for specialized collections.

## Boundaries and limitations

- The current contributor model is local and does not claim external ORCID/ROR identity resolution.
- It is not a journal issue management or submission-tracking system.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/edited-collection/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py edited-collection
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
