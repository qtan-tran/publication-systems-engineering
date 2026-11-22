# Regression Strategy

## Principle

A regression occurs when a change causes previously valid behavior to break or materially drift. Because PSE centralizes shared rules, regression testing is mandatory for shared-core and profile changes.

## Test layers

### 1. Smoke regression

Fast checks that each selected fixture:
- compiles;
- produces a PDF;
- has expected page geometry;
- has no fatal references or missing required files.

### 2. Feature regression

Synthetic fixtures exercise specific capabilities:

- `RegressionBasicBook`
- `RegressionLongHeadings`
- `RegressionLongNotes`
- `RegressionIndex`
- `RegressionBibliography`
- `RegressionMultilingual`
- `RegressionGreek`
- `RegressionDrama`
- `RegressionScholarly`
- `RegressionFrontMatter`
- `RegressionStress`

Names are descriptive and generic. Fixture prose is synthetic.

### 3. Visual regression

Selected canonical pages are rendered to images and compared with approved baselines.

Visual difference is a **review gate by default**, not an automatic hard failure. This prevents harmless rasterization or pagination differences from blocking all development while still making typography drift visible.

### 4. Release regression

Before a tagged framework release:
- all supported profiles build;
- all regression fixtures build;
- hard failures are zero;
- warning deltas are reviewed;
- visual baseline changes are explicitly approved.

## Change-to-test mapping

- title-local change → title checks only;
- profile change → profile fixtures + core smoke tests;
- core change → full regression suite;
- generator change → generator fixtures + generated-project build test;
- QA-tool change → self-tests + representative regression subset.

## Baseline discipline

A visual baseline must never be updated merely to make CI green. Baseline changes require a reason recorded in the change history.

## Performance

The suite must remain layered so routine editor work does not require the heaviest test run. Fast local checks and full CI/release checks are distinct operations.

## current release operational policy

current release implements the layered strategy with `pse regression`. Visual drift and page-count drift are `review` findings by default. Regression infrastructure failures and machine-QA `error` findings remain blocking. See `QA-SEVERITY-MODEL.md`, `VISUAL-REGRESSION.md`, and `REGRESSION-ORCHESTRATION.md`.
