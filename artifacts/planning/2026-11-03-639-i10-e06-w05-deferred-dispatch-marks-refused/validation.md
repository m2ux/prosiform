# Validation

The checks W05 and W08's work items name, run against task branch `i10/e06/w05-deferred-dispatch-marks-refused` at `1f45185c`, on the design pinned at engineering commit `fa29043d1f9d56f9a4f4e4fdf107e311d15a1b93`.

## T1 Deferred Dispatch Refused

`dispatch/a-deferred-dispatch-is-refused`, `a-deferred-dispatch-in-a-dispatched-bundle-is-refused`, `a-deferred-dispatch-reached-through-a-chain-is-refused` and `parallel-dispatch/a-deferred-parallel-dispatch-is-refused` fail with `E_UNSUPPORTED_CONSTRUCT` naming the `¬⇉` or `¬⫽` link and publish nothing. `test_a_deferral_written_against_a_dispatch_mark_is_refused` in `src/tests/test_closure.py` and the two deferred-dispatch cases of `test_a_link_stating_no_one_operation_is_refused_and_publishes_nothing` in `src/tests/test_cli.py`. Result: held. Observes AC10.

## T2 Composition Under The Inline Mark

Every placement fixture of `composition/` writes `[↳ Title](p.md#s)` and publishes `[Title](#…)` at the contribution heading: destination sections, order, shared titles, sibling scopes, nested directives, presets and `subst`, budgets and cycles. `src/tests/test_composition.py` (`test_a_text_opening_with_the_composition_mark_is_a_directive`) and `src/tests/test_candidate.py`. Result: held. Observes AC14.

## T3 Deferred Composition

`composition/a-composed-contract-leaves-its-deferred-implementation-absent` and `a-deferred-directive-is-activated-by-the-run-its-line-names` build the destination section and publish `[↳ Title](path)` with its path rebased, from `[¬↳ Title](…)`. The four `a-deferral-whose-…` fixtures hold the preset refusal, and `a-section-composed-and-deferred-in-one-step-is-refused` the section both composed and deferred. `test_a_deferred_composition_is_written_with_its_marks_together` in `src/tests/test_cli.py`. Result: held. Observes AC15.

## T4 Arrow Labels Refused

`composition/an-arrow-label-is-refused`, `a-deferred-arrow-label-is-refused`, `a-supplementary-arrow-label-is-refused`, `an-entity-decoding-to-one-arrow-is-refused` and the blank and dispatch-mark variants fail with `E_UNSUPPORTED_CONSTRUCT` naming the link and pointing at `↳`; `a-dispatch-mark-written-against-the-composition-mark-is-refused` and `a-parallel-mark-written-against-the-composition-mark-is-refused` hold `⇉↳` and `⫽↳`. Each publishes nothing. `test_a_label_of_one_arrow_beside_its_marks_is_an_arrow_label` and `test_a_dispatch_mark_written_against_the_composition_mark_is_refused`. Result: held. Observes AC16.

## T5 Heading Of A Set Of One

`parallel-dispatch/a-parallel-link-in-a-heading-of-a-set-of-one-publishes-as-a-dispatch` publishes the heading with the dispatch mark and a link to its fragment. Before the fix the run failed with an internal error, `the candidate shows 'Check ⇉ the code' where the provenance records 'Check the code'`. Result: held.

## T6 Design Clauses

`make conformance` reports 360 clauses, 0 declarations naming no clause; `make vocabulary` accepts 3193 terms, with the glossary terms *dispatch sub-section* and *Prosiform section* removed and the manifests citing *Dispatch links*, *The run-pf line* and *Run-pf line*. Result: held.

## T7 Unit Tests

`src/tests`: 1731 passed.

## T8 Make Check

`make check` with `PROSIFORM_BUILD='uv run --project <worktree>/src --frozen pf'`, after `git fetch origin engineering`, with `origin/i10/e06/main` already merged. Corpus: 515 fixtures, 515 pass; harness, which carries the `section-composition` corpus test: 1294 passed; lint, format, types, smoke, layout, tables, links, vocabulary, invocation, conformance and independence: ok.
