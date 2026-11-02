# Change List

The plan changes the W00 delivery session applied and held.

## Applied

None. W00 linked [#553](https://github.com/m2ux/prosiform/pull/553), which merged into `i09/e04/main`, and ticked Done and `AC15` on [#460](https://github.com/m2ux/prosiform/issues/460), which records delivery rather than changing the plan. The draft review pull request [#556](https://github.com/m2ux/prosiform/pull/556) was opened and linked to #460.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **The merge waited on I08:E05.** The pin `99bec9f7` sits after I08:E05's `a7069f30`, whose fixtures reached `main` with [#550](https://github.com/m2ux/prosiform/pull/550). `i09/e04/main` took `main` at `00f16692`, the branch took the base keeping the `99bec9f7` pin, and `make check` then passed.
- **AC18 agrees with the clause.** The clause states that a `group` pair places no contribution, so a selected preset governs a contribution through its `subst`. AC18 was reworded the same day to "a fixture whose composed section a selected preset's `subst` governs"; W09's work item still names a preset that "places" a composed section, which W09's planning reads against AC18.
- **No new code.** A composition cycle is refused under `E_UNSUPPORTED_CONSTRUCT` with its chain, as the operator refusals are. A code of its own needs the fixture schema, a fixture and the build at once, which W05 may add with its fixtures.
- **No new budget.** Materialised contributions count toward `output-bytes` as they are composed and each directive is a `depth` hop, so *Resource limits* keeps its eight names.
- **The operator marks.** `¬`, `⇉`, `⫽` and the guide's `↳` are excluded from the directive label set, so a lone mark stays an ordinary link and the guide's inline-target rule keeps its meaning. A deferred directive's contribution carries a generated `↳` line, so the guide already tells an agent how to activate it.
