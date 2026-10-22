# Changes

The plan changes this session applied, the ones it held, and the debt its validation found.

## Applied

| Change | Kind | Where |
| --- | --- | --- |
| The design states the destination a member carrying nothing above the grouping depth reaches | Design record | [`design.md`](../2026-10-17-prosiform-v1/design.md), `A heading for every member`, `Link text` and the grouping corpus list |
| W02's row links its pull request, carries its Done tick and its criterion AC3 is ticked | Epic delivery | [#195](https://github.com/m2ux/prosiform/issues/195), [#201](https://github.com/m2ux/prosiform/pull/201) merged into `i01/e02/main` at `8863b72` |
| The review pull request cites this delivery and states the destination rule as it stands | Epic review | [#198](https://github.com/m2ux/prosiform/pull/198) |
| Two corpus declarations restated to the destinations their own bytes show | Corpus | `delivery/an-entry-destination-under-a-grouping-rule`, `grouping/a-whole-document-reference-to-a-member` |
| A member named by no heading in its section, raised and placed as a new task | Task creation | [#203](https://github.com/m2ux/prosiform/issues/203) as `I01:E03:W11`, criterion AC12 on [#187](https://github.com/m2ux/prosiform/issues/187), board status Backlog |
| A check reading a branch that moves beneath it, raised and placed as a new task | Task creation | [#204](https://github.com/m2ux/prosiform/issues/204) as `I01:E03:W12`, criterion AC13 on [#187](https://github.com/m2ux/prosiform/issues/187), board status Backlog |

## Held

Nothing. No change this session met needed an initiative, and none fell outside the kinds the run's allowance covers.

## Debt the validation found

- **Non-trivial, deferred — a member named by no heading in its section.**
  A pooled section splits into variants when more than one contributing document writes body text above its first subheading. One document writing such body text beside another that writes only subheadings leaves the section unsplit, so that document's body is emitted beneath the pooled heading with nothing naming it, and a whole-document reference to it is answered by a heading both documents write. Fixing it changes what the arrangement emits inside a pooled section, which warrants a work item of its own, so it is deferred to [#203](https://github.com/m2ux/prosiform/issues/203). The shapes this unit's criterion names are unaffected.

- **Non-trivial, deferred — the contract read from a branch that moves.**
  The vocabulary, conformance and independence checks read the design from the engineering branch as it currently stands, so a contract term marked there before its glossary entry reaches the repository fails every branch at once, the long-lived ones included. This unit met it as a red check on a revision carrying nothing that could answer it. It is deferred to [#204](https://github.com/m2ux/prosiform/issues/204).

- **Nothing blocking.**
  Every check this unit's criterion rests on passes, and no debt stood between the criterion and its verification.

## The merge

[#201](https://github.com/m2ux/prosiform/pull/201) merged into `i01/e02/main` at `8863b72` with every target of `make check` holding on its head but `make vocabulary`, which reports a contract term marked on the engineering branch by [#194](https://github.com/m2ux/prosiform/issues/194) and not yet defined in `docs/glossary.md`. The base reported the same failure at `9037a91`, before this branch reached it, so the merge changed nothing about it. The reading that lets one commit's result turn on another branch is [#204](https://github.com/m2ux/prosiform/issues/204).
