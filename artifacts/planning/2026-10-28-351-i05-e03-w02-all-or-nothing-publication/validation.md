# I05:E03:W02 Validation

Each check the work item's test row names, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e03/w02-all-or-nothing-publication`, cut from `i05/e03/main` at `0e75ab3d99a1c50d3ff7a8aac4ecbfac191d045b`.
- **Tested revision.** `3919f9188676cf77ff2794b1f307543720bfda25` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`.
- **Contract.** The README pins the design at `906646ca1dd6d75e7620cc32a01a2a43c90be032` on `engineering`, whose Publication clause states the set behaviour.
- **Sets.** A run publishes one bundle until W03 dispatches targets, so T1 to T4 hold `publication` over sets of three bundles each test constructs, and T2 also runs the command.

## T1 A member failing validation

`test_cli.py::test_a_set_whose_member_fails_validation_writes_no_bundle`: three bundles under a 16-byte output budget, the second crossing it. The step raises `E_RESOURCE_LIMIT`, the folder stays empty and no member's warning is emitted. Observes AC4.

`test_cli.py::test_a_set_whose_member_cannot_be_written_writes_no_bundle`: the third member's folder does not exist. The step raises `E_PUBLICATION_FAILED` naming that path while staging, and the first two members are not written. Observes AC4 for a refusal before any rename.

`test_cli.py::test_a_set_is_published_whole_once_every_member_validates`: the same set within budget writes all three with their bytes, and emits each member's warning in turn.

## T2 Files the run does not produce

`test_cli.py::test_a_set_leaves_every_file_it_does_not_produce_as_it_was`: a folder holding `notes.md`, `other.bundle.md` and a hidden file named like a temporary file keeps each byte for byte after a set is published; the only new files are the set's. Observes AC5.

`test_cli.py::test_a_run_leaves_every_file_in_its_folder_it_does_not_produce`: `pf -o <folder> guide.md` into a folder holding `notes.md` and `docs_note.bundle.md` keeps both byte for byte and adds `guide.bundle.md` alone. Observes AC5.

## T3 A validation-only run over a set

`test_cli.py::test_a_validation_only_set_validates_every_member_and_writes_none`: a passing set under `-c` writes nothing; a set whose last member crosses the budget still raises `E_RESOURCE_LIMIT` under `-c`, so every member was validated, and writes nothing. Observes AC6.

## T4 A rename refused part-way

`test_cli.py::test_a_rename_refused_after_earlier_ones_is_a_publication_failure`: the second destination is a directory, which refuses the rename after the first has landed. The step fails with status 3 and `E_PUBLICATION_FAILED` naming the second path; the first bundle is published, the directory stands, the third destination keeps its earlier bytes, and no temporary file remains. Observes the design's Publication clause.

## T5 make check

`PROSIFORM_BUILD=<pf> make check` exited 0: lock check, lint, format check, type check, 1259 unit tests, 697 harness tests, the corpus, the installed-wheel smoke run, layout, tables, links (online), vocabulary, invocation, conformance and independence. The vocabulary check reads the design at the new pin: 41 contract terms, each defined in `docs/glossary.md`.

## T6 make corpus

`corpus check: 315 fixture(s), 315 pass, 0 fail, 0 awaited, 0 unexpected pass`.

Review bar: every fixture is a single-bundle run, and each publishes the same bytes and diagnostics as on the base revision, since every expected bundle and every declared diagnostic is unchanged by this branch.

## T7 make conformance and make invocation

- `make conformance`: 298 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere.
- `make invocation`: 28 statements of `invocation.md`, each held to the build's help.

## Continuous integration

`Checks` ran `make check` on the pull request head `3919f918` and passed ([run](https://github.com/m2ux/prosiform/actions/runs/40653342775/job/122698387718)).
