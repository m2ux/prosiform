## Overview

A session starts from a skill its CLI discovers and opens with its task in plain words, on every harness the eval keeps. The epic builds skill entry on the two workflows already written as skills, so the families that follow convert onto a working runner while the rest keep running as they are.

## Problem

- **Skills are off or suppressed on two harnesses.**
  The Claude harness [passes `--disable-slash-commands` and no skill tool](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/harness.py#L325-L333), and the Codex bridge [disables skill discovery and skill instructions](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/codex_agent.py#L27-L30).
- **Every prompt is an instruction file.**
  [`instruction()`](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/workflow.py#L1134-L1145) picks one of three instruction files by form and puts the entry document's name in it.
- **Only one form starts from a skill.**
  [`prepare()`](https://github.com/m2ux/prosiform/blob/d6072b20cfd5541b3edfa561e15677404e0f4cf6/evals/diagram-following/run.py#L440-L456) places a skill for `bootstrap` alone; every other form copies a tree or a bundle into the workspace.

## Proposal

- **Only CLIs that discover skills natively stay.**
  Codex stays only where its CLI's documentation states native discovery under a project root the bridge leaves on; otherwise its harness, bridge and stub leave the eval.
- **A variant is a skill.**
  A workflow's variant is a `SKILL.md` text at `skills/<variant>.md` and a material tree; the runner places the text as `SKILL.md` under the harness's discovery root and the tree beside it under `sources/`.
- **Each CLI offers the placed skill and no other.**
  The Claude harness admits its skill tool and drops the switch that disables skills, and the preflight refuses a configuration directory holding skills of its own.
- **The opening prompt is the scenario's task.**
  A skill workflow's `scenarios.toml` states a `task` in plain words, filled from the scenario's inputs, and the run sends it as the session's only prompt.
- **The skill states the tracing duty.**
  One paragraph every variant's `SKILL.md` shares states how a session records `trace.log`, names a sub-agent's trace and reads `answers.txt`.
- **The bootstrap pair proves it end to end.**
  `bootstrap-audit` and `inline-bootstrap` move to the variant layout as the first product variants; the other workflows run as they do until their family converts.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e00/w01.md) | Codex kept only with native discovery | AC1 | | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e00/w02.md) | Each harness places the session's skill | AC2, AC3 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e00/w03.md) | The opening prompt states the task | AC4, AC5 | W02 | | | |

## Acceptance Criteria

- [ ] **AC1.** Each harness the eval keeps drives an agent CLI whose own documentation states native skill discovery, cited in the harness, as the harness tests show.
- [ ] **AC2.** Every skill session's workspace holds its variant's skill under the discovery root its harness's CLI documents, as the harness tests show.
- [ ] **AC3.** A session's CLI offers the placed skill and no skill of the eval's configuration or the caller's, as the harness isolation tests show.
- [ ] **AC4.** A skill session's opening prompt is its scenario's task in plain words, naming no file, skill or instruction, as the run tests show.
- [ ] **AC5.** Every skill text in the corpus carries its workflow's shared tracing paragraph, stating how a session records `trace.log`, names a sub-agent's trace and reads `answers.txt`, as the corpus test shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-real-use-eval) — the decisions and defaults behind the layout, the prompt and the tracing paragraph.

