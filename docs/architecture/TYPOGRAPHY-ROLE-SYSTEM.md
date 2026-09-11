# Typography Role System

PSE defines typography as a presentation contract rather than scattering font-family, size, weight, and shape decisions across semantic code. The role system is owned by `pse-core`; profiles override role values, while semantic modules may consume roles without redefining them.

## Contract version

`\PSETypographyRoleContractVersion` is currently `1`.

## Public roles

- `\PSETypographyBodyRole` - ordinary running text.
- `\PSETypographyDisplayRole` - display-family material such as compact labels.
- `\PSETypographyChapterTitleRole` - chapter/unit title typography.
- `\PSETypographySectionHeadingRole` - first-level section heading typography.
- `\PSETypographySubsectionHeadingRole` - subordinate prose heading typography.
- `\PSETypographyMetadataLabelRole` - labels such as Abstract, Keywords, DOI, or equivalent publication metadata.
- `\PSETypographyMetadataValueRole` - compact metadata values.
- `\PSETypographyRunningHeadRole` - running heads and comparable navigational display text.
- `\PSETypographyCaptionRole` - captions and caption-like explanatory text.
- `\PSETypographyApparatusRole` - critical/editorial apparatus text.

Roles are declarations: they select typography but do not own content, semantic identity, spacing, alignment, numbering, page geometry, or publication metadata.

## Ownership

`pse-core` owns the role names and conservative defaults. A profile may `\renewcommand` a role to establish a reusable profile presentation. Semantic modules must not redefine these commands. A title may make a local exception in `config/pse-local.tex`; such an override should not be promoted to a profile unless it is reusable.

## What this release does not do

The role system is not a brand theme, font marketplace, CSS-like cascade, or web-design layer. It does not introduce publisher-specific branding, colors, logos, or house-style names. Font files remain governed by the existing open-font policy.

## Stability rule

A profile may change the implementation of a role without changing semantic manuscript source. Conversely, semantic modules must remain meaningful if a profile changes family, size, weight, or shape. This boundary is regression-tested.
