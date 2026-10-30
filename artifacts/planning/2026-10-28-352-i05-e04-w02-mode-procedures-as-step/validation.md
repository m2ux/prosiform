# Validation — I05:E04:W02

The checks the W02 work item names, run on the task branch `i05/e04/w02-mode-procedures-as-step` at `43875ab4577521f3db49f7961903031131087f1f`, cut from `i05/e04/main` at `c388f714`. Each ran in the task worktree with `PROSIFORM_BUILD` naming that worktree's own `pf` through `uv run --project <worktree>/src --frozen pf`.

## Inspection

Observes AC2. Result: ✓.

- **Count.** The base held 86 top-level numbered steps across 12 procedures and no nested numbered list: advance 6, align 10, deliver 22 (9 + Run Delivery Session 10 + Hoist Arising Issue 3), hoist 8, plan 9, propose 8, revise 7, standup 6, sync 7, understand 3.
- **Form.** Each became a `N. Action` sub-section one level below its procedure: `###` under each `## Procedure`, `####` under deliver mode's `### Run Delivery Session` and `### Hoist Arising Issue`, which follow the main procedure's steps.
- **Nothing left.** `grep -rnE '^\s*[0-9]+\. ' example/work-planner/modes` returns no line, so no numbered step list and no bold step label remains.
- **Text unchanged.** A comparison of each mode against the base, with whitespace stripped and each old `N. **Label.**` and new `N. Label` reduced to the lowercased label, finds no difference in any of the ten files.
- **Action titles.** Labels keep their articles (`Read the Brief`, `Place It`); `example/work-planner/guidelines.md` Action titles states that a step heading is not a procedure title.

## Links

`make links`: exit 0, `link check: every reference in 106 document(s) resolved`. Result: ✓.

## Corpus

`make corpus`: exit 0, `corpus check: 335 fixture(s), 335 pass, 0 fail, 0 awaited, 0 unexpected pass`. Result: ✓.

- Regenerated: the advance, plan, revise and hoist mode bundles, and the sync and understand mode bundles both mode fixtures publish beside them. The two artifact-entry fixtures reproduce unchanged.
- Each bundle change is the conversion: steps become headings, `pf` puts a blank line between an instruction and its bullets, and each dispatch sub-section (`Dispatch Sync Mode`, `Dispatch Issue Placement` and the rest) sits one level below the step that dispatches it, `####` where it was `###`.

## Check

`make check`: exit 0. Result: ✓.

- ruff `All checks passed!`; mypy no issues in 64 files; `src` pytest 1281 passed; `checks/tests` 720 passed; corpus 335 pass; smoke, layout, tables, links, vocabulary, invocation, conformance and independence all report ok.
