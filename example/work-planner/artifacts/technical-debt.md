---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Technical Debt

One problem a unit's validation finds, and the class that decides where it is fixed.

## Operations

### *Classify* Technical Debt

One debt item sorted into the class that decides whether the unit fixes or defers it.

**Inputs:** The debt item, the evidence that shows it, and the criteria the unit's Coverage carries.

1. Match the item to one class against the supplied criteria, deciding it yourself rather than putting it to the user.
   - Test [Blocking](#blocking) first, then [Trivial](#trivial) and [Non-trivial](#non-trivial).
2. Return the item with its class to the caller.

## Fields

### Debt Item

One problem the unit's validation finds — running its tests, auditing the definitions it changed, reviewing its pull request — with the evidence that shows it. An item carries exactly one class.

### Blocking

The unit's own criteria cannot be verified without the fix. The unit fixes it, whatever its size.

### Trivial

It blocks none of the unit's criteria and needs no work item of its own. The unit fixes it.

### Non-trivial

It blocks none of the unit's criteria and would warrant a work item of its own. The unit defers it to its initiative's [Deferred Debt](initiative-issue-body.md#deferred-debt) epic, so the epic in hand keeps the scope it was planned with.
