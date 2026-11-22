# Documentation release engineering

PSE 1.46 treats the documentation website as a generated public artifact while keeping `/wiki` as the only editable canonical documentation source.

## Release path

1. validate `/wiki`, navigation, links, assets, and the public/private boundary;
2. bind the actual deployment base URL into an ephemeral MkDocs configuration;
3. run `mkdocs build --strict`;
4. validate the generated site for HTML output, page titles, canonical links, and sitemap/base-URL consistency;
5. create `documentation-release-evidence.json`, schema `0.1`, containing a SHA-256 inventory of generated-site files and the source revision;
6. upload the generated site to Pages and retain the evidence as a workflow artifact.

The evidence record proves only what it contains. It is not a digital signature, trusted timestamp, notarization, live-deployment verification, or preservation certification.

## Stable URLs

The frozen 1.40 top-level information architecture and `use_directory_urls: true` define the stable URL family. Renames of existing published paths require an explicit redirect/migration decision rather than silent deletion. The canonical host is deployment-bound; it is deliberately not hard-coded into the repository.

## Source and generated artifacts

`/wiki` is canonical source. `site/`, deployment configuration, sitemap, canonical tags, and documentation release evidence are generated artifacts and must not be edited as documentation source.

## GitHub Wiki decision

PSE does **not** enable a GitHub Wiki mirror in 1.46. A mirror would create a second public rendering surface, extra URL maintenance, and a risk that users edit the mirror directly. The MkDocs site already supplies navigation, search, stable URLs, and Pages deployment. If a future use case justifies a mirror, it must be generated one-way from `/wiki`; it must never become an editable source of truth.
