# Validation

Evidence for each check `w00.md` names, run in the task worktree with `PROSIFORM_BUILD` naming the worktree's own build.

## Tested revisions

- **Design:** engineering `e7c0180b`, which the README badge pins. A concurrent session's sweep committed this clause under its own subject, `record the I09:E04 W00 merge, its validation and change list`; the commit carries the design change in full.
- **Task branch:** `i08/e06/w00-design-clause-retired-option` at `96322841`.
- **Unmerged clause carried.** The pin also carries I09:E04's section composition clauses (`601cba55`, `99bec9f7`), which are not yet in `main`. Conformance passes with them; `make vocabulary` needs the glossary to define the *composition directive* they mark, so the branch carries that one definition verbatim from I09:E04 W00.

## Conformance

`make conformance` at the new pin, observing AC13.

- **The only channel.** `Link classification and resource handling — The substitution mapping` states the union of the `subst` pairs the presets governing the writing document state as the one channel, resolved from the declaring document's directory and reaching only the links that document writes; 23 fixtures declare it.
- **The retired option.** `CLI contract — -m is retired` is a clause of the pinned design, uncovered until W01 and W11 land `fixtures/cli/the-mock-option-is-gone`. No other section names `-m`.
- **The renamed codes.** `W_SUBST_USED` (15 fixtures) and `W_SUBST_UNUSED` (3 fixtures) are declared by the design, reported by the build's `-C` listing and declared by the corpus; no `W_MOCK_` code remains in either.
- **Every declaration lands.** The report closes with 0 declarations naming no clause, 0 declared codes the build reports nowhere and 0 reported codes the contract declares nowhere: 356 clauses, 82 covered by no fixture.
- **The epic's fixtures have clauses.** A reference under no `subst`, an entry reference, a substitute's fragment-only link, a dispatched target's own presets, a folder side (`Conversion metadata — subst holds colon pairs`) and a pair reached only outside the selection are each stated at the pinned design.

## Repository check

`make check` exits 0: lint, format, typecheck, unit and harness suites (1592 and 1163 passed), corpus 433 of 433 fixtures pass, smoke, layout, tables, links, vocabulary (48 terms), invocation, conformance, independence and mock scenarios (5 of 5) all hold. `make invocation` still compares the `-m` row: the documented table and the help output change together in W04 and W11.
