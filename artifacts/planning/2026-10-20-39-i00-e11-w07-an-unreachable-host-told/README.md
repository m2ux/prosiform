# I00:E11:W07 An Unreachable Host Told Apart From an Unresolved Reference - October 2026

> Task Plan - Created 2026-10-20

## Executive Summary

This record holds the local plan for the row that makes the link check distinguish a reference that does not resolve from a host that did not answer. A status of 400 or above below 500 is the host answering about the target and fails the check. A status of 500 or above, a failed connection and a timed-out request each mean the host reported nothing about the target, so the address is attempted three times with a growing delay and then counted as unreachable, reported on a WARN line and counted beside the references that resolved, with the run passing.

It matters because a check that fails on something the repository cannot control teaches a reader to re-run it rather than to read it, which is the habit that lets a genuine broken reference through. It also blocks a merge the evidence supports: a session that must not merge on a failed run, and must not claim a run it did not get, has no move left but to wait on a third party.

The row is delivered ahead of its epic. [I00:E11](https://github.com/m2ux/prosiform/issues/39) runs after every other epic in the initiative, and this row gates nothing and is gated by nothing, so every wave between now and then would otherwise risk a lost continuous-integration run.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w07.md](w07.md) | The task's plan: the two verdicts, what separates them, and the retry |
| [validation.md](validation.md) | What the check was measured to do and the checks the delivery was held to |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Defect | [#84 The Link Check Fails a Branch on a Third-Party Outage](https://github.com/m2ux/prosiform/issues/84) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
