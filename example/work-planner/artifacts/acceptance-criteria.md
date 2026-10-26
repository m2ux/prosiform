---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Acceptance Criteria

The quality and verification state of an issue's acceptance criteria: how each criterion holds against its characteristics and marked sources, what its instrument reported, against which revision, and which criteria that evidence lets a body tick.

## Operations

### *Check* Criteria Quality

The quality findings for the acceptance criteria of the issues being aligned, against their characteristics and the marked sources they answer to.

**Inputs:** Each issue body whose criteria are checked, the initiative's References, checkout, authenticated source access and source destination files.

1. Check each criterion against [Requirement Characteristics](../references/requirement-characteristics.md), through [Verifiable](issue-body.md#verifiable).
   - Record each criterion that fails, with the characteristic it fails.
2. Apply [Read Requirement Sources](initiative-issue-body.md#read-requirement-sources) with the initiative's References, checkout, authenticated source access and source destination files.
3. Align the criteria with each source read, as [Sources](initiative-issue-body.md#sources) defines.
   - Record each departure, with the criterion and the source it departs from.
   - Record each gap, with the source requirement no criterion makes true.
4. Return the failing criteria, departures and gaps with the source findings Read Requirement Sources returns.

### *Verify* Selected Criteria

The verification evidence for a supplied set of criteria whose delivery is ready.

**Inputs:** Criterion ids, current issue body, delivery findings, delivery revisions, named instruments, the project checkout to run them in, and the [verification evidence](#verification-evidence) the run has already taken, when it has any.

1. Confirm the supplied delivery findings establish [Readiness](#readiness) for each selected criterion.
   - Return an undelivered or unreadable dependency as a blocker for that criterion.
2. Check out each branch the delivering pull requests merged into, in the supplied project checkout, meeting [Instrument Checkout](#instrument-checkout).
   - Keep the supplied evidence of each criterion taken on the revision now checked out, meeting [Verification Evidence](#verification-evidence).
   - Run the named instrument of each other criterion there.
   - Record the result against the tested revisions, meeting [Instrument Result](#instrument-result).
3. Return the verification evidence of each selected criterion, kept or taken, the verified criterion ids, and each unresolved criterion with what is missing.
   - Leave body publication and further planning to the caller.

### *Tick* Verified Criteria

The confirmed criteria and completed rows recorded in an epic or initiative body.

**Inputs:** Issue JSON, verified criterion ids, output body file, and the pull request records with the complete issue-link snapshot for an epic or every linked epic record for an initiative.

1. Record the criteria, meeting [Tick State](#tick-state).
   - For an epic, apply [Record Epic Criteria](epic-issue-body.md#record-epic-criteria) with the issue JSON, pull request records, complete issue-link snapshot, verified criterion ids and output body file.
   - For an initiative, apply [Record Initiative Criteria](initiative-issue-body.md#record-initiative-criteria) with the issue JSON, every linked epic record, verified criterion ids and output body file.
2. Return the resulting body and any criteria refused as not ready to verify. The artifact operations return the updated bodies for publication.

### *Untick* Criteria

The criteria a body ticked without the delivery their evidence depends on, returned to unticked.

**Inputs:** Current issue body, criterion ids and output body file.

1. Clear the tick on each supplied criterion, and Done on each row or table that cites it, meeting [Tick State](#tick-state).
2. Write the body to the output file and return it for publication, leaving every other criterion and row as it stands.

### *Record* Verified Criteria

The verified criteria of one epic or initiative, ticked and saved to its issue.

**Inputs:** Repository, criterion ids, current issue JSON and body, delivery findings, delivery revisions, named instruments, the project checkout, the verification evidence the run has already taken when it has any, output body file, and the pull request records with the complete issue-link snapshot for an epic or every linked epic record for an initiative.

1. Apply [Verify Selected Criteria](#verify-selected-criteria) with the criterion ids, current issue body, delivery findings, delivery revisions, named instruments, project checkout and the run's verification evidence.
   - When it returns no verified id, continue at step 4.
2. Pass only its returned verified ids to [Tick Verified Criteria](#tick-verified-criteria) with the issue JSON and output body file, and the pull request records with the complete issue-link snapshot for an epic or every linked epic record for an initiative.
3. When the returned body differs from the current issue body, apply [Save Tracker Issue](issue.md#save-tracker-issue) with the repository, issue number and output body file.
4. Return the verified ids, the verification evidence Verify Selected Criteria returned, the ids refused as not ready to verify, and each unverified criterion with what it is missing. A refused or unverified criterion stays unticked.

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

A criterion is verified only on a passing run of its named instrument, recorded against the tested revisions as [Coverage Reports](issue-body.md#coverage-reports) define. A failed, unavailable or inconclusive instrument leaves it unverified, and an unverified criterion is not ticked.

### Verification Evidence

One criterion's instrument result, passing or failing, with the issue that states the criterion and the revision it was taken on. Within one run, evidence stands for its criterion on its revision: the criterion's instrument runs at most once on each revision, and a later verification on that revision keeps the earlier evidence.

### Tick State

A ticked criterion carries verification evidence. Done on the row or table that cites it follows [Tables](issue-body.md#tables) and [Work Breakdown](epic-issue-body.md#work-breakdown). A criterion refused as not ready to verify is returned unticked with what it is missing.
