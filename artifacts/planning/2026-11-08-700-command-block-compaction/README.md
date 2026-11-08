# Command Block Compaction — November 2026

> Hot-fix · Created 2026-11-08

## Executive Summary

F07 lets `pf` carry a skill's command blocks as written: a `<big><pre>` wrapper, HTML entities and bold parameter links, all of which serve a renderer. A bundle is read by an agent, so this hot-fix emits each command block as its linked Markdown alone, while the source keeps the rendered form.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Issue body](issue-body.md) | The published hot-fix body |
| [Decisions](decisions.md) | The confirmed compaction, its scope, the release and a collision with another plan |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | https://github.com/m2ux/prosiform/issues/700 |
| Python board | https://github.com/users/m2ux/projects/18 |
| F07 record | [2026-11-08-697-command-blocks](../2026-11-08-697-command-blocks/README.md) |
