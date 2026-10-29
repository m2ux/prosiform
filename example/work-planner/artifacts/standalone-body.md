---
prosiform:
  root: ".."
  group: "artifacts"
  group-depth: 1
---
# Standalone Body

Populates one standalone issue body.

## Operations

### Populate Standalone Body

One standalone issue body from its supplied scope.

**Inputs:** [Standalone scope](#standalone-scope), [Output body path](issue-body.md#body-file)

**Outputs:** [Standalone body](#template)

- Populate the body from the [Template](#template) at the supplied output path.
  - The title must meet the shared [Titles](issue-body.md#titles) conditions.
  - The Problem and Proposal must meet [Problem and Proposal](issue-body.md#problem-and-proposal).
  - All populated fields must meet [Fields](#fields), including the required [Sections](#sections).

### Revise Standalone Body

One standalone body with its confirmed boundary integrated.

**Inputs:** [Current body](#template), [Confirmed decisions](issue-body.md#body-resolutions), [Output body path](issue-body.md#body-file)

**Outputs:** [Revised body](#template)

#### 1. Populate the Standalone Body

Populate the body through [Populate Standalone Body](#populate-standalone-body), folding any Non-Goals into Proposal as a closing boundary.

#### 2. Return the Revised Standalone Body

Return the revised file for publication.

## Fields

### Template

````markdown
## Overview

{{One paragraph: what this issue asks for and why.}}

## Problem

{{The friction as it is now. Bullets for distinct facets, sub-bullets for several items.}}

## Proposal

{{The design, in bullets or paragraphs, each opening with a bold statement, and its body on the next line.}}

## Acceptance Criteria

- [ ] **AC1.** {{An end state of one invariant. It ends by naming its instrument.}}

## Open Questions

- {{An undecided point the work cannot start without. Resolve every one before the work starts, then delete the section.}}

## References

- **R1.** [{{Title}}]({{URL}}) — {{What the reader finds there. Delete the section when there is none.}}
````

### Titles

- The title is `Name: Subtitle`, with no prefix.
- A standalone issue carries no [kind label](../configuration.md#kind-labels).

### Sections

- A standalone issue has the [epic issue body](epic-issue-body.md)'s sections without the Work Breakdown table.

### Standalone Scope

The problem, design, acceptance criteria and open questions one standalone issue states, as the [Template](#template) sections hold them.
