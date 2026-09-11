---
title: Edit Your Book
description: Replace PSE synthetic starter metadata and manuscript content while preserving semantic structure.
---

# Replace the starter content

For the first round, make only a small edit so that installation problems and manuscript problems remain easy to distinguish.

## Edit metadata

Open `book.yml`. A basic starter looks like:

```yaml
title: My First PSE Book
subtitle: ''
author: Example Author
language: en
publication_year: 2026
profile: basic-book
page:
  width_mm: 126
  height_mm: 198
```

Keep the YAML indentation intact. Do not change the profile name casually after generation; profiles can have different starter structures and semantic requirements.

## Edit manuscript content

Open `content/chapter-01.tex` and replace the synthetic prose. Preserve semantic commands rather than manually imitating their appearance:

```tex
\chapter{First chapter}

This is the first paragraph of my test book.

\section{A first section}

This is another paragraph with a footnote.\footnote{A synthetic test note.}
```

Use commands such as `\chapter`, `\section`, quotations, footnotes, and profile-specific semantic commands to say **what a passage is**. Let the profile decide how that structure looks.

!!! warning "Keep source private"
    Once you move beyond synthetic testing, keep unpublished text and project assets in a private repository or private storage controlled by you or your organization. Do not place manuscripts or recipient proofs in the public PSE repository.

Next: [Build and check the PDF](build-and-check.md).
