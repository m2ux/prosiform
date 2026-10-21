# Validation — I00:E10:W02

Every run below was made unsandboxed from the worktree `.worktrees/i00-e10-w02`, with the build under test named by

```bash
PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform"
```

## The base measured first

`make check` at the epic base `fc8e285` returns 0, so a result on the branch is attributable to the branch. Its harness suite is 532 tests and its corpus run reports 231 fixtures, 229 passing and 2 awaited.

## The repository check set

`make check` on `i00/e10/w02-clause-to-fixture-mapping` returns 0. Each of its fourteen targets passes: the lock check, lint, format check, type check, the build's own suite of 682 tests, the harness suite of 541, the corpus, the smoke run, and the layout, table, link, vocabulary, invocation and conformance checks.

```text
corpus check: 231 fixture(s), 229 pass, 0 fail, 2 awaited, 0 unexpected pass
```

The corpus is unchanged in what it runs: this row rewrites the `clauses` of 120 manifests and nothing else about them, so the fixture count, the passes and the two awaited fixtures are the base's figures.

`make tables` is what holds the new target to its documentation in both directions, and `make links` resolves the corpus guide's new section link.

## The conformance suite

`make harness` grows by the nine cases of `checks/tests/test_conformance.py`, which supply the report a design and a corpus of their own rather than the repository's, so each case states what the report reads rather than what this repository happens to hold.

- The design states a clause in every form the reader recognises — a heading, a bold-led bullet, a numbered step, a table row — and a bullet inside a fenced block that is an example rather than a rule. The reader returns the ten clauses that design states and not the eleventh.
- A clause the corpus names carries the identity of the fixture naming it, and a clause named with a case after the comma carries that fixture too.
- A clause no fixture names appears in the uncovered list, and one a fixture names does not. This is the report run against a deliberately unfixtured clause: the design states `Resource limits — --max-links` and `Entry line — Order`, the corpus names neither, and both are listed.
- A declaration naming no clause the design states is reported against the fixture carrying it and fails the report.
- An error code and an exit status a fixture reaches carry that fixture; one only a fixture awaiting later work declares is unfixturable and carries the work it awaits; one no fixture declares at all fails the report.
- The report rendered twice from one design and one corpus is identical, so the generated mapping is reproduced on a second run.

## The conformance report

`make conformance` returns 0 over this repository's design and corpus:

```text
conformance report: 253 clause(s) the design states, 66 covered by no fixture,
0 declaration(s) naming no clause; 27 declared name(s) reached, 3 unfixturable
```

**The mapping.** Each of the 253 clauses is listed with the fixtures naming it, 187 of them with at least one. The identities are the fixtures' own paths under `fixtures/`, so a clause is read back to the directories that exercise it.

**The uncovered list.** 66 clauses are named by no fixture. Nine of them are the design's own non-behavioural sections — `Design status`, `Implementation verification and residual policy detail` and `Upstream follow-up reference` with their bullets — which no run can exercise. The rest are gaps in the corpus, and `Adversarial acceptance fixtures — Consistency` and `Adversarial acceptance fixtures — Parser exhaustion` among them are the two families [W01](https://github.com/m2ux/prosiform/pull/166) left held by nothing, so the report reproduces the family listing that row used until it existed.

**The declared surface.** Every error code, warning code and exit status the contract declares is declared by a fixture. Three are declared only by a fixture awaiting later work and are listed as unfixturable with that work as the reason:

```text
exit status 4: unfixturable, awaiting I00:E11:W24
error E_SOURCE_CHANGED: unfixturable, awaiting I00:E11:W24
error E_UNEXPECTED_INTERNAL_ERROR: unfixturable, awaiting I00:E11:W24
```

Exit status 4 and `E_UNEXPECTED_INTERNAL_ERROR` are what [AC8](https://github.com/m2ux/prosiform/issues/9) places with W05, and the installation claims AC7 places with W04 are not a code or a status, so neither row's entries are delivered here. The listing names what the corpus reaches and leaves the shape of their entries to them.

## What the validation found

- **66 clauses of the design are reached by no fixture.** The report is what makes the figure readable, and closing it is the work of the epics that own those clauses rather than of this row. Non-trivial and blocking nothing here, so it is deferred.
- **A code the build emits outside the corpus is held to nothing.** The schema's catalogues are the design's codes and the corpus runner compares every diagnostic a fixture's run emits, so within the corpus the codes the build emits are the codes the design declares. A code a build emits on a path no fixture reaches is observed by neither. Non-trivial and blocking nothing here, so it is deferred.
- **The design's non-behavioural sections read as uncovered clauses.** Nine entries of the uncovered list are sections that state no behaviour a run can produce. The reading is correct — nothing exercises them — and separating them would mean the design marking which of its sections bind a build, which is a change to the contract rather than to the report.

## What could not be ticked

**AC2, AC3 and AC5 are ticked.** The mapping carries every clause the design states with the fixtures exercising it; a clause no fixture names is listed as uncovered, as the suite's deliberately unfixtured clause shows; and the declared surface lists every code and status the contract declares, with the three no run of the corpus reaches named unfixturable and the work each awaits as the reason.

**AC1 stays unticked**, which is [W01](https://github.com/m2ux/prosiform/pull/166)'s reading unchanged. The report now emits the family listing that row's script stood in for, and it reports the same two families held by nothing: Consistency and Parser exhaustion, each a tracked row.
