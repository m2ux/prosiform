# Combined Specimen Set

The three proposed features in one run: an entry importing its level map, a stage whose grouped alternatives import their substitutions, and the ledger that build writes. Every file under `expected/` is hand-written.

## The Run

```text
pf --ledger -o bundles entry.md
```

- [entry.md](entry.md) imports `models` from [shared/settings.md](shared/settings.md) and dispatches the stage with `"alpha, small"`.
- [worker.md](worker.md) states a `component` group and a `test` group. Each alternative imports one substitution from the shared settings.
- [shared/settings.md](shared/settings.md) writes each key as `../component.md` or `../test.md`: a key resolves from the folder of the source declaring it, so the shared source names the slots beside the worker.

## Files

| File | Origin | Shows |
| --- | --- | --- |
| [entry.md](entry.md), [worker.md](worker.md), [shared/settings.md](shared/settings.md) | Proposed form | Imports and choice groups together |
| [component.md](component.md), [alpha.md](alpha.md), [beta.md](beta.md), [test.md](test.md), [small.md](small.md), [large.md](large.md) | Real | Plain declaring documents |
| [expected/entry.bundle.md](expected/entry.bundle.md), [worker-alpha+small.bundle.md](expected/worker-alpha%2Bsmall.bundle.md) | Hand-written | The bundles the run writes |
| [expected/ledger.yaml](expected/ledger.yaml) | Hand-written | The ledger the run writes |

A hand-written file says so in its first line. A hand-written bundle begins on line 3.

## What To Scrutinise

- **The bundles are the control's.**  From line 3 they equal the bundles pf 0.36.0 writes for [valid-two-bindings](../valid-two-bindings/), where every setting is written in place. The three features change what an author writes and what an operator can read, and leave what an agent reads as it is.
- **The ledger joins the three.**  Each substitution names the shared preset that declared it and the alternative that imported it; `choices` names each group and its member; `levels` names the imported map.
- **An alternative is a receiver, never a target.**  `alpha` imports settings and keeps its `choice`, with the group it names. A preset stating a `choice` cannot be imported.

## Design Points Settled At Scrutiny

| Point | Ruling | Shown in |
| --- | --- | --- |
| Does the ledger record the warnings a build raised? | No: the ledger records what was built. | [ledger.yaml](../ledger/run/bundles/entry-recorded.bundles/ledger.yaml) |
| Which code does a verification mismatch report? | `E_LEDGER_MISMATCH`, and `E_LEDGER_NOT_FOUND` for a folder with no ledger. | [verify.txt](../ledger/verify.txt) |
| Does a source read only for an import count toward the budgets? | Yes, as any source the run opens. | [diagnostics-proposed.txt](../imports/proposed/diagnostics-proposed.txt) |
| Does an imported pair no link names warn in each receiving document? | No: once, where no importer in the run names its key. | [diagnostics-proposed.txt](../imports/proposed/diagnostics-proposed.txt) |
| Do import refusals take new codes? | Existing codes, with `E_IMPORT_CYCLE` new. | [refusals/diagnostics.txt](../imports/refusals/diagnostics.txt) |
| What does the ledger record where two declarations state one value? | Every origin, the further ones under `also`. | [diagnostics-proposed.txt](../imports/proposed/diagnostics-proposed.txt) |
| What does a pick naming a member of a fixed group report? | Invalid usage, naming the fixed group. | [entry-picks.txt](../choice-groups/expected/entry-picks.txt), case 6 |
| Is the preset listing text or the ledger's notation? | Text. | [presets.txt](../choice-groups/expected/presets.txt) |
| Which notation is the ledger written in? | YAML, each string quoted, written by the library pf already ships. | [ledger.yaml](../ledger/run/bundles/entry-recorded.bundles/ledger.yaml) |
| Where do hashes and file names live? | In the ledger, which `--verify` holds a published set to. | [ledger.yaml](../ledger/run/bundles/entry-recorded.bundles/ledger.yaml), [verify.txt](../ledger/verify.txt) |
| Is the ledger itself held to a hash? | Yes: `ledger.yaml.sha256` holds the ledger's hash alone, and the ledger holds every other. | [ledger.yaml.sha256](../ledger/run/bundles/entry-recorded.bundles/ledger.yaml.sha256) |
| Does the schema number rise as features arrive? | No: schema 1 is whole from the ledger epic, and the later features write fields it already admits. | [ledger.schema.json](../ledger/ledger.schema.json) |
| Does the ledger record which part of a source a bundle carries? | Yes: `lines`, the first and last source line carried. | [ledger.yaml](../ledger/run/bundles/entry-recorded.bundles/ledger.yaml) |
| Does the ledger record the line a setting or link was written on? | No: a setting's origin is its document and preset. | [ledger README](../ledger/README.md#what-the-ledger-leaves-out) |
| Where is an alternative's group written? | In `choice`, as `group` beside `states`. An alternative with no group keeps the plain string. | [worker.md](worker.md) |

A bundle's name joins its effective preset names sorted by Unicode code point, as pf 0.36.0 names it, so `"small, alpha"` writes `worker-alpha+small.bundle.md` and two groups need no new naming rule.

## Behaviour pf 0.36.0 Has That The Forms Change

- **A title naming a component and no test is refused.**  It bundles today with the test slot unselected.
- **A deferred link may name an alternative beside the pick token.**  It is refused today; with groups it fixes one group and leaves the others to the later run's picks.
- **`--pick` is repeatable.**  It is given once today.
- **A check run writes to standard output.**  With the ledger option alone; a check run's standard output is empty today.

## Checks Made On This Set

- The expected bundles equal the retained control bundles from line 3.
- The ledger parses as YAML, validates against the [ledger schema](../ledger/ledger.schema.json), and each source hash equals the file it names.
