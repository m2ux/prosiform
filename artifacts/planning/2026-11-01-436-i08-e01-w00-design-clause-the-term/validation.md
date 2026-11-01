# Validation

The checks [W00](w00.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`7e98083f`](https://github.com/m2ux/prosiform/blob/7e98083fe8d988f00a51002997b585d84da212eb/artifacts/planning/2026-10-17-prosiform-v1/design.md#presets) |
| Branch head | `c4ec8745` on `i08/e01/w00-design-clause-the-term` |

## T1 Inspection of the Pinned Clauses

Read *Conversion metadata* and *Presets* at the pinned revision against AC11.

- **A property of the governed document.** *Presets* opens by stating a preset as a property of the document declaring it, governing that document's own content; *What a selection governs* stops its reach at that document.
- **Chosen by a keyword in the linking section's title.** *Selection by keyword* selects the presets whose names appear as whole words, case-insensitively, in the title of the section containing the reference; *A command-line entry reads the file it names* covers a reference written in no document.
- **`default` always applies.** *`default` always applies* and *`default` is not selectable by keyword*.
- **Union and its refusal.** *Selected presets union* combines the selected presets and refuses a disagreement as invalid usage with exit status `2`.
- **Citations hold.** *The admitted keys*, *`root` is refused*, *An empty block declares* and *Unrelated fields have no conversion meaning* keep their titles.
- **The warning carries no code yet.** *A preset nothing selected warns* states the warning by its effect: the catalogue test holds every `W_` code the design names to the schema's catalogue, and no fixture reaches the warning before W06.

Result: pass.

## T2 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `c4ec8745`, exit 0. The corpus reported 398 fixtures, 398 pass, 0 fail, 0 awaited. `make conformance` read 323 clauses at the new pin, among them the eleven *Presets* clauses and the new *Conversion metadata* rules, with 0 declarations naming no clause.

Result: pass.
