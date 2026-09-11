# Choose a profile

You do not need to understand PSE's internal architecture before choosing a starting point. Pick the profile closest to the publication you want to make; you can inspect the finished demo PDF before creating a project.

| If you are making… | Start with |
| --- | --- |
| A general prose book | `basic-book` |
| A novel or reading-oriented prose work | `literary-fiction` |
| A research monograph | `academic-monograph` |
| A scholarly edition with apparatus and indexing | `scholarly-edition` |
| A source-oriented critical edition | `critical-edition` |
| A play | `drama` |
| A parallel bilingual text | `bilingual-edition` |
| A poetry collection | `poetry` |
| A volume with chapter-level contributors | `edited-collection` |

All gallery examples use synthetic content. The profile controls presentation; semantic modules provide reusable meaning-aware structures where the publication type needs them.

## Create your own project

After installing PSE from the checked-out repository:

```text
pse profiles --generator-only
pse new /path/to/private-projects --profile poetry
pse build /path/to/private-projects/<generated-project>
```

Use another profile id from the table as needed. Keep real manuscripts in private storage, not in a public repository.

See [Build the demos](BUILD-THE-DEMOS.md) if you want to reproduce the PDFs shipped in the gallery.
