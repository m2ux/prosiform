# I05:E01:W05 First Baseline From the Default Matrix — October 2026

> Task delivery · Created 2026-10-28

## Executive Summary

This record holds the delivery of I05:E01 W05: the first full run of the diagram-following eval's default matrix. The matrix is `claude-haiku-5-5` and `claude-sonnet-5-5`, every workflow, form and scenario, five repetitions — 150 sessions. Failures are reviewed, and a failure the corpus causes is fixed and its cells re-run. The result is committed as the baseline later runs compare against, with the measured cost of a default run stated in the eval's README.

Until one full run is recorded, the eval has no reference point, and its first finding is unknown. That finding is how well agents follow a bundled diagram, against the unbundled tree and prose.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W05 work item](w05.md) | The run, the review of failures, the baseline and the measured cost |

## Decisions

- **Eval login.** The user logged in once to the eval's own config directory, `~/projects/eval/prosiform/config`. This resolves the epic's Open Question, which deferred W05 until that login. (User, 2026-10-28.)
- **Calibration.**
  - The sessions were measured on `i05/e01/main` at `22ae0f2e`.
  - `claude-haiku-5-5` cost about USD 0.0032–0.0039 a session.
  - `claude-sonnet-5-5` cost about USD 0.038 on the linear bundle.
  - The full run is estimated at about USD 3.5–4.5.
- **Run approved.** The user approved the full run of 150 sessions with `--session-budget-usd 0.25 --budget-usd 40`. No combination of runs, re-runs included, may pass USD 40 in total. (User, 2026-10-28.)

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic plan | [Diagram Following planning record](../2026-10-27-333-i05-e01-diagram-following-eval/README.md) |
| Review pull request | [#353](https://github.com/m2ux/prosiform/pull/353) |
