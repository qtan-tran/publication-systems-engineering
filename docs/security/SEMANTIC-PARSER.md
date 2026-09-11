# Semantic parser security and resource limits

The PSE semantic parser is intentionally not a TeX engine. It scans allow-listed PSE semantic commands without executing source.

Default safeguards are conservative upper bounds rather than publishing limits:

- source file: 8 MiB;
- nested brace depth: 128;
- one semantic argument: 1,000,000 source characters;
- semantic nodes per file: 100,000;
- parser errors per file: 1,000.

Inputs exceeding these bounds fail source QA instead of consuming unbounded parser resources. The limits protect local/CI diagnostics from accidental or malicious pathological source; they do not limit LuaLaTeX itself.

The parser treats percent signs as comments only when they are not escaped by an odd run of preceding backslashes. UTF-8 decoding is strict for semantic QA; invalid UTF-8 is reported as an error with a file-level location.
