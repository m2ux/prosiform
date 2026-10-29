# I05:E07:W02 Validation

Each check the work item's Test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e07/w02-sub-agent-record-and`, cut from `i05/e07/main` at `535ed374d4615f01cf1729afe6e70feab73ebc2b`.
- **Tested revision.** `5d19eee1` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`, `src/.venv/bin/pf`, version `0.15.0 (skill-markdown-v4)`.
- **No paid session ran.** Every session below starts [`stub_agent.py`](https://github.com/m2ux/prosiform/blob/5d19eee1/evals/diagram-following/stub_agent.py) in place of the agent.

## T1 AC3 — every bundle reached a sub-agent

A dispatch scenario's trace passes only when every section it dispatches reached a sub-agent, in its order; a bundle that reached none, or reached one out of turn, takes `undispatched`.

| Test | Observes |
| --- | --- |
| `test_score.py::test_a_dispatch_scenario_passes_on_its_path_and_its_record` | AC3: each of the four dispatch workflows, on its scenario's path with the record its scenario states, passes, and the record names every entry the trace names. |
| `test_score.py::test_a_bundle_that_reached_no_sub_agent_is_undispatched` | AC3: the chain's own path with no sub-agent start takes `undispatched`. |
| `test_score.py::test_a_bundle_dispatched_after_another_is_undispatched` | The chain's two sections started in the other order take `undispatched`, since the record is held in order. |
| `test_score.py::test_a_start_naming_its_compiled_bundle_names_the_same_section` | A compiled form's start names `pf`'s bundle, `plan__work.bundle.md`, and is read as the section `plan#work`, so one record serves both forms. |
| `test_run.py::test_a_run_starting_no_sub_agent_is_undispatched` | AC3 end to end: the stub starts no sub-agent, so the run records `undispatched` and its `subagents.json` names no start. |

## T2 AC3 — a set's bundles started together

A set's members must start beside the one above them; started serially they take `sequential_set`.

| Test | Observes |
| --- | --- |
| `test_score.py::test_a_set_started_one_after_another_is_sequential_set` | AC3: the parallel set's two sections, both reached, with neither marked as starting beside the other, take `sequential_set`. |
| `test_run.py::test_a_run_that_ran_a_set_in_sequence_is_sequential_set` | AC3 end to end: the stub starts both sections in a message of their own, so the run records `sequential_set` and both entries read `together` false. |

## T3 AC3 — every question was relayed

A sub-agent's returned question must be put to the user; a session that returns `done` where the scenario states `question` answered it in the sub-agent's place and takes `unrelayed_question`.

| Test | Observes |
| --- | --- |
| `test_score.py::test_a_question_answered_in_the_sub_agents_place_is_unrelayed` | AC3: the question workflow's record returning `done` where its scenario states `question` takes `unrelayed_question`. |
| `test_run.py::test_a_question_the_session_answered_is_unrelayed_question` | AC3 end to end: the stub returns `done` for both starts, so the run records `unrelayed_question` and both entries read `done`. |

## T4 AC3 — the run completed

The completion check is read first, so a trace short of its path is `unfinished` however few sub-agents it started.

| Test | Observes |
| --- | --- |
| `test_score.py::test_a_run_that_stopped_short_is_unfinished_though_nothing_was_dispatched` | AC3: the chain's path one state short, with no record, takes `unfinished` at index 1. |
| `test_run.py::test_a_dispatch_run_that_stopped_short_is_unfinished` | AC3 end to end: a stub stopped after one state that also dispatched nothing records `unfinished`, not `undispatched`. |

## T5 AC3 — the classification order

A trace failing two checks takes the earlier, so the report's failure kinds separate the three departures.

| Test | Observes |
| --- | --- |
| `test_score.py::test_the_dispatch_checks_are_read_in_order` | AC3: a chain record that started too few sub-agents and gave the wrong return takes `undispatched`; a set run in sequence that also gave the wrong return takes `sequential_set`. |
| `test_score.py::test_a_scenario_dispatching_nothing_passes_the_dispatch_checks` | A workflow that dispatches nothing states no trace, so all three checks pass and the seven path classes still decide it. |
| `test_run.py::test_a_scenario_dispatching_nothing_records_no_start` | End to end: a `linear` session writes `subagents.json` naming no start and passes. |

## T6 The record is the transcript's, and sits beside the trace

The sub-agent record is read from the transcript once as the session settles, written beside the trace and the session's cost, and read by the scorer in place of the transcript.

| Test | Observes |
| --- | --- |
| `test_score.py::test_a_start_is_read_from_the_transcript_with_its_position_and_return` | A start reads its section from the call's description, its return from the `tool_result` (a text opening `question` is `question`, else `done`), and its `together` flag from sharing an assistant message. Three calls across two messages read as ordered, with the second of a shared message marked together. |
| `test_score.py::test_an_absent_transcript_records_no_start` | An absent transcript, and a record never written, name no start. |
| `test_run.py::test_a_dispatch_session_records_its_sub_agents_beside_its_trace` | AC3: a compiled-form session's records hold `subagents.json` beside `trace.log`, `session.json` and `transcript.jsonl`, its entries are the scenario's trace, and the session passes. |

## T7 make check

`PROSIFORM_BUILD=/home/mike1/projects/dev/md-composer/.worktrees/i05/e07/w02-sub-agent-record-and/src/.venv/bin/pf make check` exited 0:

- lock check, lint, format check and type check over `src/prosiform`, `src/tests`, `checks` and `evals`;
- 1302 unit tests in `src`;
- 941 harness tests over `checks/tests` and `evals/diagram-following`, up from 921 before this branch: the eval's own suite grew by twenty tests, fourteen in `test_score.py` and six in `test_run.py`;
- the corpus, the installed-wheel smoke run, layout, tables, links, vocabulary, invocation, conformance, independence, steps and authoring checks, each clean.

`make harness` alone: 941 passed in 26.66 s. `evals/diagram-following/test_score.py`: 42 passed. `ruff check`, `ruff format --check` and `mypy` over `evals/diagram-following`: all clean.

## What this unit does not claim

- **AC4** is W03's: the first baseline of the dispatch scenarios under the default matrix. No paid session ran here and the eval budget was not touched; `EVAL_BUDGET_USD` still reads USD 100.
- **No baseline moved.** `baseline.json` and `report.md` are untouched, and every baseline cell is a `linear`, `branching` or `looping` workflow the dispatch scenarios do not join.
