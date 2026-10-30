# Dispatch Depth Warning — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

The dispatch operator is `⇉`, and `»` is an ordinary character. A dispatched target's own dispatches are now examined: pf computes, for analysis only, the closure each dispatched target would have as its own entry and follows its dispatches. A chain reaching a fourth hop warns `W_DISPATCH_DEPTH`; a chain returning to a target on it warns `W_DISPATCH_CYCLE`; a target with no numbered step warns `W_DISPATCH_NOT_PROCEDURAL`; a dispatch naming its own document warns `W_DISPATCH_SELF`. Every warning publishes the bundle and exits 0. A `¬` or `⇉` link naming no Markdown document or section under the root fails with `E_UNSUPPORTED_CONSTRUCT`.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w24.md) | Scope, rulings, the definitions and reporting rule, fixture outcomes |
| [Validation](validation.md) | Check results, the corpus re-run and the work-planner bundles |

## Delivery Context

- Epic: I02 E00, issue #258; task W24.
- Task branch: `i02/e00/w24-dispatch-depth-warning`, cut from epic base `i02/e00/main` at `736a7d25`; merged `da6d0515` (W23) before conversion of the example.
- Worktree: `.worktrees/i02-e00-w24`.
- Components: `src/prosiform` (`dispatch.py` new, `cli.py`, `closure.py`, docstrings in `bundle.py`, `rewrite.py`), `src/tests`, `fixtures`, `invocation.md`, `docs/glossary.md`, `README.md` (design pin), `example/work-planner`, `example/work-tracker`; `design.md` on this branch.
- Rulings (the user's, relayed): nested dispatch is allowed and a chain deeper than three warns; a cycle warns; `⇉` replaces `»` with no alias; an operator naming no Markdown target under the root fails; a non-procedural dispatched target warns; a dispatch of its own document warns; Deliver links Run Delivery Session without the operator. No flag for the depth limit. A parallel `⇉` operator beside `»` was briefed and withdrawn before commit.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#288](https://github.com/m2ux/prosiform/pull/288) |
