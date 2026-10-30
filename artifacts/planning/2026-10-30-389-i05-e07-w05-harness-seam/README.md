# I05:E07 W05 Harness Seam — October 2026

> Task delivery · Created 2026-10-30

## Executive Summary

The eval could drive one agent CLI. A pass rate it produced said what that CLI did with a workflow form and nothing about whether another CLI, given the same material, would do the same. The coupling was never in the measurement: the matrix, the workspaces, the budget, the timeout and the scorer are alike whatever CLI runs them. It was in the command line, the environment a session is confined by, and the shape of the stream read back.

This record holds the delivery of W05, which puts those three behind one seam and declares a second harness against it. Cursor's stream was read from a real session's output before the adapter was written, so the shape it reads is the shape the CLI prints.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W05 work item](w05.md) | What a harness is, the two declared, and the budget it is held to |
| [Validation](validation.md) | Each check the work item's Test row names, with the revision it ran on and what it observed |
| [Change list](change-list.md) | The plan changes this session met and those it held |

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E07 Dispatch Following](https://github.com/m2ux/prosiform/issues/389) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Epic record | [Dispatch Following design](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-29-389-i05-e07-dispatch-following) |
| Delivery | [Pull request 418](https://github.com/m2ux/prosiform/pull/418) |
