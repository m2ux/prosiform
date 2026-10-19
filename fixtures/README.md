# Fixtures

The language-neutral corpus and the contract it encodes.

A fixture declares a source tree, an invocation and an expected result, so it binds any implementation of prosiform rather than describing one. Nothing here is written in the language of a build: the Python prototype and the production build run the same corpus.

The harness that declares and runs a fixture is the first epic of the prototype initiative; the families it runs are listed in the [design](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md).

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
| `expected.diagnostics` | The diagnostics standard error must carry, in order, each with a severity and a code. A run emitting none declares an empty list. |

The runner supplies the allowed source root and asks for diagnostics as data, so neither is written in `arguments`: a code is compared as a value rather than as prose, which is what makes the comparison the same in every language.

Expected output is a file rather than text inside the manifest because the preservation invariant turns on bytes — newline spelling and the trailing newline among them — and because a bundle is read and reviewed as the Markdown it is.

## The schema

[`manifest.schema.json`](manifest.schema.json) is a [JSON Schema 2020-12](https://json-schema.org/draft/2020-12) document, and it is the shape every manifest takes. A manifest is parsed as TOML and validated against it: TOML's value model is a subset of JSON's, so the parsed document validates with no intermediate form. Python reads it with `tomllib` and `jsonschema`; Rust reads it with the `toml` and `jsonschema` crates.

A manifest that leaves out one of the five declarations, carries a field the schema does not describe, or names an error code outside the catalogue fails validation, so a malformed fixture fails as a fixture rather than as a bundling.

## The catalogue

A diagnostic's `code` comes from this set and no other. Each is a code the design declares, and the clause it comes from is why it exists.

| Code | Declared by |
| --- | --- |
| `E_AMBIGUOUS_FILE_GROUP` | File-scoped hierarchy — two documents whose paths differ only by Markdown extension. |
| `E_AMBIGUOUS_SOURCE_HEADING` | Source-heading resolution — two headings in one source producing one slug. |
| `E_GENERATED_INPUT` | Generated input policy — a source opening on a file heading. |
| `E_HEADING_DEPTH_OVERFLOW` | File-scoped hierarchy, Depth overflow — an emitted heading beyond H6. |
| `E_INVALID_GROUP_RULE` | Grouping — a depth outside 1 through 6, an unknown slug, or a repeated slug. |
| `E_NESTED_SECTION_TARGET` | Section extraction, Nested target — a fragment naming a container-nested heading. |
| `E_PARSER_REFERENCE_LIMIT` | Parser viability gates — a parser resource limit suppressing a reference lookup. |
| `E_SOURCE_OUTSIDE_ROOT` | Reference normalization — a normalized path outside the allowed root. |
| `E_SOURCE_SYMLINK` | No-symlink source policy — a source path containing a symlink below the root. |
| `E_TARGET_NOT_FOUND` | Validation and failure contract — a local Markdown reference resolving to nothing. |
| `E_UNSAFE_BUNDLE_BOUNDARY` | Block boundaries — a boundary merging content into an unintended container. |
| `E_UNTERMINATED_FRONTMATTER` | Frontmatter policy — a recognized opener with no closing delimiter. |

The catalogue is closed over errors. The design describes two warnings — a grouping rule that arranges nothing, and the portability of a resource reference — and names a code for neither, so a warning diagnostic cannot yet be declared.

A test holds the catalogue to the design's own text: it collects every `E_`-prefixed code the design carries and requires the schema to enumerate exactly those, so the catalogue cannot drift from the contract it is derived from.

## Running a fixture

The runner takes one fixture, invokes the build under test against its source tree, and decides pass or fail by comparing the run with the manifest. The build is named by configuration rather than written in the corpus, so one fixture binds every implementation:

```bash
export PROSIFORM_BUILD=prosiform
```

The value is a command line, split as a shell splits one, so a build reached through a wrapper is named in full. There is no default and no fallback: with nothing configured the runner refuses to produce a verdict, because a fixture that never ran has not held.

The runner appends `--root`, the fixture's source tree resolved to an absolute path, and `--diagnostics json` to that command, and then the manifest's `arguments`. The run's standard output, exit status and diagnostics are each compared with what the manifest declares, and a mismatch names the expectation that differed and locates the difference inside it.

| Expectation | Compared | Located by |
| --- | --- | --- |
| `expected.stdout` | Byte for byte against the file the manifest names. | The offset of the first differing byte, the line and byte column it falls on, and a window of each side whose control bytes are spelled out, so a CRLF against an LF is visible. |
| `expected.exit_status` | As the integer the contract's categories declare. | The status expected and the status the run returned. |
| `expected.diagnostics` | In order, each on the fields the manifest declares, so a diagnostic carrying a message or a remedy the manifest does not name still matches. | The position of a diagnostic missing, extra or carrying another code; both orders when the expected diagnostics arrive in another one; and the field, with both values, when one differs. |

A standard error line that is not a JSON object is reported as one, because the declared format carries diagnostics and nothing else.

## Running the checks

```bash
make corpus
```

Every manifest in this tree is validated against the schema, every path a manifest names is required to exist, the schema's own cases run with it, and the runner's comparison runs with them.
