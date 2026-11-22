---
title: First Troubleshooting
description: Diagnose common first-run PSE failures without editing generated output or framework internals.
---

# First troubleshooting

Start with the earliest failing layer. Changing several things at once makes diagnosis harder.

## `pse` is not found

The PSE launcher is not available in the current shell. Re-run the installation route you chose, open a new terminal if PATH was changed, and then run:

```text
pse doctor
```

## `pse doctor` reports LuaLaTeX missing

Install or repair a TeX distribution that provides LuaLaTeX. The PSE bootstrap scripts install PSE itself; they do not install TeX.

## `pse doctor --deep` fails

Treat required doctor failures as workstation/runtime problems before debugging the book. Fix the reported Python, LuaLaTeX, TeX-package, font-baseline, temporary-write, or safe-build issue and rerun doctor.

## `pse build .` says the project is invalid

Confirm that your terminal is in the generated project root—the directory containing `book.yml` and `main.tex`. If you edited `book.yml`, check YAML indentation and required values.

## LuaLaTeX fails after a content edit

Undo or isolate the most recent edit. Check braces and command spelling first. Rebuild after a small correction rather than making broad layout changes.

## The PDF builds but looks wrong

Run `pse check . --human`, then inspect the PDF. If the problem is a one-title presentation exception, `config/pse-local.tex` is the intended project-local customization point. Do not patch shared core files to fix one book.

## Resetting generated output

Generated `build/` content is not canonical source. Use the PSE workflow rather than hand-editing generated files. Preserve `book.yml`, `main.tex`, `content/`, `assets/`, and project-owned configuration.

If a minimal synthetic starter fails in the same environment, reproduce the problem with synthetic content before involving a private manuscript.

Next: [Where to go next](next-steps.md).
