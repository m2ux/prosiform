# Test Results

Results for F23 at `5a11be68b` on `f23-alternative-diagnostics`, run on 2026-11-18 in the unit checkout.

## T1 Agreeing Default Pair

`fixtures/inclusion/a-default-pair-an-alternative-agrees-with-warns`: `stage.md` declares `default: {subst: [{body.md: alpha-body.md}]}` and an `alpha` alternative stating the same pair, and its Given section links `body.md#body`. `[Given](stage.md#given "alpha")` publishes the alpha body and warns `W_SUBST_USED` at `stage.md:16`, with source `body.md#body` and resolved `alpha-body.md#body`. The build of `origin/main` at `4b0466803` exits 0 with no diagnostic. Held.

## T2 Picking Dispatch Remedy

`fixtures/dispatch-brief/a-picking-dispatch-whose-brief-an-alternative-routes-is-refused`: `[⇉ Stage](stage.md "?")`, whose brief `#given` links `body.md#body`, which alternatives `Task` and `Epic` each route, fails with `E_ALTERNATIVE_UNRESOLVED` and exit status 2, naming the brief `stage.md#given` as its reference, the chain `guide.md`, `stage.md#given` and the location `guide.md:8:1`, and publishes nothing. The corpus manifest declares no remedy field, so `test_a_dispatch_whose_brief_an_alternative_routes_is_remedied_by_its_pick` in `test_cli.py` holds the remedy text on the same tree: the `?` dispatch's remedy is "write the brief 'stage.md#given' so it compiles with no alternative in force, since the picking dispatch carrying it leaves the pick to its agent", and a plain dispatch keeps the remedy naming the alternative in its title. The build of `origin/main` at `4b0466803` remedies the `?` dispatch with "name the alternative that fits your task in the title of the directive or dispatch placing this copy". Held.

## T3 Full Check

`make check`, with `src/.venv/bin` first on `PATH` and `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2272 passed), harness (1121 passed), corpus (682 fixtures, 682 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
