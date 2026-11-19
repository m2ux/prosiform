# Test Results

Results for F26 at `f6dc70c62` on `f26-take-the-answer`, run on 2026-11-19 in the unit checkout.

## T1 Guide Text

`fixtures/cli/informational-guide-response`: `pf` with no arguments exits 0 and prints, among its lines, "yourself: hand on its link. Do not check or redo its work: take" and "its answer as given.". `test_the_guide_hands_a_bundle_over_by_the_path_of_its_file` in `test_cli.py` holds the sentence. Held.

## T2 Specimen Answer

The counting specimen, Tally dispatching Count the Lines dispatching Count the Words, each with its Contract as brief, run against a `pf` installed from this branch's guide; each run one agent given the Tally bundle and a folder holding a four-line `source.md`:

| Guide | Runs | Every level dispatched | Tally opened the child bundle first | Tally checked the counts after the answer | Tally recorded its own count |
| --- | --- | --- | --- | --- | --- |
| 0.28.1 | 5 | 5 | 4 | 4 | 1 |
| This branch | 6 | 6 | 3 | 2 | 0 |

All runs are Haiku 5.5. Held: every level dispatched in each of 6 runs, and no Tally recorded a count other than the one it was answered.

## T3 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2278 passed), harness (1122 passed), corpus (683 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
