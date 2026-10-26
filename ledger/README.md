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
| `run` | Optional. The identity of a run record the entry cites. |

A reader reproduces an entry by checking out each source at its revision, changing to `invocation.cwd` and running `invocation.command`, then comparing what it writes with `observed` and `expected`.

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
