# Validation

The checks the task pull request's Test Plan records, run against task branch `i15/e01/w06-a-measured-agent-pick` at `87c1141c7`, on `i15/e01/main` at `5ed17e5c4`, from the unit checkout with the locked development environment (`uv sync --frozen`).

## T1 Agent-Pick Run

- **Procedure.** The runbook's [Agent-Pick Run](https://github.com/m2ux/prosiform/blob/i15/e01/w06-a-measured-agent-pick/evals/diagram-following/RUNBOOK.md#agent-pick-run) command, live, after its fourth shakedown set the caps the user approved on 2026-11-12: `make eval-diagrams HARNESS=opencode ARGS='--models openrouter/deepseek/deepseek-v4.1-flash-1017 --workflows agent-pick --forms compiled --repetitions 5 --session-budget-tokens 820000 --budget-tokens 16400000 --run-id agent-pick'`; then each failing session triaged by the rubric into `dispositions.json` and the report rewritten with `report.py`.
- **Observation.** `completed`: 20 of 20 sessions started, 0 passed, USD 0.158708 over 5 037 116 tokens, under the USD 1 cost cap. Every session traced its scenario's path. Failures: `read_source` 15, `overcompiled` 4, `uncompiled` 1; each triaged `miss`, none `defect` or `unclear`, and the report lists no `untriaged` session. `report.json` is committed as `agent-pick.json` and `report.md` as `agent-pick.md`; `baseline.json`, `report.md` and `mvp-proof.json` are untouched.

| Scenario | Sessions | Passed | Failures |
| --- | --- | --- | --- |
| `epic-picked` | 5 | 0 | `read_source` 5 |
| `initiative-picked` | 5 | 0 | `read_source` 3, `overcompiled` 2 |
| `task-picked` | 5 | 0 | `read_source` 3, `overcompiled` 1, `uncompiled` 1 |
| `unknown-kind-held` | 5 | 0 | `read_source` 4, `overcompiled` 1 |

## T2 Record Tests

- **Procedure.** `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/test_readme.py evals/diagram-following/test_runbook.py`
- **Observation.** 15 passed. The README's Agent-pick run section states the cost, session count and per-class failure counts `agent-pick.json` records, every failure a miss.

## T3 Eval Harness

- **Procedure.** `make eval-harness`
- **Observation.** 764 passed.

## T4 Repository Checks

- **Procedure.** `make check` with `PROSIFORM_BUILD="uv run --project <unit checkout>/src --frozen pf"`.
- **Observation.** Exit 0: lint clean, `make test` 2039 passed, `make harness` 1022 passed, corpus 583 fixtures, and the remaining targets pass.

## T5 Checks Workflow

- **Procedure.** The repository's Checks workflow, which runs `make check`, on the task pull request at head `87c1141c7`.
- **Observation.** Pending.
