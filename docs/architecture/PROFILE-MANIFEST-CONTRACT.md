# Profile Manifest Contract

`profile.json` is the machine-readable boundary between the project generator/runtime and a presentation profile. The JSON Schema at `schema/profile.schema.json` is normative for public profile metadata; runtime validation fails closed when a required field, profile package, or schema version is invalid.

Capabilities describe supported presentation/semantic primitives. They are not marketing labels. `required_metadata` is enforced before the profile enters LuaLaTeX. Profiles may add requirements in later schema versions, but a schema migration must be documented rather than silently changing behavior.

The generator discovers profiles from validated manifests. A source checkout and an installed wheel must expose the same registry.
