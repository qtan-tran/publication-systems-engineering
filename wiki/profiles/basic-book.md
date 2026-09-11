# Basic Book

**Profile ID:** `basic-book`  
**Best for:** general nonfiction, essays, manuals, memoir-like prose, and books that need a neutral starting point without specialist scholarly machinery.

Use another profile when projects whose identity depends on dramatic speakers, verse-line semantics, parallel alignment, or a critical apparatus.

## What this profile feels like

Conservative general book design: familiar chapters, sections, running heads, footnotes, and a comfortable reading measure.

Its integrated presentation preset is `book-reading`. The page-grid mode is `book`, side-material mode is `fallback`, apparatus mode is `deferred`, locator mode is `none`, and parallel-text mode is `none`.

## Semantic modules

Modules enabled by the generated starter: `index`, `structural-hierarchy`.

Other modules with an explicit policy for this profile: `publication-unit-metadata`, `contributor-metadata`, `margin-objects`, `apparatus`.

| Module | Policy | Starter default |
| --- | --- | --- |
| `index` | recommended | on |
| `structural-hierarchy` | required | on |
| `publication-unit-metadata` | optional | off |
| `contributor-metadata` | recommended | off |
| `margin-objects` | optional | off |
| `apparatus` | discouraged | off |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- `content/chapter-01.tex` — primary manuscript source
- `book.yml` — publication metadata
- `config/pse-local.tex` — local presentation overrides

Create a private starter project with:

```text
pse new /path/to/private-projects --profile basic-book
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- Keep the profile simple; add modules only for a real editorial need.
- The index is already recommended and enabled by default.
- Publication-unit metadata and margin objects are available but not assumed.

## Boundaries and limitations

- Critical apparatus is deliberately discouraged.
- The profile does not supply domain-specific semantics such as verse, drama, or bilingual alignment.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/basic-book/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py basic-book
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
