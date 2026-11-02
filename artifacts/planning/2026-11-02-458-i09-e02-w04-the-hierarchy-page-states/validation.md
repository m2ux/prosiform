# Validation

The checks [W04](w04.md) names, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`b7e5a449`](https://github.com/m2ux/prosiform/blob/b7e5a449996cf5c8b4ee24839508339ef55ded95/artifacts/planning/2026-10-17-prosiform-v1/design.md#grouping) |
| Branch head | `4d22b028` on `i09/e02/w04-the-hierarchy-page-states` |

## T1 The Page Against the Grouping Fixtures

Each statement the page makes about a group's or a member's heading, read against the fixture or unit test that observes it.

| Page statement | Observed by | Agrees |
| --- | --- | --- |
| A member's subsection absorbs its own title where the title's slug agrees with the stem, and the title is not emitted again. | `grouping/a-member-named-by-the-title-it-absorbs`: `notes/titled.md` titled `Titled` emits `### Titled` and no second `Titled` heading. `with-preamble.md` titled `With Preamble` in `a-whole-document-reference-to-a-member` emits `#### With-Preamble` alone. | ✓ |
| A member whose title is absorbed takes its subsection though everything else sits at the grouping depth; the subsection is the heading alone. | `a-member-named-by-the-title-it-absorbs`: `### Titled` carries nothing, `### Findings` follows; `test_a_member_whose_title_the_subsection_absorbs_takes_one`. | ✓ |
| A member the group emits nothing else from takes a subsection. | `test_a_member_the_group_emits_nothing_else_from_takes_a_subsection`. | ✓ |
| A whole-document reference to the member and a reference to its absorbed title resolve to the subsection. | `a-member-named-by-the-title-it-absorbs`: `[Titled](#titled)`; `test_such_a_subsection_answers_the_whole_document_and_the_title_it_absorbed`. | ✓ |
| A title above the grouping depth that does not agree with the stem is the member's content beneath the subsection. | `Member.shift` in `grouping.py`, which emits an unabsorbed title beneath the subsection at the level that makes room. | ✓ |
| A member whose content all sits at the grouping depth, with no title to absorb, takes no subsection, and a whole-document reference resolves to the first heading the group emits from it alone. | `a-whole-document-reference-to-a-member`: `bare.md` takes no subsection and `[Bare](#outcomes)`; `test_a_member_whose_content_sits_at_the_grouping_depth_takes_no_subsection`. | ✓ |
| A titled first entry that is a member opens the group on its title and takes no subsection. | `test_a_titled_parent_s_whole_document_reference_reaches_its_title`; `a-titled-parent-reached-as-a-whole-at-depth-one` records the depth-one case, where the title is the merged section. | ✓ |
| A file heading stands at the top level wherever its document is placed. | `an-intermediate-group-nests-inside-its-parent`: `# Plain` and `# Extra` follow as top-level file groups though the guide and the notes link them. | ✓ |
| A merged group stands inside the division holding the document whose link placed its first member, after that division's own content, one level deeper. | `an-intermediate-group-nests-inside-its-parent`: `## Notes` after the guide's `## Procedure`; `a-member-named-by-the-title-it-absorbs` and `members-of-one-stem-in-different-directories`: `## Notes` and `## Guides` inside `# Entry`. The page's outline sketch is the first of these. | ✓ |
| A heading a nested group pushes beyond H6 fails the run. | `a-nested-group-pushing-a-heading-past-the-sixth-fails`: exit 1, `E_HEADING_DEPTH_OVERFLOW`. | ✓ |

A search of the page for a group or a document called top-level finds two statements, both current: a file heading stands at the top level wherever its document is placed, and a group whose first member is an entry stands at the top level. The retired *A group is one top-level division* and *one top-level heading per contributing document* are gone.

Result: pass.

## T2 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `4d22b028`, exit 0. `make links` resolved every reference in 237 documents, the page's design link to `design.md#grouping` on engineering among them; `make vocabulary` and `make tables` passed; `make test` 1579 passed; `make harness` 1154 passed; the corpus reported 427 fixtures, 427 pass.

Result: pass.
