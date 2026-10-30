# Validation — I05:E06 W10

> Test evidence · Created 2026-10-29

## Revision

| Revision | Meaning |
| --- | --- |
| `cdcc91e2` | Head of `i05/e06/w10-authoring-guard-under-make` these runs were made on |
| `2602d454` | Epic base `i05/e06/main`, the W09 merge this branch was cut from |

Every run below used `UV_CACHE_DIR=/tmp/w10-uv` and, where the check reads a
build, `PROSIFORM_BUILD="uv run --project <worktree>/src --frozen pf"`. The
link check and the smoke run reached the network.

## Wiring

### `make tables` — the row `make tables` requires

The command table in `checks.md` now carries a `make authoring` row, so the
two-direction comparison holds: every `Makefile` target is named by a table
and no row names a target the `Makefile` does not declare.

```text
table check: 19 command(s) and 8 declaration(s), each declared by the project and named by a table
```

Before the row was added the same run failed with `make authoring — the
Makefile declares it and no command table names it`, which is why the row and
the wiring landed in one commit.

### `make check` runs the authoring check

`check` names `authoring` last in its prerequisite list, after `steps`. The
full run reaches it:

```text
python3 checks/authoring.py
authoring check: 59 document(s) under example/work-planner/
...
authoring check: 0 finding(s)
```

`make check` exited `0` on `cdcc91e2`.

## Guard Bites

A tick that the target is wired in does not show the guard works, so a rule
was broken in a real example file and the failure observed.

**What was broken.** `example/work-planner/protocols/task-merge.md` gained a
`## Commands` section holding an `### Merge the Pull Request` operation and a
fenced `gh pr merge` command ahead of its steps — two rules at once.

**Why that file.** The usage-example fixtures point at the example tree
through a `source` symlink, so `make corpus` compares every file a fixture's
closure reaches. A break in a reached file fails `corpus`, which runs before
`authoring`, and `make check` stops there without showing the authoring
verdict. `task-merge.md` is reached by no fixture, so the break reaches the
authoring check. The earlier attempt against `board.md` failed at `corpus`
for exactly this reason and is recorded here because it is the reason the
demonstration file was chosen.

**Observed failure**, from `make check` on the broken tree:

```text
protocols: 2 finding(s)
  example/work-planner/protocols/task-merge.md:13 — Commands section: a 'Commands' heading; no file has a Commands section
  example/work-planner/protocols/task-merge.md:19 — Command placement: a command sits outside a step, under 'Merge the Pull Request'; a command sits in an unindented fenced block in the step that runs it

  area         Inputs and Outputs | Commands section | Command placement | File-relative links
  protocols    0 | 1 | 1 | 0

authoring check: 2 finding(s)
make: *** [Makefile:108: authoring] Error 1
```

`make check` exited `2`. The failure names the file, the line and the rule
for each finding, and the target that failed.

**Restored** with `git checkout -- example/work-planner/protocols/task-merge.md`;
`git status --short` was empty afterwards and the same `make check` exited
`0` with `authoring check: 0 finding(s)`.

## Test Plan

| Check | Command | Result |
| --- | --- | --- |
| Lockfile | `make lock-check` | pass — `Resolved 24 packages` |
| Lint | `make lint` | pass — `All checks passed!` |
| Format | `make format-check` | pass — `69 files already formatted` |
| Types | `make typecheck` | pass — `Success: no issues found in 68 source files` |
| Build suite | `make test` | pass — `1302 passed` |
| Check suite | `make harness` | pass — `771 passed` |
| Corpus | `make corpus` | pass — `342 fixture(s), 342 pass, 0 fail, 0 awaited, 0 unexpected pass` |
| Smoke | `make smoke` | pass — wheel built and installed, `pf` resolved outside the repository |
| Layout | `make layout` | pass — `3 tree(s) present` |
| Tables | `make tables` | pass — `19 command(s) and 8 declaration(s)` |
| Links | `make links` | pass — `every reference in 107 document(s) resolved` |
| Vocabulary | `make vocabulary` | pass — `44 contract term(s)`, every one defined |
| Invocation | `make invocation` | pass — `29 statement(s)` held to the build's help |
| Conformance | `make conformance` | pass — 303 clause(s), 55 covered by no fixture, 0 declared code the build reports nowhere |
| Independence | `make independence` | pass — every word of every declaration and report entry is one the contract states |
| Steps | `make steps` | pass — `59 document(s)` |
| Authoring | `make authoring` | pass — `0 finding(s)` across 59 documents |
| End to end | `make check` | pass — exit `0`, having run `authoring` |

`make render` was not run: it needs mermaid-cli and a headless browser, it
sits outside `make check` by design, and this task's criteria do not reach it.

## Criteria

### AC11 — every cross-file link is file-relative

Observed by `make links` (107 documents resolved) and by `make authoring`
(`0 finding(s)`, so no link in the example is absolute, a repository URL to a
held file, or written from the declared root). Both pass.

### AC12 — `make check` runs the authoring check and fails on a breaking file

Observed three ways:

- the full `make check` run reaches `authoring` and exits `0` clean;
- the demonstrated break exits `2` with the finding naming
  `example/work-planner/protocols/task-merge.md` and the rule it breaks;
- `checks/tests/test_authoring_check.py` holds the verdict as a test:
  `test_the_check_fails_naming_the_file_that_breaks_a_rule` asserts
  `main()` returns `1` and prints the offending path, and
  `test_the_check_passes_on_a_file_meeting_every_rule` asserts `0`.

### AC13 — the fixtures reproduce the converted example's bundles

Observed by `make corpus`: 342 fixtures, 342 pass. The two fixtures that
compile the example tree through its `source` symlink
(`a-mode-and-the-board-reads-it-steps-through` and
`a-procedure-and-everything-it-reaches`) reproduce their expected bundles byte
for byte.

## Rule Coverage

`checks/tests/test_authoring_check.py` gained thirteen cases. Each rule the
check enforces, and the case that fails on it:

| Rule | Failing case |
| --- | --- |
| Inputs and Outputs | prose Inputs and a missing Outputs line; a missing Inputs beside an Outputs line; both lines after the first step; a link without a contract section; one link of a pair without one; Inputs running onto a second line |
| Commands section | a section holding a command; a section holding none; a heading written with emphasis |
| Command placement | a command in a step's fence (no finding); an indented fence; a command under `Fields`; a command in the preamble; a command ahead of an operation's steps; a tilde fence; a non-shell fence (no finding); a command fence inside a template fence (no finding) |
| File-relative links | an absolute path; a path resolving only from the declared root; a repository URL to a held file; a reference definition carrying an absolute path; a link with no path part (no finding); a link in literal content (no finding) |
| Verdict | the check fails naming the file; the check passes on a clean file |
| Report | the size report at either limit; each document falling in one area |

The suite went from 15 to 28 cases; `make harness` passes.
