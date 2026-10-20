# Validation

The checks this row was held to, the revision they ran at, and what they observed.

## Revision

The branch `i00/e11/w02-a-corpus-fixture-declaring`, cut from `i00/e11/main` at `9ffb716`. Every run below invoked the Makefile target a developer and continuous integration both call, from the repository root of the task worktree, with `PROSIFORM_BUILD` naming the locked build's console entry point.

## Coverage Measured

The warning catalogue the schema enumerates, read against the codes the corpus's manifests declare.

| Warning | Fixtures declaring it | Of those, awaiting later work |
| --- | --- | --- |
| `W_EMPTY_GROUP_RULE` | 1 | 1, `grouping/a-rule-matching-no-document-in-the-closure`, awaiting `I00:E11:W14` |
| `W_ENTRY_DESTINATION` | 168 | 2 |
| `W_RESOURCE_PORTABILITY` | 5 | 1 |

Every warning the design declares is carried by a manifest, so the invariant holds at this revision and the work of the row is the check that keeps it holding.

The same measurement over the error catalogue found five codes no manifest declares: `E_ROOT_NOT_FOUND`, which `I00:E11:AC5` carries; `E_PARSER_REFERENCE_LIMIT`, which `I00:E11:AC15` carries; and `E_PUBLICATION_FAILED`, `E_SOURCE_CHANGED` and `E_UNEXPECTED_INTERNAL_ERROR`, which no row covers. The last three are deferred: the coverage they need is a fixture apiece for a failed publication, a source that changed mid-compilation and an internal error, which is a work item of its own rather than this row's.

## Harness Suite

`make harness`, the corpus's own checks, which carry the coverage assertion.

```text
380 passed in 6.33s
```

`test_every_warning_the_design_declares_is_declared_by_a_fixture` is among them. It subtracts the codes the corpus's manifests declare from the warning catalogue and requires the difference to be empty, naming any code the corpus leaves unstated.

The assertion was exercised against a corpus that fails it: the fixture tree was copied, `grouping/a-rule-matching-no-document-in-the-closure` removed from the copy, and the coverage read against that copy.

```text
catalogue: ['W_EMPTY_GROUP_RULE', 'W_ENTRY_DESTINATION', 'W_RESOURCE_PORTABILITY']
declared by the corpus: ['W_EMPTY_GROUP_RULE', 'W_ENTRY_DESTINATION', 'W_RESOURCE_PORTABILITY']
unstated: []
with that fixture removed, unstated: ['W_EMPTY_GROUP_RULE']
```

A warning losing its only fixture is therefore reported rather than passing in silence, which is what makes the green run above a statement.

## Corpus Run

`make corpus`, the whole corpus against the build under test.

```text
corpus check: 203 fixture(s), 201 pass, 0 fail, 2 awaited, 0 unexpected pass
```

The run names a fixture for each declared warning:

```text
grouping/a-rule-matching-no-document-in-the-closure: awaited, awaiting I00:E11:W14
traversal/a-relative-resource-warns: pass
```

`traversal/a-relative-resource-warns` declares `W_RESOURCE_PORTABILITY` and `W_ENTRY_DESTINATION` together on a successful run, and `grouping/a-rule-matching-no-document-in-the-closure` declares `W_EMPTY_GROUP_RULE`. The grouping fixture carries `awaiting`, so the corpus reports it as awaiting the row that delivers the warning and the run stays green. The declaration is the corpus's whatever the build currently produces, which is why the criterion is met by the fixture carrying the code rather than by the run passing: `I00:E11:AC16` carries the delivery of that warning, and neither row waits on the other.

## Repository Check Suite

`make check`, the full pass over the repository: the lock check, lint, formatting, type checking, the build's tests, the harness, the corpus, the smoke test, the layout, table, link and vocabulary checks and the documented invocation.

The run reached its last target and passed:

```text
link check: every reference in 12 document(s) resolved
vocabulary check: 34 contract term(s) marked … every one defined in docs/glossary.md
invocation check: 27 statement(s) of the documented invocation, each held to the build PROSIFORM_BUILD names
```

The link check ran online and resolved the references the two READMEs carry, which is what holds the documentation this change edits.

## Review

- The declared-code reading takes a code from a manifest alone, so a fixture added anywhere is counted by being a fixture and no list of codes sits beside the corpus.
- A fixture awaiting later work is counted, so the check does not make this row wait on the rows that deliver the warnings.
- The error catalogue's coverage is left to the rows that carry it, so the check states only what its criterion states.
