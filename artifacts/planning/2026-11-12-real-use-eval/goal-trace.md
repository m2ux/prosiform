# Goal Trace

## Trace

| Goal clause | Initiative criteria | Epics | Epic criteria | Source requirement |
| --- | --- | --- | --- | --- |
| A session starts from a skill placed where its CLI discovers skills | AC1 | E00, E01 | E00 AC1, AC2; E01 AC1–AC5 | Decisions 1, 3, 4, 11, 16 and 18 |
| The session opens with its task in plain words | AC2 | E00, E01 | E00 AC4, AC5; E01 AC6 | Decisions 2, 9 and 17 |
| The CLI's own skill mechanism is the only disclosure; the eval adds nothing | AC2 | E00 | E00 AC3, AC4 | Decisions 1, 8 and 9 |
| A bare prompt naming an entry file is not an eval | AC2, AC4 | E01, E02 | E01 AC6; E02 AC1 | Decisions 5 and 10 |
| The comparisons stay, each behind a skill | AC3 | E01 | E01 AC1–AC5 | Decision 3 |
| One baseline is measured on the skill-entry eval, over every workflow | AC5 | E02 | E02 AC2, AC3, AC4 | Decisions 5, 14, 19, 20 and 21 |

The marked source is the record's [decisions](decisions.md), Confirmed 1 to 21.

## Gaps

Ranked; the flagged ones most threaten the goal.

1. **Resolved.** The tracing duty had no home; decision 9 puts it in a paragraph every variant's `SKILL.md` shares, E00 W03 writes it and E00 AC5 holds it (decision 17).
2. **Resolved.** Retiring the bare-prompt path in E00 left families unrun; decision 10 moves it to E01 W06, after every family row.
3. **Resolved.** E01 AC4 names all four composition workflows E01 W04 converts (decision 16).
4. **Flagged: discovery depends on harness flags.** The Claude harness disables skills today; E00 AC3 holds the change, and a host-managed configuration still reaches sessions, recorded by count and fingerprint as the README states.
5. **Flagged: the eval runs mixed while E01 is open.** Converted families run as skills and the rest on bare prompts; a run in that window is no baseline, and E02 starts only after E01 W06.
6. **Noted: the cross-initiative edges.** The agent-pick remeasurement waits on E02 W03 (decision 13), and E02 W04 waits on I15's first-run scorer (decision 21).

## Outside Threats

- **Readers of the changed surface.** `make eval-harness` and the `checks.yml` dispatch run the eval's tests; `report.py` reads `baseline.json` and reads `—` with none, so E02 W01 leaves it working before W04 writes the new one.
- **Fail-closed paths.** After E01 W06 the corpus test refuses a workflow with no skill texts, so no workflow silently drops out of the matrix.
- **Instrument independence.** The baseline is fixed by E02 W04 after E01 lands and after the scorer accepts a first-run `--pick`, and the scorer, not the harness, decides each verdict.
- **Ground shift.** I15's `?` pick and guide land on main through I15; the deferral row converts `agent-pick` as it stands when E01 starts.

## Checks

- Format: the initiative and the three epics report nothing to fix, apply or decide.
- Dependencies: no problems; every candidate unit is named on a record line in [decisions](decisions.md#joins), and E02 W01 with W04 is split by rule.
