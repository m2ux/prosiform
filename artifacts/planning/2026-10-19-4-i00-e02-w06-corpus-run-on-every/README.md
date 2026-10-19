# I00:E02:W06 Corpus Run on Every Change - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the last task of [I00:E02] Walking Skeleton. A continuous-integration job runs every fixture the corpus holds against the build under test on each change, reports the failing fixtures by identifier, and fails the change when one fails. The build comes from configuration, and a job that cannot reach one fails rather than skipping, because a skipped corpus run sits inside a passing suite saying nothing.

It matters because the corpus has never been executed by anything but a person. `make corpus` runs the manifest schema tests and the runner's own unit tests; it executes no fixture. Every count this epic has reported — 11 of 26, 30 of 32, 36 of 38 — came from a driver written by hand for that one session and thrown away, so the whole corpus's verdict has rested on work nothing repeats. It matters again because the corpus is knowingly incomplete: two fixtures declare behaviour that epics after this one deliver, so a job that fails on any failing fixture would make the tree permanently red, and the rule that separates a fixture waiting for a row from a fixture reporting a defect is this task's to settle. The task covers AC11.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w06.md](w06.md) | The task's plan: the runner's invocation as a job step, how a fixture awaiting a later row is told from one reporting a defect, the job's reporting, and its failure when no build is configured |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#4 \[I00:E02\] Walking Skeleton](https://github.com/m2ux/prosiform/issues/4) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Corpus harness | [#3 \[I00:E01\] Corpus Harness](https://github.com/m2ux/prosiform/issues/3) |
| W04 record | [Whole-document emission under a filename heading](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w04-whole-document-emission-under) |
| W05 record | [Fixtures from unmodified workspace skills](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w05-fixtures-from-unmodified-workspace) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
