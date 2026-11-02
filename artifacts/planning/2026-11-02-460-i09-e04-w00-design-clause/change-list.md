# Change List

The plan changes the W00 delivery session applied and held.

## Applied

None. W00 linked [#553](https://github.com/m2ux/prosiform/pull/553) on [#460](https://github.com/m2ux/prosiform/issues/460), which records delivery rather than changing the plan.

## Held

- **The W00 merge.** `make check` fails at `conformance` on eight `Resource limits` declarations that I08:E05's design commit `a7069f30` retires, because its fixtures and build reach `main` only with [#550](https://github.com/m2ux/prosiform/pull/550). #553 stays open and unmerged; Done, `AC15` and the epic's draft review pull request wait on #550 merging and `i09/e04/main` taking `main`.
- **AC18's demonstration.** AC18 reads "as a fixture whose composed section a selected preset places demonstrates", and W09's test row says the same. The clause states that a `group` pair places no contribution, so a selected preset governs a contribution through its `subst` alone. Rewording a criterion is outside the allowance's change kinds, so the wording is held for the user: "a fixture whose composed section a selected preset's `subst` governs".

## Notes

- **No new code.** A composition cycle is refused under `E_UNSUPPORTED_CONSTRUCT` with its chain, as the operator refusals are. A code of its own would need the fixture schema, a fixture and the build at once, which W05 may add with its fixtures.
- **No new budget.** Materialised contributions count toward `output-bytes` as they are composed and each directive is a `depth` hop, so *Resource limits*, which I08:E05 restates, keeps its eight names.
- **The operator marks.** `¬`, `⇉`, `⫽` and the guide's `↳` are excluded from the directive label set, so a lone mark stays an ordinary link and the guide's inline-target rule keeps its meaning. A deferred directive's contribution carries a generated `↳` line, so the guide already tells an agent how to activate it.
- **The pin carries I08:E05.** `99bec9f7` sits after `a7069f30` on `engineering`, so this base pins a design holding both.
