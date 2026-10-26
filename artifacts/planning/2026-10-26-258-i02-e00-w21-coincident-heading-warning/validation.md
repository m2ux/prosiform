# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w21`, branch `i02/e00/w21-coincident-heading-warning`, cut from `i02/e00/main` at `b46b1bf4`; validated at `6704ba46`.
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`.
- Design: `artifacts/planning/2026-10-17-prosiform-v1/design.md` at `05057116`, as `README.md` pins it.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 253 fixture(s), 253 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | documented invocation held to the build | 0 |
| `make conformance` | 288 clause(s), 55 covered by no fixture, 0 declaration(s) naming no clause; 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere | 0 |
| `make independence` | every word of every fixture declaration and report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 38 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1073 passed | 0 |
| `make harness` | 615 passed | 0 |
| `make smoke` | installed command named on the path, independent of the working directory and the repository | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

## Corpus re-run

Before the corpus edits, the build failed exactly three fixtures: `grouping/two-members-whose-paths-differ-only-by-suffix` (exit 1 expected, 0 produced; warning in place of the error), `identity/two-documents-sharing-a-title` and `identity/paths-differing-only-by-suffix` (an undeclared warning). No expected bundle other than the member fixture's (previously empty) changed.

## Work-planner bundles

All ten `example/work-planner/modes/*.md` bundles build with exit 0 and an empty stderr: no `W_COINCIDENT_HEADING`.
