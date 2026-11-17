# Test Results

Results for F14 at `4bbb3e4b1` on `f14-unrouted-deferrals`, run on 2026-11-17 in the unit checkout.

## T1 Deferred Unrouted Section

`fixtures/deferral/a-deferral-naming-no-alternative-to-a-section-no-alternative-routes-publishes`: a deferred link with no title names the Hand-off section of a document whose two alternatives route `body.md`, which only its Steps section links, and state no `group` pair. The run publishes at exit status 0 with no diagnostic, the link carried as `[hand-off](stage.md#hand-off)`. The build of `origin/main` at `470a18590` fails it with `E_UNSUPPORTED_CONSTRUCT`. Held.

## T2 Deferred Directive to an Unrouted Section

`fixtures/deferral/a-deferred-directive-naming-no-alternative-to-a-section-no-alternative-routes-publishes`: a deferred composition directive with no title names the same Hand-off section. The run publishes at exit status 0 with no diagnostic, the deferred composition line carried as `[↳ Hand-off](stage.md#hand-off)`. The build of `origin/main` at `470a18590` fails it with `E_UNSUPPORTED_CONSTRUCT`. Held.

## T3 Deferred Routed Section

`fixtures/deferral/a-deferral-naming-no-alternative-to-a-section-writing-a-routed-link-is-refused`: a deferred link titled with the ordinary preset `checks` alone names the Steps section, which links `body.md`, a key both alternatives route. The run fails with `E_UNSUPPORTED_CONSTRUCT` and exit status 1, naming the link, its source location and the alternatives, and publishes nothing. Held.

## T4 Deferral Unit Tests

In `test_cli.py`:

- `test_a_deferral_naming_no_alternative_to_unrouted_content_publishes`: a `¬` link and a `¬↳` directive, each with no title and with the ordinary preset `checks`, naming a section that writes no routed link, publish as authored.
- `test_an_entry_title_naming_the_targets_alternative_is_no_deferrals_pick`: an entry title naming the target's alternative, which the published deferral leaves out, does not satisfy the check.
- `test_a_deferral_whose_later_run_fails_otherwise_needs_no_pick`: a later run failing whatever is picked publishes the deferral.
- `test_a_deferral_whose_later_run_fails_for_want_of_a_pick_is_refused`: a later run failing unpicked on the unrouted body, which a pick routes past, refuses the deferral.
- `test_a_deferral_stating_no_one_pick_is_refused` still refuses a deferral naming no alternative to a whole document writing a routed link.

Held.

## T5 Documented Rule

A reading of `docs/references.md`, section "The pick token", and the design's **The pick token** under Link classification: each states that a deferral names neither an alternative nor `?` only where the later run, compiling the published link as its entry, needs no alternative in force, as **Exactly one alternative** states, that it is refused where one is needed, and that a later run failing for another reason whatever the deferral picks reports that failure itself. The design's **Exactly one alternative** names the deferral case by what its later run carries, and its Alternatives fixture row lists the five fixtures. Held.

## T6 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf` and `origin/engineering` carrying the design change, exits 0: lint, format, typecheck, `make test` (2185 passed), harness (1071 passed), corpus (632 fixtures, 632 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T7 Later-Run Content Fixtures

`fixtures/deferral/a-deferral-naming-no-alternative-to-a-section-linking-a-routed-section-is-refused`: the deferred Hand-off section writes no routed link but links the Steps section of its own document, which does, so the later run carries Steps and needs a pick; the run fails with `E_UNSUPPORTED_CONSTRUCT` and exit status 1. `fixtures/deferral/a-deferral-naming-no-alternative-to-a-section-picking-an-alternative-of-its-own-publishes`: the deferred section picks `alpha` by its own link, so the later run finds it in force, and the run publishes at exit status 0. At `fb36680e2` the first published and its later run failed, and the second was refused though its later run compiles; the agent review found both. Held.
