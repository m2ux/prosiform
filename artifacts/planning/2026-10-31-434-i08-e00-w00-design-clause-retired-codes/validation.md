# Validation — W00 Design Clause, Retired Codes and Pin

> Evidence record · Created 2026-10-31

Every check below ran in the worktree `.worktrees/i08/e00/w00-design-clause-retired-codes` on branch `i08/e00/w00-design-clause-retired-codes`, cut from `i08/e00/main` at `23882b7d`. The build under test was named by `PROSIFORM_BUILD` as `uv run --project <worktree>/src --frozen pf`, the same form the continuous-integration job supplies.

The design amendment is `771f8c1b` on `engineering`, stating the declaration, presets, exclusion, conformance faults and named budgets. The pin in `README.md` names it.

## T1 — The clause set the epic's fixtures cite is absent at the previous pin

**Ran:** `make conformance` at the previous pin `4c72d818`, the corpus unchanged.

**Observed:** exit `0`, `303 clause(s) the design states, 55 covered by no fixture, 0 declaration(s) naming no clause`. No clause of the `fixtures/inclusion/` family exists, so no fixture could name one.

## T2 — The amendment lands and the pin names it

**Ran:** `git push origin engineering` from the engineering worktree, then `make conformance` at the new pin `771f8c1b`.

**Observed:** exit `1`, `309 clause(s) the design states, 72 covered by no fixture, 12 declaration(s) naming no clause`. Six clauses are added and eight renamed; the count rises by six because the eight budget options collapse into eight named rows under one clause.

## T3 — The corpus is unchanged by the amendment

**Ran:** `make corpus` at the new pin, the build unchanged.

**Observed:** exit `0`, `349 fixture(s), 349 pass, 0 fail, 0 awaited, 0 unexpected pass`. No source tree, invocation or expected bundle in the corpus changes, which is the property the clause states: the bundles the example published before this epic are the ones it publishes after it.

## T4 — T2's failures are the clause renames, not a defect

**Ran:** the failing declarations, grouped from the `make conformance` report.

| Retired declaration | Fixtures | What the design now states |
| --- | --- | --- |
| `Resource limits — -F`, `-B`, `-I`, `-O`, `-T`, `-L`, `-N`, `-E` | 13 | `Resource limits — files`, `file-bytes`, `input-bytes`, `output-bytes`, `targets`, `links`, `nesting`, `depth`, one row per ceiling, with the name as the clause's identifier |
| `Link classification and resource handling — Local Markdown document links under the root` | 10 | no clause of that name; the clause is now `Local Markdown document links` |
| `Link classification and resource handling — Local Markdown links resolving outside the root` | 9 | no clause of that name; the clause is now `A link naming a document that declares nothing` |
| `CLI contract — -f DOC, …` | 2 | no such option row; a fragment-only entry is refused, and `document#fragment` is the one spelling |
| `Reference normalization and path identity, a fragment-only command-line reference requires -f` | 2 | no such rule; the step states that a positional reference is `document` or `document#fragment` |

33 distinct fixtures across twelve families declare a clause this amendment retires or renames.

## Findings

- **Blocking, and unresolved.** A design amendment cannot land red. The two link-classification renames are mechanical and belong to this row, but retiring the budget letters and `-f` is a behaviour change no merged row has made: the build still accepts `-F` and `-f`, so the instruments still exercise them. Stating the retirement in the design before the build implements it leaves `make conformance` failing across twelve families and makes the pinned contract describe a build that does not exist.
- **The row's grain is the cause.** The row was planned to carry seven amendments at one pin so that seven epics would not serialise on one commit. That optimisation trades a chain of seven pull requests for one pull request that cannot be green until six other epics' code has landed, which is a longer chain rather than a shorter one.

The amendment itself is committed and pushed to `engineering` at `771f8c1b`; it is not published as a change to the canonical contract, since the pin this branch moves is the statement that would adopt it.
