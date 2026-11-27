# Proposed Bundler Contract

A future extension design. The fixed control is released pf 0.36.0 at `8cedda4cc06b0486168addc05f057161192a22a6`. A passing control does not claim these proposed fields exist. Each form below is a proposal until its specimen set carries the requester's ruling; [decisions.md](decisions.md#scrutiny-rulings-2026-11-27) holds the rulings made.

## Specimens

Each feature has a specimen set under `specimens/`: sources written in the proposed form, the expected output, the nearest build the 0.36.0 release accepts and a README naming what the form needs from the bundler. Output the release wrote is retained with its command and diagnostics. A hand-written file says so in its first line. A combined set shows the three features in one run and lists each design point settled at scrutiny.

## Ledger

The explicit `--ledger` option adds one `ledger.yaml` to the atomically published bundle-set folder. Its versioned schema records:

- the build and profile identity, and the invocation: the entry reference, each pick and each budget in force;
- one row for each authored dispatch and deferral link, naming the source and line that wrote it;
- source-relative paths and hashes, and selected regions;
- ordered default and named preset contributions, layout groups, substitution keys and targets with lexical origins, and entry-stub roles;
- alternatives and picks, brief selections, dispatch and deferral targets;
- stage capability levels, resolved model names and the hash of each bundle.

A feature-to-field and exclusion table prevents partial schema coverage. Runtime effort, provider and context execution, delivery, obedience and semantic completeness are outside the ledger, and so is every warning a build raises: what a warning points at is a field already, a stand-in being a substitution of kind `stand-in`. The ledger's own bytes are outside the hashes it records. Where two declarations state one value, the ledger records every origin, each further one under `also`.

The serializer projects the existing capture and provenance records; it never reads rendered Markdown. It writes YAML through `ruamel-yaml`, the library the build reads frontmatter with, in a fixed key order: each string quoted, a list of scalars on one line, a list of mappings as a block, and each key holding a list of mappings in its plural. The ledger is one YAML 1.2 Core mapping under the rules frontmatter is read by, so it carries no alias, merge key, custom tag or duplicate key. Enabling the ledger preserves authored Markdown bytes. Failure uses the existing complete-or-refused publication owner. A JSON Schema ships beside the corpus's fixture schema, and the corpus holds each fixture's ledger to it.

A check-mode run with the option writes the same ledger to standard output and publishes nothing.

The explicit `--verify` option names a published folder, re-hashes each source and bundle its ledger names and reports each differing path with `E_LEDGER_MISMATCH`. A set with no ledger is refused with `E_LEDGER_NOT_FOUND`. The ledger is held to its schema before any other file is opened; a bundle is named by a file name alone and compared with the folder's own contents in both directions; a source resolves from the working directory under the build's own access rules.

## Pure Imports

The imports field is a list of mappings with path and preset keys. Path is a source-relative local Markdown source; preset selects one explicitly declared metadata key by the existing complete-name normalization, never a list or wildcard. Unknown targets fail. No body or implicit default is selected. An explicitly declared pure default key can be named; an absent default is not synthesized for import lookup. Imported metadata counts as selected for diagnostics and provenance.

The target carries only levels, subst and recursive pure imports. Brief, level, layout group, choice, choice-group and stub roles make it impure. Imports flatten inside one receiving preset; equal values coalesce while retaining every origin, and incompatible values, imported or local, fail with both origins. Existing selected-over-default layering applies after that flattening.

A substitution key retains the source directory that declared it; the substitute retains existing key-relative resolution. Import graph identity is the captured source and the normalized preset name. Cycles, missing or unsafe sources, missing presets and impurity refuse publication. A missing source or preset reports `E_TARGET_NOT_FOUND`, an impure target `E_INVALID_CONVERSION_METADATA`, a conflict `E_INVALID_USAGE` and a cycle the new `E_IMPORT_CYCLE`. A source read only for an import counts toward the file and byte budgets and is rechecked before publication. An imported pair is silent in an importer that does not use it, and warns once where no importer in the run names its key. A receiving ordinary preset stays local; the existing entry-map and entry-stub roles keep their reach. Imports add no role and no global context channel.

## Local Exclusive Groups

`choice-group` names a choice alternative's local exclusive axis. Where the field is absent, the alternative belongs to the document's one unnamed group under the same resolver. The existing layout `group` is separate. Preset names remain complete document-local names; group membership creates no global registry and no tag namespace.

Every group affecting selected content or an entry map has one member selected. Ordinary presets remain additive; optional stubs retain their role. A dispatch may leave one relevant group to a pick token with the others explicit, and is refused with a remedy for each group where several are open; no Cartesian pick tree is published. At the entry `--pick` is repeatable, each occurrence naming one member of one open group; a pick naming a member of a group the title fixes is invalid usage. A deferred link names exactly one alternative of each group, or carries the pick token, which leaves open every group the link names no alternative of; the run bundling it names one pick for each. Briefs remain independent of unpicked alternatives, and dispatch and deferral carry every fixed and chosen binding.

The public synthetic source uses alpha and beta components and small and large tests. The 0.36.0 release combines a component alternative with an ordinary test preset, and bundles without a test where none is named.

## Preset Listing

The explicit `--presets` option names one document and prints its ordinary presets, its alternatives by choice group with their choice lines, its stubs and its imports with origins. The listing is text, laid out as a refusal lists alternatives. It bundles nothing and writes no folder.

## Contract Revisions And The Design Link

The repository's conformance check reads the contract at the revision the README's design link names, and holds the codes that revision declares to the codes the build lists, in both directions. Each feature's clauses therefore reach the contract in feature order, and the change that admits a form moves the design link to the revision stating it. Verification and listing are each stated in the contract by the work that delivers them.

## Naming

A bundle's name joins its effective preset names sorted by Unicode code point, as the 0.36.0 release names it, so two groups need no naming rule.

## Authored And Runtime Boundaries

Contracts, operations and their governing Rule links remain readable source. Imported metadata carries no rules or hidden policy. Model maps remain string-valued and stage capability declarations retain their meaning; runtime effort and profile capture remain the harness's responsibility. Permissions, secrets, session settings and capacity remain outside presets. Structured execution descriptors and focused reviewer modes are outside implementation scope.
