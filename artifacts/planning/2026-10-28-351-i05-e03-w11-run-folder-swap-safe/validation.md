# I05:E03:W11–W15 Validation

Each test-plan check, the revision it ran on and what it observed.

- **Branch.** `i05/e03/w11-run-folder-swap-safe`, cut from `i05/e03/main` at `751e66e29a588d5c73a968179df0f59b81965db1`, the tree `main` holds at 8e56baf3.
- **Tested revision.** `cbe3d664` for every check below; the three commits split one tested tree.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf` (`src/.venv/bin/pf`, `pf 0.15.0 (skill-markdown-v4)`), never the host's installed `pf`.
- **Contract.** The README pins the design at `7cb8bc9d23e2b2fd7e951076fbc32e4dd44c7186` on `engineering`, which states each behaviour below.

## T1 A link at the run folder

AC27. `src/tests/test_derived_output.py::test_a_link_at_the_run_folder_is_replaced_and_never_followed`, live and dangling: `out/a.bundles -> ../precious` is replaced by a real folder holding `a.bundle.md`; `precious/data.txt` is untouched and `precious/` holds no bundle; the dangling link's target is never created.

## T2 A refused restore

AC28. `src/tests/test_cli.py::test_a_refused_swap_that_cannot_restore_names_where_the_earlier_set_is`: with both renames into the run folder refused, publication fails with status 3, `E_PUBLICATION_FAILED`, a message and remedy naming the `.pf.old.<hex>` path, and that path holds the earlier set.

## T3 A refused cleanup

AC29. `src/tests/test_cli.py::test_an_earlier_set_that_cannot_be_removed_warns_on_a_published_run`: the new set stands, the earlier set remains at the aside path, and one `W_EARLIER_SET_RETAINED` warning names it. Fixture `publication/an-earlier-set-the-run-cannot-remove-warns` (fault `cleanup-refused`): exit 0, `guide.bundle.md`, the warning.

## T4 Two bundles deriving one name

AC30. `src/tests/test_derived_output.py::test_two_targets_deriving_one_name_are_refused_naming_both`, with and without `-c`: an entry dispatching `a/b.md` and `a_b.md` exits 3 with one `E_PUBLICATION_FAILED` naming both and `a_b.bundle.md`, and writes nothing. `src/tests/test_cli.py::test_two_bundles_deriving_one_name_publish_nothing` holds the same at `publication`, both modes, with no warning emitted.

## T5 A missing output folder under -c

AC31. `src/tests/test_derived_output.py::test_an_output_folder_that_does_not_exist_fails_the_check_as_the_run`: `-o zz` exits 3 with `E_PUBLICATION_FAILED`, with and without `-c`, creating nothing. `src/tests/test_cli.py::test_an_output_folder_that_does_not_exist_is_refused_before_any_write` at `publication`. Fixture `publication/a-check-run-into-a-folder-that-does-not-exist-fails`.

## T6 A source read two ways

AC32. `src/tests/test_derived_output.py::test_a_source_changed_between_two_bundles_reads_publishes_nothing`: `plan.md` is edited after the entry's bundle is compiled and before the dispatched bundle's; the run exits 1 with one `E_SOURCE_CHANGED` naming `plan.md` and writes nothing.

## T7 A long run folder name

AC33. `src/tests/test_derived_output.py::test_a_run_folder_name_the_filesystem_accepts_publishes`: a 240-character entry name publishes `<name>.bundles/<name>.bundle.md` and leaves nothing else. `test_derived_publication_swaps_the_folder_in_whole` observes the `.pf.new.` and `.pf.old.` names.

## T8 Collapsed link text

AC34. Fixture `dispatch/dispatch-link-text-is-written-on-one-line`: a soft-wrapped, a hard-broken and a trailing-space `⇉` link name `## Dispatch the shared rules`, `## Dispatch the plan steps` and `## Dispatch the review`, each link keeping its source text. Fixture `parallel-dispatch/parallel-link-text-is-listed-on-one-line`: the listing reads `(the shared rules)` and `(the review)`.

## T9 Empty link text

AC35. Fixture `dispatch/a-dispatch-link-with-no-text-is-refused`: `[⇉ ](plan.md)` exits 1 with `E_UNSUPPORTED_CONSTRUCT`, reference `plan.md`, and no bundle.

## T10 Headings pf does not emit

AC36. Fixtures `dispatch/a-prosiform-heading-publishes-where-nothing-is-dispatched` and `dispatch/a-parallel-heading-publishes-beside-a-dispatch-only`: each publishes with no diagnostic. `src/tests/test_cli.py::test_a_heading_pf_does_not_emit_in_the_bundle_publishes` (three cases); `test_an_authored_heading_equal_to_one_pf_emits_is_refused` still refuses all three headings where the bundle emits them.

## T11 Test manifests

AC37. `checks/tests/test_conformance.py::test_every_manifest_the_corpus_fixture_writes_is_one_the_schema_accepts` and `checks/tests/test_independence.py::test_every_manifest_a_test_writes_is_one_the_schema_accepts`: no schema error.

## T12 Fixture family names

AC38. `ls fixtures/` lists `parallel-dispatch` and `publication`, and no `run-set` or `delivery`.

## T13 One dispatched-link reader

No criterion: findings 7c and 7d. `src/tests/test_cli.py::test_two_links_dispatching_one_deep_target_warn_once` holds the one-warning-per-target rule end to end now that the analysis takes the traversal's distinct hops; every dispatch and parallel-dispatch fixture reproduces its bundles.

## T14 make check

Every target passed: lock-check, lint, format-check, typecheck, `test` (1297 passed), `harness` (731 passed), `corpus` (342 fixtures, 342 pass), smoke, layout, tables, links, vocabulary, invocation, conformance (0 codes the build reports that the contract declares nowhere) and independence.
