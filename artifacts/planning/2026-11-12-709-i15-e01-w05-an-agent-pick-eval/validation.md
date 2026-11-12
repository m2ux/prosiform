# Validation

The checks the task pull request's Test Plan records, run against task branch `i15/e01/w05-an-agent-pick-eval` at `eae0abebf` (read check at `47678cd19`, workflow at `eae0abebf`), rebased on `i15/e01/main` at `63d0cc561`, from the unit checkout with the locked development environment (`uv sync --frozen`). No live model session ran.

## T1 Workflow Corpus

- **Procedure.** `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/test_workflow.py -k "agent and pick or choice_line or failure_class"`
- **Observation.** 21 passed. The form bundles cleanly; each of the four scenarios' paths is the walk its inputs determine and the walk the compiled bundles state, the walk running `pf reference/work-kind.md#route --presets=?`, reading the listing and rerunning with the alternative whose choice line the input holds (`other`, declared last, where none does); each scenario states those two runs. Each choice line but `other`'s is held by exactly one input, one input holds none, and no input names an alternative. A scenario stating another pick, and an input holding two choice lines, are faults. Every failure class, `read_source` among them, is produced by some scenario.

## T2 Scorer and Harness Reads

- **Procedure.** `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/test_score.py evals/diagram-following/test_harness.py evals/diagram-following/test_codex_agent.py -k "agent_pick or read_tool or record_holds_the_files or bridge_records or file_the_bridge"`
- **Observation.** 16 passed. An agent-pick session passes with the guide, the listing and the pick, reading bundles and inputs or with reads unreported; it fails `read_source` for a read of the router, a state or a route document; `uncompiled` without the rerun or without the listing; `overcompiled` beside a wrong pick; `misordered_compile` with the pick before the listing; and `wrong_branch` entering another kind's state. The Claude, Cursor, opencode and Codex streams each report their read tool's files, the Codex bridge records each `read_file` path, and the record holds `reads` for a shell form and null otherwise.

## T3 Stub-Agent Runs

- **Procedure.** `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/test_run.py -k agent_pick`
- **Observation.** 4 passed. A stub-agent run of each of the four scenarios in the `compiled` form passes when it makes its stated runs; with `STUB_AGENT_SCENARIO` taking another kind's path and runs each other scenario fails `wrong_branch`, with `STUB_AGENT_READ` opening `reference/work-kind.md` each fails `read_source`, and with `STUB_AGENT_RUNS=1` stopping after the listing each fails `uncompiled`.

## T4 Eval Harness

- **Procedure.** `make eval-harness`
- **Observation.** 761 passed: the eval's workflow corpus, scorer, harnesses, runner, report, README and runbook rubric, `read_source` among the rubric's classes.

## T5 Repository Checks

- **Procedure.** `make check` with `PROSIFORM_BUILD="uv run --project <unit checkout>/src --frozen pf"`.
- **Observation.** Exit 0. Lint, format, type and lock checks clean; `make test` 2039 passed; `make harness` 1022 passed; corpus 583 fixtures, 583 pass, 0 fail; smoke, layout, tables, links, vocabulary, invocation, conformance and independence pass, the conformance report naming 0 declarations that name no clause.

## T6 Checks Workflow

- **Procedure.** The repository's Checks workflow, which runs `make check`, on pull request [#725](https://github.com/m2ux/prosiform/pull/725) at head `eae0abebf`.
- **Observation.** The `Checks` run completed with conclusion success: [run 43202564110](https://github.com/m2ux/prosiform/actions/runs/43202564110/job/131129450765).
