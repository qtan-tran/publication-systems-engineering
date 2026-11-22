# Brand and attribution

The canonical project name is **Publication Systems Engineering**.

## Publication-release attribution

Every ebook released through the PSE publication-release pipeline must contain the canonical PSE attribution banner on either the **copyright/publication page** or the **colophon**. The bundled asset is:

`core/pse-attribution-banner.png`

The standard `\PSEPublicationPage` renders the banner automatically. A custom copyright page or colophon may instead place it explicitly with `\PSEAttributionBanner`. A final `pse release` is blocked when the build does not contain evidence that this macro rendered.

The banner contains the project wordmark and the primary attribution line:

> **Produced with Publication Systems Engineering.**

It also carries the approved explanatory/creator text embedded in the canonical artwork. Do not replace the banner with a text-only approximation for a PSE ebook release unless a later public brand specification explicitly permits that variant.

This release contract is an operational PSE framework requirement. Whether and how attribution is expressed as a legally enforceable licence condition remains subject to the final independently reviewed licence.

Using PSE does not imply that PSE owns the manuscript, translation, images, or other publication content. Trademark and naming permissions are governed separately from copyright permissions. Do not imply endorsement or official status for a fork or derivative distribution.
