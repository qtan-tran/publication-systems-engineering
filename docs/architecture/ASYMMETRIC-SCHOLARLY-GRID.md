# Asymmetric Scholarly Grid

PSE 1.35 introduces a reusable **page-grid presentation contract**. The contract names the physical regions that a profile allocates before composition: inner gutter, primary text block, outer margin zone, header zone, footer zone, and an explicit apparatus allocation.

The grid is presentation infrastructure, not manuscript semantics. A note, locator, apparatus entry, or caption may later be placed into a grid region, but those semantic objects do not own page geometry.

## Contract

The core contract version is `\PSEPageGridContractVersion` = `1`. Profiles configure the grid with:

```tex
\PSEConfigurePageGrid
  {<inner>}{<outer>}{<top>}{<bottom>}
  {<head-height>}{<head-separation>}{<foot-separation>}
  {<apparatus-allocation>}
\PSEApplyPageGrid
```

The current profile baselines reserve `0mm` as a dedicated apparatus zone. This is deliberate: 1.35 establishes the allocation boundary but does not yet move apparatus or marginal objects into it. Later layout capabilities may reserve non-zero space without changing apparatus semantics.

Read-only presentation accessors include `\PSEGridInnerGutter`, `\PSEGridOuterMarginZone`, `\PSEGridPrimaryTextMeasure`, `\PSEGridHeaderHeight`, `\PSEGridHeaderSeparation`, `\PSEGridFooterSeparation`, and `\PSEGridApparatusZone`.

## Grid policy by profile

The capability policy for the asymmetric scholarly grid is:

| Profile | Policy |
| --- | --- |
| Critical Edition | required |
| Scholarly Edition | required |
| Bilingual Edition | recommended |
| Academic Monograph | recommended |
| Drama | recommended |
| Edited Collection | optional |
| Poetry | optional |
| Basic Book | optional |
| Literary Fiction | optional |

All profiles use the same core grid contract so that page geometry has one technical surface. The policy describes how central an asymmetric scholarly grid is to the publication type; it does not imply that optional profiles lack page geometry.

## Composition boundary

The grid must be resolved before ordinary page composition. PSE does not allow a semantic module to enlarge or shrink the page grid dynamically in response to content already being typeset. This keeps line measure, pagination, locators, and later margin-object placement reproducible.

## Ownership

- **Core** owns grid vocabulary, setters, accessors, and conservative defaults.
- **Profiles** choose reusable grid dimensions appropriate to a publication type.
- **Projects** may make title-specific overrides before composition.
- **Semantic modules** may consume available regions but must not own or silently resize them.

PSE 1.35 intentionally does not implement margin objects, side captions, or multi-stream apparatus placement. Those are later capabilities built on this contract.
