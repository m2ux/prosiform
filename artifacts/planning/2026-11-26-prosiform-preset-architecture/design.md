# Proposed Bundler Contract

A future extension design. The fixed control is released pf 0.36.0 at `8cedda4cc06b0486168addc05f057161192a22a6`. A passing control does not claim these proposed fields exist. Each form below is a proposal until its specimen set carries the requester's ruling.

## Specimens

Each feature has a specimen set under `specimens/`: sources written in the proposed form, the expected output, the nearest build the 0.36.0 release accepts and a README naming what the form needs from the bundler. Output the release wrote is retained with its command and diagnostics. A hand-written file says so in its first line. A combined set shows the three features in one run and lists every open design point with its candidate answers.

## Ledger

The explicit `--ledger` option adds one `ledger.toml` to the atomically published bundle-set folder. Its versioned schema records:

- the build and profile identity, and the invocation: the entry reference, each pick and each budget in force;
- source-relative paths and hashes, and selected regions;
- ordered default and named preset contributions, layout groups, substitution keys and targets with lexical origins, and entry-stub roles;
- alternatives and picks, brief selections, dispatch and deferral targets;
- stage capability levels, resolved model names and the hash of each bundle.

A feature-to-field and exclusion table prevents partial schema coverage. Runtime effort, provider and context execution, delivery, obedience and semantic completeness are outside the ledger. The ledger's own bytes are outside the hashes it records.

The serializer projects the existing capture and provenance records; it never reads rendered Markdown. It writes TOML through the `tomli-w` library in a fixed key order. Enabling the ledger preserves authored Markdown bytes. Failure uses the existing complete-or-refused publication owner. A JSON Schema ships beside the corpus's fixture schema, and the corpus holds each fixture's ledger to it.

A check-mode run with the option writes the same ledger to standard output and publishes nothing.

The explicit `--verify` option names a published folder, re-hashes each source and bundle its ledger names and reports each differing path. A set with no ledger is refused.

## Pure Imports

The imports field is a list of mappings with path and preset keys. Path is a source-relative local Markdown source; preset selects one explicitly declared metadata key by the existing complete-name normalization, never a list or wildcard. Unknown targets fail. No body or implicit default is selected. An explicitly declared pure default key can be named; an absent default is not synthesized for import lookup. Imported metadata counts as selected for diagnostics and provenance.

The target carries only levels, subst and recursive pure imports. Brief, level, layout group, choice, choice-group and stub roles make it impure. Imports flatten inside one receiving preset; equal values coalesce while retaining origins, and incompatible values, imported or local, fail with both origins. Existing selected-over-default layering applies after that flattening.

A substitution key retains the source directory that declared it; the substitute retains existing key-relative resolution. Import graph identity is the captured source and the normalized preset name. Cycles, missing or unsafe sources, missing presets and impurity refuse publication. A receiving ordinary preset stays local; the existing entry-map and entry-stub roles keep their reach. Imports add no role and no global context channel.

## Local Exclusive Groups

`choice-group` names a choice alternative's local exclusive axis. Where the field is absent, the alternative belongs to the document's one unnamed group under the same resolver. The existing layout `group` is separate. Preset names remain complete document-local names; group membership creates no global registry and no tag namespace.

Every group affecting selected content or an entry map has one member selected. Ordinary presets remain additive; optional stubs retain their role. A dispatch may leave one relevant group to a pick token with the others explicit, and is refused with a remedy for each group where several are open; no Cartesian pick tree is published. At the entry `--pick` is repeatable, each occurrence naming one member of one open group. Briefs remain independent of unpicked alternatives, and dispatch and deferral carry every fixed and chosen binding.

The public synthetic source uses alpha and beta components and small and large tests. The 0.36.0 release combines a component alternative with an ordinary test preset, and bundles without a test where none is named.

## Preset Listing

The explicit `--presets` option names one document and prints its ordinary presets, its alternatives by choice group with their choice lines, its stubs and its imports with origins. It bundles nothing and writes no folder.

## Contract Revisions And The Design Link

The repository's conformance check reads the contract at the revision the README's design link names, and holds the codes that revision declares to the codes the build lists, in both directions. Each feature's clauses therefore reach the contract in feature order, and the change that admits a form moves the design link to the revision stating it. Verification and listing are each stated in the contract by the work that delivers them.

## Open Design Points

The specimen sets show each point's candidate answers; the scrutiny ruling settles it.

- Whether the ledger records the warnings a build raises.
- Which code a verification mismatch reports.
- Whether a source read only for an import counts toward the file and byte budgets.
- Whether an imported substitution no link names warns in each receiving document.
- How a bundle's derived name orders the members of two groups.
- What a pick naming a member of an already fixed group reports.
- Whether each new refusal takes a new code or an existing one.

## Authored And Runtime Boundaries

Contracts, operations and their governing Rule links remain readable source. Imported metadata carries no rules or hidden policy. Model maps remain string-valued and stage capability declarations retain their meaning; runtime effort and profile capture remain the harness's responsibility. Permissions, secrets, session settings and capacity remain outside presets. Structured execution descriptors and focused reviewer modes are outside implementation scope.
