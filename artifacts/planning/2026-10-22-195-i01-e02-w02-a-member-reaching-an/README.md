# A Member Reaching an Unshared Destination — October 2026

> Delivery · Created 2026-10-22

## Executive Summary

A merged group pools its members' headings by text, so two documents contributing a section of one name hang their content under one heading, each behind a variant heading that names its own document. A whole-document reference to a member resolves to that member's first contribution, which for a member whose content all sits at the grouping depth is the pooled heading rather than the variant beneath it. Two such members therefore resolve to one fragment, and a bundle emits `[Common](#style)` beside `[Agents](#style)`. This unit holds a whole-document reference to a heading its member does not share.

A reference that reaches the wrong member is a silent fault: the bundle validates, the link resolves, and the reader lands on another document's content. The variant headings the arrangement already composes name each contributor uniquely, so the destination exists; what is missing is the member registering it as its own.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [w02.md](w02.md) | The implementation plan for this unit |
| [validation.md](validation.md) | The checks this unit ran, the revision they ran against and what each observed |

## Links

| Resource | Link |
| --- | --- |
| Epic | [#195 \[I01:E02\] Merged Groups](https://github.com/m2ux/prosiform/issues/195) |
| Initiative | [#20 \[I01\] Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Epic planning | [i01-e02](../2026-10-17-prosiform-v1/i01-e02) |
| Epic base | [i01/e02/main](https://github.com/m2ux/prosiform/tree/i01/e02/main) |
| Review | [#198](https://github.com/m2ux/prosiform/pull/198) |
