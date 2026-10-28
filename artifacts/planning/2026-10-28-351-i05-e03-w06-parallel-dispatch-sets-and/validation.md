# I05:E03:W06+W07 Validation

Each check the work items' test rows name, in execution order, with the revision it ran on and what it observed.

- **Branch.** `i05/e03/w06-parallel-dispatch-sets-and`, cut from `i05/e03/main` at `4fdaf8a2ffb1c46784ef454522e5deb37dfef32a`.
- **Tested revision.** `58274e76` for every check below.
- **Build under test.** `PROSIFORM_BUILD` named the worktree's locked environment's `pf`.
- **Contract.** The README pins the design at `09e0e8eee2f378160729f5261ae14845592c8d85` on `engineering`, whose parallel dispatch mark, Dispatched bundles, Parallel dispatch sub-sections and Dispatch depth clauses state the set, and which declares no `W_RUN_SET_SHAPE`.

## T1 One set per section (unit)

`test_run_set.py` is removed with the module it tested; the set's unit tests sit in `test_cli.py` beside the dispatch sub-section tests, and the operator's in `test_closure.py`.

| Test | Observes |
| --- | --- |
| `test_cli.py::test_a_sections_parallel_links_point_at_one_sub_section_listing_each_bundle` | AC12: two `⫽` links in one section publish without marks, both pointing at `#dispatch-in-parallel`, whose list names `review__code.bundle.md` (Code Review) and `review__tests.bundle.md` (Test Review); three bundles, no diagnostic. |
| `test_cli.py::test_a_target_named_twice_in_one_set_is_listed_once` | AC12: a target two links name is listed once, with the first link's text. |
| `test_cli.py::test_a_child_sections_parallel_links_form_its_own_set` | AC12: a child section's links point at its own sub-section, `#dispatch-in-parallel-1`. |
| `test_cli.py::test_a_section_carrying_both_operators_has_a_sub_section_for_each` | AC13: a `Dispatch plan` sub-section, then one `Dispatch in parallel`; a target named by `⇉` and `⫽` reaches both. |
| `test_cli.py::test_a_parallel_target_of_any_shape_publishes_with_no_diagnostic` | AC14: a paragraph, a numbered list, an item linking no document and a nested item linking a remote address each publish `plan__reviews.bundle.md` with no diagnostic. |
| `test_cli.py::test_a_parallel_dispatch_is_a_hop_of_a_chain`, `..._closing_a_cycle_is_refused`, `..._in_a_level_six_section_is_refused` | A `⫽` hop counts toward `W_DISPATCH_DEPTH`, closes `E_DISPATCH_CYCLE`, and overflows at level 6. |
| `test_cli.py::test_a_parallel_mark_with_another_operator_is_refused`, `..._link_naming_no_markdown_under_the_root_is_refused`, `..._mark_with_no_space_after_it_opens_an_ordinary_link` | The operator's refusals and the unspaced mark hold. |
| `test_closure.py::test_a_link_opening_with_the_parallel_mark_states_a_parallel_dispatch`, `test_a_parallel_dispatch_withholds_its_target`, `test_an_unspaced_withholding_mark_is_published_as_written` | The `⫽` mark is a dispatch, withholds its target and is stripped. |
| `test_cli.py::test_the_codes_reported_are_the_codes_the_build_declares` | No `W_RUN_SET_SHAPE` is declared. |

## T2 One set per section (end to end)

| Fixture | Observes |
| --- | --- |
| `run-set/a-set-in-one-section` | AC12: exit 0, `guide`, `review__source` and `review__tests` bundles; both links point at `### Dispatch in parallel`, listing each bundle with its link text. |
| `run-set/a-target-named-twice-in-one-set-is-listed-once` | AC12: three links, two targets, two list items. |
| `run-set/a-section-carrying-both-operators` | AC13: `### Dispatch Plan`, then `### Dispatch in parallel`, before `### Detail`. |
| `run-set/a-target-holding-a-paragraph-publishes`, `...-a-numbered-list-publishes`, `...-an-item-linking-no-document-publishes` | AC14: exit 0, `plan__reviews.bundle.md` published, no diagnostic. |
| `run-set/a-link-carrying-the-parallel-mark-and-the-dispatch-operator`, `run-set/a-parallel-link-naming-a-remote-address`, `run-set/a-parallel-mark-with-no-space-after-it-opens-an-ordinary-link` | The refusals and the ordinary link hold under the renamed clauses. |

## T3 Board Reads as steps (inspection)

AC15: `example/work-planner/artifacts/delivery-evidence.md` at `58274e76`.

- Read Board Delivery Evidence's first step is `Apply the [board reads](#board-reads).`, with no `⫽`; the file holds no `⫽` anywhere.
- `#### Board Reads` holds `##### 1. Read Board State`, `##### 2. Fetch Initiative Pull Requests`, `##### 3. Fetch Pull Request Issue Links`, `##### 4. Read Board Configuration` and `##### 5. Read Board Assignee`, each headed by its position and action one level below Board Reads.
- Order follows the results taken: step 2 takes the repositories step 1 returned, step 3 the pull request records step 2 returned; steps 4 and 5 take the board identity and output paths the operation's inputs give.
- Every read the run-set held is a step: the five calls are the five steps.
- `usage-example/a-mode-and-the-board-reads-it-steps-through` (renamed from `a-mode-and-the-calls-it-runs-together`) compiles Board Reads at level 5 with its steps at level 6; its `modes_sync-mode` bundle and `a-procedure-and-everything-it-reaches/expected/modes_sync-mode.bundle.md` take the same rewrite. No other usage-example bundle changes.

## T4 make links

`link check: every reference in 107 document(s) resolved`, the example README's renamed fixture links among them.

## T5 make check

`PROSIFORM_BUILD=<pf> make check` exited 0: lock check, lint, format check, type check, 1259 unit tests, 705 harness tests, the corpus, the installed-wheel smoke run, layout, tables, links (online), vocabulary, invocation, conformance and independence.

## T6 make corpus

`corpus check: 322 fixture(s), 322 pass, 0 fail, 0 awaited, 0 unexpected pass`. Review bar: every `fixtures/run-set` expectation is the set the design's Parallel dispatch sub-sections clause states; the nested run-set fixture is removed with the ordering it showed.

## T7 make conformance and make invocation

- `make conformance`: 300 clauses, 0 declarations naming no clause, 0 declared codes the build reports nowhere, 0 reported codes the contract declares nowhere; `pf -C` declares the design's codes.
- `make invocation`: 28 statements of `invocation.md`, each held to the build's help.
- `make vocabulary`: 42 contract terms, `set` among them, each defined in the glossary.

## Continuous integration

`Checks` ran `make check` on the pull request head `58274e76` and passed ([run](https://github.com/m2ux/prosiform/actions/runs/40674006057/job/122767650752)).
