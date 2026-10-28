---
prosiform:
  root: ".."
  group: "protocols"
  group-depth: 1
---
# Delivery Base Preparation

The epic bases a set of epics needs, created once their prerequisites hold, and the open delivery pull requests pointed at them.

Follow the [Procedure](#procedure), adhering to [Rules](../rules.md) and [Conventions](../conventions.md).

## Procedure

### 1. Confirm Prerequisites

For each supplied epic:
- Apply [Check Epic Prerequisites](../artifacts/epic.md#check-epic-prerequisites) with the current initiative and epic bodies and the prerequisite issue and base-merge records.
- Carry a missing or unconfirmed prerequisite into the result as that epic's finding, and leave its bases uncreated.

### 2. Prepare the Bases

For each epic whose prerequisites are confirmed, apply [Prepare Delivery Bases](../artifacts/delivery-branches.md#prepare-delivery-bases) with the project checkout, epic identity, changed long-lived branches and the confirmed [Prerequisite Evidence](../artifacts/epic.md#prerequisite-evidence).
- Carry unevaluable branch names or a failed creation into the result.

### 3. Read Branches and Pull Requests

- Apply [Read Delivery Branches](../artifacts/delivery-branches.md#read-delivery-branches) with the project checkout and each supplied epic's identity.
- Use the current pull request records the caller supplies. When it supplies none, apply [Read Initiative Pull Requests](../artifacts/pull-request.md#read-initiative-pull-requests) with the repository, initiative prefix and destination collection file.
- Return to the caller with the findings when the branch names are unevaluable or the pull request evidence is incomplete.

### 4. Align the Pull Requests

Apply [Align Pull Request Base](../artifacts/pull-request.md#align-pull-request-base) with the repository, those pull request records, the long-lived branches and epic bases Read Delivery Branches returned, and the project checkout.

### 5. Return the Result

Return to the caller:
- The bases created and each epic's prerequisite findings.
- The long-lived branches and epic bases Read Delivery Branches returned.
- The retargeted pull requests, updated task branches, conflicts and pull requests awaiting a decision that Align Pull Request Base returned.
