## Overview

A session starts from a skill its CLI discovers and opens with its task in plain words, on every harness the eval keeps. The epic leaves the eval running end to end on the two workflows already written as skills, so the families that follow are converted onto a working runner.

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
  Each workflow's `scenarios.toml` states a `task` in plain words, filled from the scenario's inputs, and the run sends it as the session's only prompt.
- **The bare-prompt path leaves.**
  The three instruction files and the entry-file wiring are removed, and the runner gives sessions only to workflows written as skills.
- **The bootstrap pair proves it end to end.**
  `bootstrap-audit` and `inline-bootstrap` move to the variant layout as the first product variants, so the runner has a family to run while the others convert.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| [W01](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e00/w01.md) | Codex kept only with native discovery | AC1 | | | | |
| [W02](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e00/w02.md) | Each harness places the session's skill | AC2, AC3 | W01 | | | |
| [W03](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e00/w03.md) | The opening prompt states the task | AC4 | W02 | W04 | | |
| [W04](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-12-real-use-eval/e00/w04.md) | The bare-prompt path retired | AC5 | W02 | W03 | | |

## Acceptance Criteria

- [ ] **AC1.** The eval's harnesses are the agent CLIs whose own documentation states native skill discovery, as the harness tests show.
- [ ] **AC2.** Every session's workspace holds its variant's skill under the discovery root its harness's CLI documents, as the harness tests show.
- [ ] **AC3.** A session's CLI offers the placed skill and no skill of the eval's configuration or the caller's, as the harness isolation tests show.
- [ ] **AC4.** A session's opening prompt is its scenario's task in plain words, naming no file, skill or instruction, as the run tests show.
- [ ] **AC5.** The runner starts no session from a prompt naming an entry document, as the corpus and run tests show.

## Open Questions

- Where the tracing duty lives: `trace.log`, the sub-agent trace names and `answers.txt` are measurement the instruction states today; the planning record recommends one paragraph shared by every variant's `SKILL.md`.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-real-use-eval) — the decisions, defaults taken and the open question's recommendation.
