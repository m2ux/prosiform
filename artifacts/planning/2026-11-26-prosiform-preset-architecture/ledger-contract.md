# Ledger Contract Coverage

Each feature pf 0.36.0 has, at revision `8cedda4cc06b0486168addc05f057161192a22a6`, mapped to the ledger field recording it or to the reason it stands outside the ledger. The clauses are [Build ledger](../2026-10-17-prosiform-v1/design.md#build-ledger) in the design contract; the accepted form is the [ledger specimen set](specimens/ledger/README.md). A row naming no field states what holds instead: the fact is bundle bytes the bundle's `sha256` covers, a refusal that writes no ledger, or an exclusion.

## Invocation

| Feature | Contract | Recorded as |
| --- | --- | --- |
| One entry reference: a plain path, a Markdown link, a Mermaid `click` line or a class diagram `link` line | Link entries | `invocation.entry`, as the caller wrote it, title and operator marks included |
| Operator marks on a link entry set aside | Link entries | `invocation.entry` keeps them as written; the bundles show their effect |
| The `--` separator before an entry opening with `-` | CLI contract | Outside: grammar; `invocation.entry` is the word after it |
| `--pick` | The agent's pick | `invocation.picks`; the alternative in force is `content.choices` |
| `--budget NAME=VALUE` and the eight defaults | Resource limits | `invocation.budgets`, every budget in force under its name, the defaults among them |
| `-o DIR` | CLI contract | Outside: the output folder is where the run's folder stands |
| `-c` | CLI contract | Outside: a check run's ledger is the ledger the publishing run writes, on standard output |
| `-d text\|json` | Exit status and JSON diagnostics | Outside: diagnostics |
| `-C`, `-v`, `-h` and a bare `pf` printing the guide | CLI contract, Guide | Outside: no build; `--ledger` beside them is invalid usage |
| Tool version and profile identifier | CLI contract | `build`: `tool`, `version`, `profile` |
| `PROSIFORM_FAULT` | Conformance faults | Outside: the conformance environment; a faulted run that still publishes writes the ledger of its build |

## Sources

| Feature | Contract | Recorded as |
| --- | --- | --- |
| Each distinct source captured once and hashed | Bundle before publishing, Source consistency | `sources`: `path`, `sha256` of the raw captured bytes, `use: "content"` where a bundle carries its bytes |
| A deferred target opened for its declaration and headings | Frontmatter policy, A deferred link's destination | `sources` row with `use: "metadata"` |
| A linked document that declares nothing, probed | A link naming a document that declares nothing | Outside: its frontmatter is read and no further byte, so it is not hashed |
| A substitution key the run redirected before reading | The substitution mapping | Outside: never opened |
| A resource or remote address | Resources are text | Outside: never opened |
| A leading BOM and frontmatter stripped from bundled content | Frontmatter policy | Inside `sources.sha256`, which hashes the raw bytes; `content.lines` counts frontmatter lines |
| The recheck before publication | Source consistency | `sources.sha256` is the captured hash the recheck confirmed; a changed source refuses the run, which writes no ledger |
| Budget consumption: files, bytes, targets, links, nesting and depth counted | Resource limits | Outside: the budgets in force are recorded, the figures counted are not; a crossed budget refuses the run |
| Encoding, suffix, symbolic-link and confinement refusals | Markdown and source-heading profile, No-symlink source policy | Refusal: no ledger |

## Selection And Arrangement

| Feature | Contract | Recorded as |
| --- | --- | --- |
| A whole-document selection | Input and output contract | `content` row whose `lines` span the body carried |
| A section selected by fragment | Input and output contract, Section extraction | `content.lines`, the first and last line of the region; a dispatched selection's fragment is in `bundles.document` |
| Recursive bundling and expanding coverage | Bundle before publishing | One `content` row for each region carried under one preset set and one group |
| Placement order | Input and output contract | The order of `content` rows |
| Structural ancestors, file headings, title case, destinations and ordinals | File-scoped hierarchy, Bundle destinations | Bundle bytes the bundle's `sha256` covers |
| Link rewriting, reference conversion, definition removal, command-block compaction | Source-local reference interpretation, Markdown profile | Bundle bytes the bundle's `sha256` covers |
| Self, ancestor and fragment-only references | Self-reference and ancestor-reference behavior | Resolved inside the bundle; no row |
| A `group` pair | Grouping | `content.group`: `name` and `depth`; absent where the document keeps its own file group |
| Merged sections, variants, member subsections and the overview | Grouping | Bundle bytes; each member region's `content.group` names the group |
| A document in several groups | Presets | One `content` row for each group it joins |
| Empty generated wrappers omitted | Grouping | Bundle bytes; the warning is outside |

## Presets

| Feature | Contract | Recorded as |
| --- | --- | --- |
| `default` in force beneath every selection | Presets | First entry of `content.presets` |
| Named presets selected by title tags | Presets | `bundles.selected`, in declaration order; `content.presets`, in layering order |
| One document under several selections in one bundle | Presets | One `content` row for each preset set it is carried under |
| A routing `subst` pair a reference used | The substitution mapping | `substitutions` row, `kind: "routing"`, with `declared` and `preset` |
| A routing pair no reference used | The substitution mapping | Outside: it shapes nothing; its warning stays on standard error |
| An alternative in force | Alternatives, Exactly one alternative | `content.choices`: `alternative`; absent where content none of the alternatives changes bundles with none in force |
| A stub in force | Stubs | `stubs`: `name`, `states`, `declared`; its used pairs are `substitutions` rows with `kind: "stand-in"` |
| A stub's pair no reference used | Stubs | Outside: its warning stays on standard error |
| `brief` | Dispatch briefs | `briefs`: `target`, `section`; the copy is a `content` row of the dispatching bundle |
| `level` | Dispatch models | `bundles.level` and `bundles.model` on the dispatched bundle; `dispatches.level` and `dispatches.model` |
| `levels` | Dispatch models | `levels`: `name`, `model`, `declared`, `preset` |
| A selected preset's value holding over `default`'s | Presets | The holding declaration is the origin; the held one is none |
| Two selected presets stating one level or one substitute | Selected presets union, Dispatch models | One row; the first origin in path and declaration order, each further one under `also` |
| A preset nothing selected | A preset nothing selected warns | Outside: warning |
| A deferral carrying the run's names | A deferral carries the run's names | `deferrals.carries` |
| Bundle selection identity | Bundle selection identity | `bundles.document` and `bundles.selected` |

## Links

| Feature | Contract | Recorded as |
| --- | --- | --- |
| An ordinary local Markdown link | Local Markdown document links | The target's `content` row; the rewritten link is bundle bytes |
| `⇉` dispatch | Dispatch links | `dispatches`: `target`, `source`, `title`, `level`, `model`, `bundle` |
| `⇉` carrying `?` | The agent's pick, Dispatch links | `dispatches.choices`: `alternative`, `states`, `bundle` for each alternative |
| `⫽` parallel dispatch | Parallel dispatch sub-sections | A `dispatches` row for each link; the dispatch-set sub-section is bundle bytes |
| Links from two sources dispatching one bundle | Dispatched bundles | Two `dispatches` rows naming one `bundle` |
| `¬` deferral, a deferring diagram link, `¬↳` deferred composition | The deferral mark, Deferred composition | `deferrals`: `target`, `source`, `carries`, `published` |
| A deferral carrying `?` | The pick token | `deferrals` row; `published` carries the title as the bundle publishes it, `?` and the run's names included |
| `↳` composition | Section composition | A `content` row for the composed copy under the directive's presets |
| A Mermaid `click` or class diagram `link` line | Link classification | The row of the link kind it states; its tooltip is `title` |
| `on <model>` after a dispatch line, `%% <node> on <model>` beneath a diagram dispatch | Dispatch models | `dispatches.model` |
| Dispatch depth and self-dispatch warnings | Exit status and JSON diagnostics | Outside: warnings |
| Dispatch and composition cycles | Dispatch cycles, Composition cycles | Refusal: no ledger |
| The `§ Instructions` heading and the run-pf line | The instruction heading, The run-pf line | Bundle bytes |
| A link to a web address or to a document that declares nothing | Link classification | Text the bundle carries; no row |

## Output

| Feature | Contract | Recorded as |
| --- | --- | --- |
| The entry's bundle and each dispatched bundle | Dispatched bundles | `bundles`: `file`, `sha256`, `role` |
| Automatic bundle names | Automatic output names | `bundles.file`; the run folder's name is outside, as its own location |
| The atomic swap of the run's folder | Validation and failure contract | The ledger and its digest join the swap: all three stand, or nothing is published |
| An earlier set that cannot be removed | Validation and failure contract | Outside: warning; the run is published with its ledger |
| Exit status | Exit status and JSON diagnostics | Outside: a ledger exists only for a build that publishes or checks |
| Delivery to the calling agent | Agent delivery contract | Outside: runtime evidence |

## Each Schema Field

Every property [ledger.schema.json](specimens/ledger/ledger.schema.json) states, with the build that writes it. A 0.36.0 form is one this contract revision states; the import and choice-group fields are admitted now and written once those features land.

| Field | Holds | Written from |
| --- | --- | --- |
| `schema` | `1` | Every ledger |
| `build.tool`, `build.version`, `build.profile` | `pf`, the version and the profile `-v` reports | Every ledger |
| `invocation.entry`, `invocation.picks`, `invocation.budgets` | The entry as written, each pick, every budget in force | Every ledger |
| `levels[].name`, `.model`, `.declared`, `.preset` | One level of the run's level map and its origin | 0.36.0 forms |
| `levels[].also[].declared`, `.preset` | A further declaration stating the same model | 0.36.0 forms |
| `levels[].imports[]`, `levels[].also[].imports[]`: `document`, `preset` | The importing documents and presets | Preset Imports |
| `stubs[].name`, `.states`, `.declared` | An entry stub in force | 0.36.0 forms |
| `sources[].path`, `.sha256`, `.use` | One opened source | Every ledger |
| `bundles[].file`, `.sha256`, `.role`, `.document`, `.selected` | One bundle | Every ledger |
| `bundles[].level`, `.model` | A dispatched bundle's level and model | 0.36.0 forms |
| `bundles[].content[].source`, `.lines`, `.presets` | One region carried | Every ledger |
| `bundles[].content[].group.name`, `.group.depth` | The named group of the region | 0.36.0 forms |
| `bundles[].content[].choices[].alternative` | The alternative in force | 0.36.0 forms |
| `bundles[].content[].choices[].group` | The alternative's choice group | Local Choice Groups |
| `bundles[].substitutions[].key`, `.substitute`, `.kind`, `.declared`, `.preset` | One used pair | 0.36.0 forms |
| `bundles[].substitutions[].also[].declared`, `.preset` | A further declaration of the same pair | 0.36.0 forms |
| `bundles[].substitutions[].imports[]`, `.also[].imports[]`: `document`, `preset` | The importing documents and presets | Preset Imports |
| `bundles[].briefs[].target`, `.section` | One carried brief | 0.36.0 forms |
| `bundles[].dispatches[].target`, `.source`, `.title`, `.level`, `.model`, `.bundle` | One dispatching link | 0.36.0 forms |
| `bundles[].dispatches[].choices[].alternative`, `.states`, `.bundle` | One alternative of a picking dispatch | 0.36.0 forms |
| `bundles[].dispatches[].choices[].group` | The alternative's choice group | Local Choice Groups |
| `bundles[].deferrals[].target`, `.source`, `.carries`, `.published` | One deferring link | 0.36.0 forms |

## Frozen Controls

The ledger's facts are held to two builds pf 0.36.0 produces, each rerun for this contract with the released command at the revision above; no agent was called.

| Build | Command | Ledger | Bundle hashes |
| --- | --- | --- | --- |
| The fixed-dispatch control | `pf -o bundles entry.md` in [valid-two-bindings](specimens/valid-two-bindings/) | [fixed.ledger.yaml](specimens/ledger/fixed.ledger.yaml) | Equal to [baseline.json](specimens/baseline.json) and to the rerun |
| The run | `pf -o bundles '[Run](entry.md "recorded")'` in [run](specimens/ledger/run/) | [ledger.yaml](specimens/ledger/run/bundles/entry-recorded.bundles/ledger.yaml) | Equal to the retained bundles and to the rerun |

- Each ledger validates against the schema, and each `sha256` equals the file it names.
- The fixed control's source and bundle hashes equal `baseline.json`.
- `sha256sum -c` passes the run's `ledger.yaml.sha256`.
- Each `use` matches the files the rerun opened: the run opens `recorded-review.md` and carries none of its bytes.
- Each list in both ledgers stands in the order the contract's **Order** clause gives: `worker.md` writes the link reaching `alpha.md` and `beta.md` before the one reaching `small.md`, so the run lists `beta.md` before `small.md`.
