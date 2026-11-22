# Semantic Namespace Contract

current release introduces semantic namespaces so independent module families can coexist without sharing unqualified identifiers. Public semantic APIs SHOULD qualify internal identifiers by namespace. The canonical locator compatibility API maps to the `canonical` locator namespace.

## Activation
Profiles may declare default semantic modules. Titles may add modules through `config/semantic-modules.json`. The runtime merges both sets, resolves direct dependencies and required capabilities, rejects conflicts, and validates profile compatibility.

## Capability graph
Modules declare `capabilities` and `requires_capabilities`. A required capability must have exactly one active or uniquely discoverable provider. Ambiguous providers fail closed. Direct `depends_on` remains supported for explicit structural dependencies.

## Security boundary
Module manifests are declarative. `qa_hooks` are names from an allow-list; manifests cannot name executable Python or shell code. Modules cannot redefine proof, release, runtime discovery, or security semantics.
