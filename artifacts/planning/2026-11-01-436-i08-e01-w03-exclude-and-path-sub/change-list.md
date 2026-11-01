# Change List

The plan changes the W03 delivery session applied and held.

## Applied

- **AC14 cites this row's fixtures.** On [#436](https://github.com/m2ux/prosiform/issues/436), AC14 named `fixtures/exclusion/a-level-tells-a-repeated-heading-apart`, which needs the carve [I08:E02](https://github.com/m2ux/prosiform/issues/445) delivers and which E02's AC6 already owns. AC14 now states the shape and its refusals, cites `fixtures/inclusion/an-exclude-list-holds-names-and-levels` and `fixtures/inclusion/a-malformed-exclude-entry-is-refused`, and points the level's effect at E02 AC6.
- **AC15 cites the side fixture.** AC15 also names `fixtures/inclusion/a-path-sub-side-is-read-by-the-reference-grammar`, the fixture that shows a side read by the reference grammar; the pair-string fixture shows only the entry's form.

W03's row links [#511](https://github.com/m2ux/prosiform/pull/511), which records delivery rather than changing the plan.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **E02's malformed-exclusion refusals exist.** E02 AC11's empty name, out-of-range level and two-key mapping are refused here; E02:W01 adds its fixture `fixtures/exclusion/a-malformed-exclusion-is-refused` against behaviour already on the base.
- **`path-sub` sides are read at capture.** `metadata` sits beneath `closure` in the import graph, so `cli.path_subs` reads each side through `closure.resolve` after decoding. E06 resolves the sides from the declaring file and makes them take effect.
- **The epic record's narrative keeps the old AC14 wording.** `epic-b-section-presets.md` and `b-w03.md` in the epic record are left as planned; the epic body is the record.
