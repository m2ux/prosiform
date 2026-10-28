# I05:E03:W10 Validation

Each check the work item's test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e03/w10-layout-permutation-fixtures-for`, cut from `i05/e03/main` at `c285144f4c993c714e2151052b147a913dd0b4b5`.
- **Tested revision.** `490b3ce1` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`, `pf 0.15.0 (skill-markdown-v4)`.
- **Contract.** The README pins the design at `429eaf810c6c985c3efde016cf0dcea8bd3eeb2f` on `engineering`. Every clause the new fixtures name is stated there; none needed a clause the pinned design lacks.
- **Derivation.** Each new fixture's expected bundles were written from the design's Dispatched bundles, Dispatch sub-sections, Parallel dispatch sub-sections, The Prosiform section, Ordinal assignment and Automatic output names clauses before the first run. The first run reproduced every one byte for byte; no expected file was changed after it.

## T1 New layout fixtures

AC22: each fixture this task adds, run by `make corpus`.

| Fixture | Layout | Observes |
| --- | --- | --- |
| `dispatch/a-dispatch-in-a-nested-section` | A dispatch in a nested section | The `⇉` link in a level-3 section points at `#### Dispatch sketch`, placed after the section's content and before its child `#### Detail`; `guide.bundle.md` and `sketch.bundle.md`, no diagnostic. |
| `dispatch/a-chain-of-two-dispatches` | A chain of depth two | `guide.bundle.md` and `plan.bundle.md` each open with `# Prosiform` and `## Dispatch`; `review.bundle.md` carries none; no `W_DISPATCH_DEPTH`. |
| `run-set/sets-in-sibling-and-nested-sections` | Sets in sibling and nested sections | Three `Dispatch in parallel` sub-sections at levels 3, 4 and 3, linked as `#dispatch-in-parallel`, `-1` and `-2` in bundle order; `review__source.bundle.md`, which two sets name, is one bundle listed in each with that set's link text; six bundles, no diagnostic. |
| `dispatch/several-joined-entries-each-dispatching` | Several joined entries | One `guide+mode.bundle.md` opening with one Prosiform section; `# Guide` carries `## Dispatch plan`, `# Mode` carries `## Dispatch review` then `## Dispatch plan` linked as `#dispatch-plan-1`; `plan.bundle.md`, which both entries dispatch, is one bundle; no diagnostic. |

## T2 Existing layout fixtures

AC22: each layout an earlier task's fixture already covers, run by the same `make corpus`.

| Layout | Fixture |
| --- | --- |
| A dispatch in a section | `dispatch/a-sub-section-per-section-before-its-child-sections` |
| A dispatch in the preamble | `prosiform/the-section-follows-a-preamble` |
| One target dispatched from two sections | `dispatch/a-sub-section-per-section-before-its-child-sections` |
| A chain of depth one | `dispatch/a-dispatched-target-is-a-bundle-of-its-own` |
| A chain of depth three | `dispatch/a-chain-of-three-dispatches` |
| A chain past the limit | `dispatch/a-fourth-dispatch-warns` |
| A refused cycle | `dispatch/a-cycle-of-dispatches-is-refused` |
| A refused level-6 dispatch | `dispatch/a-dispatch-in-a-level-six-section-is-refused` |
| A set in one section | `run-set/a-set-in-one-section` |
| A set beside a `⇉` link | `run-set/a-section-carrying-both-operators` |
| One target named twice in a set | `run-set/a-target-named-twice-in-one-set-is-listed-once` |

Each passes.

## T3 make corpus

`corpus check: 334 fixture(s), 334 pass, 0 fail, 0 awaited, 0 unexpected pass`: the 330 fixtures of the base and the four this task adds.

## T4 make conformance

302 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere. Coverage of the clauses the new fixtures name: Dispatched bundles 16 fixtures, Dispatch sub-sections 8, Parallel dispatch sub-sections 4, Dispatch depth 4, Ordinal assignment 12.

## T5 make check

`PROSIFORM_BUILD=<pf> make check` exited 0: lock check, lint, format check, type check, 1275 unit tests, 717 harness tests, the corpus, the installed-wheel smoke run, layout, tables, links, vocabulary, invocation, conformance and independence. `make independence` read 334 fixtures and found every word of every declaration one the contract states.
