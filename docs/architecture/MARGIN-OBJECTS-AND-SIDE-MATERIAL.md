# Margin Objects and Side Material

PSE 1.36 introduces `margin-objects`, a reusable semantic module for material whose preferred presentation may be in an outer page zone but whose meaning must survive when that zone is unavailable.

## Ownership boundary

The module owns stable object identity, object type, and content. The page-grid/core/profile presentation layer owns placement. A profile may place an object in the outer margin, while another profile or output path may use the deterministic fallback in the primary text stream. Semantic content must never disappear merely because margin placement is unavailable.

The supported version-1 object types are `marginal-note`, `side-caption`, `apparatus-anchor`, `locator-marker`, and `running-side`. These names describe reusable publication functions, not a particular visual style.

## API

```tex
\PSEDeclareMarginObject{marginal-note}{mn-001}{A concise contextual note.}
\PSEPrintMarginObject{mn-001}
```

Convenience forms declare and render in one operation:

```tex
\PSEMarginalNote{mn-002}{Context for this passage.}
\PSESideCaption{sc-001}{Caption material.}
\PSEApparatusAnchor{aa-001}{Apparatus anchor material.}
\PSELocatorMarker{lm-001}{Locator marker material.}
\PSERunningSideObject{rs-001}{Running-side material.}
```

IDs must be unique and stable. Rendering an undeclared ID is an error.

## Presentation and fallback

Core defaults to `fallback` mode. `\PSEUseOuterMarginObjects{<width>}{<separation>}` switches a profile to `outer-margin` presentation and establishes a fixed `marginparwidth` and `marginparsep`. This is configured before body composition; semantic modules do not resize the page grid dynamically.

The fallback is deliberately visible in the primary reading stream. It is not an accessibility certification and does not imply that arbitrary margin placement has a verified reading order in tagged PDF.

## Profile policy

| Profile | Policy | Default |
| --- | --- | --- |
| Critical Edition | recommended | on |
| Scholarly Edition | recommended | on |
| Bilingual Edition | recommended | off |
| Academic Monograph | recommended | off |
| Drama | recommended | off |
| Edited Collection | optional | off |
| Poetry | optional | off |
| Basic Book | optional | off |
| Literary Fiction | optional | off |

The policy advertises availability and sensible defaults; it does not make side material mandatory in a manuscript.

## Deferred work

Collision management between dense margin objects, semantic attachment to apparatus/locator records, advanced running-side heads, and formal tagged-PDF reading-order semantics are outside 1.36. Later increments may integrate these capabilities without changing the stable object identity contract.
