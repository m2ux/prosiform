# Validation

The checks the work item names, run against the design at engineering commit `f028ee97` and the worktree at `i07/e00/w20-state-the-publication-and`, revision `86e26296`, with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`.

## T1 Clauses Read Against the Pages

| Clause | Design at `f028ee97` | Page |
| --- | --- | --- |
| Validation and failure contract — Publication | An earlier set is renamed aside; a symbolic link is renamed and removed as the link it is; anything else, a regular file among them, is refused with `E_PUBLICATION_FAILED` naming the path, under `-c` as without it, and left where it stands. | `docs/bundles.md`, Publication: the same three cases and the same refusal. |
| Link classification and resource handling — Dispatch sub-sections | A dispatch in a heading the bundle emits as text alone fails with `E_UNSUPPORTED_CONSTRUCT`, naming the link; the three such headings named; a dispatch in the entry's own title publishes. | `docs/dispatch.md`: the same refusal, the same three headings and the same entry-title case. |

No sentence of the design at `f028ee97` states that a non-folder at the run folder's path is renamed aside. **AC31** holds for the design on the engineering branch.

## T2–T4 Checks at a Moved Pin

The README's Design link was moved from `827b66fc` to `f028ee97` in the worktree and `make check` run:

- `make corpus`: 384 fixtures, 384 pass.
- `make vocabulary`: fails on *boundary*, a term the design marks from `771f8c1b` that `docs/glossary.md` on `i07/e00/main` does not define.
- `make conformance`: fails. Fixtures cite `Local Markdown document links under the root` and `Local Markdown links resolving outside the root`, clauses `771f8c1b` renamed.

Six design commits lie between `827b66fc` and `f028ee97`, all I08 declaration work (`771f8c1b` to `ca8e1c97`): they refuse `prosiform.root`, derive a document's boundary from its links and rename the root clauses. The `i07/e00` build implements none of it, and the `i08/e00` branches pin those commits with their own glossary and fixtures. Moving the I07 pin past them would state I08's contract over the I07 build, so the pin was left at `827b66fc` and the worktree change reverted. Both clause names W20 edits are unchanged, so every fixture citing them resolves at either pin.
