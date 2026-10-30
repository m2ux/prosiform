# Operators Followed by a Space — October 2026

> Delivery Record · Created 2026-10-26

## Executive Summary

A link's text opens an operator only when the mark is followed by at least one space (U+0020). `[⇉ Sync](sync.md)` dispatches and `[¬ Guide](g.md)` defers; `[⇉Sync](sync.md)` and `[¬Guide](g.md)` are ordinary links, compiled with the mark kept as text and no diagnostic. `[¬ ⇉ X](x.md)` opens both operators and is refused; `[¬⇉ X](x.md)` opens none and is an ordinary link.

## Artifacts

| Artifact | What it holds |
| --- | --- |
| [Work Item](w25.md) | Scope, rulings, the recognition rule, fixture outcomes |
| [Validation](validation.md) | Check results, the unspaced-mark audit and the work-planner bundles |

## Delivery Context

- Epic: I02 E00, issue #258; task W25.
- Task branch: `i02/e00/w25-operators-spaced`, cut from epic base `i02/e00/main` at `d56f3b2c`.
- Worktree: `.worktrees/i02-e00-w25`.
- Components: `src/prosiform/closure.py`, `src/tests`, `fixtures`, `invocation.md`, `docs/glossary.md`, `README.md` (design pin); `design.md` on this branch.
- Rulings (the user's, relayed): `⇉` opens the dispatch operator only when followed by at least one space; the deferral operator `¬` follows the same rule; one link states one operator applies to spaced marks only. No flag or compatibility path.

## Links

| Resource | Link |
| --- | --- |
| Epic | [I02:E00 Example Migration](https://github.com/m2ux/prosiform/issues/258) |
| Initiative | [I02 MVP Demonstration](https://github.com/m2ux/prosiform/issues/261) |
| Pull request | [#289](https://github.com/m2ux/prosiform/pull/289) |
