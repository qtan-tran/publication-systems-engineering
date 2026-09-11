# Runtime Discovery Contract — current release

Status: **implemented and regression-tested in current release**

Publication Systems Engineering separates a private downstream book project from the framework runtime that builds it. A book project must not need to know where the PSE source repository is located.

## Discovery order

The CLI resolves the runtime in this order:

1. `PSE_ROOT`, when an operator deliberately sets it. An invalid override fails closed.
2. A valid PSE source checkout containing `core/pse-core.sty` and a runtime/project marker.
3. The source checkout containing the executing CLI during development/editable use.
4. Installed runtime data under the Python installation's `share/publication-systems-engineering/` location, with a colocated `share/` fallback for `pip --target`/bundled deployments.

Normal installed use requires neither `PSE_ROOT` nor `PYTHONPATH`.

## Runtime payload

The minimal runtime payload is deliberately small:

```text
share/publication-systems-engineering/
├── core/
│   └── pse-core.sty
└── runtime/
    └── pse-runtime.json
```

The Python package supplies the CLI. The runtime payload supplies production resources that LuaLaTeX must discover.

## Rules

- Downstream projects never vendor the framework core by default.
- Generated projects may live anywhere the user has appropriate private storage and write permission.
- `PSE_ROOT` is an explicit development/operations override, not an installation requirement.
- An invalid explicit override must not silently fall back to a different runtime.
- Runtime discovery is observable through `pse doctor`.
- Installed-runtime behavior must be regression-tested from outside the framework repository.

## Future compatibility

Profiles, schemas and other runtime assets may later join the installed runtime payload. They must follow the same versioned discovery contract rather than inventing profile-specific environment variables.
