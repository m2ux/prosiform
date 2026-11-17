# Dispatch Picks — November 2026

> Hot-fix · Created 2026-11-17

## Executive Summary

A dispatch link compiles its target up front, so on `main` it refuses the pick token `?`: no agent is left to pick among the target's alternatives. A route that dispatches one stage under each of its alternatives writes a link for each and restates the choice the stage already declares.

With this hot-fix, a `⇉` link carrying `?` compiles its target once for each alternative and lists each bundle beside its choice line in a `⇉ Dispatch Pick` sub-section, so the agent that dispatches hands on the one its work calls for. A `⫽` link carrying `?` stays refused.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f12.md](f12.md) | The work item: the confirmed design, the design points decided, and the checks it carries |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F12] Dispatch Picks](https://github.com/m2ux/prosiform/issues/774) |
| Design | [design.md](../2026-10-17-prosiform-v1/design.md) |

## Plan Changes

None: the session applied no plan change and held none.
