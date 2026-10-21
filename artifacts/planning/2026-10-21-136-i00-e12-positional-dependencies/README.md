# I00:E12 Positional Dependencies — October 2026

> Epic Plan · Created 2026-10-21

## Executive Summary

This record holds the plan for the epic that makes a reference's position decide what the bundle does with it, and gives the author one mark that defers a compilation instead of requesting one. A local Markdown reference resolving under the allowed source root is compiled and rewritten; one resolving outside it is text; one the author marks is carried into the bundle with its mark and a root-relative destination, so an agent reading the bundle compiles it in a run of its own.

It matters because the previous rule asked an author to mark everything the bundle must carry, which made a forgotten mark a silent omission and stated inside the root what the root already said. The inversion keeps the character and spends it on something the design could not express before: a bundle that states its immediate context and leaves its deeper context reachable.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [joins.md](joins.md) | The rows that could share a pull request and keep their own, and why |

## Links

| Resource | Link |
| --- | --- |
| Epic issue | [#136 \[I00:E12\] Positional Dependencies](https://github.com/m2ux/prosiform/issues/136) |
| Initiative issue | [#2 \[I00\] Prototype Compiler](https://github.com/m2ux/prosiform/issues/2) |
| Design and decision | [2026-10-17-prosiform-v1](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-17-prosiform-v1) |
| Theme board | [Bundling](https://github.com/users/m2ux/projects/18) |
