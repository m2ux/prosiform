# Preset Alternatives — November 2026

> Initiative · Created 2026-11-12

## Executive Summary

A link's presets are fixed when its author writes them, so a document generic over a kind of work cannot be compiled for the kind an agent is handling. work-planner's `work-kind.md` shows the cost: it routes eight operations by an item's kind through a registration table the agent reads and applies at run time, unchecked by any compile.

This initiative lets a document declare one preset per kind as an alternative, and lets a deferred link hand the pick to the agent with a `?` title tag. `pf` answers `?` with each alternative and when to pick it; the agent compiles the one that fits, and the bundle holds that kind's routes alone. Compiling with no alternative or two fails with the same list, so a wrong pick stops the run rather than compiling the wrong route.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Design](design.md) | Alternatives, the `?` tag, the pick, routing pairs, the guide entry and the change surface |
| [Decisions](decisions.md) | Decisions from the design interview, defaults taken, and open questions |

## Links

| Resource | Link |
| --- | --- |
| Motivating case: work-planner `work-kind.md` | [workflow-server `workspace`](https://github.com/m2ux/workflow-server/blob/workspace/skills/work-planner/artifacts/work-kind.md) |
