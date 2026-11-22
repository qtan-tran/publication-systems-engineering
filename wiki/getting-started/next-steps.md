---
title: Where to Go Next
description: Move from a first working PSE build toward profile-specific features, proofs, QA, and release.
---

# Where to go next

Once a synthetic starter builds and checks successfully, replace it gradually with project-owned content. Keep using the short edit/build/check/inspect loop rather than waiting until the entire manuscript has been imported.

For the next learning step, choose the path that matches your work:

- explore [Book Profiles](../profiles/index.md) when the publication type drives the next decision;
- explore [Book Features](../book-features/index.md) for apparatus, locators, parallel text, or margin material;
- read [How PSE Works](../how-pse-works/architecture-overview.md) when you need to understand the boundary between core, profiles, semantic modules, and title source;
- use [Customization](../customization/typography.md) only after the baseline profile works;
- continue to [Quality and Release](../quality-release/index.md) before treating an output as a publication artifact.

## Working PDF, proof, and release are different things

`pse build` creates a working PDF. `pse proof` creates a recipient-specific proof artifact. `pse release` promotes a final build through the release contract, and `pse verify-release` verifies the resulting release evidence. Do not use an ordinary working build as a substitute for the release boundary.

The Beginner Handbook deliberately stops before advanced profile APIs, semantic-module authoring, release audit engineering, and framework development. Those are separate tasks, not prerequisites for making your first book.
