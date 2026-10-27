# I05:E01:W03 Headless Agent Runner With Spending Cap — October 2026

> Task delivery · Created 2026-10-27

## Executive Summary

This record holds the delivery of I05:E01 W03: the runner that gives each workflow form and scenario to an isolated headless `claude -p` session per model and repetition, records each session's transcript, usage, cost and verdict, and stops before a run would pass its spending cap.

It reads the corpus through W01's `workflow.py` and scores each session with W02's `score`; W04's report reads its records, and W05 runs the default matrix through it. One live `claude-haiku-5-5` session here gives the per-session cost W05's estimate rests on.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W03 work item](w03.md) | The runner, its records, its cap and the stub agent |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Prior row | [W02 record](../2026-10-27-333-i05-e01-w02-trace-scorer-and-failure/README.md) |
