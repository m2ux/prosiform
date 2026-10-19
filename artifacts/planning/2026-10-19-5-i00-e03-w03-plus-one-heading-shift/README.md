# I00:E03:W03 Plus-One Heading Shift and Setext Conversion - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for the third row of [I00:E03] Outline Hierarchy. Every emitted source heading in a file group moves down exactly one level, inside retained containers as elsewhere, preserving visible text and relative depth. A group whose title the file heading absorbed keeps its source levels instead, the file heading having taken the level the shift makes room for. A Setext heading is converted to the equivalent ATX heading carrying the same visible text and inline semantics.

It matters for three criteria rather than its own two. AC3 and AC4 are this row's. AC1 is [W02](https://github.com/m2ux/prosiform/pull/72)'s and was left unticked, because its container half cannot be published until this shift exists: showing a container-nested heading at a correct level needs a group shift of zero, which needs an absorbed title, which needs the whole document selected, and a whole-document selection has no boundary to demonstrate. The fixture is already written and awaits this row.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w03.md](w03.md) | The task's plan: the shift for each heading form, the Setext conversion, and the criterion W02 left for this row |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#5 \[I00:E03\] Outline Hierarchy](https://github.com/m2ux/prosiform/issues/5) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W02 record | [Eligible section extraction and boundaries](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-5-i00-e03-w02-eligible-section-extraction-and) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
