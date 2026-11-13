# Scorer Shell Reading — November 2026

> Hot-fix · Created 2026-11-13

## Executive Summary

The diagram-following scorer reads each session's shell commands lexically to decide whether the session ran `pf` and with what selection. Two valid shell forms are misread on `main`: an adjacent redirection such as `2>&1>out` invalidates the command that carries it, and a heredoc body is read as commands, so compiler-looking text inside it counts as a compile.

Both misreadings change a session's verdict, so a scored run can record a compile that never ran or miss one that did. Every run the eval commits, the real-use baseline among them, is scored by this reading, so it must match the shell before those runs are taken.

## Artifacts

| Artifact | What it holds |
| --- | --- |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F10] Scorer Shell Reading](https://github.com/m2ux/prosiform/issues/675) |
| Heredoc finding | [#676](https://github.com/m2ux/prosiform/issues/676) |
| Product integration | [#666](https://github.com/m2ux/prosiform/pull/666) |
| Scorer repair | [#674](https://github.com/m2ux/prosiform/pull/674) |
