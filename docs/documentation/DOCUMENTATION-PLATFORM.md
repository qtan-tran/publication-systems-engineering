# Documentation Platform Contract

PSE 1.41 treats the MkDocs website as the primary rendered documentation product and `/wiki` as its canonical Markdown source. The native GitHub Wiki, if added later, is a derivative mirror rather than a source of truth.

## Build targets

`mkdocs.yml` is the source configuration for local authoring. Deployment binds an absolute `site_url` into an ephemeral configuration with `scripts/docs/prepare_mkdocs_config.py`. Generated site files and generated deployment configuration are build artifacts and are not committed.

An explicit site URL is required for a public deployment so canonical links and sitemap entries are generated against the actual host. The deployment workflow may use the repository's GitHub Pages URL until a custom documentation domain is configured. Moving to a custom domain therefore does not require rewriting Markdown URLs.

## Stable URL policy

The top-level URL families frozen in 1.40 remain stable: `getting-started`, `how-pse-works`, `profiles`, `book-features`, `workflows`, `quality-release`, `customization`, and `reference`. User-facing URLs must describe concepts rather than implementation versions. Renamed published pages require an explicit redirect decision rather than silent deletion.

## Presentation baseline

MkDocs Material is the rendering layer. The initial PSE documentation treatment is deliberately restrained: the PSE oxblood accent, warm paper-like light background, dark/light mode, structured navigation, and search. This is a documentation baseline, not a marketing landing page.

## Metadata and discoverability

The site has a global description and individual pages may provide YAML metadata. Public deployment must bind the real site URL. Sitemap generation and search are build outputs. SEO copy must remain useful documentation first; internal module names are not substituted for user concepts merely to target keywords.

## Analytics and privacy

No analytics provider is hard-coded in 1.41. Analytics remains an explicit deployment choice so privacy, consent, retention, and jurisdictional requirements can be reviewed before activation.

## Quality gates

Documentation QA checks navigation targets, internal Markdown links, referenced local assets, orphan pages, private-boundary leakage, and deployment configuration behavior. `mkdocs build --strict` is the renderer-level gate when documentation dependencies are installed. Passing these checks does not constitute an accessibility certification.
