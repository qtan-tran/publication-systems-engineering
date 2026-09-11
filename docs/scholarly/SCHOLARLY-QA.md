# Scholarly QA gates

For scholarly profiles such as `scholarly-edition` and `critical-edition`, ordinary PDF QA is supplemented by source-level semantic checks. Locator-scheme violations are errors when a strict scheme is declared. Bibliography and index tool failures remain build errors. Missing required scholarly dependencies are surfaced by `pse doctor --profile <profile-id>`.

Machine QA does not replace textual collation, apparatus review, bibliographic fact-checking, index editing, or visual proofreading.
