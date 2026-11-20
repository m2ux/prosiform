# Capability Levels — November 2026

> Hot-fix · Created 2026-11-20

## Executive Summary

A sub-agent runs on whatever model starts it, so one model ran every stage of a run. A preset's `level` now names the capability a stage's work needs, the run's entry maps each level to a model in its `levels`, and `pf` publishes the resolved model as `on <model>` after every dispatch link, set line and pick line. The guide tells the dispatcher to start the sub-agent on it.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [f30.md](f30.md) | The work item: the preset fields, the run's level map and the published model |
| [test-results.md](test-results.md) | The checks run on the delivering branch and their results |
| [agent-review.json](agent-review.json) | The agent review records of the delivering pull request's reviewed heads and base |

## Links

| Resource | Link |
| --- | --- |
| Hot-fix issue | [[F30] Capability Levels](https://github.com/m2ux/prosiform/issues/827) |
| Delivering pull request | [[F30] Capability Levels](https://github.com/m2ux/prosiform/pull/828) |
