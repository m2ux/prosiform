# I05:E01:W09 Refused Run — October 2026

> Task delivery · Created 2026-10-29 · Revised 2026-10-29

## Executive Summary

Run `20261029T143428Z` started all 200 sessions of the default matrix and every one was refused by the login's weekly limit. It was recorded as a completed run — 200 started, zero cost, nothing skipped — and a report compared its pass rates against the baseline, so a reader cannot tell it from a matrix of genuinely failing agents without opening a transcript.

This task records such a run as refused, quoting the agent's own message as the reason, and makes its report name that instead of comparing pass rates. It is the part of the epic's last row that needs no paid session, so `make check` holds it against a stub agent.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W09 work item](w09.md) | The refused state, its recorded reason, the boundary around it and the test that holds both |
| [W09 validation](validation-w09.md) | The test-plan results, the mutation checks and the limitations |
| [W09 change list](change-list-w09.md) | What this delivery applied, and what it held |

## Decisions

- **The row keeps only the refused-run guard.** It carried the four-form baseline refresh and the corpus-separability question too; those moved to [I05:E08](https://github.com/m2ux/prosiform/issues/403), because only this guard is stub-testable and only this guard can close this epic without a paid run. (User, 2026-10-29.)
- **The state is decided after the sessions settle, not during them.** `outcome` reads the session records once the pool has completed and before `run.json` is written, so the refusal rests on the whole matrix rather than on whichever session finished last, and the report reads the recorded state rather than inferring one. (Session, 2026-10-29.)
- **A refusal needs the whole matrix started, not merely every session errored.** A run its budget stopped part way has sessions that never ran, and they might have entered a state. Reading an incomplete matrix as refused would claim more than the run observed, so it stays a completed run with sessions not started. (Session, 2026-10-29.)
- **The reason is one session's `result` text, in matrix order.** A refusal a reader cannot distinguish from an error count answers the problem only partly, and the login's own message names the limit. Where sessions were refused for different reasons, the first is quoted and the rest stay in their own records. (Session, 2026-10-29.)

## Result

- **Pull request:** [#404](https://github.com/m2ux/prosiform/pull/404), `[I05:E01] Refused Run`, head `i05/e01/w09-refused-run-a-matrix` → base `i05/e01/main`. Merged as a merge commit, `6fca69ba1d3b17fd9deabde426a80386608f399f`.
- **Epic:** 333's AC21 is ticked and W09's row takes Done. Every row is now delivered; the epic's completion check reports one blocker, the unmerged epic base, whose review draft is [#353](https://github.com/m2ux/prosiform/pull/353).
- **Board:** epic 333 is In Review on `users/m2ux/projectsV2/18`. Task issue [#396](https://github.com/m2ux/prosiform/issues/396) closed as completed.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Diagram Following planning record](../2026-10-27-333-i05-e01-diagram-following-eval/README.md) |
| Task issue | [#396](https://github.com/m2ux/prosiform/issues/396) |
| Predecessor | [#400](https://github.com/m2ux/prosiform/pull/400) — session isolation, the boundary the refusal is read inside |
| Review pull request | [#353](https://github.com/m2ux/prosiform/pull/353) — draft; its base carries this merge |
| Pull request | [#404](https://github.com/m2ux/prosiform/pull/404) — delivered and merged |
| Deferred to | [I05:E08 Corpus Separability](https://github.com/m2ux/prosiform/issues/403) — the baseline refresh and the harder corpus |
