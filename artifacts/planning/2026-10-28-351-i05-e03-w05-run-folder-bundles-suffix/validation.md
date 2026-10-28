# I05:E03:W05 Validation

Each check the work item's test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e03/w05-run-folder-bundles-suffix`, cut from `i05/e03/main` at `f006e0b8d7a3c2fdc23627df67809fe379ffb717`.
- **Tested revision.** `cfbbf607` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`.
- **Contract.** The README pins the design at `233e261339e0ff106030099844e2c5a620fe0b4a` on `engineering`, whose CLI, Automatic output names and Publication clauses state the `.bundles` suffix.

## T1 The suffixed run folder (unit)

| Test | Observes |
| --- | --- |
| `test_cli.py::test_an_author_folder_named_like_the_entry_is_left_as_it_was` | AC26: `guide.md` beside `guide/` holding a linked note and an unlinked draft succeeds, writes `guide.bundles/guide.bundle.md`, and leaves `guide/` byte for byte. |
| `test_cli.py::test_a_bundle_is_written_into_the_folder_o_names`, `..._into_the_working_directory_without_o`, `test_several_entries_write_one_bundle_joining_their_names` | AC26: the run folder is `guide.bundles` and `guide__run+docs_note+guide.bundles`. |
| `test_cli.py::test_a_run_folder_is_published_through_one_rename`, `test_a_run_folder_replaces_the_earlier_one_whole`, `test_a_failed_run_leaves_the_earlier_folder_alone`, `test_derived_output.py::test_derived_publication_swaps_the_folder_in_whole` | The swap renames aside, moves in and removes only `<name>.bundles`. |
| `test_cli.py::test_a_run_folder_holding_a_dependency_source_is_invalid_usage`, `test_derived_output.py::test_derived_folder_cannot_hold_any_captured_source` | A source under the run's own `.bundles` folder is still refused, exit 2, the source intact. |

## T2 The suffixed run folder (end to end)

| Fixture | Observes |
| --- | --- |
| `cli/an-author-folder-named-like-the-entry-is-left-untouched` | AC26: exit 0, the note under `guide/` compiled into `guide.bundles/guide.bundle.md`. |
| `rewriting/a-state-diagram-click-in-each-form` | Runs from `source/` with no `-o`, beside `states/`, publishing the bundle it did before W03. |
| `cli/run-folder-holding-a-dependency-source` | A source under `guide.bundles/` refuses the run, naming it. |

## T3 Runner instrument

`make harness`: 706 passed, among them `test_a_folder_missing_the_run_folder_suffix_is_reported` and `test_a_folder_named_for_no_declared_bundle_is_reported`.

## T4 make check

`PROSIFORM_BUILD=<pf> make check` exited 0: lock check, lint, format check, type check, 1277 unit tests, 706 harness tests, the corpus, the installed-wheel smoke run, layout, tables, links (online), vocabulary, invocation, conformance and independence.

## T5 make corpus

`corpus check: 321 fixture(s), 321 pass, 0 fail, 0 awaited, 0 unexpected pass`. Review bar: no expected bundle's bytes change; only the folder runs write into is renamed, and one fixture is added.

## T6 make conformance and make invocation

- `make conformance`: 300 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere.
- `make invocation`: 28 statements of `invocation.md`, each held to the build's help.
