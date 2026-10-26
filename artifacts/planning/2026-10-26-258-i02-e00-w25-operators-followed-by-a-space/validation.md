# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w25`, branch `i02/e00/w25-operators-spaced`, cut from `i02/e00/main` at `d56f3b2c`; validated at `30677e1d`; merged into `i02/e00/main` as `2ff72d16`.
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`.
- Design: `artifacts/planning/2026-10-17-prosiform-v1/design.md` at `2501b66d`, as `README.md` pins it.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 271 fixture(s), 271 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build | 0 |
| `make conformance` | 293 clause(s), 55 covered by no fixture, 0 declaration(s) naming no clause; 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere | 0 |
| `make independence` | every word of every fixture declaration and report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 39 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1101 passed | 0 |
| `make harness` | 641 passed | 0 |
| `make smoke` | installed command named on the path, independent of the working directory and the repository | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 66 files already formatted | 0 |
| `make typecheck` | no issues found in 65 source files | 0 |
| `make check` | **not run**, as the brief directs | — |
| CI (`Checks`) on `30677e1d` | success | — |

The first `make lint` failed on one docstring line over 88 characters in `closure.py`; the rewrap was folded into the source commit.

## Unspaced-mark audit

Every `¬` and `⇉` in `src`, `example`, `fixtures`, `docs`, `invocation.md` and `README.md` not followed by a space was listed. None in `example/` or `fixtures/` is link text: the only hits are code spans naming the mark. Unit tests carrying unspaced `¬` link text were rewritten with the space and pass unchanged.

## Work-planner bundles

All ten `example/work-planner/modes/*.md` bundles were built from `example/work-planner` with the base build (`d56f3b2c`) and with this branch; `diff -r` reports them byte-identical.
