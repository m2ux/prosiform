# I00:E00:W04 Continuous Integration Running Those Commands - October 2026

> Task Plan - Created 2026-10-18

## Executive Summary

This record holds the local plan for the fourth and last task of [I00:E00] Project Foundation. The task adds the continuous-integration job that installs the environment from the lockfile and runs the documented check commands on every change, failing the change when one of them fails. It invokes those commands rather than reimplementing them, so a local run and a remote run exercise the same configuration. It also supplies the job with the credential and the branch history the link check needs, and brings that check's heading-slug rule to the one GitHub generates.

It matters because a check that exists only as a command someone remembers to type passes silently when it is skipped. The five criteria of this epic that hold today hold because someone ran the checks by hand; this task is what makes them hold on every change without anyone remembering. The task covers AC4, the last unticked criterion of the epic.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W04 Continuous Integration](w04.md) | The task's local plan: the job, the credential and the branch history it carries, and the heading-slug rule |
| [Validation](validation.md) | The integration runs, clean and against a deliberate violation of each check, and the slug comparison |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#26 \[I00:E00\] Project Foundation](https://github.com/m2ux/prosiform/issues/26) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W03 record | [Test runner and static checks](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-18-26-i00-e00-w03-test-runner-and-static) |
| Epic review | [#34](https://github.com/m2ux/prosiform/pull/34) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
