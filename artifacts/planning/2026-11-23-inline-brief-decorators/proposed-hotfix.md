## Overview

Inline calls should show the same brief decorator as dispatched calls, with an execution link to material in the current bundle. A plain reference includes material without this decorator. This lets an author choose the execution boundary without manually copying a Contract or narrating a command's mechanics.

Target: `main`

## Problem

- **Briefs apply only to dispatch.**
  Released pf 0.34.0 selects a declared brief for a dispatched call but ignores that brief for inline composition and plain references.
- **Inline callers carry manual structure.**
  Authors must compose the Contract explicitly or write wrapper prose even when the target already declares its brief.
- **Rendering can diverge at the execution boundary.**
  An inline call and a dispatch of the same selected target should share brief content, section order and placement rules.

## Proposal

- **Use the same brief decorator.**
  Resolve an inline call's brief from its target's effective presets through the same selection and placement rules as dispatch. Emit the same named subsection, brief lead and child sections, with the execution link in the same position.
- **Point inline execution at local material.**
  Include the selected target through the current bundle's inclusion and grouping rules and link the decorator to its resolved local section. The current agent follows it. Dispatch keeps its separately compiled target and external bundle link.
- **Keep plain references undecorated.**
  A plain link retains ordinary inclusion and receives no automatic brief, including when its target declares one. An active inline call to a document or section selecting a brief receives the decorator without a manually authored Contract composition.
- **Share the existing behavior.**
  Preserve preset precedence, substitutions, selection identity, heading and ordering rules, grouping, repeated-call handling, diagnostic boundaries and provenance through common compiler paths. Inline adds no child bundle, agent handoff or model annotation. Existing explicit section composition and deferral outside this brief-bearing call are not a separate redesign in this fix.
- **Validate with paired specimens.**
  Compile one target through plain, inline and dispatch links, using Markdown and diagram forms. Compare the decorated sections after normalizing only the execution operator and target. Update the public contract, guide, tests and corpus together. Classifier adoption and native workflow evaluation are separate follow-up work after compiler review.

## Acceptance Criteria

- [ ] **AC1.** An inline call selecting a brief emits the same ordered decorator as the equivalent dispatch, apart from its execution link, as paired Markdown and diagram snapshots show.
- [ ] **AC2.** Every inline decorator's execution link reaches its complete selected target in the current bundle, as local-link walks and sentinel fixtures show.
- [ ] **AC3.** A plain reference remains undecorated when its target declares a brief, as the three-operator comparison fixture shows.
- [ ] **AC4.** Inline calls execute in the current context without creating a separate target bundle, as generated-file and execution-link inventories show.
- [ ] **AC5.** Inline brief selection follows dispatch's effective-preset resolution, as default, override, substitution and conflicting-selection regressions show.
- [ ] **AC6.** Decorated inline calls retain the compiler's structural validity rules, as grouping, repeated-target, collision, H6 overflow, cycle and provenance regressions show.
- [ ] **AC7.** The public language contract and invocation guide describe the implemented operator distinction, as documentation and conformance guards show.
- [ ] **AC8.** The delivering compiler revision passes make check, as its retained check log shows.

## References

- **R1.** [Dispatch Briefs](https://github.com/m2ux/prosiform/blob/61ddc5aa1/docs/dispatch.md#briefs) — the released selection, placement and section-order rules to share.
- **R2.** [Composition](https://github.com/m2ux/prosiform/blob/61ddc5aa1/docs/composition.md) — current section-composition boundaries.
- **R3.** [Inline Brief Plan](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-23-inline-brief-decorators/README.md) — confirmed goal, implementation sequence and validation matrix.
