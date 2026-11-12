# Test Results

Revision tested: `a006ee5fb` on `i15/e00/w03-routing-pairs-route-quietly`, based on `i15/e00/main` at `b3027cd1a`. Every check ran from the unit checkout with `PROSIFORM_BUILD` naming that checkout's build: `uv run --project <unit-checkout>/src --frozen pf`.

## T1 CLI Unit Tests

`uv run --frozen pytest tests/test_cli.py -k "routing or stand_in or names_a_key"` from `src/`: 13 passed.

- A used routing pair raises no diagnostic, and the bundle carries the routed material.
- A routing pair whose only link sits in a section the run did not select raises nothing, for a document key and for a section key.
- A routing pair no link of its document names warns `W_SUBST_UNUSED`, its message naming the declaring document and stating that no link the document writes names it; a section key whose section no link names warns the same way.
- An ordinary preset's pair beside a picked alternative warns `W_SUBST_USED` when a selected link uses it, and `W_SUBST_UNUSED` when its only link sits outside the selection.
- A key carrying a section is named by a link to that section only; a key naming a whole document is named by a link to it or to any section of it.

## T2 Inclusion Fixtures

`make corpus`, the four new `inclusion/` fixtures and the updated W01 fixture: each passes.

- `inclusion/a-used-routing-pair-raises-no-warning`: no diagnostics, exit 0.
- `inclusion/a-routing-pair-outside-the-selection-stays-quiet`: no diagnostics; the selection compiles one section and the route its other section names stays silent.
- `inclusion/a-stale-routing-pair-warns-unused`: one `W_SUBST_UNUSED` for `retired.md`, naming `work-kind.md`.
- `inclusion/a-stand-in-beside-an-alternative-still-warns`: one `W_SUBST_USED` for `checklist.md` resolved to `stub.md` at `work-kind.md:13:1`; the epic route raises nothing.
- `inclusion/a-link-picks-an-alternative-beside-an-ordinary-preset`: its `W_SUBST_USED` expectation removed; the remaining `W_PRESET_UNUSED` belongs to W02.

## T3 Full Check

`make check`: exit 0.

- `corpus check: 559 fixture(s), 559 pass, 0 fail, 0 awaited, 0 unexpected pass`.
- `make test` 1996 passed, `make harness` 996 passed; lint, format, typecheck, lock, smoke, layout, tables, links, vocabulary, invocation, conformance and independence each passed.
- Conformance: `0 declaration(s) naming no clause`. The new fixtures name clauses of the design the repository pins (`2f8d860e8`); W04 repins the design.
