# Edited collection

The `edited-collection` profile is a neutral baseline for multi-author scholarly books. It presents chapter-level contributor credits while delegating contributor identity and contributor-to-unit roles to the reusable `contributor-metadata` semantic module.

## Semantic boundary

Declare each contributor once with `\PSEDeclareContributor{id}{display name}[affiliation][ORCID]`, then record a relation with `\PSEContribution{contributor-id}{publication-unit-id}{role}` where that contribution applies. The role belongs to the relation rather than permanently to the person, so the same contributor may be an author in one unit and an editor in another.

Affiliation and ORCID are optional. This module deliberately does not perform ORCID/ROR lookups, CRediT mapping, Crossref export, identity reconciliation, or authority control.


## Indexing

The reusable `index` module is **recommended and enabled by default** for edited collections. Add entries with `\PSEIndex{term}` or `\PSEIndexTerm{sort key}{display form}` and print the index with `\PSEPrintIndex`. The index remains module-owned rather than implemented by the edited-collection profile.

A title that genuinely does not need an index can add `"index"` to `deactivate` in `config/semantic-modules.json`. Contributor metadata remains required and cannot be deactivated.
