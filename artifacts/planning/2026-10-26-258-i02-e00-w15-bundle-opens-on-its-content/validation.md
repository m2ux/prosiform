# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w15`, branch `i02/e00/w15-bundle-opens-on-its-content`, cut from `i02/e00/main` at `ad8f1a2a`, `6c51fe55` merged in; validated at `6b0d0473`.
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`.
- Design: `artifacts/planning/2026-10-17-prosiform-v1/design.md` at `f2ce75c7`, as `README.md` pins it.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 250 fixture(s), 250 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build | 0 |
| `make conformance` | 288 clause(s), 55 covered by no fixture, 0 declaration(s) naming no clause; 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 37 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1059 passed | 0 |
| `make harness` | 612 passed | 0 |
| `make smoke` | the installed command is named on the path, independent of the working directory, independent of this repository | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

`make independence` first failed on three words the removed Entry line and generated-input sections stated (`remainder`, `however`, `instruct`); they are registered in `docs/corpus-vocabulary.md`.

## Re-record diff check

Every fixture with an expected `stdout` file was run against the build and its output line-diffed with the recorded bytes. A difference passed only when it was one contiguous deletion of a paragraph opening `Follow [` and carrying `The other sections are material`, plus exactly one blank line, with nothing added. 175 passed and were written; 73 were unchanged; none differed otherwise.

## Search

- `entry sentence`, `entry line`, `The other sections are material`, `prosiform.dispatch`, `dispatch text`, `generated-input`, `entry declaration` (case-insensitive) in the task branch: one occurrence, the unknown-key fixture's expected message `unknown field prosiform.dispatch`.
- `design.md` at `f2ce75c7`: none.
