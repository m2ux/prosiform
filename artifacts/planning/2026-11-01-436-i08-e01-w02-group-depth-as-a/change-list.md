# Change List

The plan changes the W02 delivery session applied and held.

## Applied

None. W02 linked [#510](https://github.com/m2ux/prosiform/pull/510) on [#436](https://github.com/m2ux/prosiform/issues/436) and ticked `AC12` and `AC13` once it merged, which records delivery rather than changing the plan; the draft review pull request [#508](https://github.com/m2ux/prosiform/pull/508) gained its Changes and its reference. The design's usage example was restated in the pair form on `engineering` and the README pin moved to it, which corrects the design rather than changing the plan.

## Held

None. Validation found no deferred debt, and no issue arose during delivery.

## Notes

- **Three trivial fixes made here.** Candidate coverage is held within each group, the design's usage example states the pair form, and the glossary's *grouping rule* names one `group-depth` entry.
- **The epic plan's governing-preset fixture is not this row's.** `b-w02.md` names `fixtures/inclusion/a-presets-pairs-reach-the-reference-it-governs`, which needs keyword selection; AC13 does not name it, so it rests with W04 and [I09:E02](https://github.com/m2ux/prosiform/issues/458). Until W04 lands, `default` is the preset whose pairs place a document.
- **A group named twice in one preset joins once.** The document is one member of that group, and two different depths raise `E_GROUP_DEPTH_CONFLICT`; W05 refuses the duplicate entry as invalid usage, exit `2`, per *Presets — Selected presets union*, and replaces this behaviour and its test.
- **Diagnostics name `prosiform.default`.** `E_GROUP_DEPTH_CONFLICT` names the `default` preset, the one in force; W04 names the selected preset once selection lands.
