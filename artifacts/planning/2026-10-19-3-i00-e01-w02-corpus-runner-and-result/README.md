# I00:E01:W02 Corpus Runner and Result Comparison - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the second task of [I00:E01] Corpus Harness. The task writes the runner that executes one fixture and decides its result from the manifest alone: it invokes the build named by configuration against the fixture's source tree and compares standard output, exit status and diagnostics against what the manifest declares. A mismatch names which expectation differed and locates the difference.

It matters because a declared fixture produces no verdict until something executes it, and a comparison that reports only that a run differed does not say where. The runner is also where the corpus's language-neutrality is tested for the first time: it must hold no knowledge of any implementation's modules, flags or internal wording, because the production build in Rust runs the same corpus through a runner of its own. The task covers AC2 and AC3 of the epic.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w02.md](w02.md) | The task's plan: the runner's interface, how the build under test is configured and invoked, how each expectation kind is compared and a difference located, the result shape, and the three things that hold the runner to naming no implementation |
| [validation.md](validation.md) | Each check as it was run: procedure, tested revision, results, the read of the runner for implementation-specific assumptions, and what the runs do not establish |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#3 \[I00:E01\] Corpus Harness](https://github.com/m2ux/prosiform/issues/3) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Fixture layout and manifest schema](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-3-i00-e01-w01-fixture-layout-and-manifest) |
| Epic review | [#41](https://github.com/m2ux/prosiform/pull/41) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
