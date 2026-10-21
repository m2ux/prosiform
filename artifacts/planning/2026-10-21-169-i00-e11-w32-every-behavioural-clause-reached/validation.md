# Validation

The checks this work runs, the revisions they ran against, and what each reported.

Every run below is `make`, with `PROSIFORM_BUILD` naming the build in the same checkout, as the corpus and invocation targets require.

## The Figure and Why It Moved

Issue [#169](https://github.com/m2ux/prosiform/issues/169) states 253 clauses, 66 reached by no fixture, 57 of them gaps against 9 non-behavioural sections. Measured on this unit's own base, `i00/e11/main` at `8cd9534`, the report closes:

```text
conformance report: 253 clause(s) the design states, 64 covered by no fixture,
0 declaration(s) naming no clause; 30 declared name(s) reached, 0 unfixturable,
3 installation claim(s) no run observes
```

Two figures moved.

- **66 to 64.**
  W24 and W30 and the merge of `main` into the epic base each brought fixtures declaring clauses nothing had declared, so two clauses left the list before this unit began.

- **9 to 11 non-behavioural.**
  Each of the three sections that state no behaviour is itself a clause beside the rules under it: `Design status` is one, `Implementation verification and residual policy detail` is one and carries four, and `Upstream follow-up reference` is one and carries four. The behavioural remainder is 53, not 57.

The branch's own report closes:

```text
conformance report: 242 clause(s) the design states, 0 covered by no fixture,
0 declaration(s) naming no clause; 30 declared name(s) reached, 0 unfixturable,
0 declared code(s) the build reports nowhere,
0 reported code(s) the contract declares nowhere,
16 clause(s) no run states, 3 section(s) stating no behaviour,
3 installation claim(s) no run observes
```

The epic base carried two further merges while this work ran, W35 and W33, each
of which states part of the same report. Both are merged into this branch and
the figures above are read after them: the declared surface now carries the
codes the build reports for itself, the installation claims name the smoke-run
property that would observe them, and the two groups this unit adds are counted
beside them.

The clause total falls by eleven because a section stating no behaviour carries no clause, it or the rules beneath it. The uncovered list empties: sixteen clauses are recorded with the reason no source tree and one invocation can state them, thirty-three gain the declaration of the fixture that already established them, and four gain a fixture.

## Base Conformance

`make check` on the base, `8cd9534`, in a detached worktree of its own, exits 0. Its conformance target prints the first summary above. The run's other summaries:

```text
corpus check: 233 fixture(s), 233 pass, 0 fail, 0 awaited, 0 unexpected pass
independence check: 60 term(s), named by no fixture declaration, no report entry and no name the contract declares
vocabulary check: 35 contract term(s) marked in the design, every one defined in docs/glossary.md
invocation check: 28 statement(s) of the documented invocation
table check: 16 command(s) and 7 declaration(s)
link check: every reference in 12 document(s) resolved
layout check: 3 tree(s) present
```

The base result is therefore attributable: every figure below that differs from one of these is this branch's.

## Branch Conformance

`make check` on the branch at `680e4a4` exits 0. The conformance target prints the second summary above, and its uncovered list is empty:

```text
# Uncovered clauses

# Unnamed declarations
```

Both criteria are read from that list. Every behavioural clause is reached by a fixture or recorded with its reason, and no section stating no behaviour appears in it.

## Corpus

```text
corpus check: 237 fixture(s), 236 pass, 0 fail, 1 awaited, 0 unexpected pass
```

Four fixtures join the corpus. Three hold against the build. The fourth, `profile/the-constructs-the-profile-supports`, awaits [I00:E11:W37](https://github.com/m2ux/prosiform/issues/181): the autolink it carries ends the run in an internal error, which the corpus had never run and which that row delivers. Its failure leaves the run green, and a run in which it meets its manifest fails instead, so the marker is lifted on the change that makes it untrue.

## Independence

```text
independence check: 60 term(s), named by no fixture declaration, no report entry and no name the contract declares
```

The check scans the rendered report whole, so the sixteen recorded reasons and the three section reasons are held to it. None names an implementation language or runtime, the machinery of modules and packaging, a source file of an implementation or the wording a build gives its own fault, although the design states two of those names in the very sections being recorded.

## Vocabulary

```text
vocabulary check: 35 contract term(s) marked in artifacts/planning/2026-10-17-prosiform-v1/design.md on origin/engineering, every one defined in docs/glossary.md, and every definition carried by the contract across 23 source(s)
```

Unchanged from the base: nothing this branch writes introduces a contract term.

## Harness

```text
587 passed
```

Five cases join `checks/tests/test_conformance.py`, over a design carrying one section that states no behaviour and one clause no run states: the inventory omits the silent heading and the rule beneath it, each section is listed with its reason, a recorded clause stays in the mapping and leaves the uncovered list, each recorded clause is listed with the reason and what states it in its place, and the closing line counts both groups beside the installation claims. The sixth change extends the existing inventory case with the four clauses the design gains.

## Check

`make check` runs lock-check, lint, format-check, typecheck, test, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence, stopping at the first failure. On the branch at `680e4a4` it exits 0.

```text
All checks passed!
Success: no issues found in 53 source files
696 passed
587 passed
corpus check: 237 fixture(s), 236 pass, 0 fail, 1 awaited, 0 unexpected pass
smoke check: the installed command is named on the path, independent of the working directory, independent of this repository
table check: 16 command(s) and 7 declaration(s), each declared by the project and named by a table
link check: every reference in 16 document(s) resolved
invocation check: 29 statement(s) of the documented invocation, each held to the build PROSIFORM_BUILD names
```
