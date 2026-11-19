# Test Results

Results for F25 at `982c333d1` on `f25-hand-on-unread`, run on 2026-11-19 in the unit checkout.

## T1 Guide Text

`fixtures/cli/informational-guide-response`: `pf` with no arguments exits 0 and prints, among its lines, "given, and continue with its answer. Do not open the bundle" and "yourself: hand on its link.". `test_the_guide_hands_a_bundle_over_by_the_path_of_its_file` in `test_cli.py` holds the sentence. Held.

## T2 Specimen Pre-opening

The #809 specimen's arm A run against a `pf` built from this branch's guide, each run one agent given the Tally bundle and its folder; a run pre-opens where a tool call other than its final report reads `count-the-words.bundle.md` before its first dispatch:

| Model | Runs | Pre-opened | Dispatch attempted |
| --- | --- | --- | --- |
| Haiku 5.5 | 8 | 1 | 7 |
| Opus 5.5 | 4 | 0 | 4 |

Three Haiku attempts were refused by the harness's concurrent sub-agent limit, twelve runs having started at once. Under the 0.28.0 guide the same arm pre-opened in 5 of 8 Haiku runs. Held: at most 1 of 8.

## T3 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2278 passed), harness (1122 passed), corpus (683 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
