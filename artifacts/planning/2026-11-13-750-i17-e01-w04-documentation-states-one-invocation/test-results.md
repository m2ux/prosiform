# Test Results

Results for W04 at `5d3293729` on `i17/e01/w04-documentation-states-one-invocation-main`, run on 2026-11-13 with `PROSIFORM_BUILD` naming the worktree's `pf` through `uv run --project src --frozen pf`.

## T1 No Presets Option

`git grep -n -- '--presets' README.md docs` prints nothing, and `git grep -n 17c1f6e2f` prints nothing: every `docs/` design link names `005b0ff1d`. Held.

## T2 One Invocation Instruction

A read of the pages:

- `README.md` Usage runs a published link as written, quoted as one argument, from the directory `pf` compiled the bundle in; adds `--pick` when the title carries `?`; names a plain path as the bootstrap entry; ignores operator marks.
- `docs/selection.md` states that an entry selects as its link does, that an entry picks by its title or by `--pick` beside the pick token, and that the listing's remedy reruns the same link with `--pick`.
- `docs/references.md` states that the link the agent runs as written carries the pick token, with `--pick` beside it naming the alternative.
- `docs/glossary.md` states the guide's two compile forms, the link entry in the preset, pick and entry reference rows, and the deferred `↳` line a later run takes as written.

Held.

## T3 Preset Alternatives Body

`gh api repos/m2ux/prosiform/issues/707 --jq .body | grep -c -- '--presets'` prints `0`. The Proposal's deferral bullet states the pick passing with `--pick` beside the link as written, and R5 cites I17. Held.

## T4 Links

`make links` (`checks/links.py --online`) passes, the `005b0ff1d` design links among the repository links it resolves. Held.

## T5 Full Check

`make check` passes: lock-check, lint, format, typecheck, `make test` (2128 passed), harness (1054 passed), corpus (615 fixtures pass), smoke, layout, tables, links, vocabulary, invocation (29 statements), conformance and independence. The first run failed `checks/tests/test_authoring.py::test_focused_deferred_command_uses_the_current_grammar`, which read `docs/composition.md`'s activation command as a plain path; the test now holds that command to the generated `↳` line run as written. Held.
