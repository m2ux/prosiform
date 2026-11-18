# Test Results

Results for F23 at `2a2f6fd15` on `f23-alternative-diagnostics`, run on 2026-11-18 in the unit checkout.

## T1 Agreeing Default Pair

`fixtures/inclusion/a-default-pair-an-alternative-agrees-with-warns`: `stage.md` declares `default: {subst: [{body.md: alpha-body.md}]}` and an `alpha` alternative stating the same pair, and its Given section links `body.md#body`. `[Given](stage.md#given "alpha")` publishes the alpha body and warns `W_SUBST_USED` at `stage.md:16`, with source `body.md#body` and resolved `alpha-body.md#body`. `test_a_default_pair_an_alternative_agrees_with_warns_in_a_copy` in `test_cli.py` holds the same warning for a composed copy, `[↳ Given](stage.md#given "alpha")`. The build of `origin/main` at `4b0466803` exits 0 on the fixture's tree with no diagnostic. Held.

## T2 Picking Dispatch Remedy

`fixtures/dispatch-brief/a-picking-dispatch-whose-brief-an-alternative-routes-is-refused`: `[⇉ Stage](stage.md "?")`, whose brief `#given` links `body.md#body`, which alternatives `Task` and `Epic` each route, fails with `E_ALTERNATIVE_UNRESOLVED` and exit status 2, naming the brief `stage.md#given` as its reference, the chain `guide.md`, `stage.md#given` and the location `guide.md:8:1`, and publishes nothing.

The corpus manifest declares no remedy field, so `test_cli.py` holds the remedy text:

- `test_a_copy_an_alternative_routes_is_remedied_at_the_link_placing_it`: the `?` dispatch's remedy is "write the brief 'stage.md#given' so it compiles with no alternative in force, since the picking dispatch carrying it leaves the pick to its agent", also where an unrouted directive of the same tags is written first; a plain dispatch keeps the remedy naming the alternative in its title, and of two directives the routed one is named.
- `test_a_picking_dispatch_s_brief_fails_at_the_picking_dispatch`: a plain dispatch of the same tags written first leaves the failure at the picking dispatch, `guide.md:9`.

The build of `origin/main` at `4b0466803` remedies the `?` dispatch with "name the alternative that fits your task in the title of the directive or dispatch placing this copy", and places the failure at the plain dispatch. Held.

## T3 Full Check

`make check`, with `src/.venv/bin` first on `PATH` and `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2276 passed), harness (1122 passed), corpus (683 fixtures, 683 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T4 Alternative Naming a Brief

`fixtures/dispatch-brief/a-picking-dispatch-to-an-alternative-declaring-a-brief-is-refused`, where the `Task` alternative of `stage.md` names a brief, and `fixtures/dispatch-brief/a-picking-dispatch-whose-alternative-overrides-the-default-brief-is-refused`, where `default` names one brief and the `Epic` alternative another: `[⇉ Stage](stage.md "?")` fails with `E_ALTERNATIVE_UNRESOLVED` and exit status 2, naming the dispatch `stage.md` as its reference, the chain `guide.md`, `stage.md` and the dispatch's line as its location, and publishes nothing. `test_a_picking_dispatch_to_an_alternative_naming_a_brief_is_unresolved` in `test_brief.py` holds the remedy: "declare the brief in default or an ordinary preset, so it does not vary by alternative, since the picking dispatch carrying it leaves the pick to its agent". The build of `origin/main` at `4b0466803` names no reference or location and remedies with "name the alternative that fits your task in the title or tooltip of each link reaching it, a link entry's among them". Held.
