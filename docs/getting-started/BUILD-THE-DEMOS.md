# Build the profile demos

The committed PDFs under `examples/profiles/*/output/` are canonical showcase artefacts built from synthetic sources. They are intentionally versioned so non-technical visitors can inspect a feasible result without installing PSE first.

Prerequisite: install PSE from the checked-out repository and confirm `pse doctor --deep` passes. LuaLaTeX must be available on the machine.

From the repository root, build every demo with:

```text
python scripts/examples/build_profile_demos.py
```

Build only selected profiles with:

```text
python scripts/examples/build_profile_demos.py poetry critical-edition
```

The script calls the normal PSE build path, copies each finished PDF to the corresponding `output/` directory, and removes transient TeX build files from the demo source tree. The standard `\PSEPublicationPage` is retained in every demo so the mandatory PSE attribution banner is part of the publication output.

These examples are for evaluation and learning. `tests/fixtures/` remains the regression-oriented synthetic test surface; `examples/profiles/` is the human-facing demonstration surface.

## Expected result

A successful build leaves one canonical PDF at:

```text
examples/profiles/<profile>/output/<profile>-demo.pdf
```

Transient TeX build directories are removed by the demo builder. If a demo command fails, fix the build or environment rather than manually replacing the canonical PDF.
