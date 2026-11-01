# Validation

The checks [W10](w10.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`ca8e1c97`](https://github.com/m2ux/prosiform/blob/ca8e1c9731e6c7887030c009fe002ea4e42025cf/artifacts/planning/2026-10-17-prosiform-v1/design.md#conversion-metadata) |
| Branch head | `44fa33c7` on `i08/e00/w10-the-conversion-clause-states` |

## T1 Inspection of the Conversion Metadata Clause

Read the *Conversion metadata* clause at the pinned revision and searched it for every statement of presence (`grep -n -i "declares nothing\|empty"` over the clause's lines).

- **One statement.** Presence is stated only at *An empty block declares*: a present `prosiform` mapping declares its document, and an empty one declares and carries no conversion settings.
- **Nothing contrary.** The paragraph under the field table no longer lists an empty `prosiform` mapping among the cases that declare nothing; the only cases declaring nothing are absent frontmatter, an empty or comments-only frontmatter block, and frontmatter with no `prosiform` key.
- **Citations hold.** The bullet keeps its title, so `fixtures/inclusion/an-empty-block-declares` and `fixtures/inclusion/no-block-does-not-declare` still cite a bullet the clause carries.

Result: pass.

## T2 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `44fa33c7`, exit 0. The corpus reported 375 fixtures, 374 pass, 0 fail, 1 awaited; `make conformance` resolved every clause citation against the new pin.

Result: pass.
