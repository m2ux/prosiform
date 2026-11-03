# I10 Handoff (2026-11-03)

State for a fresh session resuming I10 delivery on board 18. Decisions live in [README.md](README.md#decisions); this file holds only where work stands.

## Done

- E01, E02, E03, E05, E06 Done.
- E04 W01-W12, W17, W18, W19 merged into `i10/e04/main` (W19 via #651; W19 and AC27 ticked on #579; review PR #622 Changes and References current).

## Stopped

- **E00 W04** ([record](../2026-11-03-403-i10-e00-w04-shake-down-the-baseline/)). Base `i10/e00/main` updated from main; task branch reconciled onto E06's compiled form. The shakedown rerun found #650; the user decided its four points (README Decisions, "Every form carries `pf`" onwards, and #650's Decisions). Nothing merged; AC10 unticked; #632 and #637 open.
  - Next: apply #650's decisions on the W04 branch; remove `results/baseline-shakedown` and `/home/mike1/projects/eval/prosiform/workspaces/baseline-shakedown`; rerun the shakedown on claude, the model the user named (USD 5 cap); set `DEFAULT_SESSION_BUDGET`, `EVAL_BUDGET_TOKENS` and the README figure from it; commit the AC10 tests (patch was in the old session scratchpad, rewrite if missing); open the PR linking #632 and #637, merge into `i10/e00/main`, tick W04 and AC10 on #403, update #610 Changes and References only, close #632 and #637.

## Next rows

- **E04 W16** (edge-run shakedown, lane 1): also restore the default matrix to the baseline workflows alone and `EVAL_BUDGET_TOKENS` to the baseline figure (W19 had raised it to 46 800 000 for 780 sessions), and add Claude to RUNBOOK's Edge Run harnesses. Then W14 (live edge run, lane 2), W15.
- **E00** W00, W02, W03 (lane 2), after W04.
- E04 and E00 integrations stop at ready; the user merges into `main`.

## Notes

- A compiled workspace now holds the compiled sources beside the bundle set (W19), since a `↳` line compiles from sources.
- The orchestrator merges task PRs into epic bases when the classifier refuses an agent's merge, after reviewing the diff, CI and an org-leak check.
