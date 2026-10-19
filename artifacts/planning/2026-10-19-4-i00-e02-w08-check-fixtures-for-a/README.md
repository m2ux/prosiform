# I00:E02:W08 Check Fixtures for a Validation-Only Run - October 2026

> Task Plan - Created 2026-10-19

## Executive Summary

This record holds the local plan for a task raised during the delivery of [I00:E02] Walking Skeleton rather than planned with it. The corpus gains fixtures for a validation-only run: one declaring the run alone, one declaring it with an output file named, each expecting an exit status of zero, standard output holding nothing and no diagnostic, and the second establishing that the named file is never created. The task also adds the number sign to the characters a generated file heading escapes.

It matters because the criterion naming that run has gone unticked since the command was first delivered, and the reason has expired. When the row that covers it landed, nothing bundled, so a validation-only run validated nothing and a fixture for it would have declared an absent stage. Emission exists now, and the run produces exactly the result the criterion describes, so what remains is a fixture nobody has written rather than a gap in the instrument. It matters for the escaping because a generated file heading carries a path as its visible text, and a path segment ending in a space and a number sign closes that heading as an ATX closing sequence, taking the character out of the heading without a diagnostic. The task covers AC10, the last unticked criterion of the epic.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w08.md](w08.md) | The task's plan: what a manifest can state about a file the run must not create, the two fixtures and the source each runs over, and the escape set's addition |
| [validation.md](validation.md) | The checks as they were run: the corpus at the base and at the head, the run AC10 names, each check's procedure and result, and the observed failure of both fixtures when a validation-only run publishes |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#4 \[I00:E02\] Walking Skeleton](https://github.com/m2ux/prosiform/issues/4) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Initiative plan | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| W01 record | [Command interface, streams and exit statuses](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w01-command-interface-streams-and) |
| W04 record | [Whole-document emission under a filename heading](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w04-whole-document-emission-under) |
| W06 record | [Corpus run on every change](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-19-4-i00-e02-w06-corpus-run-on-every) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
