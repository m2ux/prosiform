# I05:E03:W03+W04 Change List

The plan changes this delivery session made, and those it held.

## Applied

- **User-confirmed design change, I05:E03 W03.** A run publishes its whole bundle set into a sub-folder of the `-o` folder named for its entry, built in a temporary sibling folder and swapped in whole, replacing W02's per-file rename stage. Confirmed by the user through the coordinator on 2026-10-28, not taken under the allowance. It reached `cli.py` publication and its tests, the corpus runner, smoke run and diagram renderer, `invocation.md`, the glossary, the design's CLI, Automatic output names and Publication clauses, and the epic record's Output section and Decisions.
- **Criteria reworded with it, I05:E03.** #351's AC1 and AC5 state the run folder; both stay ticked, held by `test_cli.py` and the `fixtures/cli` runs under the new layout. AC4 and AC6 state no layout and are unchanged.
- **Folded work, I05:E03 W03.** A run folder holding a captured source is invalid usage, replacing the check on a bundle path naming one; `cli/output-naming-a-dependency-source` becomes `cli/run-folder-holding-a-dependency-source`.
- **Folded work, I05:E03 W03.** `rewriting/a-state-diagram-click-in-each-form` runs with `-o ..`: its entry `states.md` stands beside `states/`, which would otherwise be its run folder.
- **Folded work, I05:E03 W03.** Two bundles of one run deriving one file name are refused with `E_PUBLICATION_FAILED` rather than one overwriting the other.
- **Folded work, I05:E03 W04.** The design's "A withheld link's destination" clause is renamed "A deferred link's destination", since a dispatched link no longer carries one; four fixtures citing it follow.
- **Folded work, I05:E03 W03.** The manifest schema's code catalogues gain `E_DISPATCH_CYCLE` and `E_HEADING_COLLISION` and lose `W_DISPATCH_CYCLE` and `W_DISPATCH_NOT_PROCEDURAL`, as the design declares.

## Held

- **Arising issue [#358](https://github.com/m2ux/prosiform/issues/358), placement held, since settled.** The user chose `<entry name>.bundles/`; #358 was placed as I05:E03 W05 and delivered by #359. A run folder named for its entry coincides with a same-named source directory beside it (`states.md` beside `states/`), so such a layout needs `-o`, and an unrelated directory of that name is replaced whole. Its fix chooses how the user-confirmed run folder is named, which is the user's decision. Recommended: place it as a new I05:E03 task ahead of W09, naming the folder `<entry name>.bundles/`.

## Deferred debt and arising issues

- **Deferred debt.** None. The duplicate-name overwrite found in review was trivial and fixed in the unit.
- **Arising.** #358, held above.
