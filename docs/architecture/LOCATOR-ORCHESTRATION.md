# Locator Orchestration

PSE 1.39 coordinates locator systems without introducing another locator engine. Semantic ownership remains with the existing modules.

## Namespace ownership

| Orchestrated namespace | Semantic owner | Identity source |
| --- | --- | --- |
| `canonical` | `canonical-locators` | `\PSELocator` / `\PSELocatorNS` |
| `dramatic-line` | `dramatic-locators` | `\PSEDramaLine` |
| `verse-line` | `verse-structure` | first argument of `\PSEVerseLine` |
| `parallel-alignment` | `parallel-text` | alignment ID declared by `\PSEParallelAlign` |

The orchestration layer does not copy, translate, or renumber those identities.

## Project policy

A locator-oriented project may declare `config/locator-orchestration.json`:

```json
{
  "schema_version": "1.0",
  "primary_namespace": "canonical",
  "secondary_namespaces": [],
  "visible_numbering": "show",
  "stable_id_policy": "required"
}
```

`primary_namespace` establishes the title's principal citation/navigation address system. `secondary_namespaces` may coordinate additional active semantic locator systems. The primary namespace cannot also be secondary.

`visible_numbering` is a presentation policy (`show`, `hide`, `source-defined`, or `profile-default`); it does not change semantic IDs. `stable_id_policy` is currently fixed to `required`.

## Generated TeX bridge

The CLI validates the JSON and generates `build/pse-locator-orchestration.tex`. `pse-core` exposes the resulting policy through `\PSEPrimaryLocatorNamespace`, `\PSESecondaryLocatorNamespaces`, `\PSELocatorVisibilityPolicy`, and `\PSELocatorStableIDPolicy`. These are presentation/integration hooks only.

## QA

`pse check` reports a unified `locator_orchestration` metric with ownership and inventory for configured namespaces. Configuration fails if it names a locator namespace whose owning module is inactive. Stable IDs are checked as machine-safe identifiers. Existing locator-specific QA remains authoritative for completeness, ordering, ranges, alignment validity, and duplicate detection.

## Non-goals

1.39 does not create a universal numbering engine, rewrite source IDs, infer locators from page position, or collapse canonical/dramatic/verse/parallel semantics into one data model.
