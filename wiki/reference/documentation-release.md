# Documentation release evidence

The public documentation website is generated from the Markdown files in `/wiki`. The generated website is a publication artifact of the documentation process; it is not an additional editable source.

For deployment builds, PSE validates the source, builds the site in strict mode, checks generated HTML metadata and the sitemap against the actual deployment base URL, and produces a SHA-256 file inventory called `documentation-release-evidence.json`. The evidence record binds the generated files to a PSE version and source revision.

This record is intentionally narrow. It does not claim that a deployment is live, and it is not a digital signature, trusted timestamp, notarization, or preservation certificate.

Published documentation paths are tracked against a stable-URL baseline. A previously published path should not disappear silently; path changes require an explicit redirect or migration decision.

PSE does not currently publish a GitHub Wiki mirror. `/wiki` remains canonical, and MkDocs Pages remains the primary rendered documentation product.
