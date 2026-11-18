# Test Results

Results for F22 at `e37af7839` on `f22-guide-compile-step`, cut from `main` at `4b0466803`, run on 2026-11-18 in the unit checkout.

## T1 Guide Clause

`pf` with no arguments prints, under "Compiling a link": "Run pf on a link in a bundle as written, quoted as one argument, from the directory pf compiled that bundle in, never on a ⇉ or ⫽ link." `invocation.md`, section Guide, states the step as `pf -o <folder> '<link>' [--pick <alternative>]` "run on a link in a bundle as written, quoted as one argument, though never by the agent on a `⇉` or `⫽` link". Each clause states what the agent runs, not what `pf` compiles. Against `main`, the diff of each text adds that clause alone; the guide's next sentence is rewrapped and otherwise unchanged. `test_the_guide_states_each_rule_an_agent_follows_a_bundle_by` in `src/tests/test_cli.py` and `fixtures/cli/informational-guide-response` in `make corpus` hold the new guide text and pass. Held.

## T2 Full Check

`make check`, with `PROSIFORM_BUILD` naming the unit checkout's `pf` and its `src/.venv/bin` first on `PATH`, exits 0: lock, lint, format, typecheck, `make test` (2270 passed), harness (1120 passed), corpus (681 fixtures, 681 pass), smoke, layout, tables, links, vocabulary, invocation (29 statements), conformance and independence. Held.
