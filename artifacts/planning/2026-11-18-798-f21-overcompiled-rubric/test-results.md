# Test Results

Results for F21 at `fb06ad50f` on `f21-overcompiled-rubric`, cut from `main` at `4b0466803`, run on 2026-11-18 in the unit checkout with its `src/.venv/bin` first on `PATH`.

## T1 Rubric Beside the Scorer

`_held_to` in `evals/diagram-following/score.py` counts `overcompiled` for a run that is invalid usage, or that names an entry no stated run names with agreeing presets. Probes of `pf_runs` read:

- `pf` as the bare guide run, exempt; `pf --help` and `pf -v x.md` as informational, skipped.
- `pf -o .` and `pf --pick x` as options with no entry; `pf x.md extra`, `pf --bogus a.md`, a pick on an entry carrying no `?`, a repeated `--pick`, and `pf --help --bogus` as refused: each invalid usage.
- `pf target.md 'unterminated` and `pf target.md <<EOF` with no closing line as a `pf` call that does not split whole: invalid usage. `ls >`, `echo 'open` and `cat <<EOF` with no closing line: no run.
- `pf -o out 'workflow.md#trace'` and `pf .` as runs naming a reference.

The RUNBOOK's `overcompiled` row states the unstated reference, the call with options but no entry, the refused entry or option, and the `pf` call whose words cannot be split, each with its `miss`, `defect` and `unclear` conditions. The README's line states the unstated reference and those malformed calls, and exempts a bare `pf` and an informational call the compiler accepts. Held.

## T2 Full Check

`make check`, with `PROSIFORM_BUILD` naming the unit checkout's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2270 passed), harness (1120 passed), corpus (681 fixtures, 681 pass), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.

## T3 Eval Harness

`make eval-harness` exits 0: 858 passed, `test_a_pick_stands_where_the_pick_token_stands` among them. `pf '[Target](target.md "checks,?")' --pick Draft` reads as `{checks, draft}`, and the listing, the link with no pick, keeps `?`. Held.

## T4 Malformed Command Running No pf

`test_a_malformed_command_running_no_pf_passes_the_run_checks` in `test_score.py`: `pf a.md` beside `ls >`, `echo 'open` or an unclosed `cat` heredoc, as separate commands and in one command string, reads as the one run `a.md`, and a scenario stating it passes the run checks. `main` at `4b0466803` fails each with `overcompiled`. Held.

## T5 Docstring and Run Checks

The `score.py` docstring states a run as a `pf` command in each segment `;`, `&&`, `||`, `|`, `&` or a newline separate; a refused run, a stray or repeated `--pick`, or one in a segment that does not split whole as malformed; and `overcompiled` for a run naming an unstated reference or a malformed run. The README's Run checks section names the same separators and malformed commands. Both match `SHELL_TOKEN`'s `separator` group, `pf_runs` and `_held_to`. Held.
