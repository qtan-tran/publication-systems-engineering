# GitHub Wiki mirror decision — 1.46

**Decision: do not create a GitHub Wiki mirror at this stage.**

The canonical documentation source remains `/wiki`, rendered by MkDocs Material. Maintaining an additional GitHub Wiki surface would add duplicated public URLs and increase the chance of source divergence without adding a capability currently missing from the documentation site.

Any future mirror must satisfy three conditions: it is generated one-way from `/wiki`; direct editing is treated as unsupported; and URL/migration behavior is documented before activation. This decision can be revisited without changing the canonical-source contract.
