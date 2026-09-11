# Book Profile Handbook

A **profile** is PSE's publication-type presentation baseline. It chooses an appropriate page character and declares which reusable semantic modules are required, recommended, optional, or discouraged. A profile does **not** own reusable semantics that belong to modules.

Choose the profile whose *editorial structure* matches the book, not the one whose demo happens to look closest. You can customize typography and page presentation later without changing the manuscript's semantic identity.

| Profile | Start here when your book is primarily... | Defining structure |
| --- | --- | --- |
| [Academic Monograph](academic-monograph.md) | a sustained scholarly argument | prose hierarchy |
| [Basic Book](basic-book.md) | general prose without specialist semantics | conventional chapters |
| [Bilingual Edition](bilingual-edition.md) | aligned source and target text | parallel-text relations |
| [Critical Edition](critical-edition.md) | an edited source text with apparatus | canonical locators + apparatus |
| [Drama](drama.md) | a play or dramatic text | speakers, stage directions, dramatic locators |
| [Edited Collection](edited-collection.md) | a multi-author volume | publication units + contributor relations |
| [Literary Fiction](literary-fiction.md) | reading-oriented narrative prose | narrative flow |
| [Poetry](poetry.md) | verse organized by stanzas/lines | stable verse-line identity |
| [Scholarly Edition](scholarly-edition.md) | an annotated edition | locators + apparatus + scholarly matter |

## Two choices that are often confused

**Academic Monograph vs Scholarly Edition:** choose the monograph when the argument and chapter hierarchy are primary. Choose the scholarly edition when an edited/annotated text and stable source locators are primary.

**Critical Edition vs Scholarly Edition:** both support edition infrastructure. `critical-edition` puts source-critical work and textual apparatus at the center; `scholarly-edition` is the broader annotated-edition baseline.

**Basic Book vs Literary Fiction:** both are intentionally lighter than scholarly profiles. `basic-book` retains a conventional structured-book baseline; `literary-fiction` keeps narrative reading rhythm primary and discourages most scholarly furniture.

## Profile policy is not a feature checklist

PSE uses five module-policy states: `required`, `recommended`, `optional`, `discouraged`, and `incompatible`. The starter activates required modules and any modules explicitly configured as default-on. A capability can be technically available without belonging in every book.

To inspect the machine-readable profile contracts installed with your PSE version, run:

```text
pse profiles --generator-only
pse profiles --presentation
```

To create a project after choosing a profile:

```text
pse new /path/to/private-projects --profile PROFILE-ID
```

If this is your first PSE project, read [Choose a Book Profile](../getting-started/choose-a-profile.md) and [Create Your First Project](../getting-started/create-a-project.md) before making local customizations.
