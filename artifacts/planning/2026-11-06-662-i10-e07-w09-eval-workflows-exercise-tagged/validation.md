# W09 Validation

## Revision

Task head: `d6fcb9b4e9c41bbef17e0647415efaaf5ab3b493`, based on W08 merge `1f6070d6bc0842cf6d656b5c85a112146108d9d1`. Task pull request: [672](https://github.com/m2ux/prosiform/pull/672), targeting `i10/e07/main`.

## Deterministic Workflow and Scorer

Passed `revision-check.py --project <task-worktree> --revision d6fcb9b4e9c41bbef17e0647415efaaf5ab3b493 -- uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/test_workflow.py evals/diagram-following/test_score.py -q` in its detached checkout. All 508 collected tests passed, exit 0.

AC20 observations:

- The existing tagged preset-deferral workflow compiles its mirror selection and follows the stored-copy transition. Source mutation and scorer controls reject omitted and wrong tags; equivalent normalized selections pass.
- Deferred dispatch activates two selections of `reference/crew.md#work`: lift and strap. Each publishes a distinct selection-qualified bundle with a distinct action.
- Deterministic bundle checks follow the selected filenames and real published dispatch links. Removing or changing the strap selection leaves its expected bundle absent.
- Scorer controls reject omitted, wrong, repeated and reversed bundle selections. Correct selections pass. Session records serialize normalized trace preset names, and a stub-runner integration test observes both selected dispatches.

## Callers at Exact Revision

The detached `revision-check.py` run at `d6fcb9b4e9c41bbef17e0647415efaaf5ab3b493` passed all 1,650 harness tests. Its first corpus attempt inherited the detached uv environment while the configured build pointed to the task checkout; uv printed a mismatched `VIRTUAL_ENV` warning on diagnostic stderr, causing all corpus comparisons to fail. This is verification setup noise, not a compiler result. The clean-environment detached rerun passed all 537 corpus fixtures and installed-wheel smoke, exit 0. It prefixes the configured build with `env -u VIRTUAL_ENV` and otherwise uses the same committed task build. AC19 is verified by those caller observations and the detached harness result.

## Full Configured Check

Passed `PROSIFORM_BUILD='uv run --project /home/mike1/projects/dev/md-composer/.worktrees/i10/e07/w09-eval-workflows-exercise-tagged/src --frozen pf' make check` at the committed task head, exit 0. The task checkout is clean.

- 1,901 source tests passed.
- 1,650 harness tests passed.
- 537 corpus fixtures passed.
- Installed-wheel smoke passed, including tagged single-entry command execution outside the repository.
- Lock, lint, format, strict typing, layout, command tables, online links, vocabulary, invocation, conformance and independence checks passed.
- Conformance reports 0 declarations naming no real design clause and 0 implementation-name disagreements. Its broader design coverage observations are reported, not represented as newly resolved by this unit.

The complete deterministic eval directory passed before the final runner test (695 tests); the added runner test passed separately. The final head collects 696 eval tests, all included in the passing full harness run (1,650 tests). No paid eval session ran.

## Review and Limitations

- Lint, formatting and strict typing passed; editor diagnostics reported no errors in the changed eval directory.
- A local read-only peer-review invocation could not execute its installed wrapper: permission denied. No peer-review verdict is claimed; direct diff review and deterministic checks supply this unit's evidence.
- The sandboxed uv attempt could not write its external cache, so validation runs outside `sbx`; wheel builds and online links also require host access.
- Epic sync at the historical W08 base reports `config/branches` absent. Integration, target-route and review-body checks that depend on it remain explicitly unevaluated; this unit adds no configuration.
- No plan expansion, production compiler change or unrelated debt was introduced. The only plan refinement is extending the existing deferred-dispatch workflow and serializing its selected trace identity.

## CI and Delivery

The [Checks CI run](https://github.com/m2ux/prosiform/actions/runs/42231292434) succeeded at exact head `d6fcb9b4e9c41bbef17e0647415efaaf5ab3b493`. Fresh epic target protection returned Branch not protected (404), and active branch rules returned an empty list. No approving review requirement applies to this target. The SHA-pinned merge-commit mutation succeeded: `f04086096c666cc29241a7fda3dcbdfd9c354743` on `i10/e07/main`, preserving the task branch. REST readback confirmed merged=true, exact head, target and merge SHA. The merge tree is identical to the validated task tree. `revision-check.py --project <task-worktree> --revision f04086096c666cc29241a7fda3dcbdfd9c354743 -- make harness corpus smoke PROSIFORM_BUILD='env -u VIRTUAL_ENV uv run --project <absolute-task-worktree>/src --frozen pf'` passed: 1,650 harness tests, 537 corpus fixtures and installed-wheel smoke, exit 0. This verifies AC19 and AC20 at the merged revision. The merged tree is identical to the task head whose full configured check passed.

Task-row recording marks W09 Done and ticks AC19/AC20 from the passing observing checks. W10 and AC22/AC23 remain pending and outside this unit. Epic issue remains open.

Default-branch integration and draft review pull requests 664 and 666 remain with the coordinator.
