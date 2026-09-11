# Scholarly Edition

**Profile ID:** `scholarly-edition`  
**Best for:** annotated scholarly editions that need canonical locators, apparatus, multilingual text, bibliography, scholarly matter, and side material without the stronger source-critical emphasis of the Critical Edition profile.

Use another profile when simple reading editions or monographs that do not need edition infrastructure.

## What this profile feels like

Integrated scholarly edition baseline: compact hierarchy, asymmetric grid, visible canonical locators, multi-stream apparatus, multilingual support, bibliography, index, and outer-margin presentation.

Its integrated presentation preset is `scholarly-edition`. The page-grid mode is `asymmetric-scholarly`, side-material mode is `outer-margin`, apparatus mode is `multi-stream`, locator mode is `primary-visible`, and parallel-text mode is `none`.

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
| `publication-unit-metadata` | recommended | off |
| `contributor-metadata` | required | on |
| `margin-objects` | recommended | on |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- edited/annotated text source with canonical locator declarations
- apparatus source linked to locator identities
- scholarly front/back matter and bibliography
- `config/locator-orchestration.json` plus locator schemes
- `book.yml` and contributor metadata

Create a private starter project with:

```text
pse new /path/to/private-projects --profile scholarly-edition
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- Use publication-unit metadata when edition components need their own metadata layer.
- Keep apparatus stream semantics separate from how labels are rendered.
- Use margin objects for side material and stable locators for addressability across output changes.

## Boundaries and limitations

- PSE validates structural contracts, not the scholarly correctness of annotations or citations.
- For a strongly source-critical text with explicit editorial intervention as the center of the edition, prefer `critical-edition`.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/scholarly-edition/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py scholarly-edition
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
