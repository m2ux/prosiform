# Ledger Specimen Set

What the proposed `--ledger` option writes, shown for two builds pf 0.36.0 produces today. The ledgers are hand-written; the sources, bundles and diagnostics beside them are real.

## What The Form Needs From Prosiform

- **`--ledger`.**  One `ledger.yaml` written into the run's folder beside its bundles, in the same swap.
- **Check mode.**  `-c --ledger` writes the same ledger to standard output and publishes nothing.
- **A digest of the ledger.**  `ledger.yaml.sha256`, written with the ledger: one line in the format `sha256sum` writes, holding the ledger's hash and no other. It reports a ledger changed by accident; a caller guarding against deliberate change keeps the line somewhere else.
- **`--verify FOLDER`.**  Holds the ledger to its digest, then re-hashes each source and bundle the ledger names, and reports each that differs.
- **A schema.**  One JSON Schema the corpus holds every ledger to.
- **No new dependency.**  The ledger is written by `ruamel-yaml`, the library pf already reads frontmatter with.

## The Format

The ledger is YAML, the notation an author already writes presets in.

- **Each string is quoted.**  A preset named `off` or `no` is then a string to every reader, an older YAML 1.1 reader among them.
- **One layout.**  A list of scalars sits on one line, and a list of mappings is a block. Keys keep one fixed order.
- **The frontmatter's own rules.**  One YAML 1.2 Core mapping, with no alias, merge key, custom tag or duplicate key.
- **Plural list keys.**  A key holding a list of mappings is plural: `sources`, `bundles`, `substitutions`.

## The Two Builds

| Build | Command | Shows |
| --- | --- | --- |
| [The fixed-dispatch control](../valid-two-bindings/) | `pf -o bundles entry.md` | An entry level map, one dispatch naming both presets, two routing substitutions |
| [The run](run/) | `pf -o bundles '[Run](entry.md "recorded")'` | An entry stub in force, a dispatch leaving its pick open, a deferral carrying the run's names |

## Files

| File | Origin | Shows |
| --- | --- | --- |
| [fixed.ledger.yaml](fixed.ledger.yaml) | Hand-written | The ledger for the fixed-dispatch control |
| [run/bundles/entry-recorded.bundles/ledger.yaml](run/bundles/entry-recorded.bundles/ledger.yaml) | Hand-written | The ledger for the run, where the option would write it |
| [run/bundles/entry-recorded.bundles/ledger.yaml.sha256](run/bundles/entry-recorded.bundles/ledger.yaml.sha256) | Real | The digest `sha256sum` wrote for the specimen ledger beside it |
| [ledger.schema.json](ledger.schema.json) | Hand-written | The schema both ledgers validate against |
| [check-mode.txt](check-mode.txt) | Hand-written | What `-c --ledger` writes and where |
| [verify.txt](verify.txt) | Hand-written | Each outcome of `--verify` |
| [refusals.txt](refusals.txt) | Hand-written | A failing build, a failed publication and invalid usage |
| [run/entry.md](run/entry.md), [worker.md](run/worker.md), [component.md](run/component.md), [alpha.md](run/alpha.md), [beta.md](run/beta.md), [test.md](run/test.md), [small.md](run/small.md), [large.md](run/large.md), [review.md](run/review.md), [recorded-review.md](run/recorded-review.md) | Real | The run's sources, in syntax pf 0.36.0 accepts |
| [run/diagnostics.txt](run/diagnostics.txt) | Real | Standard error of the run, exit status 0 |
| [entry-recorded.bundle.md](run/bundles/entry-recorded.bundles/entry-recorded.bundle.md), [worker-alpha+small.bundle.md](run/bundles/entry-recorded.bundles/worker-alpha%2Bsmall.bundle.md), [worker-beta+small.bundle.md](run/bundles/entry-recorded.bundles/worker-beta%2Bsmall.bundle.md) | Real | The bundles pf 0.36.0 wrote for the run |

A hand-written file says so in its first line; the schema says so in its `$comment`. Every hash in a ledger is the SHA-256 of the real file beside it. Each ledger's layout is the one `ruamel-yaml` writes.

## Each Feature And Its Field

A field under `bundles` is written here from one bundle's entry. A `line` is the line the setting's key is written on.

| What pf 0.36.0 does | Ledger field |
| --- | --- |
| Reports its version and profile | `build` |
| Takes one entry reference, picks and budgets | `invocation`: `entry`, `picks`, `budgets` |
| Opens each source once and hashes it | `sources`: `path`, `sha256`, and `use` (`content` where a bundle carries its bytes, `metadata` where the run read it and no bundle carries its bytes) |
| Selects a region of a source for a bundle | `content`: `source` and `lines`, the first and last source line carried |
| Puts `default` and named presets in force | `content.presets`, in layering order; `selected`, the names the reaching reference gave |
| Places a document under a layout group | `content.group`: `name` and `depth`; absent where the document keeps a group of its own |
| Redirects a link through a `subst` pair | `substitutions`: `key`, `substitute`, `kind` (`routing` or `stand-in`), and where it was declared: `declared`, `preset`, `line` |
| Puts an entry stub in force | `stubs`: `name`, `states`, `declared`, `line` |
| Picks an alternative | `content.choices`: the `alternative` in force and the `line` its `choice` is written on |
| Carries a dispatch's brief | `briefs`: `target`, `section`, `line` |
| Dispatches a target to a bundle of its own | `dispatches`: `target`, the `source` and `line` writing the link, its `title`, and the `bundle` written for it |
| Leaves a dispatch's pick to the dispatching agent | `dispatches.choices`: one entry for each alternative, with its choice line and bundle |
| Defers a link for a later run | `deferrals`: `target`, the `source` and `line` writing the link, the names it `carries`, and the link as `published` |
| Maps a level to a model | `levels`: `name`, `model` and where the map was declared; `level` and `model` on a dispatched bundle |
| Writes each bundle | `file` and `sha256` |

## What The Ledger Leaves Out

- **Runtime facts.**  Effort, the provider and model a session really ran on, delivery, obedience and whether the work was done well.
- **The working directory.**  Paths are written from it; the directory itself is the caller's.
- **The output folder.**  `-o` names where the run's folder went, which the folder's own location already says.
- **Its own bytes.**  The ledger records no hash of itself. `ledger.yaml.sha256` beside it holds that one hash, and the ledger holds every other.
- **Warnings.**  They stay on standard error. What a warning points at is a field already: a stand-in is a substitution whose `kind` is `stand-in`.
- **Secrets and permissions.**  A preset holds none, so a ledger holds none.

## A Row For Each Link

Each authored dispatch and deferral link has a row naming the source and line that wrote it, so two links reaching one bundle are two rows. The ledger's projection therefore needs each link's coordinates, where the bundler's own record of a dispatched bundle keeps one.

## Checks Made On This Set

- Each ledger parses as YAML, reads back as the data it was written from, and validates against the schema.
- Each `sha256` equals the hash of the real file it names.
- `ledger.yaml.sha256` was written by `sha256sum` over the specimen ledger, and `sha256sum -c` passes it.
- The `use` of each source matches the files pf 0.36.0 opened, read from a system-call trace of both builds.
