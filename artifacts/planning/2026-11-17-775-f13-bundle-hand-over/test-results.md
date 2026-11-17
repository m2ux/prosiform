# Test Results

Results for F13 at `58b34a541` on `f13-bundle-hand-over`, run on 2026-11-17 in the unit checkout.

## T1 Hand-Over by Path

`test_cli.py::test_the_guide_hands_a_bundle_over_by_the_path_of_its_file`: the guide `pf` prints with no arguments says a `⇉` bundle is handed on by giving a sub-agent the path of its file, which it reads there, and that each member of a dispatch set goes to its own sub-agent as its file path. `cli/informational-guide-response` holds the same wording against the built `pf`. Held.

## T2 The Dispatching Step's Inputs

`test_cli.py::test_the_guide_states_a_sub_agents_inputs_are_the_dispatching_steps`: the guide states "with the inputs the dispatching step states as given" in both the `⇉` and the `⫽` entries, and no longer carries "the step that led there". Held.

## T3 A Bundle Linking Nothing Outside It

Fixture `prosiform/a-bundle-linking-nothing-outside-it-opens-with-its-content`: a bundle whose links resolve inside it or name a remote address opens on `# Guide`, with no `§ Instructions` heading and no run-pf line. `test_bundle.py::test_a_link_naming_no_local_document_needs_no_run_pf_line` holds the same for a remote Markdown address, an image of a `.md` file, a non-Markdown resource and a fragment, and `test_bundle.py::test_a_bundle_linking_nothing_outside_it_opens_with_its_content` for a bundled dependency. 380 committed bundles across the corpus and the project-lifecycle example that link nothing outside them drop the instruction group, and the corpus holds each byte for byte. Held.

## T4 A Bundle Linking Out

Fixture `prosiform/a-bundle-linking-an-undeclared-document-opens-with-the-run-pf-line`: a bundle whose one link names a document declaring nothing opens on the instruction heading and the run-pf line. The existing fixtures hold the other kinds: `prosiform/a-bundle-using-the-dispatch-operator-carries-no-protocol` (`⇉`), `prosiform/a-bundle-using-the-parallel-mark-carries-no-protocol` (`⫽`), `dispatch/a-deferred-directive-in-a-dispatched-bundle-opens-with-the-run-pf-line` (a deferred `↳` line), `dispatch/a-plain-deferral-in-a-dispatched-bundle-opens-with-the-run-pf-line` (a deferral) and `deferral/a-mode-publishes-its-kind-router-link-with-the-pick-token` (the pick token). `test_bundle.py::test_a_link_to_a_document_outside_the_bundle_keeps_the_run_pf_line` covers an undeclared, a missing and a deferred document, a deferred composition directive and a pick-token deferral. Held.

## T5 Documentation

A reading of `docs/dispatch.md` (sections "What it looks like", "The guide" and "The run-pf line"), `invocation.md` (section "Guide") and the design (the guide's text and its preamble, and "Dispatch links", "The instruction heading", "The run-pf line", "Clean Markdown" and the "Run-pf line" fixture clause) finds each stating that a bundle is handed over by its file's path with the inputs the dispatching step states as given, and that only a bundle linking a document outside it opens with the run-pf line. `docs/glossary.md`, `docs/composition.md`, `docs/destinations.md`, `fixtures/README.md` and the eval README carry the same, and the drawings are redrawn with `make examples`. Held.

## T6 Eval Harness

`make eval-harness`: 815 passed. Its compiled-form check holds each bundle to opening with the run-pf line exactly when it links a document outside it. `make check` does not run it. Held.

## T7 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's installed `pf`, exits 0: lock, lint, format, typecheck, `make test` (2147 passed), harness (1055 passed), corpus (616 fixtures, 616 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## Limitations

- A link to a remote address that names a Markdown file is not counted as one outside the bundle: no `pf` run compiles it, so it asks nothing of the guide.
