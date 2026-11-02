# MVP Review Against the Pinned Design

> Review record · I09:E05 W01 · Created 2026-11-02

Everything merged into `main` since `contract/v0.15.0`, read against the design the README pins.

## Scope

- **Build.** `main` at [74b00cd9](https://github.com/m2ux/prosiform/tree/74b00cd9), carrying I08 (E00, E01, E03, E04, E05, E06, E08) and I09 (E02, E04).
- **Design.** [4958ad38](https://github.com/m2ux/prosiform/blob/4958ad38bc2bb6a0786f93aa6de30a7b6a2e27c9/artifacts/planning/2026-10-17-prosiform-v1/design.md), the README's pin, against [21f4687d](https://github.com/m2ux/prosiform/blob/21f4687d58cf26a89328e3abddd7929a9b5905c0/artifacts/planning/2026-10-17-prosiform-v1/design.md), the design `contract/v0.15.0` pinned.
- **Clauses.** A clause is what `checks/conformance.py` names one: a heading, a bold-led bullet, a numbered step or a table row. 166 clauses changed or were added between the two revisions, and 32 were retired.

## Method

- **Clause diff.** Each clause's text at both revisions, compared; the changed and added clauses are the rows below, the retired ones the second table.
- **Corpus.** `make check` at 74b00cd9 with `PROSIFORM_BUILD` set passes: 498 of 498 fixtures, 1161 build tests, 1663 check tests. Each row cites the fixtures whose manifests name the clause.
- **Code.** Each row cites the module and functions under `src/prosiform/` implementing the clause.
- **Probes.** Clauses no fixture names, and the places the epics meet, were run against the build in scratch trees: presets with `subst` and `group` across two references and across dispatched bundles, a deferred directive inside a dispatched bundle, nested groups with title-cased slugs, the overview arrangement, the run folder's publication cases, the budget and fault refusals, and the automatic names.
- **Prior reviews.** The integration reviews of [#541](../agent-review-541.json) and [#556](../agent-review-556.json) are evidence for E02 and E04; their findings are resolved on `main`.

## Findings

Three departures, each a row of [I09:E05](https://github.com/m2ux/prosiform/issues/523). The build is right in each, so each row brings the design to it.

### F1. The output folder is made

- **Clause.** *CLI contract — `-o DIR`*: "The folder must exist." *Validation and failure contract — Publication*: the run holds "the output folder to existing" before writing.
- **Build.** `cli.py` `publish_folder` makes a missing output folder and refuses only one it cannot make (commit 1dafc779, after `contract/v0.15.0`). `pf -h` says "made if absent" and the guide "The run makes it if it is not there". `pf -o nothere a.md` publishes `nothere/a.bundles/a.bundle.md`, exit 0.
- **Row.** W30: the design states the folder made where absent, since an agent following the guide is spared a failed run and a `mkdir`.

### F2. `subst` pairs combine across references

- **Clause.** *Presets — One document under several selections*: "each reference bundles that document's content under the selection it made."
- **Build.** `cli.py` `governing` builds one `subst` table per document from every reference reaching it, and refuses two references whose presets map one key to two alternatives (I08:E06 W01's decision). A section one reference bundles under `default` alone has its links redirected by a pair another reference's `checks` preset states: with `## Plain` linking `rules.md#one` and `## Checks` linking `rules.md#two`, `rules.md#one`'s link to `x.md` compiles to the substitute `y.md`. The same holds across the two copies of a document in two groups, and for two section entries of one document.
- **Row.** W31: the design states that a document's links resolve through the `subst` pairs every reference reaching it selects, refused where two disagree, since a region a group emits once cannot carry two resolutions of one link.

### F3. The option table omits the code listing

- **Clause.** *CLI contract*: a command line naming an undeclared option is refused with `E_INVALID_USAGE`, and the option table declares `-o`, `-c`, `-d`, `--budget`, `-v` and `-h`. The clause's prose names a code-listing response and *Metadata failures* a build's own list of codes, which no option declares.
- **Build.** `cli.py` `parser` admits `-C`/`--codes`, which `make conformance` invokes, and the long spellings `--version` and `--help`.
- **Row.** W32: the design's option table declares the code listing and the long spellings the build admits.

## Where the Epics Meet

Each held.

- **Presets in dispatched bundles.** A dispatched target compiles as an entry and selects by its own title; a preset selected only in a dispatched bundle raises no `W_PRESET_UNUSED`.
- **`subst` on operators.** A writer's pair redirects a dispatched and a deferred link; the dispatched bundle takes the substitute's name.
- **Composition in a dispatched bundle.** A deferred directive there opens the bundle on *Run pf first* and the line referring to it; the entry's bundle carries none.
- **Nested groups under presets.** A document in two groups nests each group in the entry's division, in placement order.
- **Publication.** A file at the run folder's path is refused, a symbolic link there is replaced and its target left, and `cleanup-refused` warns `W_EARLIER_SET_RETAINED`.

## Documentation Notes

For the page rows W02–W21: no page under `docs/`, `README.md`, `invocation.md` or the checks pages names a retired option, code or the run-set mark. `fixtures/README.md` states that "The invocation working directory must exist", which holds; W30 changes what the design says of the output folder, which W03 and W09 read.

## Clauses

| Clause | State | Code | Evidence | Verdict |
| --- | --- | --- | --- | --- |
| Input and output contract — Entry references | changed | `cli.py` `declared_entries`, `entry` | `frontmatter/delimiter-with-trailing-spaces`, `frontmatter/indented-delimiter` and 3 more; probe: an undeclared entry fails `E_TARGET_NOT_FOUND` | Meets |
| Input and output contract — Continuous Markdown | changed | `bundle.py` `assemble`, `openings` | `rewriting/a-cross-group-reference` | Meets |
| Input and output contract — Generated headings | changed | `heading.py` `title_cased`; `grouping.py` `member_headings`; `dispatch.py` `Placing` | `grouping/one-spelling-for-every-generated-heading`, `headings/an-authored-heading-beside-a-generated-one` | Meets |
| Input and output contract — Groups | changed | `cli.py` `placement`, `divisions`, `holders` | `consolidation/a-child-then-its-whole-document`, `consolidation/a-subsection-and-its-section` and 5 more | Meets |
| Input and output contract — Dependency order | changed | `cli.py` `placement`, `holders` | `grouping/a-document-no-group-matches`, `identity/same-basename-in-two-directories` | Meets |
| Markdown and source-heading profile | changed | `profile.py` `parser`; `__init__.py` `PROFILE` | `cli/informational-long-version-response`, `cli/informational-version-response` and 2 more | Meets |
| Markdown and source-heading profile — Unsupported extensions | changed | `profile.py` `inline_refusals`; `closure.py` `directive` | `profile/extension-lookalikes`, `profile/unsupported-construct` and 1 more | Meets |
| CLI contract | changed | `cli.py` `parser`, `execute` | `cli/a-bare-fragment-is-invalid-usage`, `cli/a-bare-fragment-is-invalid-usage` and 14 more; probe: `-C`/`--codes` lists codes, exit 0 | Departs: [F3](#f3-the-option-table-omits-the-code-listing) |
| CLI contract — -o DIR | added | `cli.py` `publication`, `publish_folder` | `cli/a-bundle-written-into-the-folder-o-names`, `cli/a-bundle-written-into-the-working-directory` and 6 more; probe: `-o nothere` makes the folder and publishes, exit 0 | Departs: [F1](#f1-the-output-folder-is-made) |
| CLI contract — --budget NAME=VALUE | added | `cli.py` `budget_entry`, `BudgetEntries`; `limits.py` `BUDGETS` | `limits/a-named-budget-bounds-the-run` | Meets |
| CLI contract — -h | changed | `cli.py` `parser` | `cli/informational-long-usage-response`, `cli/informational-usage-response`; probe: `-h` states bare `pf` prints the guide | Meets |
| Guide | added | `cli.py` `GUIDE`, `execute` | `cli/informational-guide-response`; probe: bare `pf` prints the guide, exit 0 | Meets |
| Conformance faults | added | `cli.py` `conformance_fault`, `FAULTS` | probe: `cleanup-refused` warns `W_EARLIER_SET_RETAINED` | Meets |
| Conformance faults — Values | added | `cli.py` `conformance_fault`, `FAULTS` | fixtures `source-consistency/a-source-that-changes-during-compilation`, `diagnostics/a-run-that-fails-in-itself`, `publication/an-earlier-set-the-run-cannot-remove-warns` | Meets |
| Conformance faults — Absent | added | `cli.py` `conformance_fault`, `FAULTS` | every fixture run without the variable | Meets |
| Conformance faults — Unknown value | added | `cli.py` `conformance_fault`, `FAULTS` | `cli/an-unknown-fault-is-invalid-usage` | Meets |
| Automatic output names | changed | `cli.py` `selections`, `run_name`, `bundle_file`, `colliding`, `overlong` | `cli/a-bundle-written-into-the-folder-o-names`, `cli/a-bundle-written-into-the-working-directory` and 5 more | Meets |
| Automatic output names — work-planner/modes/align-mode.md, declaring prosiform | added | `cli.py` `selections`, `run_name`, `bundle_file`, `colliding`, `overlong` | probe: `work-planner_modes_align-mode.bundles/work-planner_modes_align-mode.bundle.md` | Meets |
| Automatic output names — work-planner/SKILL.md, declaring prosiform | added | `cli.py` `selections`, `run_name`, `bundle_file`, `colliding`, `overlong` | probe: `work-planner_SKILL.bundles/work-planner_SKILL.bundle.md` | Meets |
| Automatic output names — Equivalent references guide.md and ./guide.md#, both declaring | added | `cli.py` `selections`, `run_name`, `bundle_file`, `colliding`, `overlong` | probe: `guide.bundles/guide.bundle.md` | Meets |
| Automatic output names — guide.md#one and guide.md#two | changed | `cli.py` `selections`, `run_name`, `bundle_file`, `colliding`, `overlong` | probe: `guide__one+guide__two.bundle.md`; fixture `cli/several-entries-joined-into-one-name` | Meets |
| Automatic output names — rules.md, then guide.md#run | added | `cli.py` `selections`, `run_name`, `bundle_file`, `colliding`, `overlong` | probe: `rules+guide__run.bundle.md` | Meets |
| Explicitly linked source structure — Explicit dependencies | changed | `closure.py` `inside`, `Declarations`; `cli.py` `probe` | `citation/a-reference-above-the-working-directory`, `composition/ascii-and-spaced-labels-are-ordinary-links` and 9 more | Meets |
| File-scoped hierarchy | changed | `bundle.py` `file_heading`, `group` | `boundary/the-file-heading-between-two-groups`, `grouping/one-spelling-for-every-generated-heading` and 7 more | Meets |
| Grouping | changed | `grouping.py`; `cli.py` `placement` | `grouping/a-member-carrying-one-heading-bundled-by-document`, `grouping/a-rule-matching-no-document-in-the-closure` and 3 more | Meets |
| Grouping — Consistent depth | changed | `cli.py` `group_depths`, `GROUP_CONFLICT` | probe: two depths for one group fail `E_GROUP_CONFLICT` with both locations | Meets |
| Grouping — A file places its own sections | added | `cli.py` `pair`, `joined`, `placement` | `grouping/a-file-places-its-own-sections`, `grouping/a-linked-file-is-composed-before-its-parent-merges-it` | Meets |
| Grouping — Composition from the leaves up | added | `cli.py` `placement`, `divisions`, `assembled` | `grouping/a-link-a-file-does-not-bundle-stays-its-content`, `grouping/a-linked-file-is-composed-before-its-parent-merges-it` and 1 more | Meets |
| Grouping — Nested groups | added | `cli.py` `divisions`, `holders`; `bundle.py` `group` | `grouping/a-document-no-group-matches`, `grouping/a-file-places-its-own-sections` and 20 more | Meets |
| Grouping — Group structure | changed | `grouping.py` `merged`, `sections` | `grouping/a-section-shallower-than-the-grouping-depth`, `grouping/one-entry-bundled-by-group` and 3 more | Meets |
| Grouping — Variants by document | changed | `grouping.py` `member_headings`, `section` | `depth-overflow/a-structural-ancestor-the-arrangement-pushes-past-the-sixth`, `grouping/a-member-whose-name-carries-no-word-takes-its-path-text` and 9 more | Meets |
| Grouping — Group naming | changed | `grouping.py` `merged_heading`; `metadata.py` `_membership`; `heading.py` `worded` | `grouping/a-document-no-group-matches`, `grouping/a-group-name-carrying-no-word-fails` and 2 more; probe: `harness-rules` heads `Harness-Rules`; a wordless slug is refused | Meets |
| Grouping — Document content above the grouping depth | changed | `grouping.py` `member_headings`, `worded_names`, `above_depth` | `grouping/a-group-emitting-no-merged-section`, `grouping/a-member-named-by-the-title-it-absorbs` and 17 more | Meets |
| Grouping — The overview section | changed | `grouping.py` `overview` | `grouping/a-group-emitting-no-merged-section`, `grouping/a-member-named-by-the-title-it-absorbs` and 1 more; probe: heading-only subsections sit beside merged sections | Meets |
| Grouping — The parent arrangement | changed | `grouping.py` `arranged`, `direct`, `names_one` | `depth-overflow/a-structural-ancestor-the-arrangement-pushes-past-the-sixth`, `grouping/a-file-places-its-own-sections` and 10 more | Meets |
| Bundle destinations — Internal links | changed | `bundle.py` `rewrite`, `target`; `closure.py` `rebased` | `composition/ascii-and-spaced-labels-are-ordinary-links`, `composition/formatted-labels-are-ordinary-links` and 34 more | Meets |
| Compile before publishing — step 2 | changed | `cli.py` `read_document`; `closure.py` `boundary` | `traversal/a-second-reference-to-one-document` | Meets |
| Compile before publishing — step 6 | changed | `cli.py` `compose`; `composition.py` `Composing` | `rewriting/a-reference-style-link` | Meets |
| Conversion metadata | changed | `metadata.py` `decode`, `_preset` | `frontmatter/invalid-conversion` | Meets |
| Conversion metadata — group | added | `metadata.py` `_membership`, `_pair` | fixtures under group holds one pair | Meets |
| Conversion metadata — subst | added | `metadata.py` `_subst`; `cli.py` `substs` | fixtures under subst holds colon pairs | Meets |
| Conversion metadata — The admitted keys | changed | `metadata.py` `decode`, `_preset` | `frontmatter/an-unknown-prosiform-key-fails`, `grouping/a-group-declaration-naming-group-heading-fails` and 2 more | Meets |
| Conversion metadata — group holds one pair | added | `metadata.py` `_membership`, `_pair` | `inclusion/two-presets-stating-two-groups-are-refused` | Meets |
| Conversion metadata — root is refused | added | `metadata.py` `_refused_root` | `inclusion/a-declared-root-is-refused`; probe: `root` refused naming the field | Meets |
| Conversion metadata — An entry is one string key with an integer value | added | `metadata.py` `_pair`, `_level` | `inclusion/a-group-entry-keyed-by-a-number-is-refused`, `inclusion/a-malformed-group-entry-is-refused` | Meets |
| Conversion metadata — subst holds colon pairs | added | `metadata.py` `_subst`; `cli.py` `substs`, `subst_identity` | `inclusion/a-duplicate-subst-entry-is-refused`, `inclusion/a-folder-subst-is-refused` and 8 more | Meets |
| Conversion metadata — A preset holds what shapes the bundle | added | `metadata.py` `_preset`, `FIELDS` | code read: `FIELDS` admits `group` and `subst` alone | Meets |
| Conversion metadata — An empty block declares | added | `source.py` `declaration`; `cli.py` `probe` | `inclusion/an-empty-block-declares`, `inclusion/no-block-does-not-declare` | Meets |
| Conversion metadata — Bounded parsing | changed | `metadata.py` `decode`; `limits.py` `NESTING` | fixtures `frontmatter/*`, `parser-limit/*` | Meets |
| Conversion metadata — Source ownership | changed | `cli.py` `read_document`; `metadata.py` `Conversion` | fixtures `ownership/*` | Meets |
| Conversion metadata — Selection boundary | changed | `cli.py` `probe`, `withheld` | `inclusion/a-deferred-target-keeps-its-preset`, `inclusion/a-followed-deferral-reads-its-preset` | Meets |
| Conversion metadata — Operational interface | changed | `cli.py` `parser` | probe: `--budget` and `-o` are options; no preset field names them | Meets |
| Presets | added | `cli.py` `keywords`, `pair`, `governing` | fixtures under its rules | Meets |
| Presets — Selection by keyword | added | `cli.py` `keyworded`, `selecting_title` | `composition/a-deferral-whose-step-and-target-select-no-preset-is-kept`, `composition/a-deferral-whose-step-and-target-select-one-preset-is-kept` and 12 more | Meets |
| Presets — default always applies | added | `cli.py` `pair`, `governing` | `composition/the-writers-subst-redirects-a-directive`, `depth-overflow/a-structural-ancestor-the-arrangement-pushes-past-the-sixth` and 45 more | Meets |
| Presets — default is not selectable by keyword | added | `cli.py` `keywords` | code read: `keywords` skips `DEFAULT` | Meets |
| Presets — A command-line entry reads the file it names | added | `cli.py` `entry_title`, `selecting_title` | `composition/a-deferral-whose-step-and-target-select-no-preset-is-kept`, `composition/a-deferral-whose-step-and-target-select-one-preset-is-kept` and 6 more | Meets |
| Presets — Selected presets union | added | `cli.py` `agreed`, `stated_once`, `disagreeing` | `inclusion/a-duplicate-subst-entry-is-refused`, `inclusion/a-pair-a-selected-preset-overrides-records-no-substitution` and 6 more; probe: two group pairs one title selects exit 2 | Meets |
| Presets — What a selection governs | added | `cli.py` `governing`, `pair`; `closure.py` `Substitution.writing` | `composition/a-selected-preset-governs-the-contribution`, `inclusion/a-dependencys-preset-comes-from-itself` and 2 more | Meets |
| Presets — One document under several selections | added | `cli.py` `governing`, `joined` | `inclusion/one-document-two-presets`; probe: a `subst` pair one reference selects redirects content another reference bundled | Departs: [F2](#f2-subst-pairs-combine-across-references) |
| Presets — A document in several groups | added | `cli.py` `joined`, `placement` | `grouping/a-group-placed-by-a-document-in-two-groups`, `inclusion/one-document-two-presets` | Meets |
| Presets — profile and preset are two terms | added | `__init__.py` `PROFILE`; `cli.py` `parser` | probe: `-v` reports `skill-markdown-v4` | Meets |
| Presets — A preset nothing selected warns | added | `cli.py` `unused_presets` | `inclusion/a-deferred-target-keeps-its-preset`, `inclusion/a-followed-deferral-reads-its-preset` and 6 more | Meets |
| Metadata failures | changed | `metadata.py` `InvalidMetadata`; `cli.py` `preset_refusal` | `frontmatter/an-unknown-prosiform-key-fails`, `frontmatter/invalid-conversion` and 10 more | Meets |
| Metadata failures — E_INVALID_CONVERSION_METADATA | changed | `metadata.py` `INVALID_CONVERSION_METADATA` | `inclusion/a-declared-root-is-refused`, `inclusion/a-folder-subst-is-refused` and 5 more | Meets |
| Metadata failures — E_GROUP_CONFLICT | added | `cli.py` `group_depths` | probe as Consistent depth | Meets |
| Metadata failures — E_SOURCE_SYMLINK | changed | `access.py` `Symlinked` | fixtures `confinement/*symbolic*` | Meets |
| Metadata failures — E_SOURCE_OUTSIDE_ROOT | changed | `closure.py` `OutsideRoot`; `cli.py` `entry` | probe: `/tmp/x.md` and `C:x.md` entries refused | Meets |
| Metadata failures — E_SOURCE_ACCESS | changed | `access.py` `refusal` | `confinement/a-path-the-filesystem-cannot-open` | Meets |
| Metadata failures — E_SOURCE_CHANGED | changed | `cli.py` `recheck`, `changed` | fixture `source-consistency/a-source-that-changes-during-compilation` | Meets |
| Link classification and resource handling | changed | `closure.py` `inside`, `Declarations` | `reference/a-declaring-document-is-a-dependency` | Meets |
| Link classification and resource handling — The substitution mapping | added | `closure.py` `Substitution`, `Redirects`; `cli.py` `governing`, `substituted`, `unused_pairs` | `composition/the-writers-subst-redirects-a-directive`, `inclusion/a-dispatched-bundle-reads-its-own-subst` and 23 more | Meets |
| Link classification and resource handling — Local Markdown document links | added | `closure.py` `inside`, `bundled` | `inclusion/a-declaring-target-above-the-working-directory-is-compiled`, `inclusion/a-declaring-target-is-compiled` and 13 more | Meets |
| Link classification and resource handling — The deferral mark | changed | `closure.py` `deferred`, `unmarked` | `composition/a-glyph-written-against-the-deferral-mark-is-a-deferred-directive`, `composition/an-ordinary-deferred-label-is-a-deferral` and 5 more | Meets |
| Link classification and resource handling — The dispatch operator | changed | `closure.py` `dispatched`; `dispatch.py` `Placing` | `dispatch/a-dispatch-mark-with-no-space-after-it-opens-an-ordinary-link`, `dispatch/a-dispatched-target-is-a-bundle-of-its-own` | Meets |
| Link classification and resource handling — The parallel dispatch mark | added | `closure.py` `parallel`; `dispatch.py` `Placing` | `parallel-dispatch/a-parallel-mark-with-no-space-after-it-opens-an-ordinary-link`, `parallel-dispatch/a-set-in-one-section` | Meets |
| Link classification and resource handling — Operators that combine | added | `closure.py` `gapped`, `contradicting`, `conflicting`; `cli.py` `refusals_of_operators` | `composition/a-blank-between-the-deferral-mark-and-a-glyph-is-refused`, `composition/a-blank-between-the-dispatch-mark-and-a-glyph-is-refused` and 9 more | Meets |
| Link classification and resource handling — An operator's target | changed | `cli.py` `refusals_of_operators` | `composition/a-deferred-directive-naming-a-document-that-declares-nothing-is-refused`, `deferral/a-deferred-image` and 8 more | Meets |
| Link classification and resource handling — Dispatched bundles | added | `cli.py` `dispatched_set`, `compiled` | `dispatch/a-chain-of-three-dispatches`, `dispatch/a-chain-of-two-dispatches` and 16 more | Meets |
| Link classification and resource handling — Dispatch sub-sections | added | `dispatch.py` `Placing`, `subsections`, `link_text` | `composition/a-dispatch-in-an-inline-only-contribution-takes-its-own-sub-section`, `dispatch/a-chain-of-three-dispatches` and 11 more | Meets |
| Link classification and resource handling — Parallel dispatch sub-sections | added | `dispatch.py` `Placing`, `listing` | `parallel-dispatch/a-section-carrying-both-operators`, `parallel-dispatch/a-set-in-one-section` and 3 more | Meets |
| Link classification and resource handling — The Prosiform section | added | `dispatch.py` `first_run`, `FIRST_RUN_PROTOCOL`, `DISPATCH_PROTOCOL`, `PARALLEL_PROTOCOL` | `dispatch/a-deferred-directive-in-a-dispatched-bundle-opens-with-a-first-run`, `dispatch/a-deferred-dispatch-in-a-dispatched-bundle` and 10 more | Meets |
| Link classification and resource handling — Generated heading collisions | added | `dispatch.py` `collisions` | `dispatch/a-heading-equal-to-a-dispatch-sub-section-is-refused`, `dispatch/a-parallel-heading-publishes-beside-a-dispatch-only` and 4 more | Meets |
| Link classification and resource handling — Dispatching its own document | changed | `dispatch.py` `selfward` | `dispatch/a-dispatch-of-a-section-of-its-own-document-by-fragment-warns`, `dispatch/a-dispatch-of-a-section-of-its-own-document-by-path-warns` and 2 more | Meets |
| Link classification and resource handling — Dispatch depth | changed | `dispatch.py` `deepest`, `LIMIT` | `dispatch/a-chain-of-three-dispatches`, `dispatch/a-chain-of-two-dispatches` and 2 more | Meets |
| Link classification and resource handling — Dispatch cycles | changed | `dispatch.py` `returning`, `cycle` | `dispatch/a-cycle-of-dispatches-is-refused`, `dispatch/a-dispatch-of-its-own-whole-document-is-a-cycle` | Meets |
| Link classification and resource handling — A deferred link's destination | added | `closure.py` `rebased`; `bundle.py` `rewrite` | `composition/a-composed-contract-leaves-its-deferred-implementation-absent`, `deferral/a-deferral-stands-where-another-reference-carried-its-target` and 7 more | Meets |
| Link classification and resource handling — A link naming a document that declares nothing | added | `cli.py` `probe`; `closure.py` `Probed` | `citation/a-reference-above-the-working-directory`, `confinement/a-drive-path-inside-a-source` and 11 more | Meets |
| Link classification and resource handling — Fragment-only links | changed | `closure.py` `inside`, `resolve` | `deferral/a-deferred-fragment-of-its-own-document`, `dispatch/a-dispatch-of-a-section-of-its-own-document-by-fragment-warns` and 4 more | Meets |
| Link classification and resource handling — A target that resolves to nothing | changed | `closure.py` `withholding_target`; `cli.py` `withheld` | `deferral/a-deferred-reference-naming-no-document`, `deferral/a-deferred-reference-naming-no-heading` and 3 more | Meets |
| Link classification and resource handling — Resources | changed | `cli.py` `resource`, `resourced` | `resource/an-image-naming-a-local-document` | Meets |
| Link classification and resource handling — Composition | added | `closure.py` `directive`, `arrow` | fixtures under Section composition | Meets |
| Link classification and resource handling — Examples | changed | `source.py` diagram link readers; `bundle.py` `clicked` | `literal-bracket/brackets-in-examples-stay-as-written`, `real-source/absorbed-title-and-self-references` and 21 more | Meets |
| Section composition | added | `composition.py` `Composing` | fixtures under its rules | Meets |
| Section composition — Recognition | added | `closure.py` `arrow`, `directive`, `placing`; `source.py` `plain_label` | `composition/a-glyph-in-code-or-unresolved-brackets-is-text`, `composition/a-glyph-label-in-a-preamble-has-no-scope` and 8 more | Meets |
| Section composition — Operator marks | added | `closure.py` `MARKS`, `against`, `contradicting` | `composition/a-blank-between-the-deferral-mark-and-a-glyph-is-refused`, `composition/a-blank-between-the-dispatch-mark-and-a-glyph-is-refused` and 4 more | Meets |
| Section composition — The eligible target | added | `cli.py` `refusals_of_directives` | `composition/a-deferred-directive-naming-a-document-that-declares-nothing-is-refused`, `composition/a-directive-naming-a-document-that-declares-nothing-is-refused` and 6 more | Meets |
| Section composition — The destination scope | added | `cli.py` `refusals_of_directives`; `composition.py` `Composing` | `composition/a-directive-in-a-title-above-the-selection-has-no-scope`, `composition/a-directive-in-an-absorbed-title-has-no-scope` and 7 more | Meets |
| Section composition — Destination sections | added | `composition.py` `Composing` | `composition/a-list-is-carried-as-written`, `composition/a-multi-paragraph-body-is-carried-whole` and 7 more | Meets |
| Section composition — Contributions | added | `composition.py` `Composing`, `Parentless` | `composition/a-contribution-resolves-links-from-its-source-directory`, `composition/a-link-inside-a-contribution-includes-its-target` and 12 more | Meets |
| Section composition — Heading depth | added | `composition.py` `Overflowing` | `composition/a-directive-composing-past-the-sixth-level-is-refused`, `composition/nested-headings-keep-their-relative-depth` | Meets |
| Section composition — Generated heading collisions | added | `composition.py` `Colliding` | `composition/an-authored-heading-equal-to-a-destination-section-is-refused` | Meets |
| Section composition — Order | added | `composition.py` `Composing` | `composition/a-directive-inside-a-contribution-composes-beneath-it`, `composition/a-repeated-directive-contributes-each-time` and 2 more | Meets |
| Section composition — Matching | added | `composition.py` `Composing` | `composition/same-titled-parents-keep-a-contribution-each`, `composition/titles-from-several-sources-share-one-destination-section` and 1 more | Meets |
| Section composition — The source of composed content | added | `composition.py` `contributions`; `provenance.py` `Contributing` | `composition/a-contribution-resolves-links-from-its-source-directory`, `composition/a-diagnostic-inside-a-contribution-names-its-source` and 2 more | Meets |
| Section composition — The directive's link | added | `bundle.py` `rewrite` | `composition/a-composed-contract-leaves-its-deferred-implementation-absent`, `composition/a-contribution-resolves-links-from-its-source-directory` and 10 more | Meets |
| Section composition — Every occurrence composes | added | `composition.py` `compositions` | `composition/a-repeated-directive-contributes-each-time`, `composition/ordinary-and-composing-links-to-one-section-each-keep-their-meaning` and 1 more | Meets |
| Section composition — Nested directives | added | `composition.py` `Composing` | `composition/a-contribution-composing-its-own-section-is-refused`, `composition/a-cycle-of-directives-is-refused` and 2 more | Meets |
| Section composition — Composition cycles | added | `composition.py` `Cycling` | `composition/a-contribution-composing-its-own-section-is-refused`, `composition/a-cycle-of-directives-is-refused` and 1 more | Meets |
| Section composition — Composing its own document | added | `cli.py` `composing_itself` | `composition/a-directive-composing-a-section-of-its-own-document-by-fragment-warns`, `composition/a-directive-composing-a-section-of-its-own-document-by-path-warns` | Meets |
| Section composition — Budgets | added | `composition.py` `Composing`; `limits.py` `OUTPUT_BYTES` | `composition/a-directive-is-a-hop-toward-the-expansion-depth`, `composition/a-multiplying-composition-crossing-the-output-budget` | Meets |
| Section composition — Inline-only targets | added | `cli.py` `placement` | `composition/a-contribution-resolves-links-from-its-source-directory`, `composition/a-dispatch-in-an-inline-only-contribution-takes-its-own-sub-section` and 14 more | Meets |
| Section composition — Presets and subst | added | `cli.py` `refusals_of_deferrals`, `governing` | `composition/a-deferral-whose-step-and-target-select-no-preset-is-kept`, `composition/a-deferral-whose-step-and-target-select-one-preset-is-kept` and 6 more | Meets |
| Section composition — Deferred composition | added | `composition.py` `Composing`; `cli.py` `placed_twice` | `composition/a-composed-contract-leaves-its-deferred-implementation-absent`, `composition/a-deferral-whose-step-and-target-select-no-preset-is-kept` and 8 more | Meets |
| Section composition — Activation | added | `candidate.py` `activation`; `provenance.py` `Instruction` | `composition/a-deferred-body-that-fails-fails-when-activated`, `composition/a-deferred-body-that-fails-is-deferred-without-failing` and 1 more | Meets |
| Section composition — Failure | added | `cli.py` `execute` | `composition/a-composition-failing-in-a-check-run-publishes-nothing`, `composition/a-composition-failing-in-a-dispatched-bundle-publishes-nothing` and 1 more | Meets |
| Reference normalization and path identity | changed | `closure.py` `resolve`, `normalized`, `boundary` | `cli/a-bare-fragment-is-invalid-usage`, `confinement/a-drive-path-inside-a-source` and 9 more | Meets |
| Bounded bootstrap capture | changed | `access.py` `opened`, `read_source`; `cli.py` `read_document` | fixtures `confinement/*`, `source-consistency/*` | Meets |
| Resolution sequence — step 3 | changed | `closure.py` `resolve` | `normalization/a-scheme-and-an-authority-in-selected-content` | Meets |
| Resolution sequence — step 7 | changed | `closure.py` `resolve` | `normalization/a-parent-segment-and-a-fragment`, `normalization/a-parent-segment-reaching-the-working-directory` and 3 more | Meets |
| Resolution sequence — A source link whose target declares nothing | added | `cli.py` `probe` | fixtures under A link naming a document that declares nothing | Meets |
| No-symlink source policy | changed | `access.py` `descend`, `walked_directory` | `cli/output-naming-what-a-link-points-at`, `confinement/a-symlink-chain-below-the-working-directory` and 6 more | Meets |
| Resource limits | changed | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `dispatch/a-dispatched-target-crossing-the-file-budget` | Meets |
| Resource limits — files | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `dispatch/a-dispatched-target-crossing-the-file-budget`, `inclusion/a-silent-target-is-text` and 2 more | Meets |
| Resource limits — file-bytes | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `inclusion/an-oversized-declaring-target-fails`, `inclusion/an-oversized-silent-target-is-text` and 1 more | Meets |
| Resource limits — input-bytes | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `limits/an-input-byte-budget-crossed` | Meets |
| Resource limits — output-bytes | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `composition/a-multiplying-composition-crossing-the-output-budget`, `limits/an-output-byte-budget-crossed` | Meets |
| Resource limits — targets | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `limits/a-target-budget-crossed` | Meets |
| Resource limits — links | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `limits/a-link-budget-crossed`, `limits/a-link-budget-crossed-by-a-links-line` and 1 more | Meets |
| Resource limits — nesting | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `file-wide-safety/an-unselected-construct-crosses-a-safety-limit`, `limits/a-nesting-budget-crossed` | Meets |
| Resource limits — depth | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `composition/a-directive-is-a-hop-toward-the-expansion-depth`, `limits/a-target-at-the-expansion-depth` and 1 more | Meets |
| Resource limits — Unknown name | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `cli/an-unknown-budget-name-is-invalid-usage`; probe: `bogus=1` refused, exit 2 | Meets |
| Resource limits — Malformed entry | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `cli/a-budget-entry-naming-no-budget-is-invalid-usage`, `cli/a-malformed-budget-entry-is-invalid-usage` and 2 more | Meets |
| Resource limits — Name given twice | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `cli/a-budget-named-twice-is-refused`; probe: `files` twice refused, exit 2 | Meets |
| Resource limits — Nesting floor | added | `limits.py` `BUDGETS`, `Limits`; `cli.py` `budget_entry` | `cli/a-nesting-budget-below-two-is-refused`; probe: `nesting=1` refused, exit 2 | Meets |
| Agent delivery contract — Clean Markdown | changed | `dispatch.py` `first_run`; `bundle.py` `assemble` | `publication/a-successful-run-writes-only-the-bundle` | Meets |
| Validation scope | changed | `cli.py` `selection`, `traverse` | `ancestor-promotion/a-promoted-ancestor-reaches-its-own-dependencies`, `file-wide-safety/an-unselected-construct-crosses-a-safety-limit` and 8 more | Meets |
| Source and candidate validation modes — Source mode | changed | `cli.py` `read_document`, `substs` | `identity/an-ordinal-names-no-source-heading` | Meets |
| Validation and failure contract — Preservation | changed | `candidate.py` `preserved`, `contributions` | `boundary/a-yaml-example-the-bundle-keeps-intact`, `candidate-validation/a-code-example-carried-byte-for-byte` and 7 more | Meets |
| Validation and failure contract — Safety | changed | `access.py`; `limits.py` | probe: `/tmp/x.md` entry refused; fixtures `confinement/*` | Meets |
| Validation and failure contract — Publication | changed | `cli.py` `publication`, `publish_folder`, `occupied`, `colliding` | `cli/an-author-folder-named-like-the-entry-is-left-untouched`, `composition/a-composition-failing-in-a-check-run-publishes-nothing` and 25 more; probes: a file at the run folder path fails `E_PUBLICATION_FAILED`; a symlink there is replaced, its target untouched; a missing output folder is made | Departs: [F1](#f1-the-output-folder-is-made) |
| Post-compilation invariants — Exactly-once coverage | changed | `candidate.py` `coverage` | `candidate-validation/repeated-identical-prose-in-two-regions` | Meets |
| Post-compilation invariants — Group isolation | changed | `candidate.py` `structure`, `levels` | `grouping/a-document-no-group-matches`, `grouping/a-group-placed-by-a-document-in-two-groups` and 1 more | Meets |
| Exit status and JSON diagnostics — 4 | changed | `cli.py` `INTERNAL_ERROR` | `diagnostics/a-run-that-fails-in-itself` | Meets |
| Adversarial acceptance fixtures — Deferral | changed | the corpus families the case list names | `deferral/a-deferral-mark-with-no-space-after-it-opens-an-ordinary-link`, `deferral/a-deferred-image` and 4 more | Meets |
| Adversarial acceptance fixtures — Dispatch | changed | the corpus families the case list names | `dispatch/a-chain-of-three-dispatches`, `dispatch/a-chain-of-two-dispatches` and 29 more | Meets |
| Adversarial acceptance fixtures — Parallel dispatch | added | the corpus families the case list names | `parallel-dispatch/a-link-carrying-the-parallel-mark-and-the-dispatch-operator`, `parallel-dispatch/a-parallel-link-naming-a-remote-address` and 9 more | Meets |
| Adversarial acceptance fixtures — Prosiform section | added | the corpus families the case list names | `dispatch/a-deferred-directive-in-a-dispatched-bundle-opens-with-a-first-run`, `dispatch/a-deferred-dispatch-in-a-dispatched-bundle` and 10 more | Meets |
| Adversarial acceptance fixtures — Composition | added | the corpus families the case list names | `composition/a-blank-between-the-deferral-mark-and-a-glyph-is-refused`, `composition/a-blank-between-the-dispatch-mark-and-a-glyph-is-refused` and 61 more | Meets |
| Adversarial acceptance fixtures — Normalization | changed | the corpus families the case list names | `normalization/an-empty-fragment` | Meets |
| Adversarial acceptance fixtures — CLI | changed | the corpus families the case list names | `cli/validation-only-run` | Meets |
| Metadata conformance cases — Per-file ownership | changed | the corpus families the case list names | families `ownership`, `inclusion` | Meets |
| Metadata conformance cases — Presets | added | the corpus families the case list names | families `inclusion`, `grouping`, `composition` | Meets |
| Metadata conformance cases — Rejected metadata | changed | the corpus families the case list names | families `frontmatter`, `inclusion` | Meets |
| Metadata conformance cases — Atomic failure | changed | the corpus families the case list names | families `publication`, `frontmatter` | Meets |
| File-owned invocation conformance cases — Declaration defaults | added | the corpus families the case list names | families `inclusion`, `citation` | Meets |
| File-owned invocation conformance cases — Target declarations | added | the corpus families the case list names | `inclusion/a-silent-target-above-is-text`, `inclusion/a-target-above-the-writing-directory-is-compiled` | Meets |
| File-owned invocation conformance cases — Shared identity | changed | the corpus families the case list names | families `identity`, `traversal` | Meets |
| File-owned invocation conformance cases — Declaration safety | added | the corpus families the case list names | families `confinement`, `inclusion` | Meets |
| File-owned invocation conformance cases — Bootstrap limits | changed | the corpus families the case list names | families `limits`, `confinement`, `source-consistency` | Meets |
| File-owned invocation conformance cases — Self references | changed | the corpus families the case list names | families `self-reference`, `deferral` | Meets |
| File-owned invocation conformance cases — Shared paths | added | the corpus families the case list names | families `identity`, `grouping` | Meets |
| File-owned invocation conformance cases — Derived filenames | changed | the corpus families the case list names | family `cli` | Meets |
| File-owned invocation conformance cases — Combined selection | changed | the corpus families the case list names | family `cli` | Meets |
| File-owned invocation conformance cases — Publication | changed | the corpus families the case list names | families `publication`, `cli` | Meets |
| File-owned invocation conformance cases — Deferred handoff | changed | the corpus families the case list names | family `deferral` | Meets |

| Retired clause | Build |
| --- | --- |
| CLI contract — -f DOC | Removed |
| CLI contract — -o FILE | Removed |
| Usage examples | Removed |
| Automatic output names — work-planner/modes/align-mode.md, root ".." | Removed |
| Automatic output names — work-planner/SKILL.md, root "." | Removed |
| Automatic output names — Equivalent references guide.md and ./guide.md#, absent root | Removed |
| Conversion metadata — prosiform.root | Removed |
| Conversion metadata — prosiform.group | Removed |
| Conversion metadata — prosiform.group-depth | Removed |
| Metadata failures — E_GROUP_DEPTH_CONFLICT | Removed |
| Metadata failures — E_ROOT_NOT_FOUND | Removed |
| Link classification and resource handling — Local Markdown document links under the root | Removed |
| Link classification and resource handling — The run-set mark | Removed |
| Link classification and resource handling — One operator per link | Removed |
| Link classification and resource handling — Dispatched procedures | Removed |
| Link classification and resource handling — Run-set shape | Removed |
| Link classification and resource handling — A withheld link's destination | Removed |
| Link classification and resource handling — Local Markdown links resolving outside the root | Removed |
| Resolution sequence — A source link normalized outside its author's root | Removed |
| Resource limits — -F | Removed |
| Resource limits — -B | Removed |
| Resource limits — -I | Removed |
| Resource limits — -O | Removed |
| Resource limits — -T | Removed |
| Resource limits — -L | Removed |
| Resource limits — -N | Removed |
| Resource limits — -E | Removed |
| Adversarial acceptance fixtures — Run-set | Removed |
| File-owned invocation conformance cases — Root defaults | Removed |
| File-owned invocation conformance cases — Explicit roots | Removed |
| File-owned invocation conformance cases — Root safety | Removed |
| File-owned invocation conformance cases — Multi-root identity | Removed |
