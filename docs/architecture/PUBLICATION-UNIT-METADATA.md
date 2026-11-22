# Publication-unit metadata

`publication-unit-metadata` owns reusable metadata attached to a stable publication-unit ID. It does not own contributor identity or typography.

## API

- `\PSEDeclarePublicationUnit{id}{title}`
- `\PSEPublicationUnitSubtitle{id}{subtitle}`
- `\PSEPublicationUnitAbstract{id}{text}`
- `\PSEPublicationUnitKeywords{id}{keywords}`
- `\PSEPublicationUnitDOI{id}{doi}`
- `\PSEPublicationUnitContributor{unit-id}{contributor-id}{role}`
- `\PSEOpenPublicationUnit{id}`

Contributor name, affiliation, and ORCID are resolved from `contributor-metadata`; they are not copied into the publication-unit record. The module exposes presentation hooks so profiles decide how the opener is rendered.

The edited-collection profile enables the module by default. Other profiles expose it according to their module policy.
