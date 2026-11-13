# I01 Retirement — November 2026

> Plan change · Created 2026-11-13

## Executive Summary

I01 (Field Refinement) planned to settle the specification through a findings ledger, a design-first revision order and a gated freeze tag. The ledger's only delivery (#324) merged into the epic base `i01/e00/main`, which was deleted without merging, so `main` holds no ledger; meanwhile real-use evidence has come from the eval initiatives I16 (#734) and I18 (#768), and each release cuts a paired contract tag. The user confirmed on 2026-11-13 that the ledger, revision and freeze epics are superseded.

The repository-check epic carried under I01 still holds live work unrelated to I01's goal. It moves to its own initiative, I19 (#770), whose goal is that every rule the repository's checks and design record state is stated exactly: each check reports what it claims to and refuses what it claims to refuse. I01 closes on its four delivered epics.

## Decisions

| Decision | Resolution |
| --- | --- |
| Ledger-based work (E00 #21, E01 #22, E13 #23) | Closed as not planned, superseded by I16 and I18; E00 W01's Done mark and AC1–AC2 ticks cleared because the delivery never reached `main` |
| Repository checks (E03 #187) | Moved to I19 #770 as E00, rows, issues, criteria and `priority: 2` kept; task titles renumbered from `I01:E03` to `I19:E00` |
| Workspace-skill prerequisite removal (E01 W04) and the `prosiform-skills` example | Retired with E01; a later proposal if `pf`-compiled workspace skills become a goal |
| I19 goal | "Every rule the repository's checks and its design record state is stated exactly: each check reports what it claims to and refuses what it claims to refuse." |
| I01 | Closed as completed on E02 #195, E06 #218, E09 #242, E10 #257; AC1–AC10 removed, AC11–AC17 kept |

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [I19 body](drafts/i19.md) | The new initiative's saved body |
| [#187 body](drafts/issue-187.md) | The repository-check epic as I19:E00 |
| [#20 body](drafts/issue-20.md) | I01's closing body |
| [#21 body](drafts/issue-21.md) | The ledger epic with its undelivered tick cleared |
| [#20 comment](drafts/comment-20.md) | I01's closing comment mapping each removed epic to its fate |
| [#21 comment](drafts/comment-21.md) | The ledger epic's retirement reason |
| [#22 comment](drafts/comment-22.md) | The revision epic's retirement reason |
| [#23 comment](drafts/comment-23.md) | The freeze epic's retirement reason |

## Links

| Resource | Link |
| --- | --- |
| I01 | https://github.com/m2ux/prosiform/issues/20 |
| I19 | https://github.com/m2ux/prosiform/issues/770 |
| I16 | https://github.com/m2ux/prosiform/issues/734 |
| I18 | https://github.com/m2ux/prosiform/issues/768 |
| Ledger delivery | https://github.com/m2ux/prosiform/pull/324 |
