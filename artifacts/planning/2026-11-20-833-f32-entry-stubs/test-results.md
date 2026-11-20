# Test Results

Results for F32 at `f504c8d30` on `f32-entry-stubs`, run on 2026-11-20 in the unit checkout.

## T1 Two Dispatches Below

`inclusion/an-entry-stub-redirects-a-link-two-dispatches-below`: the entry declares `recorded` and dispatches `outer.md`, which dispatches `stage.md`; `stage.bundle.md` carries "The recorded review a trial reads." and the run warns `W_SUBST_USED` at `stage.md:8`. Held.

## T2 Unselected Stub

`inclusion/a-run-naming-no-stub-raises-no-warning-for-it`: `pf entry.md` publishes the stage with its live review and no diagnostic. Held.

## T3 Stub Below the Entry

`inclusion/a-stub-a-dispatched-stage-declares-fails`: `E_STUB_OFF_ENTRY`, exit 1, naming `'recorded'` and `stage.md`, nothing published; `test_a_stub_below_the_entry_is_refused` in `make test`. Held.

## T4 Precedence

- `inclusion/an-entry-stub-holds-over-a-stage-s-own-pair`: the stage's `default` maps `review.md` to `draft-review.md`; the bundle carries the entry's recorded review, and the stage's pair warns `W_SUBST_UNUSED`.
- `inclusion/an-alternative-routes-beside-an-entry-stub`: the stage's `strict` alternative routes `rules.md` to `strict-rules.md` silently while the entry's stub redirects `review.md`.
- `test_subst.py`: an entry stub redirects another document's link, holds over a document's pair for one key, and a document's section key holds over an entry's document key.

Held.

## T5 Warnings

- `inclusion/an-entry-stub-no-link-uses-warns`: `W_SUBST_USED` for `review.md`, `W_SUBST_UNUSED` for `notes.md` naming `prosiform.recorded` in `entry.md`.
- `mock/a-stubs-pair-warns-once-across-bundles`: one `W_SUBST_USED` for a pair two bundles use.

Held.

## T6 Deferral

`deferral/a-deferral-carries-no-pair-of-the-entry`: `[¬ review the stage](stage.md "checks")` publishes `[review the stage](../stage.md "checks, recorded")`; the entry's pair, used by no link of the run, warns `W_SUBST_UNUSED`. Held.

## T7 Documents

`docs/selection.md` owns the rule under **The entry declares the run's stubs**, its deferral bullet and the substitution mapping; `docs/sources.md`, `docs/glossary.md` and `invocation.md` name it; `docs/validation.md` lists `E_STUB_OFF_ENTRY`; the design states it under Stubs, the substitution mapping and Metadata failures, pinned at `30b8d24b2`. Held.

## T8 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lint, format, typecheck, `make test` (2290 passed), harness (1148 passed), corpus (703 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T9 Stand-ins

`inclusion/a-stand-in-links-the-material-it-stands-in-for`: the entry's stub redirects the stage's review link to `recorded-review.md`, whose own link to `review.md#rules` reaches the live Rules section. `test_subst.py`: a stand-in keeps every other stub, and a section substitute in its key's own document redirects that document's links. Held.
