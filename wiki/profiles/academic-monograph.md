# Academic Monograph

**Profile ID:** `academic-monograph`  
**Best for:** research monographs, dissertations revised as books, and sustained scholarly arguments with a conventional chapter hierarchy.

Use another profile when a play, verse collection, parallel bilingual edition, or source-critical edition whose primary structure is not ordinary prose chapters.

## What this profile feels like

Structured and restrained. Numbered hierarchy and scholarly notes are easy to scan, while the page remains less apparatus-heavy than an edition profile.

Its integrated presentation preset is `scholarly-monograph`. The page-grid mode is `asymmetric-scholarly`, side-material mode is `outer-margin`, apparatus mode is `available`, locator mode is `none`, and parallel-text mode is `none`.

## Semantic modules

Modules enabled by the generated starter: `index`, `structural-hierarchy`.

Other modules with an explicit policy for this profile: `publication-unit-metadata`, `contributor-metadata`, `margin-objects`, `apparatus`.

| Module | Policy | Starter default |
| --- | --- | --- |
| `index` | recommended | on |
| `structural-hierarchy` | required | on |
| `publication-unit-metadata` | recommended | off |
| `contributor-metadata` | recommended | off |
| `margin-objects` | recommended | off |
| `apparatus` | optional | off |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- `content/chapter-01.tex` — replace the synthetic chapter with your manuscript
- `book.yml` — title, author, language, and publication year
- `config/semantic-modules.json` — activate optional scholarly capabilities only when needed

Create a private starter project with:

```text
pse new /path/to/private-projects --profile academic-monograph
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- Use `config/pse-local.tex` for project-local typography or spacing changes instead of editing the shared profile.
- Add publication-unit metadata when individual chapters need abstracts, keywords, DOI-like identifiers, or contributor relations.
- Activate apparatus or margin objects only when the argument genuinely needs them.

## Boundaries and limitations

- No canonical locator system is enabled by the profile. If stable source locators are central, start from an edition profile instead.
- It assumes prose hierarchy as the main organizing structure.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/academic-monograph/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py academic-monograph
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
