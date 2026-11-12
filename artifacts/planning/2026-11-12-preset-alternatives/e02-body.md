## Overview

An agent that reaches a `?` pick in real use keeps to what `pf` prints and writes. The epic measures agent-pick again once the eval starts every session from a skill the agent's CLI discovers, so initiative AC4's "without reading a source" rests on a real-use run.

## Problem

- **The measured run was not real use.**
  The [agent-pick run](https://github.com/m2ux/prosiform/pull/732) started each session from a prompt naming a bundle in a folder of loose sources. Every pick was right, and no session passed: fifteen of twenty opened source files and five ran `pf` on references no step states.

## Proposal

- **A real-use measurement.**
  Agent-pick runs on the eval reworked to start each session from a skill the agent's CLI discovers, and its record replaces the bare-prompt one.

## Work Breakdown

| Task | Description | Coverage | Depends on | Joins | Lane | Done |
| --- | --- | --- | --- | --- | --- | --- |
| W00 | A real-use agent-pick run | AC1 | [E01](https://github.com/m2ux/prosiform/issues/709) | | | |

## Acceptance Criteria

- [ ] **AC1.** An agent reaching a `?` pick through a skill resolves it from what the bundle and `pf` print without reading a source, as the agent-pick run on the skill-entry eval shows.

## References

- **R1.** [Planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-11-12-preset-alternatives) — the decisions placing this epic and the eval rework it waits on.
- **R2.** [Agent-pick run](https://github.com/m2ux/prosiform/pull/732) — the bare-prompt measurement this epic replaces.
