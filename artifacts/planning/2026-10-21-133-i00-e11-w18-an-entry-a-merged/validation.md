**Component:** `src/prosiform/grouping.py`

## Procedure

Each run below is made from the task's worktree against the build the checkout holds. The corpus and the documented invocation reach that build through `PROSIFORM_BUILD`:

```text
PROSIFORM_BUILD="uv run --project <worktree>/src --frozen prosiform" make check
```

The three invocations the fault was measured on were run directly against the same build, over a source root written for them, before the change and after it.

## Reproduction on the base

The source root carries `notes/bare.md`, holding `# Bare` and nothing else, and `notes/second.md`, holding `# Second` and one `## Outcomes` section. The rule `--group notes:2` merges both. `bare.md` contributes nothing to the group: its only H1 is the title its overview subsection heading absorbs, and it carries nothing above or at the grouping depth.

| Invocation | On the base | After the change |
| --- | --- | --- |
| `--group notes:2 notes/bare.md` | `E_UNEXPECTED_INTERNAL_ERROR: IndexError('list index out of range')`, status 4 | status 0, the bundle opening on `[Notes](#notes)` |
| `--group notes:2 'notes/second.md#second'` | `E_UNEXPECTED_INTERNAL_ERROR: IndexError('list index out of range')`, status 4 | status 0, the bundle opening on `[Outcomes](#outcomes)` |
| `--group notes:2 entry.md`, where `entry.md` links both members | `E_UNEXPECTED_INTERNAL_ERROR: KeyError(('notes/second.md', 'second'))`, status 4 | status 0, the links rewritten to `#outcomes` and `#notes` |

The first two are the entry line written from an empty destination list. The third is the rewrite reading a target out of the destination map by an identity the map never held, which is the same unanswered target reached by the other of its two readers.

## T1 — The command over a member a merged group emits no heading for

`make test`, 673 passed. Three runs state the outcome of each invocation above:

- `test_an_entry_naming_a_member_the_group_emits_no_heading_for_opens_on_the_group` — the bundle opens on the group's own heading.
- `test_an_entry_naming_the_absorbed_title_of_a_member_opens_on_its_contribution` — an entry naming the title the member's own heading carries opens on the member's first contribution.
- `test_a_reference_into_a_member_the_group_emits_no_heading_for_is_rewritten` — a compiled reference into such a member is rewritten to the group's heading.

Each returns status 0, so none of the three returns `E_UNEXPECTED_INTERNAL_ERROR`.

## T2 — The corpus declares both readings

`make corpus`, 219 fixtures, 219 pass, 0 fail, 0 awaited, 0 unexpected pass. Two of them are new:

- `grouping/an-entry-naming-a-member-contributing-nothing` — two members, one contributing and one not; the entry line names both and the non-contributing member resolves to `#notes`.
- `grouping/a-reference-to-a-member-contributing-nothing` — a compiled reference into the non-contributing member, rewritten to `#notes`.

No existing fixture's expected bytes moved, so the arrangement is unchanged for every member a group already emitted a heading for.

## T3 — The repository's whole check suite

`make check` exits 0: lock-check, lint, format-check, typecheck, test (673), harness (489), corpus (219), smoke, layout, tables, links, vocabulary and invocation all pass.

## Observations

- **The invariant already existed; nothing reached it.** The candidate's entry-line check refuses a run whose entry reference names a target no destination was assigned to. The entry line is written before that check runs, so the index error arrived first. With every member answered, the construction satisfies the invariant and the check is what would report a disagreement.
- **The absorbed title is the second unanswered destination.** A member's overview subsection answers both the document and the title its own H1 carries. Where no subsection is emitted, both go unanswered, so the fallback covers both rather than the document alone.
- **Both readers of the destination map share one fault.** The entry line and the rewrite reach for the same missing assignment and fail differently, which is why the fix belongs to the arrangement that assigns rather than to either reader.

## Limitations

- **The design's clause coverage report is not regenerated here.** `coverage.py` reports counts that have moved with the wave's other rows, and the report it writes is shared state. The clause this row amends states the same obligation under the same heading, so its row in that report is unchanged.
- **A member contributing nothing still joins the group.** The arrangement emits the group's heading and nothing from such a member, so the bundle names the member's destination without carrying its content. That is what a member with nothing selected contributes, and it is stated rather than refused.
