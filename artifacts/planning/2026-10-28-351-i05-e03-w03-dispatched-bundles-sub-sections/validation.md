# I05:E03:W03+W04 Validation

Each check the work items' test rows name, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e03/w03-dispatched-bundles-sub-sections`, cut from `i05/e03/main` at `45acf3e1dd6228a3d99ea12406c9926cbfcadd4e`.
- **Tested revision.** `e91b406b` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`.
- **Contract.** The README pins the design at `a967754811fb00ba888fbac061d27ec2daaa00a2` on `engineering`, whose Dispatched bundles, Dispatch sub-sections, Generated heading collisions, Dispatch cycles, Resource limits and Publication clauses state this unit's behaviour.

## T1 Bundle set, sub-sections and budgets (unit)

`src/tests/test_cli.py`, each passing:

| Test | Observes |
| --- | --- |
| `test_a_run_publishes_a_bundle_for_each_target_its_dispatches_reach` | AC7: a two-hop chain publishes `guide`, `plan__steps` and `review` bundles, each link naming the next bundle. |
| `test_a_dispatched_link_points_at_its_sub_section_without_its_mark` | AC8: the published link reads `[the rules](#dispatch-the-rules)` and the section ends with `## Dispatch the rules` naming `rules.bundle.md`. |
| `test_one_target_dispatched_from_two_sections_is_one_bundle` | AC7, AC8: two sections dispatching one target publish one bundle; each section carries its own sub-section, the second `#dispatch-plan-1`, two links in one section sharing it. |
| `test_a_sub_section_precedes_the_child_sections_of_its_section` | AC8: the sub-section stands after the section's content and before `### Detail`. |
| `test_a_dispatch_above_the_first_heading_takes_its_level` | AC8: a preamble dispatch takes the first heading's level. |
| `test_a_dispatch_in_a_linked_document_sits_under_its_shifted_section` | AC8: a dispatch in a shifted file group sits one level below that group's heading. |
| `test_each_bundle_holds_the_file_budget_for_its_own_closure` | AC9: `-F 4` passes and `-F 3` fails with `E_RESOURCE_LIMIT`, the target opening four documents and the entry two. |
| `test_each_bundle_counts_expansion_depth_from_its_own_entry` | AC9: `-E 1` holds for each bundle of a chain three link hops long across a dispatch. |

`src/tests/test_dispatch.py`: depth on graphs as before; `test_two_links_dispatching_one_target_warn_once`.

## T2 Refusals and warnings (unit)

| Test | Observes |
| --- | --- |
| `test_a_cycle_of_dispatches_is_refused_naming_the_chain` | AC10: exit 1, `E_DISPATCH_CYCLE` as an error, chain `guide.md → a.md → b.md → a.md`, nothing written. |
| `test_a_dispatch_of_the_entry_is_a_cycle`, `test_a_section_dispatching_its_own_document_is_a_cycle` | AC10: a chain returning to the entry, and a section dispatching its whole document, are cycles. |
| `test_a_dispatch_in_a_level_six_section_is_refused` | AC10: exit 1, `E_HEADING_DEPTH_OVERFLOW` naming `plan.md` at `guide.md:13`. |
| `test_an_authored_heading_equal_to_one_pf_emits_is_refused[Prosiform, Dispatch in parallel, Dispatch plan]` | AC10: exit 1, `E_HEADING_COLLISION` at the authored heading's line, its text in the message. |
| `test_a_section_dispatched_from_its_own_document_warns_once` | The self-dispatch warning is kept where no cycle closes. |
| `test_a_fourth_dispatch_warns_naming_the_chain`, `test_a_dispatched_section_of_the_entry_is_a_hop` | The depth warning is kept, its chain through the bundles. |
| `test_a_dispatched_section_of_fields_raises_nothing`, `test_a_dispatch_a_run_set_holds_names_its_bundle` | AC11: a target with no numbered step publishes with no diagnostic. |
| `test_dispatch.py::test_a_cycle_longer_than_the_limit_is_refused`, `test_a_dispatch_of_the_entry_is_refused`, `test_a_target_dispatching_itself_is_refused`, `test_a_dense_graph_terminates`, `test_a_dense_acyclic_graph_terminates` | AC10: the refusal over graphs, terminating on dense ones. |

## T3 Bundle set, sub-sections and budgets (end to end)

`make corpus`, each `fixtures/dispatch` fixture passing:

| Fixture | Observes |
| --- | --- |
| `a-chain-of-three-dispatches` | AC7: four bundles, one per target the chain reaches, no warning. |
| `a-dispatched-target-is-a-bundle-of-its-own` | AC7, AC8: the link without its mark points at `## Dispatch the shared rules`, naming `rules.bundle.md`, published beside it. |
| `a-sub-section-per-section-before-its-child-sections` | AC8: a sub-section per section, before `### Detail`; one target from two sections is one bundle; ordinals `#dispatch-plan` and `#dispatch-plan-1`. |
| `a-dispatched-bundle-named-from-the-working-directory` | AC7: targets named through `..` and a spaced path publish under their working-directory names. |
| `a-dispatched-target-crossing-the-file-budget` | AC9: `-F 3` ends in `E_RESOURCE_LIMIT` with the entry's closure at two documents. |
| `a-fourth-dispatch-warns`, `a-dispatched-section-of-the-entry-is-a-hop`, `a-dispatched-section-carrying-steps`, by-fragment and by-path self-dispatch | The bundle set for each, with the kept warnings. |

## T4 Refusals and a target with no step (end to end)

| Fixture | Observes |
| --- | --- |
| `a-cycle-of-dispatches-is-refused` | AC10: exit 1, `E_DISPATCH_CYCLE`, chain `guide.md → plan.md → review.md → plan.md`, no bundle. |
| `a-dispatch-of-its-own-whole-document-is-a-cycle` | AC10: the shortest cycle, refused. |
| `a-dispatch-in-a-level-six-section-is-refused` | AC10: exit 1, `E_HEADING_DEPTH_OVERFLOW` naming `publish.md`. |
| `a-heading-equal-to-a-dispatch-sub-section-is-refused`, `a-prosiform-heading-is-refused` | AC10: exit 1, `E_HEADING_COLLISION` naming the heading. |
| `a-dispatched-document-carrying-no-step`, `a-dispatched-section-of-fields` | AC11: both bundles publish with no diagnostic. |

## T5 The run's folder (user-confirmed design change)

| Test | Observes |
| --- | --- |
| `test_cli.py::test_a_bundle_is_written_into_the_folder_o_names`, `..._into_the_working_directory_without_o`, `test_several_entries_write_one_bundle_joining_their_names` | AC1: `-o build guide.md` writes `build/guide/guide.bundle.md`; no `-o` writes `guide/guide.bundle.md`; joined entries name the folder and the bundle. |
| `test_a_set_whose_member_fails_validation_writes_no_bundle`, `test_a_set_whose_member_cannot_be_written_writes_no_bundle`, `test_two_bundles_deriving_one_name_publish_nothing` | AC4: no folder is written, an earlier one kept byte for byte. |
| `test_a_set_leaves_every_file_it_does_not_produce_as_it_was`, `test_a_run_leaves_every_file_in_its_folder_it_does_not_produce` | AC5: everything under the output folder outside the run's own folder stays as it was. |
| `test_a_validation_only_set_validates_every_member_and_writes_none` | AC6. |
| `test_a_run_folder_replaces_the_earlier_one_whole`, `test_a_refused_swap_restores_the_earlier_folder`, `test_a_run_folder_is_published_through_one_rename`, `test_derived_output.py::test_derived_publication_swaps_the_folder_in_whole`, `test_atomic_failure_preserves_existing_folder` | The swap: an earlier folder's stale bundles are gone after a run; a refused rename restores the earlier folder; the new folder lands in one rename. |
| `test_a_run_folder_holding_a_dependency_source_is_invalid_usage`, `fixtures/cli/run-folder-holding-a-dependency-source` | A run folder holding a captured source exits 2 and leaves the source intact. |
| `checks/tests/test_runner.py` (`test_a_file_written_outside_a_folder_of_the_run_is_reported`, `test_a_folder_named_for_no_declared_bundle_is_reported`, and the rest) | The corpus runner matches bundles within the run's folder. |

## T6 make check

`PROSIFORM_BUILD=<pf> make check` exited 0: lock check, lint, format check, type check, 1276 unit tests, 704 harness tests, the corpus, the installed-wheel smoke run, layout, tables, links (online), vocabulary, invocation, conformance and independence.

## T7 make corpus

`corpus check: 320 fixture(s), 320 pass, 0 fail, 0 awaited, 0 unexpected pass`.

Review bar:

- Every rewritten `fixtures/dispatch` expectation was read against the design before it was accepted: each entry bundle differs only by its links losing the mark and pointing at a sub-section after their section's content, and each new bundle is its target compiled as an entry.
- The usage-example entry bundles change only at a dispatch: `modes_plan-mode`, `modes_advance-mode` and `modes_hoist-mode` each lose one mark and gain one sub-section, and the fixtures gain the bundles those dispatches reach (Sync Mode, Understand Mode, Delivery Recording, Epic Closure, Issue Placement).
- `rewriting/a-state-diagram-click-in-each-form` runs with `-o ..`: its entry `states.md` stands beside `states/`, which its run folder would otherwise be.

## T8 make conformance and make invocation

- `make conformance`: 300 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere; `pf -C` and the design declare the same codes, `E_DISPATCH_CYCLE` and `E_HEADING_COLLISION` among them and `W_DISPATCH_CYCLE` and `W_DISPATCH_NOT_PROCEDURAL` gone.
- `make invocation`: 28 statements of `invocation.md`, the `-o DIR` row among them, each held to the build's help.
