# Change List — I00:E05:W01

> Applied 2026-10-20 under the session's change allowance. Creating a new initiative sits outside it; nothing here needed one. No permission was denied.

## Applied

| Kind | Issue or row | What was applied |
| --- | --- | --- |
| Folded work | [`design.md`](../2026-10-17-prosiform-v1/design.md) Source-heading resolution | A heading's fragment is the slug its own visible text produces, and nothing numbers two headings of one source apart. The clause previously put the renderer's ordinal inside the source heading index, one sentence before the clause refusing a fragment two headings produce, and the build was built to the first of the two |
| Folded work | [`design.md`](../2026-10-17-prosiform-v1/design.md) Bundle destinations — Ordinal assignment | The walk names the headings a retained container carries beside the file headings, the structural ancestors and the selected source headings, and states the pass-over the renderer applies to an ordinal something already carries. The ordinal rule is now stated once, where the bundle destination is defined |
| Folded work | [`i00-e05.md`](../2026-10-17-prosiform-v1/i00-e05.md) | The Overview states the destination D23 settled, and the superseded hierarchy-path bullet is gone. It contradicted the bullet directly beneath it |
| Folded work | [#7](https://github.com/m2ux/prosiform/issues/7) | The same two corrections, patched into the live epic body against a fresh read. The epic body is never published from the planning file |
| Trivial debt, fixed | `fixtures/destinations/source-heading-fragments`, `fixtures/headings/{an-entity-in-a-heading,collision-with-a-natural-suffix,image-alternative-text}` | Four manifests named the ordinal clause under `Destination identity and link rewriting`, a section the design does not carry. They name `Bundle destinations` |
| Non-trivial debt, raised | [#84](https://github.com/m2ux/prosiform/issues/84) | The link check reports an unreachable host as an unresolved reference, so PyPI answering `503` to a page `src/README.md` names failed continuous integration on a branch touching neither. Hoisted onto [#39](https://github.com/m2ux/prosiform/issues/39) as row W07 with AC8 and R6 |
| Folded work | `src/tests/test_source.py` | Three tests asserted that a source fragment resolves by the renderer's ordinal, which is what `Source-heading resolution` refuses. They are replaced by tests of the slug a heading's own text produces, the ambiguity refusal and its precedence over the nested-target refusal, and an ordinal naming no heading of a source |
| Delivery record | [#7](https://github.com/m2ux/prosiform/issues/7) row W01 | The row links [#83](https://github.com/m2ux/prosiform/pull/83), AC1 and AC2 are ticked, and Done is ticked after the merge |
| Delivery record | [#85](https://github.com/m2ux/prosiform/pull/85) | The epic review draft, `i00/e05/main` into `main`, opened as a draft, labelled `bot:ai-assisted` and linked to #7 with `addCloseIssueReferences` |
| Delivery record | [#75](https://github.com/m2ux/prosiform/issues/75) | Linked to [#83](https://github.com/m2ux/prosiform/pull/83), which fixes it, and to [#85](https://github.com/m2ux/prosiform/pull/85), which carries it to `main` |

## Held

| Kind | Issue or row | What is recommended |
| --- | --- | --- |
| Board | [#7](https://github.com/m2ux/prosiform/issues/7) on [Bundling](https://github.com/users/m2ux/projects/18) | Not moved, and [#85](https://github.com/m2ux/prosiform/pull/85) is not marked ready. Three rows remain on the epic. Recommended: the row that merges W04 moves both |
| Closure | [#75](https://github.com/m2ux/prosiform/issues/75) | Left open. The fix is merged into `i00/e05/main` and a closing keyword does nothing on a base that is not the default branch, so the issue closes when the epic reaches `main` through #85 |
| Propagation | `main`, `i00/e01/main`, `i00/e07/main` | Each still numbers a destination over the document-level regions alone, so [#75](https://github.com/m2ux/prosiform/issues/75) reproduces on any of them until the epic base merges upward. No branch here is this unit's to push |
| Scope | `Ordinal assignment` — structural ancestors | The clause names them in the walk and the build emits none yet; they arrive with [I00:E09](https://github.com/m2ux/prosiform/issues/37). The numbering runs over the headings each emitted region carries, so it takes them in when they are emitted. Recommended: no row of its own |
| Repair | [#84](https://github.com/m2ux/prosiform/issues/84) | Not fixed here. The check's verdict for an unreachable host is a contract decision rather than a defect to patch mid-row, and the outage cleared on its own |
| — | — | Nothing else is held. No finding needed an initiative |

## Markers

| Marker | Fixture | Disposition |
| --- | --- | --- |
| — | — | None added. This unit's three fixtures all hold against the build it delivers |
| — | — | None lifted. The three the base carried — `I00:E09:W02`, `I00:E05:W03` and `I00:E08` — are untouched |

## Catalogue

No error code was added. `E_AMBIGUOUS_SOURCE_HEADING` and `E_AMBIGUOUS_FILE_GROUP`, the two failures AC2 declares, were both already among the twenty-three the schema carries, so the two-branch hazard was not entered and the vocabulary is unchanged at 34.
