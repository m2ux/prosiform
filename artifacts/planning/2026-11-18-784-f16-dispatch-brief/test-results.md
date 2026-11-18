# Test Results

Results for F16 at `7bcf48ac0` on `f16-dispatch-brief`, run on 2026-11-18 in the unit checkout, with `origin/engineering` carrying the design at `d3e39b6b5`.

## T1 Lifted Dispatch

`fixtures/dispatch-brief/a-dispatch-to-a-target-declaring-a-brief-is-lifted-into-a-sub-section`: a `⇉` link to a target whose `default` declares `brief: "#given"` publishes `### ⇉ Investigate` one level below its section, after the section's own content and before its child section, holding the Given body and then `[⇉ Investigate](investigate.bundle.md)`; the authored link is published as `[Investigate](#⇉-investigate)`. The target's bundle carries its Given section unchanged. Held in `make corpus`.

## T2 Named-Preset Brief

`fixtures/dispatch-brief/a-brief-in-a-named-preset-is-carried-by-the-dispatch-selecting-it`: a dispatch titled `briefed` is lifted with the brief, and a dispatch of the same target selecting no preset publishes in place with its mark, pointing at its own bundle file. Held in `make corpus`.

## T3 Diagram Dispatch

`fixtures/dispatch-brief/a-click-dispatch-to-a-target-declaring-a-brief-points-at-its-sub-section`: a Mermaid click on a node whose text opens with `⇉` is published as `click Intake href "#⇉-investigate"`, pointing at the lifted sub-section. Held in `make corpus`.

## T4 Picking Dispatch

`fixtures/dispatch-brief/a-picking-dispatch-carries-its-brief-above-its-pick-lines` places the brief in `⇉ Dispatch Pick` above the two pick lines. `a-picking-dispatch-whose-brief-an-alternative-routes-is-refused` (a brief link both alternatives route) and `a-picking-dispatch-to-an-alternative-declaring-a-brief-is-refused` each fail with `E_ALTERNATIVE_UNRESOLVED`, exit status 2, listing the alternatives, and publish nothing. Held in `make corpus`.

## T5 Dispatch Set

`fixtures/dispatch-brief/a-set-publishes-each-briefed-member-as-its-brief-and-its-line`: the `⫽ Dispatch Set` sub-section holds the briefed member's brief then its line, and the unbriefed member's bare line, in the set's order. `a-set-of-one-briefed-target-is-lifted-as-a-dispatch`: a set of one is lifted into `⇉ Investigate` as a `⇉` link is. Held in `make corpus`.

## T6 Brief Compilation

`fixtures/dispatch-brief/a-brief-s-links-are-followed-into-the-dispatching-bundle`: the brief's link to `rules.md#tests` joins the dispatching bundle and points at `#tests` there, its child heading nests at level 4 beneath the level-3 sub-section, and the target's bundle carries the section unchanged. Held in `make corpus`.

## T7 Refusals and Preset Rules

`a-lifted-heading-equal-to-an-authored-heading-is-refused` and `two-briefed-dispatches-of-one-text-and-two-selections-are-refused` fail with `E_HEADING_COLLISION`; `a-brief-naming-another-document-is-refused` fails with `E_INVALID_CONVERSION_METADATA` naming `prosiform.default.brief`; `a-brief-naming-a-missing-heading-is-refused` fails with `E_TARGET_NOT_FOUND` naming `investigate.md#missing` and the route through the dispatch. Unit tests: `src/tests/test_brief.py` (default and named-preset layering, two selected briefs refused as `E_INVALID_USAGE`, the composing reference, an alternative's brief on a pick unresolved) and the two brief tests in `src/tests/test_metadata.py`. Held.

## T8 Documented Rule

A reading of `docs/dispatch.md` (section Briefs, The guide, Generated headings), `docs/sources.md` (the `brief` key), `invocation.md`, the guide `pf` prints and the design's **Dispatch briefs**, **`brief` names a section of its own document** and **Generated heading collisions**: each states the brief, where its sub-section stands, that it compiles as a `↳` composition, and the guide states that text above a `⇉` line in the sub-section a link points at is the bundle's brief, done before the bundle is handed on. Held.

## T9 Eval Unit Tests

`make eval-harness`: 849 passed. `test_score.py` holds `premature_dispatch`: `test_a_sub_agent_started_before_its_brief_was_acted_on_is_premature` fails a session whose sub-agent copied no brief value, and `test_a_sub_agent_that_found_its_brief_written_passes` passes one that did. `test_workflow.py` holds `test_the_dispatch_brief_forms_differ_only_in_the_brief` and `test_a_brief_precedes_its_dispatch_and_a_composition_follows_it`, which bundles both forms with this build. Held.

## T10 Live Run

Not run. The runbook's Dispatch-Brief Run section states a cost cap awaiting the user's approval.

## T11 Full Check

`make check` with `PROSIFORM_BUILD` naming the worktree's `pf` exits 0: lint, format, typecheck, `make test` (2257 passed), harness (1089 passed), corpus (650 fixtures, 650 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
