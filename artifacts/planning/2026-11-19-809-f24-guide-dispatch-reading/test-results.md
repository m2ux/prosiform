# Test Results

Results for F24 at `4d8b496e6` on `f24-guide-dispatch-reading`, run on 2026-11-19 in the unit checkout.

## T1 Guide Text

`fixtures/cli/informational-guide-response`: `pf` with no arguments exits 0 and prints, among its lines, "Read the bundle you were given and follow every instruction in it as", "handed a bundle follows it the same way, handing on each ⇉ and ⫽ link", "asks of you before you hand the bundle on. What it states the bundle", "takes is what you hand over; what it states the bundle leaves or" and "answers is the sub-agent's work". In `test_cli.py`, `test_the_guide_opens_on_following_a_bundle` holds that the guide opens "Following a bundle:" with the symbol grammar ahead of usage, and `test_the_guide_leaves_a_briefs_stated_work_to_the_sub_agent` holds the brief's split. Held.

## T2 Specimen Dispatch on Haiku

The #809 specimen's arm A, the child's Contract as brief, run 8 times on Haiku 5.5 with `pf` installed from this branch, each run one agent given the Tally bundle and its folder: 7 runs handed Count the Words to a sub-agent, counted from each run's sub-agents. The eighth followed the child bundle itself, answering that it held no dispatch tool, though one was listed to it. Under `pf` 0.27.0 the same arm dispatched in 4 of 8. Held: at least 7 of 8.

A full finding-classification trial on Haiku 5.5 against this branch's `pf` dispatched Read the Home Graph and Measure the Reach from Investigate, which it ran in its own context in both trials under 0.27.0; Measure the Reach followed its Probe the Component bundle itself.

## T3 Full Check

`make check`, with `PROSIFORM_BUILD` naming the worktree's `pf`, exits 0: lock, lint, format, typecheck, `make test` (2278 passed), harness (1122 passed), corpus (683 fixtures), smoke, layout, tables, links, vocabulary, invocation, conformance and independence. Held.
