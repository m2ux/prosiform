# Validation

Evidence for the checks the [work item](w01.md) names, at branch `i08/e06/w01-the-preset-subst-read`.

## Corpus fixture

`fixtures/inclusion/a-preset-states-the-pair`: `guide.md` declares `default: {subst: [{rules.md: stub.md}]}` and its `## Keep` section links `rules.md`. `pf guide.md` exits `0`, publishes `stub.md` under `# Stub` in place of `rules.md`, and warns `W_SUBST_USED` with `source` `rules.md`, `resolved` `stub.md` at `guide.md:10:1`.

The same tree with `prosiform: {}` and `pf -m rules.md=stub.md guide.md` publishes a byte-identical bundle, so the preset compiles the substitute the option's pair compiled.

`make corpus`: 434 fixtures, 434 pass. `fixtures/inclusion/default-applies-in-every-section` now expects the `W_SUBST_UNUSED` its selected `Checks` pair raises, since that pair is in force and no link of `rules.md` names `notes.md`.

## Unit tests

`src/tests/test_mock.py`: a document's pair redirects the links it writes and no other document's; it holds over a run key for its own links; it records to the run's record; a default pair publishes the substitute and states it; a selected preset's pair holds over `default`'s; a document under no `subst` compiles as authored; an unused pair warns naming its document; two titles selecting disagreeing pairs exit `2`; an alternative naming no Markdown document exits `2`.

## make check

`make check` with `PROSIFORM_BUILD` naming the worktree build: exit `0` at `53243d787`.
