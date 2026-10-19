# I00:E02:W01 Command Interface, Streams and Exit Statuses - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the first task of [I00:E02] Walking Skeleton. The task gives prosiform a command: the option set the design declares, the split that puts bundled Markdown on standard output and diagnostics on standard error, and the exit status each outcome returns. It adds no bundling of its own — a run that parses its arguments and reports an outcome is the whole of it — so the epic's later tasks extend a command that already runs rather than building one around work already written.

It matters because the corpus harness delivered by [I00:E01] decides a fixture's result from an invocation, a standard output, an exit status and a diagnostic stream, and until something answers to those four it can execute nothing. This is the task that makes the harness's own fixtures runnable for the first time, and the first that can state the stream discipline the design relies on: a consumer reading the presence of Markdown as success accepts a failed run as a complete one, so the status is the signal and the bundle is the only thing standard output carries. The task covers AC3, AC4 and AC10.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | The task's plan: the option set and its defaults, the stream discipline, the outcome-to-status mapping, and what the command does not yet do |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#4 \[I00:E02\] Walking Skeleton](https://github.com/m2ux/prosiform/issues/4) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Corpus harness | [#3 \[I00:E01\] Corpus Harness](https://github.com/m2ux/prosiform/issues/3) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
