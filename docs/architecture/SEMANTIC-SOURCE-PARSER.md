# Semantic Source Parser and Intermediate Representation

PSE 1.7 introduces a small non-executing parser for PSE's public semantic TeX commands. Its purpose is quality assurance, not TeX replacement.

## Trust boundary

The parser never executes TeX, expands macros, reads arbitrary files, invokes shell commands, or attempts to interpret general TeX. It recognizes only allow-listed PSE semantic commands and the `PSESpeech` environment. LuaLaTeX remains the production engine.

## Why this exists

Earlier alpha QA used regular-expression scanners. Those scanners were adequate for synthetic fixtures but could not safely represent nested braced content, multiline arguments, comments, or reliable source locations. The parser uses balanced-brace reading and emits a source-located intermediate representation (IR).

## IR contract

Each node records:

- node kind (`command` or `environment_begin`);
- public PSE semantic command/environment name;
- unexpanded argument strings;
- source file;
- 1-based line and column;
- byte/character offset in the decoded source text.

Run:

```text
pse semantic-ir <project>
pse semantic-ir <project> --output semantic-ir.json
```

The JSON output is diagnostic and machine-readable. It is not a canonical manuscript format and must not be edited as a substitute for `.tex` source.

## Parsing limits

PSE deliberately does not implement TeX expansion. Semantic IDs used by machine QA therefore need to appear as literal braced arguments to the public PSE semantic API. User-defined macros that synthesize semantic IDs are outside the machine-audited contract.

Malformed recognized commands produce an `error` finding with source location. Unknown TeX commands are ignored by this parser and remain LuaLaTeX's responsibility.

## Migration policy

During the alpha series, semantic QA migrates family-by-family from regex scanning to the IR. The public semantic TeX API remains stable; parser changes must not require title source rewrites unless accompanied by an explicit migration note.
