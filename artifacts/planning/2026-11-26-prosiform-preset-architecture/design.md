# Proposed Compiler Contract

This is a future extension design. The fixed control is released pf0.34.0 at191c0cf8d2a8fa39b17f674b579daee413c0e655; current upstream main is794922d41465b91deb4edb3a7484506cb8f519cd. A passing control does not claim these proposed fields already exist.

## Effective Manifest

The explicit --manifest option adds one build-manifest.json to the atomically published bundle-set folder. Check mode checks the same projection but publishes nothing. Its versioned schema records compiler/profile identity, source-relative paths/hashes, selected regions, ordered default/named preset contributions, layout groups, substitution keys/targets and lexical origins, entry-stub roles, alternatives and picks, brief selections, dispatch/deferral targets, stage capability levels, resolved model names and output hashes. A feature-to-field/exclusion table prevents partial schema coverage. Runtime effort, actual provider/context execution, delivery, obedience and semantic completeness are not compiler facts.

The serializer projects existing capture/provenance records without parsing rendered Markdown. Enabling the sidecar preserves authored Markdown bytes. Failure uses the existing complete-or-refused publication owner.

## Pure Imports

The imports field is a list of mappings with path and preset keys. Path is a source-relative local Markdown source; preset selects one explicitly declared metadata key using existing complete-name normalization, not a list or wildcard. Unknown targets fail. No body or implicit default is selected. An explicitly declared pure default key can be named explicitly; an absent default is not synthesized for import lookup. Imported metadata is counted selected for diagnostics/provenance.

The target carries only levels, subst and recursive pure imports. Brief, level, layout group, choice, choice-group and stub roles make it impure. Imports flatten inside one receiving preset; equal values coalesce while retaining origins, and incompatible imported/imported or imported/receiving-local values fail with both origins. Existing selected-over-default layering applies after that flattening and is not replaced by inheritance.

A substitution key retains the source directory that declared it; the substitute retains existing key-relative resolution. Import graph identity is captured source plus normalized preset name. Cycles, missing/unsafe sources, missing presets and impurity refuse publication. A receiving ordinary preset stays local; the existing explicit entry-map and entry-stub roles keep their existing reach. Imports add no new role or global context channel.

## Local Exclusive Groups

choice-group names a choice alternative's local exclusive axis. Without the field, alternatives belong to the document's one unnamed group under the same resolver. The existing layout group is separate. Preset names remain complete document-local names; group membership creates no global registry or new tag namespace.

Every group affecting selected content or an entry map has one member selected. Ordinary presets remain additive; optional stubs retain their current role. Explicit component/test combinations are valid. One relevant unresolved group may be left to a pick token with other groups explicit. Several unresolved groups refuse with grouped remedies; the feature creates no Cartesian pick tree. Briefs remain independent of unpicked alternatives, and dispatch/deferral carries every fixed and chosen binding.

The public synthetic source uses alpha/beta components and small/large tests. Current0.34 can combine a component alternative with an ordinary test preset but does not express the missing test as an exclusive-axis failure. The future group specimen states both axes, rather than inferring a need from unrelated reviewer misses.

## Authored And Runtime Boundaries

Contracts, operations and their governing Rule links remain readable source. Imported metadata carries no rules or hidden policy. There is no inline-brief change. Model maps remain string-valued and stage capability declarations retain their current meaning; runtime effort/profile capture remains the harness's responsibility. Permissions, secrets, fork/session settings and capacity remain outside presets. Structured execution descriptors and focused reviewer modes are not implementation scope.
