---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 2
  group-heading: false
---
# Acceptance Criteria

The verification state of an issue's acceptance criteria: what each criterion's instrument reported, against which revision, and which criteria that evidence lets a body tick.

## Operations

### *Verify* Selected Criteria

The verification evidence for a supplied set of criteria whose delivery is ready.

**Inputs:** Criterion ids, current issue body, delivery findings, delivery revisions, named instruments and the project checkout to run them in.

1. Confirm the supplied delivery findings establish [Readiness](#readiness) for each selected criterion.
   - Return an undelivered or unreadable dependency as a blocker for that criterion.
2. Check out each branch the delivering pull requests merged into, in the supplied project checkout, meeting [Instrument Checkout](#instrument-checkout).
   - Run each criterion's named instrument there.
   - Record the result against the tested revisions, meeting [Instrument Result](#instrument-result).
3. Return verified criterion ids with their evidence and each unresolved criterion with what is missing.
   - Leave body publication and further planning to the caller.

### *Tick* Verified Criteria

The confirmed criteria and completed rows recorded in an epic or initiative body.

**Inputs:** Issue JSON, verified criterion ids, output body file, and the pull request records with the complete issue-link snapshot for an epic or every linked epic record for an initiative.

1. Record the criteria, meeting [Tick State](#tick-state).
   - For an epic, run [Record Epic Criteria](artifacts/epic-issue-body.md#record-epic-criteria) with the issue JSON, pull request records, complete issue-link snapshot, verified criterion ids and output body file.
   - For an initiative, run [Record Initiative Criteria](artifacts/initiative-issue-body.md#record-initiative-criteria) with the issue JSON, every linked epic record, verified criterion ids and output body file.
2. Return the resulting body and any criteria refused as not ready to verify. The artifact operations return the updated bodies for publication.

## Fields

- **Criterion.** The id of one acceptance criterion in the issue body that states it.
- **Instrument.** The command, test or check the criterion names as the thing that observes it.
- **Revision.**
  The branch and commit the instrument ran against, which is the branch the delivering pull requests merged into.

### Readiness

A criterion is ready to verify when the supplied delivery findings show the work its evidence depends on delivered and readable. An undelivered or unreadable dependency leaves it unready.

### Instrument Checkout

An instrument runs in a checkout of the project at the merged revision it is verifying, which the caller supplies. A checkout the caller is editing is not that revision, so a criterion verified against uncommitted work is unverified.

### Instrument Result

A criterion is verified only on a passing run of its named instrument, recorded against the tested revisions as [Coverage Reports](artifacts/issue-body.md#coverage-reports) define. A failed, unavailable or inconclusive instrument leaves it unverified, and an unverified criterion is not ticked.

### Tick State

A ticked criterion carries verification evidence. Done on the row or table that cites it follows [Tables](artifacts/issue-body.md#tables) and [Work Breakdown](artifacts/epic-issue-body.md#work-breakdown). A criterion refused as not ready to verify is returned unticked with what it is missing.
