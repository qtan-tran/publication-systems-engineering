---
title: Understand the Project Folder
description: Learn which generated PSE project files are source, configuration, assets, and disposable build output.
---

# Understand the project folder

A generated `basic-book` starter has this shape:

```text
my-first-pse-book/
├── book.yml
├── main.tex
├── content/
│   └── chapter-01.tex
├── assets/
├── config/
│   ├── pse-local.tex
│   └── semantic-modules.json
├── tests/
├── README.md
├── SECURITY.md
└── .gitignore
```

After a build, PSE creates `build/`. **Do not edit files in `build/` as source.** They are generated and can be recreated.

The files you normally touch first are:

- `book.yml` — title-level metadata such as title, author/editor, language, year, profile, and page size;
- `content/` — manuscript source;
- `main.tex` — the book assembly order; beginners usually need little or no change here for the first test;
- `assets/` — project-owned images and other assets;
- `config/pse-local.tex` — restrained title-local presentation exceptions;
- `config/semantic-modules.json` — semantic feature activation; leave it alone until you know you need a change.

Do not edit the shared PSE core or an installed profile to make a one-book exception. A title-local exception belongs in the project.

Next: [Replace the starter content](edit-your-book.md).
