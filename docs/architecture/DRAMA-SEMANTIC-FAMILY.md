# Drama Semantic Family Foundation

current release introduces drama semantics without imposing a drama house style. Stable speaker, act, and scene IDs are source semantics. Display names and typography remain presentation concerns.

## Public primitives

- `\PSEDeclareSpeaker{id}{display}`
- `\begin{PSESpeech}{id} ... \end{PSESpeech}`
- `\PSEStageDirection{text}`
- `\PSEAct{id}{display}`
- `\PSEScene{id}{display}`
- optional dramatic locator helpers through `dramatic-locators`

## QA policy

Undefined and duplicate speaker IDs are errors. Duplicate act/scene IDs are errors. Declared but unused speakers are review findings, because cast lists can legitimately contain silent or off-stage roles.

Drama semantics do not own security, proof, release, or visual typography.
