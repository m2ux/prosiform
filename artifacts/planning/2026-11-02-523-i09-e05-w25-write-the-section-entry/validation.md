# Validation — I09:E05 W25–W27, W33

Every check the work items name, run in the unit worktree on branch `i09/e05/w25-write-the-section-entry` at `1fe57960`.

## Section entry

`test_a_section_entry_compiles_its_section_alone` passes under `make harness`. `pf workflow.md#onboarding` writes `workflow__onboarding.bundles/workflow__onboarding.bundle.md`, carrying each state of `document-fragment` with its action and neither the Upkeep section nor the note it links; `pf workflow.md` carries the note. Observes AC26 and AC37.

## Section composition

`test_composed_sections_stand_beneath_the_step_naming_them` passes. Each scenario's path holds its permutation's state and no other's; `Configure` carries one `Inputs` destination section with the settings then the schema contribution; `Migrate` carries `[↳ Steps](reference/migration.md#steps)` and none of the deferred body, which `pf reference/migration.md#steps` compiles; `Amend` carries `Rules` and `Lint` beneath the `Amendment` contribution. Observes AC27.

## Declared inclusion

`test_a_declared_link_is_followed_and_an_undeclared_one_left_as_text` and `test_a_document_declaring_under_the_undeclared_directory_is_a_fault` pass. Each scenario's path holds its permutation's state and no other's; Inspect's link names `#verify` and the bundle carries Verify's action; Liaise's link stays `../undeclared/handover.md` and the bundle carries no Handover heading. Observes AC28.

## Corpus

The per-workflow corpus tests pass for the three workflows: each form bundles clean carrying every state, the sections state the diagram's transitions, each entry carries only what its form allows, every document declares save those under `undeclared/`, and each scenario's path is the walk its inputs determine. Observes AC26, AC27 and AC28.

## Runner

The runner tests pass over the whole corpus with the stub agent, each bundled form's workspace holding the entry's bundle as `workflow.md`, the section entry's included. Observes AC37.

## Full check

`make harness`: 1193 passed. `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check`: exit 0.

## Default cells

The default matrix runs the Claude harness, which carries no shell, over `bundle` and `tree` for these workflows.

| Scenario | `bundle` | `tree` |
| --- | --- | --- |
| `document-fragment` | The agent follows a bundle compiled from `workflow.md#onboarding`, which carries Onboarding alone. | The agent follows the whole handbook's source, the Upkeep section beside the workflow. |
| `merged-sources` | The agent passes through a step carrying one destination section with two sources' contributions. | The agent passes through the step's source, its directives unresolved. |
| `deferred-occurrence` | The agent completes the path through a step carrying a `↳` line. It cannot prove activation: no shell runs `pf`, and the workspace holds no source for the line to name. The harness test proves the line's reference activates. | The agent passes through the step's `[¬→]` source. Activation is unproven for the same reason. |
| `nested-composition` | The agent passes through a step carrying a contribution with a nested contribution beneath it. | The agent passes through the step's source, its directives unresolved. |
| `declared-link-followed` | The agent reaches Verify through a link the bundle rewrote to its section. | The agent reaches Verify through the source link to its document. |
| `undeclared-link-as-text` | The agent passes a link the bundle left as written, to a document the workspace lacks. | The agent passes the same link, its document present in the tree. |
