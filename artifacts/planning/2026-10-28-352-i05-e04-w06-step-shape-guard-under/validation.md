# Validation — I05:E04:W06

The checks the W06 work item names, run on the task branch `i05/e04/w06-step-shape-guard-under` at `86a82cc0841336ce5867b7a4bdba7ef9b1e25464`, cut from `i05/e04/main` at `f4ad4b34`. Each ran in the task worktree with `PROSIFORM_BUILD` naming that worktree's own `pf` through `uv run --project <worktree>/src --frozen pf`.

## Guard Tests

`checks/tests/test_steps.py`, 12 cases. Observes AC6. Result: ✓, 12 passed.

- **Passing corpus.** A mode procedure and an artifact operation written as step sub-sections, with a child section's steps one level below it, report nothing.
- **Numbered step.** `1. Fetch the issue.` and `2. Save it.` at column 0 under `## Procedure` fail as `mode.md:5` and `mode.md:6`.
- **Code blocks.** A numbered list inside a fenced block, inside an indented block, and nested under a bullet reports nothing.
- **Depth.** `#### 1. Select` under `## Procedure` fails as two levels below its parent; a step after a deeper non-step heading reads its procedure as its parent and passes.
- **Duplicates.** `### 1. Select` twice in one document fails on the second, naming the first's line; the same heading in two documents passes.
- **Not a step.** `#### 2026 Plan` carries no full stop and is no step heading.
- **Scope and corpus.** The scope is every tracked document under `example/work-planner/`, and each of them meets the convention.

## Step Check on the Corpus

`make steps` on the converted corpus. Result: ✓.

```text
step check: every procedure in 58 document(s) under example/work-planner/ writes its steps as sub-sections
```

## Step Check on a Planted Step

`1. Fetch the issue.` appended to `example/work-planner/artifacts/board.md`, run, then reverted; never committed. Observes AC6 end to end. Result: ✓, exit 2 from `make`.

```text
FAIL example/work-planner/artifacts/board.md:449 — a numbered list item; write each step as an 'N. Action' heading one level below its procedure

step check: 1 place(s) breaking the step convention
make: *** [Makefile:100: steps] Error 1
```

## Command Table

`make tables`. Result: ✓.

```text
table check: 18 command(s) and 8 declaration(s), each declared by the project and named by a table
```

## Repository Checks

`make check`, exit 0. Result: ✓.

- `make lint`, `make format-check`, `make typecheck`: clean, 66 source files type checked.
- `make test`: 1281 passed. `make harness`: 732 passed.
- `make corpus`: 335 fixtures, 335 pass, 0 fail, 0 awaited.
- `make smoke`, `make layout`, `make tables`, `make links` (106 documents), `make vocabulary`, `make invocation`, `make conformance`, `make independence`: each passed.
- `make steps`: 58 documents.

`i05/e04/main` moved to `aa826060` before the merge, carrying I05:E03 through `main`. The task branch merged it at `a869dfbf91df5f7f181494c36848f4b1cba7f09b` with no conflict, and `make check` ran again there, exit 0: `make test` 1302 passed, `make harness` 743 passed, `make corpus` 342 of 342 fixtures, every other check passed, and `make steps` passed over 58 documents.

## Scope Finding

The guard reads `example/work-planner/`, not all of `example/`. `example/my-skill/procedure.md` lines 7–8 write two numbered steps; it is the README's small demo skill, which E04 did not convert and the repository README's diagram example uses. Every other document under `example/` already passes: run over all of `example/`, the rules find those two lines and nothing else. The change list holds the AC6 wording question.
