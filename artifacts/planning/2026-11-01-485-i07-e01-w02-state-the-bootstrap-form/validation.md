# Validation

Evidence for each check the [work item](w02.md) names, run in the task worktree on branch `i07/e01/w02-state-the-bootstrap-form` at `310c624e`, and again at `5cf609bf` after merging the epic base (W01, #494) into it.

## T1

**The README check holds the form table and `--forms` default to `run.FORMS`.** Observes AC2.

- **Procedure.**
  `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/test_run.py -k readme`
- **Observation.**
  `test_the_readme_states_every_form_the_runner_offers_and_its_default` passes against the edited README.
- **Negative control.**
  With the `bootstrap` row deleted from the Forms table, and separately against the README as it stood at the epic base `23602423`, the test fails on the form list (`['bundle', …, 'authored'] == ['bundle', …, 'bootstrap']`).
- **Result.**
  ✓

## T2

**`make check` with `PROSIFORM_BUILD` set.**

- **Procedure.**
  `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check`
- **Observation.**
  Exit 0. `make test` 1482 passed (1483 at `5cf609bf`); `make harness` 1105 passed, the new check among them; lint, format, typecheck, steps, authoring, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and mock-scenarios all pass.
- **Result.**
  ✓
