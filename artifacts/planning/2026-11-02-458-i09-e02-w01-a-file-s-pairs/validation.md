# Validation

The checks [W01](w01.md) and [W02](w02.md) name, at the revisions they ran.

## Revisions

| Item | Revision |
| --- | --- |
| Design (engineering) | [`b7e5a449`](https://github.com/m2ux/prosiform/blob/b7e5a449996cf5c8b4ee24839508339ef55ded95/artifacts/planning/2026-10-17-prosiform-v1/design.md#grouping) |
| Branch head | `eec446e9` on `i09/e02/w01-a-file-s-pairs` |

## W01 T1 A File's Pair Places Its Own Sections

`test_a_file_s_pair_places_its_own_sections` bundles a guide paired with `modes` that links rules paired with `rules`: the outline is `# Guide`, `## Procedure`, `## Rules`, `### Rules`, `### Procedure`, so the rules' Procedure stays in the Rules group nested in the guide's division. `test_a_parent_s_pair_leaves_the_sections_it_links_alone` gives the rules no pair, and they keep a top-level file group. The fixture `grouping/a-file-places-its-own-sections` records the first bundle.

Result: pass.

## W01 T2 Composition From the Leaves Up

`test_a_linked_file_is_composed_before_its_parent_merges_it` bundles guide → steps (`steps`) → checks (`checks`): the Checks group stands at `###` inside the Steps group at `##`, after the steps' own sections, inside the guide's division. The fixture `grouping/a-linked-file-is-composed-before-its-parent-merges-it` records it.

Result: pass.

## W02 T1 An Intermediate Group Nests Inside Its Parent

- `test_an_intermediate_group_nests_inside_its_parent`: the Notes group sits at `##` after the guide's Procedure, and the unpaired documents the guide and the notes link keep top-level file groups.
- `test_a_nested_group_moves_every_heading_down_one_level_per_division`: `merged` at level 3 emits every heading two levels below the top-level group, with the same texts.
- `test_a_group_placed_by_a_document_in_two_groups_nests_in_the_first`: rules in Reviews and Drafts place Leaves, which nests in Reviews, and the leaf's content is carried once.
- `test_a_nested_heading_pushed_beyond_h6_fails`: a depth-one member's H5 nested once fails with `E_HEADING_DEPTH_OVERFLOW` and publishes nothing.
- The fixtures `grouping/an-intermediate-group-nests-inside-its-parent`, `grouping/a-group-placed-by-a-document-in-two-groups` and `grouping/a-nested-group-pushing-a-heading-past-the-sixth-fails` record the same.

Result: pass.

## W02 T2 An Unbundled Link Stays Content

`test_a_link_a_file_does_not_bundle_stays_its_content`: inside the nested Notes group, `[the draft](draft.md)`, naming a document that declares nothing, and `[the web](https://example.com/page)` keep their authored destinations, and the draft contributes no content. The fixture `grouping/a-link-a-file-does-not-bundle-stays-its-content` records it.

Result: pass.

## T3 Make Check

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` at `eec446e9`, exit 0. `make test` 1579 passed; `make harness` 1154 passed; the corpus reported 427 fixtures, 427 pass, 0 fail, 0 awaited. `make conformance` read 327 clauses at the new pin with 0 declarations naming no clause: *A file places its own sections* is covered by 2 fixtures, *Composition from the leaves up* by 3 and *Nested groups* by 24. `make mock-scenarios` passed 5 of 5.

Result: pass.

## Re-Recorded Fixtures

Each was read for the intended outline: the merged group a non-entry document places stands inside that document's division after its own content, one level deeper, and nothing else moved.

- `grouping/`: `a-document-no-group-matches`, `a-member-named-by-the-title-it-absorbs`, `a-member-whose-name-carries-no-word-takes-its-path-text`, `a-reference-to-a-grouping-depth-heading`, `a-reference-to-a-member-carrying-one-heading`, `a-whole-document-reference-to-a-member`, `members-of-one-stem-in-different-directories`, `one-spelling-for-every-generated-heading`, `two-members-sharing-a-name-beneath-an-entry`.
- `inclusion/`: `a-dependencys-preset-comes-from-itself`, `a-presets-pairs-reach-the-reference-it-governs`, `a-section-matching-no-preset-selects-default`, `a-section-title-selects-its-preset`, `a-title-matching-two-keywords-selects-both`, `default-applies-in-every-section`, `one-document-two-presets`.
- `usage-example/`: `a-mode-and-the-guidelines-it-defers` and `artifacts-and-references-under-declared-groups` re-recorded; `a-procedure-and-everything-it-reaches` and `a-mode-and-the-board-reads-it-steps-through` record the depth overflow the example's Delivery Evidence artifact meets once the Artifacts group nests in the mode's division.
