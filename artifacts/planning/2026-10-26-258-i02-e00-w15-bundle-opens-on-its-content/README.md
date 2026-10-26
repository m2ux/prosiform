# Bundle Opens on Its Own Content — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

Every bundle opened with a generated paragraph telling the agent to follow the selected entries, optionally extended by a `prosiform.dispatch` text. The instruction to follow an entry belongs in each source's own preamble, because it may change per bundle, so `pf` writes no such paragraph and the `dispatch` key goes with it. This row removes both outright, with the generated-input policy that read the paragraph and the candidate check that held it to the entries.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w15.md) | Scope, components and fixture outcomes |
| [Validation](validation.md) | Check results, the re-record diff check and the stale-wording search |

## Delivery Context

- Epic: I02 E00, issue #258; task W15.
- Task branch: `i02/e00/w15-bundle-opens-on-its-content`, cut from epic base `i02/e00/main` at `ad8f1a2a`; `6c51fe55` (W14) merged in before re-recording.
- Worktree: `.worktrees/i02-e00-w15`.
- Components: `src/prosiform`, `src/tests`, `checks`, `fixtures`, `example/work-tracker`, `scripts/render-diagram.py`, docs, `README.md` design pin; `design.md` on this branch.
- Ruling: the user's — `pf` emits no entry line, and the `prosiform.dispatch` key is removed with it; the `»` and `¬` operators stay.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#280](https://github.com/m2ux/prosiform/pull/280) |
