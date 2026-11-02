# Validation

The checks [W00](w00.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`febd4a6d`](https://github.com/m2ux/prosiform/blob/febd4a6da4a57064942810d2e1cb381e7bccc8eb/artifacts/planning/2026-10-17-prosiform-v1/design.md#grouping) |
| Branch head | `fbd9d9e9` on `i09/e02/w00-design-clause` |

## T1 Inspection of the Pinned Clauses

Read the design at the pinned revision against AC7.

- **A file places its own sections.** *Grouping* states that the pair in force for a document places that document's own sections in the result the document bundling it merges and no other document's, that a parent's pair applies where a further reference bundles the parent, and that the invocation bundles each entry. Whose presets are in force stays with *Presets — What a selection governs*, which the clause links rather than restates.
- **Composition from the leaves up.** *Grouping* states that each placed document is composed under its own pair before the document that placed it merges the result, that a reference to a document already placed merges nothing more, and that a link a document does not bundle stays its content.
- **Nested groups.** *Grouping* states that a named group stands inside the division of the document whose reference placed its first member, after that division's own content, one level deeper per enclosing division, overflow failing as *Depth overflow* states; that a group whose first member is an entry stands at the top level; and that a document with no pair keeps its file group at the top level.
- **The surrounding clauses agree.** *Groups*, *Continuous Markdown*, *Dependency order*, *Group structure*, *Presets — A document in several groups* and *Group isolation* state a group as a division that may nest rather than as one top-level H1.
- **Every cited title stands.** Every clause title the corpus cites is unchanged; the three new clauses are additions.
- **Revision history.** The clause lands in engineering commit `febd4a6d`, and the README pin moves to it in `fbd9d9e9`, before W01 and W02 change the build.
- **The requirement trace.** The initiative record's goal trace maps G2 to E02 AC1–AC7; AC7 is this clause.

Result: pass.

## T2 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at the README pin `febd4a6d`, exit 0. The corpus reported 421 fixtures, 421 pass, 0 fail, 0 awaited. `make conformance` read 327 clauses at the new pin, the three new *Grouping* clauses among them as covered by no fixture yet, with 0 declarations naming no clause.

Result: pass.
