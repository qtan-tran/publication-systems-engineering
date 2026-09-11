---
title: Choose a Book Profile
description: Select the PSE presentation profile closest to the publication you are producing.
---

# Choose a book profile

A **profile** supplies the presentation defaults for a kind of book. Choosing a profile does not lock your content into a proprietary format, but starting with the closest publication type reduces unnecessary customization.

Run:

```text
pse profiles --generator-only
```

PSE currently generates nine profiles:

| Profile | Start here when you are making… |
| --- | --- |
| `basic-book` | a general prose book without specialist scholarly architecture |
| `literary-fiction` | a novel or reading-oriented prose work |
| `academic-monograph` | a research monograph |
| `scholarly-edition` | an annotated scholarly edition |
| `critical-edition` | a source-oriented critical edition |
| `drama` | a play or dramatic text |
| `bilingual-edition` | a parallel bilingual publication |
| `poetry` | a poetry collection |
| `edited-collection` | a multi-author edited volume |

For your first test, `basic-book` is the simplest general choice. If you already know the real publication type, use that profile so your synthetic test exercises the relevant starter.

!!! note
    Profiles own presentation. Reusable semantic features—such as an index, apparatus, verse structure, contributor metadata, or parallel text—are separate capabilities. You do not need to configure those manually for the first build; generated projects start with the profile's supported defaults.

Next: [Create your first project](create-a-project.md).
