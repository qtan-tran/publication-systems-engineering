# Architecture Specification — current release

Status: **Draft for architecture freeze**  
Version: **0.1.0-alpha**

## 1. Purpose

Publication Systems Engineering (PSE) is a framework for constructing book-production systems, not a collection of finished visual templates. Its first production target is print-ready PDF produced by LuaLaTeX.

The framework must remain useful across different kinds of series without embedding title-specific or organization-specific production logic in the core.

## 2. System model

The canonical production flow is:

`content → metadata → title configuration → profile + semantic modules → core → build → QA → release`

Each stage has one responsibility and should not silently take over responsibilities from another stage.

## 3. Architectural layers

### 3.1 Core

The core provides stable primitives and cross-project infrastructure:

- engine and compatibility checks;
- page-model primitives;
- baseline typography interfaces;
- metadata access;
- navigation primitives;
- note infrastructure;
- output/PDF primitives;
- diagnostic hooks.

The core must not know individual book titles or downstream brands.

### 3.2 Profiles

Profiles compose presentation capabilities for a class of books. Current generator-supported profiles:

- `basic-book`
- `literary-fiction`
- `academic-monograph`
- `scholarly-edition`
- `critical-edition`
- `poetry`
- `edited-collection`
- `drama`
- `bilingual-edition`

Profiles are behavioral configurations, not visual imitations of existing publishers.

### 3.3 Title projects

Generated projects contain:

- canonical content source;
- title metadata;
- title-local configuration;
- title assets permitted by the project license;
- bibliography/index data where applicable;
- title-local tests or release checks.

Title-local overrides are allowed only through documented extension points.

## 4. Dependency rule

> **Core knows nothing about profiles or titles. Profiles may depend on core. Titles may depend on a profile and on documented core APIs. Dependencies never point upward.**

Circular dependencies are architectural defects.

## 5. Canonical source policy

For v0.x, generated book projects use LaTeX as the canonical prose/content source. PSE does not introduce a Markdown, XML, TEI, or other conversion layer in the initial architecture.

Metadata is externalized from prose source and should be machine-readable from the beginning.

## 6. Metadata

The initial metadata format will be YAML unless implementation testing demonstrates a material cross-platform problem. Metadata is validated against a schema before release.

The design objective is single-entry metadata: title, author, contributor, language, edition, date, identifier, and series information should not be manually duplicated across multiple title files.

## 7. Build abstraction

Users should not need to memorize engine command sequences. PSE will expose stable commands through a project tool:

- `pse new`
- `pse build`
- `pse check`
- `pse clean`
- `pse release`

The implementation language is intentionally not frozen in current release. Cross-platform maintainability is more important than early tool choice.

## 8. Quality architecture

QA is part of the architecture, not an afterthought. Checks are divided into:

- build validity;
- source validity;
- metadata validity;
- PDF/output validity;
- regression validity;
- visual review.

Warnings are not automatically failures. Each check has an explicit severity.

## 9. Extension policy

New functionality should first be classified as:

1. title-local requirement;
2. reusable profile requirement;
3. genuinely core requirement.

Promotion upward requires evidence of reuse. The core must not become an accumulation point for exceptions.

## 10. Portability

Supported host operating systems:

- Windows;
- macOS;
- Linux.

The framework must not require a specific graphical editor or IDE.

## 11. Font policy

Core, examples, and regression fixtures use only fonts whose licenses permit redistribution and commercial book production. Downstream projects may configure other fonts at their own responsibility.

Font files themselves should not be duplicated into the repository unless redistribution is explicitly permitted and doing so is architecturally necessary.

## 12. Public/private boundary

This repository contains only generic architecture and synthetic examples. It must not contain confidential downstream source, private macros, proprietary series rules, or internal production artifacts.

## 13. Non-goals for v0.x

- EPUB/HTML generation;
- Markdown/XML/TEI ingestion;
- cloud editorial platform features;
- publisher-specific visual clones;
- WYSIWYG editing;
- automated copyediting or AI editorial decisions.

## 14. Architecture acceptance criteria

current release can freeze when:

- layer responsibilities are explicit;
- dependency direction is explicit;
- project directory contract is explicit;
- build lifecycle is explicit;
- QA severities are explicit;
- regression strategy is explicit;
- licensing strategy is explicit enough to prevent accidental public release under incompatible terms;
- roadmap separates core work from later profiles and convenience tooling.
