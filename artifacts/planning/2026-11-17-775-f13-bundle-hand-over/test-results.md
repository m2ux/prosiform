# Test Results

Results for F13 at `cc9505fe6` on `f13-bundle-hand-over`, based on `main` at `bd0f5c6bb`, run on 2026-11-17 in the unit checkout.

## T1 Hand-Over by Path

`test_cli.py::test_the_guide_hands_a_bundle_over_by_the_path_of_its_file`: the guide `pf` prints with no arguments says a `⇉` bundle is handed on by giving a sub-agent the path of its file, which it reads there, and that each member of a dispatch set goes to its own sub-agent as its file path. `cli/informational-guide-response` holds the same wording against the built `pf`. Held.

## T2 The Dispatching Step's Inputs

`test_cli.py::test_the_guide_states_a_sub_agents_inputs_are_the_dispatching_steps`: the guide states "with the inputs the dispatching step states as given" in both the `⇉` and the `⫽` entries, and does not carry "the step that led there". Held.

## T3 Documentation

A reading of `docs/dispatch.md` (sections "What it looks like" and "The guide"), `invocation.md` (section "Guide") and the design (the guide's preamble and its text) finds each stating that a bundle is handed over by its file's path, with the inputs the dispatching step states as given. `docs/glossary.md` carries the same in its "guide" row. Held.

## T4 Full Check

`make check` with `PROSIFORM_BUILD` naming the worktree's `pf`: exit 0. Test 2157 passed, harness 1060 passed, corpus 621 of 621, and lock-check, lint, format, typecheck, smoke, layout, tables, links, vocabulary, invocation, conformance and independence each ok. Held.
