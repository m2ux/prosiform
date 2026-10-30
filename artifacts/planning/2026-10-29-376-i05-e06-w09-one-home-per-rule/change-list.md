# Change List — I05:E06 W09

## Applied

- **Shared rules homed in the conventions.**
  `Command result`, `Helper result` and the lagging-list clause of `Write confirmation` state once in `example/work-planner/conventions.md`, and the 61 identical step sentences, the 6 helper sentences and the 4 lag statements become links naming those anchors.
- **The dispatch rules resolve to one home.**
  `rules.md` `Execution` gains the sub-agent parenthetical the guidelines' Modes section added, and that section links it instead of restating the call and dispatch rules.
- **Repeated step sequences collapse into shared operations.**
  `Copy Board Template`, `Run Delivery Planner`, `Render Standup Report`, `Run Closure Gate` and the reuse of `Read Delivery Branches` replace the copies in `board.md`, `delivery-plan.md`, `standup-report.md`, `issue.md` and `delivery-branches.md`.
- **The breakdown-prose rule moves to its shared home.**
  `Breakdown Prose` states once in `issue-body.md`; the epic and initiative body files link it.
- **Both rule files gain sections.**
  `conventions.md` and `rules.md` state each entry under its own `##` heading, so a link names the entry it means rather than opening the file.
- **Bundles regenerate.**
  Ten usage-example expected bundles are rewritten by the corpus tooling from the build under test.
- **Checks recorded.**
  Every repository target passes; `validation.md` records the ownership matrix, the five subject dispositions and each result.
- **Pull request #394 delivers the task.**
  It merges the validated head into `i05/e06/main` at `2602d4540ed5ae0f218b8bb29a317f1eea3eb91c`, and epic #376 links W09 to it. The epic body keeps AC9 and AC10 unticked: the epic's own review ticks its criteria at closure.

## Held

- **Authoring guard integration.**
  `make check` still does not run `make authoring`. W10 owns that wiring, and this task leaves it.
- **Splits.**
  No file the size report names is split. Each holds one subject, recorded with its reason in `validation.md`; splitting for size alone is refused.
