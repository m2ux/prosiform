# W16 Validation — November 2026

> Validation evidence · Created 2026-11-01

Evidence for each check the [W16 work item](w16.md) names, on branch `i07/e00/w16-name-the-sub-agent` at `0a442443`.

## Before the Change

- `instruction.md`, which the compiled and authored forms use, named no sub-agent trace. `instruction-bootstrap.md` named it in a bullet addressed to the sub-agent, which reads only the prompt its session writes.
- `stub_agent.py` wrote one `trace-<section>.log` per start whatever its instruction said, and its `Task` prompt named no trace, so the scored dispatch test passed without any instruction asking for the trace.

## Instruction States the Trace

`test_every_dispatching_form_names_the_sub_agent_trace` in `evals/diagram-following/test_workflow.py` reads the instruction each corpus form is given, the compiled, authored and bootstrap forms among them, and holds that each tells the session to hand its sub-agent `trace-<section>.log` (`SUB_AGENT_TRACE` in `score.py`).

- With `instruction.md` restored to its prior text, the test fails on the compiled form.
- With the change, it passes.

## Scored Dispatch in Both Forms

`test_a_scored_dispatch_keeps_the_sub_agents_trace_it_was_given[compiled]` and `[authored]` in `evals/diagram-following/test_run.py` run `dispatch-chain` through the stub agent in each form. Each holds that the session passes, that each `Task` prompt in the transcript names `trace-work.log` and `trace-check.log` in dispatch order, and that the session's records keep exactly `trace.log`, `trace-work.log` and `trace-check.log`.

- With `instruction.md` restored to its prior text, both cases fail: no prompt names a trace, so no sub-agent trace is written or kept.
- With the change, both pass.

## Untold Sub-Agent Keeps None

`test_a_sub_agent_untold_its_trace_name_keeps_none` in `evals/diagram-following/test_run.py` runs the compiled form under an instruction with the trace bullet removed, and holds that no `Task` prompt names a trace and the records keep `trace.log` alone. This is the review the work item names: the stub writes no sub-agent trace its instruction does not ask for.

- Its guard, that the shipped instruction states the name, fails without the change; with it, the case passes.

## Test Runs

- Targeted: the four cases above, `4 passed`, and each failing with `instruction.md` at its prior text (`4 failed`).
- `make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`: exit 0. `make test` 1420 passed; `make harness` 1062 passed; lint, format, type check, corpus, smoke and every guard pass.
