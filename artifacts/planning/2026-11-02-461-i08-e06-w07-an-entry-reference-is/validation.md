# Validation

Evidence for the checks the work items [W07](w07.md) and [W10](w10.md) name, at branch `i08/e06/w07-an-entry-reference-is`.

## Corpus fixtures

- **AC10.** `fixtures/inclusion/an-entry-is-not-substituted`: `entry.md` declares `default: {subst: [{entry.md: stand-in.md}]}`. `pf entry.md` exits `0`, publishes `entry.bundles/entry.bundle.md` carrying `# Entry`, and warns `W_SUBST_UNUSED` with `source` `entry.md`.
- **AC14.** `fixtures/inclusion/a-pair-reached-only-outside-the-selection-is-unused`: `guide.md` holds `## Keep` and `## [¬ Rules](rules.md)` with `default: {subst: [{rules.md: stub.md}]}`. `pf 'guide.md#keep'` exits `0` and warns `W_SUBST_UNUSED` with `source` `rules.md`, and no `W_SUBST_USED`. Before the change the same run warned `W_SUBST_USED` with no location. `pf guide.md` on the same tree warns `W_SUBST_USED` at `guide.md:12:1`.
- `fixtures/mock/a-redirected-entry-derives-its-name-from-the-substitute` is withdrawn with the entry redirect.

## Unit tests

- `src/tests/test_cli.py`: an entry whose default preset names it compiles as named; `entry` returns the path the caller wrote.
- `src/tests/test_mock.py`: reading what a heading shows records no substitution; an unrecorded mapping answers as the mapping does; a pair reached only by a heading outside the selection is unused. The three fail without the `bundle.py` change. Five entry-redirect cases are removed with the capability.

## make check

`make check` with `PROSIFORM_BUILD` naming the worktree build: exit `0` at `8d035af71`.
