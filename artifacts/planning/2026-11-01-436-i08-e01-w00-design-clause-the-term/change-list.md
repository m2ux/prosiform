# Change List

The plan changes the W00 delivery session applied and held.

## Applied

None. W00 linked [#507](https://github.com/m2ux/prosiform/pull/507) and ticked `AC11` on [#436](https://github.com/m2ux/prosiform/issues/436), which records delivery rather than changing the plan, and the draft review pull request [#508](https://github.com/m2ux/prosiform/pull/508) was opened and linked to #436.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **The unused-preset warning carries no code in the design.** The catalogue test holds every `W_` code the design names to the schema's warning catalogue, and conformance holds that catalogue to codes the build reports and a fixture declares, so W06 names `W_PRESET_UNUSED` in the design with the fixture and the build that reach it.
- **`-m` stays in the design.** Its retirement in favour of `path-sub` belongs to [I08:E06 Preset-Only Substitution](https://github.com/m2ux/prosiform/issues/461), so no issue was raised for it.
