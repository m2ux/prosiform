# Review Finding

One evidenced problem and its proposed solution.

## Operations

### Populate Review Finding

One finding verified against its supplied source.

**Inputs:** Area, severity, problem, proposed solution, source text and file:line, decision requirement and any confirmed answer.

1. Verify the problem against the supplied source.
2. If evidence is missing or contradictory, return that finding for the caller to resolve.
3. Populate the finding with its source quotation.
   - It must meet [Finding Content](#finding-content) and [Decision State](#decision-state).
4. Return the finding and any pending decision.

## Fields

### Finding Content

Each finding has an area, severity, one problem/solution pair and a source quotation with file and line. The source establishes the stated problem. Findings are grouped by area when presented together.

### Decision State

A finding identifies whether it needs a user decision and records any supplied answer. An unanswered decision remains pending.
