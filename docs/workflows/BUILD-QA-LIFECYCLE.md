# Build & QA Lifecycle Specification

## Lifecycle

```text
NEW → EDIT → BUILD → CHECK → REVIEW → RELEASE
                  ↘ FIX ↗
```

## `pse new`

Creates a valid project from a selected profile. It must:

- collect minimum metadata;
- validate requested options;
- write predictable directory structure;
- create a buildable minimal title;
- create local README and QA configuration;
- never require the user to understand internal core directories.

## `pse build`

Builds the title without deleting valid intermediates unless needed. It should:

- verify LuaLaTeX availability;
- resolve the configured profile/core;
- run the required compilation sequence;
- run bibliography/index processors when configured;
- write logs under a predictable build directory;
- return a meaningful exit status.

## `pse clean`

Removes generated/intermediate artifacts while preserving canonical source and user assets.

A clean build is:

`pse clean` → `pse build` → `pse check`

## `pse check`

Runs machine QA without rewriting source.

### Hard failures

- compilation failure;
- required source/dependency missing;
- invalid required metadata;
- configured bibliography/index processor failure;
- severe missing-glyph condition;
- incorrect required PDF page geometry;
- corrupted or missing output PDF.

### Review warnings

- overfull/underfull boxes;
- font substitution;
- hyperlink diagnostics;
- unexpected page-count drift;
- visual regression difference;
- density/pagination heuristics;
- nonfatal PDF metadata discrepancy.

Warnings are recorded in a structured report and can be promoted to failures per project policy.

## `pse release`

Release is a gated operation, not an alias for build.

Minimum release sequence:

1. clean build;
2. machine QA;
3. regression suite if shared code changed;
4. required visual review;
5. metadata validation;
6. release manifest;
7. checksums;
8. version/tag readiness check.

The release command must refuse to proceed after hard-failure gates.

## Source of truth

Canonical source must be distinguishable from:

- generated intermediates;
- build output;
- regression baselines;
- release artifacts.

PDF patching outside the source/build process is not a supported production workflow.
