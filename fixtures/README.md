# Fixtures

The language-neutral corpus and the contract it encodes.

A fixture declares a source tree, an invocation and an expected result, so it binds any implementation of prosiform rather than describing one. Nothing here is written in the language of a build: the Python build and the production build run the same corpus.

The harness that declares and runs a fixture is the first epic of the first initiative; the families it runs are listed in the [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md).

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
            └── stdout.md
```

`source/` is the tree the run is confined to. `expected/` holds the bytes the run must produce. They are separate because an expected bundle is itself Markdown, and a bundle offered as input is refused under the generated-input policy.

## A symbolic link in a source tree

A source tree carries a symbolic link where the clause under test is about one. Git records a link as its own object — mode `120000`, the target as its content — so a fixture declaring the no-symlink source policy declares it as a link rather than as a file holding a path, and a runner materialises the tree the manifest describes.

A link's target is a path inside the fixture, written relative to the link, so the fixture is self-contained wherever the repository is checked out. A target outside the source tree sits beside it under the fixture's own directory, which is how a link that resolves out of the allowed root is declared without naming anything of the host.

A checkout whose filesystem or configuration cannot create a link writes the target path into a regular file instead. Such a tree no longer states what the fixture declares, and the fixture fails rather than passing against a file that looks like a document.

## Copied sources

Most families write their sources for the clause they exercise. The `real-source/` family does not: each of its sources is a document copied byte for byte from one of this workspace's skills, at the root-relative path that skill gives it. A source written to exercise one clause exercises that clause and says nothing about the documents the tool exists to bundle, so this family is where the corpus meets prose nobody wrote for it.

A copied source is not edited. A document that needs an edit to bundle is a defect in the build or a gap in the design, and the record of that is a finding rather than a changed document. The documents live upstream and a copy carries no authority to change them; each is held to its original with `cmp` and `sha256sum`, outside the corpus, because the original is in another repository.

A document joins the family when its closure is itself: no local Markdown document reference, and fragment-only references only where the destination the bundle generates is the fragment the source already spells. Such a document bundles to the same bytes under a build that traverses references and one that has nothing to traverse, so its expected bundle states the contract rather than a stage of the work.

## The manifest

The manifest is the whole declaration. A runner reads it and the fixture's files, and decides pass or fail from them alone.

```toml
description = "A reference normalizing to a path outside the allowed source root fails."

clauses = [
  "Reference normalization and path identity — Resolution sequence, step 7",
]

[invocation]
root = "source"
arguments = ["guide.md"]

[expected]
exit_status = 1
stdout = "expected/stdout.md"

[[expected.diagnostics]]
severity = "error"
code = "E_SOURCE_OUTSIDE_ROOT"
reference = "../outside.md"
source = "guide.md:3"
```

| Field | Declares |
| --- | --- |
| `description` | What the fixture establishes. |
| `clauses` | The design clauses it encodes, so every clause maps to the fixtures that cover it. |
| `invocation.root` | The source tree, fixture-relative. The runner resolves it and passes it as the allowed source root. |
| `invocation.arguments` | The arguments of the invocation, in order. |
| `expected.exit_status` | The process exit status: one of the five categories the contract declares. |
| `expected.stdout` | The fixture-relative file holding the bytes standard output must carry. A run publishing no bundle names an empty file. |
| `expected.diagnostics` | The diagnostics standard error must carry, in order, each with a severity and a code drawn from the catalogue that severity selects. A run emitting none declares an empty list. |
| `expected.absent` | Optional. The fixture-relative paths the run must leave absent, such as an output file a validation-only run is told to write and must not. A fixture whose run creates no file names none. |
| `awaiting` | Optional. The work that delivers the behaviour the fixture declares, written as an initiative and an epic and optionally the task within it, such as `I00:E03`. A fixture carrying it is one the corpus declares ahead of the build. |

The runner supplies the allowed source root and asks for diagnostics as data, so neither is written in `arguments`: a code is compared as a value rather than as prose, which is what makes the comparison the same in every language.

Expected output is a file rather than text inside the manifest because the preservation invariant turns on bytes — newline spelling and the trailing newline among them — and because a bundle is read and reviewed as the Markdown it is.

A run's working directory is the fixture's own, so a path an invocation writes lands among the fixture's files. A comparison of the two streams says nothing about such a file, which is why a run that must leave one unwritten declares the path:

```toml
[invocation]
root = "source"
arguments = ["--check", "--output", "bundle.md", "guide.md"]

[expected]
exit_status = 0
stdout = "expected/stdout.md"
diagnostics = []
absent = ["bundle.md"]
```

A fixture that already holds a path it declares absent is malformed and is refused before the build is invoked, because a declaration the directory contradicts before the run states nothing about the run.

## A fixture ahead of the build

The corpus states the contract, and the contract is delivered epic by epic, so a fixture may declare behaviour no build produces yet. Such a fixture names the work that delivers it:

```toml
awaiting = "I00:E03"
```

A fixture carrying `awaiting` and failing is reported as awaiting that work, and the corpus run stays green: an expectation the contract makes and the build has not met yet is a statement about the schedule rather than a defect. A fixture carrying it and meeting its manifest fails the run, naming the manifest to lift the marker from, so the marker is temporary by construction — the change that delivers the work is the change that fails until the marker goes.

The marker lives in the manifest because the expectation is the fixture's own. A list of excepted fixtures held in a command or a job definition drifts from the corpus in both directions: a fixture renamed or deleted leaves a line behind, and a reader of the fixture sees nothing. Naming the work rather than setting a flag tells the session delivering that work which fixtures to revisit.

Two fixtures carry the marker. `normalization/root-escape` awaits `I00:E04`, which delivers dependency traversal. `extraction/an-unterminated-example-at-the-section-end` awaits `I00:E08`, which delivers boundary safety: a code example a source never closes absorbs the group written after it, and the run refuses that boundary rather than closing the example.

## The schema

[`manifest.schema.json`](manifest.schema.json) is a [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) document, and it is the shape every manifest takes. A manifest is parsed as TOML and validated against it: TOML's value model is a subset of JSON's, so the parsed document validates with no intermediate form. Python reads it with `tomllib` and `jsonschema`; Rust reads it with the `toml` and `jsonschema` crates.

A manifest that leaves out one of the five declarations, carries a field the schema does not describe, or names a code outside the catalogue its diagnostic's severity selects fails validation, so a malformed fixture fails as a fixture rather than as a bundling.

## The catalogues

A diagnostic is named by its severity and its code together, and the severity decides which catalogue the code comes from. Each code is one the design declares, and the clause it comes from is why it exists.

An error decides a failing run.

| Code | Declared by |
| --- | --- |
| `E_AMBIGUOUS_FILE_GROUP` | File-scoped hierarchy — two documents whose paths differ only by Markdown extension. |
| `E_AMBIGUOUS_SOURCE_HEADING` | Source-heading resolution — two headings in one source producing one slug. |
| `E_GENERATED_INPUT` | Generated input policy — a source opening on a file heading. |
| `E_HEADING_DEPTH_OVERFLOW` | File-scoped hierarchy, Depth overflow — an emitted heading beyond H6. |
| `E_INVALID_ENCODING` | Markdown and source-heading profile, Encoding — a source that is not valid UTF-8. |
| `E_INVALID_GROUP_RULE` | Grouping — a depth outside 1 through 6, an unknown slug, or a repeated slug. |
| `E_INVALID_USAGE` | CLI contract — a command line the contract's grammar does not admit. |
| `E_NESTED_SECTION_TARGET` | Section extraction, Nested target — a fragment naming a container-nested heading. |
| `E_PARSER_REFERENCE_LIMIT` | Parser viability gates — a parser resource limit suppressing a reference lookup. |
| `E_PUBLICATION_FAILED` | Validation and failure contract, Publication — an output destination that refuses the write. |
| `E_RAW_HTML` | Markdown and source-heading profile, HTML — raw HTML in selected content. |
| `E_ROOT_NOT_FOUND` | CLI contract — an allowed source root naming no directory. |
| `E_SOURCE_OUTSIDE_ROOT` | Reference normalization — a normalized path outside the allowed root. |
| `E_SOURCE_SYMLINK` | No-symlink source policy — a source path containing a symlink below the root. |
| `E_TARGET_NOT_FOUND` | Validation and failure contract — a local Markdown reference resolving to nothing. |
| `E_UNEXPECTED_INTERNAL_ERROR` | Exit status and JSON diagnostics — an unexpected internal error, which is no source-document defect. |
| `E_UNSAFE_BUNDLE_BOUNDARY` | Block boundaries — a boundary merging content into an unintended container. |
| `E_UNSUPPORTED_CONSTRUCT` | Markdown and source-heading profile, Unsupported extensions — a recognized unsupported dependency or section-naming construct in selected content. |
| `E_UNSUPPORTED_ENTRY_SUFFIX` | Markdown and source-heading profile, File suffixes — an explicit entry whose suffix is outside the profile. |
| `E_UNTERMINATED_FRONTMATTER` | Frontmatter policy — a recognized opener with no closing delimiter. |

A warning accompanies a successful run, so a fixture declaring one states what a run writes to standard error while still succeeding.

| Code | Declared by |
| --- | --- |
| `W_EMPTY_GROUP_RULE` | Grouping — a rule whose directories contribute no document to the closure. |
| `W_RESOURCE_PORTABILITY` | Resources are text — a bundle read elsewhere may not find the resources its text mentions. |

The two catalogues stay distinct: an error diagnostic naming a warning code, and a warning diagnostic naming an error code, each fail validation. A fixture that confuses them has declared a different run.

A test holds each catalogue to the design's own text: it collects every code the design carries under a prefix — `E_` for an error and `W_` for a warning — and requires the schema to enumerate exactly those, so neither catalogue can drift from the contract it is derived from.

## Running a fixture

The runner takes one fixture, invokes the build under test against its source tree, and decides pass or fail by comparing the run with the manifest. The build is named by configuration rather than written in the corpus, so one fixture binds every implementation:

```bash
export PROSIFORM_BUILD=prosiform
```

The value is a command line, split as a shell splits one, so a build reached through a wrapper is named in full. A run's working directory is the fixture's own, so a build named by path is named absolutely and one named by a bare name is found on `PATH`. There is no default and no fallback: with nothing configured the runner refuses to produce a verdict, because a fixture that never ran has not held.

The runner appends `--root`, the fixture's source tree resolved to an absolute path, and `--diagnostics json` to that command, and then the manifest's `arguments`. The run's standard output, exit status and diagnostics are each compared with what the manifest declares, and a mismatch names the expectation that differed and locates the difference inside it.

| Expectation | Compared | Located by |
| --- | --- | --- |
| `expected.stdout` | Byte for byte against the file the manifest names. | The offset of the first differing byte, the line and byte column it falls on, and a window of each side whose control bytes are spelled out, so a CRLF against an LF is visible. |
| `expected.exit_status` | As the integer the contract's categories declare. | The status expected and the status the run returned. |
| `expected.diagnostics` | In order, each on the fields the manifest declares, so a diagnostic carrying a message or a remedy the manifest does not name still matches. | The position of a diagnostic missing, extra or carrying another code; both orders when the expected diagnostics arrive in another one; and the field, with both values, when one differs. |
| `expected.absent` | Each declared path, after the run. | The path the run created and the bytes it wrote. The file is removed once it is reported, so the directory a fixture leaves behind is the one its manifest declares. |

A standard error line that is not a JSON object is reported as one, because the declared format carries diagnostics and nothing else.

## Running the corpus

```bash
make corpus
```

Every fixture in this tree runs against the build `PROSIFORM_BUILD` names, in path order, and each one's verdict is printed under its identity — its path under `fixtures/`. A fixture that differs from its manifest fails the run and its differences are printed under its name; one awaiting later work is reported as awaiting it; one awaiting work it already meets fails the run. The run ends on a count of the fixtures against each verdict, and returns a nonzero status when any fixture failed it or when no build is configured.

## Running the checks

```bash
make harness
```

Every manifest in this tree is validated against the schema, every path a manifest names is required to exist, the schema's own cases run with it, and the runner's comparison runs with them.
