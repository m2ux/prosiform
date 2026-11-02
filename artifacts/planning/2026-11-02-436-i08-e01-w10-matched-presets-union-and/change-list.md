# Change List

The plan changes the W10 delivery session applied and held.

## Applied

None. W10's row links its pull request and `AC5` and `AC16` are ticked once it merges, which records delivery rather than changing the plan. The design's *Selected presets union* and *What a selection governs* clauses already state what this row delivers, so the design pin is unchanged.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **The work item `b-w10.md` predates the design's layering of `default`.** It refused `default` and a selected preset disagreeing; the design layers `default` beneath every selection, so only selected presets disagree, and the fixture `two-presets-disagreeing-are-refused` uses two keyword presets. The epic body, the design and this record are the record.
- **Three AC16 cases have no fixture the criterion names.** `two-presets-disagreeing-about-a-subst-key-are-refused`, `a-subst-key-naming-its-value-is-refused` and `a-group-named-twice-in-one-preset-is-refused` show them beside the three the criterion names.
