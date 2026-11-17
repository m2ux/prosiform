# Comment Convention — November 2026

> Hot-fix · Created 2026-11-17

## Executive Summary

No document states what a docstring or comment in the Python build holds, so each change follows its neighbours, and docstrings restate rules other modules own: one rule change rewrites prose across most of `src/prosiform/`.

The fix states the convention in `src/README.md`: a rule is stated once, in the docstring of the unit that implements it; every other docstring states what its own unit does and names the rules it relies on by their owner; a comment states only why code is as it is.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [agent-review.json](agent-review.json) | The agent review records of the delivering pull request's reviewed heads and base |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F17] Comment Convention](https://github.com/m2ux/prosiform/issues/788) |
| Delivering pull request | [[F17] Comment Convention](https://github.com/m2ux/prosiform/pull/787) |
| Follow-on | [Comment Cleanup](https://github.com/m2ux/prosiform/issues/786) |
| Origin | [[F15] Diagram Link Text](../2026-11-17-783-f15-diagram-link-text/README.md) |
