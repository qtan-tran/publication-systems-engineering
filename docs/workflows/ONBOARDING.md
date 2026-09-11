# Onboarding: from installation to verified release

This is the shortest supported path for an editor or layout professional who is new to PSE.

## 1. Install the framework

Use Python 3.11+ in an environment controlled by your organization:

```text
python -m pip install .
```

Then run:

```text
pse doctor --deep
```

Do not continue with confidential manuscript work until required checks pass.

## 2. Create a private project

```text
pse new /path/to/private-projects
```

Choose a supported profile. Generated projects are meant to live outside the public framework repository, ideally in private version-controlled storage.

## 3. Edit canonical source

Edit:

- `book.yml` for metadata;
- `content/` for canonical manuscript source;
- `config/` for title configuration;
- `config/pse-local.tex` only for sanctioned title-local presentation overrides.

Do not hand-edit files under `build/` or `release/`.

## 4. Build and check

```text
pse build .
pse check . --human
```

Fix `error` findings. Review `warning` and `review` findings rather than treating every warning as automatically fatal.

## 5. Share a proof

```text
pse proof . --recipient "Recipient Name" --email recipient@example.org
```

The proof is recipient-specific and includes provenance/checksum data. Watermarking is deterrence and traceability, not unremovable DRM.

## 6. Create a release

```text
pse release .
```

If only acknowledged `review` findings remain:

```text
pse release . --acknowledge-review
```

Then verify:

```text
pse verify-release release/<release-id>
```

The release directory, not `build/book.pdf`, is the publication artifact boundary.

## 7. Keep the project private

Never submit unpublished manuscripts, recipient proofs, credentials, or commercial contract information to public PSE issues.
