# Bundle Hand-Over — November 2026

> Hot-fix · Created 2026-11-17

## Executive Summary

A dispatching agent reads the guide to learn how to hand a bundle to a sub-agent. On `main` the guide says to give the bundle "with the inputs of the step that led there", which says neither whether the bundle travels as its path or its text nor which inputs travel with it.

The fix states the hand-over in the guide: the sub-agent is given the bundle file's path and reads it there, with the inputs the dispatching step states as given. Every bundle keeps the run-pf line, since it is how a reader reaches the guide to the symbols the bundle carries.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f13.md](f13.md) | The work item: the hand-over wording and the checks it carries |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |
| [agent-review.json](agent-review.json) | The agent review records of the delivering pull request's reviewed heads and bases |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F13] Bundle Hand-Over](https://github.com/m2ux/prosiform/issues/775) |
| Delivering pull request | [[F13] Bundle Hand-Over](https://github.com/m2ux/prosiform/pull/779) |
| Design | [Guide](../2026-10-17-prosiform-v1/design.md#guide) |

## Plan Changes

- **The run-pf line stays on every bundle.**
  The first delivery also dropped the instruction heading and the run-pf line from a bundle linking nothing outside it. The owner noted that a reader runs `pf` for the guide to the symbols any bundle carries, so that half was removed from the issue, the branch and the design. The issue's original body is kept as [a comment on it](https://github.com/m2ux/prosiform/issues/775#issuecomment-6948431160).
