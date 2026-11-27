# Preset Import Specimen Set

A preset reusing another source's levels and substitutions through the proposed `imports` field. The proposed sources are written in the form; the inline control beside them is real, and its bundles are the output the form must equal.

## What The Form Needs From Prosiform

- **An `imports` key in a preset.**  A list of mappings, each a `path` to a source and the `preset` of it to import.
- **Pure targets.**  An imported preset holds `levels`, `subst` and `imports` alone.
- **Origins kept.**  An imported key resolves from the folder of the source that declared it, and its substitute from the key's folder, as a `subst` pair does today.
- **No body, no default.**  The imported source contributes its named preset's settings and nothing else.
- **Refusals.**  A missing source or preset, an impure target, a cycle and a conflict each fail the build before anything is published.

## The Form

```yaml
prosiform:
  default:
    level: judgement
    imports:
      - path: shared/settings.md
        preset: strict
```

[proposed/shared/settings.md](proposed/shared/settings.md) states `strict` as `subst: [{rules.md: strict-rules.md}]`. The key names `shared/rules.md`, the rules beside the settings, wherever the importing document sits.

## Files

| File | Origin | Shows |
| --- | --- | --- |
| [proposed/entry.md](proposed/entry.md) | Proposed form | An entry importing its level map |
| [proposed/worker.md](proposed/worker.md) | Proposed form | A stage importing a substitution |
| [proposed/shared/settings.md](proposed/shared/settings.md) | Proposed form | The source both import from, holding two pure presets |
| [proposed/subject.md](proposed/subject.md), [shared/rules.md](proposed/shared/rules.md), [shared/strict-rules.md](proposed/shared/strict-rules.md) | Real | Plain declaring documents |
| [proposed/diagnostics-0.36.0.txt](proposed/diagnostics-0.36.0.txt) | Real | pf 0.36.0 refusing the proposed source as an unknown field |
| [proposed/diagnostics-proposed.txt](proposed/diagnostics-proposed.txt) | Hand-written | What the proposed form writes, and two open points |
| [proposed/ledger.toml](proposed/ledger.toml) | Hand-written | The ledger tracing each imported setting to its declaration |
| [inline/entry.md](inline/entry.md), [inline/worker.md](inline/worker.md) | Real | The same settings written in place, in syntax pf 0.36.0 accepts |
| [inline/subject.md](inline/subject.md), [shared/rules.md](inline/shared/rules.md), [shared/strict-rules.md](inline/shared/strict-rules.md) | Real | The inline control's plain documents |
| [inline/bundles/entry.bundles/entry.bundle.md](inline/bundles/entry.bundles/entry.bundle.md), [worker.bundle.md](inline/bundles/entry.bundles/worker.bundle.md) | Real | The bundles pf 0.36.0 wrote for the inline control, exit status 0, no diagnostics |
| [refusals/settings.md](refusals/settings.md) | Proposed form | The target the refusal specimens import, one preset of it impure |
| [refusals/missing-source.md](refusals/missing-source.md), [missing-preset.md](refusals/missing-preset.md), [impure-target.md](refusals/impure-target.md), [cycle-a.md](refusals/cycle-a.md), [cycle-b.md](refusals/cycle-b.md), [imported-conflict.md](refusals/imported-conflict.md), [local-conflict.md](refusals/local-conflict.md) | Proposed form | One source for each refusal |
| [refusals/diagnostics.txt](refusals/diagnostics.txt) | Hand-written | The diagnostic each refusal raises, and the open point on codes |

A hand-written file says so in its first line.

## What To Scrutinise

- **The output is the inline control's.**  The proposed build writes the two bundles under [inline/bundles](inline/bundles/entry.bundles/), byte for byte. An import moves where a setting is written and changes nothing a reader of the bundle sees.
- **The level map is imported by the entry.**  The entry alone supplies the run's level map today, and that holds: `models` reaches the run because the entry imports it.
- **The receiving preset keeps its role.**  The worker's `default` still states `level` itself. An imported preset stating `level` would be impure.
- **Nothing overrides.**  An import and its receiving preset stating one key differently is a refusal, not a precedence.
- **The ledger names both ends.**  Each imported setting records the preset that declared it and, under `imports`, the preset that imported it.

## Open Points

- **Budgets.**  Whether a source read only for an import counts toward `files`, `file-bytes` and `input-bytes`: both answers are in [diagnostics-proposed.txt](proposed/diagnostics-proposed.txt).
- **Unused imported pairs.**  Whether a pair no link names warns in each receiving document: both answers are in the same file.
- **Codes.**  Existing codes with one new one, or a code for each import refusal: both answers close [refusals/diagnostics.txt](refusals/diagnostics.txt).

## Checks Made On This Set

- The inline control was built with pf 0.36.0: exit status 0, standard error empty.
- The proposed source was put to pf 0.36.0 and its refusal retained.
- The ledger parses as TOML, validates against the [ledger schema](../ledger/ledger.schema.json), and each source hash equals the file it names.
