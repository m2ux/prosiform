## Overview

The prototype is used as the tool agents in this workspace invoke, and what that use reveals changes the specification until it stops changing. Every surprise becomes a ledger entry reducible to a fixture; an accepted finding changes the design first, then the corpus, then the build. Per-file conversion metadata and the dispatch operator are explicit contract extensions within this refinement. The initiative ends when every entry is resolved or explicitly deferred and the design and corpus carry one tagged revision, which is the target the production build names.

## Problem

The worked example bundles a full copy of a real skill on a tagged revision, and nothing yet records what bundling does when agents rely on it for work.

- **A specification proven on one tree is still a hypothesis.**
  The example's mode bundles pass on the demonstrated revision, and the design still names its residual items as needing measured real-skill data before their defaults are revisited ([residual policy](https://github.com/m2ux/prosiform/blob/3ff368936aa577ef57bd43b7a2fae63c264a99dc/artifacts/planning/2026-10-17-prosiform-v1/design.md#L532-L537)).

- **Findings from the demonstration sit in planning prose.**
  The dispatch saving and the route that pushed a mode past the output budget were measured once and recorded beside the work that met them, so neither can be re-run or counted.

- **A corpus built beside an implementation tests what was implemented.**
  Fixtures accumulate from the work that needed them, so a construct real sources carry but nobody implemented has no fixture and produces no failure.

- **A surprise met mid-task has nowhere to go.**
  The agent is doing something else, so without a recorded place for a finding the cheapest action is a local workaround, and the design keeps its original claim.

- **A fix applied to the build leaves the contract wrong.**
  Correcting a bundling in code without changing the design leaves the design asserting the original behaviour, and the next implementation reads the design.

- **A moving contract cannot be implemented twice.**
  A corpus that changes under refinement gives a second implementation no fixed target and no revision it can be said to satisfy.

## Proposal

- **The prototype is the tool in use.**
  It is invoked from this workspace's skills, so the contract meets real sources and real agents rather than constructed examples.

- **The exposure set covers the example and the skills in use.**
  The example's mode entries and the workspace skills agents invoke are declared together, so the freeze needs both the demonstrated tree and real use.

- **The ledger records every run.**
  A bundling run is recorded with the source identities it bundled and its outcome, so how much the tool was used is a fact the ledger holds rather than an impression.

- **Every surprise becomes a ledger entry.**
  An entry carries its date, the invocation, the source identities, the observed result and the expected one, and a triage state naming whether it changes the design, fills a corpus gap, fixes a build defect, or changes nothing.

- **An entry is reducible to a fixture.**
  A capture tool reduces an entry's sources and invocation to the smallest fixture that still reproduces the observed result, so a finding becomes something that can be re-run.

- **A finding changes the design first.**
  The design is the contract; the corpus follows the design, and the build follows the corpus. Each revision cites the entry that motivated it.

- **An accepted finding becomes a row.**
  Rows are added to the revision epic as findings are accepted, so what remains is visible rather than implied.

- **Deferral is a recorded decision.**
  An entry not resolved before the freeze names what is deferred and why, and stays in the ledger for the stage that takes it.

- **A prerequisite list goes when bundling replaces it.**
  The example removed its prerequisite sections and states its compile command in its bootstrap. A workspace skill follows that pattern once a recorded bundling supplies what its list named, and a shortfall is a ledger entry rather than a silent loss.

- **Each run is measured against what it replaces.**
  A run record carries the bundled output size and the whole-file size of the sources it bundled, so the retrieval cost the proposal measured can be compared with the cost of bundling instead.

- **The freeze is a tag.**
  Design and corpus take one tagged revision, and the production build names that revision as its target. The demonstration's tag names a demonstrated revision and is not the freeze.

- **Source files own structural conversion settings.**
  Each contributing file supplies its settings through skill-compatible metadata, independent of the caller that selects it.

- **Entry files define their invocation.**
  A file declares its root and determines its bundle filename, so ordinary compilation needs only `pf <file>`.

- **A link states who compiles it.**
  A second operator marks the material a sub-agent compiles, and the entry document's metadata states what that mark means, so a dispatching skill says so in the bundle rather than in prose beside it.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/21) | Findings Ledger | AC1, AC2, AC9 | | |
| [E01](https://github.com/m2ux/prosiform/issues/22) | Specification Revision | AC3, AC4, AC8 | | |
| [E02](https://github.com/m2ux/prosiform/issues/195) | Merged Groups | AC3 | | ✓ |
| [E03](https://github.com/m2ux/prosiform/issues/187) | Repository Checks | AC10 | | |
| [E06](https://github.com/m2ux/prosiform/issues/218) | Document Metadata | AC3, AC12, AC13 | | ✓ |
| [E09](https://github.com/m2ux/prosiform/issues/242) | Dispatch Operator | AC3, AC15 | | ✓ |
| [E10](https://github.com/m2ux/prosiform/issues/257) | Repository Configuration | AC16 | | ✓ |
| [E13](https://github.com/m2ux/prosiform/issues/23) | Specification Freeze | AC5, AC6, AC7 | | |

## Acceptance Criteria

- [ ] **AC1.** A surprise met while bundling in real use is recorded with the evidence needed to reproduce it without the original session, as the ledger's entries show.
- [ ] **AC2.** A recorded finding is reducible to a corpus fixture that reproduces it, as the capture tool's reduction tests show.
- [ ] **AC3.** An accepted finding changes the design before the corpus or the build, as the revision history citing that finding shows.
- [ ] **AC4.** What remains unsettled is visible without reading the ledger whole, as the open-finding summary shows.
- [ ] **AC5.** Each ledger entry is resolved or carries a recorded deferral naming what is deferred and why, as the ledger's status summary shows.
- [ ] **AC6.** The design and the corpus carry one tagged revision that a production build can name as its target, as the tag shows.
- [ ] **AC7.** The specification is settled only after the tool has bundled each source in a declared exposure set holding both the worked example's mode entries and the skills this workspace's agents invoke, as the freeze check shows.
- [ ] **AC8.** A prerequisite section is removed only where a recorded bundling supplies what it named, and any shortfall is a ledger entry, as the removal records show.
- [ ] **AC9.** Each exposure-set source carries a bundled size recorded against the size of the same sources read whole, as the run records show.
- [ ] **AC10.** Each item the prototype initiative deferred and its product did not need is delivered or carries a recorded deferral, as the carried-debt epic rows show.

- [x] **AC12.** Linked sources retain their declared structural intent across supported entry and dependency selections, as the metadata conformance corpus demonstrates.

- [x] **AC13.** File-owned metadata supports file-only invocation, as the root-resolution and output-identity conformance suite demonstrates.

- [x] **AC15.** The refined contract supports a link whose material the reading agent compiles for a sub-agent, and an entry document declaring what that mark means, as the dispatch conformance suite demonstrates.

- [x] **AC16.** The repository holds the branch shape its delivery procedure assumes, with merge and deletion on its long-lived branches governed by the platform rather than by convention, as the protection settings show.

## Non-Goals

- It does not implement a production build.
- It does not add ontology inference, workflow execution or sentence-level substitution.
- It does not rewrite authored source structure.
- It does not add inline section composition or root inheritance from a reaching parent.
- It does not commit to a date for the freeze.
- It does not accept a finding by working around it in a source document.
- It does not open an issue or a pull request on another project.

## References

- **R1.** **Source.** [v1 design](https://github.com/m2ux/prosiform/blob/3ff368936aa577ef57bd43b7a2fae63c264a99dc/artifacts/planning/2026-10-17-prosiform-v1/design.md) — the specification this initiative settles, including the residual items it names as needing measured real-skill data.
- **R2.** [Planning decisions](https://github.com/m2ux/prosiform/blob/3ff368936aa577ef57bd43b7a2fae63c264a99dc/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) — why the prototype is used before a production build is committed to, and what marks the specification settled.
- **R3.** [Proposal](https://github.com/m2ux/prosiform/issues/1) — the scoped problem and the goal clauses these criteria trace to.

- **R4.** [Section Composition: Unicode Links Compose Content Within the Containing Section](https://github.com/m2ux/prosiform/issues/214) — the requirements for inline section composition, which this stage leaves to a later one.

- **R5.** **Source.** [Document Metadata: Per-File Settings Govern Linked Compilation](https://github.com/m2ux/prosiform/issues/216) — originating requirements for per-file conversion metadata.
- **R6.** **Source.** [File-owned invocation decisions](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/design.md) — confirmed metadata root and entry-derived output requirements.
- **R7.** **Source.** [Dispatch operator planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-24-242-i01-e09-dispatch-operator) — the operator, the metadata key and the published deferral form, with the decisions behind them.
- **R8.** [Parent Merge: Each File Groups the Links It Writes](https://github.com/m2ux/prosiform/issues/234) — grouping owned by the file that writes the link, a candidate finding the ledger accepts only where real use shows a need.
- **R9.** [Refinement scope record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-26-20-i01-replan) — the exposure set, the epics this stage does not take, and the Parent Merge epic, with the evidence behind each.

