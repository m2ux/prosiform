# I05:E01:W09 Refused Run — October 2026

> Task delivery · Created 2026-10-29

## Executive Summary

Run `20261029T143428Z` started all 200 sessions of the default matrix and every one was refused by the login's weekly limit. It was recorded as a completed run — 200 started, zero cost, nothing skipped — and a report compared its pass rates against the baseline, so a reader cannot tell it from a matrix of genuinely failing agents without opening a transcript.

This task records such a run as refused, quoting the agent's own message as the reason, and makes its report name that instead of comparing pass rates. It is the part of the epic's last row that needs no paid session, so `make check` holds it against a stub agent.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W09 work item](w09.md) | The refused state, its recorded reason and the test that holds it |

## Decisions

- **The row keeps only the refused-run guard.** It carried the four-form baseline refresh and the corpus-separability question too; those moved to [I05:E08](https://github.com/m2ux/prosiform/issues/403), because only this guard is stub-testable and only this guard can close this epic without a paid run. (User, 2026-10-29.)

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Diagram Following planning record](../2026-10-27-333-i05-e01-diagram-following-eval/README.md) |
| Task issue | [#396](https://github.com/m2ux/prosiform/issues/396) |
| Deferred to | [I05:E08 Corpus Separability](https://github.com/m2ux/prosiform/issues/403) — the baseline refresh and the harder corpus |
| Review pull request | [#353](https://github.com/m2ux/prosiform/pull/353) |
