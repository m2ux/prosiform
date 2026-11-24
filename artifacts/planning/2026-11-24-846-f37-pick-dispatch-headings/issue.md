## Overview

Give each picking dispatch its own named section so graph nodes navigate to the operation they name and several picks remain distinguishable.

Target: `main`

## Problem

- Several differently named picking dispatches produce identical “Dispatch Pick” headings, each with its own alternatives. The graph's node names and generated section names disagree.
- The fixed heading reserves an otherwise ordinary dispatch name. Collision checks for briefed dispatches do not account for named picks.

## Proposal

- **Name the generated section from its dispatch.**
  Use the link text without its dispatch mark and point each local graph link at that named section. Preserve every alternative's order, choice description, model and bundle target.
- **Keep one meaning per generated name.**
  Share heading collision validation between picks and briefed dispatches. Refuse an authored collision or the same name addressing different effective selections through the existing error code.

## Acceptance Criteria

- [ ] **AC1.** Three distinct picks with three choices each produce their three named sections and matching local graph targets, with and without briefs, as the compiler regression observes.
- [ ] **AC2.** Alternative order, choice descriptions, model annotations and bundle destinations retain their declared values, as the fixture corpus verifies.
- [ ] **AC3.** Conflicting authored headings and distinct pick or brief selections sharing one name are refused without publication, as collision tests verify.
- [ ] **AC4.** The documented output and fixture expectations describe named pick sections, with compiler tests, corpus, lint, types and changed-document links passing.

## References

- **R1.** [Dispatch output contract](https://github.com/m2ux/prosiform/blob/61ddc5aa1a89ddf3f83a5d78a450ccec428aaabf/docs/dispatch.md#where-the-links-point) — The published behavior exhibiting the fixed generic heading.
