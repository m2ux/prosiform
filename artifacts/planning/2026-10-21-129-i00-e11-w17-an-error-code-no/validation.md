# Validation

The checks this row was held to, the revision they ran at, and what they observed.

## Revision

The branch `i00/e11/w17-an-error-code-no`, cut from `i00/e11/main` at `ce4483c`. Every run below invoked the Makefile target a developer and continuous integration both call, from the repository root of the task worktree, with `PROSIFORM_BUILD` naming the locked build's console entry point.

## Coverage Measured

The error catalogue the schema enumerates, read against the codes the corpus's manifests declare, at this revision.

| Error | Fixtures declaring it | Of those, awaiting later work |
| --- | --- | --- |
| `E_AMBIGUOUS_FILE_GROUP` | 1 | |
| `E_AMBIGUOUS_SOURCE_HEADING` | 1 | |
| `E_GENERATED_INPUT` | 2 | |
| `E_HEADING_DEPTH_OVERFLOW` | 2 | |
| `E_INVALID_ENCODING` | 3 | |
| `E_INVALID_GROUP_RULE` | 3 | |
| `E_INVALID_USAGE` | 10 | |
| `E_NESTED_SECTION_TARGET` | 2 | |
| `E_PARSER_REFERENCE_LIMIT` | 1 | |
| `E_PUBLICATION_FAILED` | 1 | |
| `E_RAW_HTML` | 1 | |
| `E_RESOURCE_LIMIT` | 9 | |
| `E_ROOT_NOT_FOUND` | 1 | |
| `E_SOURCE_CHANGED` | 1 | 1, `source-consistency/a-source-that-changes-during-compilation`, awaiting `I00:E11:W24` |
| `E_SOURCE_OUTSIDE_ROOT` | 4 | |
| `E_SOURCE_SYMLINK` | 5 | |
| `E_TARGET_NOT_FOUND` | 9 | |
| `E_UNEXPECTED_INTERNAL_ERROR` | 1 | 1, `diagnostics/a-run-that-fails-in-itself`, awaiting `I00:E11:W24` |
| `E_UNSAFE_BUNDLE_BOUNDARY` | 4 | |
| `E_UNSUPPORTED_CONSTRUCT` | 1 | |
| `E_UNSUPPORTED_ENTRY_SUFFIX` | 2 | |
| `E_UNTERMINATED_FRONTMATTER` | 1 | |

The same measurement taken before the change found three codes no manifest declared: `E_PUBLICATION_FAILED`, `E_SOURCE_CHANGED` and `E_UNEXPECTED_INTERNAL_ERROR`. `E_ROOT_NOT_FOUND` and `E_PARSER_REFERENCE_LIMIT`, which the issue records as unreached when it was raised, arrived with the rows this one depends on and were already declared when the work began. Every error the design declares is now carried by a manifest, and the warning catalogue is unchanged and still fully declared.

## Reachability of Each Unreached Run

A fixture declares a source tree, an invocation and the result the run must produce, and the runner decides its verdict from those alone. Two of the three runs do not arise from that declaration.

| Code | The run | Reached from a fixture |
| --- | --- | --- |
| `E_PUBLICATION_FAILED` | An output destination that refuses the write | Yes — `--output no-such-directory/bundle.md` names a path whose parent the fixture does not hold, so the write is refused on every checkout |
| `E_SOURCE_CHANGED` | A source that is no longer the source the run read | No — the bytes discovery captured are the bytes the recheck reads, because nothing writes to the tree between them |
| `E_UNEXPECTED_INTERNAL_ERROR` | A fault that is no source-document defect | No — the code names the run rather than any document, so a source provoking one would be a defect to fix rather than the outcome the contract declares |

The two unreachable runs are declared with the `awaiting` marker and await `I00:E11:W24`, raised from this row, which gives the runner the fault a manifest names.

## Harness Suite

`make harness`, the corpus's own checks, which carry the coverage assertion.

```text
491 passed in 7.35s
```

`test_every_code_the_design_declares_is_declared_by_a_fixture` is among them, parametrized over each severity. It subtracts the codes the corpus's manifests declare from the catalogue the severity selects and requires the difference to be empty, naming any code the corpus leaves unstated.

The assertion was exercised against a corpus that fails it: the manifest of `delivery/an-output-destination-that-refuses-the-write` was held aside and the suite re-run.

```text
E   AssertionError: no fixture declares E_PUBLICATION_FAILED, so the corpus states nothing about the run that error names
E   assert not {'E_PUBLICATION_FAILED'}
FAILED checks/tests/test_catalogue.py::test_every_code_the_design_declares_is_declared_by_a_fixture[error]
1 failed, 4 passed in 0.07s
```

An error losing its only fixture is therefore reported rather than passing in silence, which is what makes the green run above a statement. The warning parametrization runs the same assertion the previous check made, so the coverage the warning catalogue already had is kept.

## Corpus Run

`make corpus`, the whole corpus against the build under test.

```text
corpus check: 220 fixture(s), 218 pass, 0 fail, 2 awaited, 0 unexpected pass
```

The run names the three fixtures this row adds:

```text
delivery/an-output-destination-that-refuses-the-write: pass
diagnostics/a-run-that-fails-in-itself: awaited, awaiting I00:E11:W24
source-consistency/a-source-that-changes-during-compilation: awaited, awaiting I00:E11:W24
```

The publication fixture runs against the build and holds: the run returns status 3, emits one `E_PUBLICATION_FAILED` diagnostic, writes nothing to standard output and leaves the output path absent. The two marked fixtures fail against the build in hand, are reported as awaiting their work and leave the corpus's verdict green. The declaration is the corpus's whatever the build currently produces, which is why the criterion is met by the fixture carrying the code.

The run also showed what a failing run does not emit: the first draft of the publication manifest declared `W_ENTRY_DESTINATION` ahead of the error, and the runner reported one diagnostic where two were expected. The entry-destination report accompanies a published bundle, so a run refused the write emits the error alone, and the manifest states that.

## Whole Check Suite

`make check`, every target the repository runs, exit status 0.

```text
670 passed in 0.72s
491 passed in 7.35s
corpus check: 220 fixture(s), 218 pass, 0 fail, 2 awaited, 0 unexpected pass
smoke check: prosiform installs into an environment and bundles a reference from a source root, resolved by name outside the repository
layout check: 3 tree(s) present
table check: 14 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 12 document(s) resolved
vocabulary check: 35 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 23 source(s)
invocation check: 27 statement(s) of the documented invocation, each held to the build PROSIFORM_BUILD names
All checks passed!
```

## Observations

- **A publication failure is declarable without touching the host.** The refusal is a path the fixture does not hold rather than a permission, an ownership or a device, so the fixture states the same run on any filesystem and leaves nothing behind.
- **The entry-destination warning belongs to a published bundle.** A run that fails before publication emits its error and nothing else, which the delivery family now states in two ways: a run that publishes no bundle, and a run whose destination refuses it.
- **The error catalogue's coverage closed in one row.** The two codes the issue listed as arriving with other rows had already arrived, so this row's measurement found three gaps rather than five.

## Limitations

- **Two codes are declared and not yet run.** `E_SOURCE_CHANGED` and `E_UNEXPECTED_INTERNAL_ERROR` are stated by fixtures no build has been held to. The criterion asks for the declaration, and the run awaits `I00:E11:W24`.
- **The marked fixtures state severity and code, and for the changed source its reference.** Neither states the message, the chain or the remedy, because no run has produced one to hold a build to. The row that lifts the markers is where those are added.
