---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Initiative Publication

A reviewed initiative and its epics saved to the tracker, linked to one another, format-checked and recorded in the planning record.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md).

## Procedure

### 1. Number the Initiative

For a new initiative, apply [Select Tracker Number](../artifacts/issue.md#select-tracker-number) with the repository, the initiative prefix letter and its existing titles.
- Use the confirmed number in the initiative's title.

### 2. Save the Initiative

Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the repository, the reviewed initiative body file, its title and labels, and each label's colour and description.
- For an existing initiative, pass its issue number and the selected body and metadata changes.

### 3. Save the Epics

For each reviewed epic, a prerequisite epic before the epics that depend on it:
- Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the repository, the epic body file, its title, its labels with the confirmed priority label among them, and each label's colour and description.
- For an existing epic, pass its issue number and the selected body and metadata changes.

### 4. Resolve the Links

Apply [Resolve Placeholder Links](../artifacts/initiative-issue-body.md#resolve-placeholder-links) with the initiative body file, each epic body file and the saved issue identity of the initiative and of each epic.
- Return each temporary link left unresolved, with the file that holds it, to the caller as a blocker.
- Apply [Save Tracker Issue](../artifacts/issue.md#save-tracker-issue) with the body change for each rewritten body file.

### 5. Repair the Format

- Apply [Repair Issue Format](../artifacts/issue-body.md#repair-issue-format) with [Validate Epic Body](../artifacts/epic-issue-body.md#validate-epic-body) as the validator, the saved initiative JSON, current pull request records and corpus branch as its further inputs, the epic template, and every saved epic with its identity, current JSON and output body path.
- Apply [Repair Issue Format](../artifacts/issue-body.md#repair-issue-format) with [Validate Initiative Body](../artifacts/initiative-issue-body.md#validate-initiative-body) as the validator, every saved epic JSON and the requirement sources as its further inputs, the initiative template, and the saved initiative with its identity, current JSON and output body path.
- Return each blocker either repair returns to the caller.

### 6. Record the Publication

Apply [Populate Planning Record](../artifacts/planning-record.md#populate-planning-record) with the record identity, folder path, the saved initiative and epic issue links, the evidence and decisions the caller supplies, and the caller's commit message file, asking it to publish.
- Return the saved initiative and epic identities, the publication result and any blocker to the caller.
