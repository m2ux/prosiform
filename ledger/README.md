# Ledger

What use of prosiform reveals, recorded so a later reader reproduces it without the session that met it, and the set of sources that must be bundled before a freeze.

The ledger sits on `main` beside [`checks/ledger.py`](../checks/ledger.py), which `make ledger` runs, so one revision carries both the entries and the check that reads them.

## An entry

An entry is one TOML file under `entries/`, named `<yyyy-mm-dd>-<slug>.toml` for the day the result was met and a short name of it. It is validated against [`entry.schema.json`](entry.schema.json).

```toml
date = "2026-10-26"
observed = "The bundle omits the protocol the publish step links."
expected = "The bundle carries that protocol beneath its step."

[invocation]
command = "pf modes/plan-mode.md"
cwd = "example/work-planner"

[[sources]]
repository = "m2ux/prosiform"
revision = "6554db86..."  # the full forty-character commit id
path = "example/work-planner"

[triage]
state = "build defect"
reason = "The link resolves in the source tree, so the bundle should reach it."
```

| Field | Holds |
| --- | --- |
| `date` | The day the result was observed, a quoted `YYYY-MM-DD` string. |
| `invocation.command` | The `pf` command line exactly as run. |
| `invocation.cwd` | The working directory, relative to the checkout of the first source; `.` is its root. |
| `sources` | Each source the run bundled: its repository as `owner/name`, the full commit id it was read at, and the path the run read. |
| `observed` | The result the run produced. |
| `expected` | The result the reader expected. |
| `triage.state` | One of the triage states below. |
| `triage.reason` | Why the entry takes that state. A blank reason is refused. |
| `run` | Optional. The identity of a run record under `runs/` this entry cites, which is the record's file name without the extension. |

A reader reproduces an entry by checking out each source at its revision, changing to `invocation.cwd` and running `invocation.command`, then comparing what it writes with `observed` and `expected`.

## A run record

A run record is one TOML file under `runs/`, named `<yyyy-mm-dd>-<slug>.toml` for the day the run was taken and a short name of it. It is validated against [`run.schema.json`](run.schema.json). Its identity is that name without the extension, which is what an entry's optional `run` carries.

A run is recorded whether or not it surprised its operator: a ledger holding only surprises says nothing about whether the tool was used, and the exposure set below is counted against these records.

```toml
date = "2026-10-28"
outcome = "published"
acted_from_bundle = true

[sizes]
bundle = 187488
whole = 239331

[[example]]
cwd = "example/work-planner"
command = "pf modes/plan-mode.md"
```

| Field | Holds |
| --- | --- |
| `date` | The day the run was taken, a quoted `YYYY-MM-DD` string. |
| `outcome` | `published` when the run wrote its bundles and `failed` when it wrote none. |
| `sizes.bundle` | The bytes of the bundle the run published; zero when it published none. |
| `sizes.whole` | The total bytes of the sources the run bundled, each read whole. |
| `acted_from_bundle` | Whether the entry reference's content was acted on from the bundle alone. A failed run published no bundle, so it is `false` there. |
| `example` | Each worked-example mode entry the run bundled, as the exposure set names it. |
| `workspace` | Each workspace skill the run bundled, as the exposure set names it. |

The `example` and `workspace` lists take the shapes the exposure set declares, so one source has one spelling across the two documents and a declared source is counted as bundled when a run names it. At least one of the two is present, because a run that bundled nothing is no bundling run.

## Triage states

| State | Answered in |
| --- | --- |
| `design change` | The contract: the design states behaviour use shows to be wrong. |
| `corpus gap` | The fixture corpus: the behaviour is right and no fixture binds it. |
| `build defect` | The build: it departs from the contract. |
| `no change` | Nowhere: the behaviour is intended, and the reason says why. |

## Exposure set

[`exposure.toml`](exposure.toml) declares the sources that must be bundled before a freeze, validated against [`exposure.schema.json`](exposure.schema.json). It has two halves, and each must name at least one source.

- `example`: each mode entry of the [worked example](../example/README.md), as its documented `pf` command and working directory. Every file under `example/work-planner/modes/` must be named, and every named entry must exist.
- `workspace`: each workspace skill agents invoke, by repository, branch and path. The skills live in that repository and are not copied here.

The set is a target the stage works toward, so a source no run has bundled yet is not a failure. `make ledger` counts the declared sources the run records name and reports the figure, so exposure is read off the records rather than assumed from the declaration.
