## Overview

The prototype is used as the tool agents in this workspace invoke, and what that use reveals changes the specification until it stops changing. Every surprise becomes a ledger entry reducible to a fixture; an accepted finding changes the design first, then the corpus, then the build. Declared sources, selected presets and compiled dispatch targets form the contract baseline for this refinement. The initiative ends when every entry is resolved or explicitly deferred and the design and corpus carry one tagged revision, which is the target the production build names.

## Problem

The build has conformance fixtures and measured evaluation runs, while ordinary skill use lacks an integrated ledger connecting exposure, findings and revisions.

- **Fixture conformance does not measure ordinary use.**
  The contract requires measured fixture and real-skill data before numerical defaults are recalibrated ([residual policy](https://github.com/m2ux/prosiform/blob/6deca17d6b56c61f477c815da6eeecc3949d8ca1/artifacts/planning/2026-10-17-prosiform-v1/design.md#L794-L799)).

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
  A workspace skill states its declared entry invocation and sends its reader to bare `pf` for the guide. A prerequisite list is removed only after a recorded bundle supplies its required sources; a shortfall is a ledger entry.

- **Each run is measured against what it replaces.**
  A run record carries the bundled output size and the whole-file size of the sources it bundled, so the retrieval cost the proposal measured can be compared with the cost of bundling instead.

- **The freeze is a tag.**
  Design and corpus take one tagged revision, and the production build names that revision as its target. The demonstration's tag names a demonstrated revision and is not the freeze.

- **Source files own structural conversion settings.**
  Each contributing document declares its own presets, and the reference selecting it determines which of those presets govern its content.

- **Entry files define their invocation.**
  An entry names a declaring document with `pf <file>`. The invocation working directory supplies the entry base and the current CLI derives the run and bundle names.

- **A link states who compiles it.**
  A dispatch link names a separately compiled target bundle. The guide printed by bare `pf` states how its reader hands that bundle to a sub-agent.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/21) | Findings Ledger | AC1, AC2, AC9 | | |
| [E01](https://github.com/m2ux/prosiform/issues/22) | Specification Revision | AC3, AC4, AC8 | | |
| [E02](https://github.com/m2ux/prosiform/issues/195) | Merged Groups | AC11, AC16, AC17 | | ✓ |
| [E03](https://github.com/m2ux/prosiform/issues/187) | Repository Checks | AC10 | | |
| [E06](https://github.com/m2ux/prosiform/issues/218) | Document Metadata | AC12, AC13 | | ✓ |
| [E09](https://github.com/m2ux/prosiform/issues/242) | Dispatch Operator | AC14 | | ✓ |
| [E10](https://github.com/m2ux/prosiform/issues/257) | Repository Configuration | AC15 | | ✓ |
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

- [x] **AC11.** Each selected member of a merged group has an emitted heading recorded for that source, as grouping tests run by `make check` show.
- [x] **AC12.** A linked source is converted under its own selected presets, as entry and dependency CLI tests run by `make check` show.

- [x] **AC13.** No structural command-line setting is needed to compile a declaring entry, as invocation tests run by `make check` show.

- [x] **AC14.** A dispatch link names its target's compiled bundle in the published set, as dispatch CLI tests run by `make check` show.

- [x] **AC15.** The repository holds the branch shape its delivery procedure assumes, with merge and deletion on its long-lived branches governed by the platform rather than by convention, as the protection settings show.

- [x] **AC16.** Distinct members of one merged group resolve to distinct bundle destinations, as candidate-validation tests run by `make check` show.
- [x] **AC17.** Headings derived from paths or group slugs follow the profile's title-casing convention, as heading-rendering tests run by `make check` show.

## Non-Goals

- It does not implement a production build.
- It does not add ontology inference, workflow execution or sentence-level substitution.
- It does not rewrite authored source structure.
- It does not add inline section composition or root inheritance from a reaching parent.
- It does not commit to a date for the freeze.
- It does not accept a finding by working around it in a source document.
- It does not open an issue or a pull request on another project.

## References

- **R1.** **Source.** [Current contract](https://github.com/m2ux/prosiform/blob/6deca17d6b56c61f477c815da6eeecc3949d8ca1/artifacts/planning/2026-10-17-prosiform-v1/design.md) — the grammar and conformance requirements pinned by the merged build, against which real-use findings and the freeze are assessed.
- **R2.** [Planning decisions](https://github.com/m2ux/prosiform/blob/3ff368936aa577ef57bd43b7a2fae63c264a99dc/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) — why the prototype is used before a production build is committed to, and what marks the specification settled.
- **R3.** [[P00] Markdown Bundling: One Validated Document From Linked Sources](https://github.com/m2ux/prosiform/issues/1) — the originating proposal and its goal of a contract settled through real use.

- **R4.** [Section Composition: Unicode Links Compose Content Within the Containing Section](https://github.com/m2ux/prosiform/issues/214) — the historical proposal for section composition.

- **R5.** [Document Metadata: Per-File Settings Govern Linked Compilation](https://github.com/m2ux/prosiform/issues/216) — historical requirements for the first per-file metadata design.
- **R6.** [File-owned invocation decisions](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-10-23-218-derived-bundle-names/design.md) — historical root metadata and entry-derived output decisions.
- **R7.** [Dispatch operator planning record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-24-242-i01-e09-dispatch-operator) — historical dispatch operator, metadata and emission decisions.
- **R8.** [Parent Merge: Each File Groups the Links It Writes](https://github.com/m2ux/prosiform/issues/234) — the historical proposal for parent-owned grouping.
- **R9.** [Refinement scope record](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-26-20-i01-replan) — the exposure set, the epics this stage does not take, and the Parent Merge epic, with the evidence behind each.
- **R10.** [Current-contract alignment](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-05-project-18-alignment/source-review.md) — the confirmed contract basis and remaining criterion and exposure-set decisions.
