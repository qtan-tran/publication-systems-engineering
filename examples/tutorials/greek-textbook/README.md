# Ancient Greek for Beginners

This is a Publication Systems Engineering project generated with the `academic-monograph` profile.

## Source of truth

The canonical project sources are `book.yml`, `main.tex`, `content/`, `assets/`, and project-owned configuration. The `build/` directory is generated and must not be edited as source.

## Environment preflight

After installing or updating PSE, run `pse doctor`. Use `pse doctor --deep` when diagnosing a workstation or secure-build environment. Normal installed use does not require `PSE_ROOT` or manual `PYTHONPATH`.

## Standard workflow

```text
pse build .
pse check .
pse proof . --recipient "Recipient Name"
pse release .
pse verify-release release/<release-id>
pse clean .
```

Do not run LuaLaTeX with shell escape. PSE invokes LuaLaTeX with `--no-shell-escape` by default.

## Security boundary

Keep unpublished manuscripts and project assets in a private repository or private storage controlled by your organization. Do not commit generated recipient proofs. Watermarked proof PDFs support deterrence and traceability; they are not unremovable DRM.

## Profile status

`academic-monograph` is a generator-supported profile. Use `config/pse-local.tex` for restrained title-local exceptions rather than editing the shared core or profile package.

## About this demo

This synthetic demo textbook was produced with the `pse new` generator and lightly edited by hand, exactly the way a real project starts.

- Five chapters live in `content/chapter-01.tex` … `content/chapter-05.tex`; they are wired into `main.tex` with one `\input` line per chapter.
- The polytonic Greek samples use the `multilingual` semantic module: it is activated once in `config/semantic-modules.json`, and every Greek run of text is wrapped in `\PSEGreek{…}` so it is set in a font with full polytonic support (Gentium Plus).
- The three illustrations are public-domain works from Wikimedia Commons: the Parthenon from the west, the British Museum bust of Homer (1825), and a sixth-century Greek cursive manuscript. The repository does not redistribute the image files; fetch them into `assets/` with the commands in the next section. The book carries an Image Credits page in the back matter.

## Fetch the illustrations

From the project root:

```text
curl -sL -o assets/parthenon-west.jpg "https://commons.wikimedia.org/wiki/Special:FilePath/Parthenon_from_west.jpg"
curl -sL -o assets/homer-bm-1825.jpg "https://commons.wikimedia.org/wiki/Special:FilePath/Bust%20Homer%20BM%201825.jpg"
curl -sL -o assets/greek-manuscript-6c.png "https://commons.wikimedia.org/wiki/Special:FilePath/Greek%20manuscript%20cursive%206th%20century.png"
```

Any other public-domain image works the same way; keep the credits accurate for whatever you use.
