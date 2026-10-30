# Validation

> Delivery Record · Created 2026-10-26

## Environment

- Worktree: `.worktrees/i02-e00-w24`, branch `i02/e00/w24-dispatch-depth-warning`, cut from `i02/e00/main` at `736a7d25`, with `da6d0515` merged; validated at `7dd08d95`.
- Build: `uv run --frozen --project <worktree>/src pf`, named as `PROSIFORM_BUILD`.
- Design: `artifacts/planning/2026-10-17-prosiform-v1/design.md` at `c20f550d`, as `README.md` pins it.

## Checks

| Check | Result | Exit |
| --- | --- | --- |
| `make corpus` | 269 fixture(s), 269 pass, 0 fail, 0 awaited, 0 unexpected pass | 0 |
| `make invocation` | 28 statement(s) of the documented invocation, each held to the build | 0 |
| `make conformance` | 293 clause(s), 55 covered by no fixture, 0 declaration(s) naming no clause; 0 declared code(s) the build reports nowhere, 0 reported code(s) the contract declares nowhere | 0 |
| `make independence` | every word of every fixture declaration and report entry is one the contract states | 0 |
| `make links` | every reference in 104 document(s) resolved | 0 |
| `make layout` | 3 tree(s) present | 0 |
| `make tables` | 16 command(s) and 8 declaration(s), each declared by the project and named by a table | 0 |
| `make vocabulary` | 39 contract term(s), every one defined in `docs/glossary.md` | 0 |
| `make test` | 1095 passed | 0 |
| `make harness` | 639 passed | 0 |
| `make smoke` | installed command named on the path, independent of the working directory and the repository | 0 |
| `make lint` | All checks passed | 0 |
| `make format-check` | 66 files already formatted | 0 |
| `make typecheck` | no issues found in 65 source files | 0 |
| `make check` | **not run**, as the brief directs | — |
| CI (`Checks`) on `7dd08d95` | success | — |

## Corpus re-run

After the operator-target refusal and before the corpus edits, the build failed exactly the two pass-through fixtures (`resource/a-marked-resource-is-emitted-as-authored`, `citation/a-marked-reference-above-the-root`), which were removed. After the procedural warning, seven fixtures whose dispatched targets were prose failed with an undeclared `W_DISPATCH_NOT_PROCEDURAL`; their targets now carry numbered steps. The usage-example bundles changed only by `»` becoming `⇉`.

## Work-planner bundles

All ten `example/work-planner/modes/*.md` bundles build with exit 0 and an empty stderr. Deliver's dispatches are Advance (chain Deliver → Advance → Sync, two hops) and Hoist (one hop); before Deliver's step 8 lost its operator, its `#run-delivery-session` link was a hop and a self-dispatch.
