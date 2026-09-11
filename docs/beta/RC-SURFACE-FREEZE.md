# Release-candidate surface freeze

Status: **stabilization freeze; not a public release candidate and not a public licensed beta**.

After the documentation roadmap through 1.46, PSE freezes the current product surface at **9 presentation profiles and 14 semantic modules** while release-candidate readiness is evaluated. The freeze is intended to reduce change risk before the external release gates are cleared.

## Frozen during stabilization

Do not add a tenth profile, a fifteenth semantic module, a new public CLI family, or a new publication output format during this stabilization window. Existing public commands, schemas, semantic IDs, profile/module policy, proof/release boundaries, audit evidence contracts, documentation IA, and the current PDF production target should change only for correctness, security, compatibility, or release-blocking defects.

A necessary corrective change is allowed when preserving existing behavior would be materially wrong. Such a change must be documented in the changelog and supplied with migration guidance when it affects a frozen public contract.

## What the freeze does not mean

The freeze does not assert that the repository is legally releasable, that live cross-platform CI has passed, that the documentation site has deployed successfully, or that accessibility/conformance has been certified. It also does not prevent documentation corrections, test hardening, packaging fixes, or security fixes.

## Exit conditions

The stabilization freeze may advance to an actual public release-candidate decision only after the maintainer has evidence for the external hard gates in `PUBLIC-BETA-CHECKLIST.md`: independent legal review, an approved operative licence, contributor/dual-licensing rights, a real commercial inquiry channel, live exact-commit cross-platform CI, and the required release/documentation evidence.

Until then, versioned snapshots remain engineering candidates.
