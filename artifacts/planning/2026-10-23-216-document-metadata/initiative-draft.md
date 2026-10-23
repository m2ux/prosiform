## Overview

The prototype is used as the tool agents in this workspace invoke, and what that use reveals changes the specification until it stops changing. Every surprise becomes a ledger entry reducible to a fixture; an accepted finding changes the design first, then the corpus, then the build. Authored section composition and per-file conversion metadata are explicit contract extensions within this refinement. The initiative ends when every entry is resolved or explicitly deferred and the design and corpus carry one tagged revision, which is the target the production build names.

## Problem

The behavioural contract has been written and reviewed, and nothing has yet bundled a real instruction set for an agent carrying out the procedure it describes.

- **A specification written before use is a hypothesis.**
  The design states its invariants against constructed examples, and names its own residual items as needing measured fixture and real-skill data before their defaults are revisited ([residual policy](https://github.com/m2ux/prosiform/blob/3ff368936aa577ef57bd43b7a2fae63c264a99dc/artifacts/planning/2026-10-17-prosiform-v1/design.md#L532-L537)).

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
  A skill's prerequisite section names whole documents, coarsely but completely. It is removed once a recorded bundling supplies what it named, and anything the bundling failed to supply is a ledger entry rather than a silent loss. In its place the skill's own text names the invocation that bundles them, so an agent is told to bundle rather than left to decide.

- **Each run is measured against what it replaces.**
  A run record carries the bundled output size and the whole-file size of the sources it bundled, so the retrieval cost the proposal measured can be compared with the cost of bundling instead.

- **The freeze is a tag.**
  Design and corpus take one tagged revision, and the production build names that revision as its target.

- **Section composition is an explicit refinement.**
  Reserved Unicode links compose fragments within their containing sections, with occurrence identity, source context, bounded expansion and staged deferral governed by the declared contract.

- **Source files own structural conversion settings.**
  Each contributing file supplies its settings through skill-compatible metadata, independent of the caller that selects it.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/prosiform/issues/21) | Findings Ledger | AC1, AC2, AC9 | | |
| [E01](https://github.com/m2ux/prosiform/issues/22) | Specification Revision | AC3, AC4, AC8 | | |
| [E02](https://github.com/m2ux/prosiform/issues/195) | Merged Groups | AC3 | | ✓ |
| [E03](https://github.com/m2ux/prosiform/issues/187) | Carried Debt | AC10 | | |
| [E04](https://github.com/m2ux/prosiform/issues/215) | Section Composition | AC3, AC11 | | |
| [E06](https://github.com/m2ux/prosiform/issues/218) | Document Metadata | AC3, AC12 | | |
| [E07](https://github.com/m2ux/prosiform/issues/23) | Specification Freeze | AC5, AC6, AC7 | | |

## Acceptance Criteria

- [ ] **AC1.** A surprise met while bundling in real use is recorded with the evidence needed to reproduce it without the original session, as the ledger's entries show.
- [ ] **AC2.** A recorded finding is reducible to a corpus fixture that reproduces it, as the capture tool's reduction tests show.
- [ ] **AC3.** An accepted finding changes the design before the corpus or the build, as the revision history citing that finding shows.
- [ ] **AC4.** What remains unsettled is visible without reading the ledger whole, as the open-finding summary shows.
- [ ] **AC5.** Each ledger entry is resolved or carries a recorded deferral naming what is deferred and why, as the ledger's status summary shows.
- [ ] **AC6.** The design and the corpus carry one tagged revision that a production build can name as its target, as the tag shows.
- [ ] **AC7.** The specification is settled only after the tool has bundled each source in a declared exposure set, as the freeze check shows.
- [ ] **AC8.** A prerequisite section is removed only where a recorded bundling supplies what it named, and any shortfall is a ledger entry, as the removal records show.
- [ ] **AC9.** Each exposure-set source carries a bundled size recorded against the size of the same sources read whole, as the run records show.
- [ ] **AC10.** Each item the prototype initiative deferred and its product did not need is delivered or carries a recorded deferral, as the carried-debt epic rows show.

- [ ] **AC11.** The refined contract supports author-directed section composition with source-preserving staged inclusion, as the composition conformance suite demonstrates.

- [ ] **AC12.** Linked sources retain their declared structural intent across supported entry and dependency selections, as the metadata conformance corpus demonstrates.

## Non-Goals

- It does not implement a production build.
- It does not add ontology inference, workflow execution or sentence-level substitution.
- It does not rewrite authored source structure; section composition arranges compiled output.
- It does not commit to a date for the freeze.
- It does not accept a finding by working around it in a source document.
- It does not open an issue or a pull request on another project.

## References

- **R1.** **Source.** [v1 design](https://github.com/m2ux/prosiform/blob/3ff368936aa577ef57bd43b7a2fae63c264a99dc/artifacts/planning/2026-10-17-prosiform-v1/design.md) — the specification this initiative settles, including the residual items it names as needing measured real-skill data.
- **R2.** [Planning decisions](https://github.com/m2ux/prosiform/blob/3ff368936aa577ef57bd43b7a2fae63c264a99dc/artifacts/planning/2026-10-17-prosiform-v1/decisions.md) — why the prototype is used before a production build is committed to, and what marks the specification settled.
- **R3.** [Proposal](https://github.com/m2ux/prosiform/issues/1) — the scoped problem and the goal clauses these criteria trace to.

- **R4.** **Source.** [Section Composition: Unicode Links Compose Content Within the Containing Section](https://github.com/m2ux/prosiform/issues/214) — the originating requirements for the section-composition extension.

- **R5.** **Source.** [Document Metadata: Per-File Settings Govern Linked Compilation](https://github.com/m2ux/prosiform/issues/216) — originating requirements for per-file conversion metadata.
