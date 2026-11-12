# Test Results

Revision tested: `297b82a3f` on `i15/e00/w02-exactly-one-alternative-in`, based on `i15/e00/main` at `c6a8ce7da`, which carries W03. Every check ran from the unit checkout with `PROSIFORM_BUILD` naming that checkout's build: `uv run --project <unit-checkout>/src --frozen pf`.

## T1 Unit Tests

`make test`: the new cases in `test_cli.py` and `test_selection.py` pass.

- `test_selection.py`: the alternatives in force are every reference's picks, in declaration order; no title, an unknown name, `?`, an ordinary preset and `default` pick none; the failure lists each alternative beside its choice line, padded to the longest name, in declaration order, with exit status 2 and the `--presets` remedy.
- `test_cli.py`: no pick, an unknown name, an ordinary preset alone and `?` each refuse with `E_ALTERNATIVE_UNRESOLVED`, publishing nothing; an entry with no `--presets` is refused, and one naming an alternative compiles its route; two links picking apart are refused before their pairs are compared; a link with no title beside a pick leaves one in force; a dispatched bundle counts its own references, so each bundle's pick compiles; only the ordinary preset warns `W_PRESET_UNUSED`; `-C` lists the code.

## T2 Inclusion Fixtures

`make corpus`: the six new `inclusion/` fixtures and the updated W01 fixture pass.

- `no-pick-of-an-alternative-fails`, `an-unknown-alternative-name-fails`, `two-alternatives-in-one-title-fail`, `two-links-picking-different-alternatives-fail` and `a-diagram-link-alone-reaching-alternatives-fails`: exit 2 and one `E_ALTERNATIVE_UNRESOLVED` naming `work-kind.md` as `source`, its message carrying the three alternatives with their choice lines in declaration order.
- `an-unpicked-alternative-raises-no-warning`: exit 0; the unpicked `initiative` and `task` alternatives raise nothing, and the ordinary `checks` preset warns `W_PRESET_UNUSED`.
- `a-link-picks-an-alternative-beside-an-ordinary-preset`: its `W_PRESET_UNUSED` expectation for `initiative` removed beside W03's removal of `W_SUBST_USED`, so it expects no diagnostic.

## T3 Full Check

`make check`: exit 0.

- `corpus check: 565 fixture(s), 565 pass, 0 fail, 0 awaited, 0 unexpected pass`.
- `make test` 2012 passed, `make harness` 1004 passed; lint, format, typecheck, lock, smoke, layout, tables, links, vocabulary, invocation, conformance and independence each passed.
- The README pins the design at `c04f5d8e6`, which declares `E_ALTERNATIVE_UNRESOLVED`: the harness holds the schema's error catalogue to the pinned design's codes, and the vocabulary check holds the glossary to its marked terms. Conformance: `0 declaration(s) naming no clause`, `0 reported code(s) the contract declares nowhere`.
