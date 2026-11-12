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
| `agent-pick-shakedown-3`, 2026-11-12 | On #729's guide: stopped on an `unclear` triage. `epic-picked` and `unknown-kind-held` took `wrong_branch` at divergence 0, omitting `Entry`, the bundle's clicked start marker; the compiled instruction lacks the clicked-marker sentence the other forms' instructions carry. `initiative-picked` and `task-picked` (`read_source`) are each `miss`. USD 0.025175 over 790 926 tokens. It sets no cap. |
| `agent-pick`, 20 sessions | Held for the user's approval of the cost cap. |
