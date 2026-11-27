# Choice Group Specimen Set

One document stating a component axis and a test axis through the proposed `choice-group` field. The proposed sources are written in the form; every bundle, listing and refusal under `expected/` is hand-written.

## What The Form Needs From Prosiform

- **A `choice-group` key on an alternative.**  One string naming the local exclusive group the alternative belongs to.
- **One member for each group.**  Each group the bundled content depends on has exactly one alternative in force.
- **One open group at a dispatch.**  A pick token leaves one group to the dispatching agent while the others are named.
- **A repeatable `--pick`.**  At the entry, one occurrence for each group the title leaves open.
- **`--presets DOC`.**  A listing of one document's presets, its alternatives by group and its stubs, publishing nothing.

## The Form

```yaml
prosiform:
  alpha:
    choice: The requested component is alpha.
    choice-group: component
    subst:
      - component.md: alpha.md
  small:
    choice: The test is small.
    choice-group: test
    subst:
      - test.md: small.md
```

An alternative stating no `choice-group` belongs to its document's one unnamed group, which is every alternative a document declares under pf 0.36.0.

## Files

| File | Origin | Shows |
| --- | --- | --- |
| [proposed/worker.md](proposed/worker.md) | Proposed form | A stage stating two groups of two alternatives |
| [proposed/direct.md](proposed/direct.md) | Proposed form | The same groups on a document stating no level, so it can be entered directly |
| [proposed/entry.md](proposed/entry.md) | Real | The entry dispatching the stage with `"alpha, small"` |
| [proposed/component.md](proposed/component.md), [alpha.md](proposed/alpha.md), [beta.md](proposed/beta.md), [test.md](proposed/test.md), [small.md](proposed/small.md), [large.md](proposed/large.md) | Real | Plain declaring documents |
| [proposed/diagnostics-0.36.0.txt](proposed/diagnostics-0.36.0.txt) | Real | pf 0.36.0 on the proposed source, and on the same source with the field removed |
| [expected/explicit/entry.bundle.md](expected/explicit/entry.bundle.md), [worker-alpha+small.bundle.md](expected/explicit/worker-alpha%2Bsmall.bundle.md) | Hand-written | The bundles for `"alpha, small"` |
| [expected/open-pick/entry.bundle.md](expected/open-pick/entry.bundle.md) | Hand-written | The entry bundle for `"alpha, ?"`: the component fixed, the test left to the pick |
| [expected/entry-picks.txt](expected/entry-picks.txt) | Hand-written | The repeatable `--pick` at the entry, and a deferred link |
| [expected/refusals.txt](expected/refusals.txt) | Hand-written | Each refusal at a dispatch |
| [expected/presets.txt](expected/presets.txt) | Hand-written | The `--presets` listing |
| [expected/ledger.yaml](expected/ledger.yaml) | Hand-written | The ledger naming each group and the alternative chosen in it |

A hand-written file says so in its first line. A hand-written bundle begins on line 3.

## What pf 0.36.0 Does Today

- **A second axis as ordinary presets.**  The control [valid-two-bindings](../valid-two-bindings/) states `small` and `large` as ordinary presets and bundles `"alpha, small"`. The explicit bundles here equal that control's from line 3, byte for byte.
- **No required test.**  The control [missing-test-axis](../missing-test-axis/) bundles `"alpha"` with exit status 0, the test slot unselected.
- **Four alternatives are one set.**  With the field removed, `"alpha, small"` is refused as two alternatives in force, as [diagnostics-0.36.0.txt](proposed/diagnostics-0.36.0.txt) records.
- **Names sort by code point.**  A bundle's name joins its effective preset names sorted by Unicode code point, whatever order a title or the document gives them, so `"small, alpha"` writes `worker-alpha+small.bundle.md`. Two groups need no new naming rule.
- **A deferred link names one alternative or the pick token alone.**  `[¬ Check](direct.md "alpha, ?")` is refused today with `E_UNSUPPORTED_CONSTRUCT`.

## What To Scrutinise

- **The changed behaviour.**  A title naming a component and no test is refused, where pf 0.36.0 bundles it. [refusals.txt](expected/refusals.txt) case 2.
- **One open group at a dispatch.**  `"alpha, ?"` publishes one line for each test, each naming its own bundle. `"?"` alone is refused with a remedy for each group. [refusals.txt](expected/refusals.txt) case 4.
- **Several picks at the entry.**  `--pick alpha --pick small` names one member of each group. [entry-picks.txt](expected/entry-picks.txt).
- **A deferral may leave any group open.**  The run that bundles a deferred link is an entry, so it names one pick for each. [entry-picks.txt](expected/entry-picks.txt), case 7.
- **No new code.**  Every refusal reports `E_ALTERNATIVE_UNRESOLVED`, naming the group.
- **The listing's layout.**  [presets.txt](expected/presets.txt).

## Settled At Scrutiny

- **A pick naming a member of a fixed group.**  Invalid usage, naming the group the title fixes and the group left open.
- **The listing's format.**  Text.

## Checks Made On This Set

- The proposed source was put to pf 0.36.0, with and without the field, and each result retained.
- The explicit expected bundles equal the retained control bundles from line 3.
- The ledger parses as YAML and validates against the [ledger schema](../ledger/ledger.schema.json).
