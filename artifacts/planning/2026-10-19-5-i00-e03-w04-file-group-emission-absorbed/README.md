# I00:E03:W04 File Group Emission: Absorbed Title and Source Order - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the last row of [I00:E03] Outline Hierarchy. A file group emits its selected regions in their original source order, a document's preamble sitting after its filename heading and before its first retained heading. A source whose only document-level H1 slugs to the slug of the final segment of its file heading has that heading absorbed, emitting no duplicate and leaving the group's headings at their source levels, while a source whose H1 differs keeps it and shifts by one.

It matters twice over. It completes the epic, and E03 closing is what releases four blocked rows of [I00:E04] and the whole of [I00:E05], so every other epic of the initiative is waiting behind it. It also carries [#63](https://github.com/m2ux/prosiform/issues/63): the absorbed-title comparison slugs the heading and reads the path segment raw, so any capitalised filename is headed twice, and the contract's own example of a document that must absorb is one that does not. AC7 is that behaviour, so the fix belongs here rather than in the deferred-debt epic, whose duplicate row has been withdrawn.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w04.md](w04.md) | The task's plan: the absorption test, the per-group shift it selects, the emission order, and the comparison both sides are slugged by |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#5 \[I00:E03\] Outline Hierarchy](https://github.com/m2ux/prosiform/issues/5) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W03 record | [Plus-one heading shift and Setext conversion](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-5-i00-e03-w03-plus-one-heading-shift) |
| Absorption defect | [#63 Title absorption: a slug compared with a path segment](https://github.com/m2ux/prosiform/issues/63) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
