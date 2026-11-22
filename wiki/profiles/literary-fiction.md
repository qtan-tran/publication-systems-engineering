# Literary Fiction

**Profile ID:** `literary-fiction`  
**Best for:** novels, novellas, story collections, and reading-oriented prose where uninterrupted narrative rhythm should dominate the page.

Use another profile when projects that need visible scholarly infrastructure as a primary reading layer.

## What this profile feels like

Quiet and reading-oriented. Chapter openings are restrained, the text measure is prioritized, and specialist scholarly furniture stays out of the default reading flow.

Its integrated presentation preset is `fiction-reading`. The page-grid mode is `book`, side-material mode is `fallback`, apparatus mode is `deferred`, locator mode is `none`, and parallel-text mode is `none`.

## Semantic modules

Modules enabled by the generated starter: none.

Other modules with an explicit policy for this profile: `index`, `structural-hierarchy`, `publication-unit-metadata`, `contributor-metadata`, `margin-objects`, `apparatus`.

| Module | Policy | Starter default |
| --- | --- | --- |
| `index` | discouraged | off |
| `structural-hierarchy` | discouraged | off |
| `publication-unit-metadata` | discouraged | off |
| `contributor-metadata` | optional | off |
| `margin-objects` | optional | off |
| `apparatus` | discouraged | off |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- chapter content files — narrative source
- `book.yml` — title, author, language, publication year
- `config/pse-local.tex` — restrained project-local presentation adjustments

Create a private starter project with:

```text
pse new /path/to/private-projects --profile literary-fiction
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- Use typography overrides sparingly so the profile retains a coherent reading rhythm.
- Footnotes and margin objects are technically available, but should be editorially justified.
- Contributor metadata can be activated for special cases such as translators or introductions.

## Boundaries and limitations

- Index, structural hierarchy, publication-unit metadata, and apparatus are discouraged by default.
- This is not a substitute for line-level poetry, drama, or critical-edition semantics.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/literary-fiction/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py literary-fiction
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
