# Change List — W09

> Delivery record · Created 2026-11-01

## Pull request

| Field | Value |
| --- | --- |
| Pull request | [#481](https://github.com/m2ux/prosiform/pull/481) |
| Base | `i07/e00/main` |
| Branch | `i07/e00/w09-refuse-a-run-that` |
| State | merged |
| Merge commit | `d8c1876051337d32985170c7fcc6fea545e58ced` |
| Epic | [#443](https://github.com/m2ux/prosiform/issues/443) |

Merged into `i07/e00/main`, never `main`. The epic's `W09` row carries the pull request and its Done cell is ticked, and `AC19`, `AC20` and `AC21` are ticked. The review pull request [#473](https://github.com/m2ux/prosiform/pull/473) carries the change under Diagram-Following Eval and cites #481.

## Commits

| Commit | Subject |
| --- | --- |
| `61ce303c` | pass a dispatched set only where it started in one message |
| `63e06cbe` | refuse a run whose started sessions all errored |
| `d1bf924f` | write a baseline only from cells the run measured |
| `1530aa80` | state the set, refusal and baseline rules in the eval README and checks page |
| `6015a8cc` | merge of `origin/i07/e00/main` |

## Files

| File | Change |
| --- | --- |
| `evals/diagram-following/score.py` | `dispatched` passes a set only where no start between its first and last member opens a message; the module docstring states the rule |
| `evals/diagram-following/run.py` | `outcome` refuses a run whose started sessions all errored, whether or not its budget stopped it |
| `evals/diagram-following/report.py` | `--write-baseline` refuses a report holding no cell, naming the run's reason where it has one |
| `evals/diagram-following/test_score.py` | AC21's split-set case, with a set started together beside an unrelated start still passing |
| `evals/diagram-following/test_run.py` | AC19's budget-stopped case, replacing the test that asserted the defect; the refused-run baseline case matches the one refusal message |
| `evals/diagram-following/test_report.py` | AC20's empty-matrix case |
| `evals/diagram-following/README.md`, `checks.md` | the set, refusal and baseline rules as the eval holds them |

## Plan changes applied

None. The work item was followed as written, and its Test row matched `AC19, AC20, AC21` without amendment.

## Plan changes held

None.

## Technical debt

None found. No blocking, trivial or non-trivial item arose from the tests, the changed definitions or the pull request.

## Arising issues

None.

## Findings delivered

| Finding | Severity | Delivered by |
| --- | --- | --- |
| 9 | major | AC21 — the set check reads message boundaries |
| 23 | major | AC19 — the budget-stopped refusal |
| 24 | major | AC20 — the baseline written only from measured cells |
