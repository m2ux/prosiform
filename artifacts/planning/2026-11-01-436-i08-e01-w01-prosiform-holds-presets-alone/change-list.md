# Change List

The plan changes the W01 delivery session applied and held.

## Applied

None. W01 linked [#509](https://github.com/m2ux/prosiform/pull/509) on [#436](https://github.com/m2ux/prosiform/issues/436) and ticked `AC1` once it merged, which records delivery rather than changing the plan; the draft review pull request [#508](https://github.com/m2ux/prosiform/pull/508) gained its Changes and its reference.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **`groups.svg` had drifted from the build.** A trivial fix, made here: the drawing is regenerated with the two others the nesting changed.
- **`exclude` and `path-sub` are admitted as lists alone.** Their entry shapes are W03's, and `path-sub` takes effect under [I08:E06](https://github.com/m2ux/prosiform/issues/461); until then a preset holding either states nothing a run reads.
- **The unused-preset warning meets this row's fixture.** `fixtures/inclusion/a-preset-key-holds-a-mapping` declares a `Target` preset no reference selects, so W06's warning will reach it; W06 settles that fixture's expected diagnostic with the code it introduces.
