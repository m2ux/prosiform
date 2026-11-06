# CLI Preset Option

## Confirmed Contract

The CLI option carrying a link's comma-separated preset names is `--presets` (user-confirmed, 2026-11-06).

```sh
pf --entry guide.md#plan-report --presets checks,draft
```

The option accepts one comma-separated list. Omitting it selects `default` alone. Authored Markdown links retain their title syntax, such as `[Plan Report](guide.md#plan-report "checks,draft")`. The selection, default layering, unknown-name handling and bundle-variant rules remain the contracts in [the design](design.md).

## Implementation Contract

The CLI grammar, guide text, help, invocation examples and observing fixtures use `--presets`. The joined CLI/caller/fixture unit adopts the amended E07 design revision when it updates the README's immutable design pin.

The task identities, dependencies, joins, lanes, priorities and acceptance-criterion identities retain their existing values. The shared list reader still interprets the preset names supplied by source titles and the CLI.

## Design Reference

The current implementation revision is [795bbfb67c66b02193f0313138f59f18aa6c5274](https://github.com/m2ux/prosiform/blob/795bbfb67c66b02193f0313138f59f18aa6c5274/artifacts/planning/2026-10-17-prosiform-v1/design.md). Its guide explains the attached `=` form for values beginning with `-`; the CLI/caller/fixture unit adopts this immutable revision. [Guide option values](guide-option-values.md) records that clarification.

[The epic design](https://github.com/m2ux/prosiform/blob/i10/e07/engineering/artifacts/planning/2026-10-17-prosiform-v1/design.md) carries the command grammar. [Amendment verification](https://github.com/m2ux/prosiform/blob/engineering/artifacts/planning/2026-11-06-i10-link-tag-presets/cli-preset-option.json) records its immutable revision and tracker readback.
