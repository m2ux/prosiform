# Review

The goal trace, the threats checked against the drafts, and the independent task pairs the dependency check reported.

## Goal Trace

Each confirmed goal clause, the initiative criterion that makes it true, and the epic whose criteria deliver it. Clause identifiers are those in [Decisions](decisions.md).

| Clause | Initiative | Criterion | Epic | Epic criteria |
| --- | --- | --- | --- | --- |
| G1 | I00 | AC1 | E03 Dependency Closure | AC1, AC2 |
| G2 | I00 | AC2 | E04 Destination Identity | AC3, AC4 |
| G2 | I00 | AC3 | E03 Dependency Closure | AC3 |
| G3 | I00 | AC4 | E05 Validation Gate | AC2 |
| G4 | I00 | AC5 | E02 Outline Hierarchy | AC1–AC7 |
| G5 | I00 | AC6 | E05 Validation Gate | AC1, AC3–AC7 |
| G5 | I00 | AC10 | E03 Dependency Closure | AC7 |
| G6 | I00 | AC7 | E01 Walking Skeleton | AC1–AC6 |
| G7 | I00 | AC8 | E00 Corpus Harness | AC1–AC4 |
| G7 | I00 | AC9 | E06 Corpus Conformance | AC1–AC4 |
| G3 | I01 | AC1 | E00 Parser Verdict | AC1–AC6 |
| G3 | I01 | AC2 | E01 Source-Range Adapter | AC1–AC4 |
| G5 | I01 | AC3 | E01 Source-Range Adapter | AC5 |
| G4 | I01 | AC4 | E02 Profile and Outline | AC1–AC6 |
| G1 | I01 | AC5 | E03 Closure and Budgets | AC1–AC7 |
| G2 | I01 | AC6 | E04 Destination Identity | AC1–AC5 |
| G5 | I01 | AC7 | E05 Validation and Delivery | AC1–AC6 |
| G7 | I01 | AC8 | E06 Differential Conformance | AC1 |
| G7 | I01 | AC9 | E06 Differential Conformance | AC2–AC4 |

- Every initiative criterion traces to a clause, and every clause is made true by at least one criterion.
- G6 is made true by I00 AC7 alone. The production build inherits that property through the corpus rather than restating it, because a source needing added markup would fail the fixtures taken from unmodified workspace skills.

## Source Alignment

The criteria of both initiatives answer to the design, which both bodies mark as a source. The upstream assessment is a marked source of I01 alone, because only its parser gates answer to it.

- Each mandatory parser viability gate the design states is answered by I01 AC1, and the route for a failed gate by the epic criterion behind it.
- The design's deferral of upstream action is held by I01's Non-Goals, which exclude opening an issue or pull request on another project.
- The design's residual policy details — the additional URI pass-through schemes and the numerical limit calibration — are stated as open in the design and are carried as Open Questions on the epics that would settle them, not as criteria.

## Threats

- **Consumers.**
  The workspace skills are the intended consumer, and their prerequisite lists become redundant once compositions replace them. Refactoring those skills is outside both initiatives and is raised separately when a build exists to refactor against.
- **Silent failures.**
  Every path the design fails closed on has a corpus fixture asserting the failure, its error code and the absence of output. A fail-closed path with no fixture is reported by the conformance report's uncovered list rather than passing silently.
- **Measurement.**
  The baseline is the evidence recorded in [Decisions](decisions.md), measured at commit `acac85867ca963df00251e4cf00a4db11b14bf24` before any of this work starts. The instrument is the corpus runner, which decides results from fixture declarations and names no implementation, so it is independent of both builds.
- **Version skew.**
  The corpus is produced by one initiative and consumed by the other. The differential run and the exact dependency pins are what keep the two builds and the corpus in agreement; a fixture changed to accommodate the production build is a recorded decision rather than an edit.
- **In-flight work.**
  The repository holds no implementation, so nothing in flight alters the ground this plan stands on.

## Independent Task Pairs

The dependency check reports task pairs within one epic where neither depends on the other and neither names the other in Joins. Each is recorded here with why it takes its own pull request.

| Pair | Why it is not joined |
| --- | --- |
| I01 E00 W01, W02, W03 | Each reproducer pins a different parser capability, and each result is read on its own into the gate report. One pull request per reproducer keeps a failed gate attributable to the evidence that failed it. |
| I01 E01 W02, W03 | Edit application and the suppression signal touch different parser surfaces, and the suppression signal's shape depends on the route the gate report records, so joining them would couple an edit mechanism to an undecided interface. |

Every other pair in every epic is ordered by a dependency.

## Checks

The checks run against the plan, and what each observed.

### Dependency Check

`deps.py` run over each initiative body and all seven of its epic bodies.

- Both initiatives report no problem: no overbroad whole-epic dependency, no backward reference, no duplicated or implied edge, and no numbering that departs from start order.
- I00's whole-epic edges are E05 on E04 and E06 on E05; every other ordering lives in the task graph.
- I01's whole-epic edges are E01, E02, E03 and E04 on E00, E05 on E04, and E06 on E05.
- I00's longest chain is 18 steps, from the fixture manifest to the independence check. I01's twelve longest chains are 15 steps, each passing through the gate report.
- The independent task pairs it reported are recorded above.

### Body Format Check

`format.py` run over every published issue, each epic against its initiative and each initiative against all seven of its epics.

- All sixteen issues report no mechanical fix, no metadata change to apply and no finding to decide.
- Each epic criterion is delivered by at least one task row, and each initiative criterion by at least one epic row.

### Goal Trace

The trace table above, built from the confirmed clauses and the drafted bodies.

- Every clause is made true by at least one initiative criterion, and every initiative criterion traces to a clause.
- No criterion is delivered by an epic whose own criteria leave it partly unmet.
