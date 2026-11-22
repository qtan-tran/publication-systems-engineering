# Bilingual Edition demo

**Best for:** parallel bilingual publications.

A parallel-text presentation for source and target language segments with translation-note support.

## What to look for

Look for source/target segments whose alignment remains semantic rather than dependent on a particular page position.

- [Open the finished demo PDF](output/bilingual-edition-demo.pdf)
- Source project: [`source/`](source/)

To rebuild this example from the repository root:

```text
python scripts/examples/build_profile_demos.py bilingual-edition
```

To create a new private project with the same profile:

```text
pse new /path/to/private-projects --profile bilingual-edition
```

The demo uses synthetic content only and includes the standard PSE publication-page attribution.

**Index policy:** recommended and enabled by default for this profile.
