# Public Documentation Information Architecture

PSE 1.40 freezes the primary top-level information architecture for the canonical `/wiki` documentation source. The freeze applies to user-facing conceptual categories and stable URL families, not to the number of pages inside each category.

## Canonical top-level navigation

1. Getting Started — `/getting-started/`
2. How PSE Works — `/how-pse-works/`
3. Book Profiles — `/profiles/`
4. Book Features — `/book-features/`
5. Workflows — `/workflows/`
6. Quality and Release — `/quality-release/`
7. Customization — `/customization/`
8. Reference — `/reference/`

The canonical `/wiki` directory names now match these clean URL families directly. Numeric implementation prefixes are intentionally avoided so public links remain readable and stable.

## Audience rule

`/wiki` explains PSE to authors, editors, translators, publishers, designers, and developers. `/docs` specifies technical contracts for implementers. Public Wiki prose should lead with publishing concepts and tasks, then link to technical contracts where useful.

## URL stability

Public page names should describe user concepts rather than internal implementation versions. Avoid version numbers, internal phase labels, or module implementation names in URLs unless the page is explicitly API/reference documentation.

## Presentation and branding boundary

PSE 1.41 adds the restrained documentation-platform baseline after the IA and publication presentation system were stabilized. The IA remains independent of theme details. Logo treatment, broader product-site branding, and analytics remain separate deployment decisions; changing them must not require URL or content-architecture changes.
