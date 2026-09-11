# Project Generator

current release introduces `pse new` for creating secure-by-default downstream projects.

## Interactive use

```text
pse new ~/Books
```

The wizard asks for the minimum required metadata and creates a `basic-book` project unless another generator-supported profile is selected.

## Non-interactive use

```text
pse new ~/Books \
  --non-interactive \
  --title "Example Book" \
  --author "Example Editor" \
  --language en \
  --publication-year 2027 \
  --slug example-book
```

Non-interactive mode is intended for regression tests, automation, and controlled organizational provisioning.

## Supported profiles

Use `pse profiles --generator-only` for the authoritative installed registry. The current source tree contains nine generator-supported profiles, including `critical-edition`, `poetry`, and `edited-collection`.

Unsupported profiles fail closed instead of silently falling back.

## After generation

```text
pse build example-book
pse check example-book
pse proof example-book --recipient "Proofreader Name"
pse clean example-book
```

## Why generated projects are separate from the framework repository

The framework may be public while manuscript projects are private. The generator therefore creates downstream project boundaries rather than encouraging users to place confidential manuscripts inside the framework source tree.
