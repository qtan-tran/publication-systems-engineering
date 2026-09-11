---
title: Build and Check Your PDF
description: Produce a working PDF and run PSE machine checks before making proofs or releases.
---

# Build and check your PDF

From the project root, run:

```text
pse build .
pse check . --human
```

A successful build writes the working PDF to:

```text
build/book.pdf
```

Open that PDF and inspect it visually. Machine checks cannot decide every editorial or typographic question.

## Read the check result

PSE uses four finding levels:

| Level | Meaning |
| --- | --- |
| `error` | blocking problem |
| `warning` | technical warning that needs attention |
| `review` | human editorial/production judgement required |
| `info` | recorded status or evidence |

Do not interpret “the PDF opened” as “the book is ready to publish.” A working build is an iteration artifact.

## A useful first loop

Use this short cycle while editing:

```text
edit source → pse build . → pse check . --human → inspect build/book.pdf
```

When a command fails, do not edit generated files in `build/` to hide the symptom. Fix the source or project configuration that produced it.

Next: [First troubleshooting](troubleshooting.md), or, if everything works, [Where to go next](next-steps.md).
