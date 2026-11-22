# Critical Edition demo

**Best for:** source-oriented critical editions.

A more text-critical presentation emphasizing canonical locators, apparatus, editorial notes, and scholarly back matter.

## What to look for

Look for source-oriented locators, the critical apparatus, and editorial back matter without page-number-dependent semantics.

- [Open the finished demo PDF](output/critical-edition-demo.pdf)
- Source project: [`source/`](source/)

To rebuild this example from the repository root:

```text
python scripts/examples/build_profile_demos.py critical-edition
```

To create a new private project with the same profile:

```text
pse new /path/to/private-projects --profile critical-edition
```

The demo uses synthetic content only and includes the standard PSE publication-page attribution.

**Index policy:** recommended and enabled by default for this profile.
