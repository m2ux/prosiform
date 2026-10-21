# Validation

The checks this row ran, the revision they ran against, and what each observed.

## Revision

- **Branch.** `i00/e12/w03-a-reference-under-the`, cut from `i00/e12/main` at `ea4227c`, the merge of [#138](https://github.com/m2ux/prosiform/pull/138).
- **Build under test.** The build this change produces, reached through its console entry point from the branch's own environment.
- **Commands.** Each is a named target of the repository's `Makefile`. A local run reaches the same tools directly, because the sandbox this session runs in carries no writable package cache; the targets needing one are read from the repository's own workflow, which runs `make check` on every push to this branch.
- **The base did not move.** `i00/e12/main` stood at `ea4227c` when the branch was cut and when it was pushed, so the suites below ran against the base the merge targets. `W02` had not merged, which is what leaves the deferred half of the criterion to it.

## Unit suite

`make test` — 623 tests, all passing. 621 of them stood before this row; the 2 added observe the criterion through the command.

- **AC5, a reference naming no document.** `test_a_reference_under_the_root_naming_no_document_publishes_nothing` writes a source citing two documents under the root, one of which the root does not carry. The run returns the input-failure status, its first diagnostic is `E_TARGET_NOT_FOUND` naming the reference that resolved nowhere, and standard output is empty. The sibling reference resolves and is read, so the empty bundle is observed against material the run had already taken in rather than against a run that read nothing.
- **AC5, a reference naming no heading.** `test_a_reference_under_the_root_naming_no_heading_publishes_nothing` writes a source citing a document the root carries, naming a heading that document does not. The run returns the input-failure status, the diagnostic is `E_TARGET_NOT_FOUND` with the document it resolved to, and standard output is empty.
- **No mark is written in either.** Both sources carry ordinary links, so what fails the run is where the reference resolves and nothing else.

## Corpus

`make corpus` — 206 fixtures, 204 passing, 0 failing, 2 awaiting later work, 0 passing while awaiting it. The two awaiting fixtures are the ones the corpus already carried: `reference/a-link-inside-image-alternative-content` awaits `I00:E11:W10` and `grouping/a-rule-matching-no-document-in-the-closure` awaits `I00:E11:W14`. The base carried 204 fixtures and 202 passing; this row adds two, both passing.

- **AC5, a reference naming no document.** `reference/a-reference-under-the-root-naming-no-document` declares a source citing `rules.md`, which the root carries, and `procedure.md`, which it does not. The declared result is exit status 1, an empty bundle, and one error diagnostic: `E_TARGET_NOT_FOUND`, the reference `procedure.md`, the location `guide.md:3`, and the chain `guide.md → procedure.md`. The run against the build produced exactly that.
- **AC5, a reference naming no heading.** `reference/a-reference-under-the-root-naming-no-heading` declares a source citing `procedure.md#review` against a document carrying `Steps` and `Record` and no `Review`. The declared result is exit status 1, an empty bundle, and one error diagnostic: `E_TARGET_NOT_FOUND`, the reference `procedure.md#review`, the resolved document `procedure.md`, the location `guide.md:3`, and the chain `guide.md → procedure.md#review`. The run against the build produced exactly that.
- **The rule stated where the criterion reads it.** Both fixtures sit in the `reference/` family beside `a-document-under-the-root-is-a-dependency` and `a-document-outside-the-root-is-text`, so the three cases position creates are declared together. The families that raised the code on the way to another subject — `delivery/a-failing-run-publishes-no-bundle`, `extraction/a-heading-only-in-a-code-example`, `identity/an-ordinal-names-no-source-heading`, `validation-scope/the-sibling-once-closure-includes-it`, `diagnostics/a-failure-two-hops-from-the-entry-reference` — each still passes and still declares its own clause.

## Repository checks

Each ran against the same revision.

| Command | Result |
| --- | --- |
| `make lint` | All checks passed |
| `make format-check` | 45 files already formatted |
| `make typecheck` | no issues in 44 source files |
| `make layout` | 3 trees present |
| `make tables` | 14 commands and 7 declarations, each declared and named |
| `make vocabulary` | 34 contract terms, every one defined in the glossary |
| `make invocation` | 27 statements of the documented invocation held to the build |
| `make harness` | 381 passing and the one failure the base carries, below |
| `make lock-check` | read from the branch's workflow run |
| `make links` | read from the branch's workflow run |
| `make smoke` | read from the branch's workflow run |

The last three reach a package cache or the network, which this session's sandbox makes read-only and offline. They are the repository's own workflow's to run, and it runs `make check` over every push to this branch, so the branch's run is the record of them.

## The catalogue check

`make harness` reports 381 passing and one failing:

```text
FAILED checks/tests/test_catalogue.py::test_a_catalogue_is_the_codes_the_design_declares[error-E_]
  Extra items in the left set: 'E_SELF_REFERENCE', 'E_MARKED_RESOURCE'
```

**It fails on the base this row was cut from, before any change of this row**, and it is the same failure, naming the same two codes, that [`W01`'s record](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-21-136-i00-e12-w01-classification-by-where-a/validation.md) dated to the base. The check derives the manifest schema's error catalogue from the design on the `engineering` branch, and [D59](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) withdrew both codes from the design when it landed. The schema still enumerates them because the build still raises them: `E_MARKED_RESOURCE` is retired by `W04` and `E_SELF_REFERENCE` by `W05`. The check turns green on the row that removes the code the design no longer declares. This row changes neither code and adds no diagnostic.

## What this row does not observe

The criterion reads *whether it is compiled or deferred*, and this build has no deferral: after `W01` the mark selects nothing, so a marked reference is a compiled one. A fixture writing a mark would therefore observe the compiled path under a deferred name, which is why neither fixture writes one and why the Test Plan carries a row with no check against the deferred shape.

`W02` gives the mark its deferring meaning. The design requires a deferred link's target to exist — the reference is resolved and the document and heading it names confirmed, without the document being opened or bundled — so the deferred shape is stated once that rule is in the build, and `W08` reads the criterion whole.
