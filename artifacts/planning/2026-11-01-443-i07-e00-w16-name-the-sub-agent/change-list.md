# Change List — W16

> Delivery record · Created 2026-11-01

## Pull request

| Field | Value |
| --- | --- |
| Pull request | [#477](https://github.com/m2ux/prosiform/pull/477) |
| Base | `i07/e00/main` |
| Branch | `i07/e00/w16-name-the-sub-agent` |
| State | merged |
| Merge commit | `43a4a093d08dda9f0e4f970399e57e46f979f28e` |
| Epic | [#443](https://github.com/m2ux/prosiform/issues/443) |

Merged into `i07/e00/main`, never `main`, after merging W09, W08 and W10 from the base and rerunning `make check` and CI on each new head. The epic's `W16` row carries the pull request with its Done cell ticked, `AC25` is ticked, and the review pull request [#473](https://github.com/m2ux/prosiform/pull/473) cites #477.

## Commits

| Commit | Subject |
| --- | --- |
| `3cc80dc4` | name the sub-agent trace in every dispatching instruction |
| `0a442443` | write a stub sub-agent trace only from a prompt that names it |
| `5b60d70a` | state that the bootstrap form takes its own instruction |

## Files

| File | Change |
| --- | --- |
| `evals/diagram-following/instruction.md` | Tells the session to hand each sub-agent `trace-<section>.log`; the header names the bootstrap form's own instruction |
| `evals/diagram-following/instruction-bootstrap.md` | The same sentence, addressed to the dispatching session, replaces the one addressed to the sub-agent |
| `evals/diagram-following/score.py` | `SUB_AGENT_TRACE` beside `TRACE` and `TRACES` |
| `evals/diagram-following/stub_agent.py` | The `Task` prompt names the trace only from an instruction that states it; a sub-agent writes only the trace its prompt names |
| `evals/diagram-following/test_workflow.py` | Every form's instruction states the sentence |
| `evals/diagram-following/test_run.py` | A scored dispatch in the compiled and the authored form; an untold sub-agent keeps no trace |
| `evals/diagram-following/README.md` | Scoring states the hand-on rule; the instruction paragraph names the bootstrap instruction |

## Plan changes applied

- **Task creation.** [I07:E01 W02](https://github.com/m2ux/prosiform/issues/485) and `AC2` added to [I07:E01 Deferred Debt](https://github.com/m2ux/prosiform/issues/479): the eval README states the `bootstrap` form and the `--forms` default `run.py` takes.

## Plan changes held

None.

## Technical debt

- **Trivial, fixed here.** `instruction.md` and the eval README said every session takes the same instruction; the bootstrap form takes its own.
- **Non-trivial, deferred.** The eval README's Forms section, its form count and its `--forms` default omit `bootstrap`. Deferred as #485 under I07:E01.

## Arising issues

None beyond the deferred item.
