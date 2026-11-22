# Visual Regression

Visual regression complements, but never replaces, human proofing.

The current release implementation renders selected canonical pages at a fixed DPI and compares them with approved PNG baselines. The comparison records SHA-256 equality, material pixel-difference ratio, image geometry and mean absolute pixel error.

Small renderer/platform differences are expected. Therefore visual drift is a `review` finding by default. It is not a hard error unless the regression infrastructure itself cannot render/compare the required page.

Baselines must not be updated merely to make a regression report green. Any intentional baseline change should be explained in the change history.

The current renderer dependency is `pdftoppm` (Poppler). It is needed for framework visual regression, not for ordinary `pse build`.
