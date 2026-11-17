# Bundle Hand-Over — November 2026

> Hot-fix · Created 2026-11-17

## Executive Summary

A dispatching agent reads the guide to learn how to hand a bundle to a sub-agent. On `main` the guide says to give the bundle "with the inputs of the step that led there", which says neither whether the bundle travels as its path or its text nor which inputs travel with it. Every bundle also opens with the instruction to run `pf`, including a bundle none of whose links leaves it, so a reader spends a call on a guide with nothing to say about that bundle.

The fix states the hand-over in the guide — the sub-agent is given the bundle file's path and reads it there, with the inputs the dispatching step states as given — and drops the instruction heading and the run-pf line from a bundle that links no document outside it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f13.md](f13.md) | The work item: the hand-over wording, the rule deciding the run-pf line and the checks it carries |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F13] Bundle Hand-Over](https://github.com/m2ux/prosiform/issues/775) |
| Design | [Link classification and resource handling](../2026-10-17-prosiform-v1/design.md#link-classification-and-resource-handling) |
