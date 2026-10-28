# Change List — I05:E04:W06

The plan changes this delivery session applied and held, under the deliver-mode allowance.

## Applied

- **Re-prioritisation: E04 to In Review.** With W06 merged every row and criterion of [#352](https://github.com/m2ux/prosiform/issues/352) is complete, so its item on board 18 moved from In Progress to In Review.

The session also recorded delivery on #352 — W06 links [#370](https://github.com/m2ux/prosiform/pull/370), merged into `i05/e04/main` at `14d059d1`, with Done ticked, and AC6 is ticked — and opened the E04 review pull request [#372](https://github.com/m2ux/prosiform/pull/372), a draft from `i05/e04/main` into `main` linked to #352, as the user confirmed through the coordinator. Neither is a plan change.

The design choices below sit inside the brief's scope and change no issue.

- **Duplicate rule per document.** The guard reads a repeated `N. Action` step heading within one document, as the brief allows when a corpus-wide rule over-constrains. Four step headings legitimately repeat across modes — `1. Select` (deliver, sync), `3. Read the Evidence` and `6. Report` (advance, standup), `8. Report` (hoist, propose) — each its own bundle entry; a corpus-wide rule would fail on them.

## Held

- **AC6 scope: `example/` or `example/work-planner/`.** AC6 reads "a Markdown file under `example/`"; the guard reads `example/work-planner/`, the skill E04 converted. `example/my-skill/procedure.md` lines 7–8 still write two numbered steps and are the only lines under `example/` the guard's rules would fail. Converting them is an `example/` edit outside E04's planned scope. Recommended: keep the guard on `example/work-planner/` and read AC6 as met, since its tests plant the failing file under `example/` and `make check` fails on it; reword AC6 to `example/work-planner/` if the user wants the text exact. The alternative is a task converting my-skill's procedure and widening `TREE` to `example/`.
- **Placement of [#373](https://github.com/m2ux/prosiform/issues/373).** The arising CI-timeout issue is created as a standalone issue and not yet hoisted. Recommended: place it as a task in a new I05 epic for test reliability, under [I05 #327](https://github.com/m2ux/prosiform/issues/327).

## Integration Notes

- **Draft #325 (I01:E00)** and **I05:E01's base `i05/e01/main` (draft #353)** also edit `Makefile` and `checks.md`. W06 adds `steps` to the `.PHONY` and `check` lines, one target after `independence`, one row before `make check` in `checks.md`'s command table, and `make steps` to the two standard-library lists in the Makefile comment and `checks.md`. `checks/README.md` gains one table row and names `steps.py` in two lists, and "the first eleven" reads "the first twelve". Expect line conflicts on those lines when either merges.

## Deferred Debt and Arising Issues

- **Deferred debt.** None. Validation found no debt the unit defers.
- **Arising: [#373](https://github.com/m2ux/prosiform/issues/373) Handoff round-trip test times out intermittently on CI.** The Checks workflow failed on `i05/e04/main` at `aa826060` and on the W06 head `a869dfbf` when `test_handoff_round_trip` hit its 60-second limit bundling `modes/deliver-mode.md`; a rerun passed. Not W06's code. Placement held, above.
