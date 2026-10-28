# Fixtures

The language-neutral corpus and the contract it encodes.

A fixture declares a source tree, an invocation and an expected result, so it binds any implementation of prosiform rather than describing one. Nothing here is written in the language of a build: a fixture names no language, no package and no module, so the corpus binds the build that runs it rather than describing how it is written.

The families the corpus runs are listed in the [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md).

## A fixture

A fixture is a directory holding `manifest.toml`. Discovery walks this tree and takes every directory that carries one, so a family is a directory and a fixture's identity is its path under `fixtures/`.

```text
fixtures/
├── manifest.schema.json
└── normalization/
    └── root-escape/
        ├── manifest.toml
        ├── source/
        │   └── guide.md
        └── expected/
            └── guide.bundle.md
```

`source/` is the tree the run is confined to. `expected/` holds each bundle the run must write, under the name the run gives it. They are separate because an expected bundle is itself Markdown, which a run over `source/` must not read as one of its sources.

## A symbolic link in a source tree

A source tree carries a symbolic link where the clause under test is about one. Git records a link as its own object — mode `120000`, the target as its content — so a fixture declaring the no-symlink source policy declares it as a link rather than as a file holding a path, and a runner materialises the tree the manifest describes.

A link inside a source tree targets a path inside the fixture, written relative to the link, so the fixture is self-contained wherever the repository is checked out. A target outside the source tree sits beside it under the fixture's own directory, which is how a link that resolves out of the allowed root is declared without naming anything of the host. The one link that leaves a fixture is the `source` of a `usage-example/` fixture, which is the tree itself rather than a file within it.

A checkout whose filesystem or configuration cannot create a link writes the target path into a regular file instead. Such a tree no longer states what the fixture declares, and the fixture fails rather than passing against a file that looks like a document.

## Copied sources

Most families write their sources for the clause they exercise. The `real-source/` family does not: each of its sources is a document copied byte for byte from one of this workspace's skills, at the path that skill gives it. A source written to exercise one clause exercises that clause and says nothing about the documents the tool exists to bundle, so this family is where the corpus meets prose nobody wrote for it.

A copied source is not edited. A document that needs an edit to bundle is a defect in the build or a gap in the design, and the record of that is a finding rather than a changed document. The documents live upstream and a copy carries no authority to change them; each is held to its original with `cmp` and `sha256sum`, outside the corpus, because the original is in another repository.

A document joins the family when its closure is itself: no local Markdown document reference, and fragment-only references only where the destination the bundle generates is the fragment the source already spells. Such a document bundles to the same bytes under a build that traverses references and one that has nothing to traverse, so its expected bundle states the contract rather than a stage of the work.

## The example tree

The `usage-example/` family runs the invocations the [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) publishes as its usage examples, so an example that stops being a valid invocation fails a run rather than going quietly stale.

Each of its fixtures reaches [`example/work-planner/`](../example/work-planner/SKILL.md) through a `source` symbolic link, because the design and the corpus must name one tree: a copy per fixture would let the published invocation and the invocation under test drift apart. The tree is the repository's own example material, maintained with the contract, rather than a source written for one clause.

## The manifest

The manifest is the whole declaration. A runner reads it and the fixture's files, and decides pass or fail from them alone.

```toml
description = "A reference normalizing to a path outside the allowed source root fails."

clauses = [
  "Resolution sequence — step 7",
]

[invocation]
cwd = "source"
arguments = ["guide.md"]

[expected]
exit_status = 1

[[expected.diagnostics]]
severity = "error"
code = "E_SOURCE_OUTSIDE_ROOT"
reference = "../outside.md"
source = "guide.md:3"
chain = ["guide.md", "../outside.md"]
```

| Field | Declares |
| --- | --- |
| `description` | What the fixture establishes. |
| `clauses` | The design clauses it encodes, named as [The clause form](#the-clause-form) states, so every clause maps to the fixtures that cover it. |
| `invocation.cwd` | Optional existing fixture-relative working directory; absent means the fixture directory. Source metadata supplies dependency roots. |
| `invocation.arguments` | The arguments of the invocation, in order. |
| `expected.exit_status` | The process exit status: one of the five categories the contract declares. |
| `expected.bundles` | Optional. The fixture-relative files under `expected/` holding the bytes of each bundle the run writes into its folder, each named as the run names the bundle. A run writing no bundle declares none. |
| `expected.stdout_contains` | Optional. The text standard output must carry, where the whole of the response is a build's own. Standard output carries no bundle, so a fixture declaring none declares an empty stream. |
| `expected.diagnostics` | The diagnostics standard error must carry, in order, each with a severity and a code drawn from the catalogue that severity selects, and optionally the `message_contains`, `reference`, `resolved`, `source` and `chain` a diagnostic carries. A run emitting none declares an empty list. |
| `awaiting` | Optional. The work that delivers the behaviour the fixture declares, written as an initiative and an epic and optionally the task within it, such as `I00:E03`. A fixture carrying it declares behaviour the build does not yet meet. |
| `fault` | Optional. The fault the run performs on itself, `source-changed` or `internal`, which the runner asks for as `-x NAME`. A fixture declaring none declares a run that meets no fault. |

The runner uses the working directory the manifest names and asks for diagnostics as data, so neither is written in `arguments`: a code is compared as a value rather than as prose, which is what makes the comparison the same in every language. The runner names no output folder, so a run writes its folder of bundles where its own arguments send it: the working directory, or the folder an `-o` among them names.

## The clause form

A clause is a heading of the [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md), or an enumerated rule under one: a bold-led bullet, a step of a numbered sequence, or a row of a table. A heading names the rule its own prose states, and a rule under it is named by both, separated by an em dash:

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

Two families are named by no fixture, each because the condition it turns on is one a source tree and one invocation cannot declare. Consistency is a source changing, disappearing or resolving elsewhere while the run reads it, and its fixture arrives with [I00:E11:W24](https://github.com/m2ux/prosiform/issues/150). Parser exhaustion is a parser resource limit suppressing a reference lookup, which `E_PARSER_REFERENCE_LIMIT` reports and no build here emits, and its fixture arrives with [I00:E11:W30](https://github.com/m2ux/prosiform/issues/164).

A published bundle is expected as a file rather than as text inside the manifest because the preservation invariant turns on bytes — newline spelling and the trailing newline among them — and because a bundle is read and reviewed as the Markdown it is.

A run's working directory is the fixture's own, so the folder a run writes its bundles into lands among the fixture's files. Every file the run creates under the fixture or its working directory is the run's output: it is compared by its name within the run's folder with the bundles the manifest declares and removed with that folder, so a run writing a file no bundle names fails, as does one writing a file outside a folder of its own or into a folder named for no declared bundle, and a validation-only run declares no bundle at all:

```toml
[invocation]
cwd = "source"
arguments = ["-c", "-o", "..", "guide.md"]

[expected]
exit_status = 0
diagnostics = []
```

## Root declarations

A source declares an explicit dependency root in its leading prosiform mapping. Missing directories fail with E_ROOT_NOT_FOUND. The invocation working directory must exist; absent roots in source metadata use that directory. A parent-directory entry is authorized by bounded no-follow bootstrap capture. The retired -r option fails as invalid usage.

## Text an output carries

Some of what a run writes is the build's own. A version string is the clearest case, and a diagnostic's wording is the same case in a smaller place. A fixture declaring either of them whole would bind the corpus to one implementation, so it declares the text the output must carry instead: a list whose entries are substrings the output contains.

```toml
[invocation]
cwd = "source"
arguments = ["-v"]

[expected]
exit_status = 0
stdout_contains = ["prosiform ", "(skill-markdown-v3)"]
diagnostics = []
```

The response reports the tool and the profile identifier, and the version between them belongs to the build. Standard output carries no bundle, so a fixture declaring no `stdout_contains` declares an empty stream, and no run goes uncompared.

A diagnostic declares the same thing about its message, which is how two faults sharing one error code are told apart:

```toml
[[expected.diagnostics]]
severity = "error"
code = "E_INVALID_USAGE"
message_contains = ["#a-section", "-f"]
```

`E_INVALID_USAGE` names every command line the grammar does not admit, and the contract has the message say which fault it was. A fixture names the run's own data the message must carry — the reference refused, the option whose value was outside its set, the run folder that held an input source — so a build reporting another fault under that code fails the fixture while each build keeps its own phrasing. The field is optional, and a diagnostic declaring none states nothing about its message.

The contract gathers seven faults under the code, and each is a fixture, so what the corpus covers under one code is read from the corpus rather than assumed from the code:

| Fault | Fixture |
| --- | --- |
| The retired `-r` option | [`cli/a-command-line-naming-no-allowed-source-root`](cli/a-command-line-naming-no-allowed-source-root/manifest.toml) |
| No entry reference | [`cli/a-command-line-naming-no-entry-reference`](cli/a-command-line-naming-no-entry-reference/manifest.toml) |
| An option the contract does not declare | [`cli/an-option-the-contract-does-not-declare`](cli/an-option-the-contract-does-not-declare/manifest.toml) |
| An option value outside the set its row names | [`cli/diagnostics-format-unknown`](cli/diagnostics-format-unknown/manifest.toml) |
| A fragment-only reference with no `-f` | [`cli/fragment-only-reference-without-from`](cli/fragment-only-reference-without-from/manifest.toml) |
| A run folder holding an input source | [`cli/run-folder-holding-a-dependency-source`](cli/run-folder-holding-a-dependency-source/manifest.toml) |
| Standard output named as the output folder | [`cli/standard-output-named-as-the-output-folder`](cli/standard-output-named-as-the-output-folder/manifest.toml) |

An entry reference whose own spelling the grammar does not admit — a query, an encoded separator, an over-long escape, an escape decoding to no UTF-8 — carries the same code, and the `normalization/` family states it where the clause under test is the resolution sequence rather than the command line's shape.

## A fixture awaiting its work

The corpus states the contract in full, so a fixture may declare behaviour the build does not yet produce. Such a fixture names the work that delivers it:

```toml
awaiting = "I00:E03"
```

A fixture carrying `awaiting` and failing is reported as awaiting that work, and the corpus run stays green: an expectation the contract makes and the build does not meet is a declared gap rather than a defect. A fixture carrying it and meeting its manifest fails the run, naming the manifest to lift the marker from, so the marker is temporary by construction — the change that delivers the work is the change that fails until the marker goes.

The marker lives in the manifest because the expectation is the fixture's own. A list of excepted fixtures held in a command or a job definition drifts from the corpus in both directions: a fixture renamed or deleted leaves a line behind, and a reader of the fixture sees nothing. Naming the work rather than setting a flag tells the session delivering that work which fixtures to revisit.

## A fault the run performs on itself

Two of the outcomes the contract declares are facts about the run rather than about any document it reads: a source that changes during compilation, and a run that fails in itself. A fixture declares a source tree, an invocation and a result, so neither arises from that declaration, and the contract declares `-x NAME` for a conformance run to reach them. A manifest names the fault its run meets:

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

The detection and the reporting are the run's own either way, which is what each outcome is about: the fault supplies the condition, and what the fixture compares is what the build did with it. A build that performs neither fault publishes a bundle and exits 0, so both fixtures fail it.

A fault writes to the tree it runs over, so a fixture declaring one runs in a copy of itself and the corpus leaves the fixture as it found it.

Two fixtures declare a fault: [`source-consistency/a-source-that-changes-during-compilation`](source-consistency/a-source-that-changes-during-compilation/manifest.toml) and [`diagnostics/a-run-that-fails-in-itself`](diagnostics/a-run-that-fails-in-itself/manifest.toml).

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
| `E_GROUP_DEPTH_CONFLICT` | Grouping, Consistent depth — contributing files declare different depths for one group. |
| `E_HEADING_COLLISION` | Link classification and resource handling, Generated heading collisions — an authored heading whose text equals one pf emits in the same bundle. |
| `E_HEADING_DEPTH_OVERFLOW` | File-scoped hierarchy, Depth overflow, and Link classification and resource handling, Dispatch sub-sections — an emitted heading beyond H6, a dispatch sub-section among them. |
| `E_INVALID_CONVERSION_METADATA` | Metadata failures — invalid conversion fields or metadata mapping. |
| `E_INVALID_ENCODING` | Markdown and source-heading profile, Encoding — a source that is not valid UTF-8. |
| `E_INVALID_FRONTMATTER` | Metadata failures — malformed or unsafe YAML, duplicate keys, or an invalid root. |
| `E_INVALID_USAGE` | CLI contract — a command line the contract's grammar does not admit. |
| `E_NESTED_SECTION_TARGET` | Section extraction, Nested target — a fragment naming a container-nested heading. |
| `E_PARSER_REFERENCE_LIMIT` | Parser viability gates — a parser resource limit suppressing a reference lookup. |
| `E_PUBLICATION_FAILED` | Validation and failure contract, Publication — an output destination that refuses the write. |
| `E_RAW_HTML` | Markdown and source-heading profile, HTML — raw HTML in selected content. |
| `E_RESOURCE_LIMIT` | Resource limits — a declared budget the run crossed, named with the figure that crossed it. |
| `E_ROOT_NOT_FOUND` | CLI contract — an allowed source root naming no directory. |
| `E_SOURCE_CHANGED` | Source consistency — a source that changed, disappeared or resolved elsewhere during compilation. |
| `E_SOURCE_OUTSIDE_ROOT` | Reference normalization — an entry reference naming a path the allowed root cannot contain. |
| `E_SOURCE_SYMLINK` | No-symlink source policy — a source path containing a symlink below the root. |
| `E_TARGET_NOT_FOUND` | Link classification — a reference under the root naming no document, or no heading in the document it resolves to. |
| `E_UNEXPECTED_INTERNAL_ERROR` | Exit status and JSON diagnostics — an unexpected internal error, which is no source-document defect. |
| `E_UNSAFE_BUNDLE_BOUNDARY` | Block boundaries — a boundary merging content into an unintended container. |
| `E_UNSUPPORTED_CONSTRUCT` | Markdown and source-heading profile, Unsupported extensions — a recognized unsupported dependency or section-naming construct in selected content; Link classification and resource handling, One operator per link and An operator's target — a link opening with more than one operator, or an operator naming no Markdown document or section under the root. |
| `E_UNSUPPORTED_ENTRY_SUFFIX` | Markdown and source-heading profile, File suffixes — an explicit entry whose suffix is outside the profile. |
| `E_UNTERMINATED_FRONTMATTER` | Frontmatter policy — a recognized opener with no closing delimiter. |

A warning accompanies a successful run, so a fixture declaring one states what a run writes to standard error while still succeeding.

| Code | Declared by |
| --- | --- |
| `W_COINCIDENT_HEADING` | File-scoped hierarchy and Grouping, Residual ambiguity — two file headings, or two member headings of one merged group, reading alike. |
| `W_DISPATCH_DEPTH` | Link classification and resource handling, Dispatch depth — a chain of dispatches reaching a fourth hop. |
| `W_DISPATCH_SELF` | Link classification and resource handling, Dispatching its own document — a dispatched link naming the document that writes it, by fragment or by path, closing no cycle. |
| `W_RESOURCE_PORTABILITY` | Resources are text — a bundle read elsewhere may not find the resources its text mentions. |
| `W_RUN_SET_SHAPE` | Link classification and resource handling, Run-set shape — a run-set link naming a target that holds anything but one bulleted list whose every item links a Markdown document or section under the root. |

The two catalogues stay distinct: an error diagnostic naming a warning code, and a warning diagnostic naming an error code, each fail validation. A fixture that confuses them has declared a different run.

A test holds each catalogue to the design's own text: it collects every code the design carries under a prefix — `E_` for an error and `W_` for a warning — and requires the schema to enumerate exactly those, so neither catalogue can drift from the contract it is derived from.

Each code either catalogue holds is declared by a fixture, which a further test requires of each severity. A code states a run — an error the failing run it decides, a warning the successful one it accompanies — and a fixture is where that statement is made; a code the catalogue carries and no manifest names is a claim nothing exercises. A fixture awaiting later work counts, because a manifest declares its diagnostics whatever the build under test currently produces.

## Running a fixture

The runner takes one fixture, invokes the build under test against its source tree, and decides pass or fail by comparing the run with the manifest. The build is named by configuration rather than written in the corpus, so one fixture binds every implementation:

```bash
export PROSIFORM_BUILD=prosiform
```

The value is a command line, split as a shell splits one, so a build reached through a wrapper is named in full. A run's working directory is the fixture's own, so a build named by path is named absolutely and one named by a bare name is found on `PATH`. There is no default and no fallback: with nothing configured the runner refuses to produce a verdict, because a fixture that never ran has not held.

The runner uses `invocation.cwd`, appends `-d json`, and `-x` where the manifest names a fault, then the manifest's `arguments`. The bundles the run writes, its standard output, exit status and diagnostics are each compared with what the manifest declares, and a mismatch names the expectation that differed and locates the difference inside it.

| Expectation | Compared | Located by |
| --- | --- | --- |
| `expected.bundles` | Every file the run creates under the fixture or its working directory, by its name within the run's folder against the bundles declared, then byte for byte, the folder named for one of them. Each is removed with its folder once read, so the directory a fixture leaves behind is the one its manifest declares. | A declared bundle the run did not write; a file no bundle names, with the bytes it holds; a file written outside a folder of the run's own; a folder named for no declared bundle; and, for a bundle that differs, the offset of the first differing byte, the line and byte column it falls on, and a window of each side whose control bytes are spelled out, so a CRLF against an LF is visible. |
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

Every manifest in this tree is validated against the schema, every path a manifest names is required to exist, the schema's own cases run with it, and the runner's comparison runs with them.
