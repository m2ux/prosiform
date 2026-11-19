# Test Results

Results for F29 at `817d13db2` on `f29-guide-hand-off-alone`, run on 2026-11-19 in the unit checkout.

## T1 Guide Text

`fixtures/cli/informational-guide-response`: `pf` with no arguments exits 0 and prints, among its lines, "Hand over the path and those inputs alone:" and "add no instruction, framing or reply form.". `test_cli.py` holds the sentence among the dispatch rules. Held.

## T2 Specimen Hand-Off

The hand-off specimen: `survey.md` hands its folder to `[⇉ Tally](tally.md)`, whose Contract is its brief, and writes a summary from Tally's answer. Compiled once and run with each build installed; each run one agent given the Survey bundle and a folder holding `source.md`:

| Guide | Runs | Hand-off is the path and the folder alone | Hand-off adds a direction |
| --- | --- | --- | --- |
| 0.29.1 | 3 | 0 | 3 |
| This branch | 3 | 3 | 0 |

All runs are Haiku 5.5, and every Tally answered with its answer line alone. Held: each hand-off under this branch was the bundle's path and the folder.

## T3 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2282 passed), harness (1124 passed), corpus (685 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
