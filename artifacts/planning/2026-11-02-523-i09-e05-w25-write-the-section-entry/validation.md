# Validation — I09:E05 W25–W27, W33

Every check the work items name, run in the unit worktree on branch `i09/e05/w25-write-the-section-entry`.

| Check | Command | Result |
| --- | --- | --- |
| Harness | `make harness` | 1193 passed |
| Full check | `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf' make check` | exit 0 |

## What each scenario proves in the default matrix

The default matrix runs the Claude harness, which carries no shell, over `bundle` and `tree` for these workflows.

| Scenario | `bundle` | `tree` |
| --- | --- | --- |
| `document-fragment` | The agent follows a bundle compiled from `workflow.md#onboarding`, which carries Onboarding alone. | The agent follows the whole handbook's source, the Upkeep section beside the workflow. |
| `merged-sources` | The agent passes through a step carrying one destination section with two sources' contributions. | The agent passes through the step's source, its directives unresolved. |
| `deferred-occurrence` | The agent completes the path through a step carrying a `↳` line. It cannot prove activation: no shell runs `pf`, and the workspace holds no source for the line to name. `make harness` proves the line's reference activates. | The agent passes through the step's `[¬→]` source. Activation is unproven for the same reason. |
| `nested-composition` | The agent passes through a step carrying a contribution with a nested contribution beneath it. | The agent passes through the step's source, its directives unresolved. |
| `declared-link-followed` | The agent reaches Verify through a link the bundle rewrote to its section. | The agent reaches Verify through the source link to its document. |
| `undeclared-link-as-text` | The agent passes a link the bundle left as written, to a document the workspace lacks. | The agent passes the same link, its document present in the tree. |
