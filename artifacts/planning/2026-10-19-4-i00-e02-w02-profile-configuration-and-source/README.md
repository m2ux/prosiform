# I00:E02:W02 Profile Configuration and Source Parsing - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the second task of [I00:E02] Walking Skeleton. The task configures the parser to the Markdown profile the design declares — CommonMark with pipe tables and double-tilde strikethrough enabled, source task-list markers preserved as text, typographic substitution disabled and unsupported extensions off — and makes the command parse a source under it. It also draws the line the profile implies: a construct the profile does not support is not quietly published as prose. One recognized as a dependency or as a section-naming extension fails the run, because emitting it as literal text would drop a dependency without reporting it, while prose that merely resembles an extension is left alone.

It matters because a default parser configuration is not the declared profile, and the difference decides whether a run of characters is a table, a strikethrough, a task marker or ordinary text. Every later clause — the outline shift, the destination identity, the preservation invariant — is stated over the parse this task fixes, so a parse that differs from the contract makes every criterion after it measure the wrong thing. The profile is also the contract's one explicitly versioned part: `skill-markdown-v1` is the identifier the command reports, and pinning the configuration beside it is what stops a later extension change reinterpreting source that already bundled. The task covers AC5, AC7 and AC9.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w02.md](w02.md) | The task's plan: each profile clause traced to the option that enforces it, the profile identifier and where it is reported, and the rule separating a recognized unsupported construct from prose that resembles one |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#4 \[I00:E02\] Walking Skeleton](https://github.com/m2ux/prosiform/issues/4) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Command interface, streams and exit statuses](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w01-command-interface-streams-and) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
