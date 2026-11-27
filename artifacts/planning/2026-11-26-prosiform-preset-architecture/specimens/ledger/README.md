# Ledger Specimen Set

What the proposed `--ledger` and `--sums` options write, shown for two builds pf 0.36.0 produces today. The ledgers are hand-written. The sources, bundles and diagnostics beside them are real, and so are the checksum file and what `sha256sum` reports for it.

## What The Form Needs From Prosiform

- **`--ledger`.**  One `ledger.yaml` written into the run's folder beside its bundles, in the same swap.
- **Check mode.**  `-c --ledger` writes the same ledger to standard output and publishes nothing.
- **`--sums`.**  One `SHA256SUMS` written into the run's folder in the same swap.
- **A schema.**  One JSON Schema the corpus holds every ledger to.
- **No new dependency and no new code.**  The ledger is written by `ruamel-yaml`, the library pf already reads frontmatter with, and neither option adds a diagnostic code.

## Two Files, Two Jobs

| File | Holds | Read by | Changes when |
| --- | --- | --- | --- |
| `ledger.yaml` | The effective configuration: what each bundle carries, the presets in force, where each setting was declared, each dispatch and deferral | An operator | A source's settings or the options change |
| `SHA256SUMS` | The hash of each file in the run's folder and of each source the run read | `sha256sum -c` | Any byte changes |

The ledger holds no hash and no file name. A bundle is named in it by its document and selected presets.

## The Ledger's Format

The ledger is YAML, the notation an author already writes presets in.

- **Each string is quoted.**  A preset named `off` or `no` is then a string to every reader, an older YAML 1.1 reader among them.
- **One layout.**  A list of scalars sits on one line, and a list of mappings is a block. Keys keep one fixed order.
- **The frontmatter's own rules.**  One YAML 1.2 Core mapping, with no alias, merge key, custom tag or duplicate key.
- **Plural list keys.**  A key holding a list of mappings is plural: `bundles`, `substitutions`, `dispatches`.

## The Checksum File

`SHA256SUMS` is in the format `sha256sum` writes: one line for each file, its hash and its path.

- **What it lists.**  Each other file in the run's folder, the ledger among them where one is written, then each source the run read.
- **Where paths start.**  A file of the folder is named alone. A source is written from the folder, as `../../worker.md`, which is how a deferred link is written today.
- **How it is checked.**  `sha256sum -c SHA256SUMS`, run in the folder. pf has no verifying mode.
- **What it does not catch.**  A file the folder holds that the checksums do not list.

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
| [ledger.schema.json](ledger.schema.json) | Hand-written | The schema both ledgers validate against |
| [run/bundles/entry-recorded.bundles/SHA256SUMS](run/bundles/entry-recorded.bundles/SHA256SUMS) | Real | The checksum file for the run, written with `sha256sum` |
| [checksums.txt](checksums.txt) | Real | What `sha256sum -c` reports for the set unchanged, with a source changed, a bundle changed and a source gone |
| [check-mode.txt](check-mode.txt) | Hand-written | What `-c --ledger` writes and where |
| [refusals.txt](refusals.txt) | Hand-written | A failing build and a failed publication |
| [run/entry.md](run/entry.md), [worker.md](run/worker.md), [component.md](run/component.md), [alpha.md](run/alpha.md), [beta.md](run/beta.md), [test.md](run/test.md), [small.md](run/small.md), [large.md](run/large.md), [review.md](run/review.md), [recorded-review.md](run/recorded-review.md) | Real | The run's sources, in syntax pf 0.36.0 accepts |
| [run/diagnostics.txt](run/diagnostics.txt) | Real | Standard error of the run, exit status 0 |
| [entry-recorded.bundle.md](run/bundles/entry-recorded.bundles/entry-recorded.bundle.md), [worker-alpha+small.bundle.md](run/bundles/entry-recorded.bundles/worker-alpha%2Bsmall.bundle.md), [worker-beta+small.bundle.md](run/bundles/entry-recorded.bundles/worker-beta%2Bsmall.bundle.md) | Real | The bundles pf 0.36.0 wrote for the run |

A hand-written file says so in its first line; the schema says so in its `$comment`. Each ledger's layout is the one `ruamel-yaml` writes.

## Each Feature And Its Field

A field under `bundles` is written here from one bundle's entry.

| What pf 0.36.0 does | Ledger field |
| --- | --- |
| Reports its version and profile | `build` |
| Takes one entry reference, picks and budgets | `invocation`: `entry`, `picks`, `budgets` |
| Writes an entry bundle and one for each dispatched selection | `bundles`: `role`, `document`, and `selected`, the names the reaching reference gave |
| Carries a source in a bundle | `content`: one row for each `source` the bundle carries |
| Puts `default` and named presets in force | `content.presets`, in layering order |
| Places a document under a layout group | `content.group`: `name` and `depth`; absent where the document keeps a group of its own |
| Redirects a link through a `subst` pair | `substitutions`: `key`, `substitute`, `kind` (`routing` or `stand-in`), and where it was declared: `declared` and `preset` |
| Puts an entry stub in force | `stubs`: `name`, `states`, `declared` |
| Picks an alternative | `content.choices`: the `alternative` in force |
| Carries a dispatch's brief | `briefs`: `target`, `section` |
| Dispatches a target to a bundle of its own | `dispatches`: `target`, the `source` writing the link and its `title` |
| Leaves a dispatch's pick to the dispatching agent | `dispatches.choices`: one entry for each alternative, with its choice line |
| Defers a link for a later run | `deferrals`: `target`, the `source` writing the link and the names it `carries` |
| Maps a level to a model | `levels`: `name`, `model` and where the map was declared; `level` and `model` on a dispatched bundle |

## What The Ledger Leaves Out

- **Hashes and file names.**  They are in `SHA256SUMS`. A bundle's file name follows from its document and selected presets by the released naming rule.
- **Which part of a source.**  A bundle's `content` names each source it carries, and not the lines or sections taken from it.
- **Line numbers.**  A setting's origin is its document and preset, which name it uniquely. A dispatch or deferral is named by its source, target and title.
- **Published links.**  A deferred link's written path depends on where the bundles go; the ledger names its target.
- **Warnings.**  They stay on standard error. What a warning points at is a field already: a stand-in is a substitution whose `kind` is `stand-in`.
- **Runtime facts.**  Effort, the provider and model a session really ran on, delivery, obedience and whether the work was done well.
- **The working directory and output folder.**  Paths are written from the first; the second is where the run's folder went.
- **Secrets and permissions.**  A preset holds none, so a ledger holds none.

## Checks Made On This Set

- Each ledger parses as YAML, reads back as the data it was written from, and validates against the schema.
- `SHA256SUMS` was written by `sha256sum` and checked by it: every file passes, and each changed or missing file is reported.
