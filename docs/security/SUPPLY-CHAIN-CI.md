# Supply Chain and CI Security

## Dependency policy

PSE should keep the executable dependency set small. New runtime dependencies require a documented reason. Dependency versions should become increasingly pinned as release engineering matures, and release manifests should record relevant versions.

## CI policy

Public pull-request CI should run with read-only repository permissions wherever possible and without publishing credentials or commercial secrets. Workflows triggered by untrusted forks must not receive signing keys, private repository tokens, publication sources, or enterprise credentials.

CI should use synthetic fixtures only. Real unpublished manuscripts do not belong in the public PSE regression suite.

## Actions and external code

Third-party CI actions are dependencies. Prefer first-party platform actions and pin stable versions; later release hardening should pin immutable revisions where practical.

## TeX packages

Ordinary builds should not fetch packages from the network. Organizations that need deterministic production should maintain a controlled TeX distribution or container image and record its version in release provenance.
