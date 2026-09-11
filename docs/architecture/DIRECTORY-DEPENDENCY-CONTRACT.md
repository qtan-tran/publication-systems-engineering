# Directory & Dependency Contract

## Repository-level layout

```text
publication-systems-engineering/
├── core/                 # generic runtime primitives (canonical source)
├── runtime/              # runtime manifest / install payload metadata
├── profiles/             # compositional book-type behavior
├── schema/               # machine-readable metadata/config schemas
├── tools/                # generator, build, QA, release tooling
├── tests/                # regression + visual tests + synthetic fixtures
├── examples/             # user-facing synthetic examples
├── docs/                 # architecture, workflow, QA, training, reference
├── scripts/              # thin platform wrappers only
└── .github/              # CI and repository automation
```

## Dependency graph

```text
tools ───────────────┐
                     v
                generated project
                     |
                     v
profiles ----------> core
   ^                 ^
   |                 |
 title config -------┘
   ^
   |
content + metadata
```

Tests may depend on all public layers. Core must never depend on tests, examples, profiles, or generated projects.

## Contracts

### `core/`

May contain only generic functionality with a documented public/internal interface distinction. The canonical framework source lives here; packaging installs the required runtime files under the platform's PSE runtime data location rather than requiring downstream projects to copy the core.

Forbidden:
- title names;
- series names;
- private downstream logic;
- profile-specific presentation decisions;
- fixture-specific hacks.


### `runtime/`

Contains runtime manifest metadata used for installation/discovery. It must not contain title-specific logic or private project data. Installed runtime resources are versioned with the Python CLI and are discovered through the current release runtime contract.

### `profiles/`

Each profile declares:
- core version/API compatibility;
- capabilities enabled;
- default configuration;
- documented extension points;
- regression fixtures required.

A profile must not patch another profile indirectly.

### `tools/`

Tooling coordinates lifecycle operations but must not silently rewrite canonical title content. Generated or normalized files must have explicit provenance.

### `tests/fixtures/`

Fixtures are synthetic and deliberately designed to exercise edge cases. They are not sample books to be copied into production unchanged.

## Generated project contract

The future generator should produce a project approximately like:

```text
my-book/
├── book.yml
├── main.tex
├── content/
├── config/
├── bibliography/
├── index/
├── assets/
├── tests/
├── README.md
└── .gitignore
```

The exact generated tree remains implementation-frozen only after current release prototype testing.

## No hidden dependencies

Every required external program, font family, package, or toolchain component must be declared in machine-readable configuration or installation documentation. A successful build must not depend on an editor's local manual state without documentation.
