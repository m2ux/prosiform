# Change List

The plan changes the W01+W02 delivery session applied and held.

## Applied

- **Folded work: the example-tree checks follow the nested arrangement.** Nesting pushes the example's Delivery Evidence headings past H6 wherever a mode without a pair reaches it, so the unit carried what `make check` needs without editing `example/work-planner`: the `usage-example` fixtures for the Plan and Advance modes record the depth overflow, the example README states those refusals in place of the removed expected bundles, the handoff round-trip test holds the five overflowing modes to that refusal, and the mock scenarios bundle the Align mode. All of it goes with the tree in [I08:E08](https://github.com/m2ux/prosiform/issues/465) W00.

W01 and W02 link the merged [#543](https://github.com/m2ux/prosiform/pull/543), with Done and AC1–AC4 ticked, on [#458](https://github.com/m2ux/prosiform/issues/458), which records delivery rather than changing the plan, and the draft review pull request [#541](https://github.com/m2ux/prosiform/pull/541) carries their Changes and References.

## Held

None. No initiative was needed, validation found no deferred debt, and no issue arose that the plan does not already hold.

## Notes

- **The design debt is fixed.** *Group isolation* stated each contributing source belongs to exactly one group, while *Presets — A document in several groups* and the build emit a document in each group its references select. Engineering `b7e5a449` reads each contribution as belonging to the group its membership names, states a nested group's opening at its level, and names the holder of a group a multi-group document places as the first of its groups the bundle places. The README pin moves to it.
- **The prose pages stay with their rows.** `invocation.md`, `docs/hierarchy.md` and the other pages describing a group as a top-level H1 are W03, W04 and the I09:E05 page rows; this unit changed only the source, the tests, the corpus and the checks that read the example.
- **A linked bootstrap specimen document now declares.** The specimen's helper wrote an ungrouped document with no frontmatter, which a run treats as text; it now declares `prosiform: {}`, and the shared documents drop their group so the five-deep chain stays within H6.
