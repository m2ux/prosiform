# Changes — I00:E10:W02

Delivered by [#167](https://github.com/m2ux/prosiform/pull/167), merged into `i00/e10/main` at `17f6e42`.

## Checks

| Change | Where |
| --- | --- |
| The conformance report: the clause mapping, the uncovered list, the declarations naming no clause, and the declared surface | `checks/conformance.py` |
| Nine cases holding the report's reading of a design and a corpus, the uncovered listing, the declared surface and the reproduction of the mapping | `checks/tests/test_conformance.py` |
| The exit statuses the schema declares, read there as the code catalogues are | `checks/manifests.py` |
| `make conformance` runs the report, and `make check` runs it with the rest | `Makefile` |

## Corpus

| Change | Where |
| --- | --- |
| 120 manifests name their clauses by the design's heading and the enumerated rule under it, with the case each fixture takes following a comma | `fixtures/*/*/manifest.toml` |
| The clause form a manifest writes, and the adversarial families read as the clauses they are | `fixtures/README.md` |

## Documentation

| Change | Where |
| --- | --- |
| The conformance check in the command table, and the environment it runs from | `README.md` |
| The conformance check in the check table, with what it asserts and what it fails on | `checks/README.md` |

## Tracker

| Change | Where |
| --- | --- |
| W02 linked to its pull request and ticked, with AC2, AC3 and AC5 | [#9](https://github.com/m2ux/prosiform/issues/9) |
| The review pull request for `i00/e10/main`, linked to the epic in its Development field | [#168](https://github.com/m2ux/prosiform/pull/168) |
| Rows W32 and W33 and criteria AC33, AC34 and AC35 added | [#39](https://github.com/m2ux/prosiform/issues/39) |
| Clause coverage raised as deferred debt, placed on the Bundling board in Backlog | [#169](https://github.com/m2ux/prosiform/issues/169) |
| The codes a build reports raised as deferred debt, placed on the Bundling board in Backlog | [#170](https://github.com/m2ux/prosiform/issues/170) |

## Plan changes

| Kind | Subject | Applied |
| --- | --- | --- |
| Task creation | W32 on [#39](https://github.com/m2ux/prosiform/issues/39), delivered by [#169](https://github.com/m2ux/prosiform/issues/169) | Applied |
| Task creation | W33 on [#39](https://github.com/m2ux/prosiform/issues/39), delivered by [#170](https://github.com/m2ux/prosiform/issues/170) | Applied |
| Folded work | AC33, AC34 and AC35 added to [#39](https://github.com/m2ux/prosiform/issues/39), so its new rows carry criteria | Applied |
| Re-prioritisation | [#169](https://github.com/m2ux/prosiform/issues/169) and [#170](https://github.com/m2ux/prosiform/issues/170) placed on the Bundling board in Backlog | Applied |

Nothing was held: no change this session met needed an initiative of its own.

## What remains open

**66 clauses are reached by no fixture**, nine of them the design's own non-behavioural sections. The report prints the figure every run and [W32](https://github.com/m2ux/prosiform/issues/169) carries the work.

**A code a build emits outside the corpus is held to nothing.** Within the corpus the codes a build emits are the codes the design declares; a path no fixture reaches is observed by neither reading, and [W33](https://github.com/m2ux/prosiform/issues/170) carries it.

**AC1 stays unticked on [#9](https://github.com/m2ux/prosiform/issues/9).** The report emits the family listing [W01](https://github.com/m2ux/prosiform/pull/166)'s script stood in for, and reports the same two families held by nothing: Consistency and Parser exhaustion, each a tracked row of [#39](https://github.com/m2ux/prosiform/issues/39).
