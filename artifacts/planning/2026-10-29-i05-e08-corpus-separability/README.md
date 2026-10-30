# I05:E08 Corpus Separability — October 2026

> Epic planning · Created 2026-10-29

## Executive Summary

This epic makes the diagram-following eval able to tell its forms apart. The committed baseline is 30 cells at 5 of 5 — every cell saturated — so a report can detect only a whole-cell collapse and cannot say whether bundling helps, whether the diagram helps, or whether a branch is resolved by following a link.

It raises the corpus's difficulty until a default run produces cells below 1.0, then commits a four-form baseline drawn from it with its report and measured cost. Both were deferred out of I05:E01, whose own remaining row is the refused-run guard that is stub-testable today.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [W01 work item](w01.md) | Scenarios that reach every failure class the scorer defines |
| [W02 work item](w02.md) | The every-form baseline drawn from the harder corpus, the dispatch scenarios among them |

## Design

- **Difficulty comes from the scenarios, not the workflows alone.** A workflow's diagram, prose and linked forms are the product under test; a scenario is what makes a mistake possible. Each failure class needs a scenario on which a plausible misreading produces it: a second decision to mis-branch at, a loop long enough to miscount, a state reachable only through a link, and a distractor state no edge leads to.
- **Every class reachable.** A class no scenario can produce measures nothing, so the corpus test holds each of the seven classes and `errored` to at least one scenario.
- **The baseline is the measure of success, not the count of scenarios.** The epic is done when a committed default-matrix baseline carries a four-form cell below 1.0. A harder corpus that still saturates has not achieved the goal.
- **The cost is measured, not estimated.** The three-form run recorded USD 4.0068 over 150 sessions; the four-form figure is unrecorded until a run completes.

## Decisions

- **Split from I05:E01, with the corpus question answered.** W09 bundled the refused-run guard with the paid baseline, and its Open Question asked whether a harder corpus was that task or another. The guard stays on I05:E01 as AC21; the baseline, the harder corpus and the measured cost move here. (User, 2026-10-29.)
- **The harder corpus belongs with the baseline, not to a further epic.** A four-form baseline on the present corpus would add a column of 100% cells and settle nothing, so the corpus change and the baseline are one epic. (User, 2026-10-29.)
- **Priority 6.** Every row extends `evals/diagram-following/workflows`, which I05:E07 W01 also extends, and both follow I05:E01, so this epic takes the number below E07's seven. (Planning, 2026-10-29.)
- **The refused-run guard stays on I05:E01.** That guard is stub-testable today, so it needs no paid run and no corpus change, and holding E01 open for it alone is the cheapest way to close the epic. (User, 2026-10-29.)
- **The dispatch scenarios' baseline joins this row.** I05:E07's W03 was the dispatch scenarios' own baseline, and `report.py` writes `baseline.json` whole, so a dispatch run and this epic's run cannot each commit one: whichever ran second would replace the first. W02 therefore runs the one default matrix over the hardened corpus and carries every form the matrix runs, the dispatch scenarios' compiled and authored forms among them, and E07 closes without a baseline of its own. W02 takes `E07:W02` as a prerequisite, since the dispatch rows and their checks must land before a run measures them, and AC6 states the dispatch rate the baseline must carry. (User, 2026-10-30.)

## Links

| Resource | Link |
| --- | --- |
| Epic | [I05:E08 Corpus Separability](https://github.com/m2ux/prosiform/issues/403) |
| Initiative | [I05 Ad Hoc Enhancements](https://github.com/m2ux/prosiform/issues/327) |
| Parent epic | [I05:E01 Diagram Following](https://github.com/m2ux/prosiform/issues/333) — the eval this epic measures |
| Superseded record | [I05:E01 W09 plan](../2026-10-27-333-i05-e01-diagram-following-eval/w09.md) — the row these two were deferred out of |
