# Drama profile contract

The `drama` profile controls presentation only. Stable speaker IDs, act/scene registration, speech semantics, stage directions, and locator validation remain in semantic modules.

Presentation hooks available to the profile include `\PSEDramaActPresentation`, `\PSEDramaScenePresentation`, `\PSEDramaSpeechStartPresentation`, `\PSEDramaSpeechEndPresentation`, `\PSEDramaStageDirectionPresentation`, `\PSEDramaCastHeadingPresentation`, and `\PSEDramaCastEntryPresentation`.

Downstream profiles may renew these hooks. They must not reimplement speaker registries, locator validation, proof/security behavior, or release logic.
