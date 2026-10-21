# Changes — I00:E10:W03

Delivered by [#171](https://github.com/m2ux/prosiform/pull/171), merged into `i00/e10/main` at `68a56a1`.

## Checks

| Change | Where |
| --- | --- |
| The independence check: the inventory of implementation terms, the scan of the corpus's declarations and the conformance report's entries, and the contract's declared names held apart from that inventory | `checks/independence.py` |
| Twelve cases holding the scan of a declaration, a fixture identity and a report entry naming an implementation, the interface terms it admits, and the disjointness of the inventory from the contract's declared names | `checks/tests/test_independence.py` |
| The rows of every table one header cell marks, read beside the other document reading the checks share | `checks/documents.py`, `checks/invocation.py` |
| `make independence` runs the check, and `make check` runs it with the rest | `Makefile` |

## Documentation

| Change | Where |
| --- | --- |
| The independence check in the command table, and the environment it runs from | `README.md` |
| The independence check in the check table, with what it asserts and what it fails on, and what it scans and why | `checks/README.md` |

## Tracker

| Change | Where |
| --- | --- |
| W03 linked to its pull request and ticked, with AC4 | [#9](https://github.com/m2ux/prosiform/issues/9) |
| The review pull request for `i00/e10/main` carrying this row's change and citing its pull request | [#168](https://github.com/m2ux/prosiform/pull/168) |
| Row W34 and criteria AC36 and AC37 added | [#39](https://github.com/m2ux/prosiform/issues/39) |
| The reference the inventory does not name raised as deferred debt, placed on the Bundling board in Backlog | [#172](https://github.com/m2ux/prosiform/issues/172) |

## Plan changes

| Kind | Subject | Applied |
| --- | --- | --- |
| Task creation | W34 on [#39](https://github.com/m2ux/prosiform/issues/39), delivered by [#172](https://github.com/m2ux/prosiform/issues/172) | Applied |
| Folded work | AC36 and AC37 added to [#39](https://github.com/m2ux/prosiform/issues/39), so its new row carries criteria | Applied |
| Re-prioritisation | [#172](https://github.com/m2ux/prosiform/issues/172) placed on the Bundling board in Backlog | Applied |

Nothing was held: no change this session met needed an initiative of its own.

## What remains open

**An implementation reference the inventory does not name passes the check.** The inventory bounds what is refused, and the disjointness check bounds the contract's declared names against it, but nothing bounds a term spelled in a word the list does not hold. Holding a declaration to the vocabulary the design and the glossary already state is the direction, and [W34](https://github.com/m2ux/prosiform/issues/172) carries it.

**AC1, AC7 and AC8 stay unticked on [#9](https://github.com/m2ux/prosiform/issues/9).** AC1 waits on the two adversarial families W01 left held by nothing, each a tracked row of [#39](https://github.com/m2ux/prosiform/issues/39); AC7 and AC8 are W04 and W05, a unit this row does not carry.
