# Test Results

Results for F11 at `580572a5d` on `f11-unrouted-sections`, run on 2026-11-17 in the unit checkout.

## T1 Composed Unrouted Section

`fixtures/composition/a-composed-section-no-alternative-routes-needs-no-pick`: a directive with no title composes the Hand-off section of a document whose two alternatives route `body.md`, which only its uncomposed Steps section links, and state no `group` pair. The run publishes at exit status 0 with no diagnostic. `pf` 0.25.0 fails it with `E_ALTERNATIVE_UNRESOLVED`. Held.

## T2 Linked Unrouted Section

`fixtures/inclusion/a-link-to-a-section-no-alternative-routes-needs-no-pick`: a plain link with no title selects the same Hand-off section. The run publishes at exit status 0 with no diagnostic. `pf` 0.25.0 fails it with `E_ALTERNATIVE_UNRESOLVED`. Held.

## T3 Routed Section

`fixtures/inclusion/a-section-writing-a-routed-link-needs-a-pick`: a plain link with no title selects the Steps section, which links `body.md`, a key both alternatives route. The run fails with `E_ALTERNATIVE_UNRESOLVED` and exit status 2, listing each alternative beside its choice line. Held.

## T4 Grouping Alternative

`fixtures/inclusion/a-section-of-a-document-whose-alternative-states-a-group-needs-a-pick`: a plain link with no title selects a Hand-off section writing no link, from a document whose `alpha` alternative states a `group` pair. The run fails with `E_ALTERNATIVE_UNRESOLVED` and exit status 2, listing both alternatives. Held.

## T5 Folder Preamble

`fixtures/inclusion/a-folder-preamble-writing-a-routed-link-needs-a-pick`: a plain link with no title selects a Hand-off section writing no link, from a document in a subfolder whose `default` group pair places its title and introduction in the folder's preamble group. The introduction links `body.md`, a key both alternatives route, so the run fails with `E_ALTERNATIVE_UNRESOLVED` and exit status 2. At `1b9e706d3` the run published that link unrouted at exit status 0; the agent review found it. Held.

## T6 Routing Unit Tests

`test_selection.py::test_an_alternative_changes_content_whose_links_name_its_key`: a whole-document key named by a section's link, a section key named by its link, a section key the link does not name, a key naming another document's section, a section writing no link, and a whole document selected, each give the expected reading. `test_selection.py::test_an_alternative_stating_a_group_pair_changes_any_content`: a `group` pair changes a section writing no link. `test_selection.py::test_an_introduction_a_folder_preamble_carries_is_selected_content`: an introduction's routed link counts for a grouped document in a subfolder, and not for one at the top level or one with no group pair. Held.

## T7 Documented Rule

A reading of `docs/selection.md`, section "Presets in force", and the design's **Exactly one alternative** under Presets: each states that several alternatives in force fail, that one is needed where an alternative states a `group` pair or a `subst` pair whose key a link in the selected content names, and that other content compiles under `default` and the ordinary presets its references select. `docs/glossary.md`, `docs/validation.md`, `invocation.md`, `fixtures/README.md` and the design's failure table, exit-status table and Alternatives fixture row state the same bound. Held.

## T8 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf` and `origin/engineering` carrying the design change, exits 0: lint, format, typecheck, `make test` (2147 passed), harness (1059 passed), corpus (620 fixtures, 620 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## Limitations

- A deferral naming a document that declares alternatives must still name one or carry `?` when it is published, whatever section it names. The issue scopes compositions and plain links, so the agent review's finding on it is held for the owner.
