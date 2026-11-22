# Regression Orchestration

`pse regression` is the framework-maintainer orchestration command. In current release it is intended for a source checkout because the minimal installed runtime does not ship the whole development test corpus.

## Full suite

Runs the accumulated core security, generator, runtime, typography, and QA regression scripts plus visual comparison for every generator-supported profile that has a registered synthetic fixture and baseline manifest.

## Quick suite

`pse regression --quick` runs smoke, typography and QA self-tests plus visual comparison. It is suitable for routine shared-style work before a full CI run.

## Aggregate report

The command writes a single JSON report containing script results, visual findings and CI-oriented exit policy. Visual `review` findings do not fail the command during alpha.
