# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w16`, branch `i02/e00/w16-root-bounds-only`, cut from `i02/e00/main` at `f5038166`, `0d3e0cff` and `8040ab68` merged in; validated at `837f7045`.
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`.
- Design: `artifacts/planning/2026-10-17-prosiform-v1/design.md` at `9d6d9731`, as `README.md` pins it.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 252 fixture(s), 252 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build | 0 |
| `make conformance` | 288 clause(s), 55 covered by no fixture, 0 declaration(s) naming no clause; 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere | 0 |
| `make independence` | every word of every fixture declaration and every report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 37 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1065 passed | 0 |
| `make harness` | 614 passed | 0 |
| `make smoke` | installed command bundles and publishes derived names from outside the repository | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 64 files already formatted | 0 |
| `make typecheck` | no issues found in 63 source files | 0 |
| `make check` | **not run**, as the brief directs | — |

`make independence` first failed on two words of rewritten descriptions (`deepest`, `ahead`); both were reworded.

## Re-record diff check

Every fixture was run against the build and each stdout difference line-diffed with the recorded bytes. A line passed when it was a heading whose text changed from a title-cased path to a source H1 or a title-cased path, a heading removed (absorbed title or former ancestor), a heading level change, or a line equal once every `](#...)` destination is blanked. 13 existing fixtures passed and were written. The rest of the flagged items were the fixtures whose sources this task changed or added (`depth-overflow/a-source-heading-the-shift-places-at-the-sixth`, `identity/paths-differing-only-by-suffix`, two new fixtures) and three usage-example headings the script could not read through the `source` link (`Propose Mode`, `Sync Mode`, `Understand Mode`, each the mode's H1, checked by hand).

## Search

- `root-relative`, `effective-root-relative`, `relative to its effective root`, `own root`, `title the path`, `path already names` in the task branch: only the leading-slash reference sense (`/x.md`), a synthetic help text in `checks/tests/test_invocation.py`, and fixture source prose.
- `design.md` at `9d6d9731`: no `root-relative`, `filename H1` or `filename heading`.
