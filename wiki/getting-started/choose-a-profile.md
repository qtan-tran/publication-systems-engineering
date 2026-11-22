# Choose a profile

Start with the six [supported book profiles](../profiles/index.md): `academic-monograph`, `bilingual-edition`, `critical-edition`, `drama`, `edited-collection` and `literary-fiction`.

Use `academic-monograph` for general nonfiction, `critical-edition` for edited or annotated source texts (without implying textual criticism in every instance), and `literary-fiction` for narrative prose. Poetry-specific semantic markup remains available but there is no general-purpose poetry presentation profile.

```sh
pse profiles --generator-only
pse new /path/to/projects --profile academic-monograph
```

