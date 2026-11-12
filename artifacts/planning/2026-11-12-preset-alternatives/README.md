# Preset Alternatives — November 2026

> Initiative · Created 2026-11-12

## Executive Summary

A link's presets are fixed when its author writes them, so a document generic over a kind of work cannot be compiled for the kind an agent is handling. work-planner's `work-kind.md` shows the cost: each of its body operations lists every kind's implementation in one step, and the agent applies the line for its item's kind as it reads, unchecked by any compile.

This initiative lets a document declare one preset per kind as an alternative, and lets a deferred link hand the pick to the agent with a `?` title tag. `pf` answers `?` with each alternative and when to pick it; the agent compiles the one that fits, and the bundle holds that kind's routes alone. Compiling with no alternative or two fails with the same list, so a wrong pick stops the run rather than compiling the wrong route.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Design](design.md) | Alternatives, the `?` tag, the pick, routing pairs, the guide entry and the change surface |
| [Decisions](decisions.md) | Decisions from the design interview and Plan mode, the dependency check, defaults taken and open questions |
| [Goal trace](goal-trace.md) | The goal clauses traced to criteria, epics and the design, with the ranked gaps |
| [Board placement](board.json) | Placement on the Python board and the field options added, existing ones preserved |
| [Initiative draft](initiative-body.md) | The initiative goal, criteria and epic coverage |
| [Declared Alternatives epic draft](e00-body.md) | E00's rows and criteria for alternatives, the exactly-one rule and routing pairs |
| [Agent Pick epic draft](e01-body.md) | E01's rows and criteria for the `?` tag, the guide entry and the router fixture |
| [Design work item](e00/w00.md) | The v1 design stating alternatives and the agent's pick |
| [Choice line work item](e00/w01.md) | The `choice` key and its refusals |
| [Exactly-one work item](e00/w02.md) | The exactly-one rule, its failure and the silent unpicked alternative |
| [Routing pairs work item](e00/w03.md) | Routing pairs quiet in both `subst` warnings, and the stale-route check |
| [Alternatives documentation work item](e00/w04.md) | The pages stating alternatives |
| [Pick tag work item](e01/w01.md) | `?` on deferred links, and its refusals on compiled ones |
| [Deferred pick work item](e01/w02.md) | The pick checks on a deferred link to alternatives |
| [Guide and router work item](e01/w03.md) | The guide entry and the end-to-end router fixture |
| [Pick documentation work item](e01/w04.md) | The pages stating the `?` tag |
| [Agent-pick eval work item](e01/w05.md) | The eval workflow in which a headless agent resolves a `?` pick |
| [Agent-pick run work item](e01/w06.md) | The live run and baseline of the agent-pick workflow |

## Links

| Resource | Link |
| --- | --- |
| Initiative: [I15] Preset Alternatives | [#707](https://github.com/m2ux/prosiform/issues/707) |
| Epic: [I15:E00] Declared Alternatives | [#708](https://github.com/m2ux/prosiform/issues/708) |
| Epic: [I15:E01] Agent Pick | [#709](https://github.com/m2ux/prosiform/issues/709) |
| Motivating case: work-planner `work-kind.md` | [workflow-server `workspace`](https://github.com/m2ux/workflow-server/blob/workspace/skills/work-planner/artifacts/work-kind.md) |
