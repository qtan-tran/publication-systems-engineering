---
title: Publication-unit and contributor metadata
description: Describe reusable publication units and contributor relations without duplicating contributor identity.
---

# Publication-unit and contributor metadata

PSE separates **publication-unit metadata** from **contributor identity**. A publication unit can be a chapter or another independently described unit. A contributor is a person associated with one or more units through contribution relations.

A publication unit may carry a stable ID, title, subtitle, abstract, keywords, DOI, and contributor relations. Contributor name, affiliation, and ORCID belong to the contributor registry and are not copied into each chapter record.

This matters in edited books: the same person can be an author of one chapter, an editor elsewhere, or hold another role in another publication unit without changing their identity record.

## Publication-unit metadata policy

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | recommended | off |
| [Basic Book](../profiles/basic-book.md) | optional | off |
| [Bilingual Edition](../profiles/bilingual-edition.md) | optional | off |
| [Critical Edition](../profiles/critical-edition.md) | optional | off |
| [Drama](../profiles/drama.md) | discouraged | off |
| [Edited Collection](../profiles/edited-collection.md) | required | on |
| [Literary Fiction](../profiles/literary-fiction.md) | discouraged | off |
| [Poetry](../profiles/poetry.md) | discouraged | off |
| [Scholarly Edition](../profiles/scholarly-edition.md) | recommended | off |

## Contributor metadata policy

| Profile | Policy | Starter default |
| --- | --- | --- |
| [Academic Monograph](../profiles/academic-monograph.md) | recommended | off |
| [Basic Book](../profiles/basic-book.md) | recommended | off |
| [Bilingual Edition](../profiles/bilingual-edition.md) | required | on |
| [Critical Edition](../profiles/critical-edition.md) | required | on |
| [Drama](../profiles/drama.md) | recommended | off |
| [Edited Collection](../profiles/edited-collection.md) | required | on |
| [Literary Fiction](../profiles/literary-fiction.md) | optional | off |
| [Poetry](../profiles/poetry.md) | recommended | off |
| [Scholarly Edition](../profiles/scholarly-edition.md) | required | on |

## Recommended model

Use stable machine-facing IDs for units and contributors. Attach roles to the **contribution relation**, not permanently to the person. This avoids claims such as “this contributor is always an editor” when the role is contextual.

For an edited collection, both modules are required and the profile presents metadata-rich unit openers. Academic and scholarly profiles can activate publication-unit metadata when chapters need independent metadata, while contributor metadata remains useful even when no chapter DOI or abstract is needed.

## Boundaries

PSE does not resolve identities against external ORCID/ROR services, validate DOI registration, or infer contribution roles. Those remain editorial or external-system responsibilities.

See the [Edited Collection profile](../profiles/edited-collection.md) for the strongest default use of this model.
