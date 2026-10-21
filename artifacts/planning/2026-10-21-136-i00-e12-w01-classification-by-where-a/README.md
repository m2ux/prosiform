# I00:E12:W01 Classification by Where a Reference Resolves — October 2026

> Task Plan · Created 2026-10-21

## Executive Summary

This record holds the local plan for the row that makes a reference's position decide what the bundle does with it. A local Markdown reference resolving to a document under the allowed source root is compiled into the bundle and rewritten to that document's destination; one resolving outside the root is emitted as the author wrote it and its target is never opened.

It matters because it is the row every other row of the epic waits on: the deferral, the resource rule, the self-reference rule and the root confinement each describe an exception to this classification, and none of them can be stated until the classification itself reads position rather than a mark.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w01.md](w01.md) | The task's plan: where classification is read, and what replaces the mark |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#136 \[I00:E12\] Positional Dependencies](https://github.com/m2ux/prosiform/issues/136) |
| Epic plan | [2026-10-21-136-i00-e12-positional-dependencies](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-136-i00-e12-positional-dependencies) |
| Design and decision | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
