# Test Results

Validation observed at `f40-live-deferrals` head fe3bb30ef, based on `main` at 6a6b78410.

## Live Layout

- **Reproduction.** On `main`, a `deferred-dispatch` `bundle-set` workspace laid out as the runner lays one out carries `[↳ Crew](...)` naming its target from the runner's temporary folder; `pf` on it fails with `E_TARGET_NOT_FOUND` from both the workspace and the bundle's folder. Bundled in place, the line reads `[↳ Crew](../reference/loading.md#crew)` and `pf` on it from `workflow.bundles/` exits 0 and writes the crew's bundle set.
- **T1, AC1.** `test_a_deferred_line_in_a_prepared_workspace_names_a_document_there` prepares each `bundle-set` and `briefed` workspace with `bundles_of` and `prepare` and resolves every deferred line from its bundle's folder to a document of the workspace. With `run.py` at `main` it fails: the line names a path outside the workspace.
- **T2, AC2.** `test_a_stub_session_bundles_a_deferred_line_from_its_bundles_folder` runs the `deferred-dispatch` scenarios through the stub on the `claude` harness. The session's call is `cd workflow.bundles && pf '[↳ Crew](../reference/loading.md#crew)'`, admitted by `Bash(cd *),Bash(pf *)`, and its result is not an error; `deferred-dispatch-bundled` passes. With `run.py` at `main` it fails: no bundle carries a line naming the stated target.
- **T3, AC3.** `test_the_instruction_guide_and_harnesses_agree_where_a_line_runs` holds the guide and the instruction to "from the folder that bundle is in", `claude` to `Bash(cd *),Bash(pf *)`, `opencode` to `cd *` and `pf *`, and `codex`'s `pf` tool to a `cwd`. The harness permission tests in `test_harness.py` and `test_run.py` hold the same rules.

## Suites

- **T4, AC4.** `make eval-harness`: 861 passed, 0 failed. `make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lint, format, types, 2,330 build tests, 1,155 harness tests and 708 corpus fixtures.
