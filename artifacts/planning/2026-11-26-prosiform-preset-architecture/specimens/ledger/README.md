# Ledger Specimen Set

What the proposed `--ledger` option writes, shown for two builds pf 0.36.0 produces today. The ledgers are hand-written; the sources, bundles and diagnostics beside them are real.

## What The Form Needs From Prosiform

- **`--ledger`.**  One `ledger.toml` written into the run's folder beside its bundles, in the same swap.
- **Check mode.**  `-c --ledger` writes the same ledger to standard output and publishes nothing.
- **`--verify FOLDER`.**  Re-hashes each source and bundle a published ledger names, and reports each that differs.
- **A schema.**  One JSON Schema the corpus holds every ledger to.
- **A TOML writer.**  The `tomli-w` library; neither existing dependency writes TOML.

## The Two Builds

| Build | Command | Shows |
| --- | --- | --- |
| [The fixed-dispatch control](../valid-two-bindings/) | `pf -o bundles entry.md` | An entry level map, one dispatch naming both presets, two routing substitutions |
| [The run](run/) | `pf -o bundles '[Run](entry.md "recorded")'` | An entry stub in force, a dispatch leaving its pick open, a deferral carrying the run's names |

## Files

| File | Origin | Shows |
| --- | --- | --- |
| [fixed.ledger.toml](fixed.ledger.toml) | Hand-written | The ledger for the fixed-dispatch control |
| [run/bundles/entry-recorded.bundles/ledger.toml](run/bundles/entry-recorded.bundles/ledger.toml) | Hand-written | The ledger for the run, where the option would write it |
| [ledger.schema.json](ledger.schema.json) | Hand-written | The schema both ledgers validate against |
| [check-mode.txt](check-mode.txt) | Hand-written | What `-c --ledger` writes and where |
| [verify.txt](verify.txt) | Hand-written | Each outcome of `--verify` |
| [refusals.txt](refusals.txt) | Hand-written | A failing build, a failed publication and invalid usage |
| [run/entry.md](run/entry.md), [worker.md](run/worker.md), [component.md](run/component.md), [alpha.md](run/alpha.md), [beta.md](run/beta.md), [test.md](run/test.md), [small.md](run/small.md), [large.md](run/large.md), [review.md](run/review.md), [recorded-review.md](run/recorded-review.md) | Real | The run's sources, in syntax pf 0.36.0 accepts |
| [run/diagnostics.txt](run/diagnostics.txt) | Real | Standard error of the run, exit status 0 |
| [entry-recorded.bundle.md](run/bundles/entry-recorded.bundles/entry-recorded.bundle.md), [worker-alpha+small.bundle.md](run/bundles/entry-recorded.bundles/worker-alpha%2Bsmall.bundle.md), [worker-beta+small.bundle.md](run/bundles/entry-recorded.bundles/worker-beta%2Bsmall.bundle.md) | Real | The bundles pf 0.36.0 wrote for the run |

A hand-written file says so in its first line; the schema says so in its `$comment`. Every hash in a ledger is the SHA-256 of the real file beside it.

## Each Feature And Its Field

| What pf 0.36.0 does | Ledger field |
| --- | --- |
| Reports its version and profile | `build` |
| Takes one entry reference, picks and budgets | `invocation.entry`, `invocation.picks`, `invocation.budgets` |
| Opens each source once and hashes it | `source`: `path`, `sha256`, and `use` (`content` where a bundle carries its bytes, `metadata` where the run read it and no bundle carries its bytes) |
| Selects a region of a source for a bundle | `bundle.content`: `source` and `lines`, the first and last source line carried |
| Puts `default` and named presets in force | `bundle.content.presets`, in layering order; `bundle.selected`, the names the reaching reference gave |
| Places a document under a layout group | `bundle.content.group`: `name` and `depth`; absent where the document keeps a group of its own |
| Redirects a link through a `subst` pair | `bundle.substitution`: `key`, `substitute`, `kind` (`routing` or `stand-in`), and where it was declared: `declared`, `preset`, `line` |
| Puts an entry stub in force | `stub`: `name`, `states`, `declared`, `line` |
| Picks an alternative | `bundle.content.choices`: the `alternative` in force |
| Carries a dispatch's brief | `bundle.brief`: `target`, `section`, `line` |
| Dispatches a target to a bundle of its own | `bundle.dispatch`: `target`, the `source` and `line` writing the link, its `title`, and the `bundle` written for it |
| Leaves a dispatch's pick to the dispatching agent | `bundle.dispatch.choice`: one entry for each alternative, with its choice line and bundle |
| Defers a link for a later run | `bundle.deferral`: `target`, the `source` and `line` writing the link, the names it `carries`, and the link as `published` |
| Maps a level to a model | `level`: `name`, `model` and where the map was declared; `bundle.level` and `bundle.model` on a dispatched bundle |
| Writes each bundle | `bundle.file` and `bundle.sha256` |

## What The Ledger Leaves Out

- **Runtime facts.**  Effort, the provider and model a session really ran on, delivery, obedience and whether the work was done well.
- **The working directory.**  Paths are written from it; the directory itself is the caller's.
- **The output folder.**  `-o` names where the run's folder went, which the folder's own location already says.
- **Its own bytes.**  The ledger records no hash of itself.
- **Warnings.**  They stay on standard error. What a warning points at is a field already: a stand-in is a substitution of `kind = "stand-in"`.
- **Secrets and permissions.**  A preset holds none, so a ledger holds none.

## Checks Made On This Set

- Each ledger parses as TOML and validates against the schema.
- Each `sha256` equals the hash of the real file it names.
- The `use` of each source matches the files pf 0.36.0 opened, read from a system-call trace of both builds.

## The Same Ledger In Each Format

The run's ledger is written three ways, each reading back to the same data.

| File | Laid out by | Shows |
| --- | --- | --- |
| [run/bundles/entry-recorded.bundles/ledger.toml](run/bundles/entry-recorded.bundles/ledger.toml) | Hand | TOML with nested tables indented and short lists on one line |
| [format/ledger.tomli-w.toml](format/ledger.tomli-w.toml) | The `tomli-w` library | TOML as the library the plan names writes it: no indentation, one list item to a line |
| [format/ledger.yaml](format/ledger.yaml) | The `ruamel-yaml` library | YAML as the dependency pf already ships writes it, each string quoted |

## A Row For Each Link

Each authored dispatch and deferral link has a row naming the source and line that wrote it, so two links reaching one bundle are two rows. The ledger's projection therefore needs each link's coordinates, where the bundler's own record of a dispatched bundle keeps one.
