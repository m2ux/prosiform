# W02+W03 Validation

Each check the [W02](w02.md) and [W03](w03.md) work items name, run in the task worktree on branch `i08/e08/w02-the-eval-workflow-tree` with `PROSIFORM_BUILD` naming the worktree's build.

## Revision

- Tested head: `cb2872a7e03c02082392379c6b118fc239482c0a`, on epic base `549f7e6b` with `origin/i08/e06/main` (`f3b902c1`, carrying #570) merged in as `d7fc82bb`.
- Commits: `9fdb2163` holds every workflow document to a declaration of presets; `5249eb95` names the preset shape in the independence and link checks' examples; `cb2872a7` drops the retired root option from the manifest-schema test.
- Design pin: unchanged at `cf3824687`.

## T1 Make Harness

`make harness` passes 1086 tests. `test_every_workflow_document_declares_presets` reads all 118 workflow documents and finds no fault; `test_a_document_declaring_outside_presets_is_a_fault` reports a copy whose state lost its block, declares a scalar, or declares `group` outside a preset. Every form bundles carrying every state. `git diff 549f7e6b cb2872a7 -- evals/diagram-following/workflows` is empty.

Result: ✓

## T2 Search of Checks

`grep -rnE 'prosiform\.(group|subst|root)\b|root: |"-r"|"-m"|--merge' checks/` finds only `checks/tests/test_corpus_run.py`, the corpus run's cases failing a fixture that declares `group` or `root` outside a preset. `checks/corpus.py` names those keys in `SETTINGS` to refuse them. No other check reads or names a retired field or option.

Result: ✓

## T3 Make Check

`make check` exits 0: lock, lint, format, type checks, 1563 build tests, 1086 harness tests, the corpus (425 fixtures pass), smoke, layout, tables, links, vocabulary, invocation, conformance (354 clauses) and independence pass.

Result: ✓
