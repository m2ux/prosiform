# Command Blocks — November 2026

> Hot-fix · Created 2026-11-08

## Executive Summary

Skills write each command as a parameterised block whose parameters are links to their definitions: a paragraph opened by `<big><pre>` and closed by `</pre></big>`. Because `<big>` opens the line, CommonMark reads the block as a paragraph carrying inline HTML, so the links inside parse and render as links. 117 such blocks exist across the work-planner skill, [Compute Board Queue](https://github.com/m2ux/workflow-server/blob/workspace/skills/work-planner/artifacts/board-queue.md#compute-board-queue) among them.

`pf` refuses every one with `E_RAW_HTML`. Link discovery already reads the links; only the profile's inline HTML refusal stops the run. With the block removed, the same section fails a second way: `E_UNEXPECTED_INTERNAL_ERROR` from the link rewrite, which counts two uses where the emitter finds three places to edit. This hot-fix accepts the wrapper and fixes the rewrite, so the section compiles.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Issue body](issue-body.md) | The hot-fix body, ready to raise |
| [Decisions](decisions.md) | The confirmed scope, the release and the acceptance route |

## Links

| Resource | Link |
| --- | --- |
| Profile refusal | `src/prosiform/profile.py`, `html_refusal` and `inline_refusals` |
| Rewrite failure | `src/prosiform/rewrite.py`, the `Unrewritable` raised on a use-count mismatch |
| Profile statement | `docs/sources.md#the-profile` |
| Versioning | `docs/versioning.md#what-the-numbers-mean` |
