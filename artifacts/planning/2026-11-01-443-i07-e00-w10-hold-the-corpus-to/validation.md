# Validation

> Validation · Created 2026-11-01

Each check the [work item](w10.md) names, run in the task worktree on branch `i07/e00/w10-hold-the-corpus-to` at `124ee13b`, and `make check` again at `ac8642ce` and `97b1c16d`, each after `origin/i07/e00/main` was merged in. CI passed on `97b1c16d`, which merged into `i07/e00/main` as `36f9b72a`. Each test was also run against the tree before the change, to show it fails there.

## T1 The linked bundle draws no branch label

**Covers:** AC22. **Result:** ✓

`test_the_linked_bundle_draws_no_branch_label[branching]` and `[looping]` bundle the linked form with this checkout's `pf` and read the entry bundle's one Mermaid diagram: it draws as many edges as the diagram form and none carries a label. Against the linked entries before the change, both fail, listing `Triage -->|high| Escalate`, `Triage -->|low| Queue` and `Review -->|revise| Revise`, `Review -->|approve| Publish`.

## T2 Every entry carries only what its form allows

**Covers:** AC23. **Result:** ✓

`test_each_entry_carries_only_what_its_form_allows` passes for every form of all eight workflows. A broken copy of each rule is a named fault:

- `test_a_linked_entry_labelling_a_branch_is_a_fault`: `the linked entry labels the edge Triage to Escalate 'high'`.
- `test_a_linked_entry_drawing_another_edge_is_a_fault`: `the linked entry draws edges the diagram does not`.
- `test_a_prose_entry_drawing_a_diagram_is_a_fault`: `the prose entry draws a diagram`.

Against the linked entries before the change, the corpus test fails on `branching/linked` and `looping/linked`, naming each labelled edge. The linked rules, now naming the state a branch enters, are held by `test_a_linked_rule_naming_a_state_its_decision_does_not_reach_is_a_fault`, `test_a_linked_rule_that_states_no_state_is_a_fault` and `test_a_linked_decision_resolves_its_branch_through_the_document`; every scenario of every form walks its path.

## T3 Every listed fixture renders

**Covers:** AC24. **Result:** ✓

`make render` with `MERMAID_CLI="npx -p @mermaid-js/mermaid-cli@11.16.0 mmdc"`: `render check: 17 fixture(s), 17 pass, 0 fail`. The two fixtures now listed pass: `a-sequence-diagram-destination-ending-at-a-semicolon` with `['#client']`, and `a-diagram-reached-through-a-linked-document` with `['#open', '#review', '#closed', '#notes']`.

Before the change, mermaid-cli refuses the semicolon fixture's bundle: `...lient;docs/server.md` ... `got 'NEWLINE'`, a parse error in the sequence diagram.

## T4 The render lists are held to every drawing fixture

**Covers:** AC24. **Result:** ✓

`checks/tests/test_render.py`, run by `make harness`: `test_every_drawing_rewriting_fixture_is_rendered` and `test_every_listed_fixture_is_a_drawing_rewriting_fixture` hold the render check's lists to exactly the `rewriting/` fixtures whose bundles draw a Mermaid diagram. `test_a_diagram_mermaid_cannot_parse_is_a_defect` shows a refused drawing returns `mermaid-cli exits 1: a diagram does not parse` with no anchors. Against `checks/render.py` before the change, the first fails naming `rewriting/a-sequence-diagram-destination-ending-at-a-semicolon`, and the last fails because the check had no such report.

## T5 make check

**Covers:** none. **Result:** ✓

`PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` exits 0 at every revision: at `97b1c16d`, `src` tests 1420 passed, harness 1091 passed, every other target passing.
