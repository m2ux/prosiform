# Test Results

Results for F21 at `fc9a56e77` on `f21-overcompiled-rubric`, cut from `main` at `4b0466803`, run on 2026-11-18 in the unit checkout with its `src/.venv/bin` first on `PATH`.

## T1 Rubric Beside the Scorer

`_held_to` in `evals/diagram-following/score.py` counts `overcompiled` for a run that is invalid usage, or that names an entry no stated run names with agreeing presets. Probes of `pf_runs` read:

- `pf` as the bare guide run, exempt; `pf --help` and `pf -v x.md` as informational, skipped.
- `pf -o .`, `pf --pick a`, `pf --pick x` as options with no entry; `pf x.md extra`, `pf --bogus a.md`, a pick on an entry carrying no `?`, a repeated `--pick`, and `pf --help --bogus` as refused: each invalid usage.
- `echo 'open`, `ls >` and `cat <<EOF` with no closing line as unsplittable: invalid usage whatever the first word.
- `pf -o out 'workflow.md#trace'` and `pf .` as runs naming a reference.

The RUNBOOK's `overcompiled` row states the unstated reference, the call with options but no entry, the refused entry or option, and the unsplittable command, each with its `miss`, `defect` and `unclear` conditions. The README's line states the unstated reference and the malformed call, counts an unsplittable command as one, and exempts a bare `pf` and an informational call the compiler accepts. Held.

## T2 Eval Harness

`make eval-harness`: 854 passed, 1 failed. The failure, `test_a_pick_stands_where_the_pick_token_stands`, is in the scorer's pick reading, which the change does not touch; it fails alike on `main` at `4b0466803`, whose `score.py` and `test_score.py` the branch carries unchanged. Arising issue [#804](https://github.com/m2ux/prosiform/issues/804). Held for the change.

## T3 Full Check

`make check`, with `PROSIFORM_BUILD` naming the unit checkout's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2270 passed), harness (1120 passed), corpus (681 fixtures, 681 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
