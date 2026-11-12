# Instruction Fix

The `compiled` instruction named the documents the bundle was compiled from, and the scorer fails a session that opens one. Escalation [#726](https://github.com/m2ux/prosiform/issues/726); pull request [#727](https://github.com/m2ux/prosiform/pull/727) into `i15/e01/main`.

## Defect

Shakedown `agent-pick-shakedown` (2026-11-12, opencode, `openrouter/deepseek/deepseek-v4.1-flash-1017`) failed `epic-picked` and `unknown-kind-held` as `read_source`. Each entered the expected states and made the correct pick through `pf`, then listed the workspace and opened `workflow.md`, `states/*.md` and `reference/work-kind.md`, as each session's `subagents.json` `reads` records. `instruction-compiled.md` told the session "the documents ENTRY was compiled from sit in this directory": it pointed the agent at the documents `read_source` fails it for opening. Disposition `defect`, in the instruction.

## Fix

- The sources stay in the session's directory on purpose. The check confirms that an agent which comes across them, as it would in a real setup, keeps to what `pf` prints and writes, so the instruction neither points at the sources nor forbids them.
- `instruction-compiled.md` states only that `pf` is on the path and that each `pf` command runs from the session's directory.
- The evaluation README states that purpose once, beside its account of `read_source`, and describes the compiled instruction as telling the session to run each `pf` command from its working directory.
- `instruction-bootstrap.md` is unchanged. Its `read_source` sources are the skill's `sources/` documents; the text names a skill to find and says the skill names documents to compile, and never says where they sit or invites reading them. `SKILL.md` sits outside `sources/`, so reading it is no source read.
- A test holds each shell-form instruction (`compiled`, `bootstrap`) to naming no sources: no `sources` and no `compiled from`.

## Tests

Run against `i15/e01/fix-instruction-source-reads` at `c6c768db7`, on `i15/e01/main` at `9086a8892`. No live model session ran.

### T1 Instruction Text

- **Procedure.** `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/test_workflow.py evals/diagram-following/test_run.py -k "shell_form_instruction or instruction_names_the_entry or sub_agent_trace or compiled_session_receives"`
- **Observation.** 4 passed. Neither shell-form instruction names sources or what the bundle was compiled from; a compiled session's prompt names its entry bundle and "Run each pf command from this directory."; every form still names the sub-agent trace.

### T2 Eval Harness

- **Procedure.** `make eval-harness`
- **Observation.** 762 passed: the eval's corpus, scorer, harnesses, runner, report, README and runbook.

### T3 Repository Checks

- **Procedure.** `make check` with `PROSIFORM_BUILD="uv run --project <unit checkout>/src --frozen pf"`.
- **Observation.** Exit 0. Lint, format, type and lock checks clean; `make test` 2039 passed; `make harness` 1022 passed; corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence pass.

## Clicked Markers

The `compiled` instruction lacked the clicked-marker tracing rule the other two forms' instructions state. Escalation [#730](https://github.com/m2ux/prosiform/issues/730); pull request [#731](https://github.com/m2ux/prosiform/pull/731) into `i15/e01/main`.

### Defect

Shakedown `agent-pick-shakedown-3` (2026-11-12, opencode, `openrouter/deepseek/deepseek-v4.1-flash-1017`) failed `epic-picked` and `unknown-kind-held` as `wrong_branch` at divergence 0: their `trace.log` reads `Classify, Breakdown, Exit` and `Classify, Hold, Exit`, omitting `Entry`, the bundle's blank start marker `Entry(( ))` the diagram clicks to its section. `agent-pick-shakedown`'s `initiative-picked` did the same. `instruction.md` and `instruction-bootstrap.md` state "A marker the diagram clicks is a state like any other", added after the baseline's fourth shakedown failed this way (`fa3c85b2a`); `instruction-compiled.md` was written before that rule and before the rule that a decision's diamond and branch conditions are not states, and traced only "a state the workflow's diagram draws as a node". Disposition `defect`, in the instruction.

### Fix

- `instruction-compiled.md` states the tracing rule `instruction.md` and `instruction-bootstrap.md` state, word for word: a state is a step the workflow takes, never a decision's diamond, a branch condition, a section heading or another name the entry carries; a marker the diagram clicks is a state, and entering the one it opens with and the one it closes on is appended.
- The compiled form's `trace-<section>.log` sentence already matched the other two, so it is unchanged. The sub-agent reference spelling and the `answers.txt` sentence are dispatch rules, not tracing rules, and stay out of scope. The instruction still names no source.
- A test holds every form's instruction to the one tracing rule.

### T4 Tracing Rule

- **Procedure.** `uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . evals/diagram-following/test_workflow.py evals/diagram-following/test_run.py -k "same_tracing_rule or shell_form_instruction or instruction_names_the_entry or sub_agent_trace"`, run against `i15/e01/fix-instruction-markers` at `5aee1a76f`, on `i15/e01/main` at `7a7256a4e`.
- **Observation.** 4 passed. With the prior `instruction-compiled.md` restored, `test_every_form_states_the_same_tracing_rule` fails for `compiled`.

### T5 Eval Harness

- **Procedure.** `make eval-harness`
- **Observation.** 763 passed.

### T6 Repository Checks

- **Procedure.** `make check` with `PROSIFORM_BUILD="uv run --project <unit checkout>/src --frozen pf"`.
- **Observation.** Exit 0: lint, format, type and lock checks, tests, harness, corpus, smoke, layout, tables, links, vocabulary, invocation, conformance and independence pass. No live model session ran.
