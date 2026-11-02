# Validation

The checks [W00](w00.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`a0a3264a`](https://github.com/m2ux/prosiform/blob/a0a3264aeb0fa9caec5a97c3fce20d6de5c7b2ba/artifacts/planning/2026-10-17-prosiform-v1/design.md#reference-normalization-and-path-identity) |
| Branch head | `db9a21be` on `i08/e03/w00-design-clause-retired-option` |

## T1 Inspection of the Pinned Clauses

Read the design at the pinned revision against AC7.

- **One spelling.** *Reference normalization and path identity* states `document#fragment` as the one spelling a section takes on the command line, and that a fragment alone names no document.
- **The refusal has one home.** The *CLI contract*'s invalid-usage list refuses an entry reference naming a fragment alone, its diagnostic naming `document#fragment` as the remedy; the normalization clause refers to it rather than restating it.
- **The removal is named.** The normalization clause states that `-f` retires with the form it served and that the CLI contract declares no referrer.
- **The link form stands.** The normalization clause links *Fragment-only links*, which still resolve a `[Check](#section)` link against the document carrying it.
- **No residue.** The option table, the usage examples, *Automatic output names*, *Source ownership*, *The substitution mapping*, the CLI validation scope and the per-file ownership case name no `-f`, referring document or fragment-only entry; a grep of the design for `-f` finds only the retirement sentence.

Result: pass.

## T2 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `db9a21be`, exit 0. The corpus reported 423 fixtures, 423 pass, 0 fail, 0 awaited. `make conformance` read 320 clauses at the new pin with 0 declarations naming no clause, after the two citations of the withdrawn `CLI contract — -f DOC` row were removed.

Result: pass.
