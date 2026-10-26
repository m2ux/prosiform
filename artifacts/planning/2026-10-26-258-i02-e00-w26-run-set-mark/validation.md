# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w26`, branch `i02/e00/w26-run-set-mark`, cut from `i02/e00/main` at `2ff72d16`; validated at `dae3a084`; merged into `i02/e00/main` as `e8b938de`.
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`.
- Design: `artifacts/planning/2026-10-17-prosiform-v1/design.md` at `dc2e172f`, as `README.md` pins it.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 279 fixture(s), 279 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build | 0 |
| `make conformance` | 296 clause(s), 55 covered by no fixture, 0 declaration(s) naming no clause; 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere | 0 |
| `make independence` | every word of every fixture declaration and report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 41 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1141 passed | 0 |
| `make harness` | 651 passed | 0 |
| `make smoke` | installed command named on the path, independent of the working directory and the repository | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 68 files already formatted | 0 |
| `make typecheck` | no issues found in 67 source files | 0 |
| `make check` | **not run**, as the brief directs | — |
| CI (`Checks`) on `dae3a084` | success | — |

The first `make independence` failed on `dispatch/a-link-carrying-both-operators`: its description used "wait", which the reworded one-operator clause no longer states. The description was reworded before the corpus commit.

## Work-planner bundles

All ten `example/work-planner/modes/*.md` bundles were built from `example/work-planner`, once with the base build (`2ff72d16`) and once with this branch. `diff -r` reports them byte-identical, and no source there carries `⫽`.
