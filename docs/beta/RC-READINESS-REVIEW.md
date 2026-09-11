# Release-candidate readiness review

This review follows completion of the 1.33–1.46 architecture and documentation roadmap. Its purpose is to distinguish **technical stabilization** from claims that require external evidence.

## Decision

PSE should enter a **stabilization-only freeze** at the current surface of 9 profiles and 14 semantic modules. It should not add product features before the release gates are cleared unless a correctness or security defect requires a contract change.

PSE is **not yet eligible to be advertised as a public release candidate or public licensed beta**. The remaining blockers are external or deployment-bound rather than reasons to expand the feature surface.

## Internally checkable readiness

The repository contains the candidate, release-evidence, documentation-deployment, integrity, packaging, schema, output-inspection, release-verification, and audit-evidence machinery needed to evaluate a candidate. `scripts/release/rc_readiness.py` emits a machine-readable review without treating missing external evidence as if it had been supplied.

The current compatibility baseline is profile manifest schema 1.1 with legacy 1.0 reading, semantic module manifest schema 1.1/API 1, semantic activation schema 1.1, parallel-text schema 1.0, bilingual layout schema 1.1 with legacy 1.0 reading, semantic IR 1.0, release manifest 0.2, and output-inspection report 0.2.

## External hard gates still open

1. independent legal review of the public/community and commercial licensing instruments;
2. approval and commit of the operative root `LICENSE`;
3. contributor-rights and dual-licensing permissions;
4. publication of a real commercial-licensing contact channel;
5. live Windows, macOS, Linux and release-evidence CI on the exact candidate commit;
6. live strict MkDocs Material render, generated-site QA, and documentation release evidence.

Local or synthetic regression evidence must not be substituted for these gates.

## Accessibility and conformance boundary

The current output-inspection contract checks a limited PDF baseline. Tagged-PDF structure, reading order, image alternative text, PDF/UA, WCAG, archival conformance, and legal accessibility compliance remain review or external-validation matters. They are not RC claims unless separately verified.

## Recommended next action

Do not create another feature roadmap yet. Push the GitHub-clean tree to the intended public repository, run the live workflows on an exact commit, retain their evidence, deploy the documentation site, and complete legal review. Any failures found there should become stabilization fixes against this frozen surface.
