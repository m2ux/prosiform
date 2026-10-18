## Overview

The prototype is used as the tool agents in this workspace invoke, and what that use reveals changes the specification until it stops changing. Every surprise becomes a ledger entry reducible to a fixture; an accepted finding changes the design first, then the corpus, then the build. The initiative ends when every entry is resolved or explicitly deferred and the design and corpus carry one tagged revision, which is the target the production build names.

## Problem

The behavioural contract has been written and reviewed, and nothing has yet composed a real instruction set for an agent carrying out the procedure it describes.

- **A specification written before use is a hypothesis.**
  The design states its invariants against constructed examples, and names its own residual items as needing measured fixture and real-skill data before their defaults are revisited ([residual policy](https://github.com/m2ux/md-composer/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-md-compose-v1/design.md#L532-L537)).

- **A corpus built beside an implementation tests what was implemented.**
  Fixtures accumulate from the work that needed them, so a construct real sources carry but nobody implemented has no fixture and produces no failure.

- **A surprise met mid-task has nowhere to go.**
  The agent is doing something else, so without a recorded place for a finding the cheapest action is a local workaround, and the design keeps its original claim.

- **A fix applied to the build leaves the contract wrong.**
  Correcting a composition in code without changing the design leaves the design asserting the original behaviour, and the next implementation reads the design.

- **A moving contract cannot be implemented twice.**
  A corpus that changes under refinement gives a second implementation no fixed target and no revision it can be said to satisfy.

## Proposal

- **The prototype is the tool in use.**
  It is invoked from this workspace's skills, so the contract meets real sources and real agents rather than constructed examples.

- **The ledger records every run.**
  A composition run is recorded with the source identities it composed and its outcome, so how much the tool was used is a fact the ledger holds rather than an impression.

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

- **The freeze is a tag.**
  Design and corpus take one tagged revision, and the production build names that revision as its target.

## Work Breakdown

| Epic | Description | Coverage | Depends on | Done |
| --- | --- | --- | --- | --- |
| [E00](https://github.com/m2ux/md-composer/issues/21) | Findings Ledger | AC1, AC2 | | |
| [E01](https://github.com/m2ux/md-composer/issues/22) | Specification Revision | AC3, AC4 | | |
| [E02](https://github.com/m2ux/md-composer/issues/23) | Specification Freeze | AC5, AC6, AC7 | | |

## Acceptance Criteria

- [ ] **AC1.** A surprise met while composing in real use is recorded with the evidence needed to reproduce it without the original session, as the ledger's entries show.
- [ ] **AC2.** A recorded finding is reducible to a corpus fixture that reproduces it, as the capture tool's reduction tests show.
- [ ] **AC3.** An accepted finding changes the design before the corpus or the build, as the revision history citing that finding shows.
- [ ] **AC4.** What remains unsettled is visible without reading the ledger whole, as the open-finding summary shows.
- [ ] **AC5.** Each ledger entry is resolved or carries a recorded deferral naming what is deferred and why, as the ledger's status summary shows.
- [ ] **AC6.** The design and the corpus carry one tagged revision that a production build can name as its target, as the tag shows.
- [ ] **AC7.** The specification is settled only after the tool has composed each source in a declared exposure set, as the freeze check shows.

## Non-Goals

- It does not implement a production build.
- It does not change the outcomes the composition contract serves.
- It does not commit to a date for the freeze.
- It does not accept a finding by working around it in a source document.
- It does not open an issue or a pull request on another project.

## References

- **R1.** **Source.** [v1 design](https://github.com/m2ux/md-composer/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-md-compose-v1/design.md) — the specification this initiative settles, including the residual items it names as needing measured real-skill data.
- **R2.** [Planning decisions](https://github.com/m2ux/md-composer/blob/d45c7f08f3878e71d9d0a99ae728fc69fc21f174/artifacts/planning/2026-10-17-md-compose-v1/decisions.md) — why the prototype is used before a production build is committed to, and what marks the specification settled.
- **R3.** [Proposal](https://github.com/m2ux/md-composer/issues/1) — the scoped problem and the goal clauses these criteria trace to.
