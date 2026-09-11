# Contributing

Publication Systems Engineering is **maintainer-led and contribution-friendly**.

## Current contribution status

During beta-candidate staging, external code contributions are **not yet accepted for merge** until contributor rights for dual licensing are legally finalized. This avoids accepting code under ambiguous commercial relicensing rights.

Users may still prepare:

- synthetic bug reproductions;
- documentation corrections;
- narrowly scoped architecture proposals;
- security reports through the channel described in `SECURITY.md`.

Do not submit confidential manuscripts, recipient proofs, proprietary downstream architecture, credentials, or commercial contract material.

## Engineering rules

1. `main` must remain buildable.
2. Core changes require a dedicated branch and review.
3. One change should have one clear purpose.
4. Generated build/release artifacts must not be committed unless explicitly approved as fixtures/baselines.
5. Public API, schema, directory-contract, or lifecycle changes require documentation and migration notes.
6. Core/profile/module changes require regression coverage appropriate to their layer.
7. Profiles must not duplicate security, QA, runtime, proof, or release logic.
8. Semantic modules must not name arbitrary executable QA hooks.
9. No confidential downstream material may enter the public repository.
10. Do not add publisher-imitation profiles or design references.

See `docs/architecture/COMPATIBILITY-MIGRATION-POLICY.md` and `docs/profiles/PROFILE-AUTHORING-GUIDE.md`.
