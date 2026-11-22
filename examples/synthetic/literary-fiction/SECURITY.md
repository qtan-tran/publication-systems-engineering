# Project Security Notes

- Treat unpublished source and proofs as confidential publishing assets.
- Keep this project in private storage unless the manuscript is intended to be public.
- Generated proofs belong under `build/proofs/`; publication releases belong under `release/`. Both are generated artifacts and are ignored by Git.
- Do not put passwords, API tokens, private keys, or credentials in `book.yml` or source files.
- PSE builds with LuaLaTeX `--no-shell-escape` by default.
- If a proof is shared externally, prefer `pse proof --recipient ...` so the artifact receives a recipient-specific proof ID and provenance manifest.
