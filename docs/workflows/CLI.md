# Command-line workflow

Publication Systems Engineering exposes the `pse` command for project generation, validation, builds, proofs, regression checks, releases, and semantic diagnostics.

The stable command families are:

- `pse new`
- `pse build`
- `pse check`
- `pse clean`
- `pse proof`
- `pse doctor`
- `pse profiles`
- `pse modules`
- `pse visual-check`
- `pse regression`
- `pse release`
- `pse verify-release`
- `pse release-migration`
- `pse contracts`
- `pse semantic-ir`

Run `pse --help` and `pse <command> --help` for the installed command surface. Public command behavior is governed by the compatibility policy in `docs/architecture/COMPATIBILITY-MIGRATION-POLICY.md`.

## Release manifest compatibility

`pse release` writes publication release manifest schema `0.2`. `pse verify-release` strictly validates `0.2`, rejects unknown future schema versions, and retains warning-level verification compatibility for legacy schema `0.1`. See [Publication release manifest contract](../release/RELEASE-MANIFEST-CONTRACT.md).

`pse contracts` exposes the active runtime's installed release/output-inspection contract files and accepted schema versions. `pse release-migration <release-dir>` produces a non-mutating assessment for historical artifacts; it does not rewrite a legacy release or infer evidence that did not exist historically.
