# Test Results

Results for F24 at `c04551cfc` on `f24-guide-dispatch-reading`, run on 2026-11-19 in the unit checkout.

## T1 Guide Text

`fixtures/cli/informational-guide-response`: `pf` with no arguments exits 0 and prints, among its lines, "Read the bundle you were given and follow every instruction in it as", "handed a bundle follows it the same way, handing on each ⇉ and ⫽ link", "Where a ⇉ link points at a sub-section rather than at a bundle", "that line, are the bundle's brief: do what it asks of you before", "you hand over; what it states the bundle leaves or answers is the" and "⇉ lines.", the dispatch set and the dispatch pick described by their lines with no heading named. In `test_cli.py`, `test_the_guide_opens_on_following_a_bundle` holds that the guide opens "Following a bundle:" with the symbol grammar ahead of usage, and `test_the_guide_leaves_a_briefs_stated_work_to_the_sub_agent` holds the brief's condition and split. Held.

## T2 Specimen Dispatch on Haiku

The #809 specimen's arm A, the child's Contract as brief, run 8 times on Haiku 5.5 with `pf` installed from this branch at `c04551cfc`, each run one agent given the Tally bundle and its folder: all 8 handed Count the Words to a sub-agent, counted from each run's sub-agents. Under `pf` 0.27.0 the same arm dispatched in 4 of 8, and under this branch at `4d8b496e6`, before the brief's condition and the heading names were revised, in 7 of 8. Held: at least 7 of 8.

A full finding-classification trial on Haiku 5.5 against this branch's `pf` at `c04551cfc` dispatched every stage the slice draws: Investigate's Read the Home Graph and Measure the Reach, Measure the Reach's Probe the Component and Judge's three tests. Both trials under 0.27.0 ran Investigate's stages in its own context.

## T3 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2278 passed), harness (1122 passed), corpus (683 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
