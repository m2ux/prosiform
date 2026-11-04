# I10 Handoff (2026-11-04)

State for a fresh session resuming I10 delivery on board 18. Decisions live in [README.md](README.md#decisions); this file holds only where work stands.

## Done

- E01, E02, E03, E05, E06 Done.
- E04 W01-W12, W17, W18, W19 merged into `i10/e04/main` (W19 via #651; W19 and AC27 ticked on #579; review PR #622 Changes and References current).

## Active

- **E00 W04** ([record](../2026-11-03-403-i10-e00-w04-shake-down-the-baseline/)). Base `i10/e00/main` updated from main; task branch reconciled onto E06's compiled form. The shakedown rerun found #650; the user decided its four points (README Decisions, "Every form carries `pf`" onwards, and #650's Decisions). Nothing merged; AC10 unticked; #632 and #637 open.
  - Resumed 2026-11-04 in lane 1, agent `lane1_e00_w04`, on the existing reserved branch and record. Live board and issue reads confirm the reservation; the clean task branch is at `73df1825`, equal to its remote. Lane 2 waits for W04 because its next row, W00, depends on it.
  - Checkpoint: #650's four decisions pass the full `make check` at `f9d69cbb` (1,731 source tests, 1,355 harness tests and system checks). The Codex adapter candidate is pushed at `3c8ab4bc`, with 133 focused tests, lint and type checking passing. Both stopped-run directories are removed. AC10 tests wait as the registered `ac10-tests.patch` for completed measurements.
  - Harness decision (2026-11-04): automatic approval review rejected the Claude monitor before a paid session began. The user selects the Codex eval harness, then explicitly chooses `gpt-6.1-sol` at `medium` reasoning for the shakedown. Its isolated auth-only home is prepared at `/home/mike1/projects/eval/prosiform/config/codex`, with directory mode 700 and credential file mode 600. The existing runbook holds a harness reporting no dollar charge to its token budget; the native per-thread usage API may supply estimated USD and still needs verification.
  - Native probes: `codex-native-simple` ran `linear/straight-through/bundle` on the selected model. It recorded 44,543 tokens, with cumulative and raw-response totals equal, and an `unfinished` result triaged `miss`: the model tried to compile the already supplied bundle, received `E_TARGET_NOT_FOUND` and stopped. `codex-native-dispatch` recorded 65,102 tokens, with cumulative and raw totals equal, then was refused by the workspace-owner spend cap before any dispatch or state. The user confirmed the cap reset on 2026-11-04; the same lane 1 agent resumes the dispatch probe with a fresh id, preserving both records. Bootstrap and the full 76-cell shakedown follow valid native telemetry. Lane 2 remains blocked on W04.
  - Next: finish the Codex adapter and shakedown; set `DEFAULT_SESSION_BUDGET`, `EVAL_BUDGET_TOKENS` and README figures from its measurement; commit the AC10 tests; open the PR with verified Development links to #632, #637 and #650; merge into `i10/e00/main`, tick W04 and AC10 on #403, update #610 Changes and References only, and close the resolved defects. The user confirmed repository issue auto-close disabled on 2026-11-04.

## Next rows

- **E04 W16** (edge-run shakedown, lane 1): also restore the default matrix to the baseline workflows alone and `EVAL_BUDGET_TOKENS` to the baseline figure (W19 had raised it to 46 800 000 for 780 sessions), and add Claude to RUNBOOK's Edge Run harnesses. Then W14 (live edge run, lane 2), W15.
- **E00** W00, W02, W03 (lane 2), after W04.
- E04 and E00 integrations stop at ready; the user merges into `main`.

## Notes

- **Lanes.** Two delivery sessions run side by side, one sub-agent per unit, one unit per lane at a time; each row's lane is in its work item and in [Delivery Lanes](README.md#delivery-lanes). The user's assignments (2026-11-04) are `gpt-6.1-sol` at `max` reasoning for lane 1 and `gpt-6.1-sol` at `medium` reasoning for lane 2. When a lane frees, dispatch its next unblocked row by priority. Eval runs use the model the user chooses; never name it in plans.
- A compiled workspace now holds the compiled sources beside the bundle set (W19), since a `↳` line compiles from sources.
- The orchestrator merges task PRs into epic bases when the classifier refuses an agent's merge, after reviewing the diff, CI and an org-leak check.
