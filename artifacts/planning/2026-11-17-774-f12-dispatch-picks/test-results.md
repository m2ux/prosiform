# Test Results

Results for F12 at `90b275103` on `f12-dispatch-picks`, run on 2026-11-17 in the unit checkout, with `PROSIFORM_BUILD` naming the worktree's built `pf`.

## T1 A Bundle for Each Alternative

`fixtures/dispatch/a-dispatch-carrying-the-pick-token-lists-a-bundle-for-each-alternative` in `make corpus`: `[⇉ Populate the body](work-kind.md "?")` against a target declaring `task` then `epic`, each routing `body.md` to its own body, publishes the entry's bundle and one bundle for each alternative, each carrying its alternative's body. The same source fails with `E_UNSUPPORTED_CONSTRUCT` on `pf` 0.25.0. Held.

## T2 The Listing

The same fixture's `guide.bundle.md`: the link reads `[Populate the body](#⇉-dispatch-pick "?")` and the section gains `### ⇉ Dispatch Pick` holding one `⇉` line for each alternative, `task` before `epic` as declared, each followed by an em dash and its choice line. `fixtures/dispatch/a-dispatch-carrying-the-pick-token-beside-a-preset-selects-it-in-each-bundle` shows `"checks, ?"` selecting the ordinary `checks` preset in both alternatives' bundles, the title carried as authored. Held.

## T3 The Guide

`test_cli.py::test_the_guide_states_each_rule_an_agent_follows_a_bundle_by` in `make test`: the guide `pf` prints with no arguments states that `?` on a `⇉` link points at the sub-section headed `⇉ Dispatch Pick`, which lists one `⇉` line for each alternative beside its choice line, and that its reader hands on the one bundle whose choice line fits its work. Held.

## T4 A Set Carrying the Pick Token

`fixtures/dispatch/a-parallel-dispatch-carrying-the-pick-token-is-refused` in `make corpus`: `[⫽ Populate the body](work-kind.md "?")` fails with `E_UNSUPPORTED_CONSTRUCT`, naming the link, and publishes nothing. `test_cli.py::test_a_parallel_click_carrying_the_pick_token_is_refused` holds the same for a click. Held.

## T5 The Documents

A reading of `docs/dispatch.md` (section "Where the links point"), `docs/references.md` (section "The pick token") and the design on `engineering` (**Dispatch links**, **The pick token**, **The agent's pick** and the guide text under **Guide**): each states that a `⇉` link carrying `?` compiles one bundle for each alternative, lists them beside their choice lines in a dispatch-pick sub-section for the dispatching agent to hand on one, and that a `⫽` link carrying `?` is refused. Held.

## T6 Unit Tests

`test_cli.py`: `test_a_dispatch_carrying_the_pick_token_lists_a_bundle_for_each_alternative` for `?`, `checks, ?` and `Checks,?`; `test_a_dispatching_click_carrying_the_pick_token_points_at_its_pick`; `test_a_dispatch_naming_an_alternative_beside_the_pick_token_is_refused`; `test_a_dispatch_carrying_the_pick_token_to_no_alternatives_is_refused`; `test_a_picking_dispatch_in_a_level_six_section_is_refused`; `test_an_authored_heading_equal_to_the_dispatch_pick_is_refused`; `test_a_picking_dispatch_of_its_own_document_warns_once`, which warns once for each alternative on `07efdb3ef`. Held.

## T7 Full Check

`make check` exits 0: lock-check, lint, format, typecheck, `make test` (2145 passed), harness (1055 passed), corpus (616 fixtures, 616 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## Limitations

- `make eval-harness` was not run: no eval workflow writes a `⇉` link carrying `?`, and `make check` does not run it.
- The README's design pin stays at `005b0ff1d`, so `make conformance` and `make vocabulary` read the design without this unit's change; the fixtures cite clauses that design already names.
