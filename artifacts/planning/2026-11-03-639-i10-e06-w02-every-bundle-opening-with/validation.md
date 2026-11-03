# Validation

The checks W02, W03 and W04's work items name, run against task branch `i10/e06/w02-every-bundle-opening-with` at `dbe7d339`, on the design pinned at engineering commit `884681c0cc4caaa9a1740a24fab204fea9a39d1a`.

## T1 Run-pf Line On Every Bundle

Every `expected/*.bundle.md` of the 507 conformance fixtures opens with ``Before reading on, run `pf` with no arguments and follow the guide it prints.`` and one blank line, whatever the bundle holds: `prosiform/` holds one fixture each for an entry, a dispatched bundle, a bundle dispatching nothing, a deferred directive's `↳` line, content above the title and a file heading. `src/tests/test_bundle.py` reads the same bytes (`test_every_bundle_opens_with_the_run_pf_line` and the four that follow it). Result: held. Observes AC5.

## T2 No Protocol In Any Bundle

`prosiform/a-bundle-using-both-operators-carries-no-protocol`, `...-the-dispatch-operator-carries-no-protocol` and `...-the-parallel-mark-carries-no-protocol` publish no Prosiform section, protocol paragraph, generated dispatch sub-section, `⫽` or `¬` mark. Authored `Prosiform`, `Dispatch` and `Parallel dispatch` headings publish in `prosiform/` and `dispatch/`. `test_a_bundle_using_both_operators_carries_no_protocol` and `test_an_authored_heading_pf_does_not_emit_publishes` in `src/tests/test_bundle.py`. Result: held. Observes AC6.

## T3 Inline Dispatch Link

`dispatch/a-dispatched-target-is-a-bundle-of-its-own`, `each-section-keeps-its-own-dispatch-link-inline`, `a-dispatch-in-a-level-six-section-publishes`, `a-dispatched-bundle-named-from-the-working-directory` and `composition/a-dispatch-in-an-inline-only-contribution-publishes-inline` publish `[⇉ x](<compiled file>)` in place with the mark and one blank. `test_a_dispatch_link_publishes_with_its_mark_and_one_blank` and `test_a_dispatched_link_stays_inline_pointing_at_its_bundle_file`. Result: held. Observes AC7.

## T4 In Parallel Section

`parallel-dispatch/a-set-in-one-section`, `sets-in-sibling-and-nested-sections`, `a-section-carrying-both-operators` and `a-target-named-twice-in-one-set-is-listed-once` publish one `In parallel` section under `Give each of these to its own sub-agent at the same time, and continue when all have answered:`, each member a `- [⇉ text](file)` item. `a-set-in-a-level-six-section-is-refused` and `an-in-parallel-heading-is-refused-beside-a-set` hold its two refusals. `test_a_set_of_two_points_at_one_in_parallel_sub_section`. Result: held. Observes AC8.

## T5 Set Of One

`parallel-dispatch/a-set-of-one-target-publishes-as-an-inline-dispatch` and the three `a-target-holding-*` fixtures publish a set of one distinct target as `⇉` links to its file with no `In parallel` section. `test_a_set_of_one_target_publishes_as_an_inline_dispatch`. Result: held. Observes AC9.

## T6 Unit Tests

`src/tests` (`test_bundle.py`, `test_cli.py`, `test_candidate.py`, `test_closure.py`, `test_subst.py` and the remaining modules): 1681 passed.

## T7 Make Check

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`, after `git fetch origin engineering` and a merge of `origin/i10/e06/main` at `754a7ad2`. Corpus: 507 fixtures, 507 pass; conformance: 360 clauses, 0 declarations naming no clause; harness: 1286 passed; smoke, layout, tables, links, vocabulary, invocation and independence: ok.
