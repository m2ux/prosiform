# I05:E03:W01 Validation

Each check the work item's test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e03/w01-output-folder-and-joined`, cut from `i05/e03/main` at `9851615028ea489c48f6b3fa5ddbe0d917438cf2`.
- **Tested revision.** `3ed32a0666b6de609179b73d64a5f8849aaf4da3` for every check below. The two later commits, `dfa94f71` and `3d2a8eaa`, relabel the README diagrams and one sentence of `example/README.md`; `make links`, `make tables`, `make layout` and `make vocabulary` were rerun on `3d2a8eaa` and hold.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`.
- **Contract.** The README pins the design at `034b65365b3be7ba19bf83cf84939f1153052d32` on `engineering`.

## T1 Unit tests

`cd src && uv run --frozen pytest` ran the whole suite: 1252 passed. The tests observing the criteria:

| Test | Observes |
| --- | --- |
| `test_cli.py::test_a_bundle_is_written_into_the_folder_o_names` | AC1: `-o build` holds `guide.bundle.md` alone; standard output is empty. |
| `test_cli.py::test_a_bundle_is_written_into_the_working_directory_without_o` | AC1: no `-o` writes `guide.bundle.md` into the working directory; both streams are empty. |
| `test_cli.py::test_several_entries_write_one_bundle_joining_their_names` | AC2: `guide.md#run docs/note.md ./guide.md#run guide.md` writes `guide__run+docs_note+guide.bundle.md`. |
| `test_derived_output.py::test_distinct_selections_join_their_names_in_entry_order` (10 cases) | AC2: names join in first-naming order (`a+b`, `b+a`, `a__one+a__two`, `a+a__one`, `a__two+b` with `-f`); check mode writes none. |
| `test_cli.py::test_standard_output_named_as_the_folder_is_invalid_usage` | AC3: `-o -` exits 2 with `E_INVALID_USAGE`, the message names standard output, and nothing is written. |
| `test_cli.py::test_a_validation_only_run_with_an_output_folder_writes_nothing` | AC1: `-c -o DIR` leaves the folder empty. |
| `test_cli.py::test_a_bundle_naming_a_dependency_source_is_invalid_usage` | A bundle path naming a captured source exits 2 and leaves the source intact. |
| `test_cli.py::test_an_output_path_the_run_cannot_write_is_a_publication_failure` | A folder that does not exist exits 3 with `E_PUBLICATION_FAILED`. |

`test_linked_bootstrap.py` and `test_handoff_round_trip.py` read each bundle from the folder an installed command writes it to, and pass.

## T2 End-to-end fixtures

`make corpus` ran every fixture; the `fixtures/cli` and `fixtures/delivery` lines:

| Fixture | Observes | Result |
| --- | --- | --- |
| `cli/a-bundle-written-into-the-folder-o-names` | AC1: `-o ..` from `source/` writes `guide.bundle.md` into the fixture directory | pass |
| `cli/a-bundle-written-into-the-working-directory` | AC1: no `-o` writes `guide.bundle.md` into the working directory | pass |
| `cli/several-entries-joined-into-one-name` | AC2: `notes/rules.md guide.md#run ./notes/rules.md` writes `notes_rules+guide__run.bundle.md` | pass |
| `cli/standard-output-named-as-the-output-folder` | AC3: `-o -` exits 2, `E_INVALID_USAGE` naming standard output, no file written | pass |
| `cli/validation-only-run-with-an-output-folder` | `-c -o ..` writes nothing | pass |
| `cli/output-naming-a-dependency-source` | The derived bundle path naming a dependency exits 2 | pass |
| `cli/output-naming-what-a-link-points-at` | The symbolic link is refused before the bundle path is checked | pass |
| `delivery/an-output-destination-that-refuses-the-write` | `-o no-such-directory` exits 3 and writes nothing | pass |

The runner reports a file no bundle names, so each fixture declaring no bundle also observes that its run wrote none.

## T3 Runner instrument

`make harness` ran `checks/tests`: 697 passed. The runner's own cases for AC1:

- `test_a_bundle_is_matched_by_name_wherever_the_run_writes_it`: a bundle written into the `-o` folder above the working directory is found by name and removed.
- `test_a_declared_bundle_the_run_does_not_write_is_reported` and `test_a_file_no_bundle_declares_names_the_expectation`: each mismatch names `expected.bundles`.
- `test_differing_bundle_bytes_are_located` and the newline, short and long cases: a bundle differing in bytes is located by offset, line and column.
- `test_standard_output_carrying_bytes_no_declaration_names_is_reported`: a bundle on standard output fails.
- `test_the_run_receives_the_allowed_root_and_the_diagnostic_format`: the runner adds `-d json` and no `-o`.
- `test_manifest_schema.py`: `expected.bundles` holds `expected/<name>.bundle.md` paths, joined, spaced and bracketed names included; `expected.stdout` and `expected.absent` are refused.

## T4 make check

`PROSIFORM_BUILD=<pf> make check` exited 0: lock check, lint, format check, type check, 1252 unit tests, 697 harness tests, the corpus, the installed-wheel smoke run, layout, tables, links (online), vocabulary, invocation, conformance and independence.

The smoke run bundles into a folder `-o` names, writes derived names into its working directory, joins a document and its section into one bundle under the joined name, refuses `-o -` with exit 2, holds a directory destination to the bundle, and refuses a missing folder with exit 3 and no temporary file.

## T5 make corpus

`corpus check: 315 fixture(s), 315 pass, 0 fail, 0 awaited, 0 unexpected pass`.

Review bar: every non-empty expected bundle of the base revision is present at the head under its fixture's `expected/` with the same blob, so no expected bundle's bytes change. 220 move from `expected/stdout.md` to their derived names; the 88 empty `stdout.md` files of runs writing no bundle are removed; three CLI fixtures add expected bundles.

## T6 make conformance and make invocation

- `make conformance`: 298 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere.
- `make invocation`: 28 statements of `invocation.md`, the `-o DIR` row among them, each held to the build's help.
