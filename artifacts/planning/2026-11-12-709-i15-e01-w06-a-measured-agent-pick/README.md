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
| `agent-pick-shakedown`, 2026-11-12 | Stopped on a `defect` of the instruction: `epic-picked` and `unknown-kind-held` took `read_source` after the instruction told them the sources sat in their directory, escalated as [#726](https://github.com/m2ux/prosiform/issues/726) and corrected by [#727](https://github.com/m2ux/prosiform/pull/727); `initiative-picked` (`wrong_branch`) and `task-picked` (`overcompiled`) are each `miss`. USD 0.03219 over 908 675 tokens. It sets no cap. |
| `agent-pick-shakedown-2`, 2026-11-12 | On #727's instruction: stopped on a `defect` of `pf`'s guide: `unknown-kind-held` resolved the bundle's link from the bundle's folder, found no file and opened the router's source, escalated as [#728](https://github.com/m2ux/prosiform/issues/728) and corrected by [#729](https://github.com/m2ux/prosiform/pull/729); `epic-picked`, `initiative-picked` (`read_source`) and `task-picked` (`unfinished`) are each `miss`. USD 0.025455 over 808 191 tokens. It sets no cap. |
| `agent-pick-shakedown-3`, 2026-11-12 | On #729's guide: stopped on a `defect` of the instruction: `epic-picked` and `unknown-kind-held` omitted `Entry`, the bundle's clicked start marker, while the compiled instruction lacked the clicked-marker tracing rule, escalated as [#730](https://github.com/m2ux/prosiform/issues/730) and corrected by [#731](https://github.com/m2ux/prosiform/pull/731); `initiative-picked` and `task-picked` (`read_source`) are each `miss`. USD 0.025175 over 790 926 tokens. It sets no cap. |
| `agent-pick-shakedown-4`, 2026-11-12 | On #731's instruction: 4 sessions, none passed, each failure `miss` (three `read_source`, one `uncompiled`), every session on the scenario's path; USD 0.028844 over 1 010 089 tokens, the largest session 408 196. It sets the run's session cap of 820 000 tokens, token budget of 16 400 000 and cost cap of USD 1, recorded in the [runbook](https://github.com/m2ux/prosiform/blob/i15/e01/w06-a-measured-agent-pick/evals/diagram-following/RUNBOOK.md#agent-pick-run). |
| `agent-pick`, 20 sessions | Held for the user's approval of the cost cap. |
