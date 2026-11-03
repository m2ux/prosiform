# I09:E05 W34 Validation — November 2026

> Validation evidence · Created 2026-11-03

## Executive Summary

Each check the [W34 work item](../2026-11-02-463-i09-grouping-and-composition/e05/w34.md) names, run against branch `i09/e05/w34-place-a-second-group` with `PROSIFORM_BUILD` naming that worktree's build.

## AC38

- **T1 — `inclusion/two-documents-placing-one-document-in-two-groups`.**
  Alpha and Beta each link `notice.md`, Alpha under its default pair `{messages: 1}`, Beta from its `Announce` section under `{announcements: 1}`. The bundle carries `## Messages` inside `# Alpha` and `## Announcements` inside `# Beta`. The build before this change emits both groups inside `# Alpha`, so the fixture fails against it.
- **T3 — `test_group_pairs_place_each_file_from_the_leaves_up`.**
  Asserts Notify's first occurrence under `Delivery › Messages` and its second under `Announce › Announcements`. Run against the previous `src/prosiform/cli.py`, the test fails at the second assertion.
- **T4 — `test_each_scenario_path_is_the_walk_its_bundle_states` for `two-presets-one-document`.**
  The path `Scope, Stage, Announce, Notify, Release` is the walk the new bundle states: Announce's Notify link resolves to the Notify heading inside Announce's Announcements group.

## Regression

- **T2 — `grouping/a-group-its-own-member-places-stands-at-the-top-level` and `inclusion/one-document-two-presets`.**
  Beta, itself an Announcements member, places the notice as that group's first member, so the group stands at the top level rather than inside itself. `inclusion/one-document-two-presets` passes unchanged: both references are the entry document's, so both groups stand inside `# Guide`.

## make check

- **T5 — `make check` with `PROSIFORM_BUILD` set.**
  Passed at `cfc06e72` (exit 0): lint, format, types, 1663 unit tests, 1253 harness tests, corpus 504 of 504, smoke, layout, tables, links, vocabulary, invocation, conformance and independence. CI's Checks job passed on the same head ([run](https://github.com/m2ux/prosiform/actions/runs/41578276823/job/125726793164)).
- **Two defects the first run found, fixed on this branch.**
  The independence check refused `Announce` and `Announcements` written bare in the two new manifests' descriptions, as terms the contract does not name; both are now code spans. An interrupted local corpus run had left a run folder inside `inclusion/an-empty-block-declares/source`, which a commit swept in; the next commit removes it.
