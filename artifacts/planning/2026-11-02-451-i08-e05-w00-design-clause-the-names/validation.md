# Validation

Evidence for each check `w00.md` names, run in the task worktree with `PROSIFORM_BUILD` naming the worktree's own build.

## Tested revisions

- **Design:** engineering `a7069f30`, which the README badge pins.
- **Task branch:** `i08/e05/w00-design-clause-the-names` at `999be768`.

## Conformance

`make conformance` at the new pin, observing AC6.

- **The design states the option.** `CLI contract — --budget NAME=VALUE` is a clause of the pinned design.
- **The design states the eight names and their counting rules.** The Resource limits table is keyed `files`, `file-bytes`, `input-bytes`, `output-bytes`, `targets`, `links`, `nesting` and `depth`, each a clause carrying its default and counting rule, and each budget fixture declares its row by name: `files` 3, `file-bytes` 3, `input-bytes` 1, `output-bytes` 1, `targets` 1, `links` 3, `nesting` 2, `depth` 2.
- **The refusals the epic's fixtures will name are clauses.** `Resource limits — Unknown name`, `— Malformed entry`, `— Name given twice` and `— Nesting floor` stand in the pinned design, uncovered until W05 lands their fixtures.
- **Every declaration lands.** The report closes with 0 declarations naming no clause: 332 clauses, 65 covered by no fixture.
- **No retired letter remains.** No section of the pinned design names `-F`, `-B`, `-I`, `-O`, `-T`, `-L`, `-N` or `-E`.

## Repository check

`make check` exits 0: unit and harness suites (1564 and 1149 passed), corpus 421 of 421 fixtures pass, smoke, layout, tables, links, vocabulary, invocation, conformance, independence and mock scenarios all hold. `make invocation` still compares the lettered options: the documented table and the help output change together in W01 and W04.

## Merge

Continuous integration passed on `999be768`, and [#549](https://github.com/m2ux/prosiform/pull/549) merged into `i08/e05/main` as `220a19cf`.
