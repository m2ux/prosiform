# Change List — W07

> Delivery record · Created 2026-10-31

## Pull request

| Field | Value |
| --- | --- |
| Pull request | [#468](https://github.com/m2ux/prosiform/pull/468) |
| Base | `i07/e00/main` |
| Branch | `i07/e00/w07-make-the-cursor-harness` |
| State | merged |
| Merge commit | `d99025c152a77d7f3116277f5c58738f0c2c31f4` |
| Epic | [#443](https://github.com/m2ux/prosiform/issues/443) |

Merged into `i07/e00/main`, never `main`. The epic's `W07` row carries the pull request and its Done cell is ticked, and both of its criteria are ticked.

## Commits

| Commit | Subject |
| --- | --- |
| `718ad27e` | read a runner form as the corpus form it carries |
| `b1b7715d` | keep a sub-agent's trace under the name the instruction states |

## Files

| File | Change |
| --- | --- |
| `evals/diagram-following/run.py` | `observable` resolves the runner's form to the corpus form before asking for sections; `keep` globs `TRACES`; the records paragraph names the sub-agent trace it keeps |
| `evals/diagram-following/score.py` | `TRACES` beside `TRACE`, the pattern each kept trace answers to |
| `evals/diagram-following/stub_agent.py` | `write_sub_agent_traces` writes one `trace-<section>.log` per dispatched start |
| `evals/diagram-following/test_run.py` | AC15's matrix case; AC16's fixture uses the stated name and a scored dispatch case keeps both |
| `evals/diagram-following/README.md` | the records a run keeps name each sub-agent's trace |

## Plan changes applied

None. The work item's Analysis, Plan, Implementation, Review and Test rows were followed as written, and its Test row matched `AC15, AC16` without amendment: the Cursor matrix case is AC15's check and the scored dispatch case is AC16's.

## Plan changes held

None.

## Technical debt

None found in this scope that blocks delivery. Nothing trivial was deferred; nothing non-trivial was found.

## Findings delivered

| Finding | Severity | Delivered by |
| --- | --- | --- |
| 1 | blocker | AC15 — the Cursor matrix on the default form list |
| 8 | major | AC15 — the same defect, reached from the other epic's report |
| 2 | blocker | AC16 — the sub-agent trace under the stated name |

Findings 1 and 8 are one defect from two directions and are delivered by one criterion, as the epic's record states.
