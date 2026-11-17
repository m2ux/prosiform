# Test Results

Results for F14 at `fb36680e2` on `f14-unrouted-deferrals`, run on 2026-11-17 in the unit checkout.

## T1 Deferred Unrouted Section

`fixtures/deferral/a-deferral-naming-no-alternative-to-a-section-no-alternative-routes-publishes`: a deferred link with no title names the Hand-off section of a document whose two alternatives route `body.md`, which only its Steps section links, and state no `group` pair. The run publishes at exit status 0 with no diagnostic, the link carried as `[hand-off](stage.md#hand-off)`. The build of `origin/main` at `470a18590` fails it with `E_UNSUPPORTED_CONSTRUCT`. Held.

## T2 Deferred Directive to an Unrouted Section

`fixtures/deferral/a-deferred-directive-naming-no-alternative-to-a-section-no-alternative-routes-publishes`: a deferred composition directive with no title names the same Hand-off section. The run publishes at exit status 0 with no diagnostic, the deferred composition line carried as `[↳ Hand-off](stage.md#hand-off)`. The build of `origin/main` at `470a18590` fails it with `E_UNSUPPORTED_CONSTRUCT`. Held.

## T3 Deferred Routed Section

`fixtures/deferral/a-deferral-naming-no-alternative-to-a-section-writing-a-routed-link-is-refused`: a deferred link with no title names the Steps section, which links `body.md`, a key both alternatives route. The run fails with `E_UNSUPPORTED_CONSTRUCT` and exit status 1, naming the link, its source location and the alternatives, and publishes nothing. Held.

## T4 Deferral Unit Test

`test_cli.py::test_a_deferral_naming_no_alternative_to_unrouted_content_publishes`: a `¬` link and a `¬↳` directive, each with no title and with the ordinary preset `checks`, naming a section that writes no routed link, publish as authored. `test_a_deferral_stating_no_one_pick_is_refused` still refuses a deferral naming no alternative to a whole document writing a routed link. Held.

## T5 Documented Rule

A reading of `docs/references.md`, section "The pick token", and the design's **The pick token** under Link classification: each states that a deferral names neither an alternative nor `?` only where its target compiles with no alternative in force, as **Exactly one alternative** states, and is refused where one is needed. The design's **Exactly one alternative** names a deferral among the references reaching unrouted content, and its Alternatives fixture row lists the three fixtures. Held.

## T6 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf` and `origin/engineering` carrying the design change, exits 0: lint, format, typecheck, `make test` (2182 passed), harness (1069 passed), corpus (630 fixtures, 630 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
