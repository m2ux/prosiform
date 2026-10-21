# Carried Debt: The Rows That Share a Pull Request — October 2026

> Planning · Created 2026-10-21

## Executive Summary

[#187 \[I01:E03\]](https://github.com/m2ux/prosiform/issues/187) holds eight rows carried from the prototype initiative's clear-up epic because no run of the tool shows them. Before its first task starts, every pair of rows where neither depends on the other is accounted for: the pair that shares a pull request names the other in `Joins`, and each pair that keeps its own is named here with the reason.

One pair shares a pull request. W06 and W07 both change `checks/independence.py`, and they change it for one reason — the vocabulary a corpus declaration is entitled to state. Delivering them apart would have two sessions editing one check against the same contract text.

The remaining twenty-seven pairs keep their own pull requests. The reason is the same in almost every case and is stated once below rather than twenty-seven times: the rows change separate components, and a criterion each row delivers is observable without the other's work.

## Components

Read from `main` at `18308e8`.

| Row | Issue | Changes |
| --- | --- | --- |
| W01 | [#158](https://github.com/m2ux/prosiform/issues/158) | `checks/documents.py` and `checks/tests/test_documents.py` |
| W02 | [#160](https://github.com/m2ux/prosiform/issues/160) | a new module under `checks/` with its tests, `Makefile`, `checks.md`, `checks/README.md`, `src/README.md` |
| W03 | [#161](https://github.com/m2ux/prosiform/issues/161) | `fixtures/` and `fixtures/README.md`, and the design's group-rule clause |
| W04 | [#162](https://github.com/m2ux/prosiform/issues/162) | one repository document, which gains a tracker reference |
| W05 | [#177](https://github.com/m2ux/prosiform/issues/177) | `design.md` and `docs/glossary.md`, both on `engineering` |
| W06 | [#185](https://github.com/m2ux/prosiform/issues/185) | `checks/independence.py` |
| W07 | [#186](https://github.com/m2ux/prosiform/issues/186) | `checks/independence.py` and one fixture declaration |
| W08 | [#189](https://github.com/m2ux/prosiform/issues/189) | `checks/corpus.py`, `fixtures/README.md`, `checks/README.md` |

## The Pair That Shares a Pull Request

- **W06 and W07.**
  Both change the vocabulary `checks/independence.py` reads a declaration against. W06 removes the words a design section stating no behaviour contributes; W07 adds the terms the glossary names as deliberately not used. Each is a rule about what the check admits, and the two rules are read in one pass over one source of truth, so one pull request states both or the second rewrites the first.

## The Pairs That Keep Their Own

Neither row of any pair below depends on the other, and each keeps its own pull request.

- **Separate components, independent criteria.**
  Every pair drawn from W01, W02, W03, W04, W05 and W08, and every pair joining one of those to W06 or to W07, changes a different component. Each criterion is observed by an instrument the other row does not touch, so neither pull request is evidence for the other's criterion. That covers twenty-five of the twenty-seven pairs.

- **W02 with W04, and W02 with W08.**
  All three write `checks/README.md`, and W02 and W08 both write the command table that `checks.md` carries a second copy of. The contention is additive — a table row and a paragraph — rather than a shared concern, and `make tables` holds both copies in both directions, so a row added in one and missed in the other fails the check rather than passing quietly. The rows are kept apart because joining them would put three unrelated criteria behind one review, and the conflict a shared table row produces is resolved in a line.

- **W03 with W08.**
  Both write `fixtures/README.md`: W03 documents what the group-rule code's fixtures cover, W08 documents the runner request that names one fixture. Different sections of one guide, and neither statement is read by the other's criterion.

## Decisions

- **W06 and W07 are joined; every other pair keeps its own pull request.**
  Confirmed 2026-10-21. The alternative considered was joining W04 into W08, since W08 writes prose in `checks/README.md` that could carry the tracker reference W04 needs and make W04 nearly free. It was refused because it makes W04's criterion depend on how another row happened to word its documentation, which is a coupling the criterion does not state.

- **I01:E02 depends on E03.**
  Confirmed 2026-10-21. The freeze's AC6 requires the design and the corpus to carry one tagged revision a production build can name. W05 rewrites the design record's CLI contract, and W03 and W07 change corpus fixtures and declarations, so a tag taken before E03 lands names a revision E03 then edits.

- **I01's AC10 stands as written.**
  Confirmed 2026-10-21. E03's rows are debt found during the prototype initiative's delivery, not entries the findings ledger recorded from use, so AC5 does not cover them and the epic would otherwise claim no initiative criterion.

## Links

| Resource | Link |
| --- | --- |
| Epic | [#187 \[I01:E03\] Carried Debt](https://github.com/m2ux/prosiform/issues/187) |
| Initiative | [#20 \[I01\] Field Refinement](https://github.com/m2ux/prosiform/issues/20) |
| Origin epic | [#39 \[I00:E11\] Deferred Debt](https://github.com/m2ux/prosiform/issues/39) |
| Criticality reading | [The three faults a run shows its user](https://github.com/m2ux/prosiform/tree/engineering/artifacts/planning/2026-10-21-163-i00-e11-w29-a-member-whose-whole) |
