# Drama

**Profile ID:** `drama`  
**Best for:** plays, dramatic texts, performance scripts, and scholarly/readable editions where speakers, stage directions, acts/scenes, and dramatic line locators matter.

Use another profile when ordinary prose or verse where dramatic structure would be artificial.

## What this profile feels like

Performance-aware and line-addressable. Speaker labels, stage directions, structural divisions, and dramatic locators are presentation-aware while their semantics remain independent of page position.

Its integrated presentation preset is `dramatic-reading`. The page-grid mode is `asymmetric-scholarly`, side-material mode is `outer-margin`, apparatus mode is `available`, locator mode is `primary-visible`, and parallel-text mode is `none`.

## Semantic modules

Modules enabled by the generated starter: `drama-structure`, `dramatic-locators`, `index`.

Other modules with an explicit policy for this profile: `structural-hierarchy`, `publication-unit-metadata`, `contributor-metadata`, `margin-objects`, `apparatus`.

| Module | Policy | Starter default |
| --- | --- | --- |
| `drama-structure` | required | on |
| `dramatic-locators` | required | on |
| `index` | recommended | on |
| `structural-hierarchy` | discouraged | off |
| `publication-unit-metadata` | discouraged | off |
| `contributor-metadata` | recommended | off |
| `margin-objects` | recommended | off |
| `apparatus` | recommended | off |

`required` means the profile depends on that semantic capability. `recommended`, `optional`, and `discouraged` describe editorial fit; they do not mean that every technically possible combination is desirable.

## Start with these project areas

- dramatic content source — speakers, stage directions, acts/scenes, and line identities
- `config/locator-orchestration.json` — dramatic-line locator policy
- `book.yml` — publication metadata

Create a private starter project with:

```text
pse new /path/to/private-projects --profile drama
```

Then run:

```text
pse build .
pse check . --human
```

Do not edit generated files in `build/` as manuscript source, and do not edit the shared PSE core to customize a single book.

## Useful customization points

- Activate apparatus when editorial or explanatory intervention is needed.
- Contributor metadata is available for translators, editors, or other roles.
- Use project-local presentation overrides for speaker spacing and display choices rather than changing semantic commands.

## Boundaries and limitations

- General prose structural hierarchy is discouraged by default because dramatic structure is authoritative.
- The profile does not model rehearsal management, blocking software, or performance-rights clearance.

## Synthetic demo

The repository contains a synthetic source project and finished PDF under:

```text
examples/profiles/drama/
```

From the PSE repository root, rebuild that demo with:

```text
python scripts/examples/build_profile_demos.py drama
```

The demo is for understanding the profile, not a manuscript template to copy blindly. Start a real book with `pse new` so project metadata, module activation, and generated configuration are coherent.

## Related handbook pages

Return to the [profile overview](index.md), or continue with [Build and Check Your PDF](../getting-started/build-and-check.md). For features such as apparatus, margin objects, parallel text, or locators, see [Book Features](../book-features/index.md).
