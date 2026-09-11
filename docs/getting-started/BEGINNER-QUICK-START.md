# Beginner quick start

> The canonical public beginner path is now the [Beginner Handbook](../../wiki/getting-started/index.md). This technical quick start remains as a compact repository reference.

This path is for editors, researchers, and small publishing teams who want to see a result before learning PSE's architecture.

## 1. Check the finished examples first

Open the [profile demo gallery](PROFILE-DEMO-GALLERY.md). Choose the publication type closest to your project.

## 2. Install from the checked-out repository

From the PSE repository root:

```text
python -m pip install .
pse doctor --deep
```

`pse doctor --deep` should complete successfully before you move on.

## 3. See the available project profiles

```text
pse profiles --generator-only
```

Choose one profile id, for example `poetry`, `academic-monograph`, or `edited-collection`.

## 4. Create a private test project

Do not start with an unpublished manuscript. Create a project in private storage:

```text
pse new /path/to/private-projects --profile poetry
```

PSE creates a project directory inside the destination. The command output tells you its exact path.

## 5. Build and check the generated project

Change into the generated project directory, then run:

```text
pse build .
pse check . --human
```

Open `build/book.pdf`. Once this synthetic starter works, replace the starter content with project-owned material while keeping real manuscripts outside public repositories.

## 6. Reproduce a repository demo when needed

From the PSE repository root:

```text
python scripts/examples/build_profile_demos.py poetry
```

Replace `poetry` with any registered profile id. To rebuild all canonical demos, omit the profile argument.

## What you do not need to learn first

You do not need to understand the semantic IR, parser, release provenance, module registry, or profile API before creating a first book. Those layers become relevant when you customise or extend PSE.

For production work, continue with [Onboarding](../workflows/ONBOARDING.md), and use `pse proof`, `pse release`, and `pse verify-release` rather than treating an ordinary working build as a publication release.
