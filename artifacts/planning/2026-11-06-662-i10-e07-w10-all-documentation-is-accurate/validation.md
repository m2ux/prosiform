# W10 Validation

## Revisions and Scope

Task head: `619a9e7d6ef2bfa1ea6e5258f45fb671de0e39d5`, based on W09 merged base `f04086096c666cc29241a7fda3dcbdfd9c354743`. Task pull request: [673](https://github.com/m2ux/prosiform/pull/673), targeting `i10/e07/main`. The task changes maintained documentation and observing documentation tests, not compiler behavior. Engineering audit publication: `1dbab81e6438b853f47ae2c1cf3dc98e651774b5`.

## Claim-Observing Tests

`revision-check.py --project <task-worktree> --revision 619a9e7d6ef2bfa1ea6e5258f45fb671de0e39d5 -- env -u VIRTUAL_ENV uv run --project src --frozen pytest --config-file src/pyproject.toml --rootdir . checks/tests/test_authoring.py src/tests/test_tags.py src/tests/test_source.py src/tests/test_selection.py src/tests/test_entry_presets.py src/tests/test_dispatch_variants.py src/tests/test_dispatch_publication.py src/tests/test_deferred_titles.py src/tests/test_deferred_presets.py evals/diagram-following/test_workflow.py evals/diagram-following/test_score.py -q` passed in its own detached checkout, exit 0: 954 tests. The checkout uses its own local `src` environment/build, not another worktree's build.

- All 15 authoring tests pass, including executed README/invocation source-copy commands, parsed fixture templates, focused deferred/budget commands and complete module inventory.
- Shared tags/source/selection/entry tests observe normalization, defaults, occurrence locality, resources, substitution, grammar, paths, quoted guide examples and leading dashes.
- Variant/publication/deferred tests observe equivalent and distinct dispatches, selected filenames, collisions, cycles/depth/budgets, title preservation and immediate/deferred parity.
- All 508 deterministic workflow/scorer tests pass, including tagged deferrals and dispatch variants. No paid agent session runs.

The human claim-to-implementation review is [audit.md](audit.md), not inferred from string-presence tests. AC22 draws on that recorded review and these executable observations.

## Inventory and Contract Review

`revision-check.py --project <task-worktree> --revision 619a9e7d6ef2bfa1ea6e5258f45fb671de0e39d5 -- python3 <published-record>/audit-check.py` passed, exit 0. Exact-checkout inventory matches all 1,964 tracked documentation paths:

- 26 primary maintained guidance pages, read and reviewed individually in the audit.
- 1,566 corpus specimens, observed through corpus execution rather than rewritten as instructions.
- 370 executable workflow source documents, observed through deterministic workflow tests.
- Two historical live-run reports, retained as historical evidence.

Additional surfaces are the CLI help/guide, nine checked SVG examples and maintained engineering/design/planning entry points. Every feature obligation is mapped in [Contract-to-Documentation Coverage](audit.md#contract-to-documentation-coverage), with observations and explicit exclusions. No path is left unclassified. The instrument establishes inventory agreement/classification, not semantic prose truth; AC23 also requires the recorded human contract review.

## Checked Examples

`make examples` passed at the task tree, regenerating all nine cases from `scripts/examples.json`: destinations, dispatch, groups, parallel, references, run, sections and source exit 0; refused exits the declared 1. All checked SVGs reproduce byte-identically, so no generated output change is needed.

## Full Configured Check

The final committed-head full check is in progress. Results are recorded before a passing pull-request Test Plan or merge is published.

## Review and Limitations

- Whole maintained-page review and claim/contract matrices are published in [audit.md](audit.md); no blanket claim is made about historical records or live agent behavior.
- Lint, formatting and strict typing pass for the complete configured source set. Editor diagnostics report no errors in the changed Python test.
- An initial new executable authoring test tried to treat README's informational `pf -v` as a compile command; it was corrected to execute only documented compile entries. A standalone mypy invocation omitted the repository's module context; the full configured typecheck passes. No compiler defect was found.
- Existing `config/branches` is absent at the historical epic base, so integration/target-route/review checks depending on it remain unevaluated. No branch configuration is invented, and no epic review readiness is asserted.
- No release, compiler redesign, unrelated repair or paid eval is authorized or performed. The only plan refinement is the documentation audit's concrete observing instruments.

## CI and Delivery

[Checks CI run](https://github.com/m2ux/prosiform/actions/runs/42234017168) is associated with exact task head `619a9e7d6ef2bfa1ea6e5258f45fb671de0e39d5`; it must succeed before merge. Development relation to epic 662 is verified from both ends, with existing links preserved. W10 delivery and AC22/23 remain unrecorded until confirmed merge and merged-revision instruments.

Default/engineering integration and draft review pull requests 664 and 666 remain with the coordinator. This task does not change their readiness or close the epic.
