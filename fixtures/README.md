# Fixtures

The language-neutral corpus and the contract it encodes.

A fixture declares a source tree, an invocation and an expected result, so it binds any implementation of prosiform rather than describing one. Nothing here is written in the language of a build: a fixture names no language, no package and no module, so the corpus binds the build that runs it rather than describing how it is written.

## The families

A family is a directory of fixtures sharing a subject. The design clauses each fixture encodes are its own `clauses`, so a family groups fixtures for a reader and states no clause.

| Family | Its fixtures exercise |
| --- | --- |
| `absorbed-title/` | A reference naming a title a file heading absorbs. |
| `ancestor-promotion/` | A heading-only ancestor promoted to a selection, and the dependencies it reaches. |
| `boundary/` | Block boundaries between bundled content: lists, code and YAML examples, file groups. |
| `candidate-validation/` | Candidate validation of the compiled bundle against the post-compilation invariants. |
| `citation/` | A link above the working directory cited as text. |
| `cli/` | The command-line grammar, its options, budgets, exit statuses and JSON diagnostics. |
| `composition/` | [Section composition](../docs/composition.md): directive labels, scopes, contributions, deferral, cycles and refusals. |
| `confinement/` | Path forms, symbolic links and unreadable paths a reference inside a source names. |
| `consolidation/` | Two selections of one document consolidated into one. |
| `deferral/` | The deferral mark: what a deferred link contributes and how it is published. |
| `depth-overflow/` | A heading the hierarchy places at or past H6. |
| `destinations/` | The destination each bundled heading takes. |
| `determinism/` | Bundle order independent of entry and discovery order. |
| `diagnostics/` | Diagnostic chains, JSON lines and a run that fails in itself. |
| `dispatch/` | Dispatched selection variants, equivalent requests, inline/parallel links, chains, depth and cycles. |
| `extraction/` | Section extraction: the headings a fragment names and where its section ends. |
| `file-wide-safety/` | A safety limit crossed in content no selection reaches. |
| `frontmatter/` | Frontmatter delimiters, YAML and the `prosiform` mapping. |
| `grouping/` | Groups, merged sections, member subsections and the presets that place them. |
| `headings/` | Source-heading slugs and generated headings beside authored ones. |
| `hierarchy/` | The file-scoped hierarchy: titles, preambles and Setext conversion. |
| `identity/` | The heading a document's path or title gives its file group. |
| `inclusion/` | Declared targets, presets and `subst` pairs as a reference reaches them. |
| `limits/` | Each resource budget at the boundary it fails on. |
| `literal-bracket/` | Bracketed text no definition resolves, kept as written. |
| `mock/` | A `subst` pair redirecting a reference, and its warnings. |
| `normalization/` | The resolution sequence for a reference's spelling. |
| `ownership/` | Self and ancestor references after consolidation. |
| `parallel-dispatch/` | The parallel dispatch mark and its dispatch-set sub-section. |
| `parser-limit/` | Parser viability gates: a reference lookup the parser suppresses or declines. |
| `profile/` | The Markdown profile: suffixes, encoding, HTML and unsupported constructs. |
| `prosiform/` | The run-pf line every bundle opens with, and the protocol paragraphs no bundle carries. |
| `publication/` | Publication of a run's folder, and what a failing or check run leaves. |
| `real-source/` | Documents copied from this workspace's skills, described under [Copied sources](#copied-sources). |
| `reference/` | Links, definitions and diagram clicks a source writes. |
| `resource/` | A link naming a resource rather than a document. |
| `rewriting/` | Destinations rewritten to the bundle's own anchors, diagram links among them. |
| `self-reference/` | A link to its own section, file or an including ancestor. |
| `source-consistency/` | A source that changes during compilation. |
| `structural-ancestors/` | Heading-only structural ancestors above a selection. |
| `traversal/` | Which references are followed as dependencies, cycles among them. |
| `validation-scope/` | A defect outside the selection, and the run that later includes it. |

## A fixture

A fixture is a directory holding `manifest.toml`. Discovery walks this tree and takes every directory that carries one, so a family is a directory and a fixture's identity is its path under `fixtures/`.

```text
fixtures/
├── manifest.schema.json
└── normalization/
    └── a-reference-above-the-working-directory-is-text/
        ├── manifest.toml
        ├── source/
        │   └── guide.md
        └── expected/
            └── guide.bundle.md
```

`source/` is the tree the run is confined to. `expected/` holds each bundle the run must write, under the name the run gives it. They are separate because an expected bundle is itself Markdown, which a run over `source/` must not read as one of its sources.

## A symbolic link in a source tree

A source tree carries a symbolic link where the clause under test is about one. Git records a link as its own object — mode `120000`, the target as its content — so a fixture declaring the no-symlink source policy declares it as a link rather than as a file holding a path, and a runner materialises the tree the manifest describes.

A link inside a source tree targets a path inside the fixture, written relative to the link, so the fixture is self-contained wherever the repository is checked out. A target outside the source tree sits beside it under the fixture's own directory, which is how a link that resolves out of the working directory is declared without naming anything of the host. No link leaves its fixture.

A checkout whose filesystem or configuration cannot create a link writes the target path into a regular file instead. Such a tree no longer states what the fixture declares, and the fixture fails rather than passing against a file that looks like a document.

## Copied sources

Most families write their sources for the clause they exercise. The `real-source/` family does not: each of its sources is a document copied byte for byte from one of this workspace's skills, at the path that skill gives it. A source written to exercise one clause exercises that clause and says nothing about the documents the tool exists to bundle, so this family is where the corpus meets prose nobody wrote for it.

A copied source is not edited beyond its declaration. A document is compiled when its leading frontmatter declares `prosiform`, and an upstream document declares nothing, so each copy's leading frontmatter opens with `prosiform: {}`, in a frontmatter block of its own where the original carries none. That declaration is what a run reads, and the one thing the copy adds. Any other edit a document needs to bundle is a defect in the build or a gap in the design, and the record of that is a finding rather than a changed document. The documents live upstream and a copy carries no authority to change them; each is held to its original, its declaration removed, with `cmp` and `sha256sum`, outside the corpus, because the original is in another repository.

A document joins the family when its closure is itself: no local Markdown document reference, and fragment-only references only where the destination the bundle generates is the fragment the source already spells. Such a document bundles to the same bytes under a build that traverses references and one that has nothing to traverse, so its expected bundle states the contract rather than a stage of the work.

## The manifest

The manifest is the whole declaration. A runner reads it and the fixture's files, and decides pass or fail from them alone.

```toml
description = "A deferred link naming a document that declares nothing is refused."

clauses = [
  "Link classification and resource handling — An operator's target",
]

[invocation]
cwd = "source"
arguments = ["guide.md"]

[expected]
exit_status = 1

[[expected.diagnostics]]
severity = "error"
code = "E_UNSUPPORTED_CONSTRUCT"
reference = "../guidelines.md"
source = "guide.md:6"
chain = ["guide.md", "../guidelines.md"]
```

| Field | Declares |
| --- | --- |
| `description` | What the fixture establishes. |
| `clauses` | The design clauses it encodes, named as [The clause form](#the-clause-form) states, so every clause maps to the fixtures that cover it. |
| `invocation.cwd` | Optional existing fixture-relative working directory; absent means the fixture directory. It resolves explicit entry references and the paths diagnostics name. |
| `invocation.arguments` | The arguments of the invocation, in order. None declares the bare command. |
| `expected.exit_status` | The process exit status: one of the five categories the contract declares. |
| `expected.bundles` | Optional. The fixture-relative files under `expected/` holding the bytes of each bundle the run writes into its folder, each named as the run names the bundle. A run writing no bundle declares none. |
| `expected.stdout_contains` | Optional. The text standard output must carry, where the whole of the response is a build's own. Standard output carries no bundle, so a fixture declaring none declares an empty stream. |
| `expected.diagnostics` | The diagnostics standard error must carry, in order, each with a severity and a code drawn from the catalogue that severity selects, and optionally the `message_contains`, `reference`, `resolved`, `source`, `chain` and `location` a diagnostic carries. `location` is the source coordinate a diagnostic standing at a link names: a fixture-relative `file`, and a one-based `line` and `column`. A run emitting none declares an empty list. |
| `awaiting` | Optional. The work that delivers the behaviour the fixture declares, written as an initiative and an epic and optionally the task within it, such as `I00:E03`. A fixture carrying it declares behaviour the build does not yet meet. |
| `fault` | Optional. The fault the run performs on itself, `source-changed`, `internal`, `cleanup-refused`, or `unrecognized` for a fault the contract does not name, which the runner asks the build for by the means the contract declares. A fixture declaring none declares a run that meets no fault. |

The runner uses the working directory the manifest names and asks for diagnostics as data, so neither is written in `arguments`: a code is compared as a value rather than as prose, which is what makes the comparison the same in every language. The runner names no output folder, so a run writes its folder of bundles where its own arguments send it: the working directory, or the folder an `-o` among them names.

## The clause form

A clause is a heading of the [design](https://github.com/m2ux/prosiform/blob/96eb2b0f4/artifacts/planning/2026-10-17-prosiform-v1/design.md), or an enumerated rule under one: a bold-led bullet, a step of a numbered sequence, or a row of a table. A heading names the rule its own prose states, and a rule under it is named by both, separated by an em dash:

```toml
clauses = [
  "Heading-only structural ancestors — Depth",
  "CLI contract, a command line the grammar does not admit",
  "Adversarial acceptance fixtures — Partial outlines, original skipped heading levels",
]
```

The clause is the text up to the comma and the case this fixture takes of it follows, so two fixtures taking different cases of one clause both map to it. `make conformance` reads the design and these declarations and reports the mapping between them, so a declaration naming no clause the design states fails rather than landing nowhere.

The declaration sits in the manifest beside the expectation it qualifies, for the reason the deferral marker does: a mapping held anywhere else drifts from the fixtures it names in both directions.

## The adversarial families

The design lists the families of hard cases a build meets, and a family is a clause like any other, so a fixture encoding one names it among its `clauses` and one reading of the corpus answers which families are represented and by what.

Every family the design lists is named by at least one fixture. Consistency, a source changing while the run reads it, is reached through the `source-changed` [fault](#a-fault-the-run-performs-on-itself); parser exhaustion, a parser resource limit suppressing a reference lookup, through the `parser-limit/` family.

A published bundle is expected as a file rather than as text inside the manifest because the preservation invariant turns on bytes — newline spelling and the trailing newline among them — and because a bundle is read and reviewed as the Markdown it is.

A run's working directory is the fixture's own, so the folder a run writes its bundles into — its entry's name with the `.bundles` suffix — lands among the fixture's files. Every file the run creates under the fixture or its working directory is the run's output: it is compared by its name within the run's folder with the bundles the manifest declares and removed with that folder, so a run writing a file no bundle names fails, as does one writing a file outside a folder of its own or into a folder named for no declared bundle, and a validation-only run declares no bundle at all:

```toml
[invocation]
cwd = "source"
arguments = ["-c", "-o", "..", "guide.md"]

[expected]
exit_status = 0
diagnostics = []
```

## Declarations

A source declares `prosiform` in its leading frontmatter, and a link is compiled when its target declares and is text when it does not, wherever the target sits. An empty mapping declares, a document carrying none declares nothing, and a mapping carrying `root` fails with E_INVALID_CONVERSION_METADATA. The invocation working directory must exist and resolves explicit entry references and the paths diagnostics name. A parent-directory entry is authorized by bounded no-follow bootstrap capture.

## Text an output carries

Some of what a run writes is the build's own. A version string is the clearest case, and a diagnostic's wording is the same case in a smaller place. A fixture declaring either of them whole would bind the corpus to one implementation, so it declares the text the output must carry instead: a list whose entries are substrings the output contains.

```toml
[invocation]
cwd = "source"
arguments = ["-v"]

[expected]
exit_status = 0
stdout_contains = ["prosiform ", "(prosiform-markdown)"]
diagnostics = []
```

The response reports the tool and the profile identifier, and the version between them belongs to the build. Standard output carries no bundle, so a fixture declaring no `stdout_contains` declares an empty stream, and no run goes uncompared.

A diagnostic declares the same thing about its message, which is how two faults sharing one error code are told apart:

```toml
[[expected.diagnostics]]
severity = "error"
code = "E_INVALID_USAGE"
message_contains = ["#stop", "document#fragment"]
```

`E_INVALID_USAGE` names every command line the grammar does not admit, and the contract has the message say which fault it was. A fixture names the run's own data the message must carry — the reference refused, the option whose value was outside its set, the run folder that held an input source — so a build reporting another fault under that code fails the fixture while each build keeps its own phrasing. The field is optional, and a diagnostic declaring none states nothing about its message.

The following fixtures illustrate invalid usage. The single-entry grammar also refuses two entry references, repeated `--presets`, presets without an entry, and complete Markdown-link expressions as entries. What the corpus covers under one code is read from the manifests rather than assumed from the code:

| Fault | Fixture |
| --- | --- |
| Arguments naming no entry reference | [`cli/a-command-line-naming-no-entry-reference`](cli/a-command-line-naming-no-entry-reference/manifest.toml) |
| An option the contract does not declare | [`cli/an-option-the-contract-does-not-declare`](cli/an-option-the-contract-does-not-declare/manifest.toml) |
| An option value outside the set its row names | [`cli/diagnostics-format-unknown`](cli/diagnostics-format-unknown/manifest.toml) |
| An entry reference naming a fragment alone | [`cli/a-bare-fragment-is-invalid-usage`](cli/a-bare-fragment-is-invalid-usage/manifest.toml) |
| A run folder holding an input source | [`cli/run-folder-holding-a-dependency-source`](cli/run-folder-holding-a-dependency-source/manifest.toml) |
| Standard output named as the output folder | [`cli/standard-output-named-as-the-output-folder`](cli/standard-output-named-as-the-output-folder/manifest.toml) |
| A conformance fault outside the three the contract names | [`cli/an-unknown-fault-is-invalid-usage`](cli/an-unknown-fault-is-invalid-usage/manifest.toml) |

An entry reference whose own spelling the grammar does not admit — a query, an encoded separator, an over-long escape, an escape decoding to no UTF-8 — carries the same code, and the `normalization/` family states it where the clause under test is the resolution sequence rather than the command line's shape.

## A fixture awaiting its work

The corpus states the contract in full, so a fixture may declare behaviour the build does not yet produce. Such a fixture names the work that delivers it:

```toml
awaiting = "I00:E03"
```

A fixture carrying `awaiting` and failing is reported as awaiting that work, and the corpus run stays green: an expectation the contract makes and the build does not meet is a declared gap rather than a defect. A fixture carrying it and meeting its manifest fails the run, naming the manifest to lift the marker from, so the marker is temporary by construction — the change that delivers the work is the change that fails until the marker goes.

The marker lives in the manifest because the expectation is the fixture's own. A list of excepted fixtures held in a command or a job definition drifts from the corpus in both directions: a fixture renamed or deleted leaves a line behind, and a reader of the fixture sees nothing. Naming the work rather than setting a flag tells the session delivering that work which fixtures to revisit.

## A fault the run performs on itself

Three of the outcomes the contract declares are facts about the run rather than about any document it reads: a source that changes during compilation, a run that fails in itself, and an earlier set the run cannot remove once its own stands. A fixture declares a source tree, an invocation and a result, so none arises from that declaration. The contract's [Conformance faults](https://github.com/m2ux/prosiform/blob/96eb2b0f4/artifacts/planning/2026-10-17-prosiform-v1/design.md#conformance-faults) section declares how a conformance run asks the build to perform one, and the runner is what asks, so a fixture names the fault and no means of reaching it. A manifest names the fault its run meets:

```toml
fault = "source-changed"

[invocation]
cwd = "source"
arguments = ["guide.md"]

[expected]
exit_status = 1

[[expected.diagnostics]]
severity = "error"
code = "E_SOURCE_CHANGED"
```

| Fault | The run |
| --- | --- |
| `source-changed` | Other bytes are written to each source the run read, once discovery has read them and before the recheck before publication, so the recheck meets a source that is no longer the source the run read. |
| `internal` | The run fails in itself once the candidate is built and before anything publishes. |
| `cleanup-refused` | An empty earlier set stands at the run's folder, and its removal once the new set stands is refused, so the run publishes and warns that the earlier set is retained. |
| `unrecognized` | The run is asked for a fault the contract does not name, and refuses the request as invalid usage. |

The detection and the reporting are the run's own either way, which is what each outcome is about: the fault supplies the condition, and what the fixture compares is what the build did with it. A build that performs none of the faults publishes its bundles with no diagnostic, so each fixture fails it.

A fault writes to the tree it runs over, so a fixture declaring one runs in a copy of itself and the corpus leaves the fixture as it found it.

Four fixtures declare a fault: [`source-consistency/a-source-that-changes-during-compilation`](source-consistency/a-source-that-changes-during-compilation/manifest.toml), [`diagnostics/a-run-that-fails-in-itself`](diagnostics/a-run-that-fails-in-itself/manifest.toml), [`publication/an-earlier-set-the-run-cannot-remove-warns`](publication/an-earlier-set-the-run-cannot-remove-warns/manifest.toml) and [`cli/an-unknown-fault-is-invalid-usage`](cli/an-unknown-fault-is-invalid-usage/manifest.toml).

## The schema

[`manifest.schema.json`](manifest.schema.json) is a [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) document, and it is the shape every manifest takes. A manifest is parsed as TOML and validated against it: TOML's value model is a subset of JSON's, so the parsed document validates with no intermediate form. The build reads it with `tomllib` and `jsonschema`.

A manifest that leaves out a declaration the schema requires, names a bundle outside `expected/`, carries a field the schema does not describe, or names a code outside the catalogue its diagnostic's severity selects fails validation, so a malformed fixture fails as a fixture rather than as a bundling.

## The catalogues

A diagnostic is named by its severity and its code together, and the severity decides which catalogue the code comes from. Each code is one the design declares, and the clause it comes from is why it exists.

An error decides a failing run.

| Code | Declared by |
| --- | --- |
| `E_AMBIGUOUS_SOURCE_HEADING` | Source-heading resolution — two headings in one source producing one slug. |
| `E_DISPATCH_CYCLE` | Link classification and resource handling, Dispatch cycles — a chain of dispatched bundles returning to one already on it. |
| `E_GROUP_CONFLICT` | Grouping, Consistent depth — contributing files declare different depths for one group. |
| `E_HEADING_COLLISION` | Link classification and resource handling, Generated heading collisions, and Section composition, Generated heading collisions — an authored heading whose text equals one pf emits in the same bundle, a destination section among them. |
| `E_HEADING_DEPTH_OVERFLOW` | File-scoped hierarchy, Depth overflow; Link classification and resource handling, Parallel dispatch sub-sections; and Section composition, Heading depth — an emitted heading beyond H6, an dispatch-set sub-section or a composed heading among them. |
| `E_INVALID_CONVERSION_METADATA` | Metadata failures — invalid conversion fields or metadata mapping, the refused `root` among them. |
| `E_INVALID_ENCODING` | Markdown and source-heading profile, Encoding — a source that is not valid UTF-8. |
| `E_INVALID_FRONTMATTER` | Metadata failures — malformed or unsafe YAML or duplicate keys. |
| `E_INVALID_USAGE` | CLI contract — a command line the contract's grammar does not admit. |
| `E_NESTED_SECTION_TARGET` | Section extraction, Nested target — a fragment naming a container-nested heading. |
| `E_PARSER_REFERENCE_LIMIT` | Parser viability gates — a parser resource limit suppressing a reference lookup. |
| `E_PUBLICATION_FAILED` | Validation and failure contract, Publication — an output destination that refuses the write, an output folder that cannot be made, a path at the run folder's own that is neither a folder nor a link, or two bundles of one run deriving one name. |
| `E_RAW_HTML` | Markdown and source-heading profile, HTML — raw HTML in selected content. |
| `E_RESOURCE_LIMIT` | Resource limits — a declared budget the run crossed, named with the figure that crossed it, or a numeric scalar longer than the 65,536 characters a byte budget admits. |
| `E_SOURCE_ACCESS` | Metadata failures — a source that cannot be opened or read for an access or filesystem error other than a missing, symlinked or unconfined one. |
| `E_SOURCE_CHANGED` | Source consistency — a source that changed, disappeared or resolved elsewhere during compilation. |
| `E_SOURCE_OUTSIDE_ROOT` | Reference normalization — an entry reference naming a path the working directory cannot contain. |
| `E_SOURCE_SYMLINK` | No-symlink source policy — a source path containing a symlink below the working directory. |
| `E_TARGET_NOT_FOUND` | Link classification, and Section composition, The eligible target — an operator's reference or a composition directive naming no document, or a reference naming no heading in the document it resolves to. |
| `E_UNEXPECTED_INTERNAL_ERROR` | Exit status and JSON diagnostics — an unexpected internal error, which is no source-document defect. |
| `E_UNSAFE_BUNDLE_BOUNDARY` | Block boundaries — a boundary merging content into an unintended container. |
| `E_UNSUPPORTED_CONSTRUCT` | Markdown and source-heading profile, Unsupported extensions — a recognized unsupported dependency or section-naming construct in selected content; Link classification and resource handling, Operators that combine and An operator's target — a link opening with two dispatch marks, a blank between two symbols, a deferral mark written against a dispatch mark, a dispatch mark written against the composition mark, an arrow label, or an operator naming no Markdown document or section; Dispatch links — a dispatched link with no text after its mark, or a dispatch in a heading the bundle emits as text alone: a title its file heading or a member's subsection absorbs, or a title above the selection; Section composition — a directive naming no eligible target, standing in no scope, naming a target with no parent heading or closing a cycle, a section one scope both composes and defers. |
| `E_UNSUPPORTED_ENTRY_SUFFIX` | Markdown and source-heading profile, File suffixes — an explicit entry whose suffix is outside the profile. |
| `E_UNTERMINATED_FRONTMATTER` | Frontmatter policy — a recognized opener with no closing delimiter. |

A warning accompanies a successful run, so a fixture declaring one states what a run writes to standard error while still succeeding.

| Code | Declared by |
| --- | --- |
| `W_COINCIDENT_HEADING` | File-scoped hierarchy and Grouping, Residual ambiguity — two file headings, or two member headings of one merged group, reading alike. |
| `W_COMPOSE_SELF` | Section composition, Composing its own document — a composition directive naming a section of the document that writes it, by fragment or by path, closing no cycle. |
| `W_DISPATCH_DEPTH` | Link classification and resource handling, Dispatch depth — a chain of dispatches reaching a fourth hop. |
| `W_DISPATCH_SELF` | Link classification and resource handling, Dispatching its own document — a dispatched link naming the document that writes it, by fragment or by path, closing no cycle. |
| `W_EARLIER_SET_RETAINED` | Validation and failure contract, Publication — a published run whose earlier set, moved aside, could not be removed. |
| `W_PRESET_UNUSED` | Presets, A preset nothing selected warns — a preset of a document the run carries that no reference reaching it selected. |
| `W_RESOURCE_PORTABILITY` | Resources are text — a bundle read elsewhere may not find the resources its text mentions. |
| `W_SUBST_UNUSED` | Exit status and JSON diagnostics — a `subst` pair no reference used, which substitutes nothing. |
| `W_SUBST_USED` | Exit status and JSON diagnostics — a reference a `subst` pair redirected, named once per pair at the first reference that used it. |

The two catalogues stay distinct: an error diagnostic naming a warning code, and a warning diagnostic naming an error code, each fail validation. A fixture that confuses them has declared a different run.

A test holds each catalogue to the design's own text: it collects every code the design carries under a prefix — `E_` for an error and `W_` for a warning — and requires the schema to enumerate exactly those, so neither catalogue can drift from the contract it is derived from.

Each code either catalogue holds is declared by a fixture, which a further test requires of each severity. A code states a run — an error the failing run it decides, a warning the successful one it accompanies — and a fixture is where that statement is made; a code the catalogue carries and no manifest names is a claim nothing exercises. A fixture awaiting later work counts, because a manifest declares its diagnostics whatever the build under test currently produces.

## Running a fixture

The runner takes one fixture, invokes the build under test against its source tree, and decides pass or fail by comparing the run with the manifest. The build is named by configuration rather than written in the corpus, so one fixture binds every implementation:

```bash
export PROSIFORM_BUILD=pf
```

The value is a command line, split as a shell splits one, so a build reached through a wrapper is named in full. A run's working directory is the fixture's own, so a build named by path is named absolutely and one named by a bare name is found on `PATH`. There is no default and no fallback: with nothing configured the runner refuses to produce a verdict, because a fixture that never ran has not held.

The runner uses `invocation.cwd`, appends `-d json`, then the manifest's `arguments`; a manifest declaring no argument runs the bare command with nothing appended. It asks for the fault a manifest names by the means the [Conformance faults](https://github.com/m2ux/prosiform/blob/96eb2b0f4/artifacts/planning/2026-10-17-prosiform-v1/design.md#conformance-faults) section declares, and a manifest naming none runs a build asked for no fault. The bundles the run writes, its standard output, exit status and diagnostics are each compared with what the manifest declares, and a mismatch names the expectation that differed and locates the difference inside it.

| Expectation | Compared | Located by |
| --- | --- | --- |
| `expected.bundles` | Every file the run creates under the fixture or its working directory, by its name within the run's folder against the bundles declared, then byte for byte, the folder named for one of them with the `.bundles` suffix. Each is removed with its folder once read, so the directory a fixture leaves behind is the one its manifest declares. | A declared bundle the run did not write; a file no bundle names, with the bytes it holds; a file written outside a folder of the run's own; a folder named for no declared bundle; and, for a bundle that differs, the offset of the first differing byte, the line and byte column it falls on, and a window of each side whose control bytes are spelled out, so a CRLF against an LF is visible. |
| `expected.stdout_contains` | For each declared entry, that standard output carries it; with none declared, that standard output is empty. | Each entry the output is missing, or the bytes an empty stream carried, and the output it produced. |
| `expected.exit_status` | As the integer the contract's categories declare. | The status expected and the status the run returned. |
| `expected.diagnostics` | In order, each on the fields the manifest declares, so a diagnostic carrying a remedy the manifest does not name still matches. A declared `message_contains` holds the message to the text it names, and a diagnostic declaring none is matched without reading its message. | The position of a diagnostic missing, extra or carrying another code; both orders when the expected diagnostics arrive in another one; the field, with both values, when one differs; and each text a message is missing, with the message it carried. |

A standard error line that is not a JSON object is reported as one, because the declared format carries diagnostics and nothing else.

## Running the corpus

```bash
make corpus
```

Every fixture in this tree runs against the build `PROSIFORM_BUILD` names, in path order, and each one's verdict is printed under its identity — its path under `fixtures/`. A fixture that differs from its manifest fails the run and its differences are printed under its name; one awaiting later work is reported as awaiting it; one awaiting work it already meets fails the run. The run ends on a count of the fixtures against each verdict, and returns a nonzero status when any fixture failed it or when no build is configured.

## Reading what a piece of work unblocks

```bash
uv run --project src --frozen python checks/corpus.py --awaiting I00:E11:W14
```

The fixtures declaring they await the named work are printed by identity, with a count beneath them, so a session starting that work reads which fixtures it turns green before it changes anything. The request reads the manifests and runs nothing, so it needs no build and returns zero whatever it finds. The name is compared as a manifest declares it: `I00:E11` and `I00:E11:W14` are separate requests, and a fixture is found by the identity its marker carries.

## Running the checks

```bash
make harness
```

Every manifest in this tree is validated against the schema, every path a manifest names is required to exist, the schema's own cases run with it, and the runner's comparison runs with them. The same target holds the [diagram-following eval](../evals/diagram-following/README.md)'s corpus, scorer, runner and report.
