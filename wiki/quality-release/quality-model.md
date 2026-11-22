---
title: Quality Model
description: Interpret PSE machine findings without turning automation into a substitute for editorial judgement.
---

# Quality model

Run project QA with:

```text
pse check . --human
```

PSE findings use four severity classes:

| Severity | Meaning | Normal action |
| --- | --- | --- |
| `error` | blocking technical/contract problem | fix before release |
| `warning` | non-blocking technical concern | investigate and resolve or document |
| `review` | machine can identify a condition but not make the publication judgement | human review |
| `info` | recorded status or evidence | retain as context |

A command returning success does not mean “zero defects.” Machine QA is one layer in a larger editorial and production process.

## What machine QA is good at

Depending on the active profile/modules, QA can validate declared metadata, semantic IDs and relations, locator structures, apparatus references, generated-file contracts, compilation results, PDF geometry, and other machine-testable invariants.

## What remains human

Humans remain responsible for matters such as factual accuracy, textual collation, translation quality, scholarly interpretation, bibliographic correctness beyond machine-checkable structure, image suitability, visual balance, reading order as experienced by users, legal permissions, and final publication approval.

Use [Human review](../workflows/human-review.md) as part of the production loop rather than only at the end.
