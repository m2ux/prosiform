# Validation — W07

> Evidence · Created 2026-10-31

## What was observed before the fix

Both defects were reproduced on `i07/e00/w07-make-the-cursor-harness` at `23882b7d`, before any edit.

### AC15 — the Cursor matrix crashes on a default run

`run.matrix(corpus, ["m"], list(FORMS), 1, HARNESSES["cursor"])` raised before building a single session:

```text
File "evals/diagram-following/run.py", line 332, in matrix
    if observable(workflow, scenario, form, harness)
File "evals/diagram-following/run.py", line 362, in observable
    section = sections_of(workflow, form)[state]
File "evals/diagram-following/workflow.py", line 977, in sections_of
    return workflow.sections[form if form in workflow.sections else TRANSITION[form]]
KeyError: 'bundle'
```

The runner's form names are `bundle`, `tree`, `prose`, `linked`, `compiled`, `authored`, `bootstrap`; the corpus's are `diagram`, `prose`, `linked`, `compiled`, `authored`, `bootstrap`. Every workflow-form pair the Cursor harness cannot observe early reached the lookup, and each raised:

| Workflow | Scenarios' form | Raised |
| --- | --- | --- |
| branching | `bundle` | `KeyError: 'bundle'` |
| branching | `tree` | `KeyError: 'tree'` |
| linear | `bundle` | `KeyError: 'bundle'` |
| linear | `tree` | `KeyError: 'tree'` |
| looping | `bundle` | `KeyError: 'bundle'` |
| looping | `tree` | `KeyError: 'tree'` |

The same call under `HARNESSES["claude"]` returned 28 sessions, because `Claude.nested_starts` is true and `observable` returns before the lookup. That is why the Claude matrix ran and the Cursor one did not.

### AC16 — the sub-agent trace is discarded

`keep()` globbed `f"{TRACE}*"`, which is `trace.log*`:

```text
TRACE constant: trace.log
glob the runner uses: trace.log*

Workspace holds: ['trace-review.log', 'trace.log']
Glob 'trace.log*' matches: ['trace.log']
Files kept: ['trace.log']
the sub-agent trace is kept: False
```

`trace.log*` matches `trace.log-review.log` and does not match `trace-review.log`. The instruction, `instruction-bootstrap.md` and `keep()`'s own docstring all state `trace-<section>.log`, so the file the agent is told to write is the one the glob cannot see.

The test that shipped beside the defect, `test_a_sub_agents_trace_is_kept_beside_the_dispatching_sessions`, **passed** at `23882b7d`. Its fixture named the file `trace.log-review.log`, the spelling the glob accepts, so the test asserted the glob rather than the instruction.

## Failing case, before and after

Each case was run with its repair reverted and then with it restored, in the worktree.

### AC15 — `test_the_cursor_harness_completes_a_matrix_over_the_default_forms`

Reverting only the `observable` lookup:

```text
FAILED evals/diagram-following/test_run.py::test_the_cursor_harness_completes_a_matrix_over_the_default_forms
  File "evals/diagram-following/run.py", line 333, in matrix
  File "evals/diagram-following/run.py", line 366, in observable
  File "evals/diagram-following/workflow.py", line 977, in sections_of
    return workflow.sections[form if form in workflow.sections else TRANSITION[form]]
KeyError: 'bundle'
1 failed
```

### AC16 — the stated trace name

Reverting only `TRACES` to `trace.log*`:

```text
FAILED test_a_sub_agents_trace_is_kept_beside_the_dispatching_sessions
FAILED test_a_scored_dispatch_keeps_the_sub_agents_trace_it_was_given
E   AssertionError: assert ['trace.log'] == ['trace-check.log', 'trace-work.log', 'trace.log']
E     Right contains 2 more items, first extra item: 'trace-work.log'
2 failed
```

Both pass with the repairs restored; the full suite below is the record of that.

## Test runs

| Run | Where | Result |
| --- | --- | --- |
| `pytest evals/diagram-following` at `23882b7d`, before any edit | worktree, sandbox | 209 passed |
| AC15 case, repair reverted | worktree, sandbox | 1 failed, `KeyError: 'bundle'` |
| AC16 cases, repair reverted | worktree, sandbox | 2 failed, `['trace.log']` where three traces were written |
| `pytest evals/diagram-following` after the repair | worktree, sandbox | 211 passed |
| `make harness` (`pytest checks/tests evals/diagram-following`) | worktree, sandbox | 992 passed |
| `ruff check` and `ruff format --check` over `evals` | worktree, sandbox | passed, 133 files formatted |
| `mypy` over `evals` | worktree, sandbox | passed, 11 source files |
| `make check` | worktree, sandbox | see below |

### `make check`

`make check` without `PROSIFORM_BUILD` stops at `make corpus`, which refuses to run without a build named:

```text
corpus check: PROSIFORM_BUILD names the build under test; a fixture has no result without one
make: *** [Makefile:85: corpus] Error 1
```

That is the check's own precondition, not a fault on the branch. With the build named as CI names it, the corpus-dependent targets run:

```text
PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make corpus invocation conformance independence
```

```text
ok   vocabulary  3284 term(s) ...
ok   corpus      349 fixture(s) and their identities
ok   report      the conformance report as it renders
independence check: every shaped term of every fixture declaration and every report entry is one the contract names
EXIT 0
```

Targets that had passed before `corpus` in the same `make check` invocation:

| Target | Result |
| --- | --- |
| `lock-check` | resolved 24 packages |
| `lint` | passed |
| `format-check` | 203 files already formatted |
| `typecheck` | 80 source files, no issues |
| `test` (`cd src && pytest`) | 1308 passed |
| `harness` | 992 passed |
| `authoring` | 0 findings |

The targets after `corpus` were run on the host, since `make links` reads the network:

```text
make links smoke layout tables vocabulary invocation conformance independence steps
link check: every reference in 237 document(s) resolved
smoke check: the installed command is named on the path, independent of the working directory, independent of this repository
layout check: 4 tree(s) present
table check: 21 command(s) and 8 declaration(s), each declared by the project and named by a table
vocabulary check: ok
invocation check: 29 statement(s) of the documented invocation, each held to the build PROSIFORM_BUILD names
conformance report: 303 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause
independence check: every shaped term of every fixture declaration and every report entry is one the contract names
step check: every procedure in 59 document(s) under example/work-planner/ writes its steps as sub-sections
EXIT 0
```

Every target of `make check` therefore passes on this branch.

## CI

`Checks` passed on `b1b7715d96319359962b3c586e54eaa2b8dee16b`, the branch head the pull request was raised from — the same commit this worktree holds. That run carries `test_linked_bootstrap` and the publication tests, which do not run in this sandbox.

## What was not proved here

- **The eval's own runs.** `make eval-diagrams` starts paid agent sessions against a real CLI and is not run by `make check`. AC15's case is the matrix construction the run performs, which is the site of the defect; no Cursor session was started in this sandbox, and the Cursor CLI is not installed here.
- **The `E_PUBLICATION_FAILED` and `test_linked_bootstrap` failures.** Both reproduce in this sandbox on every settled branch and pass in CI; the CI run above is the evidence that they pass with this change in place.
