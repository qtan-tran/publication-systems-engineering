# Scholarly Edition demo

**Best for:** annotated scholarly editions.

A reusable scholarly foundation with locators, apparatus, multilingual text, bibliography, and index support.

## What to look for

Look for canonical locators, multilingual terms, apparatus, bibliography, and index as separate reusable semantics.

- [Open the finished demo PDF](output/scholarly-edition-demo.pdf)
- Source project: [`source/`](source/)

To rebuild this example from the repository root:

```text
python scripts/examples/build_profile_demos.py scholarly-edition
```

To create a new private project with the same profile:

```text
pse new /path/to/private-projects --profile scholarly-edition
```

The demo uses synthetic content only and includes the standard PSE publication-page attribution.

**Index policy:** recommended and enabled by default for this profile.
