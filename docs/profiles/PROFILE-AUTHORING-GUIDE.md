# PSE Profile Authoring Guide

## Purpose

A profile is a presentation layer that inherits the PSE backbone. It may define page architecture, typography, heading hierarchy, running heads, folios, and documented presentation hooks. It must not duplicate or override security, metadata setters, runtime discovery, proof controls, QA semantics, release semantics, or provenance logic.

## Manifest contract

Every profile contains `profile.json` validated against `schema/profile.schema.json`. Schema version `1.0` requires a stable lowercase-hyphenated `id`, profile `version`, `extends: pse-core`, explicit generator support, capabilities, required metadata, an open-font policy, and a concise description.

## Required regression obligations

A generator-supported profile must have a synthetic fixture, machine QA pass, recipient-proof pass, publication-release/verification pass, installed-runtime build pass, and approved visual baselines. Registry-driven regression discovers all manifests declaring `generator_supported: true`, so a new profile cannot rely on a manually maintained test tuple. Visual drift is a human-review signal rather than an automatic design verdict.

## Contribution checklist

1. Keep the profile neutral; do not imitate or name external publisher styles.
2. Use only openly licensed fonts in framework/demo code.
3. Do not redefine core security, metadata, QA, proof, release, or provenance APIs.
4. Declare capabilities honestly; do not advertise unsupported semantics.
5. Add or update the frozen synthetic fixture.
6. Add visual baselines for title, chapter opening, and representative body page.
7. Run `pse doctor --deep`, profile regression, security regression, and full regression.
8. Document any intentional visual drift and regenerate baselines only after human approval.
