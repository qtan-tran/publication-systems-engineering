# Profile module policy

PSE profiles do not need identical feature sets. A profile expresses a publication type and its presentation defaults; reusable scholarly or structural behavior belongs to semantic modules.

Profile manifest schema `1.1` adds `module_policy`. Each referenced module has two fields:

- `status`: `required`, `recommended`, `optional`, `discouraged`, or `incompatible`;
- `default_enabled`: whether the module is active in a newly generated project unless the project explicitly deactivates it.

## Status semantics

`required` means the profile depends on the module for its core semantic contract. Required modules are always default-enabled and cannot be deactivated by title configuration.

`recommended` means the capability normally belongs to the publication type. It may be default-enabled, but a title may deactivate it when the publication does not need that feature.

`optional` means the capability is legitimate for the profile but should be activated only when the title needs it.

`discouraged` means the capability is technically reusable but outside the normal convention of that profile. It remains an explicit opt-in rather than a hard prohibition.

`incompatible` is reserved for genuine semantic or technical incompatibility. PSE rejects project activation of an incompatible module.

## Project override

Generated projects use `config/semantic-modules.json` schema `1.1`:

```json
{
  "schema_version": "1.1",
  "activate": [],
  "deactivate": [],
  "config": {}
}
```

`activate` adds optional or discouraged modules deliberately. `deactivate` removes default-enabled recommended modules. Required modules cannot be deactivated.

## Index policy

PSE 1.31 establishes the following cross-profile policy for the reusable `index` module:

| Profile | Status | Default |
| --- | --- | --- |
| academic-monograph | recommended | enabled |
| basic-book | recommended | enabled |
| bilingual-edition | recommended | enabled |
| critical-edition | recommended | enabled |
| drama | recommended | enabled |
| edited-collection | recommended | enabled |
| literary-fiction | discouraged | disabled |
| poetry | optional | disabled |
| scholarly-edition | recommended | enabled |

This is an architectural policy, not a claim that every individual title must print an index. For example, a short edited collection can deactivate the recommended index, while a large poetry collection can activate it.

## Ownership rule

A reusable feature does not become profile-owned merely because one profile uses it frequently. Index semantics stay in `modules/index/`; edited-collection presentation stays in `profiles/edited-collection/`. The same principle applies to bibliography, contributor metadata, multilingual text, and future reusable capabilities.
