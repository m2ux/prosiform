# Change List

The plan changes the W00 delivery session applied and held.

## Applied

None. W00 linked [#520](https://github.com/m2ux/prosiform/pull/520) and ticked `AC7` on [#449](https://github.com/m2ux/prosiform/issues/449), which records delivery rather than changing the plan, and the draft review pull request [#521](https://github.com/m2ux/prosiform/pull/521) was opened and linked to #449.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **The pin moved in this row.** The work item in the epic record said I08:E00:W00 would move the pin; I08:E00 and I08:E01 had already merged, so the brief assigned the move to this row.
- **Two fixtures lost a citation, not their place.** `extraction/a-fragment-alone-selects-from-the-referrer` and `usage-example/a-bare-fragment-and-its-referring-document` cited the withdrawn `CLI contract — -f DOC` row, which would fail `make conformance` at the new pin. Only that citation was removed; W03 withdraws or rewrites the fixtures.
