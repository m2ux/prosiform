# Review

The goal trace, the threats checked against the drafts, and the independent task pairs the dependency check reports.

## Goal Trace

Each confirmed goal clause, the initiative criterion that makes it true, and the epic whose criteria deliver it. Clause identifiers are those in [Decisions](decisions.md).

| Clause | Initiative | Criterion | Epic | Epic criteria |
| --- | --- | --- | --- | --- |
| G1 | I00 | AC1 | E04 Dependency Closure | AC1, AC2, AC9, AC10 |
| G2 | I00 | AC2 | E05 Destination Identity | AC3, AC4 |
| G2 | I00 | AC3 | E04 Dependency Closure | AC3 |
| G3 | I00 | AC4 | E06 Validation Gate | AC2 |
| G4 | I00 | AC5 | E03 Outline Hierarchy | AC1–AC7 |
| G5 | I00 | AC6 | E06 Validation Gate | AC1, AC3–AC9 |
| G5 | I00 | AC10 | E04 Dependency Closure | AC7 |
| G6 | I00 | AC7 | E02 Walking Skeleton | AC1–AC8 |
| G7 | I00 | AC8 | E01 Corpus Harness | AC1–AC4 |
| G7 | I00 | AC9 | E07 Corpus Conformance | AC1–AC4 |
| G1 | I00 | AC11 | E08 Field Deployment | AC1, AC4 |
| G5 | I00 | AC12 | E08 Field Deployment | AC2, AC3, AC5 |
| G7 | I00 | AC13 | E00 Project Foundation | AC2–AC4 |
| G1 | I00 | AC14 | E04 Dependency Closure | AC8 |
| G8 | I01 | AC1 | E00 Findings Ledger | AC1, AC2 |
| G8 | I01 | AC2 | E00 Findings Ledger | AC3, AC4 |
| G8 | I01 | AC3 | E01 Specification Revision | AC1, AC2 |
| G8 | I01 | AC4 | E01 Specification Revision | AC3, AC4 |
| G8 | I01 | AC5 | E02 Specification Freeze | AC1, AC2 |
| G7 | I01 | AC6 | E02 Specification Freeze | AC3 |
| G8 | I01 | AC7 | E02 Specification Freeze | AC4 |
| G8 | I01 | AC8 | E01 Specification Revision | AC5, AC6, AC7 |
| G8 | I01 | AC9 | E00 Findings Ledger | AC7 |
| G3 | I02 | AC1 | E00 Parser Verdict | AC1–AC6 |
| G3 | I02 | AC2 | E01 Source-Range Adapter | AC1–AC4 |
| G5 | I02 | AC3 | E01 Source-Range Adapter | AC5 |
| G4 | I02 | AC4 | E02 Profile and Outline | AC1–AC6 |
| G1 | I02 | AC5 | E03 Closure and Budgets | AC1–AC7 |
| G2 | I02 | AC6 | E05 Destination Identity | AC1–AC5 |
| G5 | I02 | AC7 | E05 Validation and Delivery | AC1–AC6 |
| G7 | I02 | AC8 | E06 Differential Conformance | AC1 |
| G7 | I02 | AC9 | E06 Differential Conformance | AC2–AC4 |
| G8 | I02 | AC10 | E01 Source-Range Adapter | AC6 |

- Every initiative criterion traces to a clause, and every clause is made true by at least one criterion.
- Two epic criteria serve no initiative criterion of their own: the foundation epic's layout and README, and the adapter epic's production tree and workspace. Each is a condition the epics after them rely on rather than an outcome the initiative is judged by.
- G6 is made true by I00 AC7 alone. The production build inherits that property through the corpus rather than restating it, because a source needing added markup would fail the fixtures taken from unmodified workspace skills.
- G8 was added to the proposal when the decision to use the Python build for an extended period was taken. Without it, the refinement initiative's criteria would trace to no clause.

## Stage Order

The three initiatives run in series, and each boundary is a dependency a task row names rather than an assumption.

- I00 opens with the repository's foundation and ends with a build that passes the corpus and is installed for agents to invoke. The foundation creates the corpus, prototype and documentation trees only; the production tree, workspace and toolchain are a first row of I02 E01, and I00 carries a Non-Goal excluding them. I01 E00 W01 depends on I00 E08 W03, so the ledger opens once there is something in use to record findings from.
- I01 ends with a tagged revision of the design and corpus. I02 E01 W01 depends on I01 E02 W02, so every implementing epic of the production build waits on the freeze.
- I02 E00, the parser verdict, depends on neither. Its reproducers test a parser, not the specification, so the largest unknown in the production build can be answered while the refinement stage runs.

## Source Alignment

The criteria of all three initiatives answer to the design, which each body marks as a source. The upstream assessment is a marked source of I02 alone, because only its parser gates answer to it.

- Each mandatory parser viability gate the design states is answered by I02 AC1, and the route for a failed gate by the epic criterion behind it.
- The design's deferral of upstream action is held by I02's Non-Goals, which exclude opening an issue or pull request on another project.
- The design's agent delivery contract is answered by I00 AC12 and the epic criteria behind it, and again by I02 AC7.
- The design's residual policy details — the additional URI pass-through schemes and the numerical limit calibration — are stated as open in the design. The scheme allowlist is an Open Question on the epic that needs it; the limit calibration is the kind of measured revision I01 exists to produce.

## Threats

- **Consumers.**
  The workspace skills are the intended consumer. Their prerequisite sections are removed during the refinement stage as bundling replaces them, each removal gated on a recorded run that supplied what the section named. Nothing else about those skills is restructured, and the initiative carries a Non-Goal saying so.
- **Silent failures.**
  A failed run halts the caller; reading the sources instead is unsupported, so a failure cannot be absorbed without a ledger entry. Every path the design fails closed on has a corpus fixture asserting the failure, its error code and the absence of output. A fail-closed path with no fixture is reported by the conformance report's uncovered list, which is regenerated on each revision so a clause added during refinement cannot hide.
- **Measurement.**
  Bundling is measured against what it replaces: each run records its bundled size and the size of the same sources read whole, and the stage is not settled until every exposure-set source carries that pair. The baseline is the evidence recorded in [Decisions](decisions.md), measured at commit `acac85867ca963df00251e4cf00a4db11b14bf24` before any of this work starts. The instrument is the corpus runner, which decides results from fixture declarations and names no implementation, so it is independent of both builds. The freeze is judged by the ledger's status summary, which is derived from the ledger rather than maintained beside it.
- **Version skew.**
  The corpus changes throughout I01 and is fixed by the freeze tag. The production build names that tag, the differential run compares the two builds against it, and exact dependency pins hold the parser behaviour the profile rests on. A fixture changed to accommodate the production build is a recorded decision rather than an edit.
- **Open-ended refinement.**
  I01 commits to no end date, which is one of its Non-Goals. The deferral path is what stops a single unresolved finding holding the stage open, and the open-finding summary is what makes the remaining distance visible while it runs.
- **In-flight work.**
  The repository holds no implementation, so nothing in flight alters the ground this plan stands on.

## Independent Task Pairs

The dependency check reports task pairs within one epic where neither depends on the other and neither names the other in Joins. Each is recorded here with why it takes its own pull request.

| Pair | Why it is not joined |
| --- | --- |
| I01 E00 W02, W03 | Fixture reduction and the run record both extend the ledger, but one is a tool that rewrites sources and the other is a schema addition read by the freeze check. Separate pull requests keep a reduction defect from blocking the exposure measure. |
| I01 E01 W02, W03, W04 | Traceability regeneration changes the conformance report, the open-finding summary reads the ledger, and prerequisite removal changes source documents. Three subjects with no shared code, so one failing should not hold the others back. |
| I02 E00 W01, W02, W03 | Each reproducer pins a different parser capability, and each result is read on its own into the gate report. One pull request per reproducer keeps a failed gate attributable to the evidence that failed it. |
| I02 E01 W02, W03 | Edit application and the suppression signal touch different parser surfaces, and the suppression signal's shape depends on the route the gate report records, so joining them would couple an edit mechanism to an undecided interface. |

| I00 E07 W02, W03, W04, W05 | Four rows of one epic touching four surfaces: the transport wrapper, the documented invocation, the released-version report and the entry-destination stream. Each is a separate deliverable a caller can read on its own, and a defect in one should not hold the rest out of the epic base. |
| I00 E08 W01, W02, W03, W04, W05 | Delivered as five pull requests. W01 and W02 are disjoint in components — the bundle assembly and the candidate against the source read and the command — so neither gains from sharing a branch, and W05 corrects a defect of a closed epic that is unrelated to the rest. |
| I00 E09 W01, W02, W03, W04, W05, W06 | The epic's rows are an example tree, structural ancestors, grouping, a depth-overflow refusal and a measured budget. They share no component and each produces evidence read on its own, so one pull request per row keeps a failing criterion attributable to the row that failed it. |
| I00 E10 W03, W04, W05 | The independence check, the installation claims and the internal-error outcome are three separate observations of the delivered build. W04 and W05 share a pull request; W03 is a check of its own and takes one. |
| I00 E11 W01–W15 | The deferred-debt epic's rows are unrelated defects collected from across the initiative, sharing no component and no criterion. The epic ships in waves ([D46](decisions.md)), and a wave is a set of rows dispatched together rather than a set sharing one pull request. |

Every other pair in every epic is ordered by a dependency.

The Joins column states the rows that **share one pull request**, which the skill defines at `artifacts/epic-issue-body.md`. It is not a statement that two rows may run concurrently. A pair that will not share a pull request is recorded above instead, and its cell is empty. [D52](decisions.md) records the correction and the four delivered rows whose cells said otherwise.

## Checks

The checks run against the plan, and what each observed.

### Dependency Check

`deps.py` run over each initiative body and all of its epic bodies.

- All three initiatives report no problem: no overbroad whole-epic dependency, no backward reference, no duplicated or implied edge, and no numbering that departs from start order.
- I00's whole-epic edges are E06 on E05, E07 on E06 and E08 on E06; every other ordering lives in the task graph. The foundation epic binds the later ones through task edges rather than a whole-epic edge, because the corpus harness's first row needs the check commands but not the integration job.
- I01 carries no whole-epic edge. Its ordering is entirely in the task graph, because the freeze needs the run record while the revision epic does not.
- I02's whole-epic edges are E01, E02, E03 and E04 on E00, E05 on E04, and E06 on E05.
- I00's two longest chains are 21 steps, sharing eighteen rows and diverging at the validation gate into conformance and into deployment. I01's longest chain is 6 steps, from the ledger format to the tagged revision. I02's twelve longest chains are 15 steps, each passing through the gate report.
- The independent task pairs it reported are recorded above.

### Body Format Check

`format.py` run over every published issue, each epic against its initiative and each initiative against all of its epics.

- All twenty-three issues report no mechanical fix, no metadata change to apply and no finding to decide.
- Each epic criterion is delivered by at least one task row, and each initiative criterion by at least one epic row.

### Goal Trace

The trace table above, built from the confirmed clauses and the published bodies.

- Every clause is made true by at least one initiative criterion, and every initiative criterion traces to a clause.
- No criterion is delivered by an epic whose own criteria leave it partly unmet.
