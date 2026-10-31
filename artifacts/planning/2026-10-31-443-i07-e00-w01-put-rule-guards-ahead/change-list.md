# Change List — W01 Put Rule Guards Ahead of the Corpus

> Delivery record · 2026-10-31

The plan changes this session applied, the ones it held, and the technical debt it classified.

## Applied

| Change | Kind | Why | Where |
| --- | --- | --- | --- |
| `steps` and `authoring` named ahead of `test` and `corpus` in `check:` | Build order | The epic states the check order lands first, because until both guards run ahead of the bundling targets a broken corpus reports moved bytes rather than the rule | `Makefile` |
| The header stating why both guards precede both bundling targets | Documentation | The order is a rule the `Makefile` states, not an incidental arrangement | `Makefile` |
| The order test held to every guard against every bundling target | Test | The prior test held one pair, so the `steps` finding could not have been caught by it | `checks/tests/test_check_order.py` |
| Each guard's position stated ahead of both targets it precedes | Documentation | The prose named the `authoring`-before-`corpus` pair alone | `checks/README.md` |
| The order claim pointed at the `Makefile` rather than at the table's row order | Documentation | `checks.md` lists the commands in its own order, which is not the order `check:` runs them in; the old wording claimed they were the same | `checks.md` |

No finding moved between tasks, no task was created, closed or renumbered, and no criterion changed. The epic's disposition already carried findings 3 and 11 to W01, and the work item's Test row already named both injected cases, so the plan as written was followed without amendment.

## Held

| Held | Why |
| --- | --- |
| A separate target for the injected cases | The work item's Test row asks the order test to read the `Makefile`, and each injected case to be shown against `make check`. Both were shown here and are recorded in [validation.md](validation.md); a target that mutates the example tree to prove the order would put a destructive check into `make check` for a property the order test already holds |
| Moving any target other than `steps` and `authoring` | Findings 3 and 11 name those two. `test` and `harness` sit where they do for reasons outside this task's scope, and a reordering for its own sake would move checks whose position no finding faults |

## Technical debt classified

| Debt | Class | Disposition |
| --- | --- | --- |
| `test_linked_bootstrap` needs network for `uv build`, so `make check` cannot complete in a network-less environment | Deferred, not this task's | Reproduces on every settled branch and passes in CI; the brief names it as out of scope. No issue raised: it is a property of the sandbox rather than a defect in the repository |
| The publication tests fail under `/tmp`'s atomic folder swap | Deferred, not this task's | Same standing as above; passes in CI |

Nothing blocking and nothing trivial was found inside the Makefile scope beyond what this change delivers.

## Placement needs

None. No new initiative, epic or task was needed, and nothing was found that needs a home outside this pull request.
