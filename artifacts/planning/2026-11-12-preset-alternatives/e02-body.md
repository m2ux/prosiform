## Overview

An agent that reaches a `?` pick in real use keeps to what `pf` prints and writes. The epic measures agent-pick again once the eval starts every session from a skill the agent's CLI discovers, so initiative AC4's "without reading a source" rests on a real-use run.

## Problem

- **A guide-compliant pick fails scoring.**
  The agent-pick scenarios [hold a session to the listing run and the picked rerun](https://github.com/m2ux/prosiform/blob/c77dba6a707023fe09bcac505ae3ec11dbccaa7e/evals/diagram-following/workflows/agent-pick/scenarios.toml#L18-L24), so a session passing `--pick` on its first run, as the guide tells an agent that knows its pick, scores as uncompiled.
- **The measured run was not real use.**
  The [agent-pick run](https://github.com/m2ux/prosiform/pull/732) started each session from a prompt naming a bundle in a folder of loose sources. Every pick was right, and no session passed: fifteen of twenty opened source files and five ran `pf` on references no step states.

## Proposal

- **Either pick satisfies a scenario.**
  A scenario's picked run is met by a first-run `--pick` or by the listing followed by the rerun, and the scorer states which path the session took.
- **A real-use measurement.**
  Agent-pick runs on the eval reworked to start each session from a skill the agent's CLI discovers, and its record replaces the bare-prompt one.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| W00 | Agent-pick scoring accepts a first-run pick | AC2 | | | | |
| W01 | A real-use agent-pick run | AC1 | W00, [I16:E02:W02](https://github.com/m2ux/prosiform/issues/737) | | | |

## Acceptance Criteria

- [ ] **AC1.** An agent reaching a `?` pick through a skill resolves it from what the bundle and `pf` print without reading a source, as the agent-pick run on the skill-entry eval shows.
- [ ] **AC2.** A session that passes `--pick` on its first run of an agent-pick scenario's link, and one that reruns after the listing, each score as compiled, as `make eval-harness` shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-preset-alternatives) — the decisions placing this epic and the eval rework it waits on.
- **R2.** [Agent-pick run](https://github.com/m2ux/prosiform/pull/732) — the bare-prompt measurement this epic replaces.
- **R3.** [Agent-pick scenarios accept a first-run pick](https://github.com/m2ux/prosiform/issues/754) — the scoring gap the first-run pick opened.
