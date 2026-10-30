# Validation — I05:E04:W01

The checks the W01 work item names, run on the task branch `i05/e04/w01-step-convention-in-the` at `06550393edbc07739903d8a57832d659ff132e72`, cut from `i05/e04/main` at `8e56baf3`. Each ran in the task worktree with `PROSIFORM_BUILD` naming that worktree's own `pf` through `uv run --project <worktree>/src --frozen pf`.

## Inspection

Observes AC1. Result: ✓.

- **`example/work-planner/guidelines.md`.**
  - Procedure states Step sub-sections: a procedure with more than one step writes each step as a sub-section one heading level below the procedure's heading, in the order performed and ahead of the procedure's child sections, headed by the step's position, a full stop and its action in title case (`### 6. Publish` under `## Procedure`, linked as `plan-mode.md#6-publish`).
  - Step anchors states that inserting or removing a step renumbers the anchors below it and that `pf`'s unresolved-link check reports a link naming an old one.
  - Sub-bullets, Separate actions, Spec layout, the modes' Procedure and Procedure steps, the protocols' Procedure, and the artifacts' Operations and Operation steps state the sub-section form; Subsection titles becomes Child section titles, so a step heading is not held to the three-word title rule.
- **`example/guidelines.md`.**
  - Procedure files defines a procedure as a top-level section holding step sub-sections, and its Procedure rule states the heading level, the heading form and the order ahead of child sections.
  - Commands defines a procedure the same way, and the Bold leads example names an item, not a step.
- **No rule left on the numbered form.**
  `grep -n -i 'numbered\|bold label\|action label'` over both files leaves two hits, Branch headers and Input labels, neither of which describes a step.
- **Agreement with Board Reads.**
  The wording matches `example/work-planner/artifacts/delivery-evidence.md`, whose Board Reads steps are `##### 1. Read Board State` to `##### 5. Read Board Assignee` under `#### Board Reads`.

## Links

`make links`: exit 0, `link check: every reference in 106 document(s) resolved`. Result: ✓.

## Corpus

`make corpus`: exit 0, `corpus check: 335 fixture(s), 335 pass, 0 fail, 0 awaited, 0 unexpected pass`. Result: ✓.

- No expected bundle changes. The one fixture reaching the guidelines, `a-mode-and-the-guidelines-it-defers`, defers its links to the skill guidelines and keeps its links to the shared guidelines outside the root, so neither file contributes content to a bundle, and no anchor it links (`#frontmatter`, `#layout`, `#prose`, `#commands`, `#changes`) changed.

## Check

`make check`: exit 0. Result: ✓.

- ruff `All checks passed!`; `src` pytest 1281 passed; `checks/tests` 720 passed; corpus 335 pass; smoke, layout, tables, links, vocabulary, invocation, conformance and independence all report ok.
- The same target on the base revision `8e56baf3` also exits 0.
