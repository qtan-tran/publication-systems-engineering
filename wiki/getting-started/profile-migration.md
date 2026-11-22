# Migrating projects from PSE 1.47 to 1.48

PSE 1.48 deliberately reduces the supported presentation profiles from nine to six. Old profile identifiers **are not silently aliased**: `pse new` and project validation reject a removed profile until its owner explicitly migrates it. Make a copy of your title-local source before migrating.

| Former profile | Recommended migration | Important qualification |
| --- | --- | --- |
| `basic-book` | `academic-monograph` | Disable unnecessary scholarly modules and review typography; there is no byte-for-byte visual equivalence. |
| `scholarly-edition` | `critical-edition` | An annotated edition does not necessarily establish a critical text; use critical-edition presentation without claiming textual criticism. Verify apparatus and canonical locator conventions. |
| `poetry` | `literary-fiction` only for narrative-oriented work | The `verse-structure` module remains, but verse/stanza presentation is **not** automatically supplied by literary-fiction. Verse-heavy books need a title-local adaptation and visual review. |

Update `book.yml` profile, review `main.tex` package imports and `config/semantic-modules.json`, then run `pse build`, `pse check` and visual review. Old rendered demo/visual fixtures are not retained as supported profile contracts.

## Minimal production workflow

For ordinary editorial iterations: `pse build .` then `pse check .`. For recipient reviews: `pse proof . --recipient "Name"`. For signed-off publication artifacts: `pse release .` then `pse verify-release <release-directory>`. Do not run candidate/release-engineering audits on each edit. They are maintainer/CI controls, not daily publishing steps.
