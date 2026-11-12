# A Measured Agent-Pick Run — November 2026

> I15 E01 W06 delivery · Created 2026-11-12

## Executive Summary

Deliver the live measurement of the agent-pick workflow: a runbook section for the run, a one-repetition shakedown that sets its caps, the twenty-session run once the user approves its cost cap, and the run's record committed beside the baseline as `agent-pick.json` and `agent-pick.md`. AC8 is the unit's coverage.

The task targets `i15/e01/main`, after the agent-pick workflow (W05). It is the epic's last row.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w06.md](w06.md) | Component plan, scope and observing checks |

## Links

| Resource | Link |
| --- | --- |
| Epic | [Agent Pick](https://github.com/m2ux/prosiform/issues/709) |
| Prerequisites | [W05 delivery](https://github.com/m2ux/prosiform/pull/725) |

## Run State

| Run | State |
| --- | --- |
| `agent-pick-shakedown`, 2026-11-12 | 4 sessions, none passed, each failure `miss`; USD 0.03219 over 908 675 tokens, the largest session 413 537. It sets the run's session cap of 830 000 tokens, token budget of 16 600 000 and cost cap of USD 1, recorded in the [runbook](https://github.com/m2ux/prosiform/blob/i15/e01/w06-a-measured-agent-pick/evals/diagram-following/RUNBOOK.md#agent-pick-run). |
| `agent-pick`, 20 sessions | Held for the user's approval of the cost cap. |
